---
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/README-md.md"]
type: "Work"
description: "Repository pattern for making codebases agent-ready with layered knowledge."
---

# Agent-Ready Repositories

Agent-ready repositories are codebases transformed to give agents three distinct surfaces: orientation, durable context, and repeatable actions. The README for [[entities/agent-smith]] presents this as the central outcome of the project: a normal repository becomes easier for agents to enter, understand, and operate because important knowledge is compiled into an interlinked wiki instead of being re-derived from raw files every session.

## What It Is

An agent-ready repository is organized so different kinds of knowledge stay in separate places:

- `AGENTS.md` provides orientation, repository rules, setup, and operational basics
- `okf/wiki/` stores durable context compiled from source material
- `.agents/skills/` contains reusable actions and workflows
- harness-specific adapters are generated only for the active runtime

This separation reflects [[concepts/context-action-separation]] and [[concepts/progressive-disclosure]]: agents should load only the surface they need, when they need it. The README also frames the repository as a practical instance of [[concepts/knowledge-layer-separation]] and [[concepts/documentation-architecture]], where each layer has a distinct responsibility and access pattern.

The agent-ready-context skill sharpens that structure further by treating the durable context source of truth as `okf/wiki/`, the OpenKB KB root as `okf/`, and the portable action surface as `.agents/skills/`. It also draws a firm boundary between compiled wiki content, repeatable skills, and root-level orientation so the repository does not drift into a single mixed documentation layer. That aligns this entity with [[concepts/agent-context-layering]], [[concepts/tooling-context-governance]], [[concepts/skill-action-boundary]], and [[concepts/documentation-layer-separation]].

The README adds a more explicit packaging model: the three distributable product skills are `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter`, while `graphify` and `openkb` are vendored toolchain copies pinned into the repo by the transformation pipeline. That distinction reinforces the separation between portable repository capabilities and local implementation dependencies.

## Why It Matters

The repository argues that agents waste effort when they repeatedly rediscover the same codebase state. By compiling knowledge into linked wiki pages, the project aims to preserve conclusions across sessions and improve retrieval, navigation, and multi-hop reasoning. That makes the repository a practical example of [[concepts/durable-context]] and [[concepts/compiled-knowledge-bases]]. The README further ties this to [[concepts/llm-wiki]] and the broader idea of a knowledge compilation pipeline.

The same design also supports [[concepts/agent-ready-context-skill]] and [[concepts/consent-first-workflows]]: the bootstrap process checks prerequisites, explains what it needs, and asks before installing anything or sending repository content to a model. The documentation emphasizes that the system is built around [[concepts/consent-first-tooling]], [[concepts/data-flow-disclosure]], and [[concepts/trust-on-first-use]].

The new README content also makes the maintenance model more explicit: OpenKB owns the compiled wiki, but the repo remains agent-ready only when deterministic source packs, validation, and staged evidence stay aligned. That reinforces [[concepts/source-pack-staging]], [[concepts/deterministic-validation]], [[concepts/evidence-staging]], and [[concepts/read-only-kb-operations]].

## OpenKB Lifecycle

The lifecycle reference for this repository's OKF maintenance makes the agent-ready pattern more operational. It treats OpenKB as the semantic engine for the KB lifecycle and describes how repositories should be compiled, validated, and repaired over time.

A key rule is to read first: run `openkb status` and `openkb list`, then inspect `okf/wiki/index.md` and relevant summary, concept, or entity pages before changing anything. That reinforces [[concepts/wiki-content-as-untrusted-data]], [[concepts/knowledge-base-navigation]], and [[concepts/preflight-checks]].

The lifecycle also defines the standard mutation flow:

- stage deterministic sources under `okf/.okf-build/input/`
- ingest them with `openkb add`
- recompile affected pages when structure or order changes matter
- run `openkb lint` as a health report and separate it from pass/fail validation
- use removal and reconciliation for deleted, moved, or deselected sources

This is a concrete expression of [[concepts/source-pack-staging]], [[concepts/incremental-compilation]], [[concepts/orphan-retraction]], [[concepts/registry-drift]], and [[concepts/hash-registry-coherence]]. The document also emphasizes that OpenKB's compiled wiki is a projection of the source set, so generated content should not be hand-edited.

A major maintenance theme is that findings live in a separate capture-and-promotion loop. Discoveries can be recorded under `okf/wiki/explorations/findings/`, then promoted into the compiled wiki only when they are verified and still matter. That makes the repository an example of [[concepts/findings]], [[concepts/findings-promotion]], and [[concepts/knowledge-graph-feedback-loops]].

