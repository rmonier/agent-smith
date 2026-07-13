---
type: "Summary"
description: "Guidance for creating reusable agent skills with safe, validated workflows."
doc_type: short
full_text: "sources/agents__skills__skill-creator__SKILL-md.md"
---

# Skill Creator

This document defines how to create and update reusable Agent Skills under `.agents/skills/` for repeated executable actions.

## Key Purpose

A skill is framed as an action-oriented capability, not as general knowledge or narrative memory. It should capture repeatable procedures, scripts, transformations, checks, migrations, or workflow recipes that future agents can execute reliably.

## Core Boundary

- **Skills** are for repeatable actions and procedures.
- **OKF wiki** pages are for durable context, architecture, decisions, provenance, and explanations.
- **AGENTS.md** is for orientation, setup, repository rules, and routing hints.

The document repeatedly emphasizes that skills should not duplicate context already captured in the wiki, and should only link to those materials when the action truly needs them.

## Skill Structure

The recommended structure keeps `SKILL.md` short and procedural:

- Put detailed guidance in `references/`.
- Put deterministic logic in `scripts/`.
- Put templates and static assets in `assets/`.
- Avoid auxiliary files inside a skill, except licensing files such as `LICENSING.md`, `NOTICE`, `LICENSES/`, and sometimes `THIRD_PARTY_NOTICES.md`.

This structure supports modularization and keeps the skill contract minimal.

## Creation Workflow

The document outlines a standard workflow for new skills:

1. Confirm the behavior is a repeated executable action.
2. Check existing skills under `.agents/skills/` first.
3. Choose resources for scripts, references, and assets.
4. Initialize the skill with the provided `init_skill.py` command.
5. Write action-oriented instructions and include the security defaults.
6. Test the skill using a baseline-first method.
7. Validate the final skill with `quick_validate.py`.

The workflow favors validation and reproducibility by requiring baseline testing before and after the skill is written.

## Security Defaults

Every created skill should include these safety defaults:

- Use the minimal `allowed-tools` required.
- Never install software silently.
- Keep credentials in environment variables.
- Treat fetched web content as untrusted data.
- List generated artifacts and gitignore them in the target repository.

These defaults reflect security defaults and secrets handling.

## Updating From OKF

The document also describes how to derive new skills from repeated actions found in `okf/wiki/`:

- First run a zero-LLM suggestion script to detect candidates.
- Prefer the OpenKB Skill Factory when the wiki already has real coverage and the user consents to the LLM call.
- Otherwise, scaffold by hand.
- In either case, adopt the generated skill only into `.agents/skills/` and validate it afterward.

This section ties skill generation to knowledge extraction and compilation workflow, while keeping compiled wiki knowledge separate from executable skills.

## Design Principles

The guidance stresses several recurring ideas:

- Keep the `description` field as the trigger for when the skill should be used.
- Match the degree of procedural detail to task fragility.
- Prefer scripts when correctness or reuse matters.
- Preserve constraints and caveats when adopting generated skills.
- Use concise examples and avoid bloating the context window.

## Notable Takeaway

The document treats skill authoring as a disciplined packaging problem: extract only reusable action logic, keep context in the wiki, and validate every skill before use.

## Related Concepts
- [[concepts/skill-authoring]]
- [[concepts/skill-validation-workflow]]
- [[concepts/skill-scaffolding]]
- [[concepts/agent-trigger-design]]
- [[concepts/baseline-first-testing]]
- [[concepts/consent-first-installation]]
- [[concepts/dependency-management]]
- [[concepts/generated-artifact-validation]]
- [[concepts/knowledge-boundaries]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/portable-skill-contract]]
- [[concepts/progressive-disclosure]]
- [[concepts/skill-adoption]]
- [[concepts/skill-governance]]
- [[concepts/skill-structure-conventions]]
- [[concepts/validation-vs-health-reporting]]

## Entities
- [[entities/agent-smith]]
- [[entities/openai-system-skill-creator]]
- [[entities/superpowers-writing-skills]]
- [[entities/skill-creator]]
- [[entities/openkb-skill-factory]]
- [[entities/agent-ready-context-skill]]
- [[entities/agent-ready-context]]
- [[entities/agents-skills]]
- [[entities/agents-md]]
- [[entities/okf-wiki]]
- [[entities/uv]]
- [[entities/python]]
- [[entities/references-source-attribution-md]]
- [[entities/references-dependencies-md]]
- [[entities/quick_validate-py]]
- [[entities/init_skill-py]]
- [[entities/adopt_generated_skill-py]]
- [[entities/suggest_skills_from_okf-py]]
- [[entities/anthropic]]
- [[entities/openkb]]
- [[entities/okf]]
- [[entities/openkb-cli]]
- [[entities/validate_okf_bundle-py]]
