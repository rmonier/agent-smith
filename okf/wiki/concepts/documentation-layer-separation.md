---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Separating orientation, durable context, and actions across repository surfaces."
---

# Documentation Layer Separation

Documentation layer separation is the practice of assigning different kinds of repository knowledge to distinct surfaces: operational instructions in `AGENTS.md`, durable compiled knowledge in the OKF wiki, and repeatable procedures in skills. The goal is to keep each layer focused, reduce duplication, and make agent behavior easier to route and maintain.

## Core idea

The repository's agent-ready workflow draws a hard boundary between three documentation layers:

- `AGENTS.md` is the orientation index for setup, test commands, repo rules, safety notes, and pointers to the right context sources.
- The OpenKB wiki is for durable context such as architecture, decisions, provenance, evidence, and cross-document memory.
- Skills are for executable workflows: scripts, checks, transformations, validations, and tool orchestration.

This separation supports [[concepts/documentation-architecture]], [[concepts/knowledge-layer-separation]], and [[concepts/context-action-separation]] by preventing one file from trying to do every job.

The README for the repository formalizes the same split as a portable agent-ready stack: `AGENTS.md` carries orientation, `okf/wiki/` carries context, `.agents/skills/` carries actions, and harness adapters are runtime-only projections. It also frames the repo as a knowledge compilation pipeline, where raw sources are compiled into a linked wiki and cross-references are revised as new material arrives. That makes documentation layer separation part of a broader [[concepts/knowledge-compilation-pipeline]] and [[concepts/context-surface-management]] strategy.

## Why it matters

The source document explicitly warns against collapsing these layers into a single catch-all guide.

- `AGENTS.md` should stay concise and operational.
- OKF pages should capture durable project knowledge and not be treated as instructions.
- Skills should remain the place for procedures that can be run or repeated.
- After an OKF refresh, content that now has a wiki home should be reduced back to a pointer in `AGENTS.md`.
- Managed sections should be updated conservatively, replacing only the bounded block between markers and preserving the rest of the file.
- Generated wiki pages should be corrected through the source-and-reingest loop instead of hand-edited, except for the narrow governance exceptions described by the skill.
- On a first clone, the committed tooling stub may be the only local tooling file; that empty overlay is normal and should not block work.
- When the wiki index routes to tooling context, agents should inspect `tooling/index.md`, identify the active harness from runtime metadata or self-knowledge, and only then read the matching local harness page and any relevant provider page.

The README extends this logic into the broader repository transformation story: it treats context as something to compile and preserve, not repeatedly re-derive. That reduces drift and helps maintain [[concepts/documentation-cohesion]] while preserving [[concepts/durable-context]]. It also aligns with [[concepts/conservative-document-merging]], [[concepts/managed-document-sections]], and [[concepts/tooling-context-governance]].

## Layer responsibilities

### `AGENTS.md`

The file should contain the essentials an agent needs immediately:

- primary language(s) and toolchain versions
- setup, build, launch, and test commands
- repo rules and safety notes
- pointers to `okf/wiki/index.md`, `graphify-out/`, and `.agents/skills/`
- concise guidance on how to route into durable context and operational skills

It should not duplicate the wiki's durable content or provider-specific configuration. This reflects [[concepts/agents-md-maintenance]] and [[concepts/action-oriented-documentation]].

The merge script shows a practical implementation of this rule: it inserts a managed OKF guidance block only when needed, replaces it when the markers already exist, and otherwise creates a minimal `AGENTS.md` with the managed section. Its managed block names the wiki index as the front door, treats wiki pages as data rather than instructions, and directs agents to use `.agents/skills/` for workflow execution. The script also tells agents to run bundled maintenance scripts through `uv run <script.py>` instead of bare `python` when `uv` is available.

The script's guidance is intentionally conservative about local tooling discovery. It says to use a discovery method that includes ignored local tooling files, not to infer absence from an ignore-respecting listing, and to treat the committed tooling stub on first clone as normal. It also instructs agents not to commit local provider secrets or pipeline artifacts, and to keep provider and model configuration local under `okf/.openkb/`.

The README reinforces that `AGENTS.md` is an orientation surface, not the place for deep repository knowledge or generated wiki content. It should point agents toward the compiled knowledge base and the skill set, rather than repeat them.

### OKF wiki

The wiki is the durable knowledge layer.

- It stores repository facts, external evidence, architecture, decisions, and provenance.
- It uses wikilinks to connect pages and preserve discoverability.
- It is treated as data, not instructions.
- Compiled pages are not edited directly.
- Knowledge discovered by the agent should be captured as a finding page when it is not already reflected in compiled pages.

