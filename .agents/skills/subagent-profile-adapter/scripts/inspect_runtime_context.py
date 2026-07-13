#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Collect runtime-harness hints without invoking vendor CLIs.

This script intentionally does not run commands such as `<tool> --version` because
installed binaries are not proof of the active harness.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path
from typing import Any

HARNESS_KEYWORDS = {
    "opencode": ["opencode"],
    "claude-code": ["claude", "claude-code", "anthropic"],
    "codex": ["codex"],
    "cursor": ["cursor"],
    "aider": ["aider"],
    "gemini-cli": ["gemini"],
}

EXPLICIT_ENV_KEYS = [
    "AGENT_HARNESS",
    "AI_AGENT_HARNESS",
    "HARNESS",
    "CURRENT_AGENT_HARNESS",
    "AGENT_RUNTIME",
    "AI_AGENT_RUNTIME",
]

ENV_HINT_KEYS = [
    "CLAUDE_CONFIG_DIR",
    "OPENCODE_CONFIG",
    "CODEX_HOME",
    "CURSOR_AGENT",
    "AIDER_MODEL",
    "TERM_PROGRAM",
    "VSCODE_PID",
]

MARKERS = {
    "opencode": [".opencode", ".opencode/agents"],
    "claude-code": [".claude", ".claude/agents", "CLAUDE.md"],
    "agent-skills-compatible": [".agents/skills"],
    "agents-md-compatible": ["AGENTS.md"],
}


def read_proc(pid: int) -> dict[str, str] | None:
    base = Path("/proc") / str(pid)
    if not base.exists():
        return None
    try:
        comm = (base / "comm").read_text(encoding="utf-8", errors="replace").strip()
    except Exception:
        comm = ""
    try:
        raw = (base / "cmdline").read_bytes().replace(b"\x00", b" ").decode("utf-8", errors="replace").strip()
    except Exception:
        raw = ""
    try:
        stat = (base / "stat").read_text(encoding="utf-8", errors="replace")
        # /proc/<pid>/stat has comm in parentheses. ppid is first field after it.
        after = stat.rsplit(")", 1)[1].strip().split()
        ppid = after[1] if len(after) > 1 else ""
    except Exception:
        ppid = ""
    return {"pid": str(pid), "ppid": ppid, "comm": comm, "cmdline": raw}


def parent_chain(limit: int = 8) -> list[dict[str, str]]:
    chain: list[dict[str, str]] = []
    pid = os.getpid()
    for _ in range(limit):
        info = read_proc(pid)
        if not info:
            break
        chain.append(info)
        try:
            next_pid = int(info.get("ppid") or "0")
        except ValueError:
            break
        if next_pid <= 1 or next_pid == pid:
            break
        pid = next_pid
    return chain


def score_candidates(texts: list[str]) -> dict[str, int]:
    joined = "\n".join(texts).lower()
    scores: dict[str, int] = {}
    for harness, words in HARNESS_KEYWORDS.items():
        score = 0
        for word in words:
            if word in joined:
                score += 1
        if score:
            scores[harness] = score
    return scores


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    env_explicit = {k: os.environ.get(k) for k in EXPLICIT_ENV_KEYS if os.environ.get(k)}
    env_hints = {k: os.environ.get(k) for k in ENV_HINT_KEYS if os.environ.get(k)}
    proc_chain = parent_chain()

    marker_hits: dict[str, list[str]] = {}
    for harness, paths in MARKERS.items():
        hits = [p for p in paths if (repo / p).exists()]
        if hits:
            marker_hits[harness] = hits

    proc_texts = [p.get("comm", "") + " " + p.get("cmdline", "") for p in proc_chain]
    proc_scores = score_candidates(proc_texts)
    env_scores = score_candidates(list(env_explicit.values()) + list(env_hints.values()))

    candidates: dict[str, dict[str, Any]] = {}
    for harness, score in proc_scores.items():
        candidates.setdefault(harness, {"confidence": "medium", "signals": []})
        candidates[harness]["signals"].append(f"parent-process-match:{score}")
    for harness, score in env_scores.items():
        candidates.setdefault(harness, {"confidence": "medium", "signals": []})
        candidates[harness]["signals"].append(f"environment-match:{score}")
    for harness, hits in marker_hits.items():
        candidates.setdefault(harness, {"confidence": "low", "signals": []})
        candidates[harness]["signals"].append("repo-markers:" + ",".join(hits))

    explicit_values = " ".join(env_explicit.values()).lower()
    for harness, words in HARNESS_KEYWORDS.items():
        if any(word in explicit_values for word in words):
            candidates.setdefault(harness, {"confidence": "high", "signals": []})
            candidates[harness]["confidence"] = "high"
            candidates[harness]["signals"].append("explicit-environment")

    result = {
        "repo": str(repo),
        "platform": platform.platform(),
        "explicit_environment": env_explicit,
        "environment_hints": env_hints,
        "parent_process_chain": proc_chain,
        "repo_marker_hints": marker_hits,
        "candidate_harnesses": candidates,
        "decision_guidance": "Use high-confidence explicit runtime signals or ask the user. Do not treat installed binaries or repo markers as active runtime proof.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
