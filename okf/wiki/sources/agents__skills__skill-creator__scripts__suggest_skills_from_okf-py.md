---
type: "source-file"
title: ".agents/skills/skill-creator/scripts/suggest_skills_from_okf.py"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/scripts/suggest_skills_from_okf.py"
source_path: ".agents/skills/skill-creator/scripts/suggest_skills_from_okf.py"
source_kind: "code"
source_hash: "sha256:0defed6874fd8dec2e809c1e20088962d22a160fa2646f69503c26de86dc30e7"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, code]
---

# .agents/skills/skill-creator/scripts/suggest_skills_from_okf.py

~~~
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Suggest custom action skills from an OKF bundle using simple heuristics."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

ACTION_PATTERNS = [
    r"\b(run|execute|rerun|launch|invoke)\b",
    r"\b(validate|verify|check|test|lint)\b",
    r"\b(generate|scaffold|build|compile|export|import|convert|transform)\b",
    r"\b(refresh|update|sync|reconcile|rotate|migrate)\b",
    r"\b(graphify|openkb|terraform|kubectl|helm|docker|git|uv|python)\b",
]
SKIP_CONTEXT = ["architecture", "decision", "evidence", "overview", "concept", "external documentation"]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:64].strip("-") or "custom-action"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--okf", default="okf/wiki")
    parser.add_argument("--min-score", type=int, default=2)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    okf = (repo / args.okf).resolve()
    if not okf.is_dir():
        raise SystemExit(f"OKF directory not found: {okf}")

    candidates: Counter[str] = Counter()
    evidence: dict[str, list[str]] = {}
    for path in okf.rglob("*.md"):
        rel = path.relative_to(okf).as_posix()
        if path.name in {"index.md", "log.md"} or rel == "AGENTS.md":
            continue
        if rel.startswith("sources/") or rel.startswith("reports/"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        if any(skip in lower for skip in SKIP_CONTEXT) and "```" not in text:
            continue
        score = sum(len(re.findall(p, lower)) for p in ACTION_PATTERNS)
        if score < args.min_score:
            continue
        title = None
        for line in text.splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip('"')
                break
            if line.startswith("# "):
                title = line[2:].strip()
                break
        name = slugify(title or path.stem)
        if not any(v in name for v in ["run", "validate", "generate", "refresh", "sync", "build", "export", "import", "migrate", "check"]):
            name = "manage-" + name
        candidates[name] += score
        evidence.setdefault(name, []).append(path.relative_to(repo).as_posix())

    if not candidates:
        print("No repeated action candidates found. Keep the discovered material in OKF context.")
        return 0

    print("Suggested custom action skills:")
    for name, score in candidates.most_common():
        print(f"- {name}  score={score}")
        for src in evidence[name][:3]:
            print(f"  evidence: {src}")
        print(f"  init: uv run .agents/skills/skill-creator/scripts/init_skill.py {name} --path .agents/skills --resources scripts,references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~
