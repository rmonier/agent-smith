---
type: "Concept"
sources: ["summaries/agent-skills-spec.md"]
description: "Skills reveal metadata, instructions, and resources in layers."
---

# Skill Progressive Disclosure

Skill progressive disclosure is the practice of structuring an Agent Skill so agents load only the minimum information needed at each stage of use. The skill metadata is available at startup, the main `SKILL.md` instructions are loaded only when the skill is activated, and supporting files are fetched only when a task requires them. This reduces context load while keeping skills expressive and extensible.

## Core idea

The specification for [[summaries/agent-skills-spec]] describes skills as directories centered on a required `SKILL.md` file, with optional `scripts/`, `references/`, and `assets/` folders. That layout supports layered disclosure:

- metadata gives agents a quick signal that a skill is relevant
- the `SKILL.md` body provides the operational instructions
- resource files hold deeper detail, examples, templates, or executable helpers

This pattern helps an agent decide whether to activate a skill before paying the cost of loading its full content.

## How the layers work

- **Startup layer**: `name` and `description` are loaded broadly so agents can identify candidate skills quickly
- **Instruction layer**: the full `SKILL.md` body loads when the skill is selected
- **Resource layer**: files under `scripts/`, `references/`, and `assets/` are loaded on demand

The spec recommends keeping the main `SKILL.md` under 500 lines and moving detailed reference material out of the primary file. That keeps the default activation path compact while preserving access to richer guidance when needed.

## Why it matters

Progressive disclosure supports [[concepts/context-surface-management]] by limiting how much information competes for attention at once. It also aligns with [[concepts/agent-context-layering]] and [[concepts/documentation-layer-separation]], where each layer of documentation serves a different purpose and audience.

For skill systems, this yields several practical benefits:

- faster skill selection from lightweight metadata
- lower context overhead during routine tasks
- clearer separation between instructions and supporting detail
- easier maintenance as long reference material can live outside `SKILL.md`

## Design guidance from the spec

The source document recommends several concrete practices that make progressive disclosure work well:

- keep skill metadata concise and accurate so agents can match tasks quickly
- put the essential behavior in `SKILL.md`, not in scattered files
- split long reference material into focused files under `references/`
- keep scripts self-contained and documented so they can be pulled in only when needed
- avoid deep file-reference chains so resources remain easy to resolve

These rules make the skill portable and reduce the chance that important instructions are buried too deep to be discovered at the right time.

## Related concepts

- [[concepts/skill-structure-conventions]] for the directory and file layout that supports this model
- [[concepts/skill-frontmatter-schema]] for the metadata fields agents read first
- [[concepts/skill-resource-organization]] for how to split instructions, references, and assets
- [[concepts/agent-ready-context]] for assembling only the context needed for a task

## Takeaway

Skill progressive disclosure is a context-efficiency pattern: expose the smallest useful layer first, then reveal deeper instruction and resource layers only as the task demands.