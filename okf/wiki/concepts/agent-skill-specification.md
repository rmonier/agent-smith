---
type: "Concept"
sources: ["summaries/agent-skills-spec.md"]
description: "Rules for structuring and validating portable Agent Skills."
---

# Agent Skill Specification

The Agent Skill Specification defines the portable on-disk contract for an agent skill: a directory centered on a required `SKILL.md` file, with optional supporting scripts, references, and assets. It standardizes how skills describe themselves, how they are loaded, and how they are validated.

## Core idea

A skill is both a packaging format and an instruction format. The spec aims to make skills easy for agents to discover, activate, and execute while keeping the main instruction file small enough for efficient loading. This makes it closely related to [[concepts/skill-structure-conventions]], [[concepts/skill-frontmatter-schema]], [[concepts/skill-progressive-disclosure]], and [[concepts/skill-validation-workflow]].

## Directory structure

A skill directory must contain `SKILL.md` and may also include:

- `scripts/` for executable helpers
- `references/` for deeper documentation
- `assets/` for templates, resources, and static files

The structure encourages separating high-level instructions from implementation detail, which supports [[concepts/documentation-layer-separation]] and [[concepts/managed-document-sections]].

## `SKILL.md` frontmatter

`SKILL.md` must begin with YAML frontmatter followed by Markdown body content.

Required fields:
- `name`: lowercase letters, numbers, and hyphens only; 1-64 characters; no leading, trailing, or consecutive hyphens; must match the parent directory name
- `description`: non-empty; 1-1024 characters; should explain what the skill does and when to use it

Optional fields:
- `license`: license name or bundled license file reference
- `compatibility`: environment requirements such as product, packages, or network access
- `metadata`: arbitrary string key/value pairs for extra properties
- `allowed-tools`: space-separated list of pre-approved tools; experimental

These rules connect directly to [[concepts/frontmatter-metadata]], [[concepts/naming-normalization]], and [[concepts/configuration-precedence]] in the broader wiki.

## Body content

The body of `SKILL.md` has no formal format restrictions, but the specification recommends including:

- step-by-step instructions
- examples of inputs and outputs
- common edge cases

The body is the main operational guidance for the agent once a skill is activated, so it should stay concise and practical. Longer detail belongs in referenced files.

## Progressive disclosure

A central design principle is progressive disclosure:

1. Metadata is available at startup for all skills
2. The full `SKILL.md` body is loaded only when a skill is activated
3. Supporting files are loaded only when needed

This keeps startup cost low and reinforces [[concepts/context-surface-management]] and [[concepts/durable-context]] by exposing only the amount of information needed at each stage.

## Supporting resources

The spec allows skills to include supplementary files:

- scripts should be self-contained or clearly document dependencies, handle edge cases, and produce helpful errors
- references should be small and focused, such as technical references or form templates
- assets should hold static resources like templates, images, or lookup data

This modularity aligns with [[concepts/skill-resource-organization]] and [[concepts/deterministic-validation]] when skills are checked by tooling.

## File references and validation

When one skill file references another, the spec recommends relative paths from the skill root and keeping references only one level deep from `SKILL.md`.

For validation, it recommends the `skills-ref` library and the command `skills-ref validate ./my-skill`. Validation checks naming and frontmatter conformance, making the format suitable for [[concepts/path-based-skill-validation]] and [[concepts/generated-artifact-validation]].

## Why it matters

This specification gives skills a shared, machine-checkable structure that supports portability, validation, and incremental loading. It is a foundation for skills that can be adopted across repositories and agent runtimes without rewriting the core instruction model.

## Related source

- [[summaries/agent-skills-spec]]