---
type: "Summary"
description: "Source note tracing skill-creator lineage and its OpenKB-specific adaptations."
doc_type: short
full_text: "sources/agents__skills__skill-creator__references__source-attribution-md.md"
---

# Summary

This document explains the provenance of the `skill-creator` skill and clarifies that it is an adaptation assembled from multiple upstream patterns rather than a novel design. It records verified lineage, highlights what this repository-specific version adds, and sets rules for how generated skills should be structured and scoped.

## Main points

- The primary upstream influence is Anthropic's `skill-creator`, especially its [[concepts/progressive-disclosure]] structure, split between `scripts/`, `references/`, and `assets/`, trigger-focused descriptions, and guidance to explain importance instead of relying on rigid MUST-style rules.
- A second major influence is `superpowers` `writing-skills`, which contributes a [[concepts/baseline-first-testing]] approach: test the task without the skill first, capture exact failures, then design the skill to address those gaps. It also reinforces token-budget discipline and warns against narrative examples, generic names, and batch skill creation.
- A third influence is OpenAI's system `skill-creator`, which contributes a lean workflow shape of understand -> plan -> initialize -> edit -> validate -> iterate, along with script patterns such as `init_skill.py` and `quick_validate.py`, the principle that the context window efficiency matters, and the rule against auxiliary files like README or CHANGELOG inside a skill.
- The document distinguishes OpenKB Skill Factory as related integration rather than direct lineage. Its role is an optional downstream packaging and validation path for generated skills before any adoption into `.agents/skills/`.

## What this adaptation adds

This adaptation exists to fit a vendor-neutral repository workflow and OpenKB-specific constraints:

- It uses a vendor-neutral `.agents/skills/` layout aligned with the agentskills.io-style model rather than product-specific directories.
- It introduces the OpenKB boundary between action, context, and orientation. Skills should remain action-oriented, while durable knowledge belongs in `okf/wiki/` and high-level orientation belongs in `AGENTS.md`.
- It adds a hardening model around dependency and execution safety, including consent-first version-pinned installs, integrity recording, registry-agnostic commands, secret hygiene, minimal scoped `allowed-tools`, and gitignored artifacts.
- It enforces vendor skill immutability and a lockfile policy.
- It prefers `uv`-first script execution with PEP 723 inline metadata.

## Adaptation rules

The document defines repository rules for skill creation:

- Write project skills only under `.agents/skills/`.
- Keep skills focused on actions rather than general knowledge.
- Store reusable context in `okf/wiki/`.
- Keep `AGENTS.md` limited to orientation.
- Validate required frontmatter and folder naming before handoff.
- Do not copy runtime-specific metadata, product-specific folders, or personal agent configuration into the repository.

## Key ideas for linking

- [[concepts/progressive-disclosure]]
- [[concepts/baseline-first-testing]]
- context window efficiency
- action vs context boundary
- vendor skill immutability
- skill hardening

## Takeaway

The document serves as a source-attribution and design-rationale note: it documents the inherited patterns behind `skill-creator`, explains the repository-specific constraints added by OpenKB, and defines the boundaries that keep skills small, actionable, and separate from longer-lived knowledge or agent orientation.

## Related Concepts
- [[concepts/context-action-separation]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/skill-based-automation]]
- [[concepts/documentation-architecture]]
- [[concepts/dependency-management]]
- [[concepts/integrity-pinning]]
- [[concepts/supply-chain-security]]
- [[concepts/tool-boundaries]]
- [[concepts/agent-context-layering]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/quality-gates]]

## Entities
- [[entities/openai-system-skill-creator]]
- [[entities/superpowers-writing-skills]]
- [[entities/anthropic]]
- [[entities/uv]]
- [[entities/agents-md]]
