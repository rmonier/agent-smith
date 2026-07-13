---
type: "source-file"
title: ".agents/skills/agent-ready-context/scripts/prune_okf_orphans.py"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/agent-ready-context/scripts/prune_okf_orphans.py"
source_path: ".agents/skills/agent-ready-context/scripts/prune_okf_orphans.py"
source_kind: "code"
source_hash: "sha256:dd1492aed62fcab7d114010a3eaabeff7ebbb66f9023df9244cb98b48cd0334c"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, code]
---

# .agents/skills/agent-ready-context/scripts/prune_okf_orphans.py

~~~
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Reconcile the OpenKB registry with the repository: retract orphaned sources.

When a repository source file is deleted (or a whole bundled directory is
removed), the document it produced stays in the KB: its `okf/raw/` copy,
`okf/wiki/summaries|sources/` pages, and any `concepts/`/`entities/` pages it
seeded all linger, and `hashes.json` still claims it is ingested. Nothing in
the normal `build pack -> openkb add` cycle heals this, because `add` only ever
adds — deletion has no inverse there.

`openkb remove` is that inverse, and it is the one OpenKB mutation that is
fully deterministic (frontmatter/`sources:` pruning + a scoped `lint --fix`,
**no LLM call**). That is what makes it safe for a script to drive: this is the
single sanctioned place where the pipeline calls `openkb` directly instead of
staging input for the LLM compiler.

Default is report-only (no `openkb` call, no mutation). `--preview` shows
OpenKB's own per-page plan via `remove --dry-run`. `--apply` executes the
retraction. A document the pipeline never created (e.g. a user's manually
`openkb add`-ed PDF, whose registry `path` does not point under the staging
dir) is never a candidate — deletion reconciliation only ever touches sources
this pipeline owns.

Mirror `build_okf_source_pack.py`: the selection/slug/bundle logic here must
match the builder, or the two will disagree about which document a repo file
maps to. When the freshly built manifest is present it is used verbatim (no
re-derivation); the git-derivation below is the fallback for a manifest-less
reconcile (e.g. a fresh clone).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

COMMIT_HASH_RE = re.compile(r"[0-9a-f]{40}")

# Pseudo-documents the builder always regenerates; they have no repo file
# behind them and must never be treated as orphans.
PSEUDO_DOC_NAMES = {"repo-snapshot", "graphify-report"}

# Marker that identifies a registry entry as produced by this pipeline's
# staging step. User-added external documents carry a different ingest path.
STAGING_MARKER = ".okf-build/input"


