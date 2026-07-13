---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Grouping repository files into staged bundles for ingestion and review."
---

# Source Bundling

Source bundling is the practice of grouping multiple repository files into a single staged document for ingestion instead of staging each file separately. In OpenKB source-pack staging, it changes the ingestion unit from individual files to directory-level digest documents while still preserving file-level provenance inside the bundle.

## Overview

Bundling is a staging strategy for repository material. Rather than emitting one staged page per selected file, the source-pack builder can aggregate files by directory prefix and write a bundle document containing multiple file sections. This makes bundling a structural choice within [[concepts/repository-ingestion]] and a practical companion to [[concepts/staging-manifests]] and [[concepts/source-provenance]].

In `.agents/skills/agent-ready-context/scripts/build_okf_source_pack.py`, bundling is enabled with `--bundle-depth`. A value greater than zero groups selected non-markdown files by the first N path segments and stages each group as a bundle document. A value of zero keeps the default one-file-per-document behavior.

The builder treats bundling as packaging, not filtering: selected files are still represented, but they are combined into fewer staged documents. That distinction matters for [[concepts/knowledge-boundaries]] and [[concepts/repository-ingestion]] because bundle mode changes the staging shape, not the source set.

The repository snapshot for this project shows why bundling is useful in practice: the tracked-file surface is broad, with repository governance files, multiple license texts, docs assets, and several self-contained skill trees under `.agents/skills/`. That mix of top-level policy files and clustered skill resources is a good fit for directory-level grouping, especially when the goal is to preserve local context without flattening the repository into unrelated one-file pages.

## How It Works

The source-pack builder first filters repository files through skip and selection heuristics. When bundling is enabled:

- files are grouped by a path prefix derived from the requested bundle depth
- each group becomes one staged Markdown page under the staged input tree
- each member file contributes a section containing its path, source hash, commit provenance, and content excerpt
- the bundle itself receives a single hash computed from the normalized contents of all included files
- the manifest records the staged bundle, its hash, origin, and member count

This design ties source bundling to [[concepts/document-normalization]], [[concepts/line-ending-normalization]], [[concepts/provenance-tracking]], and [[concepts/hash-registry-coherence]] because stable grouping depends on normalized text and preserved per-file metadata.

Markdown files are intentionally excluded from bundle mode in this implementation. Prose is treated as a primary concept source with its own identity, while bundles are reserved for supporting files that benefit from directory-level aggregation.

The implementation also keeps the bundle logic aligned with orphan cleanup by sharing the same path-selection assumptions as the repository pruning workflow. That means bundling is not just a write-time concern; it also affects later reconciliation in [[concepts/orphan-retraction]] and [[concepts/manifest-authoritative-reconciliation]].

## Why Use Source Bundling

Bundling is useful when the goal is to preserve repository context at a directory or subsystem level rather than at the level of isolated files. It can help present related files together, especially when they collectively describe one capability, workflow, or component.

Potential advantages include:

- reducing the number of staged documents produced during [[concepts/repository-ingestion]]
- keeping nearby files together for easier contextual reading
- emphasizing folder-level structure as a meaningful knowledge unit
- creating digest-style artifacts that are easier to review than many tiny pages
- making large repositories more practical to ingest without changing the underlying source set

Bundling also fits well with [[concepts/index-based-discovery]] because one bundle page can stand in for a coherent slice of a repository.

The tracked inventory in `repo-snapshot` suggests an additional practical benefit: bundling can keep each skill package's files grouped together while leaving top-level policy and license files visible as distinct units. In a repository with many reusable skill modules, that makes the output easier to browse as a map of subsystems instead of a long, flat file list.

## Tradeoffs and Cautions

The source-pack builder makes an important caution explicit: changing bundle depth re-stages content under new hashes, which causes the next add operation to re-ingest the pack. In other words, bundling is not just a display preference; it changes content identity in the staged corpus.

Key tradeoffs include:

