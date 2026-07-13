---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"]
description: "Safe process for copying, validating, and reviewing generated skills."
---

# Skill Adoption

Skill adoption is the controlled process of moving a generated skill from a source staging area into the repository-owned skills directory, then validating it before treating it as usable. It sits between [[concepts/generated-artifact-adoption]] and [[concepts/generated-artifact-validation]], with a strong emphasis on review, provenance, and safe replacement behavior.

## What it does

The adoption workflow in [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]] copies a skill from `okf/output/skills/` into `.agents/skills/`, then runs `quick_validate.py` against the copied result. The script is designed to make adoption explicit rather than implicit, so a generated skill is not considered ready until it passes validation.

## Core rules

- The skill name must match a restricted lowercase, hyphenated naming pattern.
- The source skill must contain `SKILL.md` before adoption can proceed.
- Existing destination skills are protected from accidental overwrite unless `--force` is used.
- Fresh copies are removed automatically if validation fails.
- Replaced skills are left in place on validation failure so the user can repair or remove them manually.

## Why it matters

Skill adoption is a governance boundary. Generated output may be useful, but it still needs human review, validation, and alignment with local standards before it becomes part of the repo-owned skill set. This aligns with [[concepts/skill-validation-workflow]], [[concepts/human-in-the-loop-review]], and [[concepts/safe-automation]].

The script’s post-validation reminders also reinforce that adopted skills should preserve important constraints from their source material, which connects to [[concepts/caveat-preservation]] and [[concepts/knowledge-distillation-risks]].

## Operational characteristics

- Path handling is repo-relative and resolved from the chosen repository root.
- Validation is executed immediately after copying, making adoption a single, auditable action.
- The workflow assumes a trusted local toolchain for the validator, but still treats the generated skill itself as something that must be checked.
- The script favors conservative failure modes over convenience when destination state is uncertain.

## Related ideas

- [[concepts/generated-artifact-adoption]] — broader pattern of accepting generated output into a maintained codebase.
- [[concepts/generated-artifact-validation]] — validation as a required gate before adoption.
- [[concepts/deterministic-validation]] — predictable checks that make adoption outcomes reproducible.
- [[concepts/path-safety]] — careful path resolution and guarded filesystem operations.
- [[concepts/minimal-tool-scoping]] — review of the adopted skill’s tool use after copy.
- [[concepts/skill-governance]] — keeping skills aligned with local standards and review practices.

See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]