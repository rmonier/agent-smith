---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Separates skills, wiki context, and AGENTS.md responsibilities."
---

# Wiki and Skill Boundaries

This concept describes the separation of responsibilities between repository skills, the compiled wiki, and `AGENTS.md` in the agent-ready context workflow.

## Core boundary

The source document frames three distinct layers:

- **Skills** are for repeatable actions: scripts, checks, transformations, validations, and workflow orchestration.
- **The wiki** is for durable context: architecture notes, provenance, external evidence, decisions, and cross-document memory.
- **`AGENTS.md`** is for orientation: setup, test commands, routing guidance, and concise best practices.

This separation is central to [[concepts/context-action-separation]] and [[concepts/durable-context]]: actions belong in skills, while stable knowledge belongs in the wiki.

## What belongs where

The document strongly discourages mixing these layers:

- Do not turn durable repository knowledge into a skill unless it describes a repeatable action.
- Do not put long-form repository knowledge into `AGENTS.md`.
- Do not create a parallel wiki outside `okf/wiki/`.
- Do not patch compiled wiki pages directly when source documents can be improved and re-ingested.

This creates a clear division between [[concepts/skill-governance]], [[concepts/compiled-knowledge-bases]], and [[concepts/generated-content-governance]].

## Why the boundary matters

The boundary is designed to keep the system maintainable and trustworthy:

- [[concepts/single-source-of-truth]]: `okf/wiki/` is the durable context source of truth.
- [[concepts/provenance-tracking]]: wiki content should be grounded in source documents and staged evidence.
- [[concepts/source-driven-regeneration]]: fixes should flow through the source pack and re-ingestion cycle, not manual edits to compiled output.
- [[concepts/knowledge-boundaries]]: each layer has a narrow purpose, which reduces drift and duplication.

## Operational implications

The skill translates the boundary into repository operations:

- repository evidence is staged deterministically before ingestion
- generated files are kept out of `okf/raw/` and `okf/wiki/`
- findings discovered during work are captured in the wiki’s findings namespace rather than copied into project docs
- `AGENTS.md` remains a compact navigation and orientation file, not a substitute for the wiki

These rules support [[concepts/consent-first-workflows]], [[concepts/deterministic-builds]], and [[concepts/okf-workflow-governance]].

## Related ideas

The boundary depends on several nearby concepts:

- [[concepts/agent-context-layering]] for the overall stack of action, context, and orientation
- [[concepts/agent-ready-repositories]] for the broader repository preparation goal
- [[concepts/documentation-architecture]] for how documentation roles are distributed
- [[concepts/documentation-cohesion]] for keeping the layers aligned without duplication
- [[concepts/documentation-source-priority]] for favoring source material over compiled output when resolving truth

## Source connection

The source skill that defines this boundary is [[summaries/agents__skills__agent-ready-context__SKILL-md]]. It is the operational policy document that explains how the repository should be made agent-ready while preserving the separation between actions, durable context, and orientation.

See also: [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]