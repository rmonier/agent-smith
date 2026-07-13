---
sources: ["summaries/agent-skills-spec.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"]
type: "Work"
description: "Fast validator script for Agent Skills directory structure and metadata."
---

# quick_validate.py

`quick_validate.py` is a Python command-line script in `.agents/skills/skill-creator/scripts/` that performs a fast structural check on an Agent Skills directory.

## What it does

- Verifies that the target path is a directory.
- Checks for a `SKILL.md` file in the directory.
- Parses basic YAML frontmatter from `SKILL.md`.
- Requires `name` and `description` fields.
- Enforces the Agent Skills naming rules for `name`, including lowercase letters, numbers, and hyphens only, no consecutive hyphens, and a match to the parent directory name.
- Limits `description` length to 1024 characters.
- Limits optional `compatibility` text to 500 characters.
- Confirms the skill is located under `.agents/skills`.
- Ensures `scripts`, `references`, and `assets` are directories if present.
- Reflects the official Agent Skills specification for skill layout and frontmatter validation.

## Validation approach

The script uses a lightweight frontmatter parser rather than a full YAML library. It reads the block between `---` markers and extracts simple `key: value` pairs, skipping blank lines and comment-like lines. This makes the validator small and dependency-light, but also means it only supports basic frontmatter shapes.

## Behavior

- On success, it prints `valid skill: <path>` and exits with status code `0`.
- On failure, it prints each validation problem prefixed with `error:` and exits with status code `1`.

## Implementation details

- Written for Python 3.11.
- Uses `argparse` for the CLI interface.
- Uses `pathlib.Path` for filesystem inspection.
- Applies a regular expression to enforce the skill naming convention.
- Treats parse errors as validation failures instead of crashing.
- Operates as a fast preflight check for the broader [[concepts/skill-validation-workflow]] and [[concepts/lightweight-frontmatter-validation]] approach.

## Related ideas

- [[concepts/lightweight-frontmatter-validation]]
- [[concepts/filesystem-validation]]
- [[concepts/path-based-skill-validation]]
- [[concepts/skill-validation-workflow]]
- [[concepts/deterministic-validation]]
- [[concepts/preflight-checks]]
- [[concepts/generated-artifact-validation]]
- [[concepts/action-oriented-documentation]]
- [[concepts/skill-authoring]]
- [[concepts/skill-scaffolding]]
- [[concepts/minimal-tool-scoping]]
- security defaults
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]

## Source

This entity is derived from the source summary for [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]], and it is used by [[summaries/agents__skills__skill-creator__SKILL-md]] as the final validation step for skill creation.

It also aligns with the official Agent Skills specification documented in [[summaries/agent-skills-spec]], especially the required `SKILL.md` frontmatter fields, directory structure, and validation guidance.

See also: [[summaries/README-md]]