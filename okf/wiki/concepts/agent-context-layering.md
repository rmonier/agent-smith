---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Ordering repository context into authority layers for agents."
---

# Agent Context Layering

Agent context layering is the practice of organizing repository context into ordered layers so an agent knows what to read first, what each source is for, and how much authority to assign to it. In the `agent-ready-context` skill, the AGENTS.md template, and the README for agent-smith, this layering is a core repository policy: concise orientation lives in `AGENTS.md`, durable repository knowledge lives in `okf/wiki/`, structural discovery comes from Graphify outputs, and repeatable procedures live under `.agents/skills/`.

The concept matters because these layers are treated as different kinds of material with different handling rules. Orientation should stay brief, durable knowledge should be compiled and evidence-backed, structural maps should aid inspection without becoming authority, and actions should remain reusable procedures. The action-vs-context guidance makes this boundary explicit by stating that repeatable procedures belong in skills, durable project understanding belongs in the wiki, and concise operating guidance belongs in `AGENTS.md`. This separation is a practical form of [[concepts/context-action-separation]] within a broader [[concepts/documentation-architecture]].

The updated `agent-ready-context` skill makes the model explicit and operational. It defines the repository's agent surface as three separated responsibilities: skills are actions, the OpenKB-compiled wiki is context, and `AGENTS.md` is orientation. It also names `okf/wiki/` as the durable context source of truth, states that OpenKB owns the `okf/` knowledge base root, and warns against creating a parallel wiki or putting long-form knowledge into `AGENTS.md`. The README adds the same architecture in broader terms by describing `AGENTS.md` as orientation, `okf/wiki/` as durable context, `.agents/skills/` as actions, and harness adapters as runtime-only projections. That turns layering from a documentation preference into a repository policy centered on [[concepts/agent-ready-context]], [[concepts/agent-ready-repositories]], [[concepts/durable-context]], and [[concepts/single-source-of-truth]].

The skill also sharpens the trust model around generation and compilation. It says generated pages should not be written directly into `okf/raw/` or `okf/wiki/`; deterministic input should be staged under `okf/.okf-build/input/` and ingested with OpenKB. It further says weak or wrong wiki pages should be corrected by improving source material and re-ingesting, not by casually patching compiled output. This makes layering part of a disciplined regeneration loop tied to [[concepts/deterministic-source-pack-staging]], [[concepts/source-driven-regeneration]], [[concepts/generated-content-governance]], and [[concepts/caveat-preservation]].

## Core idea

The concept defines a priority order for context sources:

1. `AGENTS.md`
2. `okf/wiki/`
3. Graphify outputs such as `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json`
4. `.agents/skills/`

This ordering helps an agent answer three questions early:

- What are the repository rules, routing notes, and safety constraints?
- Where is the durable knowledge, evidence, and provenance-backed context?
- Which tools or reusable procedures should be used for a task?

By making these layers explicit, the repository reduces ambiguity and lowers the risk that an agent will treat generated maps, background knowledge, compiled wiki output, and action instructions as interchangeable. The skill makes the ordering operational by telling agents to start with repository orientation, then use the compiled wiki as the durable source of truth, then use graph structure to narrow inspection, and only then execute procedural skills.

The AGENTS.md template adds two important refinements. First, it states that `okf/wiki/AGENTS.md` is a conventions manual for the wiki itself, which should be inspected after OpenKB initialization or upgrades and customized only deliberately. Second, it frames the four-layer order as a reusable context map for agent operation, not merely as a suggested reading pattern. These details deepen the connection to [[concepts/agent-ready-repositories]], [[concepts/durable-context]], and [[concepts/tool-boundaries]].

The action-vs-context guidance sharpens this model by distinguishing between context that explains a project and actions that should be executed again. In practice, layering is not only about read order; it is also about choosing the correct home for information so repository knowledge does not drift into automation and automation does not become a substitute for durable context.

## Role of each layer

### `AGENTS.md` as the orientation layer

`AGENTS.md` is the first-stop guide for repository-specific behavior. It contains setup and test commands, safety notes, workflow boundaries, routing guidance, and pointers to the other context sources. Its role is not to hold all durable knowledge, but to direct the agent to the right place and record key operating rules such as toolchain pin records, validation commands, and where the OpenKB bundle lives.

