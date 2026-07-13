#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Preflight checks for the agent-ready-context skill.

This script intentionally avoids third-party dependencies so it can run in a
fresh repository. It checks hard requirements, optional tooling, companion
skills, and basic repository writability.

Run it with `uv run` so the PEP 723 metadata keeps it isolated from the
target repository's own environment; bare python3 works in degraded mode.
"""
from __future__ import annotations

import argparse
import json
import os
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


# Project-shared config keys that must match between the committed example and
# the local config.yaml (they shape the compiled wiki for every contributor).
# Provider keys (model, litellm, timeout) are per-user and never compared.
SHARED_CONFIG_KEYS = ("language", "pageindex_threshold", "entity_types")


def _read_yaml_scalars(path: Path) -> dict[str, str]:
    """Top-level ``key: value`` scalars without a YAML dependency.

    Good enough for the shared-key drift check; nested blocks (litellm:) and
    lists keep their raw first-line value, which still compares stably.
    """
    values: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line or line.startswith((" ", "\t", "#")):
                continue
            key, sep, value = line.partition(":")
            if sep:
                values[key.strip()] = value.split("#", 1)[0].strip()
    except Exception:
        pass
    return values


def check_openkb_config(repo: Path, result: dict[str, Any]) -> None:
    """Config-surface and credential-home checks (existence and non-secret
    config only — .env files are checked by NAME, their contents never read).
    """
    group: dict[str, Any] = {}
    result["openkb_config"] = group

    okf = repo / "okf"
    example = okf / ".openkb" / "config.yaml.example"
    local = okf / ".openkb" / "config.yaml"
    if not okf.is_dir():
        group["config"] = {"ok": True, "detail": "no okf/ yet - checked after init"}
        return

    if example.exists() and not local.exists():
        group["config"] = {
            "ok": False,
            "detail": "config.yaml missing - copy config.yaml.example to config.yaml and choose a provider mode",
        }
        result["notes"].append(
            "okf/.openkb/config.yaml is per-user and uncommitted: create it from the committed "
            "config.yaml.example (see references/openkb-providers.md, 'Backend connection modes')."
        )
    elif example.exists() and local.exists():
        ex_vals = _read_yaml_scalars(example)
        loc_vals = _read_yaml_scalars(local)
        drifted = [
            k for k in SHARED_CONFIG_KEYS
            if k in ex_vals and loc_vals.get(k, ex_vals[k]) != ex_vals[k]
        ]
        if drifted:
            group["config"] = {
                "ok": False,
                "detail": "shared keys drifted from config.yaml.example: " + ", ".join(drifted),
            }
            result["notes"].append(
                "Project-shared config keys (" + ", ".join(drifted) + ") differ between your local "
                "config.yaml and the committed example - align them or the compiled wiki diverges "
                "between contributors. Provider keys (model/litellm/timeout) are yours to choose."
            )
        else:
            group["config"] = {"ok": True, "detail": "local config present, shared keys match example"}
    else:
        group["config"] = {
            "ok": True,
            "detail": "no config.yaml.example (pre-12.8 layout or KB not initialized)",
        }

    kb_env = okf / ".env"
    # openkb hardcodes Path.home()/.config/openkb on EVERY OS, Windows included
    # (openkb config.py GLOBAL_CONFIG_DIR) - do not "fix" this to %APPDATA%,
    # it must mirror where openkb actually looks.
    home_env = Path.home() / ".config" / "openkb" / ".env"
    kb_exists, home_exists = kb_env.exists(), home_env.exists()
    if kb_exists and home_exists:
        group["credential_homes"] = {
            "ok": True,
            "detail": "both okf/.env and ~/.config/openkb/.env exist - the project file wins for shared keys",
        }
        result["notes"].append(
            "Two credential homes exist (okf/.env and ~/.config/openkb/.env). openkb loads the "
            "project file first (it wins); keep only one authoritative to avoid confusion."
        )
    elif home_exists:
        group["credential_homes"] = {
            "ok": True,
            "detail": "using the user-global ~/.config/openkb/.env (no project okf/.env)",
        }
    elif kb_exists:
        group["credential_homes"] = {"ok": True, "detail": "using project okf/.env"}
    else:
        group["credential_homes"] = {
            "ok": True,
            "detail": "no .env found - fine for OAuth providers; key-based providers need LLM_API_KEY",
        }


def check(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    result: dict[str, Any] = {
        "repo": str(repo),
        "ok": True,
        "required": {},
        "optional": {},
        "vendored_tool_skills": {},
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
        "graphify": ["graphify", "--version"],
        "openkb": ["openkb", "--help"],
    }.items():
        # openkb's first invocation can spend well over 10s importing litellm;
        # a short timeout would misreport an installed CLI as missing.
        ok, detail = run(cmd, repo, timeout=60)
        result["optional"][name] = {"ok": ok, "detail": detail}

    # A tool's own agent skill must be vendored into the target repo before
    # this pipeline invokes that CLI: the vendored copy is what future agents
    # in this repo defer to when the pipeline is not installed. Only the main
    # CLI skill per tool is a precondition; optional family members (openkb
    # deck/critic skills) live under their own names and are never enforced.
    for tool in ["graphify", "openkb"]:
        skill_md = repo / ".agents" / "skills" / tool / "SKILL.md"
        vendored = skill_md.exists()
        cli_installed = result["optional"][tool]["ok"]
        if vendored:
            detail = str(skill_md.relative_to(repo))
        elif cli_installed:
            detail = "missing - vendor before first CLI use"
        else:
            detail = "missing (CLI not installed, not required yet)"
        result["vendored_tool_skills"][tool] = {
            "ok": vendored or not cli_installed,
            "detail": detail,
            "required": False,
        }
        if cli_installed and not vendored:
            result["notes"].append(
                f"The {tool} CLI is installed but its vendor skill is not vendored at "
                f".agents/skills/{tool}/. Vendor the pinned copy before the first {tool} "
                "CLI invocation (copy sources in references/dependencies.md, "
                "'Vendoring the toolchain skills')."
            )

    check_openkb_config(repo, result)

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

    for rel in ["okf/.okf-build/input", "okf", ".agents/skills"]:
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
    if not result["optional"]["graphify"]["ok"]:
        result["notes"].append(
            "graphify is optional; with user consent install it via `uv tool install 'graphifyy==<pinned-version>'` "
            "through the environment's configured Python index "
            "(package graphifyy, upstream source: https://github.com/safishamsi/graphify). "
            "Without it, source packs rely on git inventory and docs only."
        )
    if not result["optional"]["openkb"]["ok"]:
        result["notes"].append(
            "OpenKB is optional for semantic compilation; with user consent install it via "
            "`uv tool install 'openkb==<pinned-version>'` through the environment's configured Python index "
            "(package openkb, upstream source: https://github.com/VectifyAI/OpenKB). "
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
        for group in ["required", "optional", "vendored_tool_skills", "openkb_config", "companion_skills", "writable_paths"]:
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
