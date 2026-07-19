#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Run stock OpenWiki against a disposable, no-remote repository.

The default action is a dry-run inventory. ``--execute`` copies the current
Git-tracked worktree byte-for-byte into an isolated repository, seeds the
accepted OKF wiki as stock ``openwiki/`` input, and executes the literal
OpenWiki argv supplied after ``--``. The adapter never reads provider state and
does not select a provider or model. By default HOME and USERPROFILE point at
``okf/`` so OpenWiki owns its normal ``okf/.openwiki/`` local state;
``--credential-home user`` keeps the classic user-global ``~/.openwiki/`` home
with the same standing.

Generated Markdown is mapped to a review candidate. Promotion is a separate,
explicit, transactional Markdown-only operation. No vendor source is changed.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence
from urllib.parse import unquote, urlsplit, urlunsplit

import yaml

from validate_openwiki_bundle import validate_openwiki


SCRIPT_DIR = Path(__file__).resolve().parent
INSTRUCTIONS_TEMPLATE = SCRIPT_DIR.parent / "assets" / "openwiki-INSTRUCTIONS.template.md"
BUILD_ROOT = "okf/.okf-build"
STOCK_WIKI = "openwiki"
CANONICAL_WIKI = PurePosixPath("okf/wiki")
LOCAL_STATE = PurePosixPath("okf/.openwiki/.last-update.json")
STOCK_STATE = PurePosixPath("openwiki/.last-update.json")
INSTRUCTIONS = "INSTRUCTIONS.md"
# Producer scratch files the stock agent is told to delete before finishing
# (OpenWiki writes a temporary openwiki/_plan.md during a run). A compliant run
# removes them; dropping any straggler defensively keeps an LLM slip from
# tripping the citation gate on a non-knowledge file.
STOCK_SCRATCH = {"_plan.md"}

