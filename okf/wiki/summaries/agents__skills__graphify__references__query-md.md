---
type: "Summary"
description: "Defines graph query, path, and explain workflows with vocab-aware traversal."
doc_type: short
full_text: "sources/agents__skills__graphify__references__query-md.md"
---

# Summary

This reference defines how `graphify` should answer questions against an existing graph, including `/graphify path` and `/graphify explain` flows. Its main contribution is a strict, auditable retrieval process that expands user queries using only tokens already present in the graph vocabulary before any traversal begins.

## Core purpose

The document describes a graph interrogation workflow that:
- verifies a built graph exists before querying
- refreshes prior lessons via `graphify reflect --if-stale`
- expands the user query from actual graph vocabulary
- traverses with either CLI support or inline `NetworkX` fallback
- answers only from graph evidence
- saves the result back into the graph for future reuse

This is a retrieval-and-feedback loop centered on graph traversal, [[concepts/query-expansion]], and [[concepts/knowledge-graph-feedback-loops]].

## Traversal modes

Two traversal strategies are defined:
- `BFS` as the default for broad neighborhood discovery and nearest-context questions
- `DFS` for tracing specific chains or dependency paths

The guidance ties traversal choice to question shape: broad “what is connected to X?” questions use breadth-first search, while “how does X reach Y?” questions use depth-first search. This reinforces a practical distinction between breadth-first search and depth-first search.

## Required constrained query expansion

A mandatory pre-traversal step addresses limitations in the graph matcher:
- matching is case-folded substring plus IDF
- there is no stemming
- there are no built-in synonyms
- there is no cross-language matching

To avoid zero-hit queries, the workflow extracts a token vocabulary from node labels, writes it to `graphify-out/.vocab.txt`, and requires selection of up to 12 semantically relevant tokens from that exact list. Important constraints include:
- no invented tokens
- no substitution from model memory when the graph lacks the concept
- empty expansion must halt the workflow
- cross-language mapping is allowed only if matching vocab tokens actually exist
- morphology normalization is allowed only when the normalized token is present in vocab

The chosen tokens must be shown to the user explicitly for auditability. This is the document’s strongest procedural idea and a clear example of constrained retrieval and vocabulary grounding.

## Query execution and fallback traversal

After expansion, the selected tokens are joined into the actual query string used for traversal. The workflow prefers `graphify query`, optionally with `--dfs` and `--budget`, but specifies an inline Python fallback using `NetworkX` when the CLI is unavailable.

The fallback process:
- scores nodes by overlap between expanded terms and node labels
- chooses 1-3 best start nodes
- performs BFS or DFS with depth limits
- ranks output nodes by relevance
- emits node labels, relations, confidence, and source metadata
- truncates output according to a token-aware character budget

The answer must be based only on returned graph structure and should cite `source_location` when stating specific facts. If evidence is insufficient, the agent must say so. This emphasizes [[concepts/evidence-grounded-answering]] and hallucination avoidance.

## Saving results back into the graph

After answering, the result is saved with `graphify save-result` using:
- the original user question
- the full answer
- cited node labels
- the query type
- an `--outcome` value of `useful`, `dead_end`, or `corrected`

The answer text should include the expanded-token trace so future graph updates can learn from prior query expansion choices. Corrections may also include `--correction`. This creates an explicit self-improving systems pattern where past successes, failures, and fixes are encoded as graph data.

## Reflection and lessons

Before graph work begins, the document instructs the agent to run `graphify reflect --if-stale` and read `graphify-out/reflections/LESSONS.md`. That file is described as containing:
- preferred sources
- known dead ends
- prior corrections

This makes reflection a standard pre-query optimization step and links the workflow to operational memory and continuous improvement.

## Path workflow

For `/graphify path`, the document defines a shortest-path query between two named concepts. It prefers `graphify path "NODE_A" "NODE_B"` but includes an inline `NetworkX` fallback that:
- finds best matching source and target nodes
- computes shortest path
- prints each hop with relation and confidence
- handles missing nodes and no-path cases

The human-facing output should explain what each hop means and why it matters. Results are then saved back with type `path_query`. This section is mainly about pathfinding in graphs and interpretable explanation of graph routes.

## Explain workflow

For `/graphify explain`, the document defines a single-node explanation flow. It prefers `graphify explain "NODE_NAME"` but provides a fallback that:
- finds the best matching node
- reports source, file type, and node degree
- lists neighboring nodes and edge relations

The expected output is a concise 3-5 sentence explanation of the node, its connections, and their significance, ideally using source locations as citations. Results are saved back with type `explain`. This supports local graph explanation and knowledge graph interpretation.

## Key ideas

- Querying should be grounded in graph vocabulary rather than freeform language.
- Traversal mode should follow the user’s question type.
- CLI tools are preferred, but deterministic inline fallbacks are fully specified.
- Answers must remain strictly bounded by graph evidence.
- Every query should improve future graph sessions through saved results and reflections.

## Potential concept links

This document could support or connect to:
- [[concepts/query-expansion]]
- [[concepts/evidence-grounded-answering]]
- [[concepts/knowledge-graph-feedback-loops]]

## Related Concepts
- [[concepts/graceful-degradation]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/action-oriented-documentation]]
- [[concepts/confidence-calibration]]
- [[concepts/documentation-source-priority]]
- [[concepts/offline-first-workflows]]
- [[concepts/preflight-checks]]
- [[concepts/provenance-tracking]]
- [[concepts/safe-automation]]
- [[concepts/skill-based-automation]]

## Entities
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/openkb]]
- [[entities/uv]]
