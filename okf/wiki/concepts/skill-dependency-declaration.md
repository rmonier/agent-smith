---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md"]
description: "Rules for declaring skill dependencies without a custom SKILL.md field."
---

# Skill Dependency Declaration

Skill dependency declaration is the practice of describing what a skill needs without adding a non-standard `dependencies` field to `SKILL.md`. In this model, the skill definition stays portable, while dependency resolution, installation state, and lockfiles remain the job of the skill manager or explicit project scripts. See [[summaries/agents__skills__skill-creator__references__dependencies-md]] for the source guidance.

## Core Idea

The central rule is separation of concerns:

- `SKILL.md` should remain within the portable Agent Skills contract.
- Dependency behavior should be documented, not embedded as custom frontmatter.
- Runtime checks and installation logic should live in scripts or external tooling, not in ad hoc metadata.

This approach supports [[concepts/portable-skill-contract]], [[concepts/skill-governance]], and [[concepts/documentation-layer-separation]].

## What Belongs Where

The document recommends these locations for dependency-related information:

- `compatibility` for runtime and environment requirements, kept concise.
- Namespaced `metadata.*` keys for local, non-portable hints.
- `references/dependencies.md` for detailed dependency guidance.
- `scripts/check_prereqs.py` for validating local requirements such as CLIs, credentials, or network access.

This keeps dependency declarations explicit while preserving [[concepts/configuration-precedence]] and [[concepts/managed-document-sections]].

## Metadata Patterns

The source defines a small vocabulary for dependency-related metadata keys:

- `<skill-name>.companion-skills` for useful sibling skills.
- `<skill-name>.companion-skill-roles` for role descriptions.
- `<skill-name>.provides` for reusable capabilities.
- `<skill-name>.vendor-skills` for third-party skills used when installed.
- `<skill-name>.prereq-check` for the prerequisite checker path.
- `<skill-name>.prereq-guidance` for the dependency reference path.

These namespaced keys are a way to express relationships without turning them into hard requirements, aligning with [[concepts/skill-dependency-declaration]], [[concepts/skill-vendoring]], and companion skill-style coordination.

## Third-Party Tooling Rules

When a skill relies on installable tooling, the document requires:

- naming the exact package, registry, and upstream source repository;
- pinning versions in install instructions;
- asking the user before installing;
- using user-scoped installers such as `uv tool install` rather than `sudo`;
- recording integrity information on first install;
- explaining graceful degradation when the tool is absent.

These rules connect strongly to [[concepts/consent-first-installation]], [[concepts/integrity-pinning]], [[concepts/provenance-aware-tool-installation]], and [[concepts/graceful-degradation]].

## Relationship to Skills and Vendors

The document distinguishes between optional companion skills and vendor skills:

- companion skills are useful but not mandatory;
- vendor skills are external, installed artifacts that should remain immutable in the repository;
- if a vendor skill needs adaptation, the recommended path is a custom companion skill under `.agents/skills/`.

This supports [[concepts/vendor-skills]], [[concepts/vendor-skill-adoption]], and [[concepts/skill-vendoring]].

## Why It Matters

This concept helps skills remain:

- portable across environments;
- clearer for future agents to reason about;
- safer by avoiding hidden install behavior;
- easier to validate through prerequisite checks;
- more consistent with the broader OpenKB and Agent Skills documentation model.

In practice, skill dependency declaration is less about listing everything a skill might use and more about making requirement boundaries visible, consent-first, and reproducible.

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]