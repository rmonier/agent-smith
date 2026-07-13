---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/README-md.md"]
description: "Turning repository sources into durable, interlinked wiki knowledge."
---

# Knowledge Compilation Pipeline

The knowledge compilation pipeline is the workflow that turns raw repository material into durable, interlinked wiki knowledge. In the README for [[summaries/README-md]], this is the central metaphor behind `agent-smith`: source files are treated as inputs to be compiled, while the wiki becomes the persistent knowledge surface that agents can reuse across sessions.

## Core idea

The pipeline treats knowledge like software compilation:

- raw documents, code, and repository artifacts are the source material
- the wiki is the compiled output
- the agent acts as the compiler that ingests, revises, links, and validates
- conclusions persist instead of being re-derived every session

This framing is meant to reduce repeated exploration, preserve context, and make agent work more efficient over time. It aligns closely with [[concepts/compiled-knowledge-bases]], [[concepts/durable-context]], and [[concepts/context-surface-management]].

## What the README emphasizes

The README presents the pipeline as part of a broader repository transformation system that makes a project agent-ready. It separates the repository into three functional surfaces:

- `AGENTS.md` for orientation and operating basics
- `okf/wiki/` for durable compiled knowledge
- `.agents/skills/` for repeatable actions and procedures

That separation supports [[concepts/context-action-separation]] and [[concepts/documentation-layer-separation]], so each surface carries only the kind of information it is meant to hold.

## How compilation works

The workflow described in the README includes several distinct steps:

- ingest repository sources and supporting documents
- stage evidence deterministically before compilation
- build or refresh the OpenKB knowledge base
- link related pages through wikilinks
- detect deletions, moves, and stale references
- validate the resulting wiki bundle

This is not just a one-time conversion. It is an incremental process that keeps the compiled knowledge synchronized with the repository, reflecting [[concepts/incremental-compilation]] and [[concepts/source-driven-regeneration]].

## Why it matters

The README argues that agents work better when they can rely on a compact, curated knowledge surface rather than re-reading entire repositories repeatedly. The pipeline provides that surface by:

- concentrating important information into the wiki
- preserving provenance and evidence
- allowing cross-document navigation
- making updates repeatable and checkable

That makes it a practical instance of [[concepts/progressive-disclosure]], [[concepts/provenance-tracking]], and [[concepts/knowledge-linking-and-citations]].

## Relationship to agent-ready repositories

Within the README, the pipeline is the mechanism that turns a repository into an [[concepts/agent-ready-repositories|agent-ready repository]]. It creates orientation, memory, and actions as separate layers so an agent can arrive, understand the project quickly, and operate without re-discovering the same facts.

That also connects the pipeline to [[concepts/agent-context-layering]], [[concepts/knowledge-lifecycle-governance]], and [[concepts/knowledge-boundaries]].

## Reliability and safeguards

The README stresses that the pipeline should be:

- consent-first
- deterministic where possible
- validated after each meaningful stage
- able to degrade gracefully when optional tools are unavailable
- explicit about data flow and external dependencies

Those safeguards tie the concept to [[concepts/consent-first-workflows]], [[concepts/deterministic-validation]], [[concepts/graceful-degradation]], and [[concepts/data-flow-disclosure]].

## Related ideas in the repository

The pipeline also depends on a few supporting concepts:

- [[concepts/repository-ingestion]] for collecting source material
- [[concepts/evidence-staging]] for preparing trustworthy inputs
- [[concepts/openkb-build-workflow]] for the compilation lifecycle
- [[concepts/okf-bundle-validation]] for checking the resulting wiki
- [[concepts/orphan-retraction]] for removing knowledge tied to deleted sources

Together, these form the operational backbone of the repository's knowledge system.


See also: [[summaries/repo-snapshot]]