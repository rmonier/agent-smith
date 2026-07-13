#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Non-interactive `openkb init`, working around a Windows-only hang.

Upstream bug (verified against openkb 0.4.4's installed `openkb/cli.py`,
`init()`): the model and language prompts are both gated by a
`_stdin_is_tty()` check ("skip optional openkb init prompts when input is
piped or redirected" — its own docstring), but the API-key prompt a few
lines below has no such gate:

    api_key = click.prompt(
        "LLM API Key (saved to .env, enter to skip)",
        default="", hide_input=True, show_default=False,
    ).strip()

`hide_input=True` routes through Python's stdlib `getpass.getpass()`. On
Windows, `win_getpass()` reads keystrokes directly from the console via
`msvcrt.getwch()`, bypassing redirected/piped stdin entirely — so
`echo | openkb init --model ... --language ...` hangs forever waiting for a
keypress a pipe can never deliver. (On Unix this already works: when the
`termios` handshake fails on a non-tty fd, `unix_getpass()` falls back to
reading a line from `sys.stdin`.) There is no `--api-key`/`--no-input` flag
and no environment-variable bypass for this specific prompt in openkb 0.4.4.

This script never wants to supply a key interactively in the first place —
this skill's credential policy is hands-off end to end (see
`references/openkb-providers.md`: never ask for, read, print, or write key
values; point the user at `LLM_API_KEY`/`.env` instead). So the fix is not
Windows-specific plumbing, it is always skipping that prompt: monkeypatch
`click.prompt` to return its own `default` (i.e. always "press Enter"), then
call `openkb.cli.init`'s underlying function directly. With `default=""` on
the API-key prompt, this is byte-identical to a human choosing "enter to
skip" interactively — `api_key` resolves to `""` and `init()`'s own
`if api_key:` guard (cli.py) skips the `.env` write. No credential value is
ever read, generated, or supplied.

Calling `init.callback(...)` directly bypasses Click's own option-callback
pipeline, which is where `--model`/`--language` normally get sanitized via
`_coerce_model`/`_coerce_language` (openkb/cli.py: these strip and validate
the strings, rejecting control characters and excessive length, "because
[they are] interpolated into LLM system prompts" — a prompt-injection guard,
not just cosmetics). The vendor runner below calls the same two coercion
functions explicitly before invoking the callback, so that guard still
applies even though the callback path itself does not.

Same execution shape as `editorial_pass.py`'s vendor calls: this is executed
by the *installed openkb tool venv's own interpreter* (found via
`uv tool dir`), never by a `uv run`-resolved isolated environment — openkb's
dependency graph pins a prerelease (`pageindex==0.3.0.dev3`), so declaring
`openkb` as this script's own PEP 723 dependency would force a second,
separate resolution of that same prerelease constraint on every run instead
of reusing the tool install already done per `references/dependencies.md`.

Private-API risk: `openkb.cli._coerce_model`, `openkb.cli._coerce_language`,
and calling `init.callback()` instead of going through openkb's public CLI
entrypoint all depend on internals with no stability contract. Rather than
hardcoding a second, independent copy of the pinned version here (this
repo's actual pin lives in one place — the toolchain pin table in root
`AGENTS.md` — and duplicating it risks drifting from a deliberately reviewed
pin bump there), the vendor runner checks for the symbols themselves and
fails loudly (never silently, `missing_symbols` status) if any are absent —
that check is self-maintaining across openkb versions and does not need a
version-string update every time the pin changes. Re-verify this script
against `openkb/cli.py`'s `init()` source whenever `AGENTS.md`'s openkb pin
moves, the same way `editorial_pass.py`'s mirrored-fallback comment asks for
a re-diff after upgrades — `missing_symbols` or a vendor-runner crash is the
signal that a re-verify is actually due, not a version-string mismatch.

Usage:

    uv run scripts/init_openkb_noninteractive.py <kb_dir> \\
        --model <litellm-model> --language <lang>

