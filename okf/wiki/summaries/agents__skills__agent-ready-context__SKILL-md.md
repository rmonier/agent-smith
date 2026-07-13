---
type: "Summary"
description: "Repository workflow for making a repo agent-ready with OKF and AGENTS.md"
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__SKILL-md.md"
---

# Agent-Ready Context

This document defines the repository workflow for making a project "agent-ready" by splitting responsibilities across skills, the OpenKB wiki, and `AGENTS.md`.

## Main Purpose

The skill is meant for repository setup and maintenance tasks such as:

- creating or refreshing the OpenKB knowledge base under `okf/wiki/`
- keeping `AGENTS.md` aligned with the wiki as the repository orientation layer
- staging external evidence and repository source packs
- validating OKF bundles and generated wiki output
- managing harness-specific tooling context when needed

## Core Model

The document emphasizes a clear separation of concerns:

- **Skills** are for repeatable actions, automation, validation, and workflows
- **OKF wiki** is for durable repository context, evidence, provenance, and cross-agent memory
- **`AGENTS.md`** is for concise orientation, setup, test commands, and where to look next

This framing makes the repository easier for agents to navigate and reduces duplication between procedural instructions and long-lived knowledge.

## OpenKB / OKF Workflow

A major theme is that the OpenKB knowledge base is the source of truth for durable context.

Important rules include:

- keep compiled KB content under `okf/wiki/`
- do not create a separate parallel wiki
- do not write generated files directly into `okf/raw/` or `okf/wiki/`
- stage deterministic inputs under `okf/.okf-build/input/` first
- ingest staged input with OpenKB rather than editing compiled pages by hand

The document also describes a correction loop: if generated wiki pages are weak or wrong, the preferred fix is to improve the committed source documents and re-ingest them rather than patching compiled pages.

## Findings and Exceptions

The skill introduces a nuanced policy for what agents may edit directly:

- normal knowledge should move through the staged-source-to-compiled-wiki pipeline
- discovered knowledge that is not directly read from sources can be captured as a finding under `okf/wiki/explorations/findings/`
- a narrow editorial exception exists for output-only semantic lint issues, where a guarded hand edit may be allowed via `scripts/editorial_pass.py`

This suggests a [[concepts/findings]] workflow centered on promote, keep, and drop triage.

## Tooling and Bootstrapping

The document is also a procedural guide for setting up the repository context:

- use `uv` as the required Python toolchain
- install optional tools like `graphify` and `openkb` only with explicit user consent
- vendor the corresponding read-only skills before first CLI use
- ensure `.gitignore`, `.gitattributes`, and `.graphifyignore` are configured correctly
- keep local OpenKB state and generated artifacts out of version control

This creates a reproducible, policy-driven bootstrap path for repository agentification.

## Validation and Review

The workflow includes several validation stages:

- run prerequisite checks before changes when repository state is unknown
- generate the repository graph with Graphify when available
- build a deterministic OKF source pack
- ingest staged input into OpenKB
- run `openkb lint`
- validate the resulting `okf/wiki/` bundle
- review generated pages for duplicate concepts, vague names, and lost caveats

The document treats validation as an ongoing maintenance loop, not a one-time setup step.

## AGENTS.md Role

`AGENTS.md` is positioned as the repository's top-level orientation file, not the place for long-form knowledge.

It should contain:

- primary language and runtime/toolchain details
- setup and bootstrap commands
- build and test commands
- a routing map to the wiki for deeper knowledge
- concise guidance about where agents should look next

The wiki holds the richer background while `AGENTS.md` stays short and operational.

## Notable Ideas

- A repository can be made "agent-ready" by separating durable knowledge from procedural guidance.
- OpenKB is treated as the canonical store for compiled repository context.
- Generated knowledge should usually be repaired at the source level, not by hand-editing compiled output.
- Findings are a first-class mechanism for capturing newly discovered but uncompiled knowledge.
- Tooling context is deliberately scoped and should not become project truth.

## Related Concepts
- [[concepts/context-surface-separation]]
- [[concepts/guarded-wiki-curation]]
- [[concepts/agent-context-layering]]
- [[concepts/agent-ready-repositories]]
- [[concepts/agents-md-maintenance]]
- [[concepts/consent-first-installation]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/documentation-architecture]]
- [[concepts/documentation-source-priority]]
- [[concepts/evidence-staging]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-boundaries]]
- [[concepts/knowledge-capture-boundaries]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/prompt-injection-defense]]
- [[concepts/source-pack-manifest]]
- [[concepts/source-driven-regeneration]]
- [[concepts/source-grounded-regeneration]]
- [[concepts/source-provenance]]
- [[concepts/tooling-boundaries]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-stub-resolving]]
- [[concepts/wiki-context-routing]]

- [[concepts/compiled-knowledge-bases]] for the knowledge-base system and compiled wiki workflow
- [[concepts/agent-orientation-index]] for the role of `AGENTS.md`
- [[concepts/findings]] for promote/keep/drop triage
- [[concepts/deterministic-okf-staging]] for setup, ignore rules, and deterministic staging
- [[concepts/tooling-context-pages]] for harness-specific and user-scoped tooling pages

## Entities
- [[entities/okf]]
- [[entities/openkb]]
- [[entities/graphify]]
- [[entities/uv]]
- [[entities/agent-smith]]
- [[entities/skill-creator]]
- [[entities/subagent-profile-adapter]]
- [[entities/openkb-skill-factory]]
- [[entities/agents-md]]
- [[entities/okf-wiki]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-agents-md]]
- [[entities/tooling]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/gitattributes-template]]
- [[entities/graphifyignore-template]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/build_okf_source_pack-py]]
- [[entities/prune_okf_orphans-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/editorial_pass-py]]
- [[entities/check_prereqs-py]]
- [[entities/scripts-inspect_runtime_context-py]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/references-dependencies-md]]
- [[entities/references-workflow-md]]
- [[entities/references-openkb-lifecycle-md]]
- [[entities/references-openkb-providers-md]]
- [[entities/references-privacy-and-data-flows-md]]
- [[entities/references-external-docs-md]]
- [[entities/references-okf-quality-md]]
- [[entities/references-official-okf-spec-web-check-md]]
- [[entities/agents-skills]]
- [[entities/agent-ready-context-skill]]
- [[entities/openkb-cli]]
- [[entities/graphifyy]]
- [[entities/openkb-wiki]]
- [[entities/okf-spec]]
- [[entities/openkb-lifecycle]]
