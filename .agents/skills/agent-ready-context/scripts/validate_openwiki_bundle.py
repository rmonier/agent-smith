#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Thin OpenWiki layout adapter over the producer-neutral OKF validator."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from validate_okf_bundle import validate_bundle

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _routes_to_quickstart(index: Path) -> bool:
    try:
        text = index.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    for raw in MARKDOWN_LINK_RE.findall(text):
        target = raw.strip().strip("<>").split(maxsplit=1)[0]
        split = urlsplit(target)
        if split.scheme or split.netloc:
            continue
        path = unquote(split.path).replace("\\", "/").lstrip("/")
        if path.startswith("openwiki/"):
            path = path.removeprefix("openwiki/")
        if path in {"quickstart", "quickstart.md"}:
            return True
    return False


def validate_openwiki(bundle: Path) -> list[str]:
    """Return producer-layout errors after generic OKF validation."""
    root = bundle.expanduser().resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f"not a directory: {root}"]
    generic_errors, _warnings, _count = validate_bundle(root)
    errors.extend("generic OKF: " + error for error in generic_errors)
    index = root / "index.md"
    quickstart = root / "quickstart.md"
    if not index.is_file():
        errors.append("missing canonical index.md")
    if not quickstart.is_file():
        errors.append("missing subordinate quickstart.md")
    if index.is_file() and quickstart.is_file() and not _routes_to_quickstart(index):
        errors.append("canonical index.md must route to quickstart.md")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OpenWiki Markdown as a canonical OKF bundle")
    parser.add_argument("path", nargs="?", help="Bundle path (default: <repo>/<bundle>)")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--bundle", default="okf/wiki", help="Bundle relative to --repo")
    args = parser.parse_args()
    bundle = Path(args.path).expanduser() if args.path else Path(args.repo).expanduser() / args.bundle
    errors = validate_openwiki(bundle)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        print(f"OpenWiki OKF validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("OpenWiki OKF validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
