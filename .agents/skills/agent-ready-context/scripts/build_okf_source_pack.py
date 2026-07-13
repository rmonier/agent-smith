#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Build deterministic OpenKB-compatible staged input from a Git repository."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

HEADING_DATE_RE = re.compile(r"\s*\(\d{4}-\d{2}-\d{2}\)\s*$")
COMMIT_HASH_RE = re.compile(r"[0-9a-f]{40}")


def run(cmd: list[str], cwd: pathlib.Path) -> str:
    return subprocess.check_output(
        cmd, cwd=cwd, text=True, encoding="utf-8", errors="replace", stderr=subprocess.DEVNULL
    ).strip()


def last_touch_commits(repo: pathlib.Path) -> dict[str, str]:
    """Map each path to the newest commit that touched it.

    Staged frontmatter must not embed the current HEAD: OpenKB dedupes by
    SHA-256 over staged file bytes, so a HEAD stamp would re-ingest (and
    re-compile) the whole pack after every commit. The last-touch commit
    only changes when the file itself changes, which is exactly when the
    staged bytes change anyway.
    """
    try:
        out = run(["git", "-c", "core.quotepath=false", "log", "--name-only", "--pretty=format:%H"], repo)
    except Exception:
        return {}
    mapping: dict[str, str] = {}
    current = ""
    for line in out.splitlines():
        if COMMIT_HASH_RE.fullmatch(line):
            current = line
        elif line and current and line not in mapping:
            mapping[line] = current
    return mapping


def safe_slug(path: str) -> str:
    return path.replace("/", "__").replace("\\", "__")


def resolve_under(repo: pathlib.Path, value: str) -> pathlib.Path:
    path = pathlib.Path(value)
    return path if path.is_absolute() else repo / path


def normalize_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def json_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def source_kind(rel: str) -> str:
    suffix = pathlib.Path(rel).suffix.lower()
    if suffix in {".md", ".markdown", ".mdx", ".rst", ".adoc"}:
        return "markdown"
    if suffix in {".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"}:
        return "text"
    if suffix in {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".kt", ".cs", ".cpp", ".c",
        ".h", ".hpp", ".rb", ".php", ".sh", ".ps1", ".sql", ".tf", ".tfvars", ".Dockerfile",
    }:
        return "code"
    if pathlib.Path(rel).name in {"Dockerfile", "Makefile"}:
        return "code"
    return "other"


# should_skip/should_select/safe_slug and the bundle-key derivation are
# mirrored in prune_okf_orphans.py (manifest-less fallback) - keep them in sync.
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


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8", newline="\n")


