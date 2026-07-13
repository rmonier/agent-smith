---
type: "Concept"
sources: ["summaries/repo-snapshot.md"]
description: "How a repository records, preserves, and uses provenance metadata."
---

# Source Provenance

Source provenance is the practice of preserving where repository content came from, how it was packaged, and what policies govern its use. In OpenKB-style repositories, provenance is not just metadata on a file; it is part of the compilation pipeline that helps keep ingested knowledge traceable, reproducible, and safe to reuse.

## What provenance captures

- The origin of a source pack or document
- The repository paths that were present at ingestion time
- Licensing and attribution constraints attached to the content
- Whether the content is a canonical source, a generated artifact, or a derived summary
- The relationship between tracked files, summaries, and higher-level compiled knowledge

## Why it matters

Provenance supports trust in downstream knowledge products. When OpenKB ingests repository material, it needs to know what was present in the source tree, what was intentionally included, and what policies apply to reuse. That makes provenance a foundation for [[concepts/repository-ingestion]], [[concepts/source-pack-manifest]], and [[concepts/licensing-and-attribution]].

## Repository snapshot as provenance evidence

The `repo-snapshot` document is a direct example of provenance-oriented inventorying. It provides a tracked-file list for the repository, which can be used to establish:

- The exact file surface available at the time of capture
- The presence of core governance files such as `README.md`, `AGENTS.md`, `LICENSE`, `NOTICE`, and `REUSE.toml`
- The existence of modular skill packages under `.agents/skills/`
- The presence of documentation assets and supporting scripts

That inventory is useful because it creates a reproducible reference point for later comparisons. If the repository changes, the snapshot can be checked against new state to detect additions, removals, or unexpected drift.

## Provenance signals in the repository

The snapshot shows several strong provenance signals:

- Multiple license texts are tracked alongside repository-level licensing files
- Third-party notice files are present, indicating explicit attribution handling
- Source-pack style organization suggests content is bundled for controlled ingestion
- Summary pages exist for the tracked documents, showing that source material is being converted into compiled knowledge with traceability back to the original paths

These signals align with [[concepts/source-trust-levels]] and [[concepts/provenance-tracking]], where the goal is to distinguish between raw inputs, managed repository artifacts, and synthesized outputs.

## Relationship to knowledge compilation

Source provenance is a core control in [[concepts/knowledge-compilation-pipeline]]. It helps the system decide:

- What can be ingested
- What should be summarized
- What deserves an entity or concept page
- What must remain linked to its original source path

In practice, provenance also supports [[concepts/documentation-source-priority]] by making the source hierarchy explicit, and it helps with [[concepts/generated-content-governance]] by separating source-derived content from compiled wiki pages.

## Practical outcome

A well-maintained provenance trail lets the wiki preserve evidence while still transforming the repository into navigable knowledge. The result is a more reliable index of the project, clearer attribution, and better resistance to accidental loss of context when files are summarized or reorganized.

## Related Documents
- [[summaries/repo-snapshot]]