The lifecycle reference also adds an important governance boundary: pipeline meta-knowledge belongs in the skills and tooling docs, not in the compiled project wiki. The compiled wiki should reflect repository-domain knowledge, while hand-authored tooling pages remain a separate exception surface. That aligns this entity with [[concepts/tooling-context-governance]], [[concepts/tooling-boundaries]], and [[concepts/wiki-skill-boundaries]].

## Core Components

The README describes three portable skills as the main distributable product for making repositories agent-ready:

- `agent-ready-context` for bootstrapping, validation, OpenKB lifecycle management, and maintenance
- `skill-creator` for converting repeated actions into new skills
- `subagent-profile-adapter` for generating harness-specific profile or subagent adapters

It also distinguishes these from vendored toolchain copies of `graphify` and `openkb`, which are installed as part of the transformation pipeline but are not the product itself. This distinction reinforces [[concepts/skill-vendoring]], [[concepts/tooling-vendoring]], and [[concepts/vendor-skills]].

The new skill file adds a more specific operational contract: `uv` is the required Python toolchain for bundled scripts, `graphify` and `openkb` are optional but supported CLI dependencies, and both must be adopted with their read-only vendor skills before first use. It also treats `scripts/check_prereqs.py`, `scripts/build_okf_source_pack.py`, and `scripts/validate_okf_bundle.py` as the core deterministic gates for keeping the repository agent-ready. That makes the entity also reflect [[concepts/toolchain-pinning]], [[concepts/provenance-aware-tool-installation]], [[concepts/vendor-skill-adoption]], and [[concepts/executable-validation]].

## Workflow Themes

The agent-ready workflow emphasizes:

- consent-first installation and bootstrap steps
- explicit provider and tool routing
- deterministic validation gates
- incremental knowledge regeneration
- deletion and rename reconciliation for stale knowledge
- air-gapped operation when local-only execution is required

These behaviors align with [[concepts/consent-first-tooling]], [[concepts/deterministic-validation]], [[concepts/orphan-retraction]], [[concepts/air-gapped-operation]], and [[concepts/explicit-provider-routing]]. The README also stresses [[concepts/integrity-pinning]], [[concepts/version-pinning]], and [[concepts/preflight-checks]] as part of the bootstrap discipline.

The skill document adds two operational details that matter for workflow design: the repo should never create a parallel wiki outside `okf/wiki/`, and generated files should flow through staged inputs rather than directly into compiled output directories. That pushes this entity toward [[concepts/self-reference-control]], [[concepts/kb-root-staging]], [[concepts/deterministic-builds]], and [[concepts/source-driven-regeneration]].

## Knowledge Governance

The README treats repository knowledge as something that must be curated, validated, and kept bounded. The compiled wiki is meant to stay aligned with the source tree, while tooling-specific guidance is isolated so project concept pages do not depend on harness details. That makes the repository a strong example of [[concepts/knowledge-lifecycle-governance]], [[concepts/tooling-context-governance]], [[concepts/wiki-skill-boundaries]], and [[concepts/tooling-link-policy]].

It also presents the wiki as a governed output of a repository ingestion pipeline: sources are staged, compiled, validated, and reconciled as the repository changes. That connects this entity to [[concepts/repository-ingestion]], [[concepts/repository-transformation-pipelines]], [[concepts/source-grounded-regeneration]], and [[concepts/okf-bundle-validation]].

The new skill makes the boundaries more explicit by naming `okf/raw/`, `okf/wiki/`, `okf/.openkb/`, and `okf/output/` as OpenKB-managed surfaces, with local artifacts and cache-like state kept out of history. That further links the page to [[concepts/local-by-default-tooling]], [[concepts/local-vs-shared-configuration]], [[concepts/local-vs-shared-ignore]], and [[concepts/reserved-wiki-files]].

## Notable Claims

- Agent-ready repositories reduce repeated context reconstruction.
- Interlinked wiki pages outperform flat chunks for reusable agent context.
- Orientation, context, and actions should live on separate surfaces.
- Repository transformation should be consent-first, pinned, and auditable.
- The generated wiki is part of the product, but the portable skills are the distributable core.
- `okf/wiki/` is the durable context source of truth, and generated pages should be refreshed from staged sources rather than patched by hand.
- OpenKB linting, source-pack staging, and deletion reconciliation are part of the normal maintenance loop.

## Related Pages

- [[entities/agent-smith]]
- [[entities/agent-ready-context]]
- [[entities/agent-skills]]
- [[entities/openkb-lifecycle]]
- [[concepts/llm-wiki]]
- [[concepts/durable-context]]
- [[concepts/progressive-disclosure]]
- [[concepts/consent-first-workflows]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/knowledge-lifecycle-governance]]

## Related Documents

- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
