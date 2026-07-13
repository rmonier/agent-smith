---
type: "Summary"
description: "Inventory of tracked repository files for OpenKB ingestion and governance."
doc_type: short
full_text: "sources/repo-snapshot.md"
---

# Repository Snapshot

This document inventories the git-tracked files in the repository as a source pack for OpenKB ingestion. It is mainly a structural reference: it shows what content exists, how the repository is organized, and which skill/reference assets are currently present.

## What it contains

- Core repository governance files such as `README.md`, `AGENTS.md`, `LICENSE`, `NOTICE`, `LICENSING.md`, `REUSE.toml`, and `THIRD_PARTY_NOTICES.md`
- Repository config and ignore files such as `.gitattributes`, `.gitignore`, and `.graphifyignore`
- Citation and licensing metadata in `CITATION.cff` and multiple license texts under `LICENSES/`
- Documentation assets under `docs/`
- A set of agent skill packages under `.agents/skills/`, including:
  - `agent-ready-context`
  - `graphify`
  - `openkb`
  - `skill-creator`
  - `subagent-profile-adapter`

## Notable patterns

- The repository is organized around reusable agent skills and supporting references, not just application code.
- Several skill packages include their own `SKILL.md`, reference docs, scripts, assets, and licensing files, suggesting a modular, self-contained packaging approach.
- The presence of `openkb` skill materials alongside wiki-schema references indicates the repo is meant to support knowledge base compilation and [[concepts/repository-ingestion]] workflows.
- Licensing is treated as a first-class concern, with multiple bundled license texts and explicit third-party notice files, pointing to a strong [[concepts/licensing-and-attribution]] emphasis.

## Cross-document themes

- agent skills: The repository contains multiple skill definitions and helper scripts for authoring, validating, and adapting skills.
- repository governance: Standard metadata, notices, and policy files show a managed repository structure.
- documentation workflows: The references and scripts imply repeatable processes for bootstrap, validation, merging, pruning, and editorial passes.
- [[concepts/licensing-and-attribution]]: The bundle includes canonical licenses and attribution files for distributed content.
- wiki schema: The `openkb` references connect repository content to the wiki compilation format used by OpenKB.

## Findings

- This snapshot is not a narrative document; its value is in establishing the repository's file surface for downstream compilation and indexing.
- The tracked files suggest the repo is designed to support both human-maintained documentation and automated agent tooling.
- The `.agents/skills/` tree appears to be the main functional center of the repository.

## Why it matters

A file inventory like this helps OpenKB decide what to ingest, what to summarize, and where to build entity or concept pages. It also provides a stable baseline for change detection when the repository evolves.

## Related Concepts
- [[concepts/repository-inventory]]
- [[concepts/repository-structure-overview]]
- [[concepts/agent-tooling-ecosystem]]
- [[concepts/source-bundling]]
- [[concepts/source-source]]
- [[concepts/agent-ready-context]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/repository-orientation-indexing]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/main-structural-patterns]]
- [[concepts/compiled-knowledge-bases]]

## Entities
- [[entities/repo-snapshot]]
- [[entities/agents-skills]]
- [[entities/openkb]]
- [[entities/agent-ready-context]]
- [[entities/skill-creator]]
- [[entities/graphify]]
- [[entities/openkb-wiki]]
- [[entities/openkb-cli]]
- [[entities/okf-spec]]
- [[entities/wiki-schema-md]]
- [[entities/third-party-notices-md]]
- [[entities/license-compliance-requirements]]
- [[entities/agents-md]]
