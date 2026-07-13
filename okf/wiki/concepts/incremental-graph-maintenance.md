---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/graphify-report.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md"]
description: "Selective graph refreshes that preserve identity, provenance, and queryability."
---

# Incremental Graph Maintenance

Incremental graph maintenance is the practice of keeping a knowledge graph current by reacting to change selectively instead of rebuilding everything from scratch. In the graphify workflow described in [[summaries/agents__skills__graphify__references__add-watch-md]], the system distinguishes between changes that can be processed immediately and changes that require a later semantic refresh. The extraction prompt described in [[summaries/agents__skills__graphify__references__extraction-spec-md]] adds an important constraint to this idea: incremental updates only stay coherent when semantic extraction uses stable IDs, exact source provenance, and a consistent schema. The GitHub clone and merge workflow in [[summaries/agents__skills__graphify__references__github-and-merge-md]] extends the same principle across multiple repositories or local subfolders by treating previously built graph files as reusable maintenance units that can be merged instead of re-extracted together from scratch. The post-commit automation described in [[summaries/agents__skills__graphify__references__hooks-md]] adds another operating mode: maintenance can be triggered automatically after each commit, without a persistent watcher, as long as the workflow remains scoped to changed code files and clearly separates deferred document refreshes. The dedicated update flow in [[summaries/agents__skills__graphify__references__update-md]] sharpens the concept further by showing how incremental maintenance depends on manifest-based change detection, selective re-extraction, deletion-aware pruning, and merge behavior that preserves the existing graph while replacing stale content correctly. The main graphify skill in [[summaries/agents__skills__graphify__SKILL-md]] adds a broader operating model around those update paths: the graph itself is treated as persistent working state, semantic and structural extraction are explicitly separated, cached outputs are reused across runs, and existing `graphify-out/graph.json` can become the default substrate for later codebase questions instead of forcing a fresh build first. The structural report in [[summaries/graphify-report]] reinforces that model by showing a large graph with 442 nodes, 520 edges, and 50 communities, where central hubs such as `main()`, `detect_orphans()`, `names_from_git()`, [[concepts/okf-validation]], and [[concepts/okf-workflow-governance]] act as bridges across workflow, validation, and maintenance clusters.

## Core Idea

The concept centers on update paths that match the kind of input that changed:

- Code-only changes can trigger a fast structural refresh.
- Document, paper, image, or video changes may require semantic reprocessing rather than a structural-only pass.
- Newly ingested remote content should be merged into the existing graph after it is saved.
- Semantic re-extraction must preserve deterministic node identity and exact source path values so replacement and merge behavior can target the existing graph correctly.
- In multi-repository or multi-subfolder setups, each graph can be refreshed independently and then recombined from its own `graph.json` artifact.
- Merged graphs remain maintainable when each node retains repository origin metadata, allowing updates and analysis to stay partition-aware.
- Automatic triggers can come from a file watcher during active editing, from a post-commit hook that runs once per commit, or from an explicit `--update` pass that diffs against a saved manifest.
- Agent-facing repository instructions can make graph refresh part of the default workflow rather than a manually remembered command.
- The persisted `graphify-out/` directory acts as maintenance state, carrying interpreter selection, manifests, caches, labels, and previous graph artifacts forward between runs.
- Incremental upkeep is not only about rebuilding less work; it is also about preserving a queryable graph between refreshes so later answers can come from existing graph state.
- Structural extraction and semantic extraction follow different maintenance rules: code can often be updated deterministically and cheaply, while document-like inputs may need cached or deferred semantic passes.
- Incremental maintenance remains trustworthy only when diagnostics, token accounting, and warning conditions are surfaced instead of hidden during partial refreshes.
- The graph report shows why this matters at scale: a large corpus with many communities benefits from navigation hubs, cross-community bridges, and explicit diagnostics for omitted or isolated nodes.
- The report also identifies 215 isolated nodes and eight thin communities omitted from the main view, which is a concrete reminder that maintenance quality depends on visibility into gaps, not just aggregate graph size.
- High-centrality nodes like `main()`, `detect_orphans()`, `names_from_git()`, [[concepts/okf-validation]], and [[concepts/okf-workflow-governance]] show that maintenance is often organized around orchestration, cleanup, provenance, and validation rather than around one monolithic graph build step.

