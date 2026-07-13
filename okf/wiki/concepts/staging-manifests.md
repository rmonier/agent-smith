---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Machine-readable ledger of a staging run for audit and replay."
---

# Staging Manifests

A staging manifest is a machine-readable ledger of a staging run. It records which source items were selected, where they were written, how they were transformed, and what provenance metadata is needed to audit or reproduce the result. In this repository, the concept is demonstrated by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], which writes a sorted JSON manifest alongside the staged OpenKB input pack.

## What a staging manifest does

A staging manifest turns an otherwise opaque staging directory into an explicit inventory. Instead of treating the output as just files on disk, the manifest enumerates each staged item and describes how it was produced.

In the source-pack builder, each entry can include:

- `source_path`: the original logical path of the staged content
- `staged_path`: the generated path written into the staging output
- `source_hash`: a content hash for the normalized source text
- `source_kind`: a category such as text, markdown, code, or bundle
- `origin`: where the staged item came from, such as repository content, Graphify output, or a repository snapshot
- `part`: the part number for oversized files that were split instead of cropped
- `member_count`: the number of source files included in a bundle

That makes the manifest useful both for one-to-one file staging and for grouped or split outputs.

## Why staging manifests matter

Staging manifests make ingestion auditable, deterministic, and easier to reconcile. The source-pack builder is designed so unchanged content produces stable staged bytes, and the manifest complements that by preserving a stable record of what the run emitted.

This supports several adjacent concerns:

- [[concepts/provenance-tracking]] by tying staged outputs back to source paths, hashes, and commits
- [[concepts/deterministic-builds]] by emitting a sorted manifest from normalized inputs
- [[concepts/repository-ingestion]] by turning a repository scan into a declared ingestion set
- [[concepts/kb-root-staging]] by documenting the exact artifacts placed under the OpenKB staging area
- [[concepts/source-pack-manifest]] as the control record for the staging step itself

## Role in deterministic pipelines

A staging manifest is especially valuable in workflows where repository content is transformed before ingestion. In the source-pack builder, files are normalized, optionally bundled, optionally split, and then written with generated frontmatter. The manifest is the compact ledger of those transformations.

It helps answer practical questions such as:

- Which source files were included in the staged pack?
- Which generated Markdown file corresponds to a given repository path?
- Did a file stage as an individual source file, a split part, or a bundle?
- What hash identifies the normalized content that was staged?
- Which commit last touched the source that produced this staged item?

Because the manifest is sorted before being written, it also improves reproducibility and comparison across runs, aligning with [[concepts/document-normalization]] and [[concepts/line-ending-normalization]].

## Behavior in the source-pack builder

In [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], the manifest is assembled as the script stages several kinds of inputs:

- a repository snapshot document listing tracked files
- an optional Graphify report, if it is safe to stage
- selected repository files from docs, code, and repo-scoped configuration
- oversized files split into full-content parts when necessary
- optional per-directory source bundles when bundle mode is enabled

The script also records `source_commit` for many staged items using the last commit that touched each file, while falling back to `untracked` or `uncommitted` when no commit is available. That makes the manifest a stronger provenance record than a plain filename list.

The builder intentionally avoids embedding `HEAD` in the staged snapshot or file metadata when that would cause needless churn. Instead, it uses last-touch provenance so the manifest changes only when the source content or its direct history changes. It also normalizes line endings before hashing and staging, which keeps manifest records stable across platforms.

After staging is complete, the script sorts the manifest by `source_path` and `staged_path` and writes it as JSON. This keeps the manifest itself deterministic and makes it suitable for diff-based inspection.

The manifest therefore connects content staging with [[concepts/source-bundling]] when multiple files are grouped into directory-level digests, with [[concepts/source-partitioning]] when oversized files are split into parts, and with [[concepts/self-reference-control]] when the builder refuses to stage a graph report that appears to reference KB output paths.

## Boundaries and expectations

A staging manifest is not the staged content itself and not the final compiled wiki. It is a control artifact that describes the staging result. Its value comes from being complete, stable, and directly tied to the generated outputs.

In a healthy workflow, the manifest should:

- cover every staged item
- use stable identifiers derived from normalized content
- reflect bundling, splitting, and special-origin rules
- remain suitable for comparison across runs
- preserve enough provenance to support later review or cleanup

This makes staging manifests a key mechanism for traceable, low-surprise automation, closely related to [[concepts/safe-automation]] and [[concepts/generated-content-governance]].

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[concepts/provenance-tracking]]
- [[concepts/deterministic-builds]]
- [[concepts/repository-ingestion]]
- [[concepts/kb-root-staging]]
- [[concepts/source-bundling]]
- [[concepts/source-partitioning]]
- [[concepts/document-normalization]]
- [[concepts/line-ending-normalization]]
- [[concepts/self-reference-control]]
- [[concepts/safe-automation]]
- [[concepts/generated-content-governance]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

See also: [[summaries/repo-snapshot]]