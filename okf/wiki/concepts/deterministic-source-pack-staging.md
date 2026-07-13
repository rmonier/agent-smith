---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Stable staging of repository sources into reproducible OpenKB input packs."
---

# Deterministic Source Pack Staging

Deterministic source pack staging is the practice of converting a Git repository into an OpenKB-compatible input pack in a way that is stable, reproducible, and safe to re-run. The staged output should be identical whenever the underlying repository content is unchanged, so OpenKB can rely on deterministic builds, content hashing, and manifest authoritative reconciliation instead of timestamp noise or ad hoc file selection.

This concept is central to [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], which builds the repository source pack used for ingestion, and it sits inside the broader agent-ready workflow that keeps `okf/wiki/` as the durable context source of truth while staging evidence separately under `okf/.okf-build/input/`.

## Core idea

A source pack is not a raw mirror of the repository. It is a curated, normalized staging layer that:

- selects only relevant tracked files,
- normalizes their text representation,
- preserves provenance metadata,
- splits oversized sources instead of truncating them,
- records the staged inventory in a manifest,
- avoids feedback loops from generated artifacts,
- keeps generated content out of `okf/raw/` and `okf/wiki/` during staging.

That makes the pack suitable for downstream ingestion while minimizing accidental churn and preserving the boundary between repository evidence and compiled knowledge.

## Key properties

- **Deterministic selection**: files are discovered from `git ls-files` and filtered with explicit skip/select rules.
- **Normalized bytes**: line endings are normalized before hashing so the same content hashes the same across platforms.
- **Stable provenance**: each staged file records the last Git commit that touched it, not the current `HEAD`.
- **No silent loss**: oversized markdown or code is split into parts rather than cropped when splitting is enabled.
- **Manifest-backed**: the staged pack is accompanied by a JSON manifest that enumerates each staged item.
- **Loop avoidance**: generated graph reports are only staged when they do not appear to reference the compiled KB itself.
- **KB-root isolation**: the KB root `okf/` is treated as OpenKB-owned, but the source pack is staged into `okf/.okf-build/input/` instead of being written directly into compiled areas.

## How the staging pipeline works

The script behind this concept performs a few distinct steps:

1. **Build a repository inventory** from tracked files.
2. **Emit a repo snapshot** document listing the included files.
3. **Optionally stage graph analysis output** after removing date churn and checking for self-reference.
4. **Stage selected source files** as markdown wrappers with frontmatter metadata.
5. **Bundle or split content** when files are too large for a single staged document.
6. **Write a manifest** for downstream reconciliation and orphan detection.
7. **Keep the staging output deterministic** so repeated runs on unchanged input do not produce noise.

These steps reflect source pack staging as a controlled transformation pipeline rather than a blind export.

## Important implementation patterns

- **Git as authority**: repository membership and file provenance come from Git, supporting [[concepts/git-tracking-policy]] and [[concepts/source-provenance]].
- **Hash-based identity**: staged documents use SHA-256 of normalized text, which supports [[concepts/hash-registry-coherence]].
- **Frontmatter metadata**: staged files carry structured metadata like `source_path`, `source_kind`, and `source_commit`, aligning with [[concepts/frontmatter-metadata]].
- **Selective inclusion**: the script has path-based heuristics to focus on repo documentation, build files, source code, and skill assets.
- **Partitioning over truncation**: large files are split into parts using layout-aware boundaries, which reflects [[concepts/source-partitioning]] and [[concepts/knowledge-capture-boundaries]].
- **Bundling for scale**: in bundle mode, related non-markdown files can be grouped by directory depth, connecting to [[concepts/source-bundling]].
- **Artifact hygiene**: the staging pipeline is designed to avoid polluting the repository with generated KB output or local OpenKB state.

## Why it matters

Deterministic staging reduces the cost and risk of ingestion. If the staged pack changes only when the repository changes, then OpenKB can use it as a reliable input to [[concepts/repository-ingestion]], [[concepts/source-driven-regeneration]], and compiled knowledge maintenance.

It also supports safer automation because operators can reason about the exact effect of a staging run. That matters for [[concepts/safe-automation]], [[concepts/quality-gates]], and [[concepts/evidence-staging]].

In the agent-ready workflow, deterministic staging is part of the broader separation between skills, context, and orientation: skills execute actions, the wiki stores durable knowledge, and the source pack provides the controlled evidence feed into compilation.

## Risks it addresses

- **Hash churn** from timestamps, commit heads, or other run-dependent fields.
- **Content loss** from cropping oversized files.
- **Self-referential loops** when generated reports describe the KB that will ingest them.
- **Orphan drift** when the pack no longer contains a file previously represented in the KB.
- **Ambiguous provenance** when staged output does not preserve source commit and source path.
- **Context confusion** when generated KB output is mixed into the source-staging layer instead of remaining staged input.

## Related ideas

- document normalization
- line ending normalization
- deterministic validation
- source provenance
- staging manifests
- repository inventory
- self reference control
- self referential ingestion loops
- orphan retraction
- source pack manifest

## Practical takeaway

A deterministic source pack is the bridge between a live repository and a stable knowledge-ingestion input. The pack should be reproducible, provenance-rich, and free of avoidable noise so downstream KB compilation stays predictable and auditable.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/repo-snapshot]]