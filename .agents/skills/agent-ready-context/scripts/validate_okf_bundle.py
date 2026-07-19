#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Validate an OKF bundle against the local Google OKF v0.1 baseline.

Run with `uv run` so PyYAML is resolved automatically in an isolated
environment; with bare python3 the YAML checks degrade when PyYAML is absent.

This script implements the hard OKF v0.1 conformance checks known from
GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md. The agent should web-check
the official spec before relying on this local validator:
- every non-reserved Markdown file is a concept document;
- every concept document has parseable YAML frontmatter;
- every concept frontmatter has a non-empty `type` field;
- reserved `index.md` and `log.md` files are not concept documents and follow
  their respective structural rules when present;
- the bundle-root `index.md` may contain an `okf_version` frontmatter block.

Deterministic auditability checks beyond the spec (warnings, gate unchanged):
- unclosed code fence at end of file — the reliable signal for truncated or
  badly merged generated pages;
- sibling pages whose names collapse to the same normalized slug — likely
  near-duplicate concepts.

It is intentionally OS-agnostic and producer-neutral. Every Markdown file is
validated solely by its OKF role; vendor-specific compatibility modes belong
outside this conformance authority.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - environment dependent
    yaml = None

RESERVED = {"index.md", "log.md"}
DATE_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}\s*$")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def normalized_slug(stem: str) -> str:
    """Collapse a file stem for near-duplicate comparison (case, `_` vs `-`)."""
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def has_unclosed_fence(text: str) -> bool:
    """True when a code fence is still open at end of file."""
    open_fence: str | None = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        if open_fence is None:
            open_fence = marker[0]
        elif marker[0] == open_fence:
            open_fence = None
    return open_fence is not None


def split_frontmatter(text: str) -> tuple[str, str] | None:
    # OKF examples and spec use LF. Be permissive for CRLF by normalizing.
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return None
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return None
    return normalized[4:end], normalized[end + 5 :]


def load_yaml(raw: str, rel: str, errors: list[str]) -> dict[str, Any] | None:
    if yaml is None:
        errors.append(
            f"{rel}: cannot validate YAML parseability because PyYAML is not installed; "
            "install PyYAML to validate OKF YAML frontmatter locally"
        )
        return None
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:  # pragma: no cover - error formatting
        message = f"{rel}: invalid YAML frontmatter: {exc}"
        if "mapping values are not allowed here" in str(exc):
            message += (
                " - likely an unquoted colon inside a string value (title, description, ...); "
                "wrap that value in double quotes so it can't be misread as a nested mapping"
            )
        errors.append(message)
        return None
    if data is None:
        return {}
    if not isinstance(data, dict):
        errors.append(f"{rel}: YAML frontmatter must be a mapping/object")
        return None
    return data


def validate_index(path: Path, rel: str, text: str, errors: list[str], warnings: list[str]) -> None:
    parts = split_frontmatter(text)
    body = text
    if parts is not None:
        raw_fm, body = parts
        if rel != "index.md":
            errors.append(f"{rel}: non-root reserved index.md must not contain YAML frontmatter")
        else:
            fm = load_yaml(raw_fm, rel, errors)
            if fm is not None:
                if "okf_version" not in fm:
                    errors.append(f"{rel}: root index.md frontmatter is only permitted to declare okf_version")
                extra = sorted(set(fm) - {"okf_version"})
                if extra:
                    warnings.append(
                        f"{rel}: root index.md frontmatter should only contain okf_version; extra keys: {', '.join(extra)}"
                    )
                if fm.get("okf_version") and not isinstance(fm.get("okf_version"), str):
                    warnings.append(f"{rel}: okf_version should be a string such as '0.1'")
    # Spec says one or more sections grouping concepts. Keep as warning because
    # conformance says reserved files follow structure, but empty/generated roots
    # may be bootstrapped before concepts exist.
    headings = [line for line in body.replace("\r\n", "\n").splitlines() if line.startswith("#")]
    if not headings:
        warnings.append(f"{rel}: index.md should contain at least one Markdown heading")
    if not MD_LINK_RE.search(body):
        warnings.append(f"{rel}: index.md should enumerate entries with Markdown links")


