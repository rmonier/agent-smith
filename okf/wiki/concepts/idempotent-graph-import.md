---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__exports-md.md"]
description: "Loading graph data safely so repeated runs do not create duplicates."
---

# Idempotent Graph Import

Idempotent graph import is the practice of loading graph data so the same import can be run multiple times without creating duplicate nodes or relationships. In this wiki, the idea appears most directly in [[summaries/agents__skills__graphify__references__exports-md]] as a core property of Graphify's direct database export flows, and it is reinforced by [[summaries/agents__skills__graphify__references__extraction-spec-md]], which defines upstream extraction rules that help repeated graph rebuilds and updates converge on the same graph structure.

## Why it matters

Graph import workflows are often iterative: users regenerate graphs, retry failed loads, refresh a database after source changes, or push updates into a running graph store. Without idempotent behavior, repeated imports can accumulate duplicates and make the graph unreliable.

Idempotent imports support:

- safe reruns after partial failure
- predictable updates during [[concepts/incremental-graph-maintenance]]
- lower operator risk in [[concepts/safe-automation]] workflows
- cleaner behavior in [[concepts/knowledge-graph-analysis]] pipelines

They also depend on upstream graph data being stable enough to match previously imported records. If extraction emits inconsistent IDs or drifting provenance fields, even a duplicate-resistant database write path can still accumulate parallel graph elements that represent the same thing.

## How the source documents frame it

In [[summaries/agents__skills__graphify__references__exports-md]], both Neo4j push and FalkorDB push are described as using `MERGE`. The document explicitly notes that this makes the import safe to re-run without creating duplicates.

The pattern appears in two export modes:

- Neo4j direct push uses `graphify export neo4j --push ...`
- FalkorDB direct push uses `graphify export falkordb --push ...`

In both cases, idempotence is a behavioral guarantee of the generated import statements rather than a separate cleanup step.

[[summaries/agents__skills__graphify__references__extraction-spec-md]] adds the upstream half of the story. It requires deterministic node IDs derived from full repo-relative paths and normalized entity names, forbids chunk-specific suffixes, and requires `source_file` to be copied exactly from the input file list. Those constraints reduce the chance that a re-extraction will manufacture ghost duplicates or orphaned replacements during later import. In other words, the import layer is idempotent because it matches existing graph elements, and the extraction layer is designed to keep those identities stable enough for matching to work.

## Operational implications

An idempotent import strategy changes how users can work with graph databases:

- rerunning an export is a normal maintenance action, not a dangerous one
- retries after connection or credential issues are less risky
- direct push workflows become more practical than one-off bulk loads
- graph refresh can fit into repeatable [[concepts/skill-based-automation]] and [[concepts/tool-boundaries]]

The extraction specification expands those implications beyond the final database write. By standardizing node identity, relation constraints, confidence scoring, and exact source provenance, it makes repeated extraction-plus-import cycles more predictable as a whole. This also complements [[concepts/deterministic-validation]], [[concepts/executable-validation]], and [[concepts/source-provenance]] because repeated runs are easier to reason about when both data generation and data loading avoid drift.

## Neo4j and FalkorDB context

The source document applies the same idempotent-import idea across both [[entities/neo4j]] and [[entities/falkordb]]. That consistency matters because the databases differ operationally:

- Neo4j supports manual Cypher export and direct push
- FalkorDB accepts OpenCypher-style statements, but practical loading is oriented toward direct execution rather than bulk shell import

Despite those differences, both direct push paths preserve the same re-runnable import property. This makes idempotence a cross-backend design choice rather than a database-specific accident, aligning with [[concepts/provider-integration]] and [[concepts/cross-platform-tooling]].

The extraction-spec context shows that backend-agnostic idempotence is not only about using `MERGE` in each database. It also depends on the exporter receiving graph fragments whose identifiers and provenance survive chunking, rebuilds, and incremental updates without accidental variation.

## Relationship to adjacent concepts

Idempotent graph import is closely related to, but distinct from, several other ideas in the wiki:

- [[concepts/incremental-graph-maintenance]] focuses on repeated graph updates over time; idempotent import makes those updates safer.
- [[concepts/safe-automation]] focuses on reducing operational hazards; idempotence removes one common failure mode.
- [[concepts/knowledge-graph-analysis]] depends on graph integrity; duplicate-free loading helps preserve trustworthy structure.
- [[concepts/tool-boundaries]] matters because import safety should be built into the export/import tool behavior, not left to manual operator discipline.
- [[concepts/schema-constrained-extraction]] matters because stable import behavior depends on extraction outputs remaining structurally predictable.
- [[concepts/source-provenance]] matters because exact source-file preservation helps replace or update existing graph elements consistently rather than creating near-duplicates.

## Practical takeaway

When a graph export tool claims imports are safe to re-run, the important implementation detail is whether the load path matches existing graph elements instead of blindly creating new ones. In the Graphify export reference, `MERGE` is the mechanism that delivers this property for direct pushes. In the extraction specification, deterministic IDs, exact `source_file` preservation, and rules against unstable chunk-based identifiers help ensure that the same semantic entity is still recognized as the same entity on the next run.

Taken together, these documents show that idempotent graph import is not only a database-write technique. It is a pipeline property that depends on stable extraction, consistent provenance, and duplicate-resistant loading working together.

## Source

- [[summaries/agents__skills__graphify__references__exports-md]]
- [[summaries/agents__skills__graphify__references__extraction-spec-md]]