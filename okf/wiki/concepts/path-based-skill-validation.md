---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md"]
description: "Validating skills by checking their directory path and local files."
---

# Path-Based Skill Validation

Path-based skill validation is a lightweight way to confirm that a skill is placed in the correct directory and that its local metadata matches repository naming rules. In this model, the filesystem path is not just a container; it is part of the contract that determines whether a skill is considered valid.

The `quick_validate.py` script in [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]] is a concrete example of this approach. It validates a candidate skill directory by checking both the directory location and the contents of `SKILL.md`, treating path conformance as a first-class rule alongside frontmatter validation.

## What this concept covers

- The skill must be located under `.agents/skills`.
- The directory name must match the `name` field in `SKILL.md`.
- The validator uses the path to enforce repository-local placement rules.
- Structural checks are performed before accepting the skill as valid.

## Why path matters

Path-based validation helps ensure that skills are organized predictably and can be discovered consistently by tooling. It reduces ambiguity about where a skill belongs and supports [[concepts/skill-validation-workflow]] by making the directory layout part of the validation process.

This also fits with [[concepts/path-based-validation]] and [[concepts/filesystem-validation]], where correctness is derived from inspecting the filesystem rather than relying only on higher-level metadata.

## Key validation rules from the source

The validator applies several path-related checks:

- The target must be a directory.
- `SKILL.md` must exist inside the directory.
- The directory name must match the frontmatter `name` field.
- The skill must reside under `.agents/skills`.
- Optional subdirectories such as `scripts`, `references`, and `assets` must be directories if present.

These checks combine structure and metadata into a single validation pass, which keeps the process simple and fast.

## Broader implications

Path-based validation supports [[concepts/portable-skill-contract]] by making skill layout predictable across repositories. It also reinforces [[concepts/skill-structure-conventions]] and [[concepts/skill-governance]], because the repository can enforce where skills live and how they are named.

In practice, this style of validation favors quick preflight checks over deeper semantic analysis. That makes it useful for automation, but it also means it should be paired with stronger checks when higher confidence is needed, especially under [[concepts/deterministic-validation]] or [[concepts/generated-artifact-validation]].

## Related ideas

- [[concepts/frontmatter-metadata]] for the metadata embedded in `SKILL.md`
- [[concepts/lightweight-frontmatter-validation]] for simple parsing and field checks
- [[concepts/executable-validation]] for validation implemented as a runnable script
- [[concepts/preflight-checks]] for early failure before skill adoption
- [[concepts/quality-gates]] for using validation as an acceptance gate

## Source anchor

- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]