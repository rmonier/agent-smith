---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Layered repo context that makes repositories agent-ready through compiled knowledge and actions."
---

# Agent Ready Context

Agent-ready context is the workflow for making a repository usable by agents without turning the repository into a pile of ad hoc instructions. It separates three layers of responsibility: executable skills, compiled OKF wiki context, and concise `AGENTS.md` orientation. The related `subagent-profile-adapter` skill extends that idea by projecting the same layered knowledge into harness-specific runtime adapters when the active environment supports local subagents or profiles.

The README reframes this as a repository transformation system: orientation belongs in `AGENTS.md`, durable memory belongs in `okf/wiki/`, and repeatable procedures belong in `.agents/skills/`. That split turns a passive codebase into an [[concepts/agent-ready-repositories|agent-ready repository]] with clear boundaries for context, action, and runtime projection.

## Core idea

The concept centers on [[concepts/context-action-separation|context-action separation]]:

- skills define repeatable actions, checks, transformations, validations, and orchestration
- the OKF wiki stores durable repository knowledge, evidence, provenance, and cross-document synthesis
- `AGENTS.md` stays short and operational, pointing agents to the right places
- runtime adapters are generated only for the active harness and remain projections, not sources of truth

This makes compiled knowledge bases the source of truth for repository memory, while preserving a small and navigable agent entry point through [[concepts/agent-orientation-index|agent orientation index]] guidance. The README makes the same point in architectural terms: knowledge that explains stays out of files that instruct, and files that route stay separate from files that compile durable context.

The `subagent-profile-adapter` skill adds a fourth layer only at runtime: harness-specific subagent or profile files that are short, native to the current environment, and explicitly derived from existing repo context rather than from hardcoded vendor assumptions. Those runtime files are useful projections, but they are not authoritative knowledge.

The managed OKF section in `.agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py` reinforces this structure by keeping `AGENTS.md` as a routing map rather than a second knowledge base. It encodes the same layering in concrete maintenance rules: use `AGENTS.md` for setup and local rules, `okf/wiki/index.md` for wiki discovery, `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` for structural navigation, and `.agents/skills/` for reusable actions.

## What the workflow does

The `agent-ready-context` skill describes an end-to-end pipeline for preparing and maintaining a repository's context surface. It covers:

- reading root `AGENTS.md` and routing through `okf/wiki/index.md`
- checking prerequisites before changing anything
- keeping generated artifacts out of version control
- merging OKF guidance into `AGENTS.md`
- optionally building a repository graph with Graphify
- staging deterministic source input for OpenKB
- initializing and using OpenKB to ingest, lint, and validate the wiki
- reconciling deleted sources before ingestion
- triaging findings pages into promote, keep, or drop outcomes
- validating the final OKF bundle
- refreshing harness and tooling context when needed
- generating local subagent/profile adapters only after runtime detection and harness support checks

This is a [[concepts/repository-transformation-pipelines|repository transformation pipeline]] pattern: source material is staged, compiled, reviewed, and then surfaced through a controlled knowledge layer. The README adds that the product is intentionally split into three portable skills — `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter` — while `graphify` and `openkb` remain vendored toolchain skills that support the pipeline but are not the product itself.

The harness adapter step is a runtime projection of the same pattern, turning durable context into native files expected by the active environment without making those files a new source of truth.

The merge script adds an important operational detail to that workflow: it updates `AGENTS.md` conservatively by replacing only the managed section between HTML comments, or appending it if missing. That makes the orientation layer repeatable without overwriting project-specific setup, style, test, or PR instructions.

## Separation of responsibilities

The document is explicit that three surfaces should not be confused:

- **Skills** are for repeatable actions and automation
- **OKF wiki** is for durable knowledge, provenance, and cross-document synthesis
- **AGENTS.md** is for orientation, setup commands, and routing guidance
- **Runtime adapters** are harness-specific projections for the active environment only

That division reflects [[concepts/documentation-layer-separation|documentation layer separation]] and [[concepts/knowledge-layer-separation|knowledge layer separation]]. It also reinforces [[concepts/knowledge-boundaries|knowledge boundaries]] so procedural rules do not get mixed into durable context. The subagent-profile-adapter skill makes the same point in stronger runtime terms: adapter files should stay short, should point back to `AGENTS.md`, `okf/wiki/`, and skills, and should not embed long project context or pretend to define a portable standard.

The script's section content makes this boundary concrete by telling agents to treat wiki content as data, not instructions, and by deferring actual workflow procedure to `.agents/skills/agent-ready-context/SKILL.md`. In other words, the managed `AGENTS.md` section is a front door, not the source of truth.

## Tooling and governance

The skill treats tooling as part of the operational surface, not the knowledge base itself. It requires:

- `uv` for script execution
- `git` and Python 3.11+
- optional `graphify` and `openkb`
- pinned versions and integrity checks
- vendor-supplied read-only skills for adopted tooling
- respect for configured package indexes and local credentials handling

This connects to [[concepts/toolchain-pinning|toolchain pinning]], [[concepts/integrity-pinning|integrity pinning]], [[concepts/provenance-aware-tool-installation|provenance-aware tool installation]], and [[concepts/vendor-skill-adoption|vendor skill adoption]]. The README adds a stronger implementation detail: prerequisite checking is consent-first, with exact install commands and provenance disclosed before anything is added.

