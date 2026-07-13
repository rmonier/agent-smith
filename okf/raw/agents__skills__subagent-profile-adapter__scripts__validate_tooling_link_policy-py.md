---
type: "source-file"
title: ".agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py"
source_path: ".agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py"
source_kind: "code"
source_hash: "sha256:462a91200d7870f08d1de222a15cd32033582000da4e72b9af433a841cf478c7"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, code]
---

# .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py

~~~
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Validate the OpenKB wiki tooling-context link direction policy.

Policy:
- pages under okf/wiki/tooling/ may link to project pages;
- project OKF concept pages and subdirectory indexes must not link back to
  okf/wiki/tooling/;
- the bundle-root index.md and log.md are reserved navigation/history files
  and are exempt from the forbidden direction;
- when okf/wiki/tooling/ contains non-reserved pages, the bundle-root index.md
  MUST reference tooling/ so the bundle stays navigable, in a clearly
  labeled harness-specific section;
- tooling context is local-by-default (user-scoped, gitignored except the
  navigation stub), so when tooling/ contains non-reserved pages the committed
  stub okf/wiki/tooling/index.md MUST exist — it is what the root-index
  reference resolves to on clones that have no local tooling pages.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(
    r"\[[^\]]+\]\(([^)]+)\)|(?<![\w./-])okf/wiki/tooling/[\w./#-]+|"
    r"(?<![\w./-])wiki/tooling/[\w./#-]+|(?<![\w./-])tooling/[\w./#-]+"
)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def is_tooling_link(target: str) -> bool:
    t = target.strip().strip('"').strip("'")
    return (
        "okf/wiki/tooling/" in t
        or "wiki/tooling/" in t
        or t.startswith("tooling/")
        or t.startswith("./tooling/")
        or t.startswith("../tooling/")
        or "/tooling/harnesses/" in t
    )


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def strip_code_preserve_lines(text: str) -> str:
    """Remove code spans/blocks while preserving line numbers for diagnostics."""
    stripped: list[str] = []
    open_fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if open_fence is None:
                open_fence = marker[0]
            elif marker[0] == open_fence:
                open_fence = None
            stripped.append("")
            continue
        if open_fence is not None:
            stripped.append("")
            continue
        stripped.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(stripped)


def should_scan_for_project_to_tooling_links(rel: Path) -> bool:
    """Return True for project concept pages and navigation indexes only.

    Entity pages may legitimately describe the committed tooling navigation
    stub when the repository's own skills are KB sources. They are not project
    concepts and the documented one-way dependency rule does not cover them.
    """
    rel_posix = rel.as_posix()
    if rel_posix in {"index.md", "log.md"}:
        return True
    if rel_posix == "AGENTS.md":
        return False
    return rel.name == "index.md" or (bool(rel.parts) and rel.parts[0] == "concepts")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--okf", default="okf/wiki", help="OKF wiki directory, relative to repo unless absolute")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    okf = Path(args.okf)
    if not okf.is_absolute():
        okf = repo / okf
    okf = okf.resolve()

    if not okf.exists():
        print(f"warning: OKF directory does not exist: {okf}")
        return 0

    tooling = okf / "tooling"
    errors: list[str] = []
    warnings: list[str] = []

    root_index_links_tooling = False

    for path in sorted(okf.rglob("*.md")):
        rel = path.relative_to(okf)
        if rel.as_posix() == "AGENTS.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        in_tooling = tooling in path.parents or path == tooling
        if in_tooling:
            fm = parse_frontmatter(text)
            if rel.name not in {"index.md", "log.md"}:
                if fm.get("scope") != "tooling" and fm.get("type") != "tooling-context":
                    warnings.append(f"{rel}: tooling page should declare scope: tooling or type: tooling-context")
                if not WIKILINK_RE.search(strip_code_preserve_lines(text)):
                    errors.append(
                        f"{rel}: local tooling page has no outgoing wikilink; add one valid "
                        "[[project-page]] link so OpenKB structural lint does not classify it as orphaned"
                    )
            continue

        is_root_reserved = rel.as_posix() in {"index.md", "log.md"}

        if not should_scan_for_project_to_tooling_links(rel):
            continue

        scan_text = strip_code_preserve_lines(text)
        for match in LINK_RE.finditer(scan_text):
            target = match.group(1) or match.group(0)
            if is_tooling_link(target):
                if is_root_reserved:
                    # Bundle-root index/log are navigation/history: linking tooling
                    # there is the required outsider entry, not a dependency.
                    if rel.as_posix() == "index.md":
                        root_index_links_tooling = True
                    continue
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel}:{line}: project OKF page links to tooling context: {target}")

    tooling_has_pages = tooling.is_dir() and any(
        p.name not in {"index.md", "log.md"} for p in tooling.rglob("*.md")
    )
    if tooling_has_pages:
        root_index = okf / "index.md"
        if not root_index.exists():
            errors.append(
                "index.md: bundle-root index.md is missing while okf/wiki/tooling/ has pages; "
                "the root index must reference tooling/ in a harness-specific section"
            )
        elif not root_index_links_tooling:
            errors.append(
                "index.md: okf/wiki/tooling/ has pages but the bundle-root index.md does not reference them; "
                "add a clearly labeled harness-specific section linking tooling/"
            )
        if not (tooling / "index.md").exists():
            errors.append(
                "tooling/index.md: missing committed navigation stub while okf/wiki/tooling/ has pages; "
                "tooling is local-by-default, so the stub is what the root index entry resolves to on other clones"
            )

    for w in warnings:
        print(f"warning: {w}")
    if errors:
        for e in errors:
            print(f"error: {e}")
        return 1
    print("tooling link policy passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~
