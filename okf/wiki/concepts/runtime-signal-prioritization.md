---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md"]
description: "Ranks runtime evidence by reliability to infer the active harness safely."
---

# Runtime Signal Prioritization

Runtime signal prioritization is the practice of ranking evidence for an active agent harness by reliability, not by convenience. The goal is to infer the current runtime from the strongest available signals first, while treating weaker clues as advisory rather than authoritative.

This concept appears in `summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py`, where the inspection script gathers multiple categories of evidence and assigns them different confidence levels before producing candidate harness matches. It also underpins the broader subagent/profile adapter workflow, where the active harness must be detected before writing native runtime-specific adapters.

## Core idea

Not all runtime signals mean the same thing.

- Explicit environment variables are the strongest evidence when they directly name a harness.
- Parent process names and command lines are useful but indirect.
- Repository markers indicate compatibility or likely intent, but not the active runtime.
- Installed binaries are intentionally ignored as proof of the current harness.

This ordering reduces false positives and supports [[concepts/confidence-calibration]] by making the inference process transparent. It also fits the boundary between durable project knowledge and runtime-specific projections: the agent should inspect context first, then decide whether a harness-specific adapter is appropriate.

## Signal tiers

The source script effectively separates runtime evidence into layers:

- **Explicit environment**: Variables such as `AGENT_HARNESS`, `HARNESS`, and `AGENT_RUNTIME` can directly identify the active runtime.
- **Environment hints**: Variables like `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, and `TERM_PROGRAM` provide softer clues.
- **Parent process chain**: Process names and command lines from `/proc` may reveal the surrounding harness.
- **Repository markers**: Paths such as `.claude`, `.opencode`, `.agents/skills`, and `AGENTS.md` show local compatibility or repo structure.

The script promotes explicit matches to high confidence, process and environment matches to medium confidence, and repo markers to low confidence unless reinforced by stronger evidence. That tiering is important when deciding whether to persist harness-specific files locally, ignore them, or commit them as shared adapters.

## Why prioritization matters

Runtime detection is easy to get wrong when a tool over-trusts local artifacts. A repository may contain markers for several systems, and a machine may have many CLIs installed that are not relevant to the current session. Prioritization helps avoid conflating presence with activation.

This aligns with [[concepts/non-invasive-detection]] and [[concepts/harness-vs-local-tools]], because the inspection process avoids executing vendor binaries and instead relies on contextual evidence. It also supports [[concepts/runtime-adapter-management]] by keeping generated adapter files tied to the actual runtime rather than to whatever tooling happens to be installed.

## Decision guidance

The source document encodes a clear rule:

- Use high-confidence explicit runtime signals when available.
- Otherwise consult weaker signals cautiously.
- Do not treat installed binaries or repository markers as proof of the active runtime.
- Ask the user if the evidence remains ambiguous.

That guidance supports [[concepts/runtime-ambiguity-resolution]] and [[concepts/adaptive-harness-detection]] by keeping the system conservative when signals disagree. It also reinforces the idea that harness selection is a detection problem before it is an adapter-writing problem.

## Related practices

Runtime signal prioritization often works together with:

- [[concepts/context-action-separation]]: infer context before taking harness-specific actions.
- [[concepts/progressive-disclosure]]: expose stronger evidence first, then supporting hints.
- [[concepts/heuristic-classification]]: combine several weak indicators into a ranked guess.
- [[concepts/tool-boundaries]]: keep detection separate from execution.
- [[concepts/privacy-preserving-tooling]]: collect only the minimum needed information.
- [[concepts/permission-scoped-agents]]: choose adapter behavior based on the confirmed runtime and its allowed scope.

## Practical result

In this script, the prioritized signal model produces a structured JSON report with candidate harnesses, confidence labels, and supporting signals. That makes the runtime inference auditable and safer for downstream subagent setup.

In the broader skill workflow, this evidence-first approach helps decide whether to generate a harness-native profile adapter, whether to keep it local-only, and whether the runtime is still too ambiguous to proceed.

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
