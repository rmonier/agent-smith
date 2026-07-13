---
type: "Summary"
description: "Script copies and validates generated skills into `.agents/skills/`."
doc_type: short
full_text: "sources/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"
---

# .agents/skills/skill-creator/scripts/adopt_generated_skill.py

This script adopts a generated skill from `okf/output/skills/` into `.agents/skills/`, then validates the copied result with the local `quick_validate.py` helper.

## Purpose

- Provides a repeatable way to move a generated skill into the repository-owned skills area.
- Enforces a basic naming rule before copying anything.
- Refuses to overwrite an existing skill unless `--force` is supplied.
- Runs validation immediately after the copy so bad skills are rejected early.

## Main behavior

- Accepts a skill `name` plus optional `--repo`, `--source`, `--dest`, and `--force` flags.
- Validates `name` with `NAME_RE` and also rejects names containing `--`.
- Resolves paths relative to the chosen repository root.
- Requires `SKILL.md` to exist in the source skill directory.
- Copies the source directory tree into the destination with `shutil.copytree()`.
- Invokes `quick_validate.py` via `subprocess.run()` on the adopted skill.

## Safety and recovery

- If the destination already exists and `--force` is not set, the script aborts rather than replacing it.
- If validation fails after a fresh copy, it removes the copied destination to avoid leaving behind a broken skill.
- If validation fails after replacing an existing skill, it leaves the replacement in place and asks for manual fixing or removal.

## Operational constraints

- The accepted skill name pattern is limited to lowercase letters, digits, and hyphens, with length bounds enforced by the regex.
- The script assumes generated skills live under `okf/output/skills/` by default and project skills live under `.agents/skills/`.
- The validator path is derived from the script location, so it stays tied to the skill-creator tooling layout.

## Notable guidance embedded in the script

- The post-validation messages remind the user to review the adopted skill against skill-creator standards.
- It specifically calls out trigger-style descriptions, minimal scoped allowed-tools, untrusted-content handling, and avoiding secrets.
- It also warns that distilled skills should preserve constraints, boundaries, and cautions from the wiki sources they came from, linking this workflow to generated artifact adoption and caveat preservation as related cross-document topics.

## Key ideas

- Generated skills are treated as drafts that still need human review.
- Validation is part of adoption, not a separate optional step.
- The script favors safe failure modes, especially when creating a new destination.
- The copy is intentionally project-owned once adopted, so the user is expected to inspect and adjust it before committing.

## Related Concepts
- [[concepts/skill-adoption]]
- [[concepts/generated-artifact-validation]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/skill-validation-workflow]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/deterministic-validation]]
- [[concepts/path-based-validation]]
- [[concepts/prompt-injection-defense]]
- [[concepts/caveat-preservation]]
- [[concepts/portable-skill-contract]]
- [[concepts/skill-vendoring]]

## Entities
- [[entities/adopt_generated_skill-py]]
- [[entities/quick_validate-py]]
- [[entities/skill-creator]]
- [[entities/openkb-skill-factory]]
- [[entities/agents-skills]]
- [[entities/openkb-cli]]
- [[entities/python]]
