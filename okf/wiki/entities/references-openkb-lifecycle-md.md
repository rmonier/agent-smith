---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
type: "Work"
description: "Lifecycle guidance for OpenKB KB creation, ingestion, repair, and triage"
---

# references/openkb-lifecycle.md

A workflow reference for managing an OpenKB knowledge base across creation, ingestion, validation, repair, and maintenance.

## Purpose

This document serves as the operational guide for OpenKB-backed wiki work in a repository context. It explains how to keep compiled knowledge aligned with staged source documents, how to treat generated pages, and when to use specialized maintenance paths.

## Core Responsibilities

- Define when to create, refresh, or repair the KB under `okf/`
- Describe the ingestion and recompile lifecycle for staged source material
- Explain how to handle deletions, orphaned documents, and registry drift
- Provide rules for findings triage and editorial curation
- Set boundaries between source documents, compiled wiki pages, and hand edits

## Key Ideas

The document treats the KB as a compiled knowledge layer rather than a place for direct authoring. Its central policy is that durable repository context belongs in the wiki, but the wiki itself should be updated through deterministic staging and compilation rather than ad hoc editing.

It also highlights a few important maintenance concepts:

- [[concepts/deterministic-okf-staging]] for building reproducible input bundles
- [[concepts/source-driven-regeneration]] for fixing weak or incorrect output by updating sources
- [[concepts/findings]] for capturing discovered knowledge that is not yet compiled into the wiki
- [[concepts/orphan-retraction]] for removing pages whose source files were deleted
- [[concepts/registry-drift]] for the risk that hash-based deduplication can hide lost wiki pages

## Workflow Themes

The lifecycle guidance emphasizes a strict sequence:

1. stage deterministic inputs
2. reconcile deletions before ingesting
3. ingest source packs and any promoted findings
4. run lint and validation checks
5. review generated output before accepting it
6. route corrections through the proper loop rather than direct page edits

This makes the process resilient to drift, duplicate content, and accidental corruption of compiled pages.

## Special Cases

The document allows a few narrow exceptions to the normal no-hand-edit rule:

- user-approved edits to `okf/wiki/AGENTS.md` conventions
- the zero-LLM skeleton fallback when no provider is available
- finding capture pages under `okf/wiki/explorations/findings/`
- a guarded editorial pass for output-only semantic lint issues

These exceptions exist to keep the workflow practical while preserving the compiled nature of the wiki.

## Related Pages

- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/generated-content-governance]]
- [[concepts/guarded-wiki-curation]]
- [[concepts/deterministic-validation]]
- [[concepts/hash-registry-coherence]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
