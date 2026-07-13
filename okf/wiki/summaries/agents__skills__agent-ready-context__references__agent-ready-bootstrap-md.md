---
type: "Summary"
description: "Bootstrap guide for making a repository agent-ready with OKF and skills."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md"
---

# Agent-Ready Bootstrap Reference

This document explains how to convert a repository into an agent-ready repository with a clear split between routing, durable knowledge, structural exploration, and reusable skills.

## Main Ideas

- `AGENTS.md` should stay short and focused on routing, operational rules, and the basic commands agents need.
- Durable project context belongs in `okf/wiki/`, not in `AGENTS.md`.
- `graphify-out/` is for structural exploration, not as the source of truth.
- `.agents/skills/` stores reusable actions and should absorb repeated procedures over time.

## Target Repository Layout

The reference recommends a repository structure centered on:

- `AGENTS.md`
- `.gitignore` for pipeline build artifacts
- `okf/` as the OpenKB knowledge base root
- `okf/wiki/` as the compiled wiki output
- `graphify-out/` for graph exploration artifacts
- `.agents/skills/` for skills such as `agent-ready-context` and `skill-creator`

## Tooling Bootstrap

The workflow is consent-first:

- Check prerequisites first with a bootstrap script.
- Install missing tools only after user approval.
- Package provenance and pinning are deferred to `references/dependencies.md`.

Suggested tools include:

- `graphify` for structural graph generation
- `openkb` for knowledge base initialization, ingestion, and linting

## Suggested Build Sequence

The document outlines a typical sequence for preparing the repository:

1. Merge the OKF section into `AGENTS.md`.
2. Run `graphify update` to refresh structure data.
3. Build an OKF source pack.
4. Add external docs as evidence under `okf/.okf-build/input/external/`.
5. Initialize OpenKB in `okf/`.
6. Add the source pack to the knowledge base.
7. Lint the generated wiki.
8. Validate the wiki bundle.
9. Merge the final `AGENTS.md` OKF section again.

A conservative fallback is also provided for cases without an LLM provider:

- Build an OKF skeleton instead of running semantic generation.
- Validate the resulting wiki bundle.

## Commit Guidance

The reference gives practical version-control advice:

- Commit core routing and wiki artifacts such as `AGENTS.md`, `okf/wiki/`, and key metadata files.
- Avoid committing build outputs, report directories, and environment-specific cache or credential files.
- Ensure `.gitignore` covers generated artifacts and local secrets.

## Skill Lifecycle Guidance

After the first OKF generation, the repository should be reviewed for repeated work that is better captured as a skill.

- Keep architecture facts, evidence, and provenance in knowledge base wiki content.
- Move repeated command sequences, migrations, validation steps, and scaffolding into skills.
- Keep `AGENTS.md` as a compact routing layer that points to `okf/wiki/index.md` as the main entry point.
- Treat vendor skills as read-only dependencies and extend behavior with custom wrapper skills when needed.

## Notable Concepts

This document reinforces several reusable ideas that may warrant cross-document synthesis:

- [[concepts/agent-ready-repositories]]
- [[concepts/durable-context]]
- [[concepts/consent-first-tooling]]
- [[concepts/skill-based-automation]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/provenance-tracking]]

## Overall Takeaway

The bootstrap process is designed to make a repository safe and practical for agent use by separating short operational routing from durable wiki knowledge, while steadily turning repeated actions into maintainable skills.

## Related Concepts
- [[concepts/skill-structure-conventions]]
- [[concepts/agents-md-maintenance]]
- [[concepts/context-action-separation]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/dependency-management]]
- [[concepts/project-scaffolding]]
- [[concepts/quality-gates]]
- [[concepts/generated-content-governance]]
- [[concepts/skill-governance]]
- [[concepts/source-driven-regeneration]]
- [[concepts/read-only-kb-operations]]
- [[concepts/kb-root-staging]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/tooling-context-isolation]]
- [[concepts/knowledge-base-discovery]]

## Entities
- [[entities/agent-ready-context]]
- [[entities/openkb]]
- [[entities/graphify]]
- [[entities/uv]]
- [[entities/okf-spec]]
- [[entities/okf-readme]]
- [[entities/skill-creator]]
- [[entities/agents-md]]
- [[entities/vectifyai-openkb]]
- [[entities/graphifyy]]
- [[entities/litellm]]
