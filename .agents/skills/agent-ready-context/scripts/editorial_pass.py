#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Briefing and deterministic checks for the guarded class-3 editorial curation pass.

The semantic half of `openkb lint` audits the compiled wiki but is read-only by
design, and some accepted findings (page merges, concept-sprawl consolidation)
have no OpenKB command. This script makes the documented last-resort hand edit
safe by *using* the pinned OpenKB's own machinery — imported from the installed
tool environment and executed by that environment's interpreter, never
re-implemented here — plus the git-based policy invariants OpenKB has no
checker for.

--brief prints the curation briefing to load into the editing agent's context
BEFORE any edit. Its core is the exact wikilink-whitelist middleware OpenKB
injects into its own compile calls: `_KNOWN_TARGETS_USER` rendered with
`_format_known_targets(list_existing_wiki_targets(wiki))`, all imported from
the installed openkb package. An approved split may extend the whitelist with
`--allow-new-pages ns/slug,...` — the same planned-slugs union the compiler
itself performs for pages about to be created. This keeps even a small local
model under the same constraints as OpenKB's own generation.

--check verifies a completed curation diff (git base → working tree, default
base HEAD) deterministically and zero-LLM. Vendor half, executed by the
installed openkb: find_broken_links (dangling inbound links after a merge,
invented targets), check_index_sync (stale or missing index entries),
find_orphans (a merge that unlinked a survivor; stale `reports/` results are
filtered per the documented vendor false positive), find_invalid_frontmatter,
and find_missing_okf_fields. Policy half, computed here from git:

  * scope — under the KB root, only `wiki/concepts/`, `wiki/entities/`, and
    the root `wiki/index.md` may change; registry, raw/, summaries/, sources/,
    log.md, AGENTS.md, reports/, tooling/, and explorations/ are off-limits
    to curation (they have their own channels);
  * provenance — the union of `sources:` values across concepts/ + entities/
    is identical before and after (a merge unions lists; nothing is lost,
    nothing is invented);
  * no new compiled pages unless listed in --allow-new-pages;
  * every changed concepts/entities page keeps a non-empty `sources:` list.

Run --check on a diff range that contains ONLY the curation (commit or stash
other KB work first), then run validate_okf_bundle.py --openkb-wiki and the
single verification lint per the loop guard.

Fragility is asymmetric and handled accordingly. `--check`'s five functions and
`list_existing_wiki_targets` are `openkb.lint`'s public (non-underscore) API —
the same surface OpenKB's own CLI calls — so a failure to import them means
something is genuinely wrong with the installed tool and `--check` fails
loudly (exit 2): re-verify this pass against the new version before curating.
`_KNOWN_TARGETS_USER` and `_format_known_targets` are underscore-prefixed
*private* compiler internals with no stability guarantee; a future OpenKB
release is free to rename or restructure them without notice. `--brief` tries
them first — using the vendor's own wording beats reimplementing it — but on
any failure (flagged loudly on stderr, never silent) falls back to a mirrored
copy of the template captured from openkb 0.4.4 (see `_MIRRORED_KNOWN_TARGETS_USER`
below). Re-diff that mirror against the installed version's source after any
openkb pin bump; a drift only degrades the briefing's wording, never `--check`'s
correctness. Exit codes: 0 pass, 1 violations, 2 environment.
"""
from __future__ import annotations

import argparse
import functools
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import yaml

# Wiki pages and vendor output are UTF-8; never let Windows' legacy default
# codepage decode child-process streams.
run_utf8 = functools.partial(
    subprocess.run, capture_output=True, text=True, encoding="utf-8", errors="replace"
)

# Executed by the *installed openkb tool venv's* interpreter, so every import
# below resolves to the pinned vendor code in its native environment.
#
# Public API (openkb.lint, no leading underscore) — stable, load-bearing for
# --check's correctness. A failure here is a real environment problem.
_VENDOR_RUNNER_STABLE = """\
import json, sys
import importlib.metadata as md
from pathlib import Path

