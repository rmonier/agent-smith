---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md"]
description: "Detect runtime context without executing vendor CLIs or invasive checks."
---

# Non-Invasive Detection

Non-invasive detection is the practice of inferring runtime or environment context from passive signals instead of actively probing tools or services. It favors reading already-available metadata, filesystem markers, and process information, while avoiding commands that could be misleading, side-effectful, or privileged.

This approach is central to [[concepts/adaptive-harness-detection]] and [[concepts/runtime-signal-prioritization]], where the goal is to identify the active agent harness from evidence that is informative but not authoritative on its own.

## Core idea

A non-invasive detector asks: what can be learned without changing state or assuming that an installed binary reflects the current runtime? In the referenced script, the answer comes from:

- explicit environment variables such as `AGENT_HARNESS` and `AGENT_RUNTIME`
- softer environment hints such as `TERM_PROGRAM` and `VSCODE_PID`
- parent-process inspection via `/proc`
- repository markers like `.claude`, `.opencode`, `.agents/skills`, and `AGENTS.md`

The script intentionally does not run commands like `<tool> --version`, because the presence of a binary does not prove the active harness. That distinction is the key boundary between passive inference and active validation.

## Why it matters

Non-invasive detection supports safer and more reliable runtime adaptation:

- It avoids false confidence from installed tooling that is not actually in use.
- It preserves user intent by not probing external tools unnecessarily.
- It works well in constrained, offline, or permission-limited environments.
- It reduces the risk of side effects during context discovery.

These properties align with [[concepts/consent-first-workflows]], [[concepts/privacy-preserving-tooling]], and [[concepts/safe-automation]].

## How the source implements it

The source document `[[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]` demonstrates a layered detection strategy:

1. Collect explicit environment values first.
2. Collect less direct environment hints.
3. Inspect the parent process chain for process-name and command-line matches.
4. Scan the repository for known marker paths.
5. Score the signals into candidate harnesses with confidence levels.
6. Emit guidance that prefers high-confidence runtime signals over weak indicators.

This is a practical example of [[concepts/agent-context-layering]] and [[concepts/confidence-calibration]]: the script separates strong evidence from weak evidence instead of collapsing them into a single brittle answer.

## Important constraints

Non-invasive detection should be treated as inference, not proof. The source script makes that explicit by warning that:

- repo markers are only hints
- parent-process names are suggestive, not authoritative
- environment values may be stale or inherited
- installed binaries are not evidence of active use

That caution supports [[concepts/runtime-ambiguity-resolution]] and [[concepts/source-trust-levels]] by keeping the interpretation of signals conservative.

## Related patterns

- [[concepts/harness-native-profiles]]: using runtime-specific profiles once the harness is identified
- [[concepts/harness-vs-local-tools]]: distinguishing active harness context from local machine tooling
- [[concepts/heuristic-classification]]: classifying context from partial evidence
- [[concepts/non-interactive-agent-design]]: operating without asking the user for every detail
- [[concepts/progressive-disclosure]]: revealing confidence and evidence instead of overclaiming

## Summary

Non-invasive detection is a conservative context-discovery pattern: infer from available signals, avoid active probing, and keep confidence calibrated. In the referenced script, this makes runtime identification safer, more portable, and less likely to misrepresent the active agent environment.