# Structural exclusions only: Git metadata, this adapter's own build root,
# canonical memory, and the stage's reserved producer path. Anything else a
# repository should keep away from the provider (evaluation
# directories, private docs) is the operating agent's job via --exclude.
ROOT_EXCLUDES = {
    ".git",
    "okf",
    "openwiki",
}
GENERATED_DIRS = {
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "cache",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "venv",
}
SECRET_NAMES = {".env", ".npmrc", ".pypirc", "credentials.json", "secrets.json", "token.json"}
SECRET_SUFFIXES = {".key", ".p12", ".pfx", ".pem"}
SAFE_ENV_SUFFIXES = (".example", ".sample", ".template")
SAME_RUN_ONBOARDING = {
    ".github/workflows/openwiki-update.yml",
    "AGENTS.md",
    "CLAUDE.md",
}
LINK_RE = re.compile(r"(\]\(\s*<?)([^)\s>]+)(>?\s*\))")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CITATION_HEADING_RE = re.compile(r"^##\s+(?:citations?|sources?|evidence)\s*$", re.IGNORECASE)
# The first backticked span in a citation bullet is the staged path; a short
# annotation before or after it is allowed and ignored.
CITATION_BULLET_RE = re.compile(r"^\s*[-+*]\s+[^`]*`([^`]+)`.*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class TrackedFile:
    path: str
    mode: str


@dataclass
class Corpus:
    files: list[TrackedFile] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    unsupported: list[str] = field(default_factory=list)


def _git(repo: Path, *args: str, capture: bool = True) -> subprocess.CompletedProcess[str]:
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git is not available")
    completed = subprocess.run(
        [git, "-c", f"safe.directory={repo.as_posix()}", *args],
        cwd=repo,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    if completed.returncode:
        detail = (completed.stderr or completed.stdout or "git failed").strip()
        raise RuntimeError(detail)
    return completed


def _clean_run_id(value: str | None) -> str:
    if value is None:
        return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", value):
        raise ValueError("run-id must match [A-Za-z0-9][A-Za-z0-9._-]{0,63}")
    return value


def _normalize_exclude(value: str) -> str:
    normalized = value.replace("\\", "/").strip("/")
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe exclude path: {value!r}")
    return path.as_posix().casefold()


def _secret_like(rel: str) -> bool:
    name = PurePosixPath(rel).name.casefold()
    if name in SECRET_NAMES or PurePosixPath(name).suffix in SECRET_SUFFIXES:
        return True
    if name.startswith(".env.") and not name.endswith(SAFE_ENV_SUFFIXES):
        return True
    return False


def _excluded(rel: str, user_excludes: Iterable[str]) -> bool:
    folded = rel.casefold()
    parts = PurePosixPath(folded).parts
    # okf/ is canonical memory and never corpus material, with one carve-out:
    # okf/external/ holds reviewed, tracked external-evidence documents that
    # exist precisely to be staged and cited.
    if folded == "okf/external" or folded.startswith("okf/external/"):
        pass
    elif parts and parts[0] in ROOT_EXCLUDES:
        return True
    if any(part in GENERATED_DIRS for part in parts[:-1]):
        return True
    if _secret_like(rel):
        return True
    for prefix in user_excludes:
        if folded == prefix or folded.startswith(prefix + "/"):
            return True
    return False


def collect_corpus(repo: Path, excludes: Iterable[str] = ()) -> Corpus:
    """Inventory Git-tracked regular files without decoding their content."""
    root = repo.expanduser().resolve()
    user_excludes = tuple(_normalize_exclude(value) for value in excludes)
    listing = _git(root, "ls-files", "-s", "-z").stdout
    result = Corpus()
    for entry in listing.split("\0"):
        if not entry:
            continue
        metadata, separator, rel = entry.partition("\t")
        if not separator:
            raise RuntimeError("unexpected git ls-files output")
        mode = metadata.split(" ", 1)[0]
        rel = PurePosixPath(rel.replace("\\", "/")).as_posix()
        if _excluded(rel, user_excludes):
            result.excluded.append(rel)
            continue
        if mode not in {"100644", "100755"}:
            result.unsupported.append(rel)
            continue
        source = _inside(root, root / PurePosixPath(rel), f"tracked path {rel}")
        if not source.exists():
            result.missing.append(rel)
            continue
        if source.is_symlink() or not source.is_file():
            result.unsupported.append(rel)
            continue
        result.files.append(TrackedFile(rel, mode))
    result.files.sort(key=lambda item: item.path)
    result.excluded.sort()
    result.missing.sort()
    result.unsupported.sort()
    return result


def _is_linklike(path: Path) -> bool:
    """Recognize symlinks and Windows reparse-point junctions."""
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    if callable(is_junction) and is_junction():
        return True
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _inside(repo: Path, path: Path, label: str) -> Path:
    """Resolve a path and require it to remain below the repository root."""
    root = repo.resolve(strict=True)
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"{label} escapes the repository: {resolved}") from exc
    return resolved


def _read_regular_optional(path: Path, label: str) -> bytes | None:
    if not path.exists() and not path.is_symlink():
        return None
    if _is_linklike(path) or not path.is_file():
        raise RuntimeError(f"{label} must be a regular file: {path}")
    return path.read_bytes()


def markdown_snapshot(root: Path) -> dict[str, bytes]:
    """Read regular Markdown files only, rejecting linked output paths."""
    if not root.is_dir():
        return {}
    result: dict[str, bytes] = {}
    for current, dirs, names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        safe_dirs: list[str] = []
        for name in sorted(dirs):
            child = current_path / name
            if _is_linklike(child):
                raise RuntimeError(f"linked directory is not allowed in wiki output: {child}")
            safe_dirs.append(name)
        dirs[:] = safe_dirs
        for name in sorted(names):
            path = current_path / name
            if path.suffix.casefold() != ".md":
                continue
            rel = path.relative_to(root).as_posix()
            if _is_linklike(path) or not path.is_file():
                raise RuntimeError(f"linked or irregular Markdown file: {rel}")
            raw = path.read_bytes()
            try:
                raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise RuntimeError(f"OpenWiki Markdown is not UTF-8: {rel}") from exc
            result[rel] = raw
    return result


def _write_snapshot(root: Path, snapshot: Mapping[str, bytes]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for rel, raw in sorted(snapshot.items()):
        relative = PurePosixPath(rel)
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"unsafe snapshot path: {rel}")
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)


