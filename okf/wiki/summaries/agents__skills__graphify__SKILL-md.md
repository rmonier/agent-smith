---
type: "Summary"
description: "Skill spec for running and querying the graphify knowledge-graph pipeline."
doc_type: short
full_text: "sources/agents__skills__graphify__SKILL-md.md"
---

# Summary

This document defines the `graphify` skill: an end-to-end procedure for turning a folder, repository, or mixed-media corpus into a persistent knowledge graph with query and export workflows. It specifies exact invocation behavior, command variants, branching logic, extraction stages, caching, graph construction, diagnostics, labeling, and reporting.

## Purpose

`graphify` is presented as a tool for converting code, documents, papers, images, and video into a navigable graph with:
- interactive HTML output
- GraphRAG-ready JSON
- a plain-language `GRAPH_REPORT.md`
- optional exports such as Obsidian, Neo4j, FalkorDB, SVG, GraphML, wiki pages, and MCP access

A key promise is an "honest audit trail" distinguishing extracted, inferred, and ambiguous relationships, alongside [[concepts/knowledge-graph-analysis]], graph traversal, and explanation tools.

## Main workflow

The skill defines a strict multi-step pipeline:
- install or locate the correct Python environment for `graphify`
- detect corpus composition and summarize file counts/word counts
- transcribe audio/video if present
- extract structure from code using AST-based analysis
- extract semantic entities and relationships from docs, papers, and images
- merge extracted outputs into a unified graph dataset
- build and cluster the graph
- analyze important nodes and cross-community connections
- generate reports and export artifacts
- save manifests and cumulative token-cost tracking

The workflow emphasizes persistence through `graphify-out/`, reuse across runs, and update-safe manifests and caches.

## Key operational rules

### Existing-graph fast path

If `graphify-out/graph.json` already exists and the user's request is a natural-language question about the corpus, the skill says to skip rebuild steps entirely and jump directly to `graphify query`. This makes existing graph state the default source of truth for exploratory questions.

This fast path is closely tied to [[concepts/agent-guided-graph-exploration]] and [[concepts/incremental-graph-maintenance]].

### Default path and URL handling

If no path is supplied, the skill defaults to `.`. GitHub URLs trigger a special Step 0 that clones repos or merges multiple repositories before continuing. Local paths skip that step.

### Help behavior

If invoked with `/graphify --help` or `/graphify -h` alone, the agent must print only the Usage block verbatim and stop.

## Detection and corpus control

The detect stage writes a JSON summary and requires a user-facing condensed report showing file and word counts by category. It includes several gating behaviors:
- stop if no supported files are found
- mention count of skipped sensitive files without listing names
- warn when corpus size exceeds 2,000,000 words or 500 files
- compute top first-level subdirectories to help narrow large corpora
- if everything is at repo root, suggest `--no-cluster` instead of asking for a subfolder

This section shows a strong concern for corpus scoping and cost-aware extraction.

## Extraction model

### Structural extraction

Code files are processed structurally via AST extraction, producing nodes and edges without using an LLM. For code-only corpora, this is the dominant extraction path.

### Semantic extraction

Documents, papers, and images are processed semantically. The skill makes several strong claims:
- `graphify` does not require an API key
- if Gemini environment variables are set, semantic extraction should use Gemini directly
- otherwise the host agent performs semantic extraction
- no other provider keys are relevant
- the agent must not block waiting for missing keys

This frames the extraction system around [[concepts/llm-free-knowledge-bootstrap]], semantic extraction, and [[concepts/graceful-degradation]].

### Parallel execution

AST extraction and semantic extraction should run in parallel. Semantic extraction itself must be chunked and dispatched via agent sub-tasks, not performed by manually reading files one-by-one. The document explicitly marks Agent/Task usage as mandatory for this phase.

### Cache-aware extraction

Before semantic extraction, the system checks cache hits, extracts only uncached files, writes chunk outputs, merges results, then saves new semantic cache data. Cached and newly extracted nodes/edges/hyperedges are combined into the final semantic output.

This is one of the document's clearest expressions of extraction caching and parallel processing.

## Graph construction and analysis