mode = sys.argv[1]
wiki = Path(sys.argv[2]).resolve()
out = {"openkb_version": md.version("openkb")}
from openkb.lint import (
    list_existing_wiki_targets,
    find_broken_links,
    find_orphans,
    check_index_sync,
    find_invalid_frontmatter,
    find_missing_okf_fields,
)
if mode == "targets":
    extra = set(json.loads(sys.argv[3])) if len(sys.argv) > 3 else set()
    out["targets"] = sorted(list_existing_wiki_targets(wiki) | extra)
else:
    out["broken_links"] = find_broken_links(wiki)
    out["orphans"] = find_orphans(wiki)
    out["index_sync"] = check_index_sync(wiki)
    out["invalid_frontmatter"] = find_invalid_frontmatter(wiki)
    out["missing_okf_fields"] = find_missing_okf_fields(wiki)
print(json.dumps(out))
"""

# Private API (openkb.agent.compiler, leading underscore) — no stability
# guarantee. Best-effort only; --brief degrades to the mirrored copy below on
# any failure instead of propagating one.
_VENDOR_RUNNER_PRIVATE_TEMPLATE = """\
import json, sys
import importlib.metadata as md
from openkb.agent.compiler import _KNOWN_TARGETS_USER, _format_known_targets

targets = set(json.loads(sys.stdin.read()))
print(json.dumps({
    "openkb_version": md.version("openkb"),
    "message": _KNOWN_TARGETS_USER.format(known_targets=_format_known_targets(targets)),
}))
"""

# Mirrored fallback — a literal copy of openkb 0.4.4's
# `openkb.agent.compiler._KNOWN_TARGETS_USER`, used only when the private
# import above fails. Re-diff against the installed version's source after
# any openkb pin bump; drift here only weakens wording, never --check's gates.
#
# SPDX-FileCopyrightText: 2026 Vectify AI
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
#
# SPDX-FileComment: _MIRRORED_KNOWN_TARGETS_USER below is a verbatim copy of
# openkb.agent.compiler._KNOWN_TARGETS_USER, and _format_targets_mirrored
# mirrors openkb.agent.compiler._format_known_targets, both from
# https://github.com/VectifyAI/OpenKB, source file openkb/agent/compiler.py,
# tag v0.4.4 (commit bd9fe3989e71fc8012b19eb305662fa307f0a799). Copied
# verbatim as a best-effort fallback when the private (underscore-prefixed,
# no-stability-guarantee) API import fails; see THIRD_PARTY_NOTICES.md.
_MIRRORED_KNOWN_TARGETS_USER = """\
The wiki currently contains these pages, and they are the COMPLETE list of \
valid [[wikilink]] targets you may use in the responses that follow:

{known_targets}

Rules for [[wikilinks]] in all subsequent responses:
- For [[concepts/X]]: X must appear in the whitelist above.
- For [[summaries/Y]]: Y must appear in the whitelist above.
- For [[entities/Z]]: Z must appear in the whitelist above.
- Do NOT invent new wikilink targets. If you want to mention a concept \
or entity that is not in the whitelist, write it as plain text without brackets.
"""


def _format_targets_mirrored(targets: set[str]) -> str:
    """Mirrors `openkb.agent.compiler._format_known_targets` (0.4.4)."""
    if not targets:
        return "(none yet — do not use any [[wikilinks]] in your output)"
    return "\\n".join(f"- {t}" for t in sorted(targets))

CURATION_RULES = """\
Curation rules (this pipeline, non-negotiable):
- Curation only: merge, split, reorganize, tighten, and cross-link content
  that already exists in the pages you touch. Do NOT add new claims — new
  knowledge goes through the findings channel (explorations/findings/), never
  through this pass.
- Touch only concepts/, entities/, and the root index.md. Everything else
  under the KB root is off-limits (summaries/, sources/, raw/, log.md,
  AGENTS.md, reports/, tooling/, explorations/, .openkb/).
- Frontmatter is machine-managed: keep it parseable YAML, keep `type` and
  `description`, and when merging pages set the survivor's `sources:` to the
  union of the merged pages' lists. Never lose or invent a source.
- Update the root index.md: remove entries for deleted pages, keep the
  survivor's entry accurate.
- After deleting or merging a page, rewire every inbound [[wikilink]] and
  index link to the survivor (hand-fix, or `openkb lint --fix` with consent).
