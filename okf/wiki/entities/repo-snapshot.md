---
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/repo-snapshot.md"]
type: "Work"
description: "Repository file inventory snapshot for OpenKB ingestion"
---

# Repository Snapshot

Repository Snapshot is a tracked-file inventory for OpenKB ingestion. It records the git-tracked surface of the repository at a point in time so downstream tooling can reason about what is present, how the repository is organized, and which assets are available for compilation and validation.

## Key facts

- It is a source-pack style inventory document titled `Repository Snapshot`.
- It lists git-tracked files across repository governance, documentation, licensing, and agent skill packages.
- It includes core repository files such as `README.md`, `AGENTS.md`, `LICENSE`, `NOTICE`, `LICENSING.md`, `REUSE.toml`, and `THIRD_PARTY_NOTICES.md`.
- It includes configuration and ignore files such as `.gitattributes`, `.gitignore`, and `.graphifyignore`.
- It includes multiple skill directories under `.agents/skills/`, notably `agent-ready-context`, `graphify`, `openkb`, `skill-creator`, and `subagent-profile-adapter`.
- It includes bundled license texts under `LICENSES/` and documentation assets such as `docs/assets/agent-smith.svg`.

## What it represents

This entity is not application behavior or a narrative guide; it is a repository inventory artifact. Its primary role is to support [[concepts/repository-inventory]], [[concepts/repository-ingestion]], and [[concepts/source-pack-manifest]] workflows by providing a stable reference for what the repository contains.

## Notable patterns

- The repository appears to be centered on reusable agent skills and support scripts rather than a single codebase.
- The tracked files show strong emphasis on licensing compliance requirements and attribution, with multiple license texts and notice files.
- The presence of the `openkb` skill materials points to integration with [[concepts/knowledge-compilation-pipeline]] and wiki-oriented workflows.
- The file set suggests a modular structure where skills, references, scripts, and assets are packaged together for validation and reuse.

## Related pages

- [[summaries/repo-snapshot]] — summary of the source document that describes this inventory.
- [[entities/openkb]] — the OpenKB project context connected to the wiki and ingestion workflow.
- [[entities/agent-skills]] — the broader category of reusable skill packages reflected in the snapshot.
- [[concepts/repository-structure-overview]] — useful lens for interpreting the file layout.
- [[concepts/agent-tooling-ecosystem]] — captures the larger environment of skills, scripts, and tooling represented here.

## Why it matters

Repository Snapshot provides the evidence base for downstream knowledge extraction. By enumerating tracked files, it helps detect structural changes, identify candidate source material, and anchor compiled knowledge in the repository's actual contents.