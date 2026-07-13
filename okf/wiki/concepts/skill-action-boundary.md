---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
description: "Separates reusable skills from wiki context and orientation docs."
---

# Skill Action Boundary

The skill-action boundary distinguishes reusable, executable agent capabilities from documentation that only provides context or orientation. In the skill-creator guidance, a skill is treated as a repeatable action pattern, while the OpenKB wiki is reserved for durable knowledge and `AGENTS.md` is reserved for repository guidance.

## What Belongs In A Skill

Skills are for repeated behaviors that can be carried out reliably by an agent. Typical skill content includes:

- scripts for deterministic work
- workflows for tool use or validation
- transformations, migrations, scaffolds, and checks
- action recipes that need to be reused across sessions

This framing keeps skills tied to [[concepts/action-oriented-documentation]] and [[concepts/skill-based-automation]], rather than turning them into general notes.

## What Does Not Belong In A Skill

The source document draws a strong line between skills and other repository knowledge layers:

- the wiki is for durable context, evidence, architecture, and explanations
- `AGENTS.md` is for setup, tests, repo rules, and routing hints
- skills should not duplicate context already captured in the wiki

This separation supports [[concepts/context-action-separation]] and [[concepts/knowledge-boundaries]].

## Why The Boundary Matters

Keeping skills narrowly action-focused reduces drift and makes them more reliable in agent workflows. It also helps prevent a skill from becoming a second knowledge base, which would blur ownership and make maintenance harder.

The document emphasizes:

- concise procedural instructions over long narrative
- deterministic code in `scripts/`
- detailed guidance in `references/`
- templates and static resources in `assets/`
- validation before release

These rules align with [[concepts/skill-structure-conventions]], [[concepts/skill-resource-organization]], and [[concepts/skill-validation-workflow]].

## Practical Implications

When a repeated action emerges, the right response is to create or update a skill. When the material is explanatory, historical, or cross-cutting, it belongs in the wiki instead. The boundary is therefore not just organizational; it is a governance rule for [[concepts/skill-governance]] and [[concepts/knowledge-lifecycle-governance]].

The source document at [[summaries/agents__skills__skill-creator__SKILL-md]] treats this boundary as the core design principle for Agent Skills.

See also: [[summaries/agents__skills__skill-creator__references__dependencies-md]]