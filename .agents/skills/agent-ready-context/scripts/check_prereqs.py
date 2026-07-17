#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Preflight checks for the agent-ready-context skill.

This script intentionally avoids third-party dependencies so it can run in a
fresh repository. It checks hard requirements, optional tooling, companion
skills, and basic repository writability. It does not install, select, pin,
or repair tools; dependency review and pinning stay consent-first in the
documented workflow.

Run it with `uv run` so the PEP 723 metadata keeps it isolated from the
target repository's own environment; bare python3 works in degraded mode.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(cmd: list[str], cwd: Path, timeout: int = 10) -> tuple[bool, str]:
    exe = shutil.which(cmd[0])
    if not exe:
        return False, "not found"
    try:
        # Use the resolved path: on Windows, command shims can be found by
        # shutil.which but not resolved by subprocess when given the bare name.
        out = subprocess.run(
            [exe, *cmd[1:]],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        ).stdout.strip()
        return True, out.splitlines()[0] if out else "found"
    except Exception as exc:  # noqa: BLE001 - diagnostics only
        return False, f"error: {exc}"


def ensure_writable(path: Path) -> tuple[bool, str]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".agent-ready-context-write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return True, "writable"
    except Exception as exc:  # noqa: BLE001 - diagnostics only
        return False, f"not writable: {exc}"


def check_openwiki_config(repo: Path, result: dict[str, Any]) -> None:
    """Credential-home checks (existence and location only — .env files are
    checked by NAME, their contents never read).
    """
    group: dict[str, Any] = {}
    result["openwiki_config"] = group

    okf = repo / "okf"
    if not okf.is_dir():
        group["credential_homes"] = {"ok": True, "detail": "no okf/ yet - checked after bootstrap"}
        return

    kb_env = okf / ".openwiki" / ".env"
    # The staged wrapper redirects the child's home (HOME on POSIX, USERPROFILE
    # on Windows) to <repo>/okf, so pipeline runs resolve okf/.openwiki/.env. A
    # bare `openwiki` invocation outside the wrapper resolves the user-global
    # home instead; the two files are independent, never merged.
    home_env = Path.home() / ".openwiki" / ".env"
    kb_exists, home_exists = kb_env.exists(), home_env.exists()
    if kb_exists and home_exists:
        group["credential_homes"] = {
            "ok": True,
            "detail": "both okf/.openwiki/.env and ~/.openwiki/.env exist - staged runs resolve the project home by default (--credential-home user selects the classic home)",
        }
        result["notes"].append(
            "Two credential homes exist (okf/.openwiki/.env and ~/.openwiki/.env). They are independent "
            "and never merged: staged runs resolve the project home by default, or the classic user-global "
            "home with the staged runner's --credential-home user; keep only one authoritative to avoid confusion."
        )
    elif home_exists:
        group["credential_homes"] = {
            "ok": True,
            "detail": "using the user-global ~/.openwiki/.env (no project okf/.openwiki/.env) - select it with the staged runner's --credential-home user",
        }
    elif kb_exists:
        group["credential_homes"] = {"ok": True, "detail": "using project okf/.openwiki/.env"}
    else:
        group["credential_homes"] = {
            "ok": True,
            "detail": "no .env found - fine before first login; the stock login flow or provider env vars supply the route",
        }