- coarser granularity for updates, because one changed file can affect the bundle hash
- reduced per-file independence compared with one-file staging
- potential re-ingestion churn if grouping strategy changes after adoption
- possible tension with [[concepts/incremental-compilation]] if large bundles are used carelessly
- a stronger need for consistent staging decisions to avoid registry drift

For that reason, the lifecycle guidance recommends choosing a bundling mode before first ingestion and sticking with it. That aligns with [[concepts/deterministic-builds]] and [[concepts/hash-registry-coherence]]: stable grouping decisions help keep downstream identity stable.

The same lifecycle also notes that bundling is part of a larger reconciliation story. If the repository changes shape, stale staged documents may need explicit removal or recompilation rather than relying on a new `add` to clean them up. That makes bundling relevant to [[concepts/registry-drift]] and [[concepts/source-driven-regeneration]].

## Relationship to Determinism

Source bundling only works well when the bundle output is deterministic. In the referenced implementation, determinism is preserved by:

- reading tracked files from Git-controlled paths
- normalizing decoded text before hashing
- hashing normalized file contents in sorted order
- writing consistent staged Markdown output
- deriving provenance from last-touch commits instead of volatile `HEAD` state

These choices ensure that the same repository state produces the same bundle documents. That makes source bundling a concrete application of [[concepts/deterministic-builds]], [[concepts/evidence-staging]], and [[concepts/generated-content-governance]].

The builder also avoids embedding volatile repository state in the bundle identity. The staging process uses the source content, not the current HEAD commit, as the basis for identity so that unchanged content does not churn staged hashes unnecessarily.

## Relationship to Metadata and Manifests

A bundle page still carries strong metadata. The staged document includes bundle-level frontmatter such as source path, source kind, and source hash, while each file section preserves member-level hash and commit details. The manifest then records the staged bundle as a single item and includes `member_count`.

This layered metadata model connects source bundling to [[concepts/frontmatter-metadata]] and [[concepts/staging-manifests]]. It shows that aggregation does not require losing provenance, only changing the level at which primary ingestion occurs.

The script also produces a repository snapshot and, when safe, stages a graph report. Those additional outputs show that bundling sits inside a broader source-pack pipeline rather than standing alone. In that pipeline, bundle documents coexist with repository inventory, graph diagnostics, and oversized-file splitting under the same staging rules.

Because the staging pipeline also reports likely orphaned KB documents when source files disappear, bundling participates in broader repository reconciliation. Bundle metadata needs to stay aligned with the hash registry and downstream wiki pages so that staged inputs, raw copies, and compiled outputs remain synchronized.

## In This Repository Context

Within `build_okf_source_pack.py`, source bundling is presented as an optional mode for building OpenKB-compatible staged input from a Git repository. The implementation is careful to describe bundling as grouping rather than filtering: selected files are still represented, but they are packaged into fewer staged documents.

The tracked-file inventory in `repo-snapshot` also clarifies the likely grouping boundaries. The repository contains several clearly segmented areas: root-level governance files, licensing files, docs assets, and multiple `.agents/skills/*` trees with their own references, assets, and scripts. Those clusters map naturally to bundling by path prefix and help explain why bundle depth is a useful control for source-pack staging.

The script also treats bundling as one part of a larger source-pack workflow that includes repository snapshots, graph-report staging, oversized-file splitting, and manifest generation. That places source bundling inside a broader pipeline of [[concepts/source-pack-staging]] and [[concepts/staging-manifests]].

## See Also

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[concepts/repository-ingestion]]
- [[concepts/staging-manifests]]
- [[concepts/deterministic-builds]]
- [[concepts/document-normalization]]
- [[concepts/provenance-tracking]]
- [[concepts/incremental-compilation]]
- [[concepts/frontmatter-metadata]]
- [[concepts/registry-drift]]
- [[concepts/source-provenance]]

See also: [[summaries/repo-snapshot]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]