---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
description: "Design descriptions as invocation triggers, not workflow summaries."
---

# Agent Trigger Design

[[concepts/agent-trigger-design]] is the practice of writing a skill or capability description so an agent can recognize when to invoke it, rather than trying to teach the procedure in the trigger text itself.

## Core idea

A trigger description should answer: *what does this skill do, and in what concrete situations should it be used?* It should not try to compress the workflow, implementation details, or edge-case handling into the short description field.

In [[summaries/agents__skills__skill-creator__SKILL-md]], this appears as an explicit rule: write the `description` as the trigger, and never as a summary of the workflow. The reason is practical: an agent may act on the description alone before reading the full body, so the description must optimize for correct routing.

## Why it matters

Good trigger design improves:

- invocation accuracy, by making the intended use cases easy to match
- [[concepts/skill-based-automation]], by helping agents select the right reusable action
- [[concepts/agent-context-layering]], by keeping short routing metadata separate from detailed procedural instructions
- [[concepts/context-action-separation]], by distinguishing "when to use this" from "how to do it"
- [[concepts/documentation-cohesion]], by giving each part of a skill a clear job

Poor trigger design causes a common failure mode: the description becomes a miniature procedure. When that happens, agents may follow an incomplete sketch instead of consulting the full skill instructions, scripts, or references.

## Trigger design in skills

Within an Agent Skill, the description field acts like a routing surface. It should:

- name the action outcome clearly
- mention the concrete contexts that should activate the skill
- avoid procedural steps
- avoid lengthy rationale or background knowledge
- stay specific enough to distinguish the skill from nearby alternatives

This makes the description a selector, while `SKILL.md`, `scripts/`, and `references/` carry execution detail. That division supports [[concepts/skill-structure-conventions]] and [[concepts/progressive-disclosure]].

## Relationship to action-oriented documentation

Trigger design is a narrow but important part of [[concepts/action-oriented-documentation]]. Action-oriented documentation explains what action to take and how to perform it. Trigger design focuses even earlier in the decision path: whether this is the right action to take at all.

A well-designed trigger therefore sits at the boundary between discovery and execution:

- the description helps the agent choose the skill
- the body of the skill explains how to perform the task
- supporting resources handle validation, edge cases, and deterministic execution

## Design heuristics

Useful trigger descriptions usually include:

- the repeated action the skill supports
- the kinds of repository state, user request, or workflow signal that should cause invocation
- distinguishing context that separates it from neighboring skills

They usually avoid:

- command-by-command instructions
- long lists of caveats better placed in the body
- broad wording that overlaps many unrelated skills
- knowledge-base material that belongs in durable context

This aligns with [[concepts/knowledge-boundaries]] and the source document's insistence that skills remain action-focused rather than turning into narrative context stores.

## Example pattern

A strong trigger description says, in effect:

- use this when repeated work reveals a reusable executable workflow
- use this when repository guidance or user requests indicate a capability should become a skill

A weak trigger description says, in effect:

- first inspect the repo, then create folders, then write frontmatter, then run validation

The first helps routing. The second tempts premature execution from incomplete instructions.

## Risks of weak trigger design

If trigger descriptions are poorly written, agents may:

- invoke the wrong skill
- skip the full instructions
- confuse context documents with action skills
- duplicate capabilities because existing skills are hard to identify
- create brittle automation from under-specified summaries

These risks connect to [[concepts/failure-driven-development]] and [[concepts/executable-validation]], because misrouting often only becomes visible when a task fails or validation reveals gaps.

## In the source document

[[summaries/agents__skills__skill-creator__SKILL-md]] treats trigger design as a core authoring principle for reusable skills. The document frames the description field as a practical control point for agent behavior: if the trigger is well designed, the agent knows when to load the skill; if it is badly designed, the skill may be misused before its full constraints are read.

That makes trigger design a small metadata choice with outsized impact on reliability, discoverability, and correct automation boundaries.

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]