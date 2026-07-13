---
type: "Summary"
description: "Graph structure report mapping OpenKB docs, hubs, and gaps for navigation."
doc_type: short
full_text: "sources/graphify-report.md"
---

# Graphify Report

This report is a structural map of the OpenKB corpus, showing how documents, skills, and reference pages connect. It is meant to guide navigation, surface hubs, and highlight weakly connected areas that may need further documentation or consolidation.

## What the report covers
- Corpus size: 63 files and about 79,281 words.
- Graph size: 472 nodes and 550 edges across 54 communities.
- Extraction quality: 100% extracted, with only 1 inferred edge and no ambiguous edges.
- Freshness note: the graph was built from commit `1bd19302`, so it may need regeneration if the repo has moved on.

## Main takeaways
- The corpus is large enough that graph structure adds practical value for discovery and maintenance.
- Several high-centrality nodes act as bridges across communities, especially `main()`, `bundle_key()`, `detect_orphans()`, and `OpenKB lifecycle for OKF maintenance`.
- The graph reveals both strong topical clusters and a large set of isolated or weakly connected nodes, suggesting missing links or under-documented areas.
- The report is especially useful for reasoning about [[concepts/knowledge-base-navigation]], [[concepts/tooling-context-governance]], and [[concepts/wiki-lifecycle-governance]].

## Notable hubs
- `README.md` and `AGENTS.md` anchor broad orientation and workflow guidance.
- `OpenKB quality and offline conformance baseline` and `OpenKB repo build workflow` form core maintenance and validation clusters.
- `Skill Creator`, `Subagent Profile Adapter`, and `Profile adapter authoring` show a dense skill/tooling design area.
- `OpenKB Wiki Schema` is a strong structural concept for how content is organized.
- `graphify reference` communities capture specific usage patterns such as query, add/watch, commit hook integration, and incremental update.

## Structural findings
- `main()` is the strongest bridge node and appears in multiple communities, linking build and skill-maintenance flows.
- `bundle_key()` unexpectedly connects `Skill Creator` and `build_okf_source_pack.py`, which may reflect a shared packaging or identifier path.
- The report flags an inferred edge from `build_okf_source_pack.py` to `prune_okf_orphans.py`, indicating a relationship worth checking in the source.
- No import cycles were detected.

## Knowledge gaps
- The report identifies 234 isolated nodes, including items like `Licensing`, `Script execution convention`, `Workflow`, and `Tooling bootstrap`.
- Nine thin communities are omitted from the report, which means additional local structure exists but was not expanded here.
- The gaps suggest opportunities for more explicit links, better decomposition, or additional concept synthesis around [[concepts/licensing-and-attribution]], [[concepts/runtime-adapter-management]], and tooling bootstrap.

## Suggested questions
- Why does `main()` connect `build_okf_source_pack.py` to `Skill Creator`?
- Why does `bundle_key()` bridge `Skill Creator` and `build_okf_source_pack.py`?
- Should large hubs like `README.md` or `Skill Creator` be split into more focused modules?
- What documentation is missing for the many weakly connected nodes?

## Why it matters
- The report provides a map for prioritizing documentation work, especially around hub pages and orphaned areas.
- It helps identify where [[concepts/documentation-architecture]] is coherent and where it is fragmented.
- It can be used as a guide for future ingestion, concept creation, and entity linking in the wiki.

## Related Concepts
- [[concepts/graph-structure-analysis]]
- [[concepts/cross-community-bridges]]
- [[concepts/documentation-gaps]]
- [[concepts/documentation-cohesion]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/knowledge-graph-feedback-loops]]
- [[concepts/main-structural-patterns]]
- [[concepts/agent-guided-graph-exploration]]
- [[concepts/index-based-discovery]]
- [[concepts/progressive-disclosure]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/graph-integrity-diagnostics]]
- [[concepts/repo-navigation]]

## Entities
- [[entities/graphify-report-agent-smith]]
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/graphify-out-graph-json]]
- [[entities/agent-smith]]
- [[entities/openkb]]
- [[entities/openkb-wiki]]
- [[entities/openkb-cli]]
- [[entities/validate_okf_bundle-py]]
- [[entities/build_okf_source_pack-py]]
- [[entities/prune_okf_orphans-py]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki]]
- [[entities/okf-spec]]
- [[entities/wiki-schema-md]]
- [[entities/readme-md]]
- [[entities/workflow-md]]
