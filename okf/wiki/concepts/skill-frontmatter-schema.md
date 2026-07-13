---
type: "Concept"
sources: ["summaries/agent-skills-spec.md"]
description: "Rules for the required YAML metadata in a skill's `SKILL.md` file."
---

# Skill Frontmatter Schema

The skill frontmatter schema defines the YAML metadata that must appear at the top of a skill's `SKILL.md` file. It is the compact, machine-readable header that lets agents identify a skill, decide whether to load it, and understand any operational constraints before reading the body instructions.

This concept is described in [[summaries/agent-skills-spec]] and is central to [[concepts/skill-structure-conventions]], [[concepts/skill-progressive-disclosure]], and [[concepts/path-based-skill-validation]].

## Purpose

Frontmatter gives a skill its identity and activation metadata. The specification treats it as the authoritative header for a skill directory, and the `name` field must match the parent directory name. That makes the metadata both human-readable and suitable for validation.

## Required fields

- `name`: required; lowercase letters, numbers, and hyphens only; 1-64 characters; no leading or trailing hyphen; no consecutive hyphens; must match the directory name
- `description`: required; 1-1024 characters; must explain what the skill does and when to use it

The `description` field is especially important for agent selection because it should contain task keywords that help the system identify the right skill for a request.

## Optional fields

- `license`: license name or bundled license file reference
- `compatibility`: environment requirements such as product, system packages, or network access, limited to 500 characters
- `metadata`: arbitrary string-to-string key/value pairs for extra properties
- `allowed-tools`: experimental space-separated list of pre-approved tools

These fields let a skill declare policy, runtime constraints, or auxiliary data without expanding the main instruction body.

## Validation implications

The schema is strict about naming and length limits, which makes it useful for [[concepts/deterministic-validation]] and [[concepts/generated-artifact-validation]]. The `name` rule in particular supports predictable directory-to-metadata alignment, while the `description` rule supports agent-facing discovery and activation.

Because the schema is small and explicit, it also fits into [[concepts/lightweight-frontmatter-validation]] and [[concepts/skill-validation-workflow]]. A skill can be rejected early if the frontmatter is malformed, mismatched, or missing required fields.

## Relationship to skill structure

Frontmatter is only the first layer of a skill definition. The markdown body carries the instructions, while optional `scripts/`, `references/`, and `assets/` directories support progressive disclosure. In practice, the schema is the entry point for [[concepts/portable-skill-contract]] and the foundation for skill loading, validation, and packaging.

## Key idea

The schema is intentionally minimal: enough metadata to route, validate, and constrain a skill, but not so much that it bloats the instruction file. That balance supports maintainable skill authoring and reinforces the separation between metadata and behavior.