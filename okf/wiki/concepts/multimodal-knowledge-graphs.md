---
type: "Concept"
sources: ["summaries/agents__skills__graphify__SKILL-md.md"]
description: "Knowledge graphs built from code, documents, images, and media in one corpus."
---

# Multimodal Knowledge Graphs

Multimodal knowledge graphs are graph representations built from multiple kinds of source material in a single corpus, such as code, documents, papers, images, and audio or video transcripts. They combine structural and semantic extraction so relationships can be traced across formats instead of staying siloed inside one file type.

This concept is central to [[summaries/agents__skills__graphify__SKILL-md]], which defines a pipeline for turning heterogeneous repository and document collections into a persistent graph with reporting, clustering, and interactive querying.

## Core idea

A multimodal knowledge graph treats different content types as parts of the same knowledge space:
- code contributes structural entities and relationships through deterministic extraction
- documents and papers contribute semantic topics, entities, and claims
- images contribute visual or diagrammatic concepts through vision-based extraction
- audio and video contribute transcript-derived content after transcription

The value of the graph comes from linking these modes together. A code module can connect to a design document, a paper concept, an image-derived diagram label, or a transcript explanation. This makes the graph useful for [[concepts/repo-navigation]], [[concepts/repository-overview-generation]], and [[concepts/agent-guided-graph-exploration]].

## In the graphify skill

In [[summaries/agents__skills__graphify__SKILL-md]], multimodal graph construction is handled as a staged pipeline:
- files are first detected and classified by type
- video and audio are transcribed before extraction
- code is extracted structurally through AST-based analysis
- docs, papers, and images are extracted semantically
- all extracted nodes and edges are merged into one graph
- the combined graph is clustered, analyzed, and exported

This design shows that multimodal graphs are not just a storage format; they are the result of coordinated ingestion, normalization, extraction, and merge logic. The concept therefore overlaps with [[concepts/repository-ingestion]], [[concepts/transcription-pipeline-design]], [[concepts/document-normalization]], and [[concepts/graph-merging]].

## Why multimodality matters

A single-modality graph often answers only narrow questions. Code-only graphs are good at architecture and call relationships, while document-only graphs are better for concepts and explanations. A multimodal graph improves coverage by connecting implementation, design intent, and surrounding context.

In the source document, this is reflected in the promise that a user can drop in code, docs, papers, images, or video and receive one queryable graph. That supports:
- richer answers grounded in more than one evidence type
- cross-file and cross-format discovery
- better question answering over mixed corpora
- more useful community detection and graph analysis

This aligns closely with [[concepts/knowledge-graph-analysis]], [[concepts/query-expansion]], and [[concepts/evidence-grounded-answering]].

## Structural and semantic complementarity

A key pattern in multimodal knowledge graphs is separating structural extraction from semantic extraction.

In the graphify workflow:
- code is processed structurally with deterministic AST extraction
- non-code content is processed semantically with LLM or vision support
- the two result sets are merged into a unified extraction artifact

This split matters because different modalities support different extraction guarantees. Structural sources often provide higher precision and clearer link direction, while semantic sources provide broader conceptual coverage. Combining both improves usefulness without forcing one extraction method onto all data.

This connects to [[concepts/llm-free-knowledge-bootstrap]], [[concepts/schema-constrained-extraction]], [[concepts/link-directionality]], and [[concepts/graceful-degradation]].

## Persistence and incremental maintenance

The source document treats multimodal graphs as durable project assets rather than temporary outputs. Intermediate and final artifacts are stored under `graphify-out/`, including detection results, extraction outputs, graph JSON, labels, reports, and cached semantic results.

That persistence enables:
- reuse of an existing graph for future questions
- selective re-extraction of changed files
- caching of semantic work across runs
- stable analysis and reporting workflows

This is closely related to [[concepts/durable-context]], [[concepts/incremental-graph-maintenance]], [[concepts/incremental-compilation]], [[concepts/generated-content-governance]], and [[concepts/staging-manifests]].

## Integrity and honesty requirements

Multimodal graphs are powerful, but they also create more ways for extraction errors or unsupported inferences to enter the graph. The graphify document addresses this by insisting on explicit integrity and honesty rules:
- never invent an edge
- preserve ambiguity where certainty is not justified
- surface graph health warnings instead of hiding them
- distinguish extracted, inferred, and ambiguous relationships
- expose token costs and diagnostics

This matters especially in multimodal settings, where semantic extraction can be noisier than structural parsing and modality boundaries can introduce mismatched identifiers or dangling links. The related ideas here are [[concepts/graph-integrity-diagnostics]], [[concepts/confidence-calibration]], [[concepts/validation-vs-health-reporting]], [[concepts/provenance-tracking]], and [[concepts/telemetry-auditing]].

## Common workflow patterns

From the source document, several recurring patterns define multimodal knowledge graph systems:
- classify content before extraction rather than using one generic pass
- preprocess media into text when needed
- use different extraction strategies per modality
- merge outputs only after each modality-specific pass completes
- keep an auditable record of how graph content was produced
- query the persisted graph directly once it exists

These patterns also support [[concepts/offline-first-workflows]], [[concepts/preflight-checks]], and [[concepts/safe-automation]].

## Relationship to agents

The graphify skill frames the graph not only as an artifact but as a navigation surface for an agent. Once a multimodal graph exists, the agent should answer questions by traversing the graph rather than by re-reading the whole corpus. That makes the graph a durable context layer for future interaction.

This is strongly related to [[concepts/agent-guided-graph-exploration]], [[concepts/agent-context-layering]], [[concepts/durable-context]], and [[concepts/skill-based-automation]].

## Practical significance

Multimodal knowledge graphs are useful when important project knowledge is distributed across many formats. They help unify implementation details, design rationale, external references, and media-based explanation into one navigable structure. In the graphify skill, this concept is operationalized as a repeatable pipeline that supports ingestion, extraction, clustering, export, and question answering over a mixed corpus.

For this wiki, [[summaries/agents__skills__graphify__SKILL-md]] is the primary source page for this concept.