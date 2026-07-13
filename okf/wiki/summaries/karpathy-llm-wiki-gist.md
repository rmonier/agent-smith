---
type: "Summary"
description: "Karpathy's pattern for using LLMs to build and maintain a persistent wiki"
doc_type: short
full_text: "sources/karpathy-llm-wiki-gist.md"
---

# LLM Wiki (Karpathy idea gist)

Andrej Karpathy's gist describes a workflow for using an LLM as a persistent maintainer of a personal knowledge base, rather than as a one-off retrieval-and-answer system.

## Core idea

The document contrasts traditional RAG with a wiki model that compounds over time. In the RAG model, each question re-derives answers from raw documents. In the wiki model, the LLM incrementally compiles source material into a structured, interlinked knowledge base that preserves synthesis across sessions.

Key properties of this wiki model:

- The wiki is a persistent artifact that accumulates knowledge over time.
- New sources are not only indexed but integrated into existing pages.
- Cross-references, contradictions, and synthesis are maintained proactively.
- The LLM writes and maintains the wiki; the human curates sources and asks questions.

This frames the wiki as a compounding system: each ingest makes the knowledge base more useful for future ingests and queries.

## Architecture

The gist describes three layers:

- **Raw sources**: immutable documents, articles, papers, images, or data files that serve as source of truth.
- **The wiki**: LLM-generated markdown pages such as summaries, entity pages, concept pages, comparisons, and synthesis pages.
- **The schema**: instructions and conventions that tell the LLM how to maintain the wiki consistently over time.

The schema is presented as the key coordination layer, because it turns the LLM from a generic assistant into a disciplined wiki maintainer.

## Operations

The document outlines three main workflows:

- **Ingest**: process a new source, summarize it, update relevant pages, add links, resolve or flag contradictions, and log the operation.
- **Query**: answer questions by reading relevant wiki pages and synthesizing an answer, ideally with outputs that can be filed back into the wiki.
- **Lint**: periodically inspect the wiki for contradictions, stale claims, missing links, orphan pages, and missing concept coverage.

A notable theme is that answers and analyses should themselves become durable wiki content when useful, so exploration compounds rather than disappearing into chat history. This is closely related to [[concepts/compounding-knowledge-bases]] and [[concepts/knowledge-lifecycle-governance]].

## Indexing and logging

The gist emphasizes two supporting files:

- **`index.md`**: a content-oriented catalog of pages with one-line summaries and metadata; used first when searching the wiki.
- **`log.md`**: a chronological append-only record of ingests, queries, and lint passes.

Together, these files provide lightweight navigation and history without requiring a full search stack at small to moderate scale.

## Optional tooling

The document suggests optional tools that can improve the workflow as the wiki grows:

- Local search over markdown pages, such as qmd or similar tools.
- Obsidian-based workflows for browsing, editing, and graph visualization.
- Image downloading for offline reference when sources include visuals.
- Marp for slide decks and Dataview for querying page metadata.

These are presented as modular additions rather than requirements.

## Why it works

The core argument is that knowledge bases fail mainly because of maintenance burden, not because of reading or synthesis. LLMs reduce the cost of bookkeeping tasks such as:

- updating cross-references,
- keeping summaries current,
- propagating new evidence,
- preserving consistency across many files.

That makes the wiki viable as a long-lived, evolving artifact instead of a static archive. The human role becomes source curation, direction, and judgment, while the LLM handles the maintenance work.

## Related ideas

The document connects this pattern to personal knowledge management, llm assisted research, and associative linking in spirit, and compares it to Vannevar Bush's Memex as a historical precursor.

## Takeaway

The main contribution is a practical operating model for building a wiki that grows with use: sources are ingested into structured pages, questions become durable additions to the knowledge base, and periodic linting keeps the system coherent over time.

## Related Concepts
- [[concepts/llm-maintained-wikis]]
- [[concepts/wiki-lifecycle-governance]]
- [[concepts/action-oriented-documentation]]
- [[concepts/agent-guided-graph-exploration]]
- [[concepts/knowledge-graph-feedback-loops]]
- [[concepts/external-documentation]]
- [[concepts/evidence-backed-skill-initialization]]
- [[concepts/source-grounded-regeneration]]

## Entities
- [[entities/andrej-karpathy]]
- [[entities/llm-wiki]]
- [[entities/obsidian]]
- [[entities/memex]]
- [[entities/agent-smith]]
- [[entities/openkb]]
- [[entities/openkb-wiki]]
- [[entities/okf-wiki]]
- [[entities/wiki-schema-md]]
