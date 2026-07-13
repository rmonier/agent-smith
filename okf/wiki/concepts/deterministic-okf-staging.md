---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Staging OKF inputs deterministically before OpenKB ingestion."
---

# Deterministic OKF Staging

Deterministic OKF staging is the practice of preparing repository evidence in a repeatable, file-based input area before OpenKB ingests it into the compiled wiki. In the agent-ready-context workflow, this means building source packs under `okf/.okf-build/input/` and treating that staged input as the only approved handoff into `okf/wiki/`.

## What it means

The core idea is that wiki content should not be edited in place or generated directly into compiled KB directories. Instead, the pipeline creates a stable intermediate representation that OpenKB can ingest consistently across runs. That keeps the resulting wiki reproducible and reduces drift between source files, staged inputs, and compiled output.

This aligns with related ideas such as [[concepts/deterministic-builds]], [[concepts/source-pack-staging]], [[concepts/source-driven-regeneration]], and [[concepts/compiled-knowledge-bases]].

## How the source document uses it

The agent-ready-context skill describes deterministic staging as a required part of the workflow:

- build a repository source pack with `scripts/build_okf_source_pack.py`
- write staged input to `okf/.okf-build/input/`
- ingest that staged input with OpenKB
- avoid writing generated files directly into `okf/raw/` or `okf/wiki/`

The document also frames this as part of a broader separation between actions, context, and orientation. The staged input is not the final knowledge base; it is the controlled bridge between repository evidence and compiled OKF output. See [[summaries/agents__skills__agent-ready-context__SKILL-md]] for the full workflow.

## Key properties

- **Repeatable inputs**: the same repository state should produce the same staged pack.
- **Deterministic handoff**: OpenKB consumes staged files rather than ad hoc edits.
- **No direct wiki writes**: generated content belongs in the compilation pipeline, not in compiled pages.
- **Clear provenance**: staged content preserves the path from repository source to compiled knowledge.

## Why it matters

Deterministic staging supports reliable regeneration, easier validation, and safer incremental updates. It also helps prevent wiki drift and makes it easier to reason about what changed when OpenKB compiles a new KB snapshot.

In practice, this concept underpins a number of adjacent governance concerns, including [[concepts/hash-registry-coherence]], [[concepts/orphan-retraction]], [[concepts/manifest-authoritative-reconciliation]], and [[concepts/read-only-kb-operations]].

## Related workflow

The staging step is usually paired with:

- prerequisite checks before ingestion
- source-pack manifests
- OpenKB add/lint/validation passes
- review of generated pages for duplicates, weak concepts, or lost caveats

Together, these steps form a deterministic pipeline for turning repository evidence into durable wiki knowledge.