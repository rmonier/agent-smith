#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Generate a conservative OKF wiki skeleton from a staged source pack.

This is a fallback for environments without LLM provider credentials.
It does not claim semantic completeness. By default it writes okf/wiki/ as the
zero-LLM floor for the OpenKB migration path.
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import subprocess


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
    parser.add_argument("--input", default="okf/.okf-build/input")
    parser.add_argument("--out", default="okf/wiki")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    input_dir = pathlib.Path(args.input).resolve()
    out = pathlib.Path(args.out).resolve()
    concepts = out / "concepts"
    refs = out / "references"
    concepts.mkdir(parents=True, exist_ok=True)
    refs.mkdir(parents=True, exist_ok=True)

    commit = run_git(repo, "rev-parse", "HEAD")
    graph_report = input_dir / "graphify-report.md"
    external_docs = sorted((input_dir / "external").glob("*.md")) if (input_dir / "external").exists() else []

    overview_body = frontmatter(
        "Repository Overview",
        "overview",
        ["repo", "architecture", "graphify"],
        "Conservative OKF overview generated from repository metadata and Graphify report.",
    )
    overview_body += "# Repository Overview\n\n"
    overview_body += f"Source commit: `{commit}`.\n\n"
    overview_body += "This page is a skeleton generated without an LLM semantic compiler. Validate and enrich it before treating it as authoritative.\n\n"
    if graph_report.exists():
        text = graph_report.read_text(encoding="utf-8", errors="replace")
        summary = "\n".join(text.splitlines()[:80])
        overview_body += "## Graphify report excerpt\n\n" + summary + "\n"
    (concepts / "repo-overview.md").write_text(overview_body, encoding="utf-8")

    if external_docs:
        body = frontmatter(
            "External Documentation Evidence",
            "reference-map",
            ["external-docs", "evidence"],
            "External documentation staged by the agent web tool for OKF enrichment.",
        )
        body += "# External Documentation Evidence\n\n"
        for doc in external_docs:
            body += f"- `{doc.name}`\n"
            (refs / doc.name).write_text(doc.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        body += "\nUse these files as evidence when expanding concept pages.\n"
        (concepts / "external-documentation-evidence.md").write_text(body, encoding="utf-8")

    index = '---\nokf_version: "0.1"\n---\n\n# Knowledge Bundle\n\n## Concepts\n\n'
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
        "* Generated conservative OKF skeleton from repository source pack.\n",
        encoding="utf-8",
    )
    print(f"Wrote OKF skeleton to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
