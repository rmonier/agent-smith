---
sources: ["summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md"]
type: "Work"
description: "Reference guidance for dependency handling in Agent Skills"
---

# .agents/skills/skill-creator/references/dependencies.md

A reference document for the [[entities/skill-creator|skill creator]] skill that explains how to represent dependencies in portable Agent Skills without adding a custom `dependencies` field to `SKILL.md`.

## What it covers

- The portable skill contract: `SKILL.md` frontmatter plus optional `scripts/`, `references/`, and `assets/` directories.
- Why dependency resolution, lockfiles, and installation state belong to the skill manager or explicit project scripts rather than the skill file itself.
- How to document runtime and environment requirements in `compatibility` and how to use namespaced `metadata.*` keys for local hints.
- When to add a `scripts/check_prereqs.py` prerequisite checker for skills that depend on local CLIs, credentials, network access, or companion skills.
- How to treat `allowed-tools` as a narrow permission hint instead of a dependency declaration.
- How Python scripts should be documented with PEP 723 metadata and run via `uv run` when possible.
- How the skill-creator itself frames dependency guidance as part of skill authoring, validation, and safe execution rather than as a knowledge-only note.

## Dependency vocabulary

The document defines a shared set of namespaced metadata keys for dependency-related relationships:

- `<skill-name>.companion-skills` for helpful sibling skills.
- `<skill-name>.companion-skill-roles` for role descriptions.
- `<skill-name>.provides` for reusable capabilities.
- `<skill-name>.vendor-skills` for third-party skills deferred to when installed.
- `<skill-name>.prereq-check` for the prerequisite checker path.
- `<skill-name>.prereq-guidance` for the dependency reference path.

## Tooling and governance rules

- Third-party tooling must be named precisely, pinned in documented install commands, and installed consent-first.
- Integrity should be recorded on first install, with mismatches treated as a supply-chain incident.
- The document requires a graceful fallback path when tooling is absent.
- Vendor skills should remain immutable in the repository; adaptation should happen through a custom companion skill instead.
- Skill creation and updates should stay aligned with [[concepts/skill-structure-conventions]], [[concepts/skill-validation-workflow]], and [[concepts/portable-skill-contract]] so dependency guidance remains concise and actionable.

## Related ideas

This work connects closely to [[concepts/portable-skill-contract]], [[concepts/dependency-management]], [[concepts/consent-first-installation]], [[concepts/integrity-pinning]], [[concepts/skill-dependency-declaration]], [[concepts/skill-vendoring]], [[concepts/skill-authoring]], and [[concepts/skill-governance]].

## Source

- Summary: [[summaries/agents__skills__skill-creator__references__dependencies-md]]

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]


See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]