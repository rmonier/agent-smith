---
type: "Summary"
description: "CLI script scaffold that creates normalized Agent Skills directories and SKILL.md files."
doc_type: short
full_text: "sources/agents__skills__skill-creator__scripts__init_skill-py.md"
---

# .agents/skills/skill-creator/scripts/init_skill.py

This script initializes a new Agent Skills compliant skill under `.agents/skills` by default. It normalizes a user-provided name, validates the target location, creates the skill directory, optionally creates common resource subdirectories, and writes a starter `SKILL.md` file.

## What it does

- Normalizes the supplied skill name into kebab-case using `normalize_name()`.
- Enforces a naming rule via `NAME_RE`, including length limits and lowercase alphanumeric/hyphen formatting.
- Refuses to write outside a `.agents/skills`-scoped path unless the parent path still appears to be within `.agents`.
- Creates the target skill directory, with `--force` allowing reuse of an existing directory.
- Writes a template `SKILL.md` containing frontmatter-like metadata and a procedural starting outline.
- Optionally creates `scripts`, `references`, and `assets` subdirectories from `--resources`.

## Key concepts

- [[concepts/kebab-case-normalization]]: Converts user-facing names into a stable machine-friendly format.
- [[concepts/path-safety]]: Applies guardrails to prevent writing outside the intended skills area.
- [[concepts/skill-scaffolding]]: Generates a consistent starter structure for new skill directories.
- [[concepts/generated-content-governance]]: Produces a starter `SKILL.md` from a fixed text template.
- [[concepts/validation-vs-health-reporting]]: Checks names and resource flags before creating files and directories.

## Behavior details

- `--path` sets the parent directory and defaults to `.agents/skills`.
- `--resources` accepts a comma-separated list limited to `scripts`, `references`, and `assets`.
- `--force` allows overwriting an existing `SKILL.md` and reusing an existing skill directory.
- The generated `SKILL.md` is intentionally generic, encouraging the user to replace placeholders with the actual workflow, commands, and validation steps.

## Notable findings

- The script couples directory creation with document templating, making it a single-entry bootstrap for skill authoring.
- The safety check for the parent path is lightweight and heuristic-based, relying on string and path-part inspection rather than strict resolution.
- The generated template emphasizes procedural guidance and defers detailed context to OKF, suggesting a separation between operational instructions and knowledge-base content.
- The `--resources` flag provides a constrained extension mechanism for common supporting materials without allowing arbitrary directory names.

## Outputs

- A normalized skill directory path is printed on success.
- Errors are surfaced as `SystemExit` messages for invalid names, invalid resource names, or disallowed target locations.

## Related ideas

- [[concepts/skill-scaffolding]]
- command line interfaces
- [[concepts/path-safety]]
- reusable workflows

## Related Concepts
- [[concepts/directory-bootstrap]]
- [[concepts/naming-normalization]]
- [[concepts/project-scaffolding]]
- [[concepts/skill-structure-conventions]]
- [[concepts/portable-skill-contract]]
- [[concepts/consent-first-workflows]]
- [[concepts/skill-authoring]]
- [[concepts/skill-governance]]
- [[concepts/skill-adoption]]
- [[concepts/filesystem-validation]]
- [[concepts/generated-artifact-validation]]
- [[concepts/project-scaffolding]]

## Entities
- [[entities/init_skill-py]]
- [[entities/agents-skills]]
- [[entities/skill-creator]]
- [[entities/openkb-skill-factory]]
- [[entities/openai-system-skill-creator]]
- [[entities/romain-monier]]
- [[entities/apache-license-2-0]]
- [[entities/agent-skills]]
- [[entities/skill-creator-references-dependencies-md]]
- [[entities/references-source-attribution-md]]
- [[entities/third-party-notices-md]]
