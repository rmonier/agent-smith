---
type: "Concept"
sources: ["summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__exports-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/graphify-report.md"]
description: "Structural analysis of graphs to reveal hubs, communities, gaps, and paths."
---

# Knowledge Graph Analysis

## Definition
Knowledge graph analysis is the use of nodes, edges, clustering, traversal, pathfinding, diagnostics, and exportable graph representations to understand how information is organized across a repository or knowledge system. In practice, it turns files, headings, functions, scripts, named topics, and extracted relationships into a structural map that explains how a project is composed, where its central hubs are, which areas are fragmented or weakly connected, how specific concepts can be explored through graph queries, which downstream tools can deepen inspection, and where the boundary between source material and generated artifacts should be enforced.

## Why it matters
Graph-based analysis becomes useful when a corpus is large enough that linear reading is no longer enough. Instead of treating a repository as a flat list of files, it highlights:
- central navigation hubs
- tightly or loosely connected topic groups
- repeated structural patterns
- isolated material that may need better linking or reorganization
- candidates for refactoring, splitting, or improved indexing
- generated outputs that should be excluded so the graph reflects the repository rather than its derived mirrors
- opportunities to export the structure into other environments for visualization, querying, or database-backed inspection
- graph-grounded query flows that let users ask what is connected, how one concept reaches another, or what a single node means in context
- integrity issues such as dangling edges, collapsed links, empty rebuilds, or stale graphs that could make the graph misleading even when it is technically present
- size-sensitive value, where large corpora justify structural analysis more strongly than small ones

This makes it especially relevant to [[concepts/repo-navigation]], [[concepts/documentation-architecture]], [[concepts/documentation-cohesion]], [[concepts/repository-overview-generation]], [[concepts/knowledge-boundaries]], and [[concepts/graph-structure-analysis]].

## How it works
A knowledge graph analysis typically models a repository as:
- nodes for files, headings, functions, or named topics
- edges for extracted structural or semantic relationships
- communities for clusters of closely related material
- hub nodes for the most connected abstractions
- outliers or isolated nodes for weakly integrated content
- exclusion rules that keep generated or self-referential material out of the graph when those artifacts would distort the structure being measured
- traversal and path queries that turn static structure into inspectable routes, neighborhoods, and explanations
- export paths that let the resulting graph be inspected through graph databases, portable interchange formats, or agent-facing query servers
- integrity checks that surface missing endpoints, self-loops, and edge-collapse problems without pretending the graph is healthier than it is

The analysis becomes more valuable when extraction is deterministic and grounded in the repository itself rather than inferred from guesswork. It becomes more operationally useful when the graph supports both structural reporting and evidence-bounded querying, so the same model can drive manual inspection, shortest-path explanation, local node explanation, live tooling integrations, and incremental rebuilds without changing the extraction baseline. That aligns it with [[concepts/deterministic-validation]], [[concepts/executable-validation]], [[concepts/source-driven-regeneration]], [[concepts/self-reference-control]], and [[concepts/mcp-server-integration]].

## What the source documents show
[[summaries/graphify-report]] provides a concrete example of knowledge graph analysis applied to the `agent-smith` repository. The report describes a graph with 472 nodes and 550 edges across 54 communities, built from a corpus of 63 files and about 79,281 words. It explicitly concludes that the corpus is large enough for graph structure to add value.

