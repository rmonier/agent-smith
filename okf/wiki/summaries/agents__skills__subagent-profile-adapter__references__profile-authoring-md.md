---
type: "Summary"
description: "Guidelines for authoring lean harness-native profile adapters."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md"
---

# Summary

This document defines how to author profile adapter files for the active harness, emphasizing that adapter structure must come from current harness documentation rather than fixed internal renderers.

## Core guidance

Profile adapters should stay minimal and task-focused. Each adapter is expected to state:

- the specialized task it handles;
- when the harness should invoke it;
- which skills it may use;
- which repository context it should consult;
- which permissions should be narrowed;
- what it must not do.

This frames profile authoring around clear operational boundaries, [[concepts/minimal-tool-scoping]], and [[concepts/permission-scoped-agents]].

## Recommended candidate profiles

The document proposes a small set of profile candidates, but only when they reflect real repository needs:

- `okf-curator` for refreshing and validating `okf/wiki/` and evidence pages;
- `skill-architect` for identifying repeated actions and creating or updating custom skills;
- `repo-cartographer` for read-only repository exploration and structural summaries;
- `security-reviewer` for reviewing authentication, secrets, CI/CD, supply chain, infrastructure as code, and risky defaults;
- `dependency-scout` for retrieving official external documentation and staging evidence.

These examples illustrate a repository-driven approach to [[concepts/subagent-role-design]] and [[concepts/skill-based-automation]].

## Anti-bloat rules

The file strongly discourages putting broad reference material into profile adapters. Adapters must not include:

- long project architecture explanations;
- copies of OKF pages;
- full external documentation;
- long troubleshooting narratives;
- vendor documentation beyond the minimum fields needed for validity.

This promotes concise adapter definitions and separation between execution guidance and reference material, aligning with [[concepts/adapter-bloat-prevention]] and [[concepts/context-action-separation]].

## Reference points

Instead of embedding large amounts of content, profile adapters should point to:

- `AGENTS.md` for orientation;
- `okf/wiki/` for source-of-truth repository context;
- `.agents/skills/` for actionable capabilities.

This creates a layered authoring model where adapters remain lightweight entry points into broader repository knowledge and skill systems, connected to [[concepts/agent-context-layering]] and [[concepts/skill-based-automation]].

## Takeaway

The main idea is that profile adapters should be harness-native, minimal, and grounded in current documentation and repository needs, with strict limits on embedded context and clear references to existing guidance and skills.

## Related Concepts
- [[concepts/harness-native-profiles]]
- [[concepts/runtime-adapter-management]]
- [[concepts/documentation-source-priority]]
- [[concepts/tool-boundaries]]
- [[concepts/durable-context]]
- [[concepts/skill-structure-conventions]]

## Entities
- [[entities/agents-md]]
- [[entities/openkb]]
