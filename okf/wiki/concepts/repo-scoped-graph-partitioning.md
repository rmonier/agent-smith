---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__github-and-merge-md.md"]
description: "Partitioning merged code graphs by repository origin for targeted analysis."
---

# Repo-Scoped Graph Partitioning

Repo-scoped graph partitioning is the practice of preserving repository origin inside a combined code graph so multiple repositories can be analyzed together without losing the ability to separate them later. It supports cross-repository analysis while keeping each node attributable to its source repository.

## Why it matters

When several repositories are merged into one graph, the result becomes more useful for broad architectural questions, dependency tracing, and shared-pattern discovery. But that value depends on retaining boundaries between repositories. Without origin metadata, a merged graph can blur ownership, make filtering difficult, and reduce confidence in repository-specific conclusions. This makes repo scoping an important companion to [[concepts/graph-merging]] and [[concepts/repository-ingestion]].

## How it works in practice

In the source workflow, each repository is first cloned and processed independently to produce its own `graph.json`. Those per-repo graphs are then merged into one combined graph. The crucial detail is that each node in the merged graph carries a `repo` attribute, which preserves source identity after the merge.

This creates a two-level structure:

- a shared graph for whole-system querying
- per-node repository labels for filtering by origin

That pattern allows one merged artifact to serve both cross-repo and repo-specific questions. It is a practical form of [[concepts/knowledge-graph-analysis]] that avoids collapsing all repositories into an undifferentiated dataset.

## Source-backed details

[[summaries/agents__skills__graphify__references__github-and-merge-md]] describes this pattern in the Graphify workflow for GitHub URLs and multi-repo use cases.

Key implementation details from the source document:

- repositories are cloned into a stable local cache under `~/.graphify/repos/<owner>/<repo>`
- each repository is processed through the normal extraction pipeline before merging
- merged output is created with `graphify merge-graphs`
- each node in the merged graph includes a `repo` attribute
- once the merged graph exists, later questions can query it directly without re-extraction

These details also connect the concept to [[concepts/idempotent-graph-import]] and [[concepts/incremental-graph-maintenance]], because stable clone reuse and persistent merged artifacts reduce repeated work.

## Relationship to local subfolder workflows

The same source document also describes merging graphs from multiple local subfolders. That workflow is related but slightly different: it is driven by output isolation and merge mechanics rather than explicit repository boundaries. In a monorepo or multi-service layout, separate extraction outputs prevent collisions, and the graphs can then be combined. Repo-scoped graph partitioning is most precise when the merged graph preserves origin labels such as `repo`, but the broader idea also aligns with [[concepts/repo-navigation]] and [[concepts/tooling-context-isolation]].

## Benefits

- enables one combined graph for cross-repository exploration
- preserves source attribution for filtering and interpretation
- reduces ambiguity in merged analysis results
- supports reuse of previously extracted per-repo graphs
- makes fast-path querying possible once the merged artifact exists

## Constraints and risks

Repo-scoped partitioning only works well if origin metadata is preserved consistently during merge. If repository labels are missing, inconsistent, or overwritten, the merged graph loses an important boundary. That can weaken traceability and limit the usefulness of the combined artifact. The concept therefore depends on reliable [[concepts/source-provenance]] and clear merge behavior.

## Related concepts

- [[concepts/graph-merging]]
- [[concepts/repository-ingestion]]
- [[concepts/idempotent-graph-import]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/repo-navigation]]
- [[concepts/source-provenance]]
- [[concepts/tooling-context-isolation]]

## See also

- [[summaries/agents__skills__graphify__references__github-and-merge-md]]
- [[entities/graphify]]