The same report identifies several structural signals that are characteristic of good graph analysis:
- major hubs such as `README.md`, `AGENTS.md`, `OpenKB Wiki Schema`, and Graphify command/reference sections act as the main navigation anchors
- highly connected nodes such as `main()`, `detect_orphans()`, `OKF quality and offline conformance baseline`, and `What You Must Do When Invoked` reveal core abstractions and operational surfaces
- multiple communities cluster around validation scripts, OpenKB workflow guidance, skill authoring, and Graphify operations
- low cohesion in large documentation clusters suggests that some documents may be overloaded and could be split into more focused units
- large numbers of isolated nodes and omitted thin communities indicate fragmentation or missing connective structure
- graph usefulness is not limited to static metrics; traversal modes, path queries, and node explanations turn structure into an interactive inspection surface
- graph quality depends not only on extraction but also on excluding generated directories like `okf/` when those outputs are derivative maps of the repository itself
- exported graph artifacts make the analysis reusable across local review, graph databases, and agent-accessible tooling without needing to rebuild the conceptual model
- saved query outcomes and reflection files turn analysis into a feedback loop that preserves preferred sources, dead ends, and corrections over time
- analysis quality depends on preserving graph integrity through empty-graph guards, shrink protection, cache-aware merging, and explicit diagnostic reporting rather than silently overwriting questionable outputs
- multimodal corpora change the analysis surface, because documents, code, images, and transcribed media can all contribute different node and edge types to one graph
- the graph report itself is a navigation map, surfacing not just central hubs but also suggested questions that the graph is uniquely positioned to answer

[[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]] adds an important operational constraint: the compiled OpenKB wiki should be excluded from graph analysis so generated knowledge-base pages do not feed back into the repository graph and get re-ingested as if they were primary structure.

[[summaries/agents__skills__graphify__references__exports-md]] expands the concept from pure analysis into downstream graph use. It shows that once a graph has been built, the same structural model can be exported as wiki output, Cypher for [[entities/neo4j]] or [[entities/falkordb]], SVG, GraphML, or exposed through an MCP server for live graph queries. It also introduces a practical threshold: token-reduction benchmarking is only worth running when corpus size exceeds 5,000 words, because for smaller corpora the graph's main value is structural clarity rather than compression.

[[summaries/agents__skills__graphify__references__query-md]] extends the concept from graph reporting and export into graph interrogation. It defines a strict query workflow that first confirms a graph exists, refreshes prior lessons through `reflect`, extracts the graph's actual vocabulary from node labels, and expands the user query only with tokens already present in that vocabulary. Traversal then runs through either the `graphify` CLI or a deterministic [[entities/networkx]] fallback using breadth-first search for broad neighborhood discovery and depth-first search for chain tracing. The same reference also formalizes shortest-path queries and single-node explanations, and it requires answers to stay bounded by graph evidence, cite source locations when possible, and save useful, failed, or corrected results back into the graph for future sessions.

[[summaries/agents__skills__graphify__SKILL-md]] turns these behaviors into a full operating procedure. It makes knowledge graph analysis a staged pipeline with corpus detection, optional transcription, structural extraction for code, semantic extraction for documents and images, graph merging, community detection, integrity checks, labeling, reporting, export, and cumulative token-cost tracking. It also introduces a fast path for existing graphs: when `graphify-out/graph.json` already exists, natural-language questions should be answered from the graph directly rather than by rebuilding. That framing shifts graph analysis from a one-time report into a persistent inspection layer.

Several practical signals emerge from these sources:
- the graph report built from `agent-smith` is already large enough that graph structure is not decorative but operational
- hubs like `README.md`, `AGENTS.md`, and `OpenKB Wiki Schema` function as navigation anchors and likely deserve cross-linking attention
- the report's 234 isolated nodes point directly to [[concepts/documentation-gaps]]
- the omitted thin communities suggest that some topics may be too small to stand alone and may need consolidation
- graph queries are most useful when they stay vocabulary-grounded and evidence-bounded rather than synonym-driven
- graph quality depends on preserving source-vs-generated boundaries, especially around wiki outputs and other derivative artifacts
- export paths turn a graph from a report into an inspection surface that can be reused in databases, visual tools, or agent workflows
- reflection and saved query results make graph analysis cumulative instead of disposable
- integrity safeguards such as empty-graph guards and shrink protection are part of analysis, not just implementation detail
- multimodal extraction broadens the graph's reach, but provenance and confidence still matter because not all edges are equally certain

