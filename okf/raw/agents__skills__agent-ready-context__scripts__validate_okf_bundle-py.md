---
type: "source-file"
title: ".agents/skills/agent-ready-context/scripts/validate_okf_bundle.py"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/agent-ready-context/scripts/validate_okf_bundle.py"
source_path: ".agents/skills/agent-ready-context/scripts/validate_okf_bundle.py"
source_kind: "code"
source_hash: "sha256:b30596139f7fdfca88f399fe84641ba877a6e32b3534e689c4cfb3d8a7d12ec2"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, code]
---

# .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py

~~~
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Validate an OKF bundle or OpenKB wiki against local Google OKF conformance rules.

Run with `uv run` so PyYAML is resolved automatically in an isolated
environment; with bare python3 the YAML checks degrade when PyYAML is absent.

This script implements the hard OKF v0.1 conformance checks known from
GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md. The agent should web-check
the official spec before relying on this local validator:
- every non-reserved Markdown file is a concept document;
- every concept document has parseable YAML frontmatter;
- every concept frontmatter has a non-empty `type` field;
- reserved `index.md` and `log.md` files are not concept documents and follow
  their respective structural rules when present;
- the bundle-root `index.md` may contain an `okf_version` frontmatter block.

Deterministic auditability checks beyond the spec (warnings, gate unchanged):
- unclosed code fence at end of file — the reliable signal for truncated or
  badly merged generated pages;
- sibling pages whose names collapse to the same normalized slug — likely
  near-duplicate concepts.

It is intentionally OS-agnostic: pathlib, tempfile and subprocess are used
instead of shell-specific commands. It does not require symlinks.

With --openkb-wiki, root AGENTS.md and OpenKB operational areas are skipped:
AGENTS.md is the wiki-conventions manual, while sources/ and reports/ are
evidence/reporting areas rather than concept pages. This mode adds OpenKB
convention checks:
- broken [[wikilinks]] are ERRORS (resolution mirrors openkb 0.4.4
  lint.find_broken_links: targets match a page's wiki-relative path without
  extension or its bare stem; `|alias` stripped; AGENTS.md/SCHEMA.md/log.md
  and sources/ + reports/ are not scanned but do provide targets; unlike
  upstream, fenced/inline code is ignored to avoid false positives);
- concepts/ and entities/ pages missing the machine-managed non-empty
  `sources:` frontmatter list are WARNED (OpenKB maintains that list on every
  generated page; its absence suggests damage or a hand edit).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - environment dependent
    yaml = None

RESERVED = {"index.md", "log.md"}
DATE_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}\s*$")
OPENKB_LOG_RE = re.compile(r"^##\s+\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\]\s+\S+.*$")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
# Mirrors openkb 0.4.4 lint._EXCLUDED_FILES for wikilink scanning.
LINK_SCAN_EXCLUDED = {"AGENTS.md", "SCHEMA.md", "log.md"}


