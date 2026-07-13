---
type: "Summary"
description: "Guidance for declaring skill dependencies without a non-standard field."
doc_type: short
full_text: "sources/agents__skills__skill-creator__references__dependencies-md.md"
---

# Summary

This document defines how skill authors should represent dependencies for portable Agent Skills without adding a custom `dependencies` field to `SKILL.md`. It frames dependency handling as a responsibility of the skill manager or explicit project scripts, while the skill itself records only portable metadata and human-readable guidance.

## Key Points

- The portable skill contract is limited to `SKILL.md` frontmatter plus optional `scripts/`, `references/`, and `assets/` directories.
- Dependency resolution, lockfiles, and installation state should not live in the skill frontmatter.
- Runtime and environment requirements belong in `compatibility`, kept under 500 characters.
- Non-portable local hints should use namespaced `metadata.*` keys with string values only.
- Detailed dependency instructions belong in `references/dependencies.md`.
- If a skill depends on local CLIs, credentials, network access, or companion skills, it should include `scripts/check_prereqs.py`.
- `allowed-tools` is treated as a permission hint, not an installer declaration, and should remain narrowly scoped.
- Python tooling should use PEP 723 inline metadata and be documented as `uv run <script>`, with bare `python3` only as a fallback.

## Metadata Vocabulary

The document standardizes several dependency-related metadata keys so different skills can describe relationships in a consistent way:

- `<skill-name>.companion-skills` for useful sibling skills that are not hard requirements.
- `<skill-name>.companion-skill-roles` for role descriptions that explain how companion skills fit together.
- `<skill-name>.provides` for reusable capabilities offered to other skills.
- `<skill-name>.vendor-skills` for third-party skills delegated to when installed.
- `<skill-name>.prereq-check` for the prerequisite checker path.
- `<skill-name>.prereq-guidance` for the dependency reference path.

## Third-Party Tooling Rules

When a skill requires installable tooling, the document requires explicit package and registry identification, pinned versions, consent-first installation, and integrity tracking for the first install. It also requires the skill to explain how it degrades gracefully when the tool is unavailable.

## Skill Relationships

The document prefers the term companion skill for helpful but optional dependencies between skills. It distinguishes these from vendor skills, which should remain immutable in the repository and be adapted through custom companion skills rather than direct patching.

## Main Takeaway

Overall, the file establishes a portable, explicit, and user-consent-first model for skill dependencies that avoids hidden installation behavior and keeps reproducibility concerns with the skill manager, not the skill definition itself.

## Related Concepts
- [[concepts/portable-skill-contract]]
- [[concepts/skill-dependency-declaration]]
- [[concepts/consent-first-installation]]
- [[concepts/skill-based-automation]]
- [[concepts/skill-action-boundary]]

## Entities
- [[entities/skill-creator]]
- [[entities/skill-creator-references-dependencies-md]]
- [[entities/uv]]
- [[entities/agents-skills]]
- [[entities/openai-system-skill-creator]]
- [[entities/tooling]]
- [[entities/agents-md]]
- [[entities/check_prereqs-py]]
- [[entities/references-tooling-context-policy-md]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/python]]