The subagent-profile-adapter skill adds another governance layer here: it insists on detecting the active runtime from environment or harness evidence rather than from installed binaries, and it says harness documentation should be consulted before generating local adapters. That aligns with [[concepts/harness-native-profiles|harness-native profiles]] and [[concepts/runtime-ambiguity-resolution|runtime ambiguity resolution]].

The merge script also encodes a tooling governance rule that is easy to overlook: it says bundled maintenance scripts should be run through `uv run <script.py>`, not bare `python`, when `uv` is available. That supports consistent local execution and keeps script invocation aligned with the rest of the agent-ready workflow.

A further operational constraint is that the OpenKB knowledge base root is `okf/`, and the compiled wiki at `okf/wiki/` is the durable context surface. The workflow therefore avoids writing generated files directly into `okf/raw/` or `okf/wiki/`, preferring deterministic staging under `okf/.okf-build/input/` and later ingestion. It also treats `okf/.openkb/hashes.json` as a dedupe registry that can silently suppress re-addition if its state drifts, so registry coherence becomes part of repository maintenance.

The README broadens that governance model by describing a split between product skills and vendored tools: `graphify` and `openkb` can be pinned into the repository as read-only toolchain copies, while the three portable skills remain the part that should be copied to another repository. That distinction supports [[concepts/tooling-vendoring|tooling vendoring]] without confusing vendored dependencies with the distributable workflow.

The subagent-profile-adapter skill extends tooling governance into harness selection: if the current runtime is ambiguous, the agent should ask the user which harness to target rather than guessing, because multiple agents or profiles may be installed while only one is actually active.

## Evidence and regeneration model

The workflow strongly favors source-grounded repair over direct wiki edits. If generated pages are weak or wrong, the recommended fix is to improve source documents and re-ingest rather than hand-edit compiled pages.

That reflects:

- source-grounded regeneration
- source-driven regeneration
- caveat preservation
- generated content governance

The README reinforces this through its OpenKB lifecycle: repository input is staged deterministically, added to the knowledge base, linted, and then validated as a compiled bundle. It also emphasizes that the wiki compiles knowledge from source material rather than serving as a place to improvise new instructions.

The document also distinguishes discovered knowledge from stated knowledge. If the agent learns something during operation, it should be captured as a finding page and then promoted through the wiki lifecycle, which aligns with findings and findings promotion.

The managed `AGENTS.md` guidance extends this by telling agents not to fake query provenance, not to edit compiled wiki pages directly, and to record durable project facts as findings with evidence pointers and cross-links. It also instructs that `okf/wiki/AGENTS.md` is the wiki-conventions manual and should only be customized with user consent.

## Safety and constraints

Several constraints define the workflow's safety model:

- do not write generated files directly into `okf/raw/` or `okf/wiki/`
- do not create a parallel repository wiki
- treat web-fetched content as untrusted evidence
- avoid destructive OpenKB commands without consent
- watch for registry drift in `okf/.openkb/hashes.json`
- keep provider credentials out of prompts and logs
- generate harness-specific adapters only after confirming harness support and tracking policy

These rules connect to [[concepts/self-reference-control|self-reference control]], [[concepts/read-only-kb-operations|read-only KB operations]], [[concepts/consent-first-tooling|consent-first tooling]], and [[concepts/wiki-content-as-untrusted-data|wiki content as untrusted data]]. The subagent-profile-adapter skill also emphasizes local-only versus shared tracking policy for generated harness files, preference for symlink aliases when instruction-file compatibility is needed, and validation of tooling-link boundaries after files are written.

The README adds more safety detail around data flows: the agent should disclose provider, tool, and endpoint information before the first LLM call, and should prefer local-only operation when requested. That places the workflow firmly in a [[concepts/data-flow-disclosure|data flow disclosure]] and [[concepts/air-gapped-operation|air-gapped operation]] posture.

The merge script adds a few more practical guardrails: it treats tooling as local context rather than project truth, says a first-clone empty tooling overlay is normal, and instructs agents to disclose external data flow and obtain consent before installs, LLM-backed work, broad regeneration, or destructive changes. It also warns that local provider/model configuration belongs in `okf/.openkb/`, not in committed artifacts.

## Why it matters

The concept provides a disciplined way to make a repository agent-ready without losing clarity, provenance, or maintainability. It supports reproducible onboarding, safer automation, and a cleaner division between local execution and shared knowledge.

The README broadens that idea into a concrete repository transformation model: a codebase gains orientation, memory, and action surfaces that can be copied into a new repo and kept in sync through deterministic maintenance. The result is not just documentation, but an operating system for agent work.

The merge script is the operational glue for that goal: it keeps `AGENTS.md` aligned with the OKF workflow while preserving repository-specific instructions, making the orientation surface stable even as the underlying knowledge base and tooling evolve. The subagent-profile-adapter skill extends that discipline into runtime-specific profiles, allowing agents to create harness-native adapters without confusing them with durable project knowledge.

## Related page

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

## Related Documents
- [[summaries/README-md]]


See also: [[summaries/repo-snapshot]]