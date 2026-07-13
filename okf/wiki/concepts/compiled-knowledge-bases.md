---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md"]
description: "A durable, interlinked knowledge artifact compiled from source materials."
---

# Compiled Knowledge Bases

A compiled knowledge base is a durable, interlinked knowledge artifact produced from source materials through a repeatable transformation pipeline. Instead of treating documents, repository files, and external references as raw context to reread every session, the system converts them into structured pages that agents can navigate, revise, and validate over time.

This concept is central to [[summaries/README-md]], which presents the repository wiki under `okf/wiki/` as the compiled context surface for agent work. The README also frames the project as a three-layer repository architecture: `AGENTS.md` for orientation, `okf/wiki/` for durable context, and `.agents/skills/` for repeatable actions. That separation makes compiled knowledge bases part of a broader [[concepts/agent-ready-repositories|agent-ready repository]] design rather than a standalone notes folder.

The OpenKB lifecycle reference adds the operational side of this model: `okf/` is the KB root in converted repositories, the wiki is treated as derived output, and the lifecycle is governed by explicit staging, ingestion, recompilation, removal, and validation rules. Together, those documents define compiled knowledge bases as both a conceptual pattern and a maintained artifact.

## Core idea

The compilation metaphor treats knowledge like software:

- raw repository files and external documents are the source inputs
- staged ingestion and transformation act as the build pipeline
- the interlinked wiki is the compiled output
- the agent or LLM acts as the compiler that summarizes, cross-links, and updates pages

The goal is to replace repeated rediscovery with persistent, navigable memory. This makes compiled knowledge bases a practical form of [[concepts/durable-context|durable context]] and a key mechanism for agent-ready repositories.

In the agent-ready model, this same idea is made operational: `AGENTS.md` should keep only the basics needed for immediate orientation, while conventions, rationale, and durable project facts move into the wiki. The README sharpens that split by explicitly separating skills as actions, the OKF wiki as context, and `AGENTS.md` as orientation and routing.