This makes graph upkeep faster and more practical for active repositories, especially when many edits happen in short bursts or are committed frequently. It aligns with [[concepts/incremental-compilation]], [[concepts/knowledge-graph-analysis]], and [[concepts/safe-automation]]. It also depends on [[concepts/provenance-tracking]], [[concepts/schema-constrained-extraction]], and [[concepts/idempotent-graph-import]] so that selective updates do not accumulate duplicates or drift. In cross-repository cases, it also overlaps with [[concepts/graph-merging]], [[concepts/repo-scoped-graph-partitioning]], and [[concepts/repository-ingestion]]. The AGENTS.md integration aspect also connects this maintenance model to [[concepts/agents-md-maintenance]] and [[concepts/agent-ready-repositories]]. The persistent-graph-query behavior further links the concept to [[concepts/agent-guided-graph-exploration]], because maintenance is valuable partly because it keeps a navigable graph continuously available.

## Fast Path vs Deferred Path

A key pattern in incremental graph maintenance is separating updates by processing cost and dependency:

- For code files, the watcher reruns AST extraction, rebuilds the graph, and reclusters immediately.
- A post-commit hook can perform the same kind of code-focused refresh after `git commit` by detecting changed files from the most recent commit.
- The `--update` flow adds a stricter fast path: when every changed file is recognized as code, graphify can skip semantic extraction entirely, run only AST processing on the changed subset, then merge and continue downstream.
- For docs, papers, images, or videos, the workflow writes a `graphify-out/needs_update` flag or otherwise leaves a clear signal instead of pretending the graph is fully current.
- The deferred path prompts a manual `/graphify --update`, acknowledging that richer semantic extraction may require additional model-driven processing.
- Pure-code corpora can skip the semantic document-extraction prompt entirely, while mixed corpora must preserve a second path for semantic chunk processing.
- Once a merged `graphify-out/graph.json` already exists, later codebase queries can use that graph directly instead of forcing another extraction pass.
- For several repositories or service folders, the fast path can operate on prebuilt per-scope graphs and only rerun extraction where changes actually happened before merging again.
- Video changes introduce an additional gate: raw media should be transcribed first, then the update state should be rewritten so semantic extraction sees transcript documents rather than unreadable media paths.
- If an update contains only deletions, the system can still proceed by creating an empty extraction payload and using merge-time pruning to remove stale graph content.
- The full graphify skill extends the fast-path idea beyond `--update`: if `graphify-out/graph.json` already exists and the user asks a natural-language question, the workflow can skip rebuild steps entirely and answer from the existing graph.
- Deferred work is not just expensive work; it is work whose correctness depends on prior normalization steps such as transcription, cache checks, or schema-constrained semantic extraction.
- The graph report adds another deferred-work clue: thin communities and isolated nodes are not necessarily errors, but they are signals that some maintenance paths or documentation links may deserve later attention.

This distinction reflects a form of [[concepts/progressive-disclosure]] in automation: cheap, deterministic work runs automatically, while more expensive or semantically sensitive work is surfaced clearly for follow-up. It also connects to [[concepts/executable-validation]] and [[concepts/validation-vs-health-reporting]] because the system signals when more work is required rather than silently masking incomplete state. The hook-based workflow sharpens this distinction by showing that incremental maintenance does not require a long-running background process; it can also be event-driven at commit time. The update workflow adds that the deferred path is not just about cost; it is also about making sure non-code inputs are transformed into machine-readable forms before semantic processing. The merge workflow further shows that incremental maintenance can mean reusing existing graph artifacts as queryable state between refreshes. The graphify skill adds another refinement: fast paths can also be cache-based, where unchanged semantic files are treated as maintained state rather than something to be recomputed every run.

## Change Detection and Stability

The source workflow uses a debounce window so that a burst of file writes does not trigger repeated rebuilds. This matters in agentic or parallel editing sessions where multiple files may change nearly at once. The hook-based workflow uses a different trigger strategy: instead of waiting for file activity to settle, it runs once after a commit and scopes work to the files changed in that commit. The `--update` workflow adds a third trigger style: it compares the current corpus against a saved manifest, records added, changed, and deleted files, and rewrites the detection state so downstream steps can run against the right subset while still retaining whole-corpus context where needed. Together, these patterns show that incremental maintenance can be driven by either live filesystem activity, repository history, or manifest diffs, as long as the scope of change is identified reliably. The main graphify skill adds supporting stability rules around this process: interpreter choice is persisted in `graphify-out/.graphify_python`, scan roots are recorded, manifests are relativized to the scan root, and semantic cache hits are separated from uncached files before new extraction is dispatched.