The template makes this role especially clear by describing `AGENTS.md` as an orientation index. It is meant to hold setup and test commands, repo rules, safety notes, and pointers to `okf/wiki/`, `graphify-out/`, and `.agents/skills/`, while human-facing documentation remains in `README.md` and `docs/`. It also records concrete maintenance expectations such as using `uv run` for bundled scripts, validating OKF output with the supplied validator, and documenting pinned knowledge-tool versions and integrity hashes after user review. This ties the layer directly to [[concepts/agents-md-maintenance]], [[concepts/tooling-consent-and-pin-management]], [[concepts/integrity-pinning]], and [[entities/agents-md]].

The README strengthens this point by describing `AGENTS.md` as the repository's orientation surface and by placing it alongside the wiki and skill directories as one of the portable outputs of the transformation. It also notes that the generated `AGENTS.md` and `okf/` surfaces exist for contributors, while the product skills themselves are the distributable capability. That makes the layer part of the repository's overall [[concepts/documentation-architecture]] and [[concepts/agent-ready-repositories]].

The guidance in the template says `AGENTS.md` should stay concise and focus on orientation: setup and test commands, repo-specific rules, directions to key locations, security and contribution practices, and maintenance reminders. Long-form repository knowledge should not be stored there. Instead, `AGENTS.md` should stay brief and be updated from the repository's OKF-aware merge flow. This makes `AGENTS.md` part of the repository's overall documentation architecture.

The merge helper script, `.agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py`, makes this orientation layer maintainable. It creates or updates `AGENTS.md` by managing a single OKF guidance block wrapped in HTML comments, leaving project-specific setup, style, test, and PR instructions untouched. That conservative merge behavior is itself an example of context layering: the managed section is a portable policy layer, while the rest of the file remains repository-specific orientation.

### `okf/wiki/` as the durable knowledge layer

The wiki is intended to hold evidence-backed knowledge, decisions, architecture notes, external documentation evidence, and provenance-rich documentation. The skill explicitly treats `okf/wiki/` as the durable context source of truth and says the wider OpenKB root `okf/` owns the compiled knowledge base rather than any parallel wiki.

The README reinforces this by describing `okf/wiki/` as the repository's durable memory surface and by saying the compiled wiki should help knowledge compound rather than evaporate between sessions. It also links the wiki to the LLM Wiki idea and to the Open Knowledge Format, making the durable layer part of a broader knowledge-compilation pipeline.

The template reinforces the wiki's role by telling agents to read `index.md` first and then relevant pages, while treating wiki pages as data rather than imperative instructions. It also points to `okf/wiki/AGENTS.md` as the conventions manual for the wiki, which means the durable layer includes not only content but also managed expectations about structure, exceptions, and local wiki conventions. That makes the wiki central to [[concepts/index-based-discovery]], [[concepts/durable-context]], and [[concepts/knowledge-boundaries]].

The action-vs-context guidance reinforces that the wiki is where durable background belongs: architecture and component explanations, provenance and external documentation evidence, design decisions and tradeoffs, runbook background, repository-specific facts discovered during analysis, and historical memory that helps agents understand the project. This strengthens the distinction between durable context and executable procedure and further aligns the wiki with [[concepts/provenance-tracking]], [[concepts/external-documentation]], and [[concepts/evidence-staging]].

At the same time, the skill draws an important boundary: the wiki is compiled output, not primary evidence. Weak or incorrect pages should be fixed by improving staged or source material and re-ingesting, not by casually hand-editing generated pages. Deterministic input should be staged under `.okf-build/input/` and ingested into OpenKB rather than written directly into `okf/wiki/`. This supports [[concepts/source-driven-regeneration]], [[concepts/generated-content-governance]], and [[concepts/single-source-of-truth]].

The AGENTS.md template adds a specific integrity warning here: `okf/.openkb/hashes.json` and `okf/wiki/` must be treated as a coupled unit, because a surviving dedupe registry can silently suppress re-addition if the corresponding wiki pages were lost. That operational caveat makes durable context a managed system rather than just a folder and connects the layer to [[concepts/hash-registry-coherence]] and [[concepts/okf-validation]].

