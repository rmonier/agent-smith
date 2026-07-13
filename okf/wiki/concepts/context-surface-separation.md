---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Separates agent instructions, durable wiki context, and repo orientation."
---

# Context Surface Separation

Context surface separation is the practice of splitting repository knowledge into three distinct layers: executable skills, durable compiled wiki context, and concise `AGENTS.md` orientation.

This concept is central to [[concepts/agent-ready-context]] and is presented as the main organizational rule for making a repository agent-ready.

## Core Separation

The source document defines three different surfaces with different jobs:

- **Skills**: repeatable actions, scripts, checks, transformations, and workflows that the agent can execute
- **OKF wiki**: durable repository knowledge, external evidence, provenance, architecture notes, and cross-agent memory
- **`AGENTS.md`**: short orientation, setup/test commands, routing guidance, and basic best practices

The model is deliberately layered so that procedural instructions do not grow into long-form knowledge, and compiled knowledge does not get mixed into action definitions.

## Why It Matters

The separation reduces confusion about where information belongs:

- actions stay in skills instead of being duplicated as passive documentation
- long-lived repository knowledge stays in the wiki instead of being flattened into `AGENTS.md`
- `AGENTS.md` stays concise and operational instead of becoming a second wiki

This supports [[concepts/documentation-layer-separation]], [[concepts/knowledge-layer-separation]], and [[concepts/context-surface-management]].

## Repository Workflow Implications

The document ties this separation to a specific maintenance flow:

- stage deterministic input under `okf/.okf-build/input/`
- ingest staged content into the OpenKB KB root `okf/`
- let OpenKB compile durable pages under `okf/wiki/`
- keep generated content out of direct hand edits except for narrowly defined exceptions
- use `AGENTS.md` as a front door, not as the primary knowledge store

That workflow reinforces [[concepts/deterministic-okf-staging]], [[concepts/source-driven-regeneration]], and [[concepts/compiled-knowledge-bases]].

## Related Boundaries

The document also distinguishes several nearby boundaries:

- [[concepts/context-action-separation]] for separating knowledge from repeatable action
- [[concepts/skill-action-boundary]] for keeping skills executable and scoped
- [[concepts/tooling-boundaries]] for keeping harness-specific context separate from project truth
- [[concepts/knowledge-capture-boundaries]] for deciding what belongs in findings, wiki pages, or source documents

## Practical Outcome

In practice, context surface separation means a repository remains easier to navigate, safer to update, and less likely to accumulate duplicated or contradictory guidance. It is a structural rule for [[concepts/agent-orientation-index]] and a foundation for [[concepts/knowledge-lifecycle-governance]].

## Source Link

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]