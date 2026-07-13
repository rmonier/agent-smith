---
type: "source-file"
title: ".agents/skills/skill-creator/scripts/quick_validate.py"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/scripts/quick_validate.py"
source_path: ".agents/skills/skill-creator/scripts/quick_validate.py"
source_kind: "code"
source_hash: "sha256:0a64b81c5b8ef6ae3f7890cbd7fd0353c939731afc1a41192fa6159c333d4dd1"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, code]
---

# .agents/skills/skill-creator/scripts/quick_validate.py

~~~
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Validate a basic Agent Skills directory."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", help="Path to a skill directory")
    args = parser.parse_args()

    root = Path(args.skill)
    errors: list[str] = []
    if not root.is_dir():
        errors.append(f"not a directory: {root}")
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        errors.append("missing SKILL.md")
    data = {}
    if skill_md.exists():
        try:
            data = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(str(exc))

    name = data.get("name", "")
    desc = data.get("description", "")
    if not name:
        errors.append("missing required frontmatter field: name")
    elif not NAME_RE.match(name) or "--" in name:
        errors.append(f"invalid name: {name}")
    elif root.name != name:
        errors.append(f"directory name {root.name!r} must match frontmatter name {name!r}")
    if not desc:
        errors.append("missing required frontmatter field: description")
    elif len(desc) > 1024:
        errors.append("description exceeds 1024 characters")
    if len(name) > 64:
        errors.append("name exceeds 64 characters")
    compat = data.get("compatibility", "")
    if compat and len(compat) > 500:
        errors.append("compatibility exceeds 500 characters")

    if not (root.parent.as_posix().endswith(".agents/skills") or ".agents" in root.parts):
        errors.append("skill must be placed under .agents/skills")

    for sub in ["scripts", "references", "assets"]:
        d = root / sub
        if d.exists() and not d.is_dir():
            errors.append(f"{sub} exists but is not a directory")

    if errors:
        for e in errors:
            print(f"error: {e}")
        return 1
    print(f"valid skill: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~