def run(cmd: list[str], cwd: pathlib.Path) -> str | None:
    try:
        return subprocess.check_output(
            cmd, cwd=cwd, text=True, encoding="utf-8", errors="replace", stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return None


# --- pure helpers mirrored from build_okf_source_pack.py -------------------
# KEEP IN SYNC with the builder (standalone scripts cannot import each other).
# Exercised only on the manifest-less fallback path; the ADVISORY cross-check
# in detect_orphans() reports when the two disagree.

def safe_slug(path: str) -> str:
    return path.replace("/", "__").replace("\\", "__")


def normalize_text(raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def should_skip(rel: str) -> bool:
    rel_posix = rel.replace("\\", "/")
    if rel_posix.startswith(("okf/", "okf/.okf-build/")):
        return True
    if rel_posix.startswith("graphify-out/"):
        return True
    parts = rel_posix.split("/")
    transient = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv"}
    return any(part in transient for part in parts)


def should_select(rel: str) -> bool:
    rel_posix = rel.replace("\\", "/")
    important_tokens = (
        "README", "README.", "docs/", ".github/workflows/", ".gitlab-ci", "Dockerfile",
        "docker-compose", "compose", "helmfile", "Chart.yaml", "values", ".tf",
        "pyproject.toml", "package.json", "uv.lock", "go.mod",
        "Cargo.toml", "Makefile", "src/", ".agents/skills/",
    )
    return rel_posix.startswith(important_tokens) or any(token in rel_posix for token in important_tokens)


def bundle_key(rel: str, depth: int) -> str:
    parts = rel.replace("\\", "/").split("/")
    return "/".join(parts[: min(depth, len(parts) - 1)]) or "root-files"


# --- repository + registry state -------------------------------------------

def git_tracked(repo: pathlib.Path) -> list[str]:
    out = run(["git", "-c", "core.quotepath=false", "ls-files"], repo)
    return sorted(out.splitlines()) if out else []


def _git_blob_bytes(repo: pathlib.Path, ref_path: str) -> bytes | None:
    """Raw bytes of ``git show <ref_path>`` (byte-exact; text mode would strip
    the trailing newline and break content hashing). None on any failure."""
    try:
        return subprocess.check_output(
            ["git", "show", ref_path], cwd=repo, stderr=subprocess.DEVNULL
        )
    except Exception:
        return None


def git_blob_content_hash(repo: pathlib.Path, rel: str) -> str | None:
    """Content hash of the last committed version of a now-absent path.

    Used only to tell a rename/move (same content resurfacing under a new path)
    apart from a true deletion. A ``git mv`` is recorded as delete+add, so the
    deleting commit's parent still holds the content. Tries HEAD first (a
    staged-but-uncommitted deletion still has it there), then the parent of the
    commit that removed it. Returns None when nothing committed matches, so the
    caller falls back to deletion semantics.
    """
    blob = _git_blob_bytes(repo, f"HEAD:{rel}")
    if blob is None:
        commit = run(["git", "log", "--diff-filter=D", "-1", "--format=%H", "--", rel], repo)
        if not commit:
            return None
        commit = commit.splitlines()[0]
        if not COMMIT_HASH_RE.fullmatch(commit):
            return None
        blob = _git_blob_bytes(repo, f"{commit}^:{rel}")
    if blob is None:
        return None
    return sha256_text(normalize_text(blob))


def load_registry(kb_dir: pathlib.Path) -> dict[str, dict]:
    reg_path = kb_dir / ".openkb" / "hashes.json"
    if not reg_path.exists():
        return {}
    try:
        data = json.loads(reg_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def is_pipeline_owned(meta: dict) -> bool:
    path = str(meta.get("path", "")).replace("\\", "/")
    return STAGING_MARKER in path


SOURCE_PATH_RE = re.compile(r'^source_path:\s*"(.*)"\s*$', re.MULTILINE)


def source_path_from_raw(kb_dir: pathlib.Path, meta: dict) -> str | None:
    """Original repository path, read from the orphan's ``okf/raw/`` copy.

    The raw copy is the verbatim staged input file, so the builder's
    ``source_path`` frontmatter field is authoritative — unlike un-slugging the
    staged name, it survives paths whose segments contain ``__`` (e.g.
    ``src/pkg/__init__.py``, whose slug round-trips to garbage). Returns None
    when the raw copy or the field is missing (legacy entries, ``--keep-raw``
    cleanups), letting the caller fall back to slug reversal.
    """
    raw_rel = meta.get("raw_path")
    if not raw_rel:
        return None
    raw_file = kb_dir / str(raw_rel)
    if not raw_file.is_file():
        return None
    try:
        head = raw_file.read_text(encoding="utf-8", errors="replace")[:4096]
    except Exception:
        return None
    match = SOURCE_PATH_RE.search(head)
    return match.group(1) if match else None


def reverse_name_to_rel(name: str) -> str:
    """Fallback inverse of ``safe_slug(rel) + '.md'`` (the staged file name).

    Only used when :func:`source_path_from_raw` cannot answer. Reverses
    ``__`` -> ``/`` and drops the extension the builder appended — wrong for
    paths whose segments themselves contain ``__``, which is exactly why the
    raw-frontmatter lookup is preferred: a wrong reverse here can only
    misclassify an orphan's *reason* (deleted vs deselected/renamed), never
    invent an orphan.
    """
    stem = name[:-3] if name.endswith(".md") else name
    return stem.replace("__", "/")


def rel_exists_tracked(rel: str, tracked: set[str]) -> bool:
    """True when ``rel`` is a tracked file, or a directory prefix of one
    (bundle documents' ``source_path`` is a directory key, not a file)."""
    return rel in tracked or any(t.startswith(rel + "/") for t in tracked)


# --- current expected document names ---------------------------------------

def names_from_manifest(manifest_path: pathlib.Path) -> tuple[set[str], dict[str, str], bool] | None:
    """Return (expected staged names, content_hash->source_path, is_bundled).

    Prefers the freshly built manifest so this script and the builder cannot
    drift on selection/slug rules. Returns None when the manifest is absent.
    """
    if not manifest_path.exists():
        return None
    try:
        items = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(items, list):
        return None
    names: set[str] = set()
    hash_to_path: dict[str, str] = {}
    bundled = False
    for item in items:
        staged = str(item.get("staged_path", ""))
        if staged:
            names.add(pathlib.PurePosixPath(staged.replace("\\", "/")).name)
        src_hash = item.get("source_hash")
        src_path = item.get("source_path")
        if src_hash and src_path:
            hash_to_path[src_hash] = src_path
        if item.get("origin") == "repo-bundle":
            bundled = True
    return names, hash_to_path, bundled


def names_from_git(repo: pathlib.Path, bundle_depth: int) -> tuple[set[str], dict[str, str]]:
    """Fallback: re-derive expected staged names directly from the repo."""
    selected = [f for f in git_tracked(repo) if not should_skip(f) and should_select(f)]
    names: set[str] = {"repo-snapshot.md", "graphify-report.md"}
    hash_to_path: dict[str, str] = {}
    if bundle_depth > 0:
        keys = {bundle_key(rel, bundle_depth) for rel in selected}
        for key in keys:
            names.add(f"{safe_slug(key)}.md")
    else:
        for rel in selected:
            names.add(f"{safe_slug(rel)}.md")
            src = repo / rel
            if src.is_file():
                try:
                    hash_to_path[sha256_text(normalize_text(src.read_bytes()))] = rel
                except Exception:
                    pass
    return names, hash_to_path


# --- detection --------------------------------------------------------------

def detect_orphans(
    repo: pathlib.Path,
    kb_dir: pathlib.Path,
    bundle_depth: int,
    manifest_path: pathlib.Path,
) -> tuple[list[dict], int, dict]:
    """Return (orphans, owned_count, diagnostics).

    An orphan is a pipeline-owned, non-pseudo registry document whose staged
    name is not among the names the current repository would stage.
    """
    registry = load_registry(kb_dir)
    owned = {
        h: m
        for h, m in registry.items()
        if is_pipeline_owned(m) and m.get("doc_name") not in PSEUDO_DOC_NAMES
    }

    manifest = names_from_manifest(manifest_path)
    if manifest is not None:
        expected_names, hash_to_new_path, bundled = manifest
        source = "manifest"
        # Freshness/drift cross-check: the manifest is authority, but if the
        # names it lists differ from what the current repository would stage,
        # either the pack is stale (recent deletions invisible to this run) or
        # the selection helpers mirrored below drifted from the builder's.
        # Skipped for bundled packs unless the matching --bundle-depth was
        # given, since per-file derivation can't reproduce bundle names.
        if not bundled or bundle_depth > 0:
            git_names, _ = names_from_git(repo, bundle_depth)
            pseudo_names = {f"{p}.md" for p in PSEUDO_DOC_NAMES}
            if (git_names - pseudo_names) != (expected_names - pseudo_names):
                only_manifest = len(expected_names - git_names - pseudo_names)
                only_repo = len(git_names - expected_names - pseudo_names)
                print(
                    f"ADVISORY: manifest and current repository disagree on staged names "
                    f"({only_manifest} only in manifest, {only_repo} only in repo). Either the "
                    "source pack is stale - rebuild it first, or orphan detection may miss "
                    "recent deletions - or this script's selection rules drifted from "
                    "build_okf_source_pack.py. Proceeding with the manifest as authority.",
                    file=sys.stderr,
                )
    else:
        expected_names, hash_to_new_path = names_from_git(repo, bundle_depth)
        source = "git"

    # Names the KB does not yet have -> documents the next/just-run add creates.
    registry_names = {str(m.get("name", "")) for m in registry.values()}
    new_hash_to_path = {h: p for h, p in hash_to_new_path.items()}

    tracked = set(git_tracked(repo))
    orphans: list[dict] = []
    for _h, meta in owned.items():
        name = str(meta.get("name", ""))
        doc_name = str(meta.get("doc_name") or "")
        if name in expected_names:
            continue  # still a current source

        rel = source_path_from_raw(kb_dir, meta) or reverse_name_to_rel(name)
        file_exists = rel_exists_tracked(rel, tracked)

        reason = "deselected" if file_exists else "deleted"
        new_path = None
        keep_empty = False
        if not file_exists:
            old_hash = git_blob_content_hash(repo, rel)
            if old_hash and old_hash in new_hash_to_path:
                reason = "renamed"
                new_path = new_hash_to_path[old_hash]
                keep_empty = True  # the new doc repopulates shared pages

        orphans.append(
            {
                "doc_name": doc_name,
                "name": name,
                "rel": rel,
                "reason": reason,
                "new_path": new_path,
                "keep_empty": keep_empty,
            }
        )

    orphans.sort(key=lambda o: (o["reason"], o["doc_name"]))
    diagnostics = {
        "expected_source": source,
        "expected_count": len(expected_names),
        "registry_intersection": len(registry_names & expected_names),
    }
    return orphans, len(owned), diagnostics


# --- reporting + execution --------------------------------------------------

def remove_command(kb_dir_arg: str, o: dict, *, apply: bool) -> list[str]:
    cmd = ["openkb", "--kb-dir", kb_dir_arg, "remove", o["doc_name"]]
    if o["keep_empty"]:
        cmd.append("--keep-empty")
    cmd += ["--yes"] if apply else ["--dry-run"]
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Retract KB documents whose repository source no longer exists."
    )
    parser.add_argument("--repo", default=".")
    parser.add_argument("--kb-dir", default="okf", help="KB root passed to openkb --kb-dir.")
    parser.add_argument(
        "--bundle-depth", type=int, default=0,
        help="Must match the depth the source pack was built with (fallback path only).",
    )
    parser.add_argument("--manifest", default="okf/.okf-build/manifests/source-pack-manifest.json")
    parser.add_argument("--preview", action="store_true", help="Run 'openkb remove --dry-run' per orphan to show the page-level plan.")
    parser.add_argument("--apply", action="store_true", help="Execute the retraction with 'openkb remove --yes'.")
    parser.add_argument("--yes", action="store_true", help="With --apply, skip the confirmation gate.")
    parser.add_argument("--force", action="store_true", help="Override the mass-orphan / mode-change safety guard.")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    kb_dir = (repo / args.kb_dir).resolve() if not pathlib.Path(args.kb_dir).is_absolute() else pathlib.Path(args.kb_dir)
    manifest_path = (repo / args.manifest).resolve() if not pathlib.Path(args.manifest).is_absolute() else pathlib.Path(args.manifest)

    if not (kb_dir / ".openkb" / "hashes.json").exists():
        print(f"No registry at {kb_dir / '.openkb' / 'hashes.json'} - nothing to reconcile.")
        return 0

    orphans, owned_count, diag = detect_orphans(repo, kb_dir, args.bundle_depth, manifest_path)

    if not orphans:
        print(f"No orphaned documents. ({owned_count} pipeline-owned docs, "
              f"expected names from {diag['expected_source']}.)")
        return 0

    removable = [o for o in orphans if o["reason"] in ("deleted", "renamed")]
    deselected = [o for o in orphans if o["reason"] == "deselected"]

    # Safety guard: a bundle-depth change or a wrong invocation makes nearly the
    # whole registry look orphaned. Refuse to auto-apply in that case (loud,
    # like the source-pack self-reference guard), detection still reported.
    guard_tripped = owned_count > 0 and (
        len(removable) > max(5, int(0.40 * owned_count))
        or (diag["expected_count"] > 0 and diag["registry_intersection"] < 0.10 * owned_count)
    )

    print(f"Orphan reconciliation ({owned_count} pipeline-owned docs; "
          f"expected names from {diag['expected_source']}):")
    print("")
    for o in orphans:
        tag = {"deleted": "DELETED ", "renamed": "RENAMED ", "deselected": "DESELECT"}[o["reason"]]
        detail = f"source gone: {o['rel']}"
        if o["reason"] == "renamed":
            detail = f"moved: {o['rel']} -> {o['new_path']}  (remove old with --keep-empty)"
        elif o["reason"] == "deselected":
            detail = f"file still tracked but no longer selected: {o['rel']}"
        print(f"  {tag}  {o['doc_name']}")
        print(f"            {detail}")
    print("")

    if deselected:
        print(f"{len(deselected)} document(s) map to files that still exist but are no longer "
              "selected. These are NOT auto-retracted: confirm a selection-policy change was "
              "intended, then remove them explicitly if so.")
        print("")

    if guard_tripped and not args.force:
        print("SAFETY GUARD: the orphan set is too large to be routine deletions - this usually "
              "means --bundle-depth does not match how the pack was built, or the wrong KB/repo "
              "was targeted. Refusing to --apply. Re-check the invocation; pass --force only if "
              "you have verified every listed retraction is intended.")
        return 3

    if not removable:
        return 0

    if args.preview:
        print("Per-orphan OpenKB plan (dry-run):")
        for o in removable:
            cmd = remove_command(args.kb_dir, o, apply=False)
            print(f"$ {' '.join(cmd)}")
            out = run(cmd, repo)
            print(out if out is not None else "  (openkb unavailable or errored)")
        print("")

    if not args.apply:
        print("Report only. To retract, re-run with --apply. Commands that would run:")
        for o in removable:
            print(f"  {' '.join(remove_command(args.kb_dir, o, apply=True))}")
        return 0

    if not args.yes:
        print(f"About to retract {len(removable)} document(s) with 'openkb remove --yes'. "
              "Re-run with --yes to proceed non-interactively.")
        return 0

    failures = 0
    for o in removable:
        cmd = remove_command(args.kb_dir, o, apply=True)
        print(f"$ {' '.join(cmd)}")
        out = run(cmd, repo)
        if out is None:
            print("  FAILED (openkb unavailable or errored)")
            failures += 1
        else:
            print(out)
    print("")
    print(f"Retracted {len(removable) - failures}/{len(removable)} document(s).")
    if failures:
        print("Re-run to retry failures; 'openkb remove' is idempotent and safe to repeat.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~
