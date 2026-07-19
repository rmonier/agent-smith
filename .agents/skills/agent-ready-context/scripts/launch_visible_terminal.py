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
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

# subprocess.CREATE_NEW_CONSOLE/CREATE_NEW_PROCESS_GROUP are Windows-only:
# the attributes do not exist at all in the subprocess module on POSIX.
# launch_windows() is only ever called when the host is actually Windows in
# normal use, but referencing them as a bare module attribute still breaks
# importing/testing this file on POSIX (verified running this suite under
# WSL Ubuntu) - Python evaluates the attribute access when that line runs,
# not only when the branch is meaningful. getattr with a default of 0 (a
# no-op creationflags bit) keeps the module portable; the real values are
# always used on an actual Windows host, where they do exist.
_CREATE_NEW_CONSOLE = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
_CREATE_NEW_PROCESS_GROUP = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

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


# Preference order for the shell hosting a spawned Windows console: pwsh
# (PowerShell 7+, cross-platform edition) if present, then the always-present
# Windows PowerShell, falling back to cmd.exe - which needs no detection,
# since it ships on every Windows install. Same idea as xdg-terminal-exec on
# Linux: prefer whatever the user actually has over one hardcoded choice.
_WINDOWS_SHELLS: list[str] = ["pwsh", "powershell"]


def _sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def _powershell_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _applescript_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _pause_wrapped_sh(command: list[str], env_exports: dict[str, str]) -> str:
    exports = "".join(f"export {key}={_sh_quote(value)}; " for key, value in env_exports.items())
    inner = " ".join(_sh_quote(part) for part in command)
    return f"{exports}{inner}; echo; read -r -p 'Press Enter to close...' _"


def _pause_wrapped_powershell(command: list[str]) -> str:
    # Unlike the macOS/Linux shell wrapping, environment variables are not
    # injected textually here: launch_windows() passes the full env dict to
    # Popen directly (a normal child-process launch, no intermediary app like
    # Terminal.app in between), so the spawned pwsh/powershell process
    # already inherits everything it needs.
    inner = " ".join(_powershell_quote(part) for part in command)
    return f"& {inner}; Write-Host; Read-Host 'Press Enter to close...' | Out-Null"


def resolve_windows() -> tuple[str, str, str]:
    """Returns (description, resolved shell binary, mode); mode is "pwsh",
    "powershell", or "cmd". Always resolves to something - cmd.exe is part
    of every Windows install, so unlike the other platforms this never
    returns None.
    """
    for name in _WINDOWS_SHELLS:
        resolved = shutil.which(name)
        if resolved is not None:
            return (f"a new Windows console running {name}", resolved, name)
    return ("a new Windows console (cmd.exe)", "cmd.exe", "cmd")


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


def _write_temp_batch(command: list[str]) -> Path:
    # Popen(argv, ...) on Windows runs the whole argv through list2cmdline
    # itself to build the actual CreateProcess command line. Folding an
    # already-quoted command string into one more argv element (the earlier
    # `cmd.exe /c "<quoted command> & pause"` shape) put list2cmdline's
    # quoting through two passes: the inner quotes come out backslash-escaped
    # (\"), which cmd.exe's own primitive parser does not treat as an
    # escaped quote the way a C-runtime argv parser does - the two passes
    # fight and corrupt any argument that itself needed quoting (a --print
    # value containing " - " arrives at OpenWiki as a detached "-" token,
    # "Unknown option: -"). A short-lived batch file
    # sidesteps this: the pause and self-delete live inside the file as
    # plain lines, so launch_windows() only ever needs to quote the script's
    # own path (never anything with pre-existing quotes in it) - a single,
    # ordinary quoting pass, the same as any Windows program handling a
    # "C:\path with spaces\file" argument.
    inner = subprocess.list2cmdline(command)
    fd, path = tempfile.mkstemp(suffix=".bat", prefix="agent-ready-context-")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write("@echo off\r\n")
        handle.write(f"{inner}\r\n")
        handle.write("echo.\r\n")
        handle.write("pause\r\n")
        handle.write('del "%~f0"\r\n')
    return Path(path)


def launch_windows(command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.Popen | None:
    _description, shell_path, mode = resolve_windows()
    if mode == "cmd":
        script = _write_temp_batch(command)
        argv = [shell_path, "/c", str(script)]
    else:
        argv = [shell_path, "-NoProfile", "-Command", _pause_wrapped_powershell(command)]
    return subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        # CREATE_NEW_PROCESS_GROUP alongside CREATE_NEW_CONSOLE: lets a
        # caller that needs to stop this window early (terminate_process_tree)
        # deliver CTRL_BREAK_EVENT to the whole group - reaching the actual
        # command's process (e.g. node.exe), not just the console shell.
        creationflags=_CREATE_NEW_CONSOLE | _CREATE_NEW_PROCESS_GROUP,
    )


def launch_macos(command: list[str], cwd: Path, env_overrides: dict[str, str]) -> subprocess.Popen | None:
    if resolve_macos() is None:
        return None
    shell_command = f"cd {_sh_quote(str(cwd))}; {_pause_wrapped_sh(command, env_overrides)}"
    # Terminal.app's do script types this text into whatever the user's
    # default login shell is - zsh since macOS Catalina. zsh's own read
    # builtin gives -p a different meaning (read from a coprocess, not show
    # a prompt), so the read -r -p pause in _pause_wrapped_sh would silently
    # misbehave there. Force bash explicitly, exactly as launch_linux()
    # already does for the same reason, rather than depending on the user's
    # shell choice for a few lines of POSIX wrapper text; bash ships on
    # every Mac.
    bash_command = f"bash -c {_sh_quote(shell_command)}"
    script = f'tell application "Terminal" to do script {_applescript_quote(bash_command)}'
    # osascript itself is a one-shot command that hands the script to
    # Terminal.app and exits; the returned process is not the actual
    # long-running command, so terminate_process_tree() cannot target it
    # through this path. No known fix without extra Terminal.app-specific
    # scripting (asking Terminal for the new window/tab's own shell pid),
    # which is out of scope until this is actually needed on macOS.
    return subprocess.Popen(["osascript", "-e", script])


def launch_linux(command: list[str], cwd: Path, env: dict[str, str], env_overrides: dict[str, str]) -> subprocess.Popen | None:
    resolved = resolve_linux()
    if resolved is None:
        return None
    _description, binary, prefix_args = resolved
    shell_command = f"cd {_sh_quote(str(cwd))}; {_pause_wrapped_sh(command, env_overrides)}"
    return subprocess.Popen(
        [binary, *prefix_args, "bash", "-c", shell_command],
        cwd=cwd,
        env=env,
        # New session (== new process group, POSIX): lets terminate_process_tree
        # target the whole tree via os.killpg rather than just this one process.
        start_new_session=True,
    )


# Windows and POSIX signal modules only define their own platform's control
# events/signals; referencing the other platform's constant directly inside
# terminate_process_tree() would raise AttributeError as soon as that line
# executes, even inside a branch that is dead code on the current platform
# (Python evaluates attribute access at call time, not at parse time, and
# this module is imported/tested on Windows). getattr with a default keeps
# the module importable, and every branch exercisable under test, regardless
# of which OS actually runs it.
_CTRL_BREAK_EVENT = getattr(signal, "CTRL_BREAK_EVENT", None)
_SIGKILL = getattr(signal, "SIGKILL", None)


def terminate_process_tree(process: subprocess.Popen, grace_seconds: float = 5.0) -> bool:
    """Stop a launched window's whole process group. Tries a graceful stop
    first - CTRL_BREAK_EVENT on Windows or SIGTERM on POSIX, to the process
    group launch_windows()/launch_linux() created - and waits up to
    grace_seconds. Verified live that the graceful signal alone is not
    reliable: a spawned pwsh console did not respond to CTRL_BREAK_EVENT
    within the grace period. Escalates on timeout: `taskkill /T /F` on
    Windows (a builtin, not a third-party dependency - there is no pure
    Python stdlib way to force-kill an entire Windows process tree; only the
    single direct process, which can leave a grandchild like node.exe
    orphaned), or SIGKILL on POSIX (unlike SIGTERM, not catchable, so this
    escalation stays pure Python there).

    Not supported for macOS: launch_macos() hands the command to
    Terminal.app via osascript and returns osascript's own short-lived
    process, not the actual command's - there is nothing this function can
    target there yet.
    """
    if process.poll() is not None:
        return True
    system = platform.system()
    if system == "Windows":
        process.send_signal(_CTRL_BREAK_EVENT)
    elif system == "Linux":
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            return True
    else:
        # macOS: launch_macos() returned osascript's own process, not the
        # actual command's - nothing to signal. Left unsupported rather than
        # guessed at; the printed-command fallback still works there.
        return False
    try:
        process.wait(timeout=grace_seconds)
        return True
    except subprocess.TimeoutExpired:
        pass
    if system == "Windows":
        subprocess.run(
            ["taskkill", "/T", "/F", "/PID", str(process.pid)],
            capture_output=True,
            check=False,
        )
    else:
        try:
            os.killpg(os.getpgid(process.pid), _SIGKILL)
        except ProcessLookupError:
            return True
    try:
        process.wait(timeout=grace_seconds)
        return True
    except subprocess.TimeoutExpired:
        return False


def detect(system: str) -> str | None:
    if system == "Windows":
        return resolve_windows()[0]
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