def validate_log(
    rel: str,
    text: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    if split_frontmatter(text) is not None:
        errors.append(f"{rel}: reserved log.md must not contain YAML frontmatter")
    lines = text.replace("\r\n", "\n").splitlines()
    for line in lines:
        if not line.startswith("## "):
            continue
        if DATE_RE.match(line):
            continue
        errors.append(f"{rel}: log date heading must be ISO 8601 YYYY-MM-DD: {line}")
    if lines and not any(line.startswith("#") for line in lines):
        warnings.append(f"{rel}: log.md should contain a Markdown title/heading")


def validate_concept(
    path: Path,
    rel: str,
    text: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    parts = split_frontmatter(text)
    if parts is None:
        errors.append(f"{rel}: missing YAML frontmatter block")
        return
    raw_fm, body = parts
    fm = load_yaml(raw_fm, rel, errors)
    if fm is None:
        return
    value = fm.get("type")
    if value is None or (isinstance(value, str) and not value.strip()):
        errors.append(f"{rel}: missing non-empty required frontmatter field 'type'")
    elif not isinstance(value, str):
        warnings.append(f"{rel}: frontmatter field 'type' should be a short descriptive string")

    # Soft guidance from the spec; callers may make these warnings strict as a
    # producer-quality policy, but generic conformance does not require them.
    for field in ("title", "description"):
        if not fm.get(field):
            warnings.append(f"{rel}: missing recommended frontmatter field '{field}'")
    if not body.strip():
        warnings.append(f"{rel}: concept body is empty")


def validate_bundle(root: Path, *, strict_warnings: bool = False) -> tuple[list[str], list[str], int]:
    """Return generic OKF errors, warnings, and the Markdown file count."""
    root = root.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        return [f"not a directory: {root}"], [], 0
    md_files = sorted(root.rglob("*.md"))
    if not md_files:
        errors.append("bundle contains no Markdown files")

    checked: list[Path] = []
    for path in md_files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: not valid UTF-8: {exc}")
            continue

        checked.append(path)
        if has_unclosed_fence(text):
            warnings.append(f"{rel}: code fence still open at end of file (possible truncation or bad merge)")

        if path.name == "index.md":
            validate_index(path, rel, text, errors, warnings)
        elif path.name == "log.md":
            validate_log(rel, text, errors, warnings)
        else:
            validate_concept(path, rel, text, errors, warnings)

    # Near-duplicate sibling pages: same normalized slug in the same directory.
    by_dir: dict[tuple[Path, str], list[str]] = {}
    for path in checked:
        if path.name in RESERVED:
            continue
        by_dir.setdefault((path.parent, normalized_slug(path.stem)), []).append(path.name)
    for (parent, slug), names in sorted(by_dir.items(), key=lambda item: str(item[0])):
        if slug and len(names) > 1:
            rel_dir = parent.relative_to(root).as_posix()
            warnings.append(
                f"{rel_dir}: near-duplicate page names collapse to the same slug '{slug}': "
                + ", ".join(sorted(names))
            )

    if strict_warnings:
        errors.extend(f"warning treated as error: {w}" for w in warnings)
        warnings = []

    return errors, warnings, len(md_files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an OKF v0.1 bundle")
    parser.add_argument("bundle", help="Path to OKF bundle directory")
    parser.add_argument("--strict-warnings", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()
    errors, warnings, markdown_count = validate_bundle(
        Path(args.bundle),
        strict_warnings=args.strict_warnings,
    )

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if errors:
        print(f"OKF validation failed: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"OKF validation passed: {markdown_count} Markdown file(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
