---
type: "Concept"
sources: ["summaries/graphify-report.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__query-md.md"]
description: "Expanding queries using only graph-native vocabulary before retrieval."
---

# Query Expansion

Query expansion is the practice of reformulating a user question into a tighter search string before retrieval. In [[summaries/agents__skills__graphify__references__query-md]], this means selecting a small set of tokens from the graph's existing vocabulary and using those tokens, rather than the raw user wording, as the actual traversal query.

## Why it matters

The source document assumes a literal matcher with important limits: case-folded substring matching plus IDF, but no stemming, no synonym model, and no cross-language understanding inside the retrieval tool. A user can ask a valid question and still get zero useful matches if their phrasing differs from the graph's labels. Query expansion addresses that gap by translating the question into terms the graph already contains.

This makes query expansion a practical bridge between human phrasing and graph-native terminology. It directly supports [[concepts/knowledge-graph-analysis]] by improving the starting point for traversal, and it strengthens [[concepts/evidence-grounded-answering]] because the search terms are anchored in the corpus rather than invented at answer time.

## Core pattern in the source

The workflow described in [[summaries/agents__skills__graphify__references__query-md]] is intentionally constrained:

1. Extract vocabulary from node labels in the graph.
2. Read the resulting token list.
3. Select up to 12 tokens that match the user's intent.
4. Use only tokens that actually appear in that vocabulary.
5. Print the selected expansion before traversal so the process is auditable.
6. Stop entirely if no suitable vocabulary exists.

This is not open-ended brainstorming. It is a bounded retrieval step that prevents the system from drifting beyond what the graph can support.

## Hard constraints

The source document makes several rules explicit:

- Only tokens present in the graph vocabulary may be used.
- The system must not invent synonyms from model memory.
- If a concept has no plausible token in the vocabulary, it must be skipped.
- If no tokens match at all, the workflow should return an empty expansion and stop.
- Cross-language or morphological normalization is allowed only when the resulting token is actually present in the vocabulary.

These rules make query expansion a form of [[concepts/schema-constrained-extraction]] applied to retrieval language: the valid search space is defined by the graph's observed labels, not by unconstrained generation.

## Relationship to graph traversal

In the source workflow, expansion happens before any BFS or DFS traversal. That ordering matters. Traversal quality depends heavily on the initial node match, so bad starting terms can collapse the whole query path into noise. By improving the query first, the system increases the odds of finding the right starting nodes and therefore improves downstream traversal quality.

This gives query expansion a strong connection to [[concepts/preflight-checks]]. It functions as a retrieval preflight: validate that the graph contains relevant language before spending effort on traversal. It also complements [[concepts/confidence-calibration]] because an empty or weak expansion is treated as a real signal that the corpus may not support the question.

## Auditability and user trust

A notable detail in [[summaries/agents__skills__graphify__references__query-md]] is the requirement to print the selected tokens to the user before running the query. That makes the transformation visible and reviewable. Instead of silently rewriting the question, the system exposes how it mapped user intent onto graph vocabulary.

This helps preserve [[concepts/provenance-tracking]] and aligns with [[concepts/knowledge-boundaries]]. Users can see when the graph supports a concept well, when it supports it only partially, and when it does not support it at all.

## Role in safe retrieval

The concept is closely tied to retrieval safety. The source explicitly says that if no matching vocabulary exists, the system should stop rather than fabricate a search. That behavior limits false confidence and keeps answers bounded by available evidence.

In that sense, query expansion is not just a recall-enhancement trick. It is also a guardrail for [[concepts/safe-automation]] and [[concepts/graceful-degradation]]: when the graph cannot support the query, the system fails clearly instead of hallucinating a path.

## Feedback loop value

The source document also instructs the agent to save answers back into the graph, including the expanded-token trace in the answer text. Over time, this turns past expansions into part of the graph's operational memory. That creates a strong connection between query expansion and [[concepts/knowledge-graph-feedback-loops]], where successful retrieval patterns become reusable context for future sessions.

## In practice

In this source, good query expansion has three properties:

- grounded in observed graph vocabulary
- narrow enough to stay precise
- explicit enough to audit afterward

That combination makes it especially useful in environments that prioritize [[concepts/llm-free-knowledge-bootstrap]], deterministic tooling, and evidence-bounded graph querying.

## See also

- [[summaries/agents__skills__graphify__references__query-md]]
- [[concepts/evidence-grounded-answering]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/knowledge-graph-feedback-loops]]
- [[concepts/preflight-checks]]
- [[concepts/confidence-calibration]]
- [[concepts/provenance-tracking]]
- [[concepts/knowledge-boundaries]]
- [[concepts/safe-automation]]
- [[concepts/graceful-degradation]]
- [[concepts/schema-constrained-extraction]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]

See also: [[summaries/graphify-report]]