---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/repo-snapshot.md"]
description: "A tracked-file inventory used to orient repository ingestion and staging."
---

# Repository Inventory

Repository inventory is the practice of listing a repository's tracked files so the wiki can understand what content exists, how it is organized, and which areas are likely to matter for ingestion and maintenance. In this wiki, the inventory is also an input to deterministic source-pack staging, where the file list becomes part of the staged knowledge trail rather than a one-off inspection artifact.

## What it captures

A repository inventory records the current tracked-file set, usually from version control, and turns it into a structured view of the repository's scope. In `repo-snapshot`, the inventory includes:

- Top-level project files such as `README.md`, `AGENTS.md`, `.gitignore`, `.gitattributes`, `LICENSE`, `NOTICE`, `LICENSING.md`, `REUSE.toml`, and `THIRD_PARTY_NOTICES.md`
- Repository policy and metadata files such as `CITATION.cff`, `.graphifyignore`, and bundled license texts under `LICENSES/`
- OpenKB and agent skill assets under `.agents/skills/`
- Supporting scripts, references, templates, and validation assets for skill lifecycle workflows
- Repository-specific assets such as `docs/assets/agent-smith.svg`
- The staged inventory itself as a generated `repo-snapshot.md` document with stable hash-based provenance

## Why it matters

- It provides a stable entry point for repository ingestion and related source-pack workflows.
- It helps distinguish core documentation, tooling, generated assets, policy files, and configuration files.
- It supports repository structure overview work by showing how the repository is organized in practice.
- It enables later wiki pages to connect specific files and skill packages to broader skill authoring and tooling governance concerns.
- It anchors deterministic source-pack staging by defining the tracked-file universe before files are normalized, hashed, and staged.
- It helps maintain manifest authoritative reconciliation because the manifest can be compared back to the repository inventory when files move, disappear, or are deselected.

## Observed patterns in the snapshot

The snapshot suggests a repository centered on agent-oriented knowledge work rather than application runtime code.

- The `.agents/skills/` tree is the dominant structure, with multiple skill packages and their accompanying references, scripts, and assets.
- Several files support validation and packaging behavior, pointing to a disciplined workflow around deterministic validation and source-pack staging.
- The source-pack builder records normalized text, stable SHA-256 hashes, and the last commit that touched each file, which makes the inventory useful as a provenance map rather than just a directory listing.
- The builder deliberately excludes transient paths such as caches and build outputs, so the inventory reflects intentional repository content instead of noise.
- Configuration files at the root indicate repository-level policy and tracking rules, which relate to git tracking policy and local ignore behavior.
- The inventory is broad enough to support future entity pages for specific skills, scripts, or templates if they recur across sources.

## Relationship to the wiki

A repository inventory is not just a list of paths; it is a source for mapping a repository into the knowledge base. It can seed pages for the repository itself, important skills, and reusable tooling patterns, while also reinforcing boundaries between source material and compiled knowledge.

The `repo-snapshot` source document is the concrete example for this concept and should be consulted alongside [[summaries/repo-snapshot]] when reasoning about the repository's structure and content. The source-pack builder that produces this snapshot also emits a manifest and staged source files, tying inventory directly to [[concepts/source-pack-manifest]] and [[concepts/source-pack-staging]].

## Practical implications

- The inventory is only as stable as the repository's tracked-file set, so changes to Git tracking policy directly affect what the wiki sees.
- A clean inventory makes it easier to detect rename-versus-delete cases and decide whether orphaned KB pages should be retracted.
- Because the pack builder stages both the inventory and the selected sources, the inventory functions as a lightweight index of what was included in a given ingestion run.
- The same inventory logic can later support repo-oriented discovery pages, validation checks, and reconciliation workflows without rereading the entire repository from scratch.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]