---
type: "Concept"
sources: ["summaries/graphify-report.md", "summaries/karpathy-llm-wiki-gist.md"]
description: "Practices for keeping a compiled wiki accurate, current, and coherent over time."
---

# Wiki Lifecycle Governance

Wiki lifecycle governance is the set of rules and workflows that keep a compiled knowledge base accurate, current, and internally consistent as it grows. In the [[concepts/llm-wiki]] pattern, it is what turns a wiki from a static archive into a maintained system that can absorb new sources, revise old claims, and stay useful over time.

## What it governs

A wiki lifecycle covers the full path from source arrival to long-term maintenance:

- **Ingest** new source material and integrate it into existing pages.
- **Query** the wiki for answers and promote useful analyses back into durable pages.
- **Lint** the wiki to find contradictions, stale claims, missing links, and orphan pages.
- **Evolve** the schema, index, and conventions as the wiki and use cases change.

The source document [[summaries/karpathy-llm-wiki-gist]] presents this as a persistent compilation workflow rather than one-off retrieval.

## Core responsibilities

Lifecycle governance focuses on a few recurring duties:

- Keep [[concepts/knowledge-linking-and-citations]] consistent so pages remain traceable to sources.
- Maintain [[concepts/knowledge-boundaries]] between raw sources, compiled wiki pages, and workflow instructions.
- Apply [[concepts/generated-content-governance]] so generated pages are curated rather than left to drift.
- Use [[concepts/documentation-cohesion]] to keep summaries, entities, and concepts aligned.
- Preserve [[concepts/provenance-tracking]] so later edits can be justified against source evidence.

## In the Karpathy pattern

The gist argues that the hardest part of a knowledge base is not reading or synthesis, but bookkeeping. The lifecycle rules exist to make that bookkeeping cheap and reliable.

Important ideas from the source include:

- The wiki is a **persistent, compounding artifact** rather than a temporary answer cache.
- New sources should update existing pages, not just create isolated summaries.
- Conflicts between pages should be flagged during maintenance, not discovered only when asked.
- Queries can produce durable outputs that become part of the wiki.
- Periodic health checks are a normal part of operation, not an exceptional cleanup task.

These ideas are closely related to [[concepts/compounding-knowledge-bases]] and [[concepts/openkb-wiki-health-checks]].

## Governance mechanisms

A practical lifecycle governance model usually includes:

- **Reserved files and roles** that define what the LLM may edit.
- **Index and log maintenance** so navigation and history stay intact.
- **Validation and lint passes** that check structural integrity, link targets, and stale content.
- **Promotion rules** that decide when a query result, note, or finding becomes a compiled page.
- **Boundary rules** that keep raw sources immutable and compiled pages editable.

These mechanisms support [[concepts/wiki-review-gates]], [[concepts/wiki-lifecycle-governance]], and [[concepts/wikilink-integrity]].

## Why it matters

Without lifecycle governance, a wiki tends to degrade in predictable ways:

- summaries diverge from newer evidence,
- pages stop linking to each other,
- duplicate or conflicting claims accumulate,
- useful analyses disappear into chat history,
- maintenance costs rise faster than value.

The Karpathy idea reframes the wiki as something that can be continuously maintained by the LLM, while the human focuses on curation and judgment. That makes [[concepts/llm-maintained-wikis]] viable as a long-running workflow.

## Related concepts

- [[concepts/compiled-knowledge-bases]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/source-driven-regeneration]]
- [[concepts/editorial-curation-passes]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/provenance-tracking]]

See also: [[summaries/graphify-report]]