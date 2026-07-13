---
type: "Summary"
description: "Validates an Agent Skills directory against naming and metadata rules."
doc_type: short
full_text: "sources/agents__skills__skill-creator__scripts__quick_validate-py.md"
---

# .agents/skills/skill-creator/scripts/quick_validate.py

This script provides a fast command-line validator for an Agent Skills directory. It checks that a candidate skill folder has the expected structure, that `SKILL.md` exists, and that required frontmatter fields are present and well-formed.

## What it validates

- `SKILL.md` must exist in the target directory.
- The file must begin with YAML frontmatter and close it properly.
- Frontmatter must include `name` and `description`.
- `name` must match the repository's skill naming pattern and the directory name.
- `description` must be present and no longer than 1024 characters.
- `compatibility`, if present, must not exceed 500 characters.
- The skill must live under `.agents/skills`.
- `scripts`, `references`, and `assets` must be directories if they exist.

## Validation rules

The script enforces a compact naming convention via a regular expression that allows lowercase letters, digits, and hyphens, with length limits and no leading or trailing hyphen. It also rejects names containing double hyphens.

Frontmatter parsing is intentionally simple: it reads the block between the opening and closing `---` markers and extracts `key: value` pairs, skipping blank lines and comment-like lines.

## Behavior

- On success, it prints `valid skill: <path>` and exits with status code `0`.
- On failure, it prints each error prefixed with `error:` and exits with status code `1`.

## Implementation notes

- Uses `argparse` for a single positional `skill` argument.
- Uses `pathlib.Path` for filesystem checks.
- Treats parsing failures as validation errors rather than crashing.
- Includes a Python 3.11 requirement marker and SPDX licensing metadata.

## Key concepts

- [[concepts/deterministic-validation]]
- [[concepts/frontmatter-metadata]]
- [[concepts/filesystem-validation]]
- [[concepts/skill-validation-workflow]]

## Findings

- The validator focuses on lightweight structural checks rather than full YAML parsing.
- The path rule is broad: it accepts any path containing `.agents` in `root.parts` or whose parent path ends with `.agents/skills`, which may be more permissive than a strict location check.
- The script distinguishes between missing fields, length limits, naming violations, and directory layout problems, making failures easy to interpret.

## Related Concepts
- [[concepts/lightweight-frontmatter-validation]]
- [[concepts/path-based-skill-validation]]
- [[concepts/skill-structure-conventions]]
- [[concepts/path-based-validation]]
- [[concepts/skill-governance]]
- [[concepts/preflight-checks]]
- [[concepts/portable-skill-contract]]
- [[concepts/kebab-case-normalization]]
- [[concepts/repository-structure-overview]]

## Entities
- [[entities/quick_validate-py]]
- [[entities/skill-creator]]
- [[entities/agents-skills]]
- [[entities/openkb]]
- [[entities/python]]
- [[entities/uv]]
- [[entities/pyyaml]]
- [[entities/init_skill-py]]
- [[entities/openkb-cli]]
- [[entities/validate_okf_bundle-py]]
- [[entities/check_prereqs-py]]