- When done, verify: editorial_pass.py --check, then
  validate_okf_bundle.py <wiki> --openkb-wiki, then the single verification
  lint allowed by the loop guard.
"""


def fail_env(msg: str) -> "int":
    print(f"ENVIRONMENT ERROR: {msg}", file=sys.stderr)
    return 2


def openkb_python() -> Path | None:
    """Interpreter of the installed openkb uv tool venv, if any."""
    try:
        out = run_utf8(["uv", "tool", "dir"], check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    root = Path(out.stdout.strip()) / "openkb"
    for cand in (root / "Scripts" / "python.exe", root / "bin" / "python"):
        if cand.exists():
            return cand
    return None


def run_vendor_stable(mode: str, wiki: Path, extra_targets: list[str]) -> dict | int:
    """Execute the public-API vendor runner: `targets` or `check`.

    Failure here is a real environment problem (public API missing/broken)
    and is never silently degraded.
    """
    py = openkb_python()
    if py is None:
        return fail_env(
            "installed openkb tool venv not found via `uv tool dir`; "
            "install openkb per references/dependencies.md before curating."
        )
    argv = [str(py), "-c", _VENDOR_RUNNER_STABLE, mode, str(wiki)]
    # extra_targets is the small, user-typed --allow-new-pages list here, not
    # the full-corpus wikilink whitelist (that one goes over stdin in
    # run_vendor_template, below, precisely because it scales with wiki size
    # and can hit Windows' ~32K command-line limit) - argv is fine for this.
    if mode == "targets":
        argv.append(json.dumps(sorted(extra_targets)))
    proc = run_utf8(argv)
    if proc.returncode != 0:
        return fail_env(
            "the pinned openkb's public lint API could not be used "
            f"(exit {proc.returncode}) — the installed openkb may be broken or "
            "the wrong version. Re-verify the editorial pass against the "
            f"installed version before curating.\n--- vendor stderr ---\n{proc.stderr}"
        )
    return json.loads(proc.stdout)


def run_vendor_template(py: Path, targets: set[str]) -> tuple[str, str, bool]:
    """Render the whitelist message. Returns (message, openkb_version, mirrored).

    Tries the private compiler internals first; on ANY failure (import error,
    signature drift, anything) falls back to the mirrored copy and flags it
    loudly on stderr — this is the one part of the script allowed to degrade
    rather than hard-fail, because it only affects prompt wording, not
    `--check`'s gates.
    """
    proc = run_utf8(
        [str(py), "-c", _VENDOR_RUNNER_PRIVATE_TEMPLATE],
        input=json.dumps(sorted(targets)),
    )
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            return data["message"], data["openkb_version"], False
        except (json.JSONDecodeError, KeyError):
            pass
    print(
        "WARNING: openkb's private compiler whitelist template "
        "(openkb.agent.compiler._KNOWN_TARGETS_USER) could not be used — it "
        "likely moved or was renamed in this openkb release. Falling back to "
        "a mirrored copy captured from openkb 0.4.4; re-diff it against the "
        f"installed version's source.\n--- vendor stderr ---\n{proc.stderr}",
        file=sys.stderr,
    )
    version = "unknown"
    try:
        vproc = run_utf8(
            [str(py), "-c", "import importlib.metadata as m; print(m.version('openkb'))"]
        )
        if vproc.returncode == 0:
            version = vproc.stdout.strip()
    except OSError:
        pass
    message = _MIRRORED_KNOWN_TARGETS_USER.format(
        known_targets=_format_targets_mirrored(targets)
    )
    return message, version, True


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    lines = text.split("\n")
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                fm = yaml.safe_load("\n".join(lines[1:i]))
            except yaml.YAMLError:
                return None
            return fm if isinstance(fm, dict) else None
    return None


def sources_of(text: str) -> set[str]:
    fm = parse_frontmatter(text) or {}
    val = fm.get("sources")
    if isinstance(val, str):
        return {val}
    if isinstance(val, list):
        return {str(v) for v in val}
    return set()


def run_git(repo: Path, *args: str) -> str:
    proc = run_utf8(["git", "-C", str(repo), *args])
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def diff_entries(repo: Path, base: str, kb_rel: str) -> list[tuple[str, str]]:
    """(status, repo-relative posix path) pairs for base → working tree.

    Renames are split into a delete of the old path and an add of the new one.
    Untracked files under the KB root are included as adds, since curation
    runs on the working tree without staging anything.
    """
    entries: list[tuple[str, str]] = []
    for line in run_git(repo, "diff", "--name-status", "-M", base, "--", kb_rel).splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) == 3:
            entries.append(("D", parts[1]))
            entries.append(("A", parts[2]))
        elif len(parts) == 2:
            entries.append((status[0], parts[1]))
    for line in run_git(repo, "status", "--porcelain=v1", "-uall", "--", kb_rel).splitlines():
        if line.startswith("?? "):
            path = line[3:].strip().strip('"')
            if path.endswith("/"):
                continue
            entries.append(("A", path))
    return entries


def base_kb_page_texts(repo: Path, base: str, dirs: list[str]) -> dict[str, str]:
    """All .md page texts under *dirs* at *base*, in one subprocess.

    A `git show` per page is minutes of process spawns on Windows wikis with
    hundreds of pages; `git archive` streams the whole tree once instead.
    """
    proc = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", base, "--", *dirs],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git archive {base} failed: {proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    texts: dict[str, str] = {}
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        for member in tar:
            if member.isfile() and member.name.endswith(".md"):
                fh = tar.extractfile(member)
                if fh is not None:
                    texts[member.name] = fh.read().decode("utf-8", "replace")
    return texts


def cmd_brief(repo: Path, wiki: Path, allow_new: list[str]) -> int:
    targets_result = run_vendor_stable("targets", wiki, allow_new)
    if isinstance(targets_result, int):
        return targets_result
    targets = set(targets_result["targets"])

    py = openkb_python()
    if py is None:
        return fail_env(
            "installed openkb tool venv not found via `uv tool dir`; "
            "install openkb per references/dependencies.md before curating."
        )
    message, openkb_version, mirrored = run_vendor_template(py, targets)

    print("# Editorial curation briefing (class-3 semantic-lint findings)")
    print(
        f"\n{'Mirrored fallback' if mirrored else 'Vendor middleware'} below "
        f"reflects openkb {openkb_version} — the same whitelist message its "
        f"compiler injects before every generation call ({len(targets)} valid targets"
        + (f", including {len(allow_new)} approved new page(s)" if allow_new else "")
        + ")."
    )
    if mirrored:
        print(
            "This is a MIRRORED COPY (openkb's private compiler template could "
            "not be used — see the warning above), not the live vendor text. "
            "Re-diff it against the installed version's source before trusting it."
        )
    print()
    print(
        "--- "
        + ("mirrored" if mirrored else "vendor")
        + " wikilink middleware ("
        + ("mirrored copy" if mirrored else "verbatim")
        + ") ---\n"
    )
    print(message)
    print("--- end middleware ---\n")
    print(CURATION_RULES)
    return 0


def cmd_check(repo: Path, kb_rel: str, wiki: Path, base: str, allow_new: list[str]) -> int:
    violations: list[str] = []
    notes: list[str] = []
    kb = kb_rel.rstrip("/")
    concepts_rel = f"{kb}/wiki/concepts/"
    entities_rel = f"{kb}/wiki/entities/"
    index_rel = f"{kb}/wiki/index.md"

    try:
        entries = diff_entries(repo, base, kb)
    except RuntimeError as exc:
        return fail_env(str(exc))

    compiled_changed: list[tuple[str, str]] = []
    for status, path in entries:
        in_compiled = path.startswith((concepts_rel, entities_rel)) and path.endswith(".md")
        if in_compiled:
            compiled_changed.append((status, path))
        elif path != index_rel:
            violations.append(
                f"scope: {status} {path} — curation may only touch "
                f"{concepts_rel}, {entities_rel}, and {index_rel}"
            )

    if not entries:
        notes.append(f"no changes under {kb}/ against base {base} — nothing to curate-check")

    wiki_prefix = f"{kb}/wiki/"
    for status, path in compiled_changed:
        slug = path[len(wiki_prefix):-3]
        if status == "A" and slug not in allow_new:
            violations.append(
                f"new-page: {path} mints a new compiled page; splits must be "
                f"pre-approved with --allow-new-pages {slug}"
            )

    # Provenance union across concepts/ + entities/ must be identical.
    try:
        before_texts = base_kb_page_texts(
            repo, base, [f"{kb}/wiki/concepts", f"{kb}/wiki/entities"]
        )
    except RuntimeError as exc:
        return fail_env(str(exc))
    before_sources: set[str] = set()
    for text in before_texts.values():
        before_sources |= sources_of(text)
    after_sources: set[str] = set()
    for sub in ("concepts", "entities"):
        d = wiki / sub
        if d.is_dir():
            for page in d.glob("*.md"):
                after_sources |= sources_of(page.read_text(encoding="utf-8"))
    for lost in sorted(before_sources - after_sources):
        violations.append(
            f"provenance-lost: source '{lost}' is no longer cited by any "
            "concepts/entities page — a merge must union the sources: lists"
        )
    for invented in sorted(after_sources - before_sources):
        violations.append(
            f"provenance-invented: source '{invented}' did not exist at "
            f"{base} — curation may not add provenance"
        )

    # Changed compiled pages keep a non-empty machine-managed sources: list.
    for status, path in compiled_changed:
        if status == "D":
            continue
        fs_path = repo / Path(path)
        if not fs_path.exists():
            continue
        if not sources_of(fs_path.read_text(encoding="utf-8")):
            violations.append(f"sources: {path} has no non-empty `sources:` list after the edit")

    # Vendor structural checks, executed by the pinned openkb itself.
    result = run_vendor_stable("check", wiki, [])
    if isinstance(result, int):
        return result
    notes.append(f"vendor checks executed by installed openkb {result['openkb_version']}")
    orphans = [
        o for o in result["orphans"] if not str(o).replace("\\", "/").startswith("reports/")
    ]
    skipped_reports = len(result["orphans"]) - len(orphans)
    if skipped_reports:
        notes.append(
            f"{skipped_reports} orphan finding(s) under reports/ ignored "
            "(documented vendor false positive on stale lint reports)"
        )
    for label, items in (
        ("broken-wikilink", result["broken_links"]),
        ("orphan", orphans),
        ("index-sync", result["index_sync"]),
        ("invalid-frontmatter", result["invalid_frontmatter"]),
        ("missing-okf-field", result["missing_okf_fields"]),
    ):
        for item in items:
            violations.append(f"{label}: {item}")

    print(f"Editorial curation check — base {base}, KB {kb}/")
    for note in notes:
        print(f"  note: {note}")
    if violations:
        print(f"\nFAIL — {len(violations)} violation(s):")
        for v in violations:
            print(f"  - {v}")
        print(
            "\nFix the violations (or revert the curation) before running the "
            "validator and the verification lint."
        )
        return 1
    print("\nPASS — curation diff obeys scope, provenance, and vendor structural checks.")
    print(
        "Next: uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py "
        f"{kb}/wiki --openkb-wiki, then the single verification lint."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=".")
    parser.add_argument("--kb-dir", default="okf", help="KB root relative to the repo")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--brief", action="store_true", help="print the pre-edit briefing")
    mode.add_argument("--check", action="store_true", help="verify a completed curation diff")
    parser.add_argument("--base", default="HEAD", help="git base for --check (default HEAD)")
    parser.add_argument(
        "--allow-new-pages",
        default="",
        help="comma-separated namespaced slugs (e.g. entities/foo) an approved split may create",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    repo = Path(args.repo).resolve()
    wiki = repo / args.kb_dir / "wiki"
    if not wiki.is_dir():
        return fail_env(f"wiki not found at {wiki}")
    allow_new = [s.strip() for s in args.allow_new_pages.split(",") if s.strip()]
    for slug in allow_new:
        ns = slug.split("/", 1)[0]
        if ns not in ("concepts", "entities"):
            return fail_env(f"--allow-new-pages entries must be concepts/* or entities/*: {slug}")

    if args.brief:
        return cmd_brief(repo, wiki, allow_new)
    return cmd_check(repo, args.kb_dir, wiki, args.base, allow_new)


if __name__ == "__main__":
    sys.exit(main())
