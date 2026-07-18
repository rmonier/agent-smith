#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Spawn a detached, visible terminal running an arbitrary command.

Generic, single-purpose: this script does not know about OpenWiki, OAuth, or
any other specific workflow. The caller constructs the full command and any
environment overrides; this script's only job is handing that command to a
real, visible terminal window so a human can interact with whatever it
prints or opens (a browser, an interactive prompt) - something the caller's
own tool-call stdio usually cannot provide, since that is captured and
returned to the caller, not shown live to a human.

Consent-first by construction, not by this script, and in two steps: run
with `--detect` first to find out which terminal mechanism *would* be used
without launching anything, disclose that specific answer to the user and
get explicit approval, and only then run again without `--detect` to
actually launch it. Detection and launching are deliberately separate calls
- which mechanism will be used cannot be disclosed honestly before it is
known, and it is only known once resolved. This script never simulates
keyboard or mouse input; it only launches a new, independent process the
human can see and use like any other window on their desktop.

The spawned window stays open after the command finishes (a trailing pause),
so the human can read the final output before closing it themselves.

Exit codes:
  0  detection found a mechanism (--detect), or a terminal was launched
  2  no terminal-launching mechanism was found for this platform (common on
     Linux); the caller should fall back to running the command through its
     own tool-call capability, and finally to asking the user to run the
     exact command themselves
  3  bad arguments (e.g. no command given, and not --detect)
"""
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# xdg-terminal-exec (freedesktop.org spec, not yet as universal as
# xdg-open) delegates to whatever terminal the user actually configured as
# their default - tried first because, when present, it is correct rather
# than a guess. Its own argv shape takes the command directly, no "-e"/"--"
# prefix needed.
_XDG_TERMINAL_EXEC = "xdg-terminal-exec"

# Fallback terminal emulators to try, in rough order of how likely they are
# to be present on a typical desktop. No single one is guaranteed present or
# configured; this is a best-effort list, not a claim of universal Linux
# support - there is no bash/sh-native way to spawn a new GUI window, since
# window creation is a windowing-system (X11/Wayland) concern, not a shell
# one.
_LINUX_TERMINALS: list[tuple[str, list[str]]] = [
    ("x-terminal-emulator", ["-e"]),
    ("gnome-terminal", ["--"]),
    ("konsole", ["-e"]),
    ("xfce4-terminal", ["-e"]),
    ("xterm", ["-e"]),
]


def parse_env_overrides(pairs: list[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"--env expects KEY=VALUE, got: {pair!r}")
        key, _, value = pair.partition("=")
        if not key:
            raise ValueError(f"--env expects a non-empty KEY, got: {pair!r}")
        overrides[key] = value
    return overrides


def _sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def _applescript_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _pause_wrapped_sh(command: list[str], env_exports: dict[str, str]) -> str:
    exports = "".join(f"export {key}={_sh_quote(value)}; " for key, value in env_exports.items())
    inner = " ".join(_sh_quote(part) for part in command)
    return f"{exports}{inner}; echo; read -r -p 'Press Enter to close...' _"


def resolve_windows() -> str:
    # cmd.exe is part of every Windows install; nothing to detect.
    return "a new Windows console (cmd.exe)"


def resolve_macos() -> str | None:
    if shutil.which("osascript") is None:
        return None
    return "Terminal.app (via osascript)"


def resolve_linux() -> tuple[str, str, list[str]] | None:
    """Returns (description, resolved binary path, prefix args) or None."""
    xdg_terminal_exec = shutil.which(_XDG_TERMINAL_EXEC)
    if xdg_terminal_exec is not None:
        return ("your configured default terminal (via xdg-terminal-exec)", xdg_terminal_exec, [])
    for binary, prefix_args in _LINUX_TERMINALS:
        resolved = shutil.which(binary)
        if resolved is not None:
            return (binary, resolved, prefix_args)
    return None


def launch_windows(command: list[str], cwd: Path, env: dict[str, str]) -> bool:
    inner = subprocess.list2cmdline(command)
    subprocess.Popen(
        ["cmd.exe", "/c", f"{inner} & pause"],
        cwd=cwd,
        env=env,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    return True


def launch_macos(command: list[str], cwd: Path, env_overrides: dict[str, str]) -> bool:
    if resolve_macos() is None:
        return False
    shell_command = f"cd {_sh_quote(str(cwd))}; {_pause_wrapped_sh(command, env_overrides)}"
    script = f'tell application "Terminal" to do script {_applescript_quote(shell_command)}'
    subprocess.Popen(["osascript", "-e", script])
    return True


def launch_linux(command: list[str], cwd: Path, env: dict[str, str], env_overrides: dict[str, str]) -> bool:
    resolved = resolve_linux()
    if resolved is None:
        return False
    _description, binary, prefix_args = resolved
    shell_command = f"cd {_sh_quote(str(cwd))}; {_pause_wrapped_sh(command, env_overrides)}"
    subprocess.Popen([binary, *prefix_args, "bash", "-c", shell_command], cwd=cwd, env=env)
    return True


def detect(system: str) -> str | None:
    if system == "Windows":
        return resolve_windows()
    if system == "Darwin":
        return resolve_macos()
    if system == "Linux":
        resolved = resolve_linux()
        return resolved[0] if resolved else None
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Spawn a detached, visible terminal running a command - generic, not workflow-specific.",
    )
    parser.add_argument("--cwd", default=".", help="Working directory for the spawned command")
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Environment variable to set for the spawned command only (repeatable)",
    )
    parser.add_argument(
        "--detect",
        action="store_true",
        help="Print which terminal mechanism would be used, without launching anything - "
        "run this first, disclose the answer, get approval, then run again without --detect",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command to run, after --")
    args = parser.parse_args()

    system = platform.system()

    if args.detect:
        description = detect(system)
        if description is None:
            print(f"error: no terminal-launching mechanism found for platform {system!r}", file=sys.stderr)
            return 2
        print(description)
        return 0

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("error: no command given - pass it after --, or use --detect", file=sys.stderr)
        return 3

    try:
        overrides = parse_env_overrides(args.env)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    cwd = Path(args.cwd).resolve()
    env = os.environ.copy()
    env.update(overrides)

    if system == "Windows":
        launched = launch_windows(command, cwd, env)
    elif system == "Darwin":
        launched = launch_macos(command, cwd, overrides)
    elif system == "Linux":
        launched = launch_linux(command, cwd, env, overrides)
    else:
        launched = False

    if not launched:
        print(
            f"error: no terminal-launching mechanism found for platform {system!r}. "
            "Fall back to running the command through the harness's own tool-call "
            "capability, and finally to asking the user to run it themselves in "
            "their own terminal:\n"
            f"  cwd: {cwd}\n"
            f"  env overrides: {overrides}\n"
            f"  command: {' '.join(command)}",
            file=sys.stderr,
        )
        return 2

    print(f"launched in a new {system} terminal: {' '.join(command)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
