---
type: "Summary"
description: "Builds deterministic OpenKB staging packs from a Git repository."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"
---

# Summary

This script builds a deterministic OpenKB-compatible source pack from a Git repository, staging tracked files into `okf/.okf-build/input` with normalized content, stable hashes, and a manifest. It is designed to make ingestion reproducible while avoiding churn from non-content changes like timestamps or commit heads.

## What it does

- Scans `git ls-files` and filters paths with `should_skip()` and `should_select()` to choose repo files worth staging.
- Writes a repository snapshot document listing tracked files so the pack always includes a simple inventory.
- Optionally includes a `graphify-out/GRAPH_REPORT.md` report, after stripping generated timestamp noise and refusing to stage it if it appears to reference the compiled KB too heavily.
- Stages each selected source file as a Markdown wrapper with frontmatter fields such as `source_path`, `source_kind`, `source_hash`, and `source_commit`.
- Produces a JSON manifest of staged items for later reconciliation and tooling.

## Key behaviors

- Uses SHA-256 over normalized UTF-8 text to generate deterministic `source_hash` values.
- Normalizes line endings to `\n` so the same file content hashes identically across platforms.
- Derives `source_commit` from the last Git commit that touched a path rather than from `HEAD`, preventing needless reingestion on unrelated commits.
- Supports `--hash-names` to add a hash prefix to staged filenames.
- Supports `--bundle-depth` to group non-markdown files into per-directory bundles instead of one staged document per file.
- Supports `--code-split` to split oversized code files into full-content parts rather than cropping them.
- Splits oversized markdown or code files at layout-aware boundaries so no content is silently lost.

## Important concepts

- deterministic source pack staging: the pack is built so identical inputs produce identical staged output.
- hash registry coherence: hashes are computed from normalized content and used for dedupe and provenance.
- source provenance: each staged document records where it came from and which commit last touched it.
- source partitioning: large files are partitioned into parts instead of truncated.
- source bundling: supporting files can be grouped into directory-based digests for large repos.
- self reference control: graph reports are excluded if they appear to map the compiled KB itself.

## Notable findings

- The script intentionally avoids embedding the current HEAD commit in staged frontmatter, because that would change staged bytes on every commit and trigger pointless reingestion.
- The code treats a code-only repository differently from a prose repo: if no markdown sources are selected, oversized code is split by default because code becomes the primary concept source.
- The bundle mode has a safety guard that deepens the grouping or warns when a bundle becomes too large, which helps keep staged documents within model-friendly size limits.
- A deletion advisory is emitted when previously known KB documents no longer have a matching source in the current pack, but actual retraction is delegated to `prune_okf_orphans.py`.

## Broader ideas

This script sits at the boundary between repository content and compiled knowledge. It encodes a philosophy of deterministic source pack staging, where file selection, normalization, and partitioning are all designed to preserve meaning while keeping ingestion stable. It also reflects a strong bias toward non-destructive handling of source material: large files are split, not cropped, and problematic graph outputs are skipped rather than silently accepted.

## Outputs

- `okf/.okf-build/input/repo-snapshot.md`
- `okf/.okf-build/input/graphify-report.md` when safe
- `okf/.okf-build/input/repo-files/*.md` staged source files or bundles
- `okf/.okf-build/manifests/source-pack-manifest.json` manifest of staged items

## Related Concepts
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/source-pack-manifest]]
- [[concepts/source-partitioning]]
- [[concepts/deterministic-builds]]
- [[concepts/document-normalization]]
- [[concepts/source-bundling]]
- [[concepts/source-provenance]]
- [[concepts/staging-manifests]]
- [[concepts/self-reference-control]]
- [[concepts/incremental-compilation]]
- [[concepts/orphan-retraction]]
- [[concepts/repository-inventory]]
- [[concepts/repo-ingestion-pipelines]]
- [[concepts/hash-registry-coherence]]
- [[concepts/line-ending-normalization]]
- [[concepts/path-based-validation]]
- [[concepts/source-driven-regeneration]]
- [[concepts/knowledge-capture-boundaries]]

## Entities
- [[entities/build_okf_source_pack-py]]
- [[entities/repo-snapshot]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/openkb]]
- [[entities/okf]]
- [[entities/graphify]]
- [[entities/git]]
- [[entities/python]]
- [[entities/uv]]
- [[entities/prune_okf_orphans-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki]]