TOOLING_INDEX_SECTION = (
    "\n## Tooling context (user-scoped)\n\n"
    "- [Tooling context](tooling/index.md) — hand-authored local harness and "
    "provider observations; local pages are discovered by listing the "
    "directory, never enumerated here.\n"
)


def _ensure_index_routes_tooling(destination: Path) -> None:
    """Deterministically restore the root-index tooling entry after promotion.

    The producer never sees the user-scoped overlay, so a regenerated root
    index cannot reference it; the labeled entry is re-appended so every clone
    keeps the committed stub reachable (tooling link policy).
    """
    tooling = destination / "tooling"
    index = destination / "index.md"
    if not index.is_file() or not any(tooling.rglob("*.md")):
        return
    text = index.read_text(encoding="utf-8")
    if "tooling/index.md" in text or "](tooling/)" in text:
        return
    index.write_text(text.rstrip("\n") + "\n" + TOOLING_INDEX_SECTION, encoding="utf-8", newline="\n")


def wiki_snapshot_without_tooling(root: Path) -> dict[str, bytes]:
    """Accepted-wiki snapshot minus the user-scoped tooling overlay.

    Local tooling pages are runtime context, never producer input or
    promotion-comparison material; they stay in place on disk and survive
    promotion untouched.
    """
    return {
        rel: raw
        for rel, raw in markdown_snapshot(root).items()
        if not rel.startswith("tooling/")
    }


def protected_instructions(repo: Path) -> bytes:
    accepted = _inside(repo, repo / CANONICAL_WIKI / INSTRUCTIONS, "accepted OpenWiki instructions")
    source = accepted if accepted.is_file() else INSTRUCTIONS_TEMPLATE
    if _is_linklike(source) or not source.is_file():
        raise RuntimeError(f"missing or linked OpenWiki instructions: {source}")
    raw = source.read_bytes()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("OpenWiki instructions must be UTF-8 Markdown") from exc
    return raw


