---
sources: ["summaries/karpathy-llm-wiki-gist.md"]
type: "Work"
description: "Karpathy's proposed pattern for LLM-maintained personal wikis."
---

# LLM Wiki

[[entities/andrej-karpathy]]'s idea for an [[concepts/llm-maintained-wikis|LLM-maintained wiki]] is a persistent, compounding knowledge base built from immutable sources and LLM-generated pages.

## Overview

LLM Wiki describes a workflow where an agent reads new source documents, compiles them into structured markdown pages, and keeps the resulting wiki current over time. Rather than answering each question from raw documents alone, the system accumulates synthesis in the wiki itself.

The idea is framed as a practical alternative to standard retrieval-augmented generation: the LLM does not just fetch text at query time, but maintains a durable artifact that already contains summaries, cross-references, and identified contradictions.

## Core model

The document defines three layers:

- **Raw sources**: immutable source documents that the LLM reads but never edits.
- **The wiki**: LLM-generated markdown pages such as summaries, entity pages, concept pages, and comparisons.
- **The schema**: a guidance document that tells the LLM how to maintain the wiki and what workflows to follow.

This structure turns the wiki into a [[concepts/compounding-knowledge-bases|compounding knowledge base]]: every ingest strengthens the existing corpus instead of restarting from scratch.

## Workflow

Karpathy's gist describes three recurring operations:

- **Ingest**: process a new source, summarize it, update relevant pages, add links, and log the change.
- **Query**: answer questions by reading relevant pages and synthesizing a response that can itself become new wiki content.
- **Lint**: check for contradictions, stale claims, missing cross-references, orphan pages, and coverage gaps.

The model assumes that good answers, comparisons, and analyses should often be promoted back into the wiki, so exploration and curation reinforce each other.

## Supporting files

Two files are highlighted as especially important:

- **`index.md`**: a content-oriented catalog of pages, used to navigate the wiki at a glance.
- **`log.md`**: an append-only timeline of ingests, queries, and lint passes.

Together, these provide lightweight navigation and operational history without requiring heavy infrastructure.

## Tools and usage

The gist presents the wiki as something an LLM agent maintains while a human curates sources and asks questions. It suggests pairing the agent with an editor such as Obsidian, using the wiki as the interface for browsing, linking, and reviewing updates.

It also points to optional tooling such as local search, slide generation, metadata queries, and image handling, but treats them as modular additions rather than requirements.

## Why it matters

The central claim is that knowledge-base maintenance fails mainly because of bookkeeping overhead, not because people cannot read or reason. An LLM can cheaply handle the repetitive work of updating links, revising summaries, and preserving consistency across many files.

That makes the wiki a practical long-lived artifact for personal research, business knowledge, reading projects, and other domains where information accumulates over time.

## Related ideas

This work connects closely to [[concepts/llm-maintained-wikis]], knowledge base architecture, and [[concepts/compounding-knowledge-bases]], and it is historically related to Memex as a vision of associative, curated knowledge.

## Related Documents
- [[summaries/karpathy-llm-wiki-gist]]
