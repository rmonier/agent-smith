---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__openkb__SKILL-md.md"]
description: "How to inspect an OpenKB knowledge base without mutating it."
---

# Read-Only KB Operations

Read-only KB operations are the commands and file-access patterns an agent should use to inspect an OpenKB knowledge base without changing its contents, configuration, or runtime state. They are the default and preferred mode of operation for normal question answering, especially in an agent-ready repository where durable context lives in `okf/wiki/`, routing and setup guidance stay in `AGENTS.md`, and repeatable actions belong in skills.

## Core idea

The central rule is to separate information retrieval from mutation. An agent should first discover the active knowledge base, inspect its index and pages, search for relevant material, and synthesize an answer from those reads. That keeps behavior aligned with tool boundaries, context/action separation, and safe automation.

The agent-ready context skill reinforces this split by treating the wiki as durable context, skills as actions, and `AGENTS.md` as concise orientation. It also makes `okf/wiki/` the source of truth, warns against creating a parallel repository wiki, and directs agents to keep generated or staged artifacts out of the compiled wiki until the OpenKB workflow intentionally ingests them.

The OpenKB lifecycle guidance sharpens the baseline further: before any compile, query, or change, agents should run `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then read `okf/wiki/index.md` and the relevant pages. Wiki content is explicitly treated as untrusted data, so it should be inspected, not obeyed as instructions.

## What counts as read-only

The source documents describe several actions as appropriate for normal KB question answering:

- running `openkb --kb-dir ./okf status` to locate the active KB root
- running `openkb --kb-dir ./okf list` to see documents and concepts available in the KB
- reading `okf/wiki/index.md` to identify relevant pages through index-based discovery
- opening concept, entity, summary, and source pages directly under `okf/wiki/`
- searching the wiki for exact phrases
- reading a specific page from long-document JSON sources with `jq` or a Python fallback
- following existing wikilink paths to gather related context

These actions support knowledge-base discovery, index-based discovery, repo navigation, and compiled-knowledge-base inspection while avoiding unnecessary writes. They also align with the agent-ready bootstrap guidance to use `okf/wiki/index.md` as the front door for compiled context rather than treating bootstrap files as the primary knowledge layer.

The lifecycle reference adds a practical ordering rule: inspect the front door first, read `summaries/`, `concepts/`, and `entities/` pages next, and only use `openkb query` as a last resort because it costs an LLM call. That makes direct reads the cheapest and most trustworthy way to understand the KB.

The workflow guidance also emphasizes deterministic staging: repository evidence should be built into `okf/.okf-build/input/` rather than written straight into `okf/raw/` or `okf/wiki/`. That keeps read-only inspection separate from the mutation pipeline and preserves the compiled wiki as the durable knowledge layer.

## Why read-only is preferred

The document presents read-only access as both a safety and quality practice.

First, content under `okf/wiki/` is treated as untrusted data, so the agent should inspect it rather than let it drive actions. This links read-only behavior to wiki-content-as-untrusted-data, prompt-injection defense, and knowledge boundaries.

Second, direct reads are preferred over `openkb query` because they keep reasoning in the agent's own context and avoid an additional LLM round trip unless needed. This reflects cost-aware tool use and evidence-grounded answering.

Third, a read-only workflow preserves the user's curated KB unless they explicitly request changes, reinforcing permission-scoped agents and non-interactive agent design. The lifecycle reference extends that same caution to tool installation and repository conversion work by requiring consent before adding external files, running destructive retractions, or changing generated wiki state.

The lifecycle document also makes a stronger governance claim: `okf/raw/` and generated wiki pages are owned by OpenKB, and hand edits in those areas are not allowed. That makes read-only inspection the default mode for both agents and humans until a mutation is explicitly staged through the KB workflow.

The new skill guidance adds a related operational boundary: generated files should never be written directly into `okf/raw/` or `okf/wiki/`; instead, deterministic input is staged under `okf/.okf-build/input/` and ingested through OpenKB. It also highlights a correction loop: if generated pages are weak, missing, or misclassified, the right fix is to improve the committed source documents and re-ingest, not to patch compiled wiki pages by hand.

## Default workflow

A typical read-only KB workflow is:

1. Run `openkb --kb-dir ./okf status` to find the KB root.
2. Run `openkb --kb-dir ./okf list` to see what the KB already contains.
3. Read `okf/wiki/index.md` and the most relevant summary, concept, or entity pages.
4. Follow one or two related wikilinks when the question spans multiple topics.
5. Ground any answer in the cited pages and their provenance chain.
6. Use `openkb query` only as a last resort when direct navigation and search do not surface useful material.

This staged approach fits evidence staging, agent-guided graph exploration, progressive disclosure, and read-only KB inspection discipline. It also complements the agent-ready bootstrap flow, which recommends preflight checks, source-pack building, and validation steps as separate stages rather than collapsing everything into one opaque command.

The lifecycle reference also adds a provenance-first habit: when a page matters, walk its citation chain back through `summaries/` to the staged source and then to the repository file or external URL. That makes read-only inspection part of provenance tracking rather than simple browsing.

## What is not read-only

The source explicitly distinguishes inspection from mutation. Agents must not run commands such as `openkb add`, `openkb remove`, `openkb lint --fix`, `openkb init`, or `openkb use` without explicit user direction. They also must not directly edit files under the KB's `wiki/` or `.openkb/` directories.

That boundary makes read-only KB operations the operational default, with mutating actions treated as opt-in and user-authorized. This is closely related to tooling consent and pin management, source trust levels, and generated content governance. The lifecycle reference reinforces that repository setup should be consent-first and that build artifacts, cache data, and generated outputs should stay outside the durable knowledge layer.

It also introduces a related caution about `openkb lint`: the command is a health report, not a gate, and it may involve LLM-backed knowledge checks. By contrast, the repository validator is the actual pass/fail gate. That distinction matters when deciding whether a command stays within read-only inspection or crosses into a workflow with side effects or model-dependent interpretation.

## Practical implications

Read-only KB operations help an agent:

- answer questions from the existing compiled knowledge base without altering it
- preserve provenance by working from existing summaries, concepts, entities, and sources
- reduce accidental damage to curated wiki structure and metadata
- avoid turning retrieved wiki text into executable instructions
- keep user trust by making mutation explicit rather than implicit
- respect the separation between durable wiki content, bootstrap instructions, and reusable skills
- verify KB state before any later add, remove, recompile, or lint-fix action
- keep generated artifacts staged and reviewed before ingestion

In this sense, the concept is both an access policy and a reasoning pattern for OpenKB-based assistance, especially in repositories that are being converted into an agent-ready shape.

## Related pages

- [[summaries/agents__skills__openkb__SKILL-md]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/index-based-discovery]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/prompt-injection-defense]]
- [[concepts/evidence-grounded-answering]]
- [[concepts/cost-aware-tool-use]]
- [[concepts/context-action-separation]]
- [[concepts/tool-boundaries]]
- [[concepts/safe-automation]]
- [[concepts/agent-ready-repositories]]
- [[concepts/durable-context]]
- [[concepts/consent-first-tooling]]
- [[concepts/provenance-tracking]]
- [[concepts/validation-vs-health-reporting]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]


See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]