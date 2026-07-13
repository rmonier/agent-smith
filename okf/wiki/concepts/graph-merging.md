---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md"]
description: "Combining multiple extracted code graphs into one queryable graph."
---

# Graph Merging

Graph merging is the practice of combining multiple extracted code graphs into a single graph so they can be queried together. In the Graphify workflow described in [[summaries/agents__skills__graphify__references__github-and-merge-md]], this is used for both cross-repository analysis and multi-subfolder projects.

## What it does

A merge step takes two or more existing `graph.json` files and produces one consolidated output. This lets downstream queries operate on a unified representation of several codebases or code partitions instead of treating each extraction separately.

## When it is used

### Cross-repository analysis

When several GitHub repositories are involved, each repository is cloned and processed independently first. After each repository has its own extracted graph, those graphs are merged into one combined graph. This supports a single analysis surface across multiple repos while preserving origin information.

### Multi-subfolder projects

When a project is split across local subfolders such as services or platform components, each subfolder can be extracted separately and then merged. This is especially useful when separate runs would otherwise interfere with each other's output locations.

## Important operational details

- Each source graph must already exist before merging; merging is a post-extraction step, not a substitute for extraction.
- In the documented Graphify flow, merged nodes retain a `repo` attribute, which supports filtering by source repository after the merge.
- Once a merged `graphify-out/graph.json` exists, later questions can use it directly as a fast path for querying without repeating extraction.
- Merging helps create a shared analysis artifact while still respecting source boundaries inside the graph.

## Why it matters

Graph merging enables broader code understanding than single-repository extraction alone. It is useful for monorepos with separated components, multi-service systems, and workflows that need cross-repo dependency or structure analysis. In practice, it supports [[concepts/knowledge-graph-analysis]] across codebases while pairing naturally with [[concepts/repository-ingestion]] and [[concepts/repo-scoped-graph-partitioning]].

It also reduces repeated work: once individual graphs have been built and merged, the merged artifact becomes a reusable input for future analysis. This aligns with [[concepts/incremental-graph-maintenance]] and [[concepts/idempotent-graph-import]] by encouraging stable graph artifacts that can be reused rather than regenerated unnecessarily.

## Constraints and cautions

A key detail from the source document is that output placement affects whether separate runs can safely coexist. In skill-driven runs, a shared `graphify-out/` in the current working directory can be overwritten by repeated executions across subfolders. The recommended workaround is to run extraction directly on each subfolder so each one gets its own local output before merging. This makes graph merging closely related to [[concepts/tool-boundaries]] and [[concepts/local-vs-shared-configuration]].

## Related pages

- [[summaries/agents__skills__graphify__references__github-and-merge-md]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/repository-ingestion]]
- [[concepts/repo-scoped-graph-partitioning]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/idempotent-graph-import]]
- [[entities/graphify]]

See also: [[summaries/agents__skills__graphify__references__hooks-md]]

See also: [[summaries/agents__skills__graphify__references__update-md]]