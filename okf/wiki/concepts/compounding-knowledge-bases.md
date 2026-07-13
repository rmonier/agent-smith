---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md"]
description: "Knowledge bases that grow richer by integrating each new source once."
---

# Compounding Knowledge Bases

A compounding knowledge base is a wiki or documentation system that does not merely store source material for later retrieval, but incrementally integrates each new source into a growing, structured knowledge graph of pages, links, and maintained synthesis.

## Core idea

The key distinction is between retrieval and compilation.

In a retrieval-only system, each question starts from raw documents again: the system finds relevant chunks, then reconstructs an answer from scratch. In a compounding knowledge base, the work of reading, extracting, linking, reconciling, and organizing is done once when the source arrives, and the result is preserved for future use.

Karpathy's LLM Wiki gist describes this as a persistent artifact: the wiki gets richer with every ingest, and the LLM is responsible for keeping it current. That makes the knowledge base cumulative rather than repeatedly rediscovered. See [[summaries/karpathy-llm-wiki-gist]] for the original framing.

## What compounds

Several kinds of value accumulate over time:

- **Synthesis**: summaries evolve from isolated notes into coherent cross-document understanding.
- **Link structure**: references between related pages are created and repaired as the wiki grows.
- **Contradiction tracking**: new evidence can challenge older claims instead of silently replacing them.
- **Coverage**: missing concepts become visible, making gaps easier to notice and fill.
- **Usability**: future questions can start from an already-organized base instead of raw documents.

This is closely related to [[concepts/compiled-knowledge-bases]] and [[concepts/knowledge-compilation-pipeline]], but the emphasis here is on growth over time rather than one-time construction.

## Why it matters

The main problem with conventional knowledge management is maintenance. Humans are usually willing to read and think, but not to continuously update cross-references, propagate new evidence, and keep summaries aligned across dozens or hundreds of pages.

A compounding knowledge base works because an LLM can perform that bookkeeping cheaply and repeatedly. The knowledge base therefore improves as more material is ingested, instead of decaying into stale notes.

This also changes the role of questioning: answers are not just temporary chat outputs, but can become durable additions to the knowledge base. That is a form of [[concepts/generated-artifact-adoption]] and [[concepts/source-grounded-regeneration]] in which explorations feed back into the system.

## Typical workflow

Karpathy's model describes a repeating loop:

1. A new source is added to the raw collection.
2. The LLM reads it and extracts the important points.
3. Existing pages are updated where needed.
4. New pages may be created for recurring entities or concepts.
5. Cross-links and log entries are maintained.
6. The wiki is later queried using the accumulated structure.

This makes ingest, query, and lint part of one continuous lifecycle rather than separate tasks. The wiki grows through [[concepts/incremental-graph-maintenance]] and remains coherent through [[concepts/openkb-wiki-health-checks]].

## Design implications

A compounding knowledge base usually benefits from:

- a strong index or orientation layer for navigation;
- explicit source provenance and citation discipline;
- page types that separate summaries, concepts, and entities;
- periodic health checks for stale claims, orphans, and missing links;
- rules that prevent the wiki from becoming a pile of disconnected notes.

These requirements align with [[concepts/knowledge-base-navigation]], [[concepts/provenance-tracking]], [[concepts/knowledge-linking-and-citations]], and [[concepts/wiki-lifecycle-governance]].

## In practice

The pattern is especially useful when knowledge is:

- accumulated over time rather than learned all at once;
- spread across many documents;
- likely to be revisited in later questions;
- improved by cross-linking and reconciliation;
- valuable enough to preserve as a long-lived asset.

Examples include research notes, personal knowledge management, competitive analysis, project documentation, and curated source collections.

## Relationship to adjacent ideas

- [[concepts/llm-maintained-wikis]] focuses on the role of the LLM as the maintainer.
- [[concepts/compiled-knowledge-bases]] focuses on the organized output.
- [[concepts/knowledge-compilation-pipeline]] focuses on the ingest-and-transform workflow.
- [[concepts/knowledge-lifecycle-governance]] focuses on keeping the system healthy over time.

The compounding aspect is what turns a wiki from a static archive into a living knowledge system.