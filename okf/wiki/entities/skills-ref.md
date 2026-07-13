---
sources: ["summaries/agent-skills-spec.md"]
type: "Product"
description: "Validation library for checking Agent Skills packages"
---

# skills-ref

`skills-ref` is a validation library and command-line tool used to check whether an Agent Skill directory conforms to the official specification described in [[summaries/agent-skills-spec]]. The spec recommends it as the reference validator for skill authors.

## What it does

`skills-ref` validates a skill package by inspecting the `SKILL.md` file and its frontmatter, then checking naming and format rules. In the specification, it is used with a command like `skills-ref validate ./my-skill`.

## Key facts from the specification

- Validates the skill's `SKILL.md` frontmatter and naming conventions.
- Helps confirm that required fields such as `name` and `description` are present and compliant.
- Supports the validation workflow for Agent Skills during authoring and review.
- Is presented as the official reference library for skill validation.

## Related concepts

- [[concepts/skill-validation-workflow]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/path-based-skill-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/executable-validation]]
- [[concepts/skill-governance]]

## Related entity

- [[entities/agent-skills]]
