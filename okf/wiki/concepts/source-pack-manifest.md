---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "The authoritative JSON inventory of staged inputs used for OpenKB reconciliation."
---

# Source Pack Manifest

A source pack manifest is the authoritative JSON inventory of staged inputs produced for OpenKB ingestion. It records what was staged, where it was written, how it was classified, and which source content each staged item came from, so downstream tools can reconcile the KB against the repository without re-deriving staging rules.

## Purpose

The manifest supports [[concepts/deterministic-source-pack-staging]] and [[concepts/manifest-authoritative-reconciliation]] by making the staging result machine-readable and reproducible. Instead of relying on directory contents alone, downstream tooling can compare the manifest against the repository and decide what should be ingested, re-ingested, or retired.

It is especially important for orphan cleanup: the prune workflow uses the freshly built manifest as authority when it is present, and falls back to git-derived expectations only when the manifest is missing. That keeps deletion reconciliation aligned with the builder and reduces the risk of drifting selection or slug rules.

## What it contains

In the staging script described in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], the manifest is written as JSON and includes entries with fields such as:

- `source_path` - the original repository path or synthetic source label
- `staged_path` - the generated Markdown file path under the staging output
- `source_hash` - a SHA-256 digest of the normalized staged content
- `source_kind` - the content class, such as `text`, `markdown`, `code`, or `bundle`
- `origin` - whether the item came from the repository, graphify output, or a repo bundle
- `part` - present for oversized sources that were split into multiple staged parts
- `member_count` - present for bundled outputs

The orphan-pruning script also reads the manifest to recover the expected staged names and, when available, a mapping from staged content hashes back to source paths. That lets it distinguish true deletions from renames or moves when the same content reappears under a new path.

## Role in the pipeline

The manifest is created after the script stages repository inventory, optional graph reports, normal selected files, split parts for oversized sources, and directory bundles. It is then sorted and written deterministically so repeated runs against the same inputs produce the same manifest bytes.

This makes the manifest central to:

- [[concepts/provenance-tracking]]: each entry ties staged output back to a source path and hash
- [[concepts/source-provenance]]: provenance is embedded at the item level, not inferred later
- [[concepts/deterministic-builds]]: manifest ordering and hashing are stable across runs
- [[concepts/source-partitioning]]: split documents retain per-part manifest records
- [[concepts/source-bundling]]: bundled directories are represented as a single manifest entry per bundle
- [[concepts/rename-vs-delete-detection]]: content hashes help separate a move from a true deletion
- [[concepts/orphan-retraction]]: stale KB documents can be retracted when the manifest no longer supports them

## Why it matters

The manifest is the bridge between staging, validation, and cleanup. It tells OpenKB what was produced, which inputs were included, and how those outputs were derived. That matters because staging alone does not update the compiled wiki; it only prepares content for later ingestion and reconciliation.

It also helps detect drift. If repository files are deleted, moved, or deselected, the manifest no longer contains matching entries, which can be used to identify stale KB documents and guide orphan retraction workflows. The prune script treats that as a controlled destructive path: it reports orphans by default, can show OpenKB's own per-page removal plan with `--preview`, and only executes removal with `--apply` and explicit confirmation.

When a manifest is present, it is treated as authority. If the manifest-derived staged names disagree with what the current repository would stage, the pruning workflow emits an advisory that the pack may be stale or the builder and detector may have drifted, but it still proceeds with the manifest rather than silently re-deriving state.

## Related ideas

- [[concepts/source-pack-staging]] - the broader act of preparing a repository for ingestion
- [[concepts/repository-inventory]] - the snapshot view of tracked files that complements the manifest
- [[concepts/hash-registry-coherence]] - keeping staged hashes and registry state aligned
- [[concepts/orphan-retraction]] - removing KB documents no longer supported by source inputs
- [[concepts/openkb-build-workflow]] - the wider OpenKB build and ingestion flow
- [[concepts/deterministic-validation]] - using stable inputs to make reconciliation checks repeatable

## Practical takeaway

A source pack manifest is not just a log artifact; it is the reconciliation contract for the staged pack. If the staged files change, the manifest changes with them, and that stable mapping is what lets OpenKB ingest incrementally, detect renames safely, and retract orphans without guessing.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]


See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]