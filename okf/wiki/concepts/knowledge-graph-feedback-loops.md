---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/graphify-report.md", "summaries/agents__skills__graphify__references__query-md.md"]
description: "Workflows where graph use feeds back into graph quality and future retrieval."
---

# Knowledge Graph Feedback Loops

Knowledge graph feedback loops are workflows where graph use generates structured evidence that is written back into the graph or companion artifacts, improving later retrieval, traversal, explanation, and maintenance. The clearest examples in this wiki come from the graphify query workflow and from the broader structural signals surfaced in [[summaries/graphify-report]], where hubs, weak communities, omitted thin communities, and isolated nodes point to places where the graph can be improved over time.

## Core idea

A feedback loop turns graph interaction into graph maintenance. Instead of treating a graph query as a one-off lookup, the system captures the outcome of the session so later sessions can start from better priors. This makes the graph an evolving operational memory rather than a static index.

In practice, the loop has four stages:
1. read the current graph and prior lessons
2. answer a question using graph-bounded evidence
3. save the answer and outcome back into the graph or companion artifacts
4. reuse those saved outcomes to guide future work

This concept connects closely to [[concepts/query-expansion]], [[concepts/evidence-grounded-answering]], [[concepts/confidence-calibration]], [[concepts/incremental-graph-maintenance]], [[concepts/graph-structure-analysis]], and [[concepts/documentation-gaps]].

## How the source document implements the loop

The graphify query workflow describes a feedback loop that is explicit rather than implied. Before graph work begins, the agent refreshes lessons and reads prior guidance about preferred sources, dead ends, and corrections. After answering, the workflow saves the result with the original question, answer text, cited nodes, query type, and an outcome label such as `useful`, `dead_end`, or `corrected`.

That structure means the system does not merely accumulate graph data from source files. It also accumulates experience about how the graph behaves in real use, including which paths were productive and which ones were misleading.

The structural report in [[summaries/graphify-report]] reinforces why this matters. It shows a graph with 472 nodes, 550 edges, and 54 communities, plus 234 isolated nodes and several thin communities omitted from the report. That mix of strong hubs and weakly connected material is exactly the kind of environment where feedback loops help: they surface cross-community bridges, highlight documentation gaps, and guide future traversal toward better-connected evidence.

The report also identifies central bridge nodes such as `main()`, `detect_orphans()`, `names_from_git()`, `OpenKB lifecycle for OKF maintenance`, and `OpenKB repo build workflow`. Those nodes are useful not just as graph landmarks but as feedback targets: they indicate where repeated successful paths, correction history, or missing links are most likely to affect future navigation.

## Why this matters

Without a feedback loop, graph querying can repeat the same mistakes:
- starting from weak nodes
- retrying known dead ends
- missing better vocabulary choices
- reusing flawed explanations

With a feedback loop, each interaction can improve later ones. The source workflow preserves query expansion history inside saved answers, creating an auditable record of how a question was grounded in available graph terms. It also records whether a path was useful, a dead end, or corrected, which helps later sessions avoid wasting effort on known failures.

The graph report adds another layer of value: it exposes structural leverage points and weak spots at scale. High-centrality nodes connect build, validation, skill management, and OpenKB lifecycle material, while omitted thin communities and isolated nodes mark areas where linking, synthesis, or decomposition may be needed. That makes the feedback loop useful not only for answer quality but also for [[concepts/documentation-cohesion]], [[concepts/repository-overview-generation]], [[concepts/repo-scoped-graph-partitioning]], and [[concepts/wikilink-integrity]].

## Main components of a graph feedback loop

### Reflection before action

The workflow starts by refreshing and reading lessons before running queries. This is important because it moves prior experience into the current session context. The graph is not the only memory store; companion reflection artifacts also shape behavior. This resembles [[concepts/durable-context]] and [[concepts/tooling-context-pages]].

### Evidence-bounded answering

The source requires answers to use only what the graph contains and to cite source locations when stating specific facts. This prevents the loop from amplifying unsupported claims. A bad feedback loop can harden hallucinations; an evidence-bounded one reduces that risk. This is why [[concepts/evidence-grounded-answering]] is central here.

### Structured outcome capture

