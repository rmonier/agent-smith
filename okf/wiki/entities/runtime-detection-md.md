---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
type: "Work"
description: "Runtime detection guidance for selecting the active harness"
---

# Runtime Detection

`runtime-detection.md` is a reference document used by the [[entities/subagent-profile-adapter]] skill to decide which harness is actually active before generating any runtime-specific adapter files.

## What it covers

- It guides agents to detect the active runtime from explicit environment, process, and harness metadata.
- It warns against treating an installed binary or available tool as proof of the current harness.
- It says repo files can be used as low-confidence hints, but not as sole evidence.
- It recommends asking the user when runtime signals remain ambiguous.

## Role in the skill

The document supports the workflow in [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]] by making runtime identification a prerequisite for adapter generation. That aligns it with [[concepts/adaptive-harness-detection]] and [[concepts/runtime-ambiguity-resolution]].

## Key ideas

- Active runtime matters more than installed tooling.
- Environment and parent-process hints are preferred evidence.
- Local or official harness documentation is the next step after detection.
- Validation should be based on the confirmed runtime, not assumptions.

## Why it matters

This document helps prevent the wrong adapter from being generated for the wrong environment. That reduces harness mismatch, keeps adapter files narrow, and supports [[concepts/runtime-signal-prioritization]] and [[concepts/permission-scoped-agents]].

## Related pages

- [[entities/subagent-profile-adapter]]
- [[concepts/harness-native-profiles]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-link-policy]]
- [[concepts/adaptive-harness-detection]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]