def materialize_corpus(repo: Path, stage: Path, corpus: Corpus) -> None:
    """Overlay selected worktree bytes without decoding or normalizing them."""
    for item in corpus.files:
        source = _inside(repo, repo / PurePosixPath(item.path), f"tracked path {item.path}")
        target = _inside(stage, stage / PurePosixPath(item.path), f"staged path {item.path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())


def prepare_stage(
    repo: Path,
    stage: Path,
    corpus: Corpus,
    baseline_state: bytes | None,
) -> tuple[set[str], bytes]:
    """Create a no-history repository and copy only the reviewed corpus into it."""
    if stage.exists():
        raise RuntimeError(f"stage already exists: {stage}")
    stage.parent.mkdir(parents=True, exist_ok=True)
    stage.mkdir()
    _git(stage, "init")
    materialize_corpus(repo, stage, corpus)

    accepted = wiki_snapshot_without_tooling(repo / CANONICAL_WIKI)
    instructions = protected_instructions(repo)
    accepted[INSTRUCTIONS] = instructions
    _write_snapshot(stage / STOCK_WIKI, accepted)
    if baseline_state is not None:
        state = stage / STOCK_STATE
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_bytes(baseline_state)

    # Indexing makes source-repository tracked files visible even when their
    # original .gitignore also appears in the staged corpus. It creates no
    # revision and never invokes signing.
    _git(stage, "add", "--force", "--all")
    if _git(stage, "remote").stdout.strip():
        raise RuntimeError("isolated OpenWiki repository unexpectedly has a remote")
    # The seeded contract is user-authored pre-run content and is citable;
    # previously generated wiki pages are memory, not evidence, and stay out.
    pre_run = {item.path for item in corpus.files}
    pre_run.add(f"{STOCK_WIKI}/{INSTRUCTIONS}")
    return pre_run, instructions


def child_environment(repo: Path, credential_home: str = "project") -> dict[str, str]:
    """Inherit provider configuration while leaving OpenWiki in charge of it."""
    env = os.environ.copy()
    # OpenWiki ships opt-out CLI telemetry (PostHog run events). Staged runs
    # stay silent by default; the user opts in by exporting
    # OPENWIKI_TELEMETRY_DISABLED=0 in their own environment.
    env.setdefault("OPENWIKI_TELEMETRY_DISABLED", "1")
    env.setdefault("DO_NOT_TRACK", "1")
    if credential_home == "user":
        # Classic behavior: the stock CLI resolves the user-global
        # ~/.openwiki/ home, shared across repositories, with the same
        # standing as the project home. Update state stays per-run in the
        # stage either way, so nothing else changes.
        return env
    home = _inside(repo, repo / "okf", "OpenWiki home")
    home.mkdir(parents=True, exist_ok=True)
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    return env


def _literal_openwiki_command(values: Sequence[str]) -> list[str]:
    command = list(values)
    if command and command[0] == "--":
        command.pop(0)
    if not command:
        raise ValueError("supply the stock OpenWiki argv after --")
    executable = command[0].replace("\\", "/").rsplit("/", 1)[-1].casefold()
    if executable.endswith((".cmd", ".exe")):
        executable = executable.rsplit(".", 1)[0]
    if executable != "openwiki":
        raise ValueError("the command after -- must invoke the stock openwiki executable")
    return command


def run_stock_openwiki(
    repo: Path,
    stage: Path,
    command: Sequence[str],
    timeout_seconds: int,
    credential_home: str = "project",
) -> None:
    argv = list(command)
    # Windows' CreateProcess does not do PATHEXT-style extension search the
    # way a shell does: shutil.which resolves a pnpm-installed CLI shim (for
    # example openwiki.CMD) correctly, but handing subprocess the bare name
    # fails with WinError 2 ("file not found") even though the shim exists
    # and is on PATH. Resolve the executable explicitly; POSIX is unaffected
    # (os.execvp there already searches PATH the same way either way).
    resolved = shutil.which(argv[0])
    if resolved is not None:
        argv[0] = resolved
    completed = subprocess.run(
        argv,
        cwd=stage,
        env=child_environment(repo, credential_home),
        timeout=timeout_seconds,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"OpenWiki exited {completed.returncode}; stage retained at {stage}")


def _validated_state(path: Path, label: str, *, required: bool) -> bytes | None:
    raw = _read_regular_optional(path, label)
    if raw is None:
        if required:
            raise RuntimeError(f"missing {label}: {path}")
        return None
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{label} must be a UTF-8 JSON object: {path}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a JSON object: {path}")
    return raw


def _normalize_stock_links(text: str, source_rel: str, known_markdown: set[str]) -> str:
    """Map stock bundle-root links to portable page-relative Markdown links."""

    def replace(match: re.Match[str]) -> str:
        target = match.group(2)
        split = urlsplit(target)
        if split.scheme or split.netloc or not split.path.startswith("/"):
            return match.group(0)
        rel = unquote(split.path).replace("\\", "/").lstrip("/")
        if rel.startswith("openwiki/"):
            rel = rel.removeprefix("openwiki/")
        candidates = [rel]
        if rel and not PurePosixPath(rel).suffix:
            candidates.extend([rel + ".md", rel.rstrip("/") + "/index.md"])
        destination = next((candidate for candidate in candidates if candidate in known_markdown), None)
        if destination is None:
            return match.group(0)
        parent = PurePosixPath(source_rel).parent.as_posix()
        relative = posixpath.relpath(destination, parent if parent != "." else ".")
        rewritten = urlunsplit(("", "", relative, split.query, split.fragment))
        return match.group(1) + rewritten + match.group(3)

    return LINK_RE.sub(replace, text)


def _citation_value(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("/") and not normalized.startswith("//"):
        normalized = normalized[1:]
    return PurePosixPath(normalized).as_posix()


def _drop_same_run_onboarding(text: str, pre_run_paths: set[str]) -> str:
    lines = text.splitlines(keepends=True)
    in_citations = False
    open_fence: str | None = None
    output: list[str] = []
    for line in lines:
        stripped = line.strip()
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if open_fence is None:
                open_fence = marker
            elif marker == open_fence:
                open_fence = None
            output.append(line)
            continue
        if open_fence is not None:
            output.append(line)
            continue
        if CITATION_HEADING_RE.fullmatch(stripped):
            in_citations = True
            output.append(line)
            continue
        if in_citations and re.match(r"^#{1,2}\s+", stripped):
            in_citations = False
        match = CITATION_BULLET_RE.fullmatch(stripped) if in_citations else None
        if match:
            value = _citation_value(match.group(1))
            if value in SAME_RUN_ONBOARDING and value not in pre_run_paths:
                continue
        output.append(line)
    return "".join(output)


def _frontmatter_sources(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return []
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return []
    try:
        metadata = yaml.safe_load(normalized[4:end])
    except yaml.YAMLError:
        return []  # The generic OKF validator reports the precise YAML error.
    if not isinstance(metadata, dict) or "sources" not in metadata:
        return []
    sources = metadata["sources"]
    if not isinstance(sources, list):
        raise RuntimeError("frontmatter sources must be a list of staged paths")
    if not all(isinstance(value, str) and value.strip() for value in sources):
        raise RuntimeError("frontmatter sources must contain non-empty staged paths")
    return list(sources)


def _body_citations(text: str, rel: str) -> list[str]:
    values: list[str] = []
    in_citations = False
    open_fence: str | None = None
    for line in text.replace("\r\n", "\n").splitlines():
        stripped = line.strip()
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if open_fence is None:
                open_fence = marker
            elif marker == open_fence:
                open_fence = None
            continue
        if open_fence is not None:
            continue
        if CITATION_HEADING_RE.fullmatch(stripped):
            in_citations = True
            continue
        if in_citations and re.match(r"^#{1,2}\s+", stripped):
            in_citations = False
        if not in_citations or not re.match(r"^[-*+]\s+", stripped):
            continue
        match = CITATION_BULLET_RE.fullmatch(stripped)
        if match is None:
            # External references, page cross-links, and prose bullets are not
            # staged citations and are ignored; the page still needs at least
            # one backticked staged citation overall, and every backticked
            # citation must resolve in the immutable pre-run stage.
            continue
        values.append(match.group(1))
    return values


NAV_LINE_RE = re.compile(r"^(#{1,6}\s.*|[-*+]\s.*\]\([^)]+\).*)$")


def _is_pure_navigation(text: str) -> bool:
    """True when every non-blank body line is a heading or a link bullet."""
    body = text.replace("\r\n", "\n")
    if body.startswith("---\n"):
        end = body.find("\n---\n", 4)
        if end != -1:
            body = body[end + 5 :]
    return all(
        NAV_LINE_RE.fullmatch(line.strip())
        for line in body.splitlines()
        if line.strip()
    )


def validate_citations(candidate: Path, pre_run_paths: set[str]) -> None:
    """Reject source references that were not in the immutable pre-run stage."""
    for rel, raw in sorted(markdown_snapshot(candidate).items()):
        # The bundle-root index.md (OKF navigation) and log.md history files
        # are citation-exempt. A subdirectory index.md is exempt only when it
        # is provably pure navigation; anything with prose is a knowledge
        # page, or knowledge could hide in uncited files.
        if rel == INSTRUCTIONS or rel == "index.md" or PurePosixPath(rel).name == "log.md":
            continue
        text = raw.decode("utf-8")
        if PurePosixPath(rel).name == "index.md" and _is_pure_navigation(text):
            continue
        sources = [*_frontmatter_sources(text), *_body_citations(text, rel)]
        if not sources:
            raise RuntimeError(f"{rel}: generated knowledge page has no source citations")
        for raw_source in sources:
            source = _citation_value(raw_source)
            path = PurePosixPath(source)
            if (
                not source
                or path.is_absolute()
                or ".." in path.parts
                or urlsplit(raw_source).scheme
                or source not in pre_run_paths
            ):
                raise RuntimeError(f"{rel}: source citation was absent before OpenWiki ran: {raw_source}")


def _normalize_generated_index(rel: str, text: str) -> str:
    """Deterministically own reserved-index frontmatter (OKF v0.1 reading).

    The stock producer may type its generated directory indexes; the spec
    reading enforced by the validator keeps non-root index.md frontmatter-free
    and limits the root index to the okf_version declaration.
    """
    if PurePosixPath(rel).name != "index.md":
        return text
    body = text.replace("\r\n", "\n")
    if body.startswith("---\n"):
        end = body.find("\n---\n", 4)
        if end != -1:
            body = body[end + 5 :].lstrip("\n")
    if rel == "index.md":
        return '---\nokf_version: "0.1"\n---\n\n' + body
    return body


def map_candidate(
    stage: Path,
    candidate: Path,
    candidate_state: Path,
    pre_run_paths: set[str],
    instructions: bytes,
) -> dict[str, bytes]:
    stock = stage / STOCK_WIKI
    generated = markdown_snapshot(stock)
    if not generated:
        raise RuntimeError("OpenWiki produced no Markdown under openwiki/")
    if candidate.exists():
        raise RuntimeError(f"candidate already exists: {candidate}")
    known = set(generated)
    mapped: dict[str, bytes] = {}
    for rel, raw in sorted(generated.items()):
        if rel == INSTRUCTIONS or rel in STOCK_SCRATCH:
            continue
        text = raw.decode("utf-8")
        text = _normalize_stock_links(text, rel, known)
        text = _drop_same_run_onboarding(text, pre_run_paths)
        text = _normalize_generated_index(rel, text)
        mapped[rel] = text.encode("utf-8")
    mapped[INSTRUCTIONS] = instructions
    _write_snapshot(candidate, mapped)
    validate_citations(candidate, pre_run_paths)
    state = _validated_state(stage / STOCK_STATE, "stock OpenWiki update state", required=True)
    assert state is not None
    candidate_state.parent.mkdir(parents=True, exist_ok=True)
    candidate_state.write_bytes(state)
    return mapped


def validate_candidate(candidate: Path) -> None:
    errors = validate_openwiki(candidate)
    if errors:
        raise RuntimeError("candidate failed OKF validation:\n" + "\n".join(errors))
    print("OpenWiki OKF validation passed")


def write_review_diff(before: Mapping[str, bytes], after: Mapping[str, bytes], destination: Path) -> None:
    lines: list[str] = []
    for rel in sorted(set(before) | set(after)):
        old = before.get(rel, b"").decode("utf-8").splitlines(keepends=True)
        new = after.get(rel, b"").decode("utf-8").splitlines(keepends=True)
        if old == new:
            continue
        lines.extend(
            difflib.unified_diff(
                old,
                new,
                fromfile=f"accepted/{rel}" if rel in before else "/dev/null",
                tofile=f"candidate/{rel}" if rel in after else "/dev/null",
            )
        )
    destination.write_text("".join(lines), encoding="utf-8", newline="\n")


def _assert_markdown_only(root: Path) -> None:
    if not root.is_dir():
        raise RuntimeError(f"missing candidate: {root}")
    markdown = set(markdown_snapshot(root))
    regular: set[str] = set()
    for current, dirs, names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in dirs:
            if _is_linklike(current_path / name):
                raise RuntimeError(f"linked directory is not allowed in wiki output: {current_path / name}")
        for name in names:
            path = current_path / name
            if _is_linklike(path) or not path.is_file():
                raise RuntimeError(f"linked or irregular wiki file: {path}")
            regular.add(path.relative_to(root).as_posix())
    unexpected = sorted(regular - markdown)
    if unexpected:
        raise RuntimeError("candidate contains non-Markdown files: " + ", ".join(unexpected))


def promote_candidate(repo: Path, run_root: Path) -> str:
    """Install reviewed Markdown and stock update state as one transaction."""
    run_root = _inside(repo, run_root, "run root")
    candidate = _inside(repo, run_root / "candidate" / "wiki", "candidate wiki")
    baseline = _inside(repo, run_root / "baseline" / "wiki", "baseline wiki")
    candidate_state_path = _inside(
        repo,
        run_root / "candidate" / "state" / ".last-update.json",
        "candidate OpenWiki state",
    )
    baseline_state_path = _inside(
        repo,
        run_root / "baseline" / "state" / ".last-update.json",
        "baseline OpenWiki state",
    )
    destination = _inside(repo, repo / CANONICAL_WIKI, "canonical wiki")
    local_state_path = _inside(repo, repo / LOCAL_STATE, "local OpenWiki state")
    _assert_markdown_only(candidate)
    _assert_markdown_only(baseline)
    if destination.exists():
        _assert_markdown_only(destination)
    baseline_snapshot = markdown_snapshot(baseline)
    candidate_snapshot = markdown_snapshot(candidate)
    baseline_state = _validated_state(baseline_state_path, "baseline OpenWiki state", required=False)
    candidate_state = _validated_state(candidate_state_path, "candidate OpenWiki state", required=True)
    current_state = _validated_state(local_state_path, "local OpenWiki state", required=False)
    assert candidate_state is not None
    expected_instructions = baseline_snapshot.get(INSTRUCTIONS, INSTRUCTIONS_TEMPLATE.read_bytes())
    if candidate_snapshot.get(INSTRUCTIONS) != expected_instructions:
        raise RuntimeError("candidate did not preserve INSTRUCTIONS.md byte-for-byte")
    validate_candidate(candidate)
    current_snapshot = wiki_snapshot_without_tooling(destination)
    if current_snapshot != baseline_snapshot:
        raise RuntimeError("accepted okf/wiki changed after candidate generation")
    if current_state != baseline_state:
        raise RuntimeError("okf/.openwiki/.last-update.json changed after candidate generation")
    wiki_changed = current_snapshot != candidate_snapshot
    state_changed = current_state != candidate_state
    if not wiki_changed and not state_changed:
        return "NO_CHANGE"

    transaction = _inside(repo, run_root / "transaction", "promotion transaction")
    if transaction.exists():
        raise RuntimeError(f"transaction path already exists: {transaction}")
    transaction.mkdir()
    next_tree = transaction / "next-wiki"
    previous = transaction / "previous-wiki"
    next_state = transaction / "next-state.json"
    previous_state = transaction / "previous-state.json"
    if wiki_changed:
        shutil.copytree(candidate, next_tree)
    if state_changed:
        next_state.write_bytes(candidate_state)
    destination.parent.mkdir(parents=True, exist_ok=True)
    local_state_path.parent.mkdir(parents=True, exist_ok=True)
    backed_up_wiki = False
    backed_up_state = False
    installed_wiki = False
    installed_state = False
    try:
        if wiki_changed and destination.exists():
            destination.replace(previous)
            backed_up_wiki = True
        if state_changed and local_state_path.exists():
            local_state_path.replace(previous_state)
            backed_up_state = True
        if wiki_changed:
            next_tree.replace(destination)
            installed_wiki = True
            # The user-scoped tooling overlay is runtime context outside the
            # producer/promotion contract: carry it over untouched.
            previous_tooling = previous / "tooling"
            if backed_up_wiki and previous_tooling.is_dir():
                previous_tooling.replace(destination / "tooling")
                _ensure_index_routes_tooling(destination)
        if state_changed:
            next_state.replace(local_state_path)
            installed_state = True
    except Exception:
        if installed_state and local_state_path.exists():
            local_state_path.unlink()
        if installed_wiki and destination.exists():
            shutil.rmtree(destination)
        if backed_up_wiki and previous.exists():
            previous.replace(destination)
        if backed_up_state and previous_state.exists():
            previous_state.replace(local_state_path)
        raise
    return "PROMOTED"


def _print_inventory(repo: Path, corpus: Corpus, run_id: str) -> None:
    bytes_total = sum((repo / PurePosixPath(item.path)).stat().st_size for item in corpus.files)
    print(
        f"DRY_RUN run_id={run_id} tracked_files={len(corpus.files)} bytes={bytes_total} "
        f"excluded={len(corpus.excluded)} unsupported={len(corpus.unsupported)} "
        f"missing={len(corpus.missing)}"
    )
    if corpus.unsupported:
        print("unsupported_tracked_paths=" + ",".join(corpus.unsupported))
    if corpus.missing:
        print("missing_tracked_paths=" + ",".join(corpus.missing))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run stock OpenWiki in an isolated no-remote repository")
    parser.add_argument("--repo", default=".", help="Git repository root")
    parser.add_argument("--run-id", help="Name under okf/.okf-build/")
    parser.add_argument("--exclude", action="append", default=[], help="Additional repository-relative prefix")
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument(
        "--credential-home",
        choices=("project", "user"),
        default="project",
        help="Which OpenWiki credential home the staged run resolves: the project's ignored okf/.openwiki/ (default) or the classic user-global ~/.openwiki/",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--execute", action="store_true", help="Call OpenWiki and prepare a review candidate")
    action.add_argument("--promote", action="store_true", help="Promote the reviewed candidate for --run-id")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="literal stock OpenWiki argv after --")
    args = parser.parse_args()

    try:
        repo = Path(args.repo).expanduser().resolve()
        if not (repo / ".git").exists():
            raise RuntimeError(f"not a Git repository: {repo}")
        if args.timeout_seconds < 1:
            raise ValueError("timeout must be positive")
        run_id = _clean_run_id(args.run_id)
        run_root = _inside(repo, repo / BUILD_ROOT / run_id, "run root")

        if args.promote:
            if args.run_id is None:
                raise ValueError("--promote requires the reviewed --run-id")
            if args.command:
                raise ValueError("--promote does not accept an OpenWiki command")
            outcome = promote_candidate(repo, run_root)
            print(outcome)
            return 0

        command = _literal_openwiki_command(args.command) if args.command else []
        corpus = collect_corpus(repo, args.exclude)
        _print_inventory(repo, corpus, run_id)
        if not args.execute:
            print("No stage was created, no provider was called, and okf/wiki was not changed.")
            return 0
        if not command:
            raise ValueError("--execute requires the stock OpenWiki argv after --")
        if corpus.unsupported or corpus.missing:
            details = [
                *(f"unsupported:{path}" for path in corpus.unsupported),
                *(f"missing:{path}" for path in corpus.missing),
            ]
            raise RuntimeError(
                "corpus is incomplete; explicitly exclude or resolve these tracked paths: "
                + ", ".join(details)
            )
        if run_root.exists():
            raise RuntimeError(f"run already exists: {run_root}")

        canonical_wiki = _inside(repo, repo / CANONICAL_WIKI, "canonical wiki")
        if canonical_wiki.exists():
            _assert_markdown_only(canonical_wiki)
        baseline = wiki_snapshot_without_tooling(canonical_wiki)
        _write_snapshot(run_root / "baseline" / "wiki", baseline)
        local_state = _validated_state(
            _inside(repo, repo / LOCAL_STATE, "local OpenWiki state"),
            "local OpenWiki state",
            required=False,
        )
        if local_state is not None:
            baseline_state = run_root / "baseline" / "state" / ".last-update.json"
            baseline_state.parent.mkdir(parents=True, exist_ok=True)
            baseline_state.write_bytes(local_state)
        stage = run_root / "worktree"
        pre_run_paths, instructions = prepare_stage(repo, stage, corpus, local_state)
        print(
            f"DISCLOSURE: stock OpenWiki will receive {len(corpus.files)} Git-tracked file(s) "
            f"plus {len(baseline)} accepted wiki page(s) in a no-history, no-remote stage. "
            "Provider configuration is inherited; the adapter does not read "
            "okf/.openwiki/.env. Stock code mode can use shell tools and is not an OS sandbox."
        )
        run_stock_openwiki(repo, stage, command, args.timeout_seconds, args.credential_home)
        candidate = run_root / "candidate" / "wiki"
        candidate_state = run_root / "candidate" / "state" / ".last-update.json"
        mapped = map_candidate(stage, candidate, candidate_state, pre_run_paths, instructions)
        validate_candidate(candidate)
        review_diff = run_root / "review.diff"
        write_review_diff(baseline, mapped, review_diff)
        print(f"CANDIDATE_READY {candidate.relative_to(repo).as_posix()}")
        print(f"STATE_READY {candidate_state.relative_to(repo).as_posix()}")
        print(f"REVIEW_DIFF {review_diff.relative_to(repo).as_posix()}")
        print(f"Review it, then promote with --run-id {run_id} --promote.")
        return 0
    except subprocess.TimeoutExpired:
        print("error: OpenWiki timed out; the isolated stage was retained", file=sys.stderr)
        return 1
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
