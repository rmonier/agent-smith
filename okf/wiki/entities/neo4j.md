---
sources: ["summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__exports-md.md"]
type: "Product"
description: "Graph database product used by graphify as an export and push target."
---

# Neo4j

Neo4j is a graph database product referenced as a supported export and direct-push target in [[summaries/agents__skills__graphify__references__exports-md]] and the main [[summaries/agents__skills__graphify__SKILL-md]] workflow. In these documents, it appears as one of the primary destinations for graph data produced by [[entities/graphify]].

## Role in the document

The documents describe two Neo4j-related workflows:

- `--neo4j` generates `graphify-out/cypher.txt` for Neo4j import.
- `--neo4j-push bolt://localhost:7687` pushes graph data directly to a running Neo4j instance.

In the main skill definition, Neo4j is part of the optional export layer rather than the default build path: Neo4j actions run only when their flags are explicitly requested. This places Neo4j within a broader pattern of [[concepts/knowledge-graph-analysis]], [[concepts/tool-boundaries]], and export-oriented tooling around graph artifacts.

## Key facts from this source

- Neo4j export is available both as file generation and direct database push.
- The skill documents `bolt://localhost:7687` as the example direct-push endpoint.
- Neo4j-related steps are grouped with other optional outputs such as wiki, FalkorDB, SVG, GraphML, and MCP.
- Neo4j export happens after graph extraction, graph building, clustering, analysis, and labeling.
- The generated Cypher output is written under `graphify-out/`, aligning Neo4j with the tool's persistent artifact model.
- Neo4j is treated as an integration endpoint for operationalizing graph output beyond local HTML and JSON deliverables.

These details connect Neo4j to [[concepts/idempotent-graph-import]], [[concepts/generated-artifact-adoption]], [[concepts/incremental-graph-maintenance]], and [[concepts/safe-automation]].

## Relationship to other entities

- [[entities/graphify]] is the tool that produces and exports the graph data.
- [[entities/falkordb]] is presented alongside Neo4j as another graph database export target.
- [[entities/networkx]] underlies the in-memory graph workflows that precede export.

## Relevance

In these sources, Neo4j matters as a practical integration endpoint for taking graph output from [[entities/graphify]] into a live graph database environment. It represents the database-backed branch of the export workflow documented in [[summaries/agents__skills__graphify__references__exports-md]] and surfaced at the top level in [[summaries/agents__skills__graphify__SKILL-md]].

See also: [[summaries/agents__skills__graphify__references__extraction-spec-md]]