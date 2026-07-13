---
type: "Summary"
description: "Reference for Graphify export flags, MCP setup, and benchmark trigger."
doc_type: short
full_text: "sources/agents__skills__graphify__references__exports-md.md"
---

# Summary

This reference file defines optional post-processing steps for `graphify` runs when specific export flags are passed, plus a benchmark step for large corpora.

## Main purpose

It documents how to handle extra export modes after graph generation, including wiki export, graph database export, visualization export, MCP serving, and a token-reduction benchmark. The steps are conditional and should run only when their matching flags are present.

## Key points

### Conditional execution model

- Each step is tied to a specific CLI flag and should only run for that flag.
- The wiki export must run before cleanup so `.graphify_labels.json` is still available.
- The benchmark runs only when corpus size exceeds a word-count threshold.

This reflects a broader pattern of safe, flag-gated workflow execution and skill-based automation.

### Wiki export

When `--wiki` is explicitly provided, run:

`graphify export wiki`

The note emphasizes ordering constraints: this step must happen before cleanup because it depends on `.graphify_labels.json`.

Related concept: [[concepts/llm-wiki]].

### Neo4j export

Two modes are described:

- `--neo4j`: generate a Cypher file for manual import.
- `--neo4j-push <uri>`: push directly to a running Neo4j instance.

Defaults:

- URI: `bolt://localhost:7687`
- User: `neo4j`

The file notes that credentials should be requested only if not already provided, and that imports use `MERGE`, making repeated runs idempotent with respect to duplicate creation.

Related concepts:
- [[concepts/idempotent-graph-import]]
- [[entities/neo4j]]

### FalkorDB export

Two modes are also described:

- `--falkordb`: generate a portable OpenCypher `cypher.txt` artifact.
- `--falkordb-push <uri>`: push directly to a running FalkorDB instance.

Important implementation nuance:

- FalkorDB accepts OpenCypher, but `GRAPH.QUERY` executes one statement at a time.
- Because there is no Neo4j-style bulk shell import workflow, direct push is preferred for actually loading a graph.

Defaults and behavior:

- Default URI: `falkordb://localhost:6379`
- `redis://` or bare `host:port` also work
- Auth is optional
- Default graph name is `graphify`
- Uses `MERGE`, so reruns do not create duplicates

Related concepts:
- [[concepts/idempotent-graph-import]]
- [[entities/falkordb]]

### SVG and GraphML export

The file includes lightweight export paths for:

- `graphify export svg`
- `graphify export graphml`

These support alternate graph consumption modes such as visualization and interchange.

Related concepts:
- [[concepts/knowledge-graph-analysis]]
- [[concepts/svg-illustration-techniques]]

### MCP server mode

When `--mcp` is used, the reference starts a stdio MCP server with:

`$(cat graphify-out/.graphify_python) -m graphify.serve graphify-out/graph.json`

The server exposes graph-querying tools including:

- `query_graph`
- `get_node`
- `get_neighbors`
- `get_community`
- `god_nodes`
- `graph_stats`
- `shortest_path`

A practical setup note is included for Claude Desktop:

- Claude Desktop cannot execute shell substitution like `$(...)`.
- The configured `command` must therefore be the absolute Python interpreter path read from `graphify-out/.graphify_python`.
- The graph path should also be given as an absolute path.

This section connects local graph artifacts to agent tooling and live querying.

Related concepts:
- [[concepts/mcp-server-integration]]
- [[concepts/tool-boundaries]]
- [[entities/claude-desktop]]

### Token reduction benchmark

If `total_words` in `graphify-out/.graphify_detect.json` exceeds 5,000, run:

`graphify benchmark`

Behavioral guidance:

- Print benchmark output directly in chat.
- If the corpus is 5,000 words or fewer, skip silently.
- The rationale given is that for small corpora, the graph's value is structural clarity rather than token compression.

This provides an explicit threshold for when graph compression analysis is worthwhile.

Related concepts:
- [[concepts/knowledge-graph-analysis]]

## Overall significance

This document is an operations reference for optional Graphify outputs and integrations. Its main contribution is specifying when each export or service mode should run, what defaults and constraints apply, and how graph artifacts can be routed into [[concepts/llm-wiki]], graph database export, visualization formats, and [[concepts/mcp-server-integration]] workflows.

## Related Concepts
- [[concepts/action-oriented-documentation]]
- [[concepts/progressive-disclosure]]

## Entities
- [[entities/graphify]]