def check(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    result: dict[str, Any] = {
        "repo": str(repo),
        "ok": True,
        "required": {},
        "optional": {},
        "companion_skills": {},
        "writable_paths": {},
        "notes": [],
    }

    py_ok = sys.version_info >= (3, 11)
    result["required"]["python>=3.11"] = {
        "ok": py_ok,
        "detail": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    }

    git_ok, git_detail = run(["git", "--version"], repo)
    result["required"]["git"] = {"ok": git_ok, "detail": git_detail}

    uv_ok, uv_detail = run(["uv", "--version"], repo)
    result["required"]["uv"] = {"ok": uv_ok, "detail": uv_detail}

    if git_ok:
        inside_ok, inside_detail = run(["git", "rev-parse", "--is-inside-work-tree"], repo)
        result["required"]["git-worktree"] = {
            "ok": inside_ok and inside_detail.strip() == "true",
            "detail": inside_detail,
        }
    else:
        result["required"]["git-worktree"] = {"ok": False, "detail": "git missing"}

    for name, cmd in {
        "fnm": ["fnm", "--version"],
        "node": ["node", "--version"],
        "corepack": ["corepack", "--version"],
        "pnpm": ["pnpm", "--version"],
        "openwiki": ["openwiki", "--version"],
    }.items():
        # openwiki's first invocation can spend longer than 10s on a cold
        # Node.js start; a short timeout would misreport it as missing.
        ok, detail = run(cmd, repo, timeout=60)
        result["optional"][name] = {"ok": ok, "detail": detail}

    check_openwiki_config(repo, result)

    companion_notes = {
        "skill-creator": "skill-creator is not present. OKF/AGENTS.md maintenance can continue, but repeated action skill creation is unavailable.",
        "subagent-profile-adapter": "subagent-profile-adapter is not present. Context maintenance can continue, but harness-specific subagent/profile adapters cannot be hydrated automatically.",
    }
    for companion, note in companion_notes.items():
        skill_md = repo / ".agents" / "skills" / companion / "SKILL.md"
        result["companion_skills"][companion] = {
            "ok": skill_md.exists(),
            "detail": str(skill_md.relative_to(repo)) if skill_md.exists() else "missing",
            "required": False,
        }
        if not skill_md.exists():
            result["notes"].append(note)

    for rel in ["okf/.okf-build", "okf", ".agents/skills"]:
        ok, detail = ensure_writable(repo / rel)
        result["writable_paths"][rel] = {"ok": ok, "detail": detail}

    hard_failed = []
    for name, data in result["required"].items():
        if not data["ok"]:
            hard_failed.append(name)
    for name, data in result["writable_paths"].items():
        if not data["ok"]:
            hard_failed.append(f"writable:{name}")

    if hard_failed:
        result["ok"] = False
        result["notes"].append("Missing hard requirements: " + ", ".join(hard_failed))

    if not result["required"]["uv"]["ok"]:
        result["notes"].append(
            "uv is a required prerequisite; ask the user to install it per "
            "https://docs.astral.sh/uv/getting-started/installation/ (source: https://github.com/astral-sh/uv). "
            "Bare python3 is a degraded fallback only when the user explicitly declines uv."
        )
    if not (result["optional"]["fnm"]["ok"] and result["optional"]["node"]["ok"]):
        result["notes"].append(
            "The producer Node runtime is optional; with user consent install user-scoped fnm "
            "(upstream source: https://github.com/Schniz/fnm) and a Node.js runtime meeting "
            "upstream's documented minimum. "
            "Without it, use the conservative skeleton generator."
        )
    if not result["optional"]["openwiki"]["ok"]:
        result["notes"].append(
            "OpenWiki is optional for semantic generation; with user consent install the pinned "
            "version per references/dependencies.md "
            "(upstream source: https://github.com/langchain-ai/openwiki). "
            "Without it, use the conservative skeleton generator."
        )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Check prerequisites for agent-ready-context.")
    parser.add_argument("--repo", default=".", help="Repository root, default: current directory")
    parser.add_argument("--json", action="store_true", help="Print full JSON diagnostics")
    args = parser.parse_args()

    result = check(Path(args.repo))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "OK" if result["ok"] else "FAILED"
        print(f"agent-ready-context prerequisites: {status}")
        for group in ["required", "optional", "openwiki_config", "companion_skills", "writable_paths"]:
            print(f"\n{group}:")
            for name, data in result[group].items():
                # ASCII markers: some Windows consoles use cp1252 and cannot print check marks.
                marker = "+" if data["ok"] else "!"
                req = " required" if data.get("required") else ""
                print(f"  {marker} {name}{req}: {data['detail']}")
        if result["notes"]:
            print("\nnotes:")
            for note in result["notes"]:
                print(f"  - {note}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
