---
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/README-md.md"]
type: "Person"
description: "Researcher and LLM Wiki originator who inspired the wiki pattern here."
---

# Andrej Karpathy

Andrej Karpathy is a researcher and software thinker whose LLM Wiki idea helped shape the design of `agent-smith` and the broader wiki workflow in this repository.

## Why he matters here

Karpathy's gist frames the wiki as a persistent, compounding knowledge base rather than a one-off retrieval layer. That idea is central to this repository's approach to [[concepts/llm-wiki]], [[concepts/compiled-knowledge-bases]], and [[concepts/compounding-knowledge-bases]].

His pattern emphasizes that raw sources remain immutable while the LLM maintains a structured wiki of summaries, entity pages, concept pages, and cross-references. That maps directly to the repository's emphasis on [[concepts/knowledge-compilation-pipeline]], [[concepts/source-grounded-regeneration]], and [[concepts/knowledge-linking-and-citations]].

The gist also treats the schema as a key control surface: a document that defines conventions, workflows, and maintenance rules so the LLM behaves like a disciplined wiki steward. That aligns with [[concepts/wiki-lifecycle-governance]], [[concepts/wiki-review-gates]], and [[concepts/guarded-wiki-curation]].

## In this repository

- His LLM Wiki concept is presented as the conceptual foundation for the OKF knowledge workflow described in [[summaries/README-md]].
- The README uses his idea to justify why durable repository knowledge should live in `okf/wiki/` instead of being re-derived every session.
- He is cited as the author of the original idea file linked from the project overview.
- The repository treats his framing as evidence for [[concepts/repository-transformation-pipelines]] that compile raw sources into maintainable agent context.
- The new gist expands that framing with explicit practices for ingest, query, and lint operations, which reinforce [[concepts/openkb-wiki-health-checks]] and [[concepts/knowledge-lifecycle-governance]].

## Related entities

- [[entities/agent-smith]]
- [[entities/okf-wiki]]
- [[entities/okf-spec]]
- [[entities/memex]]

## Related Documents
- [[summaries/karpathy-llm-wiki-gist]]