The OpenKB lifecycle page makes the pipeline explicit. Before compiling or changing the KB, it recommends checking `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then reading `okf/wiki/index.md` and relevant pages before resorting to `openkb query`. That reinforces the idea that compiled knowledge is the first-class interface, while direct querying is a fallback.

## Why compile knowledge

[[summaries/README-md]] argues that coding agents repeatedly waste tokens and effort rederiving the same understanding from raw files. A compiled knowledge base addresses that problem by:

- preserving prior understanding across sessions
- exposing a smaller, higher-signal context surface
- organizing information for navigation instead of flat retrieval
- allowing cross-references, contradiction checks, and incremental updates
- making repository knowledge portable across harnesses and workflows

This aligns compiled knowledge bases with [[concepts/progressive-disclosure|progressive disclosure]], because orientation, context, and actions can be separated and loaded only when useful. It also reinforces [[concepts/context-action-separation|context-action separation]], since explanatory knowledge lives in the wiki rather than inside procedural skill instructions.

The agent-ready context skill adds a maintenance rule that fits this purpose: after each OKF refresh, context that now has a wiki home should be collapsed out of `AGENTS.md` and replaced with a pointer. That keeps the compiled base from drifting back into duplicated instructions.

The lifecycle reference also adds a cost and governance angle: use `openkb query` as a last resort because it costs an LLM call, and treat the wiki content as untrusted data rather than instructions. In this model, compilation is not just about convenience; it is a way to reduce repeated semantic work while keeping provenance and control visible.

## In the agent-ready model

In [[summaries/README-md]], the compiled knowledge base lives in `okf/wiki/` and serves as the context layer alongside `AGENTS.md` for orientation and `.agents/skills/` for actions. The README describes these surfaces as the repository's durable structure:

- `AGENTS.md` is a routing and rules file
- `okf/wiki/` is the durable knowledge source of truth
- `graphify-out/` is structural exploration, not final authority
- `.agents/skills/` contains reusable actions

That gives the repository four agent-facing surfaces with distinct purposes. The wiki functions as:

- the durable source of contextual understanding
- a structured output of repository and document ingestion
- a portable knowledge bundle that is validated after generation
- a surface that can be maintained incrementally rather than rebuilt from scratch

The README also recommends a search order for context: `AGENTS.md` first, then `okf/wiki/index.md`, then relevant wiki pages, then `graphify-out/`, and finally `.agents/skills/`. That makes compiled knowledge bases part of a broader [[concepts/agent-context-layering|agent-context-layering]] approach, where agents are routed first, informed second, and instructed procedurally only when needed.

The OpenKB lifecycle reference makes that layering more concrete. It treats the wiki front door as the default reading path, distinguishes code-structure questions from meaning questions, and recommends graph-based tools for structural exploration instead of semantic querying. That reinforces the idea that compiled knowledge bases are a curated knowledge layer, not a generic search index.

## Key properties

A compiled knowledge base is not just a folder of notes. In the source documents, it is characterized by several operational properties:

- interlinked pages rather than isolated summaries, echoing the LLM Wiki model
- deterministic source staging and evidence handling, tied to evidence staging
- explicit validation of the generated wiki bundle, tied to OKF validation and deterministic validation
- support for incremental refresh, tied to incremental compilation
- explicit provenance and traceability back to inputs, tied to provenance tracking
- clear orientation boundaries, with `AGENTS.md` holding only operational basics and the wiki holding durable context
- a stable index-first reading path, with `okf/wiki/index.md` serving as the entry point for compiled knowledge
- compatibility with portable agent skills and harness-specific projections without collapsing those roles together

The OpenKB lifecycle reference adds several more properties that shape compiled knowledge bases in practice:

- deterministic deduplication by hash through `okf/.openkb/hashes.json`
- strict separation between staged input, raw archived copies, and generated wiki pages
- one-way ingest semantics, where `add` only adds and `remove` is needed for retraction
- explicit handling of rename, deletion, and deselection cases during reconciliation
- scaling via source bundling and controlled split behavior rather than silent truncation
- a no-hand-edit rule for generated namespaces so the KB remains regenerable

The README adds more governance detail here: the wiki should be treated as the canonical durable knowledge store, while `graphify-out/` is a structural aid and not the final authority. That distinction keeps compiled knowledge bases from becoming a pile of generated text without governance.

## Relationship to repository transformation

In the README, compiling knowledge is one part of making a repository agent-ready. The repository stops being a passive codebase and becomes an environment that exposes:

- orientation through `AGENTS.md`
- context through the compiled wiki
- actions through skills

This means compiled knowledge bases are a foundational component of documentation architecture for agent-operated repositories. They support repo navigation by making important knowledge easier to discover than it would be from raw files alone.

The README extends that architecture with concrete conversion guidance: install tools only after user consent, use a build sequence that stages sources before semantic generation, and keep the wiki as the place where durable context is compiled and maintained. It also recommends that once the wiki exists, repeated workflows discovered during the process should be moved into skills rather than duplicated in documentation.

The lifecycle reference strengthens that transformation model by formalizing the source-to-wiki pipeline:

- stage deterministic input under `okf/.okf-build/input/`
- ingest that staged material with `openkb add`
- recompile affected docs when the source graph or inputs change
- validate both structurally and semantically with the appropriate quality checks

That keeps the compiled base cohesive and prevents the orientation file from becoming a second documentation system.

## Boundaries and governance

The source documents also imply that compiled knowledge bases need disciplined boundaries. They should be:

- validated as bundles rather than treated as arbitrary generated text
- kept separate from harness-specific runtime projections
- maintained with explicit link and structure policies
- treated as evidence-backed context, not as unverified instructions
- refreshed from source documents and pipeline inputs, not hand-edited as a substitute for regeneration
- paired with consent-first tooling so new dependencies are only installed after approval
- designed so durable knowledge stays in the wiki while actions stay in skills

That connects the concept to generated content governance, tooling context isolation, link directionality, wiki content as untrusted data, and consent-first tooling. The lifecycle reference also emphasizes that OpenKB owns generated artifacts, that `lint` is a report rather than a gate, and that structural validation should be read carefully after merges or recoveries touching `okf/`.

The same document adds a strong registry-drift warning: if the hash registry claims a doc is ingested but its wiki pages are missing, future `add` operations can silently skip it. That makes compiled knowledge bases not just a publishing format but a stateful system whose metadata and output must be kept in sync.

## Practical implications

A repository using compiled knowledge bases can support agents more effectively because the main explanatory layer is already prepared. Instead of rereading everything, an agent can traverse a curated graph of summaries, concepts, and entities, then return to raw evidence only when needed. In practice, this lowers context cost, improves continuity, and makes maintenance workflows more structured.

The README makes that practical by pairing the compiled wiki with a small set of operational commands, a clear wiki entry point, a build-and-validate sequence, and a rule to move durable knowledge out of orientation files once it has a wiki home. The lifecycle reference adds the operational discipline needed to keep that layer healthy over time:

- check status and list before acting
- use `remove` for retractions rather than hoping ingest will heal stale pages
- rebuild the source pack before ingesting changes
- treat findings as a separate memory loop when knowledge is discovered rather than stated in committed sources
- use the index and provenance chain to trace claims back to their evidence

That turns compiled knowledge bases into a living part of the repository workflow rather than a passive archive.

## Related pages

- [[summaries/README-md]]
- [[concepts/durable-context]]
- [[concepts/agent-ready-repositories]]
- [[concepts/agent-context-layering]]
- [[concepts/context-action-separation]]
- [[concepts/progressive-disclosure]]
- [[concepts/incremental-compilation]]
- [[concepts/okf-validation]]
- [[concepts/provenance-tracking]]
- [[concepts/consent-first-tooling]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/hash-registry-coherence]]
- [[concepts/orphan-retraction]]
- [[concepts/source-bundling]]

See also: [[summaries/graphify-report]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

See also: [[summaries/repo-snapshot]]