---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/repo-snapshot.md"]
description: "How this repo is organized across skills, docs, configs, and inventories."
---

# Repository Structure Overview

Repository Structure Overview describes how this codebase is laid out across reusable agent skills, supporting references, scripts, assets, top-level governance files, and tracked inventory artifacts. The `repo-snapshot` source makes the repository's structure visible as a whole by listing every git-tracked file that matters to OpenKB ingestion.

## What the structure shows

- The repository centers on several skill collections under `.agents/skills/`, rather than a single application codebase.
- Each skill area is organized into a `SKILL.md` entry plus supporting `references/`, `scripts/`, and sometimes `assets/`.
- Repository-level policy files like `.gitattributes`, `.gitignore`, `.graphifyignore`, and `REUSE.toml` are tracked alongside docs.
- Top-level files such as `AGENTS.md`, `README.md`, `LICENSE`, `NOTICE`, `LICENSING.md`, `CITATION.cff`, and `THIRD_PARTY_NOTICES.md` sit beside the skill infrastructure.
- A visual asset exists at `docs/assets/agent-smith.svg`, showing that the repository also carries media used by its documentation ecosystem.
- The tracked inventory includes both source-pack metadata and the compiled wiki surface, which helps distinguish source material from generated knowledge.

## Major structural zones

- `agent-ready-context`: bootstrap, validation, pruning, and bundle-building support for OKF-oriented context preparation
- `graphify`: graph-oriented skill docs and workflows for export, query, transcribe, update, and related operations
- `openkb`: core OpenKB commands and wiki-schema references
- `skill-creator`: templates, validation helpers, dependency references, and skill adoption tooling
- `subagent-profile-adapter`: runtime detection, profile authoring, and tooling-context policy enforcement

## Key patterns

- The repository uses [[concepts/skill-structure-conventions]] to organize each skill as a self-contained package of guidance and executable support.
- The file layout reflects [[concepts/documentation-architecture]]: primary instructions in `SKILL.md`, deeper context in `references/`, and utility code in `scripts/`.
- The tracked inventory supports [[concepts/repository-inventory]] by making the current contents explicit and machine-readable.
- The presence of ignore, attribute, and licensing files indicates [[concepts/tooling-boundaries]] and repository-specific file handling rules.
- The repository combines source-pack manifests with the compiled wiki surface, aligning with [[concepts/repository-ingestion]] and [[concepts/compiled-knowledge-bases]].
- The overall layout is consistent with repository orientation use cases where navigation, onboarding, and ingestion depend on a clear map of the repo.

## Why it matters

- It helps humans and agents understand where to look for policy, workflow, implementation, and licensing details.
- It supports repository ingestion and wiki compilation by identifying stable file clusters and governance files.
- It reduces ambiguity when distinguishing core skills, reference material, generated wiki content, and support artifacts.
- It provides a baseline for future changes to be compared against, especially when files are added, removed, or reorganized.

## Related knowledge

- [[concepts/repository-inventory]] for the broader practice of tracking repository contents
- [[concepts/repository-ingestion]] for turning repo content into compiled knowledge
- [[concepts/documentation-architecture]] for how documentation layers are arranged
- [[concepts/skill-authoring]] for the skill-centered structure used throughout the repo
- [[concepts/tooling-boundaries]] for how repository files govern local and shared tooling behavior
- [[summaries/repo-snapshot]] for the underlying tracked-file inventory that informed this concept

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]