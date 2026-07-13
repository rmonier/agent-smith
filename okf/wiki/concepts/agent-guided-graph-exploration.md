---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/graphify-report.md", "summaries/agents__skills__graphify__SKILL-md.md"]
description: "Using an agent to navigate a knowledge graph and explain its structure."
---

# Agent-Guided Graph Exploration

Agent-guided graph exploration is the practice of using an agent not just to build a knowledge graph, but to navigate it with the user: selecting promising questions, traversing relevant nodes and edges, explaining cross-community paths, and turning graph structure into an interactive investigative workflow.

This concept is central to `summaries/agents__skills__graphify__SKILL-md`, where the graph is treated as a persistent map of a repository or mixed-media corpus and the agent is explicitly framed as the guide.

## Core idea

A knowledge graph becomes more useful when a user does not have to inspect raw nodes, edges, and exports manually. In agent-guided exploration, the agent:
- starts from an existing graph when possible instead of rebuilding it
- translates natural-language questions into graph queries
- follows paths, neighborhoods, and community bridges through the graph
- explains why a connection matters in plain language
- cites graph-backed evidence such as source locations when available
- proposes the next worthwhile question to keep exploration moving

This makes graph analysis conversational rather than purely visual or programmatic, and connects [[concepts/knowledge-graph-analysis]] with [[concepts/evidence-grounded-answering]].

## In the graphify workflow

In `summaries/agents__skills__graphify__SKILL-md`, agent-guided exploration appears in several concrete rules.

### Existing graph first

If `graphify-out/graph.json` already exists and the user asks a natural-language question about the corpus, the workflow says to skip rebuild steps and go straight to query execution. This prioritizes reuse of persistent graph state and supports fast investigation over repeated extraction, aligning with [[concepts/incremental-graph-maintenance]] and [[concepts/durable-context]].

### Query as traversal

The query flow is not described as generic chat over a corpus. It is graph traversal over an existing structure, with BFS for broad context and DFS for path tracing. The workflow also requires expanding the user's wording against the graph's own vocabulary before traversal, which ties this concept directly to [[concepts/query-expansion]].

### Graph report as navigation surface

The `graphify-report` document makes the navigational role of the graph explicit. It describes a corpus of 63 files and about 79,281 words, with 472 nodes, 550 edges, and 54 communities, which is large enough that graph structure adds value. It also surfaces:
- community hubs for navigation, including `README.md`, `build_okf_source_pack.py`, `validate_okf_bundle.py`, and `OpenKB repo build workflow`
- god nodes such as `main()`, `detect_orphans()`, `OKF quality and offline conformance baseline`, and `OpenKB lifecycle for OKF maintenance`
- a surprising inferred edge from `build_okf_source_pack.py` to `prune_okf_orphans.py`
- 234 isolated nodes and 9 thin communities that suggest documentation gaps

That report shows agent-guided exploration in a more operational form: the graph is not only a data structure, but a map of where attention should go next.

### Guided follow-up

After building the graph, the agent must surface selected report sections, choose the single most interesting suggested question, and ask whether to trace it. If the user agrees, the agent should walk through:
- which nodes connect
- which community boundaries are crossed
- what the path reveals
- what natural follow-up question the path suggests

This is the clearest expression of agent-guided exploration: the graph is the map, and the agent is responsible for route selection and interpretation.

## Key behaviors

### Turn structure into explanation

The agent should convert graph structure into a user-understandable narrative. Instead of merely returning a node list or shortest path, it explains the significance of bridge nodes, clusters, and surprising links. This supports [[concepts/progressive-disclosure]] by revealing more detail only as the exploration deepens.

### Preserve graph boundaries

The agent is instructed to answer using only what the graph output contains. That keeps exploration grounded in extracted evidence rather than free-form speculation, reinforcing [[concepts/knowledge-boundaries]] and [[concepts/evidence-grounded-answering]].

### Use report outputs as navigation aids

The workflow treats community hubs, god nodes, surprising connections, knowledge gaps, and suggested questions as starting points for exploration rather than final outputs. In this model, analysis artifacts become an interface layer between graph generation and user inquiry.

### Favor continuity across sessions

Because graph data is stored in `graphify-out/`, the same graph can support later questioning without rerunning extraction. This makes exploration persistent and cumulative rather than one-shot, connecting to [[concepts/knowledge-graph-feedback-loops]].

## Why it matters

Without agent guidance, graph outputs can be difficult to use: visualizations can be dense, JSON exports can be technical, and community labels can still leave users unsure where to look. Agent-guided graph exploration solves this by combining:
- graph computation for structure
- report generation for synthesis
- agent interaction for navigation and explanation

It is especially useful in repository analysis, where users ask questions like how a component works, what calls a module, or how data flows across subsystems. In that setting, it complements [[concepts/repo-navigation]] and [[concepts/repository-overview-generation]].

The `graphify-report` adds a further practical insight: graph structure can also reveal documentation quality problems. Large numbers of isolated nodes, weak communities, and unexpected cross-community bridges are not just analysis curiosities; they point toward gaps in [[concepts/documentation-gaps]] and opportunities for [[concepts/documentation-architecture]] improvements.

## Relationship to other concepts

Agent-guided graph exploration overlaps with but is distinct from nearby ideas:
- [[concepts/knowledge-graph-analysis]] focuses on producing graph insights such as communities or central nodes.
- [[concepts/query-expansion]] improves matching between user language and graph vocabulary.
- [[concepts/incremental-graph-maintenance]] keeps the graph current across updates.
- [[concepts/multimodal-knowledge-graphs]] concerns the graph's mixed-media inputs.
- [[concepts/agent-context-layering]] helps explain how persistent artifacts and live interaction can work together.
- [[concepts/cross-community-bridges]] describes the graph edges that make guided navigation especially useful.

What makes this concept distinct is the agent's role after graph construction: not just builder or summarizer, but active guide.

## Practical pattern

A typical agent-guided graph exploration loop looks like this:
1. Reuse an existing graph if available.
2. Interpret the user's question as a graph query.
3. Expand terms to match graph vocabulary.
4. Traverse the graph for relevant paths, hubs, and community bridges.
5. Explain findings in plain language with graph-backed evidence.
6. Offer one compelling next question to continue navigation.

This pattern turns graph infrastructure into a usable exploratory interface.

## Source grounding

The main source for this concept is `summaries/agents__skills__graphify__SKILL-md`, which explicitly says that after building the graph, "The graph is the map. Your job after the pipeline is to be the guide." That line captures the essence of agent-guided graph exploration: graph outputs are not the endpoint; they are the substrate for interactive reasoning with the user.

See also: `summaries/graphify-report`

See also: `summaries/karpathy-llm-wiki-gist`

## Related Documents
- [[summaries/graphify-report]]