Saving the result is not freeform note taking. The workflow stores:
- the original question
- the full answer
- referenced nodes
- query type
- outcome status
- optional correction text

That structure makes the saved result machine-usable during later updates and reflections. It also supports [[concepts/schema-constrained-extraction]] and [[concepts/provenance-tracking]].

### Graph-health signals as feedback

The structural report expands the feedback loop beyond individual query outcomes. Community cohesion, isolated nodes, omitted thin communities, and surprise cross-community edges all function as health signals. Those signals suggest where to focus future cleanup, where to create new links, and where to split or consolidate documentation.

This makes feedback loops useful not only for answer quality but also for [[concepts/documentation-gaps]], [[concepts/documentation-cohesion]], [[concepts/repository-overview-generation]], and [[concepts/knowledge-graph-analysis]].

### Reuse in later sessions

The loop closes only when saved outcomes affect future work. In the source document, later sessions read lessons that identify preferred sources, dead ends, and corrections. In the graph report, later sessions can also use hub structure, omission lists, and suggested questions to decide where to look next. That is the mechanism that turns stored traces into behavior change.

## Relationship to graph analysis

This concept is not the same as graph traversal. Traversal answers the immediate question; the feedback loop improves how future traversals begin and how their results are interpreted.

For example, the report describes:
- hubs that bridge build, validation, and lifecycle workflows
- communities centered on graphify references, OpenKB, and skill tooling
- isolated nodes and thin communities that likely indicate missing links or undocumented components
- suggested questions that target structural weak points

The feedback loop sits across all of these operations. It is the cross-session learning layer for graph use, not a single traversal algorithm.

## Benefits

- reduces repeated dead-end searches
- preserves successful starting points as preferred sources
- records corrections so known bad answers are not silently reused
- makes query expansion choices inspectable and reusable
- surfaces graph-health signals that support [[concepts/graph-structure-analysis]] and [[concepts/documentation-gaps]]
- strengthens [[concepts/knowledge-boundaries]] by tying later answers to past graph-supported evidence
- helps identify hubs, omitted thin communities, and isolated nodes that need repair or synthesis

## Risks and limits

Feedback loops can degrade quality if bad outputs are saved without controls. The source workflow counters this by requiring graph-only answers, explicit outcomes, and correction handling. Even so, the loop is only as good as the discipline used when labeling outcomes and citing nodes.

Another limit is vocabulary mismatch. The query workflow addresses this through constrained expansion from actual graph terms, but if the graph lacks relevant vocabulary entirely, the correct behavior is to stop rather than fabricate a search. That preserves trust and keeps the loop aligned with [[concepts/knowledge-boundaries]].

A final risk is overfitting to current graph shape. The report shows a graph that is already rich in hubs but still has many isolated nodes. If feedback loops only reinforce existing hubs, they can make the graph easier to traverse without making it more complete. That is why feedback should also inform link creation and documentation repair.

## In this wiki

Knowledge graph feedback loops describe the pattern where graph interactions create reusable graph-facing memory and structural improvement signals. In [[summaries/agents__skills__graphify__references__query-md]], this appears as a deliberate cycle of reflection, evidence-grounded traversal, result capture, and future reuse. In [[summaries/graphify-report]], it also appears as a diagnostic lens on the graph itself: hubs reveal leverage points, weak communities reveal cohesion problems, and isolated nodes reveal where additional linking or synthesis would help.

The concept is especially relevant to systems that want graph querying to become more accurate and efficient over repeated sessions rather than remain stateless.

## Related pages

- [[summaries/agents__skills__graphify__references__query-md]]
- [[summaries/graphify-report]]
- [[concepts/query-expansion]]
- [[concepts/evidence-grounded-answering]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/provenance-tracking]]
- [[concepts/durable-context]]
- [[concepts/tooling-context-pages]]
- [[concepts/confidence-calibration]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/knowledge-boundaries]]
- [[concepts/graph-structure-analysis]]
- [[concepts/documentation-gaps]]
- [[concepts/documentation-cohesion]]
- [[concepts/repository-overview-generation]]
- [[concepts/wikilink-integrity]]

See also: [[summaries/karpathy-llm-wiki-gist]]