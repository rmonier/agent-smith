---
type: "Summary"
description: "Specifies the prompt and schema for graphify extraction subagents."
doc_type: short
full_text: "sources/agents__skills__graphify__references__extraction-spec-md.md"
---

# Summary

This document defines the verbatim prompt used by the graphify extraction subagent during semantic extraction for non-code corpus chunks. It explains when the prompt is loaded, what kinds of relationships and nodes the subagent should emit, and the exact JSON schema and path-writing behavior required for downstream graph building.

## Main Purpose

- Provides the extraction prompt used in Step 3 Part B when the corpus includes at least one document, paper, or image chunk.
- Skips this prompt entirely for pure-code corpora, where semantic document extraction is not needed.
- Standardizes how a subagent converts source chunks into a knowledge graph fragment.

## Extraction Scope

The subagent is instructed to read listed files and emit a graph fragment with:

- `nodes`
- `edges`
- optional `hyperedges`
- token counts

It distinguishes among several source modalities:

- `code`
- `document`
- `paper`
- `image`
- `rationale`
- `concept`

A central rule is that rationale should not become its own standalone rationale node unless it is attached as a `rationale` attribute on a relevant concept-like node. This makes schema-constrained extraction and rationale capture likely future concept pages.

## Relationship Semantics

The prompt defines three confidence classes for extracted relationships:

- `EXTRACTED` for explicit relationships present in the source
- `INFERRED` for reasonable interpretation-based relationships
- `AMBIGUOUS` for uncertain relationships that should still be surfaced for review

It also defines allowed edge relations, including:

- `calls`
- `implements`
- `references`
- `cites`
- `conceptually_related_to`
- `shares_data_with`
- `semantically_similar_to`
- `rationale_for`

Notable semantic constraints include:

- AST-derived imports must not be duplicated by the semantic extractor.
- `calls` edges must run from caller to callee.
- `calls` edges must stay within a single language and never imply cross-language invocation artifacts.
- `semantically_similar_to` should only capture genuinely non-obvious, cross-cutting similarity.

These rules point toward [[concepts/confidence-calibration]], link directionality, and semantic similarity in graphs.

## Confidence Scoring Rules

The specification strongly constrains confidence scoring:

- Every edge must include `confidence_score`.
- `EXTRACTED` always uses `1.0`.
- `INFERRED` must use one discrete value from a fixed rubric: `0.95`, `0.85`, `0.75`, `0.65`, or `0.55`.
- `AMBIGUOUS` must use a low score between `0.1` and `0.3`.
- `0.5` is explicitly forbidden as a default.

The document explains that discrete scoring is preferred because continuous ranges were collapsing into poor production behavior. This is a concrete design decision relevant to [[concepts/confidence-calibration]] and [[concepts/schema-constrained-extraction]].

## Hyperedges

The prompt allows sparse use of hyperedges when group-level meaning cannot be captured by pairwise edges alone. Examples include:

- protocol or interface implementation groups
- authentication-flow function sets
- coherent concept groups from a paper section

Hyperedges are limited to a maximum of three per chunk and must add information beyond standard edges. This suggests a future concept page like hyperedges in knowledge graphs.

## Node Identity Rules

A major portion of the specification is devoted to deterministic node IDs.

Rules include:

- IDs must be lowercase and limited to `[a-z0-9_]`.
- IDs are built from the full repo-relative path with extension removed, plus a normalized entity name.
- Every directory segment must be preserved in the ID stem.
- Chunk numbers or sequence suffixes must never be added.

The goal is to prevent duplicate or orphaned nodes and to align semantic extraction with AST extraction. The spec warns that old immediate-parent-only ID formats can cause ghost duplicates and recommends force rebuilds when re-extracting legacy projects. This is strongly connected to naming normalization and [[concepts/incremental-graph-maintenance]].

## Source File Preservation

The spec emphasizes that `source_file` must be copied exactly from `FILE_LIST`:

- verbatim
- absolute
- no basename shortening
- no re-relativization
- no separator normalization by the model

This preserves compatibility between full builds and incremental updates, especially during downstream merge-and-replace behavior. This is relevant to [[concepts/source-provenance]] and incremental extraction consistency.

## Output Contract

The subagent must:

- output only valid JSON matching the schema exactly
- include nodes, edges, and optional hyperedges
- write the JSON to disk using the Write tool
- write to the exact absolute path provided in `CHUNK_PATH`

The warning about relative paths is operationally important: relative writes may resolve against an undefined working directory and silently lose output.

## Key Ideas

- Semantic extraction complements AST extraction rather than duplicating it.
- Confidence should be structured with a discrete rubric instead of vague continuous scoring.
- Deterministic IDs are essential for graph stability.
- Provenance fidelity is required for incremental rebuild correctness.
- Hyperedges should be rare and information-rich.
- Rationale belongs on concept-like nodes rather than becoming free-floating graph fragments.

## Notable Design Decisions

- Pure-code corpora bypass this semantic extraction prompt.
- Image understanding must use vision-level interpretation, not just OCR.
- YAML frontmatter metadata should propagate onto every node from a source file.
- Cross-language `calls` edges are treated as invalid phantom artifacts.
- Ambiguous relationships should be surfaced rather than omitted.

## Related Concepts
- [[concepts/idempotent-graph-import]]
- [[concepts/naming-normalization]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/provenance-tracking]]
- [[concepts/deterministic-builds]]
- [[concepts/path-safety]]
- [[concepts/multimodal-url-ingestion]]
- [[concepts/subagent-role-design]]
- [[concepts/deterministic-validation]]

- [[concepts/schema-constrained-extraction]]
- [[concepts/confidence-calibration]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/source-provenance]]

## Entities
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/openkb]]
- [[entities/falkordb]]
- [[entities/neo4j]]
