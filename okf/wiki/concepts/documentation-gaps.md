---
type: "Concept"
sources: ["summaries/graphify-report.md"]
description: "Weakly connected or missing documentation that limits discoverability and synthesis."
---

# Documentation Gaps

Documentation gaps are places where a knowledge base has weak connectivity, thin coverage, or missing explanation around important nodes, making it harder to navigate, validate, or synthesize the corpus.

## In the graphify report
The [[summaries/graphify-report]] highlights several signs of documentation gaps:

- 234 isolated nodes with one or zero connections
- 9 thin communities omitted from the main community list
- bridge nodes such as `main()` and `bundle_key()` that connect otherwise separate clusters
- suggested questions that point to likely missing context, especially around build, skill, and workflow boundaries

## What the report reveals
The report is not just a structural snapshot; it is a diagnostic tool for the wiki itself. It shows where the corpus has strong internal organization and where it likely needs more explicit linking or new synthesis pages.

Common gap patterns in the report include:

- isolated implementation pages with little cross-reference
- large hub pages that may be doing too much at once
- inferred edges that hint at real relationships not yet documented clearly
- communities with low cohesion, suggesting mixed concerns or incomplete decomposition

## Why it matters
Documentation gaps affect several higher-level wiki goals:

- [[concepts/knowledge-base-navigation]] becomes harder when pages are disconnected
- [[concepts/documentation-cohesion]] weakens when hubs accumulate unrelated material
- [[concepts/graph-structure-analysis]] helps identify where content is sparse or fragmented
- [[concepts/query-expansion]] becomes more valuable when the graph has blind spots
- [[concepts/knowledge-graph-feedback-loops]] can use these findings to drive better curation

## Practical uses
This concept is useful for:

- prioritizing missing explanations or link additions
- deciding when to create a concept page versus keep a detail in an existing summary
- finding candidate pages for [[concepts/orphan-retraction]] or consolidation
- identifying where a cross-document concept page could unify scattered references

## Relationship to graphify-style analysis
The report uses graph structure to surface gaps rather than relying on manual reading alone. That makes it a good example of [[concepts/agent-guided-graph-exploration]] and [[concepts/incremental-graph-maintenance]] as maintenance aids for the wiki.

In this framing, documentation gaps are not failures to eliminate entirely; they are signals that guide future compilation, linking, and synthesis work.