---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
description: "Managing harness-specific subagent and profile adapter files safely."
---

# Runtime Adapter Management

Runtime adapter management is the practice of creating, maintaining, and validating harness-specific subagent or profile adapters from repository knowledge without turning those adapters into a source of truth. It treats adapter files as runtime projections: useful for the current execution environment, but secondary to durable project context.

## What It Covers

This concept applies when a repository needs local subagents, personas, or task-scoped execution contexts that vary by harness. The adapter layer translates existing guidance into the native file format expected by the active runtime, rather than inventing a portable standard.

## Core Principles

- Keep adapter files narrowly scoped and harness-specific.
- Treat [[concepts/agent-ready-context]] and `AGENTS.md` as the main orientation inputs.
- Keep durable knowledge in [[concepts/compiled-knowledge-bases]] and wiki pages, not in runtime adapter files.
- Use generated adapters as projections of repo state, not as authoritative documentation.
- Prefer runtime detection based on explicit environment or harness documentation, not installed binaries alone.

## Workflow Pattern

The source skill behind this concept describes a staged process:

1. Confirm the repository has refreshed orientation material and compiled wiki context.
2. Detect the active runtime from explicit signals and harness documentation.
3. Verify whether the runtime supports local subagents or profiles.
4. Decide how generated files should be tracked: local-only, ignored, or committed.
5. Write short native adapter files that point back to `AGENTS.md`, the wiki, and relevant skills.
6. Validate that the files follow the repo's link and tooling policies.

## Boundary Rules

Runtime adapter management depends on clear separation between layers:

- Project knowledge belongs in the wiki and source-backed summaries.
- Agent orientation belongs in `AGENTS.md`.
- Reusable procedures belong in Agent Skills.
- Runtime adapters belong only to the active harness.

That separation supports [[concepts/documentation-layer-separation]], [[concepts/tooling-context-isolation]], and [[concepts/context-action-separation]].

## Tooling and Link Policy

A key part of this concept is making sure tooling context does not leak back into project concept pages. The source document requires strict link directionality: tooling context may reference project context, but project pages must not depend on tooling pages. This aligns with [[concepts/link-directionality]] and [[concepts/tooling-link-policy]].

It also emphasizes that the wiki index may enumerate tooling pages for navigation, while concept pages should stay free of deep tooling dependencies. That supports [[concepts/tooling-navigation-exception]] and [[concepts/tooling-context-governance]].

## Important Risks

- Ambiguous runtime detection can produce the wrong adapter format.
- Overstuffed profiles can become a duplicate source of truth.
- Weak validation can let harness-specific files drift from repository policy.
- Unclear file-tracking policy can create noisy or accidental commits.

These risks make [[concepts/generated-artifact-validation]], [[concepts/runtime-ambiguity-resolution]], and [[concepts/local-only-repo-artifacts]] especially relevant.

## Related Ideas

Runtime adapter management overlaps with [[concepts/harness-native-profiles]], [[concepts/subagent-role-design]], [[concepts/permission-scoped-agents]], and [[concepts/portable-skill-contract]] because all of them concern how agent capabilities are shaped by environment-specific rules.

It also depends on [[concepts/adaptive-harness-detection]] and [[concepts/runtime-signal-prioritization]] when determining which harness is actually active.

## Source Connection

This concept is grounded in [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]], which defines the workflow for detecting the runtime, generating native adapter files, and validating their placement and policy compliance.
