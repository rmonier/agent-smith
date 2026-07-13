---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/repo-snapshot.md"]
description: "The repository's reusable agent skills, scripts, and conventions."
---

# Agent Tooling Ecosystem

The agent tooling ecosystem is the collection of skills, scripts, templates, references, and repository conventions that support agent-driven work in this repository. It combines reusable skill bundles with validation helpers, documentation structure, and Git hygiene so agents can operate consistently across ingestion, transformation, and maintenance tasks.

## What It Includes

- Skill packages under `.agents/skills/`, each centered on a `SKILL.md` file and usually backed by references, scripts, and assets.
- Repository-level conventions that shape how tools interact with tracked files, generated outputs, and documentation boundaries.
- Validation and build helpers that turn source material into structured OpenKB-compatible outputs.
- Supporting assets and templates that standardize setup, configuration, and generated artifacts.
- Repository inventory and summary artifacts such as `repo-snapshot`, which make the tracked file surface visible for ingestion and orientation.

## Main Skill Areas

The repository snapshot shows several distinct but related skill clusters:

- `agent-ready-context` focuses on preparing OpenKB-ready source packs, bootstrap material, and validation workflows.
- `graphify` supports graph extraction, updates, exports, and query-oriented operations.
- `openkb` provides the wiki schema and command references for working with the knowledge base.
- `skill-creator` helps create, validate, and adopt reusable skills.
- `subagent-profile-adapter` manages runtime detection, profile alignment, and tooling-context policy.

These skills form a shared ecosystem rather than isolated utilities: they reuse similar patterns for references, scripts, assets, and validation, and they help enforce consistent behavior across the repository.

## Structural Patterns

The snapshot also reveals a repeated internal structure across the skills:

- A root `SKILL.md` file defines the skill's purpose and usage.
- `references/` contains guidance, policies, and workflow notes.
- `scripts/` contains executable helpers for setup, validation, or transformation.
- `assets/` contains templates and example files used by the skill.

That repeated layout is a form of [[concepts/skill-structure-conventions]] and supports [[concepts/documentation-architecture]] by keeping skill-specific knowledge easy to find and reuse.

## Repository-Level Support

Several tracked files reinforce the ecosystem:

- `.gitattributes`, `.gitignore`, and `.graphifyignore` define how the repository handles tracked content and ignored paths.
- `AGENTS.md` and `README.md` provide top-level orientation for agent use and repository navigation.
- `LICENSE`, `NOTICE`, `LICENSING.md`, and `THIRD_PARTY_NOTICES.md` show that licensing and attribution are treated as core repository concerns.
- `CITATION.cff` adds citation metadata, while `REUSE.toml` and the `LICENSES/` directory support repeatable compliance handling.
- `docs/assets/agent-smith.svg` shows that the repository also maintains visual and explanatory material.

The repository snapshot itself is a useful inventory for understanding this tooling surface, and it supports [[concepts/repository-inventory]] by cataloging the tracked files that make the ecosystem visible.

Together, these pieces support [[concepts/agent-ready-repositories]] by making the repo easier for agents to ingest, inspect, and operate within.

## Why It Matters

This ecosystem reduces ad hoc agent behavior and makes tooling more predictable. It provides:

- reusable patterns for building and validating agent workflows,
- clearer boundaries between source material, generated content, and operational scripts,
- stronger support for [[concepts/deterministic-validation]] and [[concepts/deterministic-builds]],
- a better foundation for [[concepts/tooling-context-governance]] and repository-wide consistency,
- explicit licensing and attribution surfaces that help preserve safe reuse across generated and sourced material.

In practice, the tooling ecosystem is what lets the repository function as a coordinated environment for OpenKB ingestion, skill maintenance, and agent-assisted documentation work.

## Related Pages

- [[concepts/agent-ready-context-skill]]
- [[concepts/skill-governance]]
- [[concepts/generated-content-governance]]
- [[concepts/repo-ingestion-pipelines]]
- [[concepts/repository-inventory]]

## Related Documents
- [[summaries/repo-snapshot]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
