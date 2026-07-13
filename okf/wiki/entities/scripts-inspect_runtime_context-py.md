---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
type: "Work"
description: "Helper script for inspecting runtime context during harness detection"
---

# Inspect Runtime Context Script

`inspect_runtime_context.py` is a repository-local helper script used by the [[summaries/agents__skills__subagent-profile-adapter__SKILL-md|Subagent Profile Adapter]] skill to gather hints about the active runtime environment.

## Purpose

The script supports the skill's [[concepts/adaptive-harness-detection|adaptive harness detection]] workflow by collecting environment and process signals that may help identify the current harness.

In the [[summaries/agents__skills__agent-ready-context__SKILL-md|Agent-Ready Context]] workflow, it is part of the optional harness-specific tooling used only after the repository context and action skills are in place. The broader pipeline treats harness detection as best-effort and explicitly says that if the active harness cannot be determined reliably, the record should be skipped and the run should continue.

## Key Facts

- It is invoked as a repository-local validation and inspection helper.
- It is used for runtime hint collection, not as proof of the active harness by itself.
- The skill treats it as a low-confidence source that must be combined with explicit context and documentation.
- The skill recommends it only as an aid for [[concepts/runtime-ambiguity-resolution|runtime ambiguity resolution]].
- In the agent-ready workflow, runtime inspection is a supporting step, not a prerequisite for core KB compilation.

## Role In The Skill

Within the subagent-profile-adapter workflow, the script helps determine whether the active environment supports local subagents or profiles and whether harness-specific adapters should be generated.

Its output can inform decisions about [[concepts/runtime-signal-prioritization|runtime signal prioritization]], but the skill explicitly warns against relying on installed binaries or version checks as the primary evidence.

Within the agent-ready-context workflow, similar inspection is used to identify the active harness only when the identity is reliable enough to write a minimal harness build record under `okf/wiki/tooling/harnesses/`.

## Related Concepts

- [[concepts/non-invasive-detection]]
- [[concepts/explicit-provider-routing]]
- [[concepts/harness-native-profiles]]
- [[concepts/harness-vs-local-tools]]
- [[concepts/runtime-adapter-management]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/agent-tooling-ecosystem]]
- [[concepts/local-by-default-tooling]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]