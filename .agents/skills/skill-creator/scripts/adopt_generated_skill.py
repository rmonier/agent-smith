#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Adopt an OpenKB Skill Factory skill from okf/output/skills/ into .agents/skills/."""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy a generated skill into .agents/skills/ and validate it."
    )
    parser.add_argument("name", help="Skill directory name under the source location")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--source", default="okf/output/skills")
    parser.add_argument("--dest", default=".agents/skills")
    parser.add_argument(
        "--force", action="store_true",
        help="Replace an existing skill of the same name (destructive; review first)",
    )
    args = parser.parse_args()

    if not NAME_RE.match(args.name) or "--" in args.name:
        print(f"error: invalid skill name: {args.name}", file=sys.stderr)
        return 2

    repo = pathlib.Path(args.repo).resolve()
    src = repo / args.source / args.name
    dest = repo / args.dest / args.name

    if not (src / "SKILL.md").is_file():
        print(f"error: no skill at {src} (missing SKILL.md)", file=sys.stderr)
        return 2
    fresh_copy = not dest.exists()
    if not fresh_copy and not args.force:
        print(
            f"error: {dest} already exists; review the differences and rerun with --force to replace it",
            file=sys.stderr,
        )
        return 2

    if not fresh_copy:
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"Copied {src.relative_to(repo).as_posix()} -> {dest.relative_to(repo).as_posix()}")

    validator = pathlib.Path(__file__).resolve().parent / "quick_validate.py"
    result = subprocess.run([sys.executable, str(validator), str(dest)])
    if result.returncode != 0:
        if fresh_copy:
            shutil.rmtree(dest, ignore_errors=True)
            print("Validation failed; removed the copied skill (source left untouched).", file=sys.stderr)
        else:
            print("Validation failed; fix or remove the replaced skill.", file=sys.stderr)
        return 1

    print(
        "Adopted. Before committing, review it against skill-creator standards: "
        "trigger-style description, minimal scoped allowed-tools, untrusted-content handling, no secrets."
    )
    print(
        "Caveat check: compare the skill against the wiki pages it distilled "
        "(okf/wiki/ concepts, entities, and their sources). Constraints, boundaries, and warnings "
        "must survive distillation; restore any that were flattened by editing the adopted copy "
        "(it is project-owned) before committing."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
