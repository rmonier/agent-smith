#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Prepare a genuinely empty stage for establishing a first OpenWiki OAuth
session, and either print the command that does it in a visible terminal, or
(with --auto-close) launch it directly and close the window automatically
once the credential file appears - so completing this step correctly does
not depend solely on a human noticing and declining OpenWiki's own prompt to
continue into a full (billable) run.

OpenWiki's own first-run OAuth wizard only triggers against an empty
`openwiki/` target directory. The normal staged run
(`run_openwiki_staged.py --execute`) always copies the accepted `okf/wiki/`
into the stage's `openwiki/` path first, so incremental updates have prior
memory to work from - which means once a wiki already exists (built through
any provider), that same staged run can never trigger a first-time OAuth
login for a *different*, not-yet-credentialed provider: OpenWiki just asks
for a pre-set access-token env var instead of opening the browser flow, even
inside a real, visible, TTY-attached console with an otherwise-correct
environment.

This script is therefore deliberately decoupled from real content
generation: it only prepares a small, disposable, always-empty directory
under `okf/.okf-build/oauth-smoke/` and either prints, or runs, the command
that establishes a credential there. Establishing a session writes nothing
under `okf/wiki/` or `okf/external/` and is never itself promoted; run the
normal staged `--execute` flow afterward once a credential exists, for the
real content work - it will proceed non-interactively.

Consent-first by construction, not by this script, and in two steps, exactly
like launch_visible_terminal.py: run with --detect first to find out which
terminal mechanism *would* be used (and that a window would be auto-closed
once the credential appears) without launching anything, disclose that to
the user and get explicit approval, and only then run again with
--auto-close to actually do it.