Important stability behaviors include:

- waiting for file activity to settle before triggering maintenance
- reducing redundant graph rebuilds during batch edits
- supporting background monitoring during active development
- using commit-scoped detection to trigger exactly one maintenance pass per commit without requiring a daemon
- using manifest-based detection so explicit update runs can distinguish changed files from deleted ones and avoid unnecessary full re-extraction
- keeping semantic extraction deterministic across chunks by prohibiting chunk-specific suffixes in node IDs
- preserving exact source-path semantics consistently enough that update-time replacement logic matches prior graph entries
- isolating outputs per scanned folder when working across multiple local subfolders, so one maintenance run does not clobber another graph artifact
- preserving repository attribution in merged graphs so later maintenance and filtering can identify the origin of each node
- appending to existing Git hook scripts rather than overwriting them, which keeps automation composable with other repository tooling
- saving the updated manifest after a successful merge so future incremental runs diff against the latest accepted state rather than an older baseline
- showing a graph diff after update so operators can quickly inspect whether node and edge changes match expectations
- persisting semantic cache entries and extracting only uncached document-like files so incremental passes reuse prior semantic work rather than duplicating it
- separating structural and semantic maintenance inputs so code changes do not accidentally trigger whole-corpus semantic rereads
- preserving directed or undirected graph semantics consistently during rebuild and merge so update passes do not silently alter edge meaning
- refusing destructive shrink cases unless explicitly intended, so a bad partial extraction does not overwrite a healthier existing graph artifact
- surfacing graph-health diagnostics such as dangling endpoints, missing endpoints, self-loops, or collapsed edges as visible warnings rather than silent corruption
- using graph structure analysis to identify bridges, omitted thin communities, and knowledge gaps that may indicate missing maintenance coverage

These behaviors make the update loop more robust and fit with [[concepts/agent-ready-repositories]] and [[concepts/skill-based-automation]]. They also show that graph freshness is not just about rerunning jobs quickly; it is about making reruns land on the same identities and provenance boundaries every time. The multi-folder guidance reinforces that output paths are part of maintenance stability too: if intermediate artifacts overwrite one another, incremental workflows lose the scoped state they depend on. The hook guidance adds a further lesson in [[concepts/safe-automation]]: repository automation should cooperate with existing hooks and stay narrow about what it updates automatically. The update guidance adds a parallel lesson in [[concepts/graph-merging]] and [[concepts/link-directionality]]: selective maintenance must preserve deletion semantics, relative path matching, and directed edge structure when recombining new extraction output with an existing graph. The new health-check and shrink-guard behaviors connect this concept closely to [[concepts/graph-integrity-diagnostics]], because stable incremental maintenance depends on detecting graph damage before it becomes accepted state. The graph report also highlights the importance of [[concepts/documentation-gaps]] and [[concepts/cross-community-bridges]]: a maintained graph is only useful if the graph makes missing links and major connectors visible.

## Incremental Maintenance After Ingestion

The same concept also applies when new external material is added through a URL ingest flow. After the resource is fetched and saved into the corpus, the update pipeline runs to merge that new material into the existing graph rather than treating ingestion and graph construction as unrelated steps.

This creates a continuous path from acquisition to graph freshness and relates to [[concepts/repository-ingestion]], [[concepts/web-evidence-ingestion]], and [[concepts/multimodal-url-ingestion]]. In mixed-source corpora, the semantic extractor's schema rules also matter here: new nodes and edges must use the same allowed file types, confidence conventions, and provenance fields as existing graph data, or the incremental merge stops being reliable.

