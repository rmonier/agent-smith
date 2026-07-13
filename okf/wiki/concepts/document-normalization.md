---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Stable canonicalization of documents before hashing and staging."
---

# Document Normalization

Document normalization is the practice of converting source material into a stable, predictable text form before hashing, packaging, indexing, or downstream analysis. Its goal is to make semantically unchanged content produce the same staged representation, supporting [[concepts/deterministic-builds]], [[concepts/provenance-tracking]], [[concepts/incremental-compilation]], and [[concepts/deterministic-validation]].

## Why it matters

Repository-to-knowledge workflows often ingest text that differs only in incidental ways: line endings, encoding behavior, trailing formatting, volatile report metadata, or generated date stamps. Without normalization, those differences can make identical content look new and trigger unnecessary re-ingestion, recompilation, or manifest churn.

Normalization keeps the pipeline focused on meaningful source changes instead of environment noise. That is especially important when downstream systems deduplicate by hash or use staged bytes as the trigger for further work. A stable canonical form supports [[concepts/hash-registry-coherence]], [[concepts/repository-ingestion]], and [[concepts/evidence-staging]].

## Core idea

The concept separates two kinds of change:

- meaningful changes in the source content
- incidental changes introduced by platform differences, encoding edge cases, or generated metadata

A normalization step preserves the first and suppresses the second. In practice, that means turning documents into a canonical form before computing hashes or emitting derived files, while still keeping enough fidelity for trustworthy provenance and review.

The source pack builder in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] shows this clearly: it normalizes bytes into UTF-8 text, collapses `\r\n` and `\r` into `\n`, strips volatile report fields, and hashes the normalized text instead of the raw file bytes. That makes the staged output deterministic without changing the underlying meaning of the source.

## How the source document illustrates the concept

[[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] shows document normalization inside an OpenKB staging pipeline.

The script normalizes text in several concrete ways:

- It decodes bytes as UTF-8 with replacement behavior so imperfect input can still be staged.
- It converts `\r\n` and `\r` line endings to `\n`, making staged text platform-independent.
- It writes output with explicit UTF-8 encoding and normalized newlines.
- It ensures emitted files end with a trailing newline so generated artifacts have a consistent byte shape.
- It computes `source_hash` from normalized text instead of raw file bytes.
- It strips volatile `timestamp:` lines from generated reports before staging.
- It removes runtime date suffixes from Graphify report headings so daily report churn does not create new hashes.
- It uses normalized text for repository snapshots, graph reports, source files, and source bundles so all staged artifacts follow the same canonicalization rules.

Those choices make the staged pack deterministic: unchanged content stays unchanged at the byte level, and hashes move only when the meaningful content moves. In this script, normalization is not an afterthought; it is the precondition for reliable staging and a direct support for [[concepts/source-pack-staging]], [[concepts/source-provenance]], and [[concepts/line-ending-normalization]].

## Normalization in generated documents

The source document also shows that normalization applies to generated outputs, not just repository source files. The `graphify-out/GRAPH_REPORT.md` file may contain a `timestamp:` line and a heading with an appended date. If staged as-is, those values would change every run or every day even when the report content stayed structurally the same.

The script removes those unstable details before hashing and storing the report. That keeps the report usable as a stable exploration artifact instead of a daily churn source. It also demonstrates that normalization is paired with governance: the script refuses to stage a Graphify report when it appears to reference `okf/` paths, because a stable document can still be the wrong document to ingest. That connects this concept to [[concepts/self-reference-control]], [[concepts/knowledge-boundaries]], [[concepts/generated-content-governance]], and [[concepts/self-referential-ingestion-loops]].

## Typical normalization operations

Common normalization steps in knowledge-ingestion pipelines include:

- decoding bytes into a consistent text representation
- standardizing line endings
- ensuring predictable trailing newlines on output
- removing or rewriting volatile generated metadata
- hashing canonicalized text rather than environment-specific byte streams
- preserving original meaning while removing accidental formatting variance

Not every document needs every step, but the principle is the same: normalize enough to make the representation stable without erasing evidence that matters.

## Benefits

Document normalization improves several properties of a knowledge workflow:

- stable content hashes for deduplication
- fewer unnecessary rebuilds and re-ingests
- better cross-platform consistency
- clearer provenance because metadata reflects actual source changes
- more trustworthy repository snapshots, staged evidence, and manifests

These benefits reinforce [[concepts/repository-ingestion]], [[concepts/staging-manifests]], [[concepts/offline-first-workflows]], and [[concepts/compiled-knowledge-bases]] where repeatability matters.

## Boundaries and cautions

Normalization should not become silent alteration of meaning. A good normalization policy removes irrelevant variance but does not discard evidence that users may need later. For example:

- line-ending conversion is usually safe
- stripping generated timestamps may be safe when timestamps are purely operational
- removing substantive dates, identifiers, or source annotations may be unsafe if they carry meaning
- replacement decoding improves robustness, but it can also hide underlying encoding problems if teams stop checking the original source quality

This makes normalization partly a governance question, not just a formatting step. Teams need clear rules for what counts as noise versus evidence, and they need to distinguish byte-level stability from semantic integrity. That links the concept to [[concepts/spec-authority]] and [[concepts/generated-content-governance]].

## In the OpenKB context

Within the workflow represented by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], document normalization is a foundational preparation step before OpenKB ingestion. It ensures that staged Markdown wrappers, repository snapshots, per-file source documents, bundled source digests, and normalized reports are suitable for stable hashing and downstream compilation.

The script also shows how normalization fits into broader source-pack staging practice: it keeps derived content deterministic, it avoids feedback loops from generated KB paths, and it records provenance in a manifest so the staged artifacts remain traceable. In that sense, document normalization is one of the basic enabling practices behind deterministic repository staging: it makes packaged source material consistent enough to support trustworthy knowledge build behavior, while still preserving file-level provenance and compatibility with [[concepts/source-bundling]], [[concepts/source-provenance]], and [[concepts/source-pack-staging]].

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[concepts/deterministic-builds]]
- [[concepts/line-ending-normalization]]
- [[concepts/evidence-staging]]
- [[concepts/generated-content-governance]]
- [[concepts/provenance-tracking]]
- [[concepts/repository-ingestion]]
- [[concepts/incremental-compilation]]
- [[concepts/hash-registry-coherence]]
- [[concepts/deterministic-validation]]
- [[concepts/self-reference-control]]
- [[concepts/staging-manifests]]
- [[concepts/source-pack-staging]]
- [[concepts/source-provenance]]
- [[concepts/source-bundling]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]