One case is enforced structurally rather than left to that convention alone:
when is_wsl() is true, --auto-close refuses to launch anything (exit 3)
unless --acknowledge-wsl-risk is also passed. Printing a warning and then
launching anyway in the same call would give the calling agent no real
chance to stop and ask the user first - the window would already be open by
the time anyone read it. The refusal forces a genuinely separate call after
that conversation happens.
"""
from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import launch_visible_terminal as terminal_launcher

SCRIPT_DIR = Path(__file__).resolve().parent
SMOKE_DIR = Path("okf/.okf-build/oauth-smoke")

# How long a completed, stable credential file's size must stay unchanged
# before treating the write as finished - OpenWiki writes the file in one
# pass, but a size check taken mid-write could otherwise look "done" by
# coincidence between two fast polls.
_STABILITY_SECONDS = 2.0
_POLL_INTERVAL_SECONDS = 0.5


def _inside(repo: Path, path: Path, label: str) -> Path:
    """Resolve a path and require it to remain below the repository root."""
    root = repo.resolve(strict=True)
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"{label} escapes the repository: {resolved}") from exc
    return resolved


def prepare_smoke_dir(repo: Path) -> Path:
    """Create (or reset) the dedicated, always-empty session-establishment
    directory. Cleared every time, not just created-if-missing: a prior
    interrupted attempt could have left partial OpenWiki-managed content
    behind there, which would reintroduce the exact non-empty-directory
    problem this script exists to avoid.

    Also git-inits the directory. OpenWiki does not treat the literal
    working directory as its scope; it walks upward looking for the
    enclosing repository's `.git` and scopes itself to whatever it finds
    there. Without its own `.git`, a plain subdirectory of this repository
    resolves straight through to the real project root, and OpenWiki writes
    its onboarding output (a stray `openwiki/`, and CI scaffolding under
    `.github/workflows/`) there instead of into this throwaway directory -
    exactly the collision the isolated staged wrapper avoids by git-initing
    its own worktree (see `run_openwiki_staged.py`'s `prepare_stage`).
    A bare `git init` is enough: nothing here is ever added, committed, or
    promoted, so there is no history or remote to keep clean afterward.
    """
    smoke = _inside(repo, repo / SMOKE_DIR, "OAuth smoke directory")
    if smoke.exists():
        shutil.rmtree(smoke)
    smoke.mkdir(parents=True)
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git is not available")
    subprocess.run([git, "init"], cwd=smoke, check=True, capture_output=True, text=True)
    return smoke


def build_command(model_id: str, message: str) -> list[str]:
    return ["openwiki", "code", "--init", "--modelId", model_id, message]


def is_wsl() -> bool:
    """Detect WSL (Windows Subsystem for Linux). The OAuth callback here is
    a known, environment-configuration-dependent risk under WSL - not a
    universal failure: WSL2's mirrored networking mode, or an xdg-open
    configured to open a WSL-native browser instead of forwarding to
    Windows, can both avoid it. Checks the standard WSL_DISTRO_NAME env var
    WSL itself sets, falling back to the kernel release string (which
    upstream WSL kernels label with "microsoft") for invocations that might
    not inherit that env var.
    """
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    return "microsoft" in platform.uname().release.lower()


_WSL_WARNING = (
    "WARNING: this looks like WSL (Windows Subsystem for Linux). The OAuth "
    "callback here can fail to arrive depending on this environment's own "
    "networking configuration - not universal, and not confirmed either way "
    "for this specific machine. If a native Windows terminal is reachable, "
    "consider establishing the session there instead. Ask the user whether "
    "to continue here or fall back to native Windows before proceeding. If "
    "you continue and no credential file appears within a reasonable time "
    "after completing sign-in in the browser, that is the likely cause - "
    "fall back to a native Windows terminal rather than waiting indefinitely."
)


def credential_path(home: Path) -> Path:
    """Where OpenWiki writes its credential file for this HOME/USERPROFILE -
    matches OpenWiki's own `path.join(os.homedir(), ".openwiki", ".env")`
    (verified against the installed package's env.js)."""
    return home / ".openwiki" / ".env"


def wait_for_stable_file(
    path: Path,
    timeout: float,
    poll_interval: float = _POLL_INTERVAL_SECONDS,
    stability_seconds: float = _STABILITY_SECONDS,
) -> bool:
    """Poll for a file to exist and its size to stop changing, so a
    still-being-written file is never mistaken for a finished one. Returns
    False on timeout, leaving the caller's window untouched either way -
    a timeout means the human is still working through the wizard, not that
    something failed.
    """
    deadline = time.monotonic() + timeout
    last_size: int | None = None
    stable_since: float | None = None
    while time.monotonic() < deadline:
        if path.exists():
            size = path.stat().st_size
            if size == last_size:
                if stable_since is None:
                    stable_since = time.monotonic()
                elif time.monotonic() - stable_since >= stability_seconds:
                    return True
            else:
                stable_since = None
            last_size = size
        else:
            stable_since = None
            last_size = None
        time.sleep(poll_interval)
    return False


def launch(command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.Popen | None:
    system = platform.system()
    if system == "Windows":
        return terminal_launcher.launch_windows(command, cwd, env)
    if system == "Darwin":
        return terminal_launcher.launch_macos(command, cwd, env)
    if system == "Linux":
        return terminal_launcher.launch_linux(command, cwd, env, env)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare an empty stage to establish a first OpenWiki OAuth session.",
    )
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--model-id", required=True, help="Model to request for this session (openwiki --modelId)")
    parser.add_argument(
        "--provider",
        default="openai-chatgpt",
        help="OPENWIKI_PROVIDER value (default: openai-chatgpt, the only OAuth route in the pinned CLI)",
    )
    parser.add_argument(
        "--message",
        default="Establishing an OpenWiki credential. No repository content is present in this directory.",
        help="The prompt/brief text passed to openwiki",
    )
    parser.add_argument(
        "--detect",
        action="store_true",
        help="Report what --auto-close would do, without launching anything - "
        "run this first, disclose the answer, get approval, then run again with --auto-close",
    )
    parser.add_argument(
        "--auto-close",
        action="store_true",
        help="Launch the session directly and close the window automatically once the "
        "credential file appears and stabilizes, instead of just printing the command",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=600.0,
        help="Seconds to wait for the credential file before giving up on auto-close (default: 600)",
    )
    parser.add_argument(
        "--acknowledge-wsl-risk",
        action="store_true",
        help="Required to actually launch with --auto-close when is_wsl() is true - run --detect "
        "or a plain --auto-close attempt first, ask the user whether to continue or fall back, "
        "and only pass this flag after they say to continue. Ignored when WSL is not detected.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    home = _inside(repo, repo / "okf", "OpenWiki home")
    env_path = credential_path(home)

    if args.detect:
        description = terminal_launcher.detect(platform.system())
        if description is None:
            print(f"error: no terminal-launching mechanism found for platform {platform.system()!r}", file=sys.stderr)
            return 2
        print(f"{description}; window auto-closes once {env_path} appears and stabilizes")
        if is_wsl():
            print()
            print(_WSL_WARNING)
        return 0

    command = build_command(args.model_id, args.message)

    if not args.auto_close:
        smoke = prepare_smoke_dir(repo)
        print(f"Prepared an empty session-establishment directory: {smoke}")
        print()
        if is_wsl():
            print(_WSL_WARNING)
            print()
        print(
            "Run this through launch_visible_terminal.py's own --detect/launch "
            "steps (disclose the resolved mechanism and get approval first):"
        )
        print()
        print(
            f"uv run {SCRIPT_DIR / 'launch_visible_terminal.py'} --cwd {smoke} "
            f"--env HOME={home} --env USERPROFILE={home} "
            f"--env OPENWIKI_PROVIDER={args.provider} "
            f"--env OPENWIKI_TELEMETRY_DISABLED=1 --env DO_NOT_TRACK=1 "
            f"-- {' '.join(command)}"
        )
        print()
        print(
            "Tell the human completing this: leave every wizard field at its "
            "default (wiki scope/path, any repository-description prompt - "
            "none of it matters in this throwaway directory), and once the "
            "wizard shows the ChatGPT login step as done, close the window or "
            "decline any 'launch now?' prompt rather than letting a full run "
            "proceed. The credential is already written by that point; a full "
            "run here only spends real, billable provider usage generating "
            "wiki content nobody needs, describing an empty directory. Or use "
            "--auto-close instead of this printed command to have that "
            "handled automatically."
        )
        print()
        print(
            "Once the credential file exists (check_prereqs.py reports it under "
            "openwiki_config), the normal staged --execute run for the real "
            "corpus will proceed non-interactively - never rerun this script "
            "for that."
        )
        return 0

    if is_wsl() and not args.acknowledge_wsl_risk:
        # Hard gate, not just a printed note: printing this warning and then
        # launching anyway in the same call would give the calling agent no
        # real chance to stop and ask the user first - the window would
        # already be open by the time anyone read the warning. Refuse to
        # launch until a separate call passes --acknowledge-wsl-risk, which
        # only happens after that conversation.
        print(_WSL_WARNING, file=sys.stderr)
        print(
            "\nNot launching: pass --acknowledge-wsl-risk to proceed anyway, only after asking "
            "the user whether to continue here or fall back to a terminal on the same host as "
            "the callback listener.",
            file=sys.stderr,
        )
        return 3

    smoke = prepare_smoke_dir(repo)
    env = {
        "HOME": str(home),
        "USERPROFILE": str(home),
        "OPENWIKI_PROVIDER": args.provider,
        "OPENWIKI_TELEMETRY_DISABLED": "1",
        "DO_NOT_TRACK": "1",
    }
    full_env = os.environ.copy()
    full_env.update(env)

    process = launch(command, smoke, full_env)
    if process is None:
        print(
            f"error: no terminal-launching mechanism found for platform {platform.system()!r}. "
            "Fall back to the printed-command form (this script without --auto-close), "
            "or ask the user to run it themselves.",
            file=sys.stderr,
        )
        return 2

    print(f"Launched (pid {process.pid}); waiting up to {args.timeout:.0f}s for {env_path} ...")
    if not wait_for_stable_file(env_path, timeout=args.timeout):
        print(
            f"Credential file did not appear within {args.timeout:.0f}s. The window is still "
            "open - the human may still be completing sign-in. Not closing it; rerun this "
            "command later, or check on it directly.",
            file=sys.stderr,
        )
        return 1

    print("Credential file detected and stable. Closing the window...")
    if terminal_launcher.terminate_process_tree(process):
        print(
            "Closed. The normal staged --execute run for the real corpus will now proceed "
            "non-interactively - never rerun this script for that."
        )
        return 0
    print(
        "Credential was written, but the window did not respond to the graceful stop signal "
        "in time. It is safe to close manually now - the credential is already saved.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