The same ingestion-to-maintenance pattern appears in repository workflows. A GitHub repository can be cloned once, reused on repeat runs, processed into its own graph artifact, and then merged with graphs from other repositories. This turns repository acquisition, scoped extraction, and graph recombination into one incremental lifecycle rather than separate one-off operations. In local project workflows, the same lifecycle can be embedded into repository conventions through AGENTS.md instructions, making post-change graph upkeep part of the normal operating context for agents working in the repo. The update flow adds an important multimodal refinement: when newly added material includes video, transcription becomes part of maintenance rather than a separate concern, because incremental correctness depends on converting those assets into extractable documents before merge. The core graphify skill adds one more lifecycle layer: once ingestion or update has completed, the resulting graph is not just an output artifact but a maintained query surface that later exploration can use directly.

The graph report suggests that this lifecycle also needs active triage of weakly connected regions. Its omitted thin communities and isolated nodes point to places where ingestion or maintenance may have succeeded technically but still left gaps in navigation, provenance, or linking.

## Why It Matters

Incremental graph maintenance helps balance speed, accuracy, and operator clarity:

- it avoids full rebuilds when only a subset of data changed
- it preserves responsiveness for code-heavy workflows
- it supports watch-based, commit-based, and explicit manifest-based automation for structural refreshes
- it exposes when semantic updates are still pending
- it supports ongoing automation without claiming more certainty than the system has earned
- it relies on deterministic IDs and exact provenance to keep selective re-extraction from creating ghost duplicates
- it relies on deletion-aware pruning and replacement-on-re-extract so changed content overwrites stale graph state instead of accumulating beside it
- it benefits from constrained confidence scoring so updated semantic edges remain comparable across runs
- it scales to multi-repository and multi-service codebases by letting each scope maintain its own graph artifact before recombination
- it keeps merged graphs reusable for later queries, reducing repeated extraction work across stable inputs
- it preserves graph semantics during updates by carrying forward hyperedges and respecting directed edge structure when needed
- it becomes easier to operationalize when repository instructions explicitly tell agents to consult and refresh the graph as part of routine work
- it supports cluster-only maintenance when extraction is unnecessary, allowing existing graph structure to be re-clustered and re-reported without replaying earlier pipeline stages
- it preserves durable working context by reusing manifests, caches, labels, interpreter state, and graph artifacts across runs
- it keeps maintenance honest by surfacing token costs, cache boundaries, and graph-health warnings instead of treating partial refreshes as invisible implementation details
- it makes knowledge-graph exploration more practical because the graph can remain continuously queryable between larger rebuilds
- it gives structural reports a practical role: hubs, communities, and knowledge gaps become actionable maintenance signals rather than static analytics
- it turns graph freshness into a governance issue as much as a technical one, because the graph stays useful only when maintenance rules are consistent and visible

In practice, it is a maintenance strategy for living knowledge graphs: update the cheap parts immediately, mark the expensive parts honestly, and keep the graph usable between larger refreshes. The newer extraction, hook, merge, diagnostics, and update rules sharpen that principle by showing that incremental maintenance is not only about when to reprocess, but also about preserving identity, provenance, scope boundaries, graph artifact reuse, cache correctness, integrity checks, and workflow integration when that reprocessing happens.

## See Also

- [[summaries/agents__skills__graphify__references__add-watch-md]]
- [[summaries/agents__skills__graphify__references__extraction-spec-md]]
- [[summaries/agents__skills__graphify__references__github-and-merge-md]]
- [[summaries/agents__skills__graphify__references__hooks-md]]
- [[summaries/agents__skills__graphify__references__update-md]]
- [[summaries/agents__skills__graphify__SKILL-md]]
- [[summaries/graphify-report]]
- [[concepts/incremental-compilation]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/safe-automation]]
- [[concepts/multimodal-url-ingestion]]
- [[concepts/provenance-tracking]]
- [[concepts/schema-constrained-extraction]]
- [[concepts/idempotent-graph-import]]
- [[concepts/graph-merging]]
- [[concepts/repo-scoped-graph-partitioning]]
- [[concepts/repository-ingestion]]
- [[concepts/agents-md-maintenance]]
- [[concepts/link-directionality]]
- [[concepts/transcription-pipeline-design]]
- [[concepts/graph-integrity-diagnostics]]
- [[concepts/agent-guided-graph-exploration]]
- [[concepts/documentation-gaps]]
- [[concepts/cross-community-bridges]]
- [[entities/agents-md]]
- [[entities/graphify]]


See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]