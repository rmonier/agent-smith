---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
type: "Work"
description: "Workflow reference for the agent-ready-context skill"
---

# references/workflow.md

## Overview

`references/workflow.md` is a core workflow reference for the `agent-ready-context` skill. It defines the end-to-end process for making a repository agent-ready, from bootstrap and staged source creation through OpenKB ingestion, validation, and post-generation review.

## Role In The Repository

This document serves as the procedural backbone for the agent-ready pipeline. It complements [[entities/agent-ready-context]] by giving step-by-step guidance for the repository's context lifecycle, especially where deterministic scripts, validation gates, and OpenKB operations need to be coordinated.

## Main Responsibilities

- Defines the recommended order of operations for repository agent readiness
- Describes how to bootstrap `AGENTS.md`, graph data, and OpenKB inputs
- Establishes when to stage deterministic source packs versus when to ingest
- Explains the review loop for generated wiki output
- Separates routine workflow steps from special-case edits and findings capture

## Key Workflow Ideas

### Progressive Disclosure

The workflow starts with progressive disclosure: read `okf/wiki/index.md` first when it exists, then follow its routing to the relevant area. This keeps agents aligned with the compiled KB rather than jumping directly into ad hoc pages.

### Deterministic Staging

A central requirement is that generated inputs must be staged deterministically before ingestion. The workflow favors `okf/.okf-build/input/` as the safe staging area and treats `okf/wiki/` as compiled output, not a hand-edit target.

### OpenKB As The Context Source Of Truth

The workflow treats `okf/wiki/` as the durable repository memory. It explicitly avoids a parallel wiki and pushes corrections back into source documents when generated pages are wrong or incomplete.

### Validation And Review Gates

The document layers multiple checks:

- prerequisite checks before work begins when repository state is unclear
- graph generation when Graphify is available
- source-pack staging before OpenKB ingestion
- OpenKB linting after ingestion
- bundle validation against the compiled wiki
- manual review of generated pages for duplicates, missing caveats, and misclassification

These gates reinforce [[concepts/deterministic-validation]] and [[concepts/generated-content-governance]].

## Notable Policies

- Never write generated files directly into `okf/raw/` or `okf/wiki/`
- Prefer source corrections and re-ingestion over hand-editing compiled wiki pages
- Treat discovered knowledge that is not directly sourced as a finding under `okf/wiki/explorations/findings/`
- Use a guarded editorial pass only for output-only semantic-lint issues with no source fault
- Keep `okf/.openkb/hashes.json` under careful review because registry drift can silently suppress future ingestion

## Related Concepts

- [[concepts/agent-ready-context]]
- [[concepts/deterministic-okf-staging]]
- [[concepts/openkb-build-workflow]]
- [[concepts/okf-bundle-validation]]
- [[concepts/guarded-wiki-curation]]
- [[concepts/findings]]
- [[concepts/registry-drift]]

## Why It Matters

This workflow is important because it turns repository knowledge into a repeatable, low-drift system. It reduces duplication between `AGENTS.md`, skills, and the compiled wiki, while keeping provenance, validation, and local tooling boundaries explicit.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