Idempotent: if `<kb_dir>/.openkb/` already exists, this is a no-op (matches
`openkb init`'s own behavior) and prints `ALREADY_INITIALIZED` instead of
`INIT_OK`. Exit codes: 0 success (fresh init or already-initialized),
2 environment problem (openkb tool venv not found, private API missing,
invalid --model/--language).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Executed by the *installed openkb tool venv's* interpreter (see
# openkb_python() below), so every import resolves to the pinned vendor code
# in its native environment rather than a freshly resolved one.
_VENDOR_RUNNER = """\
import importlib.metadata as md
import json
import os
import sys

kb_dir, model_arg, language_arg = sys.argv[1], sys.argv[2], sys.argv[3]
result = {"openkb_version": md.version("openkb")}

try:
    import click
    import openkb.cli as cli_mod
except ImportError as exc:
    result["status"] = "import_error"
    result["detail"] = str(exc)
    print(json.dumps(result))
    raise SystemExit(0)

missing = [n for n in ("init", "_coerce_model", "_coerce_language") if not hasattr(cli_mod, n)]
if missing:
    result["status"] = "missing_symbols"
    result["detail"] = ", ".join(missing)
    print(json.dumps(result))
    raise SystemExit(0)

try:
    model = cli_mod._coerce_model(model_arg)
    language = cli_mod._coerce_language(language_arg)
except click.BadParameter as exc:
    result["status"] = "bad_parameter"
    result["detail"] = str(exc)
    print(json.dumps(result))
    raise SystemExit(0)

os.makedirs(kb_dir, exist_ok=True)
if os.path.isdir(os.path.join(kb_dir, ".openkb")):
    result["status"] = "already_initialized"
    print(json.dumps(result))
    raise SystemExit(0)

original_cwd = os.getcwd()
original_prompt = click.prompt


def _skip_prompt(*_args, **kwargs):
    return kwargs.get("default", "")


os.chdir(kb_dir)
click.prompt = _skip_prompt
try:
    cli_mod.init.callback(model=model, language=language)
finally:
    click.prompt = original_prompt
    os.chdir(original_cwd)

result["status"] = "ok"
print(json.dumps(result))
"""


def openkb_python() -> Path | None:
    """Interpreter of the installed openkb uv tool venv, if any."""
    try:
        out = subprocess.run(
            ["uv", "tool", "dir"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    root = Path(out.stdout.strip()) / "openkb"
    for cand in (root / "Scripts" / "python.exe", root / "bin" / "python"):
        if cand.exists():
            return cand
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize an OpenKB knowledge base non-interactively, "
        "skipping the API-key prompt that hangs on Windows under non-interactive stdin."
    )
    parser.add_argument("kb_dir", help="Knowledge base root (created if missing).")
    parser.add_argument(
        "--model", required=True, help="LiteLLM provider/model string, e.g. chatgpt/responses/gpt-5.4-mini"
    )
    parser.add_argument("--language", required=True, help="Wiki output language, e.g. en")
    args = parser.parse_args()

    py = openkb_python()
    if py is None:
        print(
            "ENVIRONMENT ERROR: installed openkb tool venv not found via `uv tool dir`; "
            "install openkb per references/dependencies.md first.",
            file=sys.stderr,
        )
        return 2

    proc = subprocess.run(
        [str(py), "-c", _VENDOR_RUNNER, str(Path(args.kb_dir)), args.model, args.language],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        print(
            f"ENVIRONMENT ERROR: vendor runner crashed (exit {proc.returncode}) — the "
            "installed openkb may be broken or an unexpected version. "
            f"Re-verify against the installed version's source.\n--- stderr ---\n{proc.stderr}",
            file=sys.stderr,
        )
        return 2

    try:
        result = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        print(f"ENVIRONMENT ERROR: could not parse vendor runner output.\n{proc.stdout}\n{proc.stderr}", file=sys.stderr)
        return 2

    version = result.get("openkb_version", "unknown")

    status = result.get("status")
    if status == "ok":
        print("INIT_OK")
        return 0
    if status == "already_initialized":
        print("ALREADY_INITIALIZED")
        return 0
    if status == "import_error":
        print(f"ENVIRONMENT ERROR: could not import click/openkb.cli: {result.get('detail')}", file=sys.stderr)
        return 2
    if status == "missing_symbols":
        print(
            f"ENVIRONMENT ERROR: openkb.cli.{result.get('detail')} not found in installed "
            f"openkb {version} — this workaround targets private internals that may have "
            "moved. Re-verify against the installed version's source before proceeding.",
            file=sys.stderr,
        )
        return 2
    if status == "bad_parameter":
        print(f"Invalid --model/--language value: {result.get('detail')}", file=sys.stderr)
        return 2

    print(f"ENVIRONMENT ERROR: unexpected vendor runner result: {result}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
