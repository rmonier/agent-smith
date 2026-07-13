---
sources: ["summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
type: "Work"
description: "Machine-generated repository graph export used for navigation and analysis."
---

# graphify-out/graph.json

`graphify-out/graph.json` is a machine-generated JSON export of the repository graph. It is used as a structural input for graph-based navigation, helping agents identify hubs, communities, and weakly connected areas before deeper wiki or skill work.

## What It Is

This file belongs to the `graphify-out/` output set and provides a structured representation of repository relationships. The paired report in `[[summaries/graphify-report]]` describes it as part of a graph map for the OpenKB corpus, with 472 nodes, 550 edges, and 54 communities. That makes it useful for repository orientation, but not a source of durable authority.

## Key Facts From the Source Document

- It is explicitly named as a source of structural repository context.
- It is paired with `graphify-out/GRAPH_REPORT.md` and the compiled summary `[[summaries/graphify-report]]`.
- It supports navigation by surfacing hubs such as `main()`, `detect_orphans()`, `OpenKB lifecycle for OKF maintenance`, and `OpenKB repo build workflow`.
- It highlights knowledge gaps, including 234 isolated nodes and 9 thin omitted communities.
- It records no import cycles and only one inferred edge, so the graph is mostly explicit.
- It was built from commit `1bd19302`, so freshness depends on the current repository state.

## Related Concepts

- [[concepts/graph-structure-analysis]]
- [[concepts/repo-navigation]]
- [[concepts/index-based-discovery]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/orientation-routing]]
- [[concepts/repository-orientation-indexing]]
- [[concepts/documentation-architecture]]
- [[concepts/documentation-gaps]]
- [[concepts/cross-community-bridges]]

## Related Entities

- [[entities/graphify-out-graph-report-md]]
- [[entities/graphify]]
- [[entities/graphify-report-agent-smith]]
- [[entities/knowledge-catalog]]
- [[entities/okf-wiki-index-md]]
- [[entities/openkb-lifecycle]]
- [[entities/openkb]]
- [[entities/graphify-out-graph-json]]

## Role in the Workflow

The source document frames this file as a support artifact for agent orientation:

1. Read `AGENTS.md` for local rules and repository basics.
2. Read `okf/wiki/index.md` for the compiled wiki front door.
3. Use `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` to narrow down relevant files.
4. Then inspect the applicable skill or wiki page.

That places this file in the repository’s navigation layer rather than the knowledge layer, which aligns with [[concepts/documentation-layer-separation]] and [[concepts/context-action-separation]]. The report also connects it to [[concepts/agent-guided-graph-exploration]] and [[concepts/documentation-cohesion]] through its hub and community analysis.

## Notes

- The entity is a work product, not a person or tool.
- The source document does not describe the file’s internal schema, only its workflow role.
- Its importance comes from helping agents choose what to inspect next without overreaching into compiled truth.
- The report suggests this artifact is most valuable when paired with validation and freshness checks rather than treated as a static map.