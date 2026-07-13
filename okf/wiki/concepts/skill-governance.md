---
type: "Concept"
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Rules and boundaries for controlling how agent skills are created and used."
---

# Skill Governance

Skill governance is the set of rules that controls how agent skills are defined, scoped, adopted, and maintained so they stay focused on repeatable actions rather than absorbing durable knowledge or orientation material.

## What It Covers

The agent-ready-context skill treats skills as the execution layer of the repository agent surface. Governance here means deciding:

- what belongs in a skill versus what belongs in the OKF wiki or `AGENTS.md`
- how skills should be scoped to repeatable procedures, scripts, checks, and workflows
- when a skill should be updated, replaced, or split
- how companion and vendor skills are adopted safely

This keeps the repository's agent surface aligned with [[concepts/context-action-separation]] and [[concepts/skill-based-automation]].

## Core Principles

The source document establishes a few strong governance rules:

- **Skills are actions**: they should describe procedures that can be executed again.
- **Context stays in the wiki**: durable repository knowledge, provenance, and cross-document memory belong in the OKF wiki, not in skills.
- **Orientation stays in `AGENTS.md`**: that file should remain a concise navigation and best-practices surface.
- **Repeatability matters**: if content is not an action, it should usually not become a skill.

These rules are part of a broader [[concepts/knowledge-lifecycle-governance]] model for repository memory.

## Governance in Practice

The document uses governance in several operational ways:

- It warns against turning compiled OKF context into a skill unless the knowledge really describes a reusable action.
- It requires companion and vendor skills to be handled deliberately, with read-only vendor skills copied into the repo before first use.
- It encourages reviewing the wiki, source pack, and `AGENTS.md` for repeated actions that might justify a new skill.
- It treats skill creation as a downstream decision, not an automatic response to every repeated pattern.

This is closely related to [[concepts/skill-vendoring]], [[concepts/minimal-tool-scoping]], and [[concepts/tool-boundaries]].

## Why It Matters

Without governance, agent skills can become bloated, redundant, or confused with documentation. The skill avoids that by preserving clean boundaries between:

- execution tooling
- durable knowledge
- repository orientation

That separation supports [[concepts/agent-context-layering]], [[concepts/durable-context]], and [[concepts/generated-content-governance]].

## Related Ideas

- [[concepts/agent-ready-context-skill]]
- [[concepts/agent-ready-repositories]]
- [[concepts/agents-md-maintenance]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-vendoring]]
- [[concepts/permission-scoped-agents]]
- [[concepts/consent-first-tooling]]
- [[concepts/supply-chain-security]]

## Source Link

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agent-skills-spec]]