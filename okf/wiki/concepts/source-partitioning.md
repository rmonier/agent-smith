---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Deterministic splitting of oversized sources into full-content parts or bundles."
---

# Source Partitioning

source partitioning is the practice of dividing repository content into smaller staged documents without discarding meaning. In the OpenKB ingestion pipeline, it is used to keep source packs deterministic, preserve full content, and avoid silent truncation when files or grouped inputs exceed practical size limits.

This concept is central to deterministic source pack staging and source pack staging, because the staging step must decide whether a source is emitted as a single document, split into parts, or grouped into bundles. The implementation in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] shows the main patterns.

## Why it exists

Source partitioning solves a basic tension in knowledge ingestion: repositories can contain large files, but compiled knowledge systems need bounded inputs. Cropping would lose content and create hidden gaps, so the pipeline prefers partitioning over truncation. That makes the resulting KB more trustworthy and keeps the staged bytes stable across runs.

It also supports source provenance and provenance tracking by keeping each partition tied to the original path, hash, and commit metadata.

## How it works in the source pack builder

The script partitions sources in two main ways:

- **Split oversized files**: If a markdown file exceeds `--max-lines`, it is split into multiple full-content parts at heading boundaries.
- **Split oversized code**: If code splitting is enabled, oversized code files are split at layout-based boundaries rather than cropped.
- **Bundle supporting files**: When `--bundle-depth` is used, non-markdown files can be grouped by directory segments into digest documents.

The partitioning logic is intentionally conservative:

- It never removes content from a selected source just to fit a line budget.
- It uses boundaries that are easy to reason about and deterministic to reproduce.
- It warns when a bundle is too large to remain in one piece and tries a deeper grouping first.

## Partition forms

### Split parts

For oversized individual files, the script emits one staged document per part. Each part gets:

- its own `source_hash`
- a `part` field like `2/5`
- the original `source_path`
- the original `source_commit`

This keeps partitions independently ingestible while preserving the link back to the source file.

### Bundles

For selected supporting files, the script can emit per-directory bundles. These are not filters; they are digest documents that still preserve all included content in grouped form. Bundle size is guarded by `--bundle-max-lines`, and the builder will deepen the grouping before warning that a bundle may be too large.

## Boundary rules

The source pack builder uses different boundary heuristics depending on source type:

- **Prose**: split at heading lines
- **Code**: split at top-level, column-zero boundaries after blank lines

This is a document normalization decision as much as a partitioning one: the goal is to keep parts legible and stable while avoiding syntax-heavy parsing.

## Related concerns

Source partitioning interacts with several other knowledge-base policies:

- knowledge capture boundaries — partitioning decides where capture must stop becoming one document and start becoming many.
- graceful degradation — large inputs are handled by splitting or bundling instead of failing hard.
- knowledge distillation risks — partitioning avoids losing source evidence, which reduces the risk of over-compressed summaries.
- single source of truth — each partition still points back to the original path and content-derived hash.
- source bundling — bundling is a sibling strategy to splitting, used for grouped support material.
- manifest authoritative reconciliation — the manifest records the partitioned outputs so later tooling can reconcile what was staged.

## Key takeaway

Source partitioning is a preservation-first technique: when a source is too large for a single staged document, the builder divides it into stable, content-complete pieces rather than truncating it. That keeps ingestion reproducible, keeps provenance attached, and makes the compiled knowledge safer to trust.
