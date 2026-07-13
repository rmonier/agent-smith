---
type: "Summary"
description: "Example intent specs for curator, skill, and repo-mapping subagent profiles."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md"
---

# Summary

This document provides example "profile intents": short, harness-agnostic role descriptions that an agent can translate into native harness configuration after consulting current harness documentation. It frames profiles as compact operational contracts covering purpose, usage triggers, required context, and permission boundaries.

## Key Points

- The file is explicitly not vendor-specific; it presents portable intent descriptions rather than concrete harness config formats.
- Each profile intent follows a consistent schema:
  - Purpose
  - Use when
  - Context
  - Permissions
- The examples focus on three subagent roles:
  - `okf-curator`
  - `skill-architect`
  - `repo-cartographer`

## Example Profiles

### `okf-curator`

- Purpose: maintain `okf/wiki/` as the durable context source of truth.
- Trigger: use when the OKF is missing, stale, invalid, or when external documentation needs evidence pages.
- Context inputs: `AGENTS.md`, relevant `okf/wiki/` pages, and the `agent-ready-context` skill.
- Permissions: read access is allowed; writes to OKF or `AGENTS.md` depend on user policy; shell access is limited to validation scripts.

This profile highlights the role of a durable documentation layer and suggests a broader pattern around [[concepts/durable-context]] and [[concepts/evidence-staging]].

### `skill-architect`

- Purpose: decide whether repeated actions should become reusable skills and create or update custom skills.
- Trigger: use when the OKF or user workflow reveals repeated executable actions.
- Context inputs: `AGENTS.md`, `okf/wiki/`, existing `.agents/skills/`, and the `skill-creator` skill.
- Permissions: read and write access to `.agents/skills/` depends on user policy; shell access is limited to validation scripts.

This profile centers on converting recurring workflows into reusable automation, connecting to [[concepts/skill-based-automation]] and workflow formalization.

### `repo-cartographer`

- Purpose: explore repository structure in a read-only way and summarize important files and flows.
- Trigger: use when initial repository understanding is needed before updating the OKF.
- Context inputs: `AGENTS.md`, `graphify-out/`, the file tree, and relevant source files.
- Permissions: read-only by default.

This profile emphasizes discovery and orientation before modification, relating to repository mapping and read-only reconnaissance.

## Main Ideas

- Profile intents can be expressed as minimal natural-language specifications independent of execution platform.
- A useful subagent definition balances mission, invocation conditions, context dependencies, and constraints.
- Permission boundaries are treated as first-class parts of subagent design rather than implementation details.
- Repository understanding, knowledge-base maintenance, and skill creation are presented as separable but cooperating agent roles.

## Potential Cross-Document Concepts

- profile intents
- [[concepts/subagent-role-design]]
- [[concepts/permission-scoped-agents]]
- [[concepts/durable-context]]
- [[concepts/skill-based-automation]]
- repository mapping

## Takeaway

The document contributes a simple template for defining reusable subagent profiles in a portable way, using three concrete examples that combine role intent, activation criteria, contextual inputs, and permission limits.

## Related Concepts
- [[concepts/tool-boundaries]]
- [[concepts/agent-context-layering]]
- [[concepts/agents-md-maintenance]]
- [[concepts/documentation-architecture]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/progressive-disclosure]]
- [[concepts/repository-overview-generation]]
- [[concepts/skill-governance]]
- [[concepts/skill-structure-conventions]]
- [[concepts/tooling-context-isolation]]

## Entities
- [[entities/agent-ready-context]]
- [[entities/agents-md]]
- [[entities/graphify]]
- [[entities/openai-system-skill-creator]]
- [[entities/openkb]]
- [[entities/vectifyai-openkb]]