def frontmatter(fields: dict[str, str], tags: list[str]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {json_string(value)}")
    lines.append("tags: [" + ", ".join(tags) + "]")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _prose_boundary(prev: str, line: str) -> bool:
    return line.startswith("#")


def _code_boundary(prev: str, line: str) -> bool:
    # Purely layout-based, language-agnostic: a non-blank line at column 0
    # right after a blank line. This is a paragraph break in source-code
    # layout, NOT syntax awareness - never extend this with per-language
    # keyword matching; the splitter must stay a text partitioner, not a
    # syntax checker. Wrong guesses only shift a part boundary, never lose
    # content.
    return bool(line) and not line[0].isspace() and not prev.strip()


def split_source(lines: list[str], budget: int, boundary) -> list[list[str]]:
    """Deterministic split of an oversized source into full-content parts.

    Cropping a concept source silently loses whatever knowledge lives past
    the budget, so it is split instead of truncated. A part closes at the
    first ``boundary`` line once past ``budget`` (headings for prose,
    top-level construct starts for code), or at a hard stop of ``2 * budget``
    when no boundary shows up.
    """
    parts: list[list[str]] = []
    current: list[str] = []
    prev = ""
    for line in lines:
        if current and len(current) >= budget and (boundary(prev, line) or len(current) >= 2 * budget):
            parts.append(current)
            current = []
        current.append(line)
        prev = line
    if current:
        parts.append(current)
    return parts


def strip_generated_timestamp_lines(text: str) -> str:
    """Drop run-dependent lines so unchanged reports stage to identical hashes.

    Graphify writes the current date into the report title heading
    (`# Graph Report - <root>  (YYYY-MM-DD)`); left in place it would churn
    the staged hash daily and trigger pointless re-ingestion.
    """
    lines = []
    for line in text.splitlines():
        if line.startswith("timestamp:"):
            continue
        if line.startswith("#"):
            line = HEADING_DATE_RE.sub("", line)
        lines.append(line)
    return "\n".join(lines) + "\n"


def report_deletion_candidates(out: pathlib.Path, current_names: set[str]) -> None:
    """Advisory: flag KB documents whose repository source no longer exists.

    Staging only ever adds; it cannot retract a document whose source file was
    deleted, moved, or deselected (its wiki pages and registry entry linger).
    This is read-only and never fatal - a missing or unreadable registry just
    means "no advice." Ownership and retraction live in ``prune_okf_orphans.py``;
    here we only mirror its ownership test (registry ``path`` under the staging
    dir = pipeline-owned; a user's externally added doc is never counted) so the
    heads-up matches what that script would actually act on.
    """
    reg_path = None
    for base in [out, *out.parents]:
        candidate = base / ".openkb" / "hashes.json"
        if candidate.exists():
            reg_path = candidate
            break
    if reg_path is None:
        return
    try:
        registry = json.loads(reg_path.read_text(encoding="utf-8"))
    except Exception:
        return
    if not isinstance(registry, dict):
        return
    pseudo = {"repo-snapshot", "graphify-report"}
    stale = [
        meta.get("doc_name") or meta.get("name")
        for meta in registry.values()
        if ".okf-build/input" in str(meta.get("path", "")).replace("\\", "/")
        and meta.get("doc_name") not in pseudo
        and str(meta.get("name", "")) not in current_names
    ]
    if stale:
        print(
            f"NOTE: {len(stale)} KB document(s) have no source in this pack - their repository "
            "files were deleted, moved, or deselected. Staging does not retract them; reconcile "
            "(deterministic, LLM-free) with:"
        )
        print("  uv run .agents/skills/agent-ready-context/scripts/prune_okf_orphans.py --repo . --kb-dir okf")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic OpenKB staged input from a Git repository.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--out", default="okf/.okf-build/input")
    parser.add_argument("--manifest", default="okf/.okf-build/manifests/source-pack-manifest.json")
    parser.add_argument("--max-lines", type=int, default=800)
    parser.add_argument(
        "--bundle-depth", type=int, default=0,
        help="Group selected files into per-directory digest documents using the first N "
             "path segments (0 = one staged doc per file). Nothing is omitted — files are "
             "bundled, not filtered. Changing this re-stages everything under new hashes, "
             "so the next add re-ingests the pack; pick a mode before first ingestion.",
    )
    parser.add_argument(
        "--code-split", action="store_true",
        help="Split oversized CODE files into full-content parts instead of cropping them "
             "(automatic when the selection contains no prose: code-only repos infer their "
             "concepts from code, so nothing may be cropped).",
    )
    parser.add_argument(
        "--bundle-max-lines", type=int, default=4000,
        help="Bundle-mode size guard: a group whose digest exceeds this many lines is split "
             "one directory level deeper (loudly); only an unsplittable group is emitted "
             "oversized, with a warning.",
    )
    parser.add_argument("--hash-names", action="store_true", help="Include source hash prefixes in staged file names")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    out = resolve_under(repo, args.out).resolve()
    manifest_path = resolve_under(repo, args.manifest).resolve()
    out.mkdir(parents=True, exist_ok=True)
    repo_files = out / "repo-files"
    if repo_files.exists():
        shutil.rmtree(repo_files)
    repo_files.mkdir(parents=True, exist_ok=True)
    for stale in [out / "repo-snapshot.md", out / "graphify-report.md"]:
        if stale.exists():
            stale.unlink()

    try:
        files = sorted(run(["git", "-c", "core.quotepath=false", "ls-files"], repo).splitlines())
    except Exception as exc:
        print(f"error: not a git repository or git unavailable: {exc}", file=sys.stderr)
        return 2

    touched = last_touch_commits(repo)

    manifest: list[dict[str, str]] = []

    # No HEAD commit in the snapshot: it would churn the staged bytes on every
    # commit and defeat OpenKB's hash dedupe. The inventory alone is the
    # snapshot's content; per-file provenance lives in each staged file.
    inventory = "\n".join(f"- `{f}`" for f in files if not should_skip(f)) + "\n"
    snapshot_body = (
        "# Repository Snapshot\n\n"
        "## Git tracked files\n\n"
        f"{inventory}"
    )
    snapshot_text = (
        frontmatter(
            {
                "type": "source-pack",
                "title": "Repository Snapshot",
                "description": "Repository tracked-file inventory for OpenKB ingestion.",
                "resource": "repo-snapshot",
                "source_path": "repo-snapshot",
                "source_kind": "text",
                "source_hash": sha256_text(snapshot_body),
            },
            ["repo", "snapshot", "source"],
        )
        + snapshot_body
    )
    snapshot = out / "repo-snapshot.md"
    write_text(snapshot, snapshot_text)
    manifest.append(
        {
            "source_path": "repo-snapshot",
            "staged_path": snapshot.relative_to(repo).as_posix(),
            "source_hash": sha256_text(snapshot_body),
            "source_kind": "text",
            "origin": "repo",
        }
    )

    graph_report = repo / "graphify-out" / "GRAPH_REPORT.md"
    graph_text: str | None = None
    if graph_report.exists():
        graph_text = strip_generated_timestamp_lines(normalize_text(graph_report.read_bytes()))
        # Self-reference guard: a graph that mapped the compiled KB would feed
        # descriptions of generated wiki pages back into the KB through this
        # report - a feedback loop that never converges (wiki -> graph ->
        # report -> ingest -> wiki). Refusal is loud and actionable, never a
        # silent omission.
        kb_refs = len(re.findall(r"\bokf/(?:wiki|raw|\.openkb|output)/", graph_text))
        if kb_refs >= 3:
            print(
                f"WARNING: graph report references {kb_refs} paths under the KB root (okf/) - "
                "graphify mapped the compiled wiki. Staging of graphify-report.md SKIPPED to "
                "avoid a self-referential ingestion loop. Fix: add 'okf/' to the repo root "
                ".graphifyignore, rerun graphify, then rebuild this source pack. If a polluted "
                "report was already ingested, preview its retraction with "
                "'openkb remove <doc> --dry-run' before re-adding the clean one.",
                file=sys.stderr,
            )
            graph_text = None
    if graph_text is not None:
        graph_hash = sha256_text(graph_text)
        graph_dest = out / "graphify-report.md"
        write_text(
            graph_dest,
            frontmatter(
                {
                    "type": "graph-report",
                    "title": "Graphify Report",
                    "description": "Graphify structural report used as an exploration map.",
                    "resource": "graphify-out/GRAPH_REPORT.md",
                    "source_path": "graphify-out/GRAPH_REPORT.md",
                    "source_kind": "markdown",
                    "source_hash": graph_hash,
                    "source_commit": touched.get("graphify-out/GRAPH_REPORT.md", "untracked"),
                },
                ["graphify", "repo-analysis"],
            )
            + graph_text,
        )
        manifest.append(
            {
                "source_path": "graphify-out/GRAPH_REPORT.md",
                "staged_path": graph_dest.relative_to(repo).as_posix(),
                "source_hash": graph_hash,
                "source_kind": "markdown",
                "origin": "graphify",
            }
        )

    selected = [f for f in files if not should_skip(f) and should_select(f)]

    # Code-split mode: in a repo that stages no prose at all, code IS the
    # concept source - cropping it starves the KB of exactly what it should
    # capture, so oversized code inherits split-not-crop. Auto-derived from
    # the selected file set (deterministic), or forced with --code-split.
    has_prose = any(source_kind(rel) == "markdown" for rel in selected)
    code_split = args.code_split or not has_prose
    if code_split and not args.code_split:
        print(
            "NOTE: no prose sources selected - code-only repository, so code is the concept "
            "source: oversized code files will be split (not cropped). Expect one compiled "
            "document per part; use --bundle-depth for very large repos."
        )

    if args.bundle_depth > 0:
        # Markdown never enters a bundle: prose is a primary concept source
        # with its own identity (and split-not-cropped handling below), while
        # bundles digest supporting files. The per-file loop handles it.
        prose = [rel for rel in selected if source_kind(rel) == "markdown"]
        bundleable = [rel for rel in selected if source_kind(rel) != "markdown"]

        def bundle_key(rel: str, depth: int) -> str:
            parts = rel.replace("\\", "/").split("/")
            return "/".join(parts[: min(depth, len(parts) - 1)]) or "root-files"

        def emit_group(key: str, members: list[str], depth: int) -> None:
            sections: list[str] = []
            digest = hashlib.sha256()
            total_lines = 0
            for rel in sorted(members):
                src = repo / rel
                if not src.is_file():
                    continue
                try:
                    normalized = normalize_text(src.read_bytes())
                except Exception:
                    continue
                digest.update(normalized.encode("utf-8"))
                body_lines = normalized.splitlines()[: args.max_lines]
                total_lines += len(body_lines)
                sections.append(
                    f"## {rel}\n\n"
                    f"- source_hash: {sha256_text(normalized)}\n"
                    f"- source_commit: {touched.get(rel, 'uncommitted')}\n\n"
                    "~~~\n"
                    + "\n".join(body_lines)
                    + "\n~~~\n"
                )
            if not sections:
                return
            # Size guard: an unbounded bundle becomes a single doc no model
            # context can compile (openkb never PageIndexes markdown). Deepen
            # this group one directory level and retry; only warn-and-emit
            # when it cannot be split any further.
            if total_lines > args.bundle_max_lines:
                subgroups: dict[str, list[str]] = {}
                for rel in members:
                    subgroups.setdefault(bundle_key(rel, depth + 1), []).append(rel)
                if len(subgroups) > 1 or (len(subgroups) == 1 and next(iter(subgroups)) != key):
                    print(
                        f"NOTE: bundle '{key}' ({total_lines} lines) exceeds --bundle-max-lines "
                        f"({args.bundle_max_lines}) - split one directory level deeper into "
                        f"{len(subgroups)} bundle(s)."
                    )
                    for subkey in sorted(subgroups):
                        emit_group(subkey, subgroups[subkey], depth + 1)
                    return
                print(
                    f"WARNING: bundle '{key}' ({total_lines} lines) exceeds --bundle-max-lines "
                    f"({args.bundle_max_lines}) and cannot be split deeper - it may exceed the "
                    "compile model's context window.",
                    file=sys.stderr,
                )
            bundle_hash = "sha256:" + digest.hexdigest()
            dest = repo_files / f"{safe_slug(key)}.md"
            write_text(
                dest,
                frontmatter(
                    {
                        "type": "source-bundle",
                        "title": key,
                        "description": "Per-directory digest of repository source files staged for OpenKB ingestion.",
                        "resource": key,
                        "source_path": key,
                        "source_kind": "bundle",
                        "source_hash": bundle_hash,
                    },
                    ["source-bundle"],
                )
                + f"# {key}\n\n"
                + "\n".join(sections),
            )
            manifest.append(
                {
                    "source_path": key,
                    "staged_path": dest.relative_to(repo).as_posix(),
                    "source_hash": bundle_hash,
                    "source_kind": "bundle",
                    "origin": "repo-bundle",
                    "member_count": str(len(sections)),
                }
            )

        groups: dict[str, list[str]] = {}
        for rel in bundleable:
            groups.setdefault(bundle_key(rel, args.bundle_depth), []).append(rel)
        for key in sorted(groups):
            emit_group(key, groups[key], args.bundle_depth)
        selected = prose

    for rel in selected:
        src = repo / rel
        if not src.is_file():
            continue
        try:
            normalized = normalize_text(src.read_bytes())
        except Exception:
            continue
        source_hash = sha256_text(normalized)
        lines = normalized.splitlines()
        kind = source_kind(rel)
        split_this = len(lines) > args.max_lines and (
            kind == "markdown" or (kind == "code" and code_split)
        )
        if split_this:
            # A concept source is never cropped: split into full-content parts
            # (headings for prose; top-level construct boundaries for code in
            # code-split mode). Each part is its own document with a stable
            # per-part hash, so editing one section re-ingests only that part.
            boundary = _prose_boundary if kind == "markdown" else _code_boundary
            parts = split_source(lines, args.max_lines, boundary)
            total = len(parts)
            print(f"NOTE: {rel} exceeds {args.max_lines} lines - split into {total} {kind} part(s), nothing cropped.")
            for idx, part_lines in enumerate(parts, 1):
                part_text = "\n".join(part_lines)
                part_hash = sha256_text(part_text)
                dest = repo_files / f"{safe_slug(rel)}.part{idx:02d}.md"
                write_text(
                    dest,
                    frontmatter(
                        {
                            "type": "source-file",
                            "title": f"{rel} (part {idx}/{total})",
                            "description": "Repository source file staged for OpenKB ingestion (oversized concept source, split not cropped).",
                            "resource": rel,
                            "source_path": rel,
                            "source_kind": kind,
                            "source_hash": part_hash,
                            "source_commit": touched.get(rel, "uncommitted"),
                            "part": f"{idx}/{total}",
                        },
                        ["source-file", kind],
                    )
                    + f"# {rel} (part {idx}/{total})\n\n"
                    "~~~\n"
                    f"{part_text}\n"
                    "~~~\n",
                )
                manifest.append(
                    {
                        "source_path": rel,
                        "staged_path": dest.relative_to(repo).as_posix(),
                        "source_hash": part_hash,
                        "source_kind": kind,
                        "origin": "repo",
                        "part": f"{idx}/{total}",
                    }
                )
            continue
        body = "\n".join(lines[: args.max_lines])
        hash_prefix = source_hash.removeprefix("sha256:")[:12] + "__" if args.hash_names else ""
        dest = repo_files / f"{hash_prefix}{safe_slug(rel)}.md"
        write_text(
            dest,
            frontmatter(
                {
                    "type": "source-file",
                    "title": rel,
                    "description": "Repository source file staged for OpenKB ingestion.",
                    "resource": rel,
                    "source_path": rel,
                    "source_kind": kind,
                    "source_hash": source_hash,
                    "source_commit": touched.get(rel, "uncommitted"),
                },
                ["source-file", kind],
            )
            +
            f"# {rel}\n\n"
            "~~~\n"
            f"{body}\n"
            "~~~\n",
        )
        manifest.append(
            {
                "source_path": rel,
                "staged_path": dest.relative_to(repo).as_posix(),
                "source_hash": source_hash,
                "source_kind": kind,
                "origin": "repo",
            }
        )

    manifest = sorted(manifest, key=lambda item: (item["source_path"], item["staged_path"]))
    write_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False))

    print(f"Wrote source pack to {out}")
    print(f"Wrote manifest to {manifest_path}")
    print(f"Staged {len(manifest)} source item(s)")
    print("Next step: openkb --kb-dir ./okf add ./okf/.okf-build/input/")
    print("Reminder: staging alone does not update okf/raw/ or okf/wiki/.")

    current_names = {pathlib.PurePosixPath(item["staged_path"]).name for item in manifest}
    report_deletion_candidates(out, current_names)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
