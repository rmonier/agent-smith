---
sources: ["summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__exports-md.md"]
type: "Product"
description: "Graph database target used by Graphify for Cypher export and direct loading."
---

# FalkorDB

FalkorDB is a graph database product used by [[entities/graphify]] as an export and direct-load target for generated knowledge graphs. In the Graphify workflow, it appears as an optional destination alongside other graph outputs, letting a built graph move from local artifacts into a running database system.

## Role in the Graphify workflow

- `graphify export falkordb` generates a portable OpenCypher `cypher.txt` artifact for FalkorDB.
- `/graphify <path> --falkordb` is the pipeline flag that requests this FalkorDB export during a full graph build.
- `/graphify <path> --falkordb-push falkordb://localhost:6379` pushes graph data directly into a running FalkorDB instance.
- FalkorDB is part of Graphify's optional export layer rather than its core extraction path; graph construction, clustering, and reporting happen before database export.
- In the skill definition, FalkorDB export sits beside other post-build outputs such as HTML, wiki export, and database targets like [[entities/neo4j]].

This makes FalkorDB part of Graphify's broader [[concepts/knowledge-graph-analysis]] workflow and its database handoff model for persistent graph use.

## Key facts from this document

- FalkorDB is named in the main Graphify skill as a supported export target during the later pipeline stages.
- Graphify can either generate a Cypher artifact for FalkorDB or push directly to a live FalkorDB server.
- The direct push form is exposed in the top-level usage examples, which signals that FalkorDB is a first-class operational target rather than only a downstream reference.
- FalkorDB export is optional and runs only when its flag is present, following Graphify's [[concepts/progressive-disclosure]] approach to non-default outputs.
- Its place in the workflow reinforces Graphify's support for durable graph destinations beyond local JSON and HTML artifacts, aligning with [[concepts/generated-artifact-adoption]].
- Because the main skill delegates detailed export behavior to [[summaries/agents__skills__graphify__references__exports-md]], FalkorDB is treated as part of a modular export subsystem rather than an always-on dependency.

## Relationship to other entities

- [[entities/graphify]] uses FalkorDB as one of its supported graph export and load targets.
- [[entities/neo4j]] is presented as a comparable graph database destination in the same export family.
- FalkorDB appears in the Graphify skill alongside other integration surfaces that move graph data into external systems, which fits the repository's wider emphasis on [[concepts/mcp-server-integration]] and optional downstream tooling.

## Significance

Within these sources, FalkorDB matters as a practical endpoint for graphs produced by [[entities/graphify]]. The updated skill page confirms that FalkorDB is not just a detail in an export reference but an explicitly supported pipeline target with both artifact-generation and direct-push modes. That positions it as part of Graphify's durable export story, where a local graph build can be handed off into a live graph database for further exploration or operational use.

See also: [[summaries/agents__skills__graphify__references__exports-md]], [[summaries/agents__skills__graphify__SKILL-md]], [[summaries/agents__skills__graphify__references__extraction-spec-md]]