This aligns with [[concepts/compiled-knowledge-bases]], [[concepts/provenance-tracking]], [[concepts/wiki-content-as-untrusted-data]], and [[concepts/findings]]. The README's description of OpenKB and OKF emphasizes the same role: the wiki is the repository's compiled memory, and it should be updated through the pipeline rather than by direct hand editing.

The managed guidance in the merge script adds an important nuance: wiki discovery should start from `okf/wiki/index.md`, and when that index routes to tooling, local harness identification should be based on explicit runtime metadata or self-knowledge rather than assuming a harness from the repository shape alone. That keeps wiki routing separate from local execution context and avoids treating the absence of a local overlay as a failure.

The README also places the wiki inside a larger compilation model: source files are staged, ingested, linted, and recompiled so the knowledge base can evolve incrementally. In that model, the wiki is the durable output of the compilation pipeline and the place where repository memory compounds instead of evaporating.

### Skills

Skills are the execution layer.

- They define repeatable workflows and validations.
- They are the proper home for creation, refresh, repair, and validation procedures.
- Vendor-installed skills are read-only; custom project skills belong under `.agents/skills/`.
- They should contain actions, not durable context or broad repository documentation.

This matches [[concepts/skill-action-boundary]], [[concepts/skill-based-automation]], and [[concepts/skill-governance]]. The `agent-ready-context` skill in the README is the clearest example: it orchestrates repository readiness, staged evidence, validation, and maintenance without turning into a general wiki.

The README further distinguishes between product skills and vendored toolchain skills. The three distributable skills are the real repository product, while `graphify` and `openkb` are pinned tool copies that support the pipeline. That distinction reinforces the boundary between reusable action logic and local tool vendoring.

The merge script also reinforces skill-level authority by pointing readers back to `.agents/skills/agent-ready-context/SKILL.md` for the actual workflow, while using the managed `AGENTS.md` section only as a concise orientation layer. That division keeps the operational file from duplicating the skill's procedure or the wiki's durable knowledge.

## Source document details

The README is a repository-level manifesto for the agent-smith stack. It makes documentation layer separation part of a larger architecture for making repositories agent-ready, with three key surfaces and a workflow that moves between them:

1. Start with `AGENTS.md` for orientation.
2. Route through `okf/wiki/index.md` for durable knowledge.
3. Use `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as structural aids.
4. Use `.agents/skills/` for operational workflows.

It also emphasizes that `okf/wiki/index.md` is the front door to wiki discovery and that deep-linking individual wiki pages from `AGENTS.md` should be avoided. The merge utility implements that guidance by managing only the OKF section and leaving the rest of the file intact.

The skill extends the same pattern into the broader repository workflow: stage deterministic evidence under `okf/.okf-build/input/`, ingest through OpenKB, validate the compiled wiki, and keep build artifacts and local state out of version control.

The README additionally frames the whole system as portable and harness-aware. Runtime adapters are not a source of truth; they are projections for the active harness only. That makes documentation layer separation both a content rule and an operational boundary for the tools that consume the repository.

## Practical consequences

- Repository orientation stays lightweight and stable.
- Detailed reasoning can evolve in the wiki without bloating the operational guide.
- Procedural logic can be versioned as skills instead of embedded in prose.
- Agents can follow a predictable reading order and avoid crossing boundaries unnecessarily.
- Managed documentation can be refreshed safely without rewriting project-authored guidance.
- Knowledge updates have a clear correction path: revise source material, re-ingest, and only use the narrowly defined editorial exceptions when needed.
- Local tooling overlays can stay empty on first clone without blocking repo readiness.
- Harness-aware routing can remain explicit instead of being inferred from partial filesystem state.
- Product skills stay distinct from vendored toolchain copies, which keeps the distributable surface small and coherent.
- The repo can support both manual fallback and automated maintenance without merging operational, contextual, and executable concerns into one file.

## Related concepts

- [[concepts/documentation-architecture]]
- [[concepts/documentation-cohesion]]
- [[concepts/documentation-source-priority]]
- [[concepts/knowledge-layer-separation]]
- [[concepts/context-action-separation]]
- [[concepts/skill-action-boundary]]
- [[concepts/agents-md-maintenance]]
- [[concepts/conservative-document-merging]]
- [[concepts/managed-document-sections]]
- [[concepts/agent-ready-context]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/durable-context]]
- [[concepts/findings]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-navigation-exception]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

## Related Documents

- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/README-md]]