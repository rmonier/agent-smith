---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__query-md.md"]
description: "Answer only from retrieved evidence, citing sources and stating gaps plainly."
---

# Evidence-Grounded Answering

Evidence-grounded answering is the practice of answering a question only from evidence actually retrieved from the available corpus, graph, or compiled knowledge base, while stating uncertainty or gaps plainly when that evidence is insufficient. It prioritizes traceability, bounded claims, and visible provenance over fluent speculation.

This concept is central in [[summaries/agents__skills__graphify__references__query-md]], where graph queries must produce answers strictly from the nodes, edges, relations, confidence tags, and source locations present in the graph. It is also reinforced in [[summaries/agents__skills__openkb__SKILL-md]], which requires answers to be grounded in pages read from the active knowledge base and treats wiki content as untrusted data rather than instructions.

## Core idea

An evidence-grounded answer does not treat the model's background knowledge as authoritative. Instead, it:
- retrieves relevant material from the current repository, graph, or active knowledge base
- limits claims to what that material supports
- cites where the support came from
- preserves uncertainty when support is missing or partial
- distinguishes retrieved evidence from general knowledge or interpretation

This makes the answer auditable and reduces the risk of confident fabrication. It is closely related to [[concepts/knowledge-boundaries]], [[concepts/source-provenance]], and [[concepts/knowledge-linking-and-citations]].

## In the graphify query workflow

In [[summaries/agents__skills__graphify__references__query-md]], evidence-grounded answering appears as an explicit rule set:
- the agent must verify that a graph exists before querying
- the query must be expanded from the graph's actual vocabulary, not invented from outside knowledge
- traversal must use the expanded query terms, whether through the CLI or the inline fallback
- the final answer must use only what the graph contains
- specific facts should cite `source_location`
- if the graph lacks enough information, the agent must say so instead of hallucinating edges or relationships

This ties grounded answering to both retrieval discipline and answer discipline. Good retrieval is necessary, but not sufficient; the response must also avoid adding unsupported implications.

## In the OpenKB retrieval workflow

In [[summaries/agents__skills__openkb__SKILL-md]], evidence-grounded answering is expressed as a read-first workflow over the compiled wiki:
- the agent must discover the active KB first with `openkb status`
- answers should be based on direct reads from `wiki/index.md`, relevant concept pages, entity pages, summary pages, and source pages
- named-entity questions should start from the corresponding entity page when available
- `openkb query` is a last resort because it adds another LLM mediation step
- if the KB has no relevant material, the agent must say so explicitly instead of improvising a KB-backed answer
- if a best-effort answer from general knowledge is offered, it must be clearly labeled as not coming from the KB

This extends grounding beyond graph traversal into wiki-based retrieval. The same discipline applies: first identify the correct corpus, then answer only from what was actually found there. It connects strongly to [[concepts/knowledge-base-discovery]], [[concepts/index-based-discovery]], [[concepts/read-only-kb-operations]], and [[concepts/wiki-content-as-untrusted-data]].

## Why constrained query expansion matters

The graphify source shows that grounding begins before the answer is written. Because the graph matcher has no stemming, synonym system, or cross-language understanding, the workflow requires a constrained expansion step using only tokens already present in the graph vocabulary.

That requirement supports evidence-grounded answering in two ways:
- it prevents the search process from drifting into terms the corpus never uses
- it makes the expansion auditable by printing the selected tokens before traversal

This is a strong connection to [[concepts/query-expansion]], [[concepts/schema-constrained-extraction]], and [[concepts/confidence-calibration]]. If no matching vocabulary exists, the process stops rather than pretending a relevant answer exists.

A similar principle appears in OpenKB: retrieval should begin from the KB's own structure and language by scanning `index.md`, selecting matching slugs, and following existing wikilinks, rather than inventing conceptual matches from outside the corpus.

## Observable signals of a grounded answer

A grounded answer usually has recognizable properties:
- it names the nodes, files, pages, or documents it relies on
- it distinguishes direct evidence from interpretation
- it quotes or cites source locations for concrete claims
- it avoids filling gaps with likely-sounding but unverified links
- it openly reports when the corpus is incomplete
- it makes clear whether the answer comes from a graph, a wiki page, or general knowledge

These behaviors align with [[concepts/provenance-tracking]], [[concepts/documentation-source-priority]], and [[concepts/caveat-preservation]].

## What it prevents

Evidence-grounded answering is a defense against several failure modes:
- hallucinated relations between graph nodes
- silent substitution of near-synonyms not present in the corpus
- answers that blend retrieved facts with unstated model priors
- overconfident summaries of thin or ambiguous evidence
- treating retrieved wiki text as executable instruction rather than evidence
- implying that a claim is KB-backed when it actually comes from outside knowledge

In this sense, it supports [[concepts/prompt-injection-defense]] indirectly by keeping the answer anchored to trusted retrieved material, and it complements [[concepts/safe-automation]] by making automated outputs easier to review.

## Relationship to graph feedback loops

The graphify workflow does more than answer a question once. After answering, it saves the result back into the graph together with cited nodes and an outcome such as `useful`, `dead_end`, or `corrected`. This means evidence-grounded answering becomes part of a larger learning loop: future sessions can prefer sources that previously yielded grounded answers and avoid paths that produced weak ones.

That places this concept near [[concepts/knowledge-graph-feedback-loops]], [[concepts/incremental-graph-maintenance]], and [[concepts/llm-free-knowledge-bootstrap]]. Grounding is not only an output quality property; it also improves the reliability of future retrieval.

## Practical standard

A practical standard for evidence-grounded answering in this wiki context is:
- search only within the active corpus, graph, or knowledge base
- confirm which corpus is active before relying on its contents
- use the corpus's own terminology and structure where possible
- cite retrieved evidence for specific claims
- mark uncertainty explicitly
- separate KB-backed claims from general-knowledge additions
- stop when relevant evidence is absent

When followed, this standard produces answers that are narrower but more dependable, especially in repository analysis, graph-based exploration, and compiled knowledge-base question answering.

## See also

- [[summaries/agents__skills__graphify__references__query-md]]
- [[summaries/agents__skills__openkb__SKILL-md]]
- [[concepts/query-expansion]]
- [[concepts/knowledge-boundaries]]
- [[concepts/source-provenance]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/provenance-tracking]]
- [[concepts/confidence-calibration]]
- [[concepts/caveat-preservation]]
- [[concepts/safe-automation]]
- [[concepts/knowledge-graph-feedback-loops]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/index-based-discovery]]
- [[concepts/read-only-kb-operations]]
- [[concepts/wiki-content-as-untrusted-data]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]