These findings connect graph analysis directly to [[concepts/main-structural-patterns]], [[concepts/index-based-discovery]], [[concepts/quality-gates]], [[concepts/generated-content-governance]], [[concepts/idempotent-graph-import]], [[concepts/query-expansion]], [[concepts/evidence-grounded-answering]], [[concepts/knowledge-graph-feedback-loops]], [[concepts/graph-integrity-diagnostics]], [[concepts/graph-merging]], and [[concepts/multimodal-knowledge-graphs]].

## What graph analysis helps reveal
### Structural centers
The most connected nodes often represent the concepts or files that a repository depends on for orientation. In the source report, onboarding documents, validation baselines, and command references function as these centers. This is useful for identifying the true working backbone of a repo, not just its nominal entrypoints.

### Community boundaries
Communities show where documentation and code naturally group together. In the source document, build scripts, validation utilities, OpenKB governance material, and skill-related references form recognizable clusters. This supports decisions about modularization, ownership, and page organization.

### Weak cohesion
A low-cohesion community can indicate that one file is doing too many jobs. In the source report, `README.md` and `What You Must Do When Invoked` are flagged this way. That makes graph analysis a practical tool for spotting where [[concepts/progressive-disclosure]] or document splitting may improve usability.

### Gaps and isolation
Large numbers of isolated nodes suggest missing links, thin coverage, or under-integrated topics. This is especially relevant in systems that rely on durable internal documentation, where weak structural connection can reduce discoverability and trust.

### Queryable neighborhoods and paths
Once a graph exists, analysis can move from passive reporting into active investigation. Breadth-first traversal is useful for asking what a concept is connected to, depth-first traversal helps trace dependency-style chains, shortest-path queries expose the minimal route between named concepts, and node explanation flows summarize everything directly attached to one node. The skill document strengthens this further by making existing-graph querying the default path for natural-language questions, which turns graph analysis into a standing service rather than a rebuild-first workflow.

### Vocabulary mismatch and retrieval failure
Graph analysis also reveals a practical limit: users often ask questions in language that does not exactly match node labels. The query reference addresses this by forcing expansion from the graph's own vocabulary instead of relying on freeform synonym guessing. That makes retrieval auditable and corpus-grounded, and it prevents analysis from silently drifting beyond what the graph can actually support. This is a concrete expression of [[concepts/query-expansion]] and [[concepts/knowledge-boundaries]].

### Self-reference risks
If a repository graph includes generated wiki output that describes the repository itself, the analysis can become recursively contaminated. The graphifyignore template shows that excluding `okf/` is not just a convenience but a method for preserving analytical validity. This is a concrete form of [[concepts/self-reference-control]] and [[concepts/generated-content-governance]], because the graph should model the territory rather than the map derived from it.

### Export-driven inspection
Once the graph exists, analysis does not need to stay inside a single report. The exports reference shows that the same structure can be pushed into graph databases, rendered as visual assets, shared as GraphML, or served to agents over MCP. That extends graph analysis from a one-time diagnostic into a reusable inspection layer that supports manual querying, comparative exploration, and live tool access. It also means export behavior matters: direct database push paths rely on MERGE semantics so repeated loads do not duplicate nodes and edges, preserving interpretability across reruns.

### Reflection-driven improvement
Graph analysis becomes more valuable when it accumulates operational memory. The query workflow's `reflect` step and saved query outcomes preserve preferred starting points, known dead ends, and corrections. This means the graph is not only analyzed once; it is iteratively tuned through use, making future analysis more efficient and less repetitive.

### Integrity and shrink safety
The skill specification adds a stronger operational lesson: graph analysis is only trustworthy when the pipeline refuses unsafe rebuilds. Empty extractions must not clobber a healthy graph, smaller replacement graphs should be rejected unless the shrink is intentional, and diagnostics should report corruption symptoms without hiding them. This turns analysis into a form of monitored graph maintenance as well as interpretation, closely related to [[concepts/graph-integrity-diagnostics]], [[concepts/incremental-graph-maintenance]], and [[concepts/validation-vs-health-reporting]].

