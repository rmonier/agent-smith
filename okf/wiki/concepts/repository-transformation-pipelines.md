---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/README-md.md"]
description: "Pipelines that convert repositories into maintained, agent-ready knowledge systems."
---

# Repository Transformation Pipelines

Repository transformation pipelines are processes that take a normal codebase and progressively turn it into an [[concepts/agent-ready-repositories|agent-ready repository]] with durable context, operational orientation, and reusable actions. In `README.md`, agent-smith presents this as a compilation pipeline: raw files are treated as source material, an interlinked wiki becomes the compiled knowledge base, and the agent acts as the compiler that ingests new material, revises cross-references, and flags contradictions so knowledge compounds instead of evaporating.

## What the Pipeline Does

A transformation pipeline typically assembles three layers:

- `AGENTS.md` for orientation, setup, repository rules, and operational basics
- `okf/wiki/` for durable compiled knowledge, evidence, provenance, and cross-links
- `.agents/skills/` for reusable actions and procedures

This separation reflects [[concepts/context-action-separation]] and [[concepts/knowledge-layer-separation]]: instructions, context, and actions are kept distinct so each can be loaded only when needed. The README also frames this as [[concepts/progressive-disclosure]], where each surface carries only the information appropriate to its role.

## Key Properties

The README emphasizes several properties that define this kind of pipeline:

- [[concepts/progressive-disclosure]] — agents get a small, curated surface instead of the whole repository at once
- [[concepts/durable-context]] — important knowledge is compiled into a wiki rather than left in transient chat history
- [[concepts/incremental-compilation]] — the knowledge base is refreshed as the repository changes
- [[concepts/deterministic-validation]] — generated knowledge is checked with validation gates
- [[concepts/evidence-staging]] — source material is collected and compiled in a controlled way
- [[concepts/orphan-retraction]] — deleted or moved sources are reconciled so stale knowledge is removed
- [[concepts/consent-first-workflows]] — the pipeline pauses before installs or LLM-backed work when approval is needed
- [[concepts/data-flow-disclosure]] — the user is told what will be sent, where, and to which provider before generation begins

The README also treats the pipeline as a consent-aware and security-conscious system, with explicit prerequisite checks, pinned tooling, and manual fallback paths when automation cannot proceed safely.

## How agent-smith Applies It

In `README.md`, agent-smith presents its own pipeline as a self-hosting example. The repository can be made "agent-ready" by running the `agent-ready-context` skill, which checks prerequisites, gathers repository structure, compiles OKF knowledge, and validates the result. The process is designed to work in normal, manual, or air-gapped modes, with explicit provider routing and consent before LLM-backed steps.

The README also describes a maintenance loop: when the repository changes, the pipeline refreshes structural context, rebuilds evidence, reconciles deletions or moves, and revalidates the compiled wiki. This makes the transformation continuous rather than one-time, and ties the workflow to [[concepts/source-driven-regeneration]] and [[concepts/manifest-authoritative-reconciliation]].

A further detail is that the repository distinguishes distributable product skills from vendored toolchain copies. The three product skills are the intended portable output, while pinned `graphify` and `openkb` copies are treated as local toolchain inputs to the transformation process. That distinction reinforces [[concepts/skill-vendoring]] and [[concepts/tooling-vendoring]].

## Why It Matters

Repository transformation pipelines matter because they reduce repeated discovery work across agent sessions. Instead of re-deriving architecture, conventions, and operating rules from raw files every time, agents can rely on a maintained knowledge surface and a small set of validated actions. That improves [[concepts/repository-ingestion]], [[concepts/repository-overview-generation]], and [[concepts/knowledge-base-discovery]], while keeping the process aligned with [[concepts/consent-first-workflows]] and [[concepts/safe-automation]].

The README's larger claim is that repository knowledge should compound. A well-run pipeline turns a repository into something that supports repeated operation, not just one-time analysis, and it does so without collapsing orientation, context, and actions into one undifferentiated file layer.

## Related Ideas

- [[concepts/agent-ready-context-skill]]
- [[concepts/repository-ingestion]]
- [[concepts/source-driven-regeneration]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/okf-workflow-governance]]
- [[concepts/quality-gates]]
- [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]