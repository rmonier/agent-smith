---
type: "Concept"
sources: ["summaries/graphify-report.md"]
description: "Nodes that connect otherwise separate graph communities."
---

# Cross-Community Bridges

Cross-community bridges are nodes or artifacts that connect otherwise separate clusters in a graph. In a documentation or codebase graph, they matter because they carry navigation, meaning, or maintenance context across topical boundaries instead of staying inside one local module.

## In the graphify report

The `graphify-report` document highlights bridge-like nodes as some of the most important structural signals in the corpus. In particular, `main()` and `bundle_key()` are called out as high-betweenness nodes that link communities together. The report also notes an inferred edge from `build_okf_source_pack.py` to `prune_okf_orphans.py`, which suggests a cross-cutting maintenance relationship worth checking.

The report’s “Suggested Questions” section is built around this idea: when a node spans multiple communities, it may reveal hidden workflow dependencies, shared abstractions, or documentation gaps. That makes bridge analysis useful for [[concepts/graph-structure-analysis]], [[concepts/knowledge-graph-analysis]], and [[concepts/documentation-gaps]].

## Why it matters

- Bridges often identify the real control points in a workflow, not just the most referenced files.
- They help explain how separate documentation areas relate to each other.
- They can expose under-documented dependencies, especially when an inferred edge appears between modules.
- They are useful for deciding when to create broader concept pages versus keeping pages narrowly scoped.

## Common signs

- A node appears in multiple communities or has unusually high betweenness.
- A node connects workflow pages with maintenance or tooling pages.
- A question about one node requires reading several seemingly unrelated areas.
- The graph shows a relationship that is plausible but not directly documented.

## In practice

In the OpenKB corpus, bridge nodes help connect workflow and maintenance concepts such as [[concepts/openkb-build-workflow]], [[concepts/agents-md-maintenance]], and [[concepts/tooling-context-governance]]. They also support navigation across the knowledge base by linking orientation pages to implementation details.

For graph-driven maintenance work, cross-community bridges are one of the clearest indicators of where [[concepts/documentation-architecture]] may need strengthening or where [[concepts/progressive-disclosure]] is already working well.

## Related source

- [[summaries/graphify-report]]