def normalized_slug(stem: str) -> str:
    """Collapse a file stem for near-duplicate comparison (case, `_` vs `-`)."""
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code spans before link scanning."""
    lines = []
    open_fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if open_fence is None:
                open_fence = marker[0]
                continue
            if marker[0] == open_fence:
                open_fence = None
                continue
        if open_fence is None:
            lines.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(lines)


def has_unclosed_fence(text: str) -> bool:
    """True when a code fence is still open at end of file."""
    open_fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        if open_fence is None:
            open_fence = marker[0]
        elif marker[0] == open_fence:
            open_fence = None
    return open_fence is not None


def wiki_link_targets(root: Path) -> set[str]:
    """All valid wikilink targets, mirroring openkb lint._all_wiki_pages keys.

    Every .md file contributes its wiki-relative path without extension
    (posix) and its bare stem.
    """
    targets: set[str] = set()
    for md in root.rglob("*.md"):
        rel = md.relative_to(root)
        targets.add(rel.with_suffix("").as_posix())
        targets.add(md.stem)
    return targets


def split_frontmatter(text: str) -> tuple[str, str] | None:
    # OKF examples and spec use LF. Be permissive for CRLF by normalizing.
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return None
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return None
    return normalized[4:end], normalized[end + 5 :]


def load_yaml(raw: str, rel: str, errors: list[str]) -> dict[str, Any] | None:
    if yaml is None:
        errors.append(
            f"{rel}: cannot validate YAML parseability because PyYAML is not installed; "
            "install PyYAML to validate OKF YAML frontmatter locally"
        )
        return None
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:  # pragma: no cover - error formatting
        errors.append(f"{rel}: invalid YAML frontmatter: {exc}")
        return None
    if data is None:
        return {}
    if not isinstance(data, dict):
        errors.append(f"{rel}: YAML frontmatter must be a mapping/object")
        return None
    return data


def validate_index(path: Path, rel: str, text: str, errors: list[str], warnings: list[str]) -> None:
    parts = split_frontmatter(text)
    body = text
    if parts is not None:
        raw_fm, body = parts
        if rel != "index.md":
            errors.append(f"{rel}: non-root reserved index.md must not contain YAML frontmatter")
        else:
            fm = load_yaml(raw_fm, rel, errors)
            if fm is not None:
                if "okf_version" not in fm:
                    errors.append(f"{rel}: root index.md frontmatter is only permitted to declare okf_version")
                extra = sorted(set(fm) - {"okf_version"})
                if extra:
                    warnings.append(
                        f"{rel}: root index.md frontmatter should only contain okf_version; extra keys: {', '.join(extra)}"
                    )
                if fm.get("okf_version") and not isinstance(fm.get("okf_version"), str):
                    warnings.append(f"{rel}: okf_version should be a string such as '0.1'")
    # Spec says one or more sections grouping concepts. Keep as warning because
    # conformance says reserved files follow structure, but empty/generated roots
    # may be bootstrapped before concepts exist.
    headings = [line for line in body.replace("\r\n", "\n").splitlines() if line.startswith("#")]
    if not headings:
        warnings.append(f"{rel}: index.md should contain at least one Markdown heading")
    if not MD_LINK_RE.search(body):
        warnings.append(f"{rel}: index.md should enumerate entries with Markdown links")


def validate_log(
    rel: str,
    text: str,
    errors: list[str],
    warnings: list[str],
    openkb_wiki: bool = False,
) -> None:
    if split_frontmatter(text) is not None:
        errors.append(f"{rel}: reserved log.md must not contain YAML frontmatter")
    lines = text.replace("\r\n", "\n").splitlines()
    for line in lines:
        if not line.startswith("## "):
            continue
        if DATE_RE.match(line):
            continue
        if openkb_wiki and OPENKB_LOG_RE.match(line):
            continue
        if openkb_wiki:
            errors.append(f"{rel}: OpenKB log heading has unexpected format: {line}")
        else:
            errors.append(f"{rel}: log date heading must be ISO 8601 YYYY-MM-DD: {line}")
    if lines and not any(line.startswith("#") for line in lines):
        warnings.append(f"{rel}: log.md should contain a Markdown title/heading")


def validate_concept(
    path: Path,
    rel: str,
    text: str,
    errors: list[str],
    warnings: list[str],
    openkb_wiki: bool = False,
) -> None:
    # explorations/ is OpenKB's agent-writable notes namespace, not compiled
    # concept output: `query --save` writes only a `query:` header (0.4.4
    # cli.py) and finding capture pages carry `type: Finding` by convention,
    # so frontmatter shape issues there are advisory, not structural.
    exploration = openkb_wiki and rel.startswith("explorations/")
    parts = split_frontmatter(text)
    if parts is None:
        if exploration:
            warnings.append(
                f"{rel}: explorations page has no YAML frontmatter; saved queries "
                "carry 'query:' and finding pages carry 'type: Finding'"
            )
        else:
            errors.append(f"{rel}: missing YAML frontmatter block")
        return
    raw_fm, body = parts
    fm = load_yaml(raw_fm, rel, errors)
    if fm is None:
        return
    value = fm.get("type")
    saved_query = exploration and bool(fm.get("query"))
    if exploration:
        if not (saved_query or (isinstance(value, str) and value.strip())):
            warnings.append(
                f"{rel}: explorations page should carry 'query:' (saved query) "
                "or a non-empty 'type:' (finding convention)"
            )
    elif value is None or (isinstance(value, str) and not value.strip()):
        errors.append(f"{rel}: missing non-empty required frontmatter field 'type'")
    elif not isinstance(value, str):
        warnings.append(f"{rel}: frontmatter field 'type' should be a short descriptive string")

    # Soft guidance from the spec; machine-written query saves never carry
    # title/description, so they are exempt. OpenKB uses the body H1 as the
    # display title on generated pages, which satisfies the intent of the
    # optional OKF title field without duplicating it in frontmatter.
    if not saved_query:
        for field in ("title", "description"):
            body_h1_supplies_title = (
                field == "title"
                and openkb_wiki
                and any(re.match(r"^#\s+\S", line) for line in body.splitlines())
            )
            if not fm.get(field) and not body_h1_supplies_title:
                warnings.append(f"{rel}: missing recommended frontmatter field '{field}'")
    if not body.strip():
        warnings.append(f"{rel}: concept body is empty")

    # OpenKB maintains a `sources:` list on every generated concept/entity
    # page; a missing or empty list means the page lost its citation chain
    # (damaged merge, hand edit, or orphaned generation).
    if openkb_wiki and rel.startswith(("concepts/", "entities/")):
        sources = fm.get("sources")
        if not (isinstance(sources, list) and sources):
            warnings.append(
                f"{rel}: missing machine-managed non-empty 'sources' frontmatter list; "
                "the page cannot be traced to a source document"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an OKF v0.1 bundle")
    parser.add_argument("bundle", help="Path to OKF bundle directory")
    parser.add_argument("--strict-warnings", action="store_true", help="Treat warnings as errors")
    parser.add_argument(
        "--openkb-wiki",
        action="store_true",
        help="Skip OpenKB operational wiki files: root AGENTS.md, sources/, and reports/",
    )
    args = parser.parse_args()

    root = Path(args.bundle).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    md_files = sorted(root.rglob("*.md"))
    if not md_files:
        errors.append("bundle contains no Markdown files")

    skipped: list[str] = []
    checked: list[Path] = []
    link_scan: dict[str, str] = {}
    for path in md_files:
        rel = path.relative_to(root).as_posix()
        if args.openkb_wiki and (
            rel == "AGENTS.md" or rel.startswith("sources/") or rel.startswith("reports/")
        ):
            skipped.append(rel)
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: not valid UTF-8: {exc}")
            continue

        checked.append(path)
        if has_unclosed_fence(text):
            warnings.append(f"{rel}: code fence still open at end of file (possible truncation or bad merge)")
        if args.openkb_wiki and path.name not in LINK_SCAN_EXCLUDED:
            link_scan[rel] = text

        if path.name == "index.md":
            validate_index(path, rel, text, errors, warnings)
        elif path.name == "log.md":
            validate_log(rel, text, errors, warnings, openkb_wiki=args.openkb_wiki)
        else:
            validate_concept(path, rel, text, errors, warnings, openkb_wiki=args.openkb_wiki)

    # Near-duplicate sibling pages: same normalized slug in the same directory.
    by_dir: dict[tuple[Path, str], list[str]] = {}
    for path in checked:
        if path.name in RESERVED:
            continue
        by_dir.setdefault((path.parent, normalized_slug(path.stem)), []).append(path.name)
    for (parent, slug), names in sorted(by_dir.items(), key=lambda item: str(item[0])):
        if slug and len(names) > 1:
            rel_dir = parent.relative_to(root).as_posix()
            warnings.append(
                f"{rel_dir}: near-duplicate page names collapse to the same slug '{slug}': "
                + ", ".join(sorted(names))
            )

    # OpenKB wiki mode: broken wikilinks are structural damage and gate the run.
    if args.openkb_wiki:
        targets = wiki_link_targets(root)
        for rel in sorted(link_scan):
            for raw_target in WIKILINK_RE.findall(strip_code(link_scan[rel])):
                target = raw_target.split("|")[0].strip().strip("/")
                if target and target not in targets:
                    errors.append(f"{rel}: broken wikilink [[{target}]]")

    if args.strict_warnings:
        errors.extend(f"warning treated as error: {w}" for w in warnings)
        warnings = []

    if args.openkb_wiki:
        print(
            "OpenKB wiki mode: skipped root AGENTS.md plus sources/ and reports/ "
            f"operational areas ({len(skipped)} Markdown file(s))."
        )
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if errors:
        print(f"OKF validation failed: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    validated_count = len(md_files) - len(skipped)
    print(f"OKF validation passed: {validated_count} Markdown file(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~
