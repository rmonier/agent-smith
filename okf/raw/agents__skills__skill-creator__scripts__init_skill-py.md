---
type: "source-file"
title: ".agents/skills/skill-creator/scripts/init_skill.py"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/scripts/init_skill.py"
source_path: ".agents/skills/skill-creator/scripts/init_skill.py"
source_kind: "code"
source_hash: "sha256:9add532e863e5a39e31b38b15765dbcd9de79e0c581e31263c106116ba3743d9"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, code]
---

# .agents/skills/skill-creator/scripts/init_skill.py

~~~
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Initialize an Agent Skills compliant skill under .agents/skills by default."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if len(value) > 64:
        value = value[:64].strip("-")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new Agent Skills directory.")
    parser.add_argument("name", help="Skill name or title. It will be normalized to kebab-case.")
    parser.add_argument("--path", default=".agents/skills", help="Parent directory. Defaults to .agents/skills.")
    parser.add_argument("--resources", default="", help="Comma-separated optional directories: scripts,references,assets")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing skill directory")
    args = parser.parse_args()

    name = normalize_name(args.name)
    if not name or not NAME_RE.match(name) or "--" in name:
        raise SystemExit(f"invalid skill name after normalization: {name!r}")

    parent = Path(args.path)
    if not (parent.as_posix().endswith(".agents/skills") or ".agents" in parent.parts):
        raise SystemExit(f"refusing to write outside .agents/skills: {parent}")

    target = parent / name
    if target.exists() and not args.force:
        raise SystemExit(f"skill already exists: {target}. Use --force to allow updates.")
    target.mkdir(parents=True, exist_ok=True)

    skill_md = target / "SKILL.md"
    if not skill_md.exists() or args.force:
        skill_md.write_text(
            "---\n"
            f"name: {name}\n"
            "description: Performs a repeated action. Use when the agent/harness needs this specific workflow, validation, transformation, tool integration, or command sequence.\n"
            "license: MIT\n"
            "metadata:\n"
            "  version: \"0.1.0\"\n"
            "  owner: project\n"
            "---\n\n"
            f"# {name.replace('-', ' ').title()}\n\n"
            "Describe the repeated action this skill performs. Keep context in OKF and keep this file procedural.\n\n"
            "## Workflow\n\n"
            "1. Replace this with the first step.\n"
            "2. Use scripts/references/assets only when needed.\n"
            "3. Validate the result before finishing.\n\n"
            "## Commands\n\n```bash\n# add commands here\n```\n",
            encoding="utf-8",
        )

    requested = {x.strip() for x in args.resources.split(",") if x.strip()}
    invalid = requested - {"scripts", "references", "assets"}
    if invalid:
        raise SystemExit(f"invalid resources: {', '.join(sorted(invalid))}")
    for dirname in sorted(requested):
        (target / dirname).mkdir(exist_ok=True)

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~
