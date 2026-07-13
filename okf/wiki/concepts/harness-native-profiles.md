---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
description: "Harness-specific subagent profiles generated from local repo context"
---

# Harness-Native Profiles

Harness-native profiles are runtime-specific subagent or persona definitions that are generated for the active harness instead of being treated as portable project knowledge. They translate existing repo context into the file format and conventions expected by the current execution environment.

This concept is central to [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]], which defines the workflow for detecting a harness, checking whether it supports local profiles, and writing minimal adapter files for it.

## Core idea

A harness-native profile is not a source of truth. It is a projection of durable project context into a harness's local runtime model. The source document draws a strong boundary between:

- [[concepts/compiled-knowledge-bases]] and other durable wiki context as the truth layer
- `AGENTS.md` as the repository orientation layer
- Agent Skills as action layers
- harness-native profiles as temporary runtime adapters

## Why it exists

The profile layer is useful when a harness supports local subagents, personas, or task-scoped execution contexts. Instead of hardcoding a portable standard, the adapter skill reads the current harness documentation and writes the native format directly.

That makes profile generation part of [[concepts/runtime-adapter-management]] and [[concepts/adaptive-harness-detection]], not a universal schema design exercise.

## Key rules

- Detect the active runtime using environment and harness clues, not installed binaries alone.
- Ask the user if the harness is still ambiguous.
- Keep profiles short and focused on purpose, activation, and permissions.
- Avoid embedding long project context inside the profile file.
- Point profiles back to `AGENTS.md`, wiki context, and reusable skills.
- Do not create extra `.agents/` directories beyond `.agents/skills/`.

## Relationship to the wiki

The source document treats the wiki as the durable knowledge layer and the profile as a disposable runtime artifact. That separation reinforces [[concepts/documentation-layer-separation]], [[concepts/knowledge-layer-separation]], and [[concepts/context-action-separation]].

It also emphasizes link direction: tooling context may inform project work, but project concept pages should not depend on tooling pages. That keeps harness details inside [[concepts/tooling-context-governance]] and [[concepts/tooling-context-isolation]].

## Validation and governance

Profile generation is not considered complete until the resulting files are validated for placement, size, and link-policy compliance. The source document specifically requires checks that:

- the generated files land in the correct harness location
- the profile does not inline large wiki content
- project concept pages do not link back to tooling context
- the root wiki index includes tooling context when needed

This aligns the concept with [[concepts/generated-artifact-validation]], [[concepts/tooling-link-policy]], [[concepts/wikilink-integrity]], and [[concepts/okf-validation]].

## Practical impact

In practice, harness-native profiles let a repository support multiple agent runtimes without turning any one runtime into the canonical model. They help teams preserve [[concepts/single-source-of-truth]] while still supporting local execution features, adapter files, and harness-specific permissions.

## Related ideas

- [[concepts/agent-ready-context]] provides the upstream repository context that profiles should project.
- [[concepts/agent-tooling-ecosystem]] frames the broader set of tools and runtime surfaces an agent may need to adapt to.
- [[concepts/permission-scoped-agents]] captures the idea that generated agents should stay bounded to the task and available permissions.
- [[concepts/portable-skill-contract]] contrasts with the non-portable nature of runtime profiles.
- [[concepts/local-by-default-tooling]] and [[concepts/local-only-repo-artifacts]] explain the preference for local adapter tracking unless the user chooses otherwise.