### Structural versus semantic layers
The source material also makes clear that graph analysis often combines two different evidence layers: deterministic structural extraction from code and semantic extraction from prose or images. The analysis becomes richer when these layers are merged, but it also becomes more important to preserve provenance and confidence because not all edges are produced the same way. That makes mixed extraction a practical form of [[concepts/llm-free-knowledge-bootstrap]] with optional semantic enrichment rather than a purely model-generated graph.

### Size-sensitive value
The benchmark guidance introduces an important limit signal: graph analysis has different payoffs at different corpus sizes. For large repositories, it can support both structural understanding and token-reduction measurement. For smaller repositories, its value may be mostly organizational rather than compressive. This helps frame graph analysis as a targeted method rather than a universal requirement.

## Practical uses in a repository wiki
In an OpenKB-style wiki or agent-ready repository, knowledge graph analysis can support:
- deciding which files deserve summaries or concept pages
- identifying recurring themes that should become shared concepts
- spotting documentation that should be broken into smaller modules
- improving navigation between source summaries, concepts, and entities
- monitoring whether structure improves over time as content evolves
- validating ignore boundaries so generated wiki artifacts do not distort graph reports
- answering graph-grounded questions through traversal, pathfinding, and node explanation
- preserving successful and failed query patterns so later graph work starts from better priors
- exporting graph structure into databases, visual formats, or MCP-accessible services for deeper querying
- using persistent graph state as a durable analysis layer that can answer questions immediately without rerunning the full build
- checking graph health during updates so a stale, partial, or collapsed graph is recognized before it is trusted

This makes it complementary to [[concepts/llm-wiki]], [[concepts/agent-ready-repositories]], [[concepts/tooling-context-pages]], [[concepts/knowledge-linking-and-citations]], and [[concepts/repository-ingestion]].

## Limits
Knowledge graph analysis is powerful for structure, but it does not replace close reading. A graph can show that material is central, fragmented, weakly linked, reachable through certain paths, reusable through exports, or contaminated by recursive inputs, but it cannot by itself determine whether content is correct, complete, or well written. Querying a graph also does not eliminate the need for retrieval discipline: if the graph lacks the vocabulary or edges needed to answer a question, the right result is to stop or answer narrowly rather than invent support. Exporting a graph into other systems likewise does not improve the underlying extraction quality on its own; it only makes the structural model easier to inspect in different ways. Multimodal extraction and semantic enrichment also increase analytical reach without eliminating uncertainty, so provenance and confidence still matter. It is best treated as a structural diagnostic and inspection layer that informs human review, editing, scope control, and selective downstream tooling.

That means it works well alongside [[concepts/human-in-the-loop-review]] and [[concepts/single-source-of-truth]].

## In this knowledge base
This concept is grounded by [[summaries/graphify-report]], which demonstrates how graph metrics such as hubs, communities, cohesion, and isolated nodes can be used to understand repository structure and identify opportunities to improve organization, linking, and documentation quality. It is further sharpened by [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]], which shows that sound graph analysis also depends on excluding generated knowledge-base output so repository analysis remains structurally meaningful and does not collapse into a self-reinforcing feedback loop. [[summaries/agents__skills__graphify__references__exports-md]] extends the concept by showing that graph analysis can flow directly into wiki generation, graph database export, visual interchange formats, MCP-based querying, and size-based benchmarking decisions. [[summaries/agents__skills__graphify__references__query-md]] adds the operational query layer: vocabulary-constrained expansion, evidence-bounded traversal, shortest-path explanation, node explanation, and feedback-driven saving of query outcomes back into the graph. [[summaries/agents__skills__graphify__SKILL-md]] adds the full lifecycle view: corpus detection, multimodal extraction, persistent graph state, fast-path querying over existing graphs, labeling, health checks, shrink guards, token accounting, and export orchestration.

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__graphify__references__add-watch-md]]

See also: [[summaries/agents__skills__graphify__references__extraction-spec-md]]

See also: [[summaries/agents__skills__graphify__references__github-and-merge-md]]

See also: [[summaries/agents__skills__graphify__references__hooks-md]]

See also: [[summaries/agents__skills__graphify__references__update-md]]