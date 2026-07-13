---
type: "Summary"
description: "Official format spec for Agent Skills directories, metadata, and validation."
doc_type: short
full_text: "sources/agent-skills-spec.md"
---

# Agent Skills Specification

This document defines the official format for an Agent Skill: a directory centered on a required `SKILL.md` file with optional supporting code, references, and assets. It explains the expected frontmatter fields, naming rules, progressive disclosure model, and validation approach for skills used by agents.

## Key structure

A skill must be a directory that contains at minimum a `SKILL.md` file. Optional subdirectories may include `scripts/`, `references/`, and `assets/` for executable helpers, deeper documentation, and static resources. This layout supports [[concepts/skill-progressive-disclosure]] by keeping the main instruction file concise and moving detailed material into separate files.

## `SKILL.md` requirements

`SKILL.md` must contain YAML frontmatter followed by Markdown body content.

Required frontmatter fields:
- `name`: lower-case, hyphenated, 1-64 characters, no leading/trailing hyphen, no consecutive hyphens, and must match the parent directory name
- `description`: non-empty, 1-1024 characters, describing both what the skill does and when to use it

Optional frontmatter fields:
- `license`: license name or bundled license file reference
- `compatibility`: environment requirements such as product, packages, or network access, limited to 500 characters
- `metadata`: arbitrary string key/value pairs for extra properties
- `allowed-tools`: space-separated list of pre-approved tools, marked experimental

The body of `SKILL.md` has no formal restrictions, but the spec recommends including step-by-step instructions, examples, and edge cases.

## Design principles

The spec emphasizes that agents load skills progressively:
- metadata is available at startup
- the full `SKILL.md` body is loaded only when the skill is activated
- supporting resources are loaded only when needed

This encourages concise skill definitions and encourages splitting longer material into files under `references/` or `scripts/`.

## Supporting files

Scripts should be self-contained or clearly document dependencies, include helpful error messages, and handle edge cases gracefully. Reference files should stay focused and be used for on-demand detail. Asset files can provide templates, images, or data files.

## File reference guidance

When one skill file references another, the spec says to use relative paths from the skill root and keep references one level deep from `SKILL.md` to avoid long chains.

## Validation

The document recommends validating skills with the `skills-ref` library using `skills-ref validate ./my-skill`. Validation checks frontmatter correctness and naming conventions, making it a useful compliance step for skill authors.

## Takeaway

Overall, this specification formalizes a compact, modular skill format optimized for agent loading behavior, maintainability, and validation. It is directly relevant to [[concepts/skill-authoring]], [[concepts/skill-frontmatter-schema]], and [[concepts/skill-validation-workflow]].

## Related Concepts
- [[concepts/agent-skill-specification]]
- [[concepts/progressive-disclosure]]
- [[concepts/skill-structure-conventions]]
- [[concepts/portable-skill-contract]]
- [[concepts/skill-governance]]
- [[concepts/skill-resource-organization]]
- [[concepts/spec-authority]]

## Entities
- [[entities/agent-skills]]
- [[entities/agentskills-io]]
- [[entities/skills-ref]]
- [[entities/openkb]]
- [[entities/skill-creator]]
- [[entities/init_skill-py]]
- [[entities/quick_validate-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/pyyaml]]
- [[entities/python]]
- [[entities/agents-skills]]
- [[entities/openkb-cli]]
- [[entities/openkb-skill-factory]]
