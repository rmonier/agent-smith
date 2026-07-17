#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Generate a conservative OKF wiki skeleton for the zero-LLM fallback.

This is a fallback for environments without LLM provider credentials.
It does not claim semantic completeness. By default it writes okf/wiki/ as the
zero-LLM floor for the OpenWiki path, seeding `quickstart.md` and the
`INSTRUCTIONS.md` preservation contract from the skill's template assets.
It never overwrites an existing okf/wiki/: manual edits or producer output
fail closed and must be handled by the staged OpenWiki updater.
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import subprocess
import sys

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "page"


def frontmatter(title: str, type_: str, tags: list[str], desc: str) -> str:
    tag_lines = "\n".join(f"  - {t}" for t in tags)
    return (
        "---\n"
        f"type: {type_}\n"
        f"title: {title}\n"
        f"description: {desc}\n"
        "tags:\n"
        f"{tag_lines}\n"
        "x-generator: okf-skeleton\n"
        "---\n\n"
    )


def run_git(repo: pathlib.Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--out", default="okf/wiki")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    out = (repo / args.out).resolve()
    concepts = out / "concepts"

    if out.exists() and any(out.rglob("*.md")):
        print(
            f"error: {out} already contains Markdown content; refusing to overwrite "
            "manual or producer output - use the staged OpenWiki updater instead",
            file=sys.stderr,
        )
        return 1
    planned = ["index.md", "log.md", "quickstart.md", "INSTRUCTIONS.md", "concepts/repository-overview.md"]
    if args.dry_run:
        print("WOULD_CREATE " + ", ".join(planned))
        return 0
    concepts.mkdir(parents=True, exist_ok=True)

    commit = run_git(repo, "rev-parse", "HEAD")
    tracked = run_git(repo, "ls-files")
    tracked_count = 0 if tracked == "unknown" else len(tracked.splitlines())

    overview_body = frontmatter(
        "Repository Overview",
        "overview",
        ["repo", "architecture"],
        "Conservative OKF overview generated from repository metadata.",
    )
    overview_body += "# Repository Overview\n\n"
    overview_body += f"Source commit: `{commit}`.\n\n"
    overview_body += "This page is a skeleton generated without an LLM semantic producer. Validate and enrich it before treating it as authoritative.\n\n"
    overview_body += f"Tracked files at generation time: {tracked_count}.\n"
    (concepts / "repository-overview.md").write_text(overview_body, encoding="utf-8")

    for name, template in (("quickstart.md", "openwiki-quickstart.template.md"),
                           ("INSTRUCTIONS.md", "openwiki-INSTRUCTIONS.template.md")):
        (out / name).write_text((ASSETS / template).read_text(encoding="utf-8"), encoding="utf-8")

    index = '---\nokf_version: "0.1"\n---\n\n# Knowledge Bundle\n\n## Start\n\n'
    index += "* [Quickstart](quickstart.md) - Compact front door; read before deeper pages.\n"
    index += "* [Preservation contract](INSTRUCTIONS.md) - Update rules every refresh must preserve.\n"
    index += "\n## Concepts\n\n"
    for page in sorted(concepts.glob("*.md")):
        title = page.stem.replace("-", " ").title()
        index += f"* [{title}](concepts/{page.name}) - Generated concept page.\n"
    tooling = out / "tooling"
    if tooling.is_dir() and any(p.name not in {"index.md", "log.md"} for p in tooling.rglob("*.md")):
        # Root index must keep the bundle navigable, but tooling context stays a
        # clearly-labeled harness-specific outsider that concept pages never depend on.
        index += (
            "\n## Tooling context (harness-specific - do not treat as project truth)\n\n"
            "* [Tooling](tooling/) - Runtime/harness adapter context. Project concept pages must not depend on it.\n"
        )
    out.joinpath("index.md").write_text(index, encoding="utf-8")
    out.joinpath("log.md").write_text(
        "# Log\n\n"
        f"## {dt.date.today().isoformat()}\n\n"
        "* Generated conservative OKF skeleton from the Git inventory.\n",
        encoding="utf-8",
    )
    print(f"Wrote OKF skeleton to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
