---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/README-md.md"]
description: "A repository design that gives agents clear orientation, durable knowledge, and reusable actions."
---

# Agent-Ready Repositories

An agent-ready repository organizes its knowledge, procedures, and runtime boundaries so coding agents can operate effectively without repeatedly re-deriving the same understanding. The core idea is to split what an agent needs to know, what it needs to do, and what it needs to inspect into distinct layers with explicit boundaries.

This concept is introduced in [[summaries/README-md]] as the central goal of `agent-smith`: transform an ordinary codebase into a repository that is immediately usable by agents while keeping knowledge durable, workflows reproducible, and tool usage constrained.

## Core structure

Agent-ready repositories typically divide content into three functional surfaces:

- `AGENTS.md` for orientation, repo rules, setup, build, launch, and test basics.
- `okf/wiki/` for durable context, architecture, decisions, provenance, and evidence.
- `.agents/skills/` for repeatable actions, scripts, and procedural automation.

The README frames these as separate surfaces with different responsibilities: orientation, context, actions, and harness-specific runtime projections. That separation reflects [[concepts/context-action-separation]] and [[concepts/documentation-layer-separation]], keeping instructions, knowledge, and executable workflows from collapsing into one another.

## Why it matters

The README argues that agents waste effort when they must repeatedly rediscover repository structure and intent. An agent-ready repository reduces that cost by providing a curated, interlinked knowledge surface that supports [[concepts/progressive-disclosure]] and [[concepts/durable-context]].

That design also improves maintainability:

- New sessions begin with a stable orientation layer instead of raw-file exploration.
- Knowledge compiled into the wiki can persist across sessions.
- Repeatable procedures live in skills rather than being embedded in prose.
- The repository can be refreshed incrementally as sources change.
- Harness-specific details stay in runtime adapters instead of polluting the compiled knowledge base.

## Operational properties

The README ties agent-readiness to several concrete practices:

- Consent-first bootstrapping, with installation requests explained before any change.
- Explicit provider and data-flow disclosure before LLM-backed work.
- Deterministic validation of generated knowledge bundles.
- Fallback paths that still produce useful structure when semantic tooling is unavailable.
- Reconciliation of deleted or moved sources so stale knowledge does not linger.
- Optional air-gapped operation with local-provider routing when the repository must stay on-device.

These properties make agent-ready repositories a form of [[concepts/consent-first-workflows]] and [[concepts/deterministic-validation]] rather than a one-time conversion. They also connect the concept to [[concepts/air-gapped-operation]], [[concepts/data-flow-disclosure]], and [[concepts/explicit-provider-routing]].

## Knowledge model

The README frames the repository transformation as a compilation pipeline:

- Raw repository files are treated as source material.
- OpenKB produces a compiled wiki as the durable knowledge base.
- The agent acts as the compiler that ingests, revises, cross-links, and validates.

That model connects agent-ready repositories to [[concepts/compiled-knowledge-bases]], [[concepts/llm-wiki]], and [[concepts/incremental-compilation]]. It also depends on [[concepts/source-provenance]] and [[concepts/knowledge-linking-and-citations]] so compiled pages remain traceable back to source material.

The README also emphasizes that the repository should be compiled, validated, and refreshed incrementally rather than rebuilt from scratch each time. This makes agent-ready repositories part of a broader [[concepts/repository-transformation-pipelines]] approach.

## Security and control

A repository is only agent-ready when it remains safe to operate on. The README emphasizes:

- No silent installs.
- Pinned and integrity-recorded dependencies.
- Local-first or air-gapped operation when needed.
- Secret hygiene and explicit data handling.
- Untrusted content treated as evidence, not instruction.

These controls align the concept with [[concepts/consent-first-installation]], [[concepts/privacy-preserving-tooling]], [[concepts/air-gapped-operation]], [[concepts/prompt-injection-defense]], [[concepts/integrity-pinning]], and [[concepts/trust-on-first-use]].

## Related repository patterns

Agent-ready repositories usually rely on a broader support stack:

- [[concepts/portable-skill-contract]] for distributing usable skills across repositories.
- [[concepts/knowledge-base-navigation]] for making the wiki easy for agents to traverse.
- [[concepts/managed-document-sections]] for keeping orientation files maintainable.
- [[concepts/manifest-authoritative-reconciliation]] for keeping source truth aligned as files move or disappear.
- [[concepts/context-surface-management]] for separating high-signal context from procedural and orientation content.
- [[concepts/orientation-routing]] for keeping the path from entrypoint to durable knowledge explicit.

Together, these patterns create a repository that is not just documented, but operationally shaped for agents.

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]