After merging AST and semantic results, the graph is built and analyzed. The spec includes:
- optional directed mode preserving source-to-target edge direction
- clustering into communities
- cohesion scoring
- god-node detection
- surprising-connection analysis
- suggested-question generation
- refusal to overwrite an existing larger `graph.json` with a smaller graph unless forced

The graph build stage stops if the resulting graph is empty, explicitly protecting against destructive or misleading rebuilds.

This part strongly relates to [[concepts/knowledge-graph-analysis]], graph construction, [[concepts/link-directionality]], and [[concepts/provenance-tracking]].

## Graph health and integrity

A dedicated read-only diagnostic step checks for:
- dangling endpoint edges
- missing endpoint edges
- self-loops
- collapsed edges due to endpoint duplication in directed or undirected contexts

Warnings must be surfaced to the user but do not abort execution. This reflects an explicit integrity model where graph usefulness and graph trustworthiness are treated separately.

## Labeling and reporting

Communities must be assigned concise human-readable labels based on their node labels. These labels are then used to regenerate:
- the report
- suggested questions
- visualization metadata

At completion, the user should receive:
- output locations
- token counts for the current run and all-time totals
- selected report sections only: God Nodes, Surprising Connections, Suggested Questions
- a proposed next exploratory question drawn from the graph

This emphasizes graph explainability and conversational graph navigation.

## Query and subcommand behavior

The document also defines behavior for follow-on commands:
- `query` for BFS/DFS traversal of existing graph state
- `path` for shortest paths between concepts
- `explain` for plain-language node explanation
- `add` for fetching URLs into the corpus
- `--watch` for automatic rebuilds
- `--update` for incremental re-extraction
- `--cluster-only` for reclustering existing graph state

Before such subcommands, the interpreter path must be restored from `.graphify_python` or re-resolved if missing.

## Exports and ecosystem integration

Optional exports include:
- HTML visualization
- Obsidian vault generation
- wiki export
- Neo4j and FalkorDB export or push
- SVG and GraphML export
- MCP server startup
- benchmarking for token reduction on large corpora

The document also references integration with commit hooks and project `AGENTS.md` wiring.

## Design principles and notable ideas

### Strict procedural orchestration

The skill is unusually prescriptive: it gives exact command snippets, exact stopping conditions, and exact branching behavior. It is less a general description than an execution protocol.

### Persistence-first architecture

The entire design revolves around `graphify-out/` as durable working state: cached extraction artifacts, interpreter path, manifest, graph JSON, analysis files, labels, and cost accounting.

### Honest graph semantics

The document repeatedly stresses honesty: do not invent edges, surface warnings, expose cohesion and token costs, and preserve uncertainty via extracted/inferred/ambiguous distinctions.

### Agent as graph guide

The intended end state is not just graph generation but interactive guided exploration. The skill frames the agent as a navigator of the graph rather than only a builder of it.

## Likely concept pages

This source would support concept synthesis around:
- [[concepts/agent-guided-graph-exploration]]
- [[concepts/graph-integrity-diagnostics]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/link-directionality]]
- [[concepts/mcp-server-integration]]
- [[concepts/multimodal-knowledge-graphs]]
- [[concepts/provenance-tracking]]
- [[concepts/query-expansion]]
- [[concepts/repository-ingestion]]
- [[concepts/transcription-pipeline-design]]

## Overall significance

The document is a detailed operating specification for a repository-analysis and corpus-analysis workflow built around persistent knowledge graphs. Its main contribution is not algorithmic theory but a disciplined execution model that combines multimodal extraction, caching, incremental updates, diagnostics, community labeling, and conversational query support into a single agent-oriented pipeline.

## Related Concepts
- [[concepts/action-oriented-documentation]]
- [[concepts/evidence-grounded-answering]]
- [[concepts/schema-constrained-extraction]]
- [[concepts/source-provenance]]
- [[concepts/validation-vs-health-reporting]]

## Entities
- [[entities/gemini]]
- [[entities/networkx]]
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/neo4j]]
- [[entities/falkordb]]
- [[entities/claude-desktop]]
- [[entities/agents-md]]
- [[entities/openkb]]
- [[entities/uv]]
- [[entities/astral]]
