---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Ordered pipeline for staging, validating, and ingesting repository knowledge."
---

# Repository Ingestion Pipelines

Repository ingestion pipelines are ordered workflows that turn repository files and optional external evidence into a compiled knowledge base. They prioritize deterministic staging, provenance, validation, and controlled regeneration over direct manual editing.

## What the pipeline does

A repository ingestion pipeline typically:

- discovers repository structure and reads an index-first view of the knowledge base
- checks prerequisites and tool availability before any build steps
- stages source files into a deterministic input pack
- optionally enriches the run with external evidence
- initializes or updates the knowledge base with the staged material
- validates the compiled result and reviews generated pages for quality issues
- reconciles deletions, moved files, and stale findings before or during ingestion

In the referenced workflow, this pipeline is the backbone of the OpenKB build process described in [[summaries/agents__skills__agent-ready-context__references__workflow-md]].

## Core properties

- **Deterministic staging** - the source pack is built in a repeatable way so unchanged inputs produce unchanged staged files.
- **Provenance tracking** - every ingested item should remain traceable back to a repository source or explicit external evidence.
- **Validation gates** - linting and bundle validation check the compiled wiki for structural and linking issues.
- **Incremental maintenance** - changed sources, orphaned pages, and stale findings are handled through targeted refresh steps rather than full rebuilds.
- **Consent-first tooling** - optional tools and bootstrap actions are offered conservatively, with degraded paths available when needed.

## Workflow shape

The workflow in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] emphasizes a specific order:

1. Inspect the wiki index and tooling context first.
2. Check environment prerequisites.
3. Ensure vendored toolchain skills are present.
4. Normalize repo metadata and ignore rules.
5. Run graph analysis when available.
6. Build the source pack from repository content.
7. Initialize the knowledge base.
8. Ingest staged sources.
9. Validate the result.
10. Review generated output and reconcile drift.

That ordering matters because later steps assume earlier structural decisions are already locked in. This is closely related to [[concepts/deterministic-builds]], [[concepts/source-pack-staging]], and [[concepts/idempotent-graph-import]].

## Key safeguards

Repository ingestion pipelines need guardrails to avoid producing misleading or unstable knowledge:

- **No self-referential graph loops** - the wiki root must stay out of the repo graph, or generated knowledge feeds back into its own source set.
- **No hidden memory** - external documentation can support the run, but it should be treated as evidence rather than instruction.
- **No silent normalization changes** - line endings and Git attribute policy must be explicit so hashes remain stable.
- **No stale pages from deleted sources** - removals and renames should be reconciled before ingest to prevent orphaned compiled content.
- **No hand-editing generated pages** - corrections should flow through source fixes and re-ingestion.

These safeguards connect to [[concepts/self-reference-control]], [[concepts/orphan-retraction]], [[concepts/document-normalization]], [[concepts/provenance-tracking]], and [[concepts/generated-content-governance]].

## Why it matters

A good repository ingestion pipeline turns a codebase into a reliable knowledge base without losing trust in the output. It keeps the compiled wiki grounded in source files, supports incremental maintenance, and makes the build process auditable and repeatable.

It is also the mechanism that separates raw repository structure from curated knowledge, which is a central idea in [[concepts/knowledge-layer-separation]] and [[concepts/repository-ingestion]].

## Related ideas

- [[concepts/source-bundling]]
- [[concepts/source-driven-regeneration]]
- [[concepts/repository-transformation-pipelines]]
- [[concepts/okf-bundle-validation]]
- [[concepts/wiki-review-gates]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/manifest-authoritative-reconciliation]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]