---
type: "Summary"
description: "Inspects runtime hints to infer the active agent harness safely."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md"
---

# .agents/skills/subagent-profile-adapter/scripts/inspect_runtime_context.py

This script gathers non-invasive signals about the current agent runtime and emits a JSON report of likely harness candidates. Its main purpose is to help subagent profile adaptation without falsely treating installed binaries as proof of the active environment.

## What it does

- Checks explicit environment variables such as `AGENT_HARNESS`, `HARNESS`, and `AGENT_RUNTIME`.
- Collects softer environment hints like `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, `TERM_PROGRAM`, and `VSCODE_PID`.
- Walks the parent process chain from `/proc` to look for process-name and command-line matches.
- Scans the repository for marker files and directories such as `.opencode`, `.claude`, `.agents/skills`, and `AGENTS.md`.
- Scores these signals to produce candidate harnesses with confidence levels and supporting signals.

## Key ideas

- [[concepts/runtime-signal-prioritization]]: The script infers execution context from multiple weak and strong signals.
- [[concepts/adaptive-harness-detection]]: It combines independent hints into a candidate ranking rather than relying on a single source.
- [[concepts/harness-native-profiles]]: The code is built to identify which agent harness is active.
- [[concepts/non-invasive-detection]]: It explicitly avoids invoking vendor CLIs like `<tool> --version`.
- [[concepts/agent-ready-context]]: Repository files and directories are treated as hints, not proof.

## Findings

- Explicit environment values can raise a candidate to high confidence when they directly name a known harness.
- Parent process names and command lines provide medium-confidence evidence when they contain harness keywords.
- Repository markers are only low-confidence hints because they may exist even when the harness is not active.
- The final guidance warns against assuming installed binaries represent the current runtime.

## Output shape

The script prints a JSON object containing:

- the resolved repository path
- platform details
- explicit environment variables
- softer environment hints
- the parent process chain
- repository marker hits
- scored candidate harnesses
- a decision guidance message

## Why it matters

This is a practical utility for adapting subagent behavior to the surrounding runtime without making unsafe assumptions. It supports more reliable [[concepts/context-action-separation]] by separating strong evidence from weak signals and by keeping detection passive.

## Related Concepts
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-adapter-management]]
- [[concepts/subagent-role-design]]
- [[concepts/tool-boundaries]]
- [[concepts/harness-vs-local-tools]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/agent-context-layering]]
- [[concepts/agent-orientation-index]]
- [[concepts/agent-ready-repositories]]
- [[concepts/agent-tooling-ecosystem]]
- [[concepts/agent-trigger-design]]
- [[concepts/consent-first-tooling]]
- [[concepts/cross-platform-tooling]]
- [[concepts/filesystem-validation]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/knowledge-boundaries]]
- [[concepts/knowledge-layer-separation]]
- [[concepts/local-by-default-tooling]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/non-interactive-agent-design]]
- [[concepts/offline-first-workflows]]
- [[concepts/preflight-checks]]
- [[concepts/progressive-disclosure]]
- [[concepts/prompt-injection-defense]]
- [[concepts/repository-orientation-indexing]]
- [[concepts/tooling-boundaries]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-pages]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-navigation-exceptions]]
- [[concepts/tooling-vendoring]]
- [[concepts/wiki-context-routing]]

## Entities
- [[entities/proc]]
- [[entities/scripts-inspect_runtime_context-py]]
- [[entities/subagent-profile-adapter]]
- [[entities/python]]
- [[entities/uv]]
- [[entities/romain-monier]]
- [[entities/agent-skills]]
- [[entities/agents-md]]
- [[entities/anthropic]]
- [[entities/claude-desktop]]
- [[entities/gemini]]
