---
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md"]
type: "Work"
description: "Python bootstrap script for creating new Agent Skills directories"
---

# init_skill.py

`init_skill.py` is a Python command-line script in `.agents/skills/skill-creator/scripts/` that bootstraps a new Agent Skills-compliant skill directory.

## What it does

- Normalizes a requested skill name into kebab-case.
- Validates the normalized name with a strict regex and length limit.
- Refuses to write outside `.agents/skills`-scoped paths.
- Creates the target skill directory, with `--force` allowing reuse of an existing one.
- Writes a starter `SKILL.md` file with metadata and a procedural template.
- Optionally creates `scripts`, `references`, and `assets` subdirectories.
- Encodes the skill-creation contract as a controlled bootstrap step for [[concepts/skill-scaffolding]] and [[concepts/skill-authoring]].
- Aligns the generated skill layout with the official Agent Skills specification for `SKILL.md`, optional supporting directories, and progressive disclosure.

## Key facts

- The script exposes a `main()` entry point and exits with status codes via `SystemExit`.
- `normalize_name()` lowercases input, replaces non-alphanumeric runs with hyphens, and trims repeated separators.
- `NAME_RE` enforces a kebab-case pattern with up to 64 characters.
- The default parent path is `.agents/skills`.
- The generated `SKILL.md` includes a name, description, license, metadata block, workflow outline, and command stub.
- The surrounding skill-creator guidance treats this script as one step in a larger validation-first workflow, not as a standalone generator.
- The spec it targets requires `SKILL.md` frontmatter fields such as `name` and `description`, supports optional `license`, `compatibility`, `metadata`, and `allowed-tools`, and recommends keeping the main file short while moving detail into `scripts/`, `references/`, and `assets/`.

## Related concepts

- [[concepts/skill-scaffolding]]
- [[concepts/kebab-case-normalization]]
- [[concepts/path-safety]]
- [[concepts/directory-bootstrap]]
- [[concepts/portable-skill-contract]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/skill-structure-conventions]]
- validation
- template generation

## Related source

- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/agent-skills-spec]]

## Significance

This script is part of the skill-creation workflow and serves as a controlled bootstrap mechanism for new skills, combining naming normalization, path validation, directory creation, and starter-document generation in one step.

It fits the broader skill-creator rules that keep `SKILL.md` short, push details into resource directories, and require validation before a skill is considered ready.

The Agent Skills specification strengthens that workflow by defining the exact file structure, frontmatter constraints, and progressive disclosure model that `init_skill.py` is expected to scaffold.

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]