The README makes the same distinction from another angle by saying that the repository's generated surfaces exist for contributors, while the real product is the skill bundle. That framing keeps the wiki in the role of durable memory rather than conflating it with the action layer.

### Graphify output as the structural map layer

Graphify outputs help the agent understand repository structure and select files to inspect. They are useful for navigation, discovery, and source-pack building, especially when the workflow needs a structural overview before staged ingestion.

However, the skill reinforces that these outputs are not final authority. They are aids for navigation and discovery rather than substitutes for reading underlying files, validating outputs, or checking compiled knowledge. This use of structure-aware tooling complements [[entities/graphify]] and fits with [[concepts/repository-overview-generation]] and [[concepts/progressive-disclosure]].

Within the layering model, Graphify output occupies a middle position: it is more informative than a simple directory listing, but less authoritative than source-backed wiki content. That intermediate role matters because it keeps structural discovery useful without letting generated maps override durable context or source inspection.

The AGENTS.md template states this role plainly: use `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` to choose files to inspect, not as final authority. It also directs the workflow to run Graphify first when available, which makes the structural map layer a practical precursor to evidence staging and ingestion rather than an endpoint. This aligns the layer with [[concepts/repository-overview-generation]], [[concepts/evidence-staging]], and [[concepts/documentation-source-priority]].

The README gives Graphify a similar status by describing it as a repository-knowledge-graph tool used for structural analysis and by treating it as a vendored dependency, not a core deliverable. That keeps structural analysis inside the context layer without promoting it above the wiki.

The Graphify report itself makes this role concrete. It describes the repository as a graph of 2,755 nodes and 2,673 edges across 301 communities, with the corpus judged large enough for graph structure to add value. It identifies hubs, community clusters, isolated nodes, and low-cohesion areas, but it also notes that no surprising cross-file connections were detected and that all connections stayed within source files. This is useful structural evidence, not final interpretation.

The same report also shows why Graphify belongs below the wiki in the trust order. It highlights 2,069 isolated or weakly connected nodes and several broad, low-cohesion communities such as `Operations Log`, `README.md`, and the aggregate community sections. Those findings are diagnostic signals for further inspection, not conclusions that override source reading. The report therefore supports [[concepts/main-structural-patterns]] and [[concepts/progressive-disclosure]] while still fitting under the authority of durable, evidence-backed context.

### Skills as the action layer

Reusable skills under `.agents/skills/` define repeatable procedures for tasks such as checking prerequisites, merging `AGENTS.md` guidance, building staged source packs, validating an OKF bundle, refreshing repository context, and suggesting new skills from repeated actions.

The action-vs-context reference makes the rule for this layer explicit: create or update a skill when the agent or harness should repeat a procedure. Examples include multi-step command sequences, predictable file generation or transformation, artifact validation, tool or API calls with non-obvious flags, repeated scaffolding patterns, migrations or incident workflows, and project-specific wrappers around vendor skills. In other words, a skill is the right home for executable, reusable behavior rather than explanatory background.

In the updated source set, the `agent-ready-context` skill is the procedural mechanism for making a repository agent-ready. It sets rules for tool usage, consent, staging, compilation, review, validation, and fallback operation. The README describes that skill as the core pipeline and lists its responsibilities, including preflight checks, consent-first bootstrap, deterministic staging, OpenKB lifecycle operations, deletion reconciliation, and zero-LLM fallback. That puts it squarely in the action layer and aligns it with [[concepts/skill-based-automation]], [[concepts/tool-boundaries]], and [[concepts/tooling-consent-and-pin-management]].

The same guidance also clarifies how vendor skills fit into layering: vendor skills installed by a skill manager are read-only, their lock files should be retained when present, and project-specific changes belong only in custom skills under `.agents/skills/`. The workflow further requires vendoring read-only Graphify and OpenKB skills before first CLI use when adopting those tools. That places vendor skill handling within [[concepts/dependency-management]], [[concepts/version-pinning]], [[concepts/integrity-pinning]], and [[concepts/lock-file-examples]] rather than in ad hoc local edits.

The AGENTS.md template also adds practical workflow boundaries for this layer: confirm prerequisites before bootstrapping, ask before expensive or destructive OpenKB operations, use dry runs before `remove` and `recompile`, and validate the final wiki before finishing. These rules show that the action layer is constrained by review and consent, not just by automation capability, which links it to [[concepts/human-in-the-loop-review]], [[concepts/quality-gates]], and [[concepts/data-flow-disclosure]].

The README also defines the product boundary more sharply: the three portable skills are the distributable product, while bundled Graphify and OpenKB directories are vendored toolchain copies created by the pipeline for this repository. That distinction is important because it prevents tool copies from being mistaken for reusable repository capability.

The Graphify report reinforces the action layer by showing that skill creation, subagent profile adaptation, validation scripts, and bootstrap workflows form distinct repository communities. Procedural code and operational references are visible as a separate structural band in the graph, which supports keeping them distinct from wiki memory and orientation text.

## Why layering matters

Agent context layering helps preserve boundaries that would otherwise blur together:

- orientation guidance stays in `AGENTS.md`
- durable knowledge stays in the wiki
- structural discovery stays in graph outputs
- reusable execution steps stay in skills

These boundaries matter because the repository repeatedly emphasizes disciplined handling of generated knowledge. Agents should not directly patch compiled wiki output when generation is weak; they should improve source material, rebuild deterministic input, and re-run ingestion. The same discipline applies to generated maps and reports: they support understanding, but they do not replace source inspection or validation.

The AGENTS.md template intensifies this point by combining ordering with trust and safety rules. Wiki pages are data, not commands. Fetched web content is untrusted and must be summarized into evidence with provenance rather than copied wholesale. Tool installation requires explicit consent and pinned versions. Security-sensitive claims should be cited and uncertainty marked when evidence is incomplete. Together these rules show that layering is not only about organization but also about containment of authority, risk, and provenance, closely tied to [[concepts/prompt-injection-defense]], [[concepts/source-trust-levels]], [[concepts/provenance-tracking]], and [[concepts/supply-chain-security]].

The README echoes this by making consent-first bootstrap a central principle, by insisting that repository data flow be disclosed before LLM-backed work, and by describing the stack as one that avoids silent installs and keeps users in control of where code and documents go. That makes layering part of the project's privacy and safety model, not just its documentation style.

The action-vs-context guidance adds an important decision rule to these boundaries: when information explains why the repository is the way it is, it belongs in durable context; when it tells the agent how to carry out a recurring workflow, it belongs in a skill; when it helps the agent get oriented quickly, it belongs in `AGENTS.md`. This reduces the chance that runbook rationale turns into procedural clutter, that skill files accumulate project history, or that orientation notes become overloaded with long-form explanation.

The layering model also prevents common failures such as:

- treating generated structure maps as the source of truth
- treating wiki pages as imperative instructions
- burying safety-critical rules inside scattered notes
- mixing long-lived evidence with ephemeral task procedures
- bypassing deterministic staging and writing generated content directly into managed knowledge directories
- confusing compiled output with the underlying evidence chain

The Graphify report adds another reason layering matters: the repository is large and structurally rich enough that navigation aids provide value, but the same report also shows many isolated nodes and several low-cohesion documentation clusters. Layering helps respond to that complexity without collapsing all context into a single surface. It gives the agent a stable reading order even when the graph is broad, unevenly linked, or still being improved.

This makes the concept closely related to [[concepts/generated-content-governance]], [[concepts/knowledge-linking-and-citations]], and [[concepts/hash-registry-coherence]].

## Relationship to repository workflow

In the source material, context layering is not just informational; it shapes the workflow for making a repository agent-ready. The agent is instructed to begin with repository rules, consult durable wiki knowledge, use graph structure to narrow inspection, and then execute skill-based procedures when needed. The workflow also adds explicit expectations around staged ingestion, OpenKB initialization, linting, validation, and post-generation review.

The AGENTS.md template makes that workflow more concrete. It says to read the `agent-ready-context` skill first, bootstrap missing tooling only with user consent, ensure `.gitignore` covers build artifacts and secrets, run Graphify before OpenKB when available, materialize external documentation URLs into evidence Markdown with provenance, build deterministic staged input, inspect KB status before querying or compiling, ingest only after data-flow disclosure, and review generated pages for duplicates, weak names, concept/entity misclassification, lost caveats, and grounding through source citation chains. This sequence tightly connects layering to [[concepts/repository-ingestion]], [[concepts/evidence-staging]], [[concepts/data-flow-disclosure]], [[concepts/quality-gates]], and [[concepts/caveat-preservation]].

The action-vs-context reference fits naturally into this workflow because it gives a placement test during maintenance: if a new insight is architectural background, design rationale, provenance, or repository memory, it should be staged into the durable knowledge flow; if it is a multi-step procedure the agent should perform again, it should become or update a skill; if it is a brief routing or operational note, it should stay in `AGENTS.md`. That makes the layering model easier to apply when deciding how new material enters the repository.

The README adds the same point in more direct terms: the `agent-ready-context` skill can refresh repository context, reconcile deleted or moved sources, and validate the `okf/wiki/` bundle. It also documents the air-gapped path, where the repository can still gain a useful context surface even when a local LLM is unavailable. This means the ordering is operational, not merely descriptive.

The repository first establishes orientation and tool boundaries, then prepares deterministic inputs, then compiles knowledge, then reviews and validates the results before relying on them. The layer order also supports graceful fallback: if no LLM provider is configured, the workflow can still produce a zero-LLM wiki skeleton and validate it, preserving the structure of the context surface even in degraded mode. That connects the concept to [[concepts/okf-validation]], [[concepts/deterministic-validation]], [[concepts/graceful-degradation]], and [[concepts/llm-free-knowledge-bootstrap]].

The Graphify report fits into this workflow as a midstream inspection tool rather than a terminal authority. It is explicitly freshness-sensitive, tied to a specific commit, and meant to be updated after code changes. That makes graph output part of an [[concepts/incremental-compilation]] and [[concepts/source-driven-regeneration]] loop: use it to inspect structure, identify hubs and gaps, and guide reading or staging decisions, then return to source-backed knowledge and validation.

## Implications

A repository that uses agent context layering well tends to have:

- clearer boundaries between instruction, evidence, structure, and automation
- better traceability for knowledge-bearing content
- safer agent behavior when generated outputs or external tools are involved
- more consistent onboarding for both humans and agents
- better control over when content leaves the machine and which tools may be installed or used
- cleaner maintenance loops because corrections flow back to sources and staged inputs rather than drifting through hand-edited compiled pages

It is especially useful in repositories that combine generated knowledge systems, code graph tooling, reusable automation patterns, and explicit consent requirements around provider use. The action-vs-context guidance also makes it easier to maintain these systems over time because it provides a stable rule for routing new information into the right layer instead of letting notes, procedures, and background accumulate in the same place.

The README's security section adds another implication: layering supports operational audits. Because setup commands, pin records, validation commands, consent gates, package-index expectations, and exception boundaries are concentrated in the orientation and action layers, an agent can establish what is allowed before it touches knowledge compilation or external sources. That makes layering useful not only for navigation but also for enforcement of [[concepts/tooling-consent-and-pin-management]], [[concepts/minimal-tool-scoping]], and [[concepts/privacy-preserving-tooling]].

The Graphify report adds a practical structural signal: the repository's strongest hubs are lifecycle, provenance, dependency, summary, and validation nodes, while many small nodes remain weakly connected. In a repository like that, layering becomes a control mechanism for attention. It tells an agent which materials deserve first trust, which tools are diagnostic only, and which procedures should be invoked only after context is established. In that sense, layering also supports [[concepts/data-flow-disclosure]] and [[concepts/tooling-context-isolation]].

## See also

- [[concepts/documentation-architecture]]
- [[concepts/durable-context]]
- [[concepts/context-action-separation]]
- [[concepts/documentation-source-priority]]
- [[concepts/knowledge-boundaries]]
- [[concepts/evidence-staging]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/quality-gates]]
- [[concepts/source-driven-regeneration]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/dependency-management]]
- [[concepts/integrity-pinning]]
- [[entities/graphify]]
- [[entities/openkb]]
- [[entities/agents-md]]
- [[summaries/graphify-report]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__skill-creator__references__action-vs-context-md]]
- [[summaries/agents__skills__skill-creator__references__source-attribution-md]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/README-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]