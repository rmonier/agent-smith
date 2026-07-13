---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md"]
description: "LLM-built wikis that accumulate and maintain knowledge over time."
---

# LLM-Maintained Wikis

LLM-maintained wikis are knowledge bases where an LLM does not just answer questions from source material, but continuously compiles, updates, and preserves a structured wiki from those sources. The wiki becomes a persistent artifact that grows with each ingest and query, rather than a temporary retrieval layer.

This concept is central to [[summaries/karpathy-llm-wiki-gist]], which frames the wiki as a compounding system for [[concepts/compiled-knowledge-bases]] and [[concepts/compounding-knowledge-bases]].

## Core idea

The key shift is from retrieval to maintenance. In a conventional RAG setup, each query re-finds and re-synthesizes relevant chunks from raw documents. In an LLM-maintained wiki, the model instead:

- reads new sources,
- extracts durable facts and themes,
- updates existing pages,
- creates new linked pages when needed,
- flags contradictions and stale claims,
- and keeps the whole structure coherent over time.

This means the wiki stores not only source summaries, but also the accumulated synthesis of prior reading and prior questions.

## Why it matters

LLM-maintained wikis reduce the bookkeeping burden that usually causes knowledge systems to decay. The model can keep cross-references current, propagate changes across pages, and surface gaps in coverage without requiring the human to manually maintain every link and summary.

That makes the wiki useful as a long-lived working artifact for research, personal notes, project tracking, due diligence, or any domain where knowledge evolves over time.

Related ideas include [[concepts/knowledge-lifecycle-governance]], [[concepts/guarded-wiki-curation]], and [[concepts/wiki-lifecycle-governance]].

## Structure

The source document describes a three-layer architecture:

- **Raw sources**: immutable originals such as articles, papers, images, or data files.
- **The wiki**: LLM-generated pages such as summaries, entities, concepts, comparisons, and overviews.
- **The schema**: the instructions that define how the LLM should ingest, update, and maintain the wiki.

This separation is closely related to [[concepts/knowledge-layer-separation]] and [[concepts/documentation-layer-separation]].

## Main operations

### Ingest

When a new source arrives, the LLM processes it into the wiki by summarizing it, connecting it to existing pages, updating relevant entities and concepts, and recording the event in a log.

### Query

When asked a question, the LLM searches the wiki first, then synthesizes an answer from maintained pages rather than rebuilding understanding from raw sources alone. Useful answers can themselves be filed back into the wiki as new durable pages.

### Lint

The wiki should be periodically health-checked for contradictions, orphan pages, missing cross-links, stale claims, and underdeveloped concepts. This keeps the knowledge base coherent as it grows.

These workflows overlap with [[concepts/openkb-wiki-health-checks]], [[concepts/openkb-wiki-validation-modes]], and [[concepts/validation-vs-health-reporting]].

## Indexing and logging

Two files are especially important in the pattern:

- `index.md` acts as a content catalog for discovery and navigation.
- `log.md` records a chronological history of ingests, queries, and lint passes.

Together, they make the wiki easier for both humans and agents to navigate, while supporting [[concepts/index-based-discovery]] and [[concepts/knowledge-base-navigation]].

## Design implications

A well-maintained wiki needs clear rules about what gets compiled, what remains in raw sources, and how updates propagate. That touches on:

- [[concepts/documentation-architecture]]
- [[concepts/documentation-cohesion]]
- [[concepts/knowledge-capture-boundaries]]
- [[concepts/single-source-of-truth]]
- [[concepts/wiki-context-routing]]

The model must also be disciplined about evidence and provenance so that synthesized pages remain trustworthy. That connects to [[concepts/evidence-grounded-answering]] and [[concepts/provenance-tracking]].

## Summary

LLM-maintained wikis turn a chat assistant into a persistent knowledge worker. Instead of treating documents as passive retrieval targets, the system compiles them into a living, interlinked wiki that keeps improving as more sources and questions are added.