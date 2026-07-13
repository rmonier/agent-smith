---
type: "Summary"
description: "Introduces agent-smith, a skill-based pipeline for making repos agent-ready."
doc_type: short
full_text: "sources/README-md.md"
---

# README.md Summary

This README presents **agent-smith**, a repository transformation system that turns a codebase into an **agent-ready** workspace by separating three surfaces: orientation (`AGENTS.md`), durable knowledge (`okf/wiki/`), and repeatable actions (`.agents/skills/`).

## Main Idea

The project is built around the [[concepts/knowledge-compilation-pipeline]] idea from Karpathy's LLM Wiki: treat raw repository content as source material, compile it into an interlinked wiki, and use the LLM as a compiler that updates cross-references, reconciles changes, and preserves conclusions across sessions.

It argues that agents work better with a small, curated, high-signal context surface, and that knowledge should be stored as linked context rather than flat chunks. This supports [[concepts/progressive-disclosure]] and reduces repeated re-derivation of repository understanding.

## Repository Surfaces

The README defines four distinct surfaces:

- `AGENTS.md` for orientation, setup, rules, and toolchain basics
- `okf/wiki/` for compiled OpenKB knowledge and evidence
- `.agents/skills/` for executable agent actions and procedures
- Harness adapters for runtime-specific projections only

The core design rule is to keep context out of action files and out of orientation files, so each surface stays focused and only loads when needed.

## Core Skills

The repository's distributable product is described as three portable skills:

- `agent-ready-context` — the main pipeline for bootstrap, validation, wiki compilation, and repository readiness
- `skill-creator` — converts repeated actions into new reusable skills with safety defaults
- `subagent-profile-adapter` — generates harness-specific adapters pointing back to the repo's canonical surfaces

Two additional skills, `graphify` and `openkb`, are treated as vendored toolchain copies rather than product skills.

## Workflow and Operations

The README documents how the system operates in practice:

- checks prerequisites such as `git` and `uv`
- asks for consent before installing anything
- records pinned versions and integrity hashes
- builds a staged OpenKB knowledge base
- validates the compiled `okf/wiki/` bundle
- reconciles deleted or moved source material
- supports a zero-LLM fallback when semantic compilation is unavailable

It also provides manual commands for bootstrap, maintenance, and CI use, plus an air-gapped mode that routes work through local models when possible.

## Security and Privacy

A substantial section describes the project's security posture:

- no silent installs
- registry-agnostic dependency handling
- trust-on-first-use pinning with recorded hashes
- explicit disclosure of data flow before LLM calls
- explicit backend routing
- no telemetry in the toolchain claims cited
- secret hygiene via environment variables or gitignored files
- untrusted content treated as data, not instructions

## Contribution Model

The README frames contributions as agent-managed lifecycle work:

- update an existing skill for a behavior change
- create a new skill from repeated actions
- keep procedural guidance in `SKILL.md`
- put details in references and deterministic logic in scripts

This reinforces the repository's broader [[concepts/skill-based-workflow]] and makes repository maintenance itself an agent task.

## Structure and Licensing

The document also explains the expected target-repo layout, including `okf/`, `graphify-out/`, and `.agents/skills/`, and states a file-scoped licensing model:

- code under Apache-2.0
- original prose under CC-BY-4.0
- vendored tools under their upstream licenses
- generated knowledge under internal working-context rules

## Overall Takeaway

The README's main contribution is a concrete architecture for making repositories easier for agents to navigate, maintain, and extend. It combines [[concepts/context-surface-management]], skill packaging, knowledge compilation, and strict safety defaults into a repeatable transformation pipeline.

## Related Concepts
- [[concepts/agent-context-layering]]
- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-repositories]]
- [[concepts/context-action-separation]]
- [[concepts/documentation-architecture]]
- [[concepts/documentation-layer-separation]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/durable-context]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/consent-first-tooling]]
- [[concepts/data-flow-disclosure]]
- [[concepts/air-gapped-operation]]
- [[concepts/explicit-provider-routing]]
- [[concepts/deterministic-validation]]
- [[concepts/incremental-compilation]]
- [[concepts/source-provenance]]
- [[concepts/wiki-context-routing]]
- [[concepts/tooling-boundaries]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/action-oriented-documentation]]
- [[concepts/agent-orientation-index]]
- [[concepts/agents-md-maintenance]]
- [[concepts/consent-first-installation]]
- [[concepts/dependency-management]]
- [[concepts/evidence-staging]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-boundaries]]
- [[concepts/knowledge-capture-boundaries]]
- [[concepts/knowledge-layer-separation]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/offline-first-workflows]]
- [[concepts/quality-gates]]
- [[concepts/repository-transformation-pipelines]]
- [[concepts/skill-authoring]]
- [[concepts/skill-governance]]
- [[concepts/tooling-context-governance]]
- [[concepts/toolchain-pinning]]
- [[concepts/wikilink-integrity]]

## Entities
- [[entities/agent-smith]]
- [[entities/agent-skills]]
- [[entities/okf]]
- [[entities/openkb]]
- [[entities/graphify]]
- [[entities/uv]]
- [[entities/agents-md]]
- [[entities/okf-wiki]]
- [[entities/andrej-karpathy]]
- [[entities/anthropic]]
- [[entities/agentskills-io]]
- [[entities/google-cloud-platform]]
- [[entities/vectifyai-openkb]]
- [[entities/openkb-cli]]
- [[entities/openkb-skill-factory]]
- [[entities/openkb-wiki]]
- [[entities/ollama]]
- [[entities/lm-studio]]
- [[entities/git]]
- [[entities/python]]
- [[entities/creative-commons-attribution-4-0]]
- [[entities/apache-license-2-0]]
- [[entities/the-matrix]]
- [[entities/build_okf_source_pack-py]]
- [[entities/check_prereqs-py]]
- [[entities/editorial_pass-py]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/quick_validate-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/validate_tooling_link_policy-py]]
