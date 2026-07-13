---
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
type: "Work"
description: "Generated graph report used to map repository structure and gaps."
---

# graphify-out/GRAPH_REPORT.md

`graphify-out/GRAPH_REPORT.md` is a generated structural report for the repository. In the context of `merge_agents_md_okf_section.py`, it is treated as a navigation aid for choosing which files to inspect, not as the final source of truth.

## Role in the workflow

This report sits alongside `graphify-out/graph.json` as part of the repo map used by agent-ready-context maintenance. The managed `AGENTS.md` guidance tells agents to consult it after `okf/wiki/index.md` and before diving into repository files.

It also acts as a graph-based exploration map for the OpenKB corpus, summarizing how repository files, maintenance scripts, and guidance pages cluster together. The report is specifically intended to support [[concepts/graph-structure-analysis]], [[concepts/agent-guided-graph-exploration]], and [[concepts/index-based-discovery]].

## Key facts from the source document

- The report covers 63 files and about 79,281 words.
- The graph contains 472 nodes and 550 edges across 54 communities.
- Extraction quality is high: 100% extracted, 0% inferred, and 0% ambiguous, with only 1 inferred edge noted.
- The graph was built from commit `1bd19302`, so freshness should be checked against the current repository state.
- It is one of the canonical graph outputs referenced by the OKF guidance section.
- It helps agents understand repository structure and locate relevant files.
- It is advisory rather than authoritative; the script says to use it to choose files to inspect.
- It belongs to the same structural-analysis layer as [[entities/graphify-out-graph-json]].

## Graph structure observations

- The strongest hubs include `main()`, `detect_orphans()`, `OKF quality and offline conformance baseline`, `What You Must Do When Invoked`, and `OpenKB lifecycle for OKF maintenance`.
- Community clusters emphasize workflow and tooling topics such as `README.md`, `build_okf_source_pack.py`, `validate_okf_bundle.py`, `Skill Creator`, `OpenKB repo build workflow`, and `OpenKB Wiki Schema`.
- The report surfaces a surprising inferred connection from `build_okf_source_pack.py` to `prune_okf_orphans.py`, suggesting a relationship worth checking in source.
- No import cycles were detected.

## Gaps and risks

- The report identifies 234 isolated nodes, which points to possible missing edges or incomplete documentation.
- Nine thin communities are omitted from the summary, so some local structure is intentionally not expanded.
- The graph may be stale if the repository has changed since commit `1bd19302`.
- The report is useful for navigation, but it should not be treated as a substitute for source files or validated wiki pages.

## Related concepts

- [[concepts/graph-structure-analysis]]
- [[concepts/repository-structure-overview]]
- [[concepts/agent-guided-graph-exploration]]
- [[concepts/index-based-discovery]]
- [[concepts/documentation-layer-separation]]
- [[concepts/documentation-gaps]]
- [[concepts/cross-community-bridges]]
- [[concepts/knowledge-graph-analysis]]

## Related entities

- [[entities/merge_agents_md_okf_section-py]]
- [[entities/graphify]]
- [[entities/openkb]]
- [[entities/graphify-out-graph-json]]
- [[entities/graphify-report-agent-smith]]

## Relationship to the source

The script `[[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]` explicitly lists `graphify-out/GRAPH_REPORT.md` as a source for structural mapping. That makes this report part of the orientation path for repository inspection and agent workflow selection.

The new report content reinforces that role by showing the repo as a large, graph-worthy corpus and by highlighting bridge nodes, weakly connected areas, and workflow-centered communities that can guide follow-up reading.

See also: [[summaries/README-md]]

## Related Documents
- [[summaries/graphify-report]]
