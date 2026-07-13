---
type: "Summary"
description: "Guidance for separating reusable actions, durable context, and repo orientation."
doc_type: short
full_text: "sources/agents__skills__skill-creator__references__action-vs-context-md.md"
---

# Summary

This reference defines where different kinds of agent-facing information should live: in a skill, in the OKF wiki, or in `AGENTS.md`.

## Core guidance

The document draws a boundary between procedural behavior and durable knowledge:

- Put information in a skill when it describes a repeatable action or workflow the agent should execute.
- Put information in the OKF wiki when it captures durable project context, background, rationale, or repository knowledge.
- Put information in `AGENTS.md` when it serves as concise repository orientation.

This is a practical distinction between procedural knowledge and project context, with `AGENTS.md` acting as lightweight repository orientation.

## When to use a skill

A skill is the right home for repeatable procedures, especially when the agent or harness should reliably perform them again. The reference includes examples such as:

- multi-step command sequences
- predictable file generation or transformation
- artifact validation workflows
- tool or API calls with non-obvious flags
- repeated scaffolding patterns
- migrations or incident workflows
- vendor skill wrappers with project-specific guardrails

This frames skills as reusable automation for repeatable workflows and agent automation.

## When to use the OKF wiki

The OKF wiki should store durable context that helps agents understand the project over time. Examples include:

- architecture and component explanations
- provenance and external documentation evidence
- design decisions and tradeoffs
- runbook background and reasons a workflow exists
- repository-specific facts discovered during analysis
- historical memory about the project

This positions the wiki as long-term storage for architectural knowledge, design rationale, and source provenance.

## When to use `AGENTS.md`

`AGENTS.md` should remain concise and focused on quick orientation. Appropriate content includes:

- setup and test commands
- repository-specific rules
- directions to important locations such as `okf/wiki/`, `graphify-out/`, and `.agents/skills/`
- security and contribution practices
- maintenance reminders

This makes `AGENTS.md` a compact guide for agent onboarding and repository orientation.

## Vendor skill rule

Vendor skills are treated as dependencies rather than editable project files. The document advises:

- install and update them through the selected skill manager
- keep generated lock files such as `skill-lock.json` when present
- avoid patching vendor files directly
- place project-specific changes in custom skills under `.agents/skills/`

This introduces a dependency-management principle for vendor dependencies and project specific guardrails.

## Key takeaway

The main contribution is a placement rule:

- actions and repeatable procedures belong in skills
- durable understanding belongs in the OKF wiki
- concise orientation belongs in `AGENTS.md`

This separation helps maintain clearer boundaries between action context boundaries, durable knowledge, and execution-focused agent tooling.

## Related Concepts
- [[concepts/context-action-separation]]
- [[concepts/agent-context-layering]]
- [[concepts/dependency-management]]
- [[concepts/agents-md-maintenance]]
- [[concepts/documentation-architecture]]
- [[concepts/durable-context]]
- [[concepts/skill-based-automation]]
- [[concepts/tool-boundaries]]
- [[concepts/tooling-context-isolation]]

## Entities
- [[entities/agents-md]]
- [[entities/openkb]]
