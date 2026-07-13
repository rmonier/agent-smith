---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md"]
description: "Controlled creation of new skill directories with safe defaults and validation."
---

# Skill Scaffolding

Skill scaffolding is the process of creating a new skill directory with a consistent starting structure, minimal defaults, and placeholder instructions so authors can focus on the actual workflow instead of manual setup. It is a practical form of [[concepts/project-scaffolding]] and template generation that supports [[concepts/skill-authoring]], [[concepts/skill-governance]], and [[concepts/skill-validation-workflow]].

## What it includes

- Normalizing a human-entered name into a stable kebab-case identifier.
- Creating the target skill directory in the expected skills area.
- Optionally creating common support directories such as `scripts`, `references`, and `assets`.
- Writing an initial `SKILL.md` template with metadata and a procedural outline.
- Keeping the scaffold aligned with the repo's security defaults, including minimal tool scope and no silent installs.
- Enforcing basic validation so the scaffold is only created when the name and location are acceptable.

## Source behavior

The script in [[summaries/agents__skills__skill-creator__scripts__init_skill-py]] acts as a bootstrap tool for Agent Skills. It accepts a skill name, normalizes it with `normalize_name()`, checks the result against a name pattern, and refuses invalid output. It also constrains the destination to the `.agents/skills` area by default, which keeps initialization aligned with [[concepts/path-safety]] and [[concepts/directory-bootstrap]].

When the target directory is created, the script writes a starter `SKILL.md` file if one does not already exist, or if `--force` is used. The generated file includes a name, description, license, metadata block, and placeholder sections for workflow and commands. The document also frames skills as executable capabilities, recommends keeping `SKILL.md` short, and pushes detail into `references/`, `scripts/`, and `assets/` so the scaffold stays lightweight and maintainable.

The same source adds stronger governance rules around skill creation: use skills for repeatable actions, treat OKF as context rather than execution logic, check for existing vendor coverage before creating new custom skills, and validate every skill before finishing. It also codifies security defaults for all created skills: minimal `allowed-tools`, consent-first installation, secrets in environment variables, untrusted web content handling, and gitignored generated artifacts.

## Key properties

- **Repeatable:** The same inputs produce the same directory shape and starter file.
- **Constrained:** Only approved resource folders are created.
- **Opinionated:** The scaffold favors a predictable skill layout over arbitrary customization.
- **Expandable:** `--resources` allows common supporting folders without changing the core template.
- **Validation-first:** Name and path checks happen before files are written, and the generated skill is meant to pass quick validation before use.

## Why it matters

Scaffolding reduces friction when creating new skills and helps maintain a consistent [[concepts/skill-structure-conventions]] across the repository. It also supports [[concepts/evidence-backed-skill-initialization]] by turning skill creation into a controlled, repeatable workflow rather than an ad hoc manual process.

A well-designed scaffold improves discoverability, makes later validation easier, and lowers the chance of malformed or misplaced skill directories. In that sense, it is a foundational step in skill-driven authoring pipelines and broader [[concepts/portable-skill-contract]] practices.

## Related concepts

- [[concepts/kebab-case-normalization]]
- [[concepts/filesystem-validation]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/generated-artifact-validation]]
- [[concepts/skill-validation-workflow]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/consent-first-installation]]
- wiki wiki boundaries

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]
