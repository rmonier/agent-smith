---
type: "Concept"
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md"]
description: "Choosing the cheapest reliable tool first, with clear escalation to costlier options."
---

# Cost-Aware Tool Use

Cost-aware tool use is the practice of choosing the least expensive tool that can reliably answer a task, while reserving higher-cost operations for cases where simpler methods are insufficient. In the OpenKB workflow described by [[summaries/agents__skills__openkb__SKILL-md]], this means preferring direct inspection of the compiled wiki over LLM-backed retrieval, and treating both expensive queries and state-changing actions as tools that require stronger justification.

## Core idea

The concept combines operational efficiency with safety and evidence quality:

- Use deterministic, low-cost commands first.
- Escalate only when direct reads, index scans, or obvious lookups cannot answer the question.
- Treat LLM-backed queries as higher-cost tools because they add another model pass and can compound issues from weak retrieval.
- Keep write-capable operations out of the default path unless the user explicitly requests them.

This aligns with [[concepts/minimal-tool-scoping]], [[concepts/safe-automation]], and [[concepts/tool-boundaries]].

## How it appears in OpenKB

The OpenKB skill gives a concrete routing policy for cost-aware work:

- Start with `openkb status` to locate the active knowledge base and avoid reading the wrong repository.
- Use `openkb list` and `wiki/index.md` as lightweight inventory and discovery tools.
- Read the most relevant concept, entity, or summary pages directly before considering richer retrieval.
- Follow a small number of `wikilink` hops to gather context rather than jumping immediately to a generated query answer.
- Use `openkb query "<question>"` only as a last resort when no obvious slug match or direct search is sufficient.
- Do not autonomously run write commands such as `openkb add`, `openkb remove`, `openkb init`, `openkb use`, or `openkb lint --fix`.

This makes cost a practical routing signal, not just a billing concern. It reduces unnecessary LLM calls, keeps reasoning in the agent's own context, and limits exposure to risky state changes. Related ideas include [[concepts/knowledge-base-discovery]], [[concepts/index-based-discovery]], and [[concepts/non-interactive-agent-design]].

## Why it matters

Cost-aware tool use improves agent behavior in several ways:

- It preserves user resources by avoiding unnecessary LLM-backed retrieval.
- It improves predictability by favoring direct, inspectable commands and file reads.
- It supports better grounding because direct page reads expose the source structure more clearly than opaque query pipelines.
- It reduces accidental side effects by keeping mutating tools behind explicit user approval.
- It lowers risk from wiki content by reducing repeated re-injection of untrusted material into additional model calls.

Because of that, the concept overlaps with [[concepts/preflight-checks]], [[concepts/permission-scoped-agents]], and [[concepts/human-in-the-loop-review]].

## Decision pattern

A cost-aware workflow typically follows this order:

1. Discover the correct knowledge base context with `openkb status`.
2. Inspect available content with `openkb list`, `wiki/index.md`, and direct file reads.
3. Read the most relevant concept, entity, or summary pages and follow 1-2 links if needed.
4. Search exact phrases or inspect specific source pages when direct navigation is insufficient.
5. Use richer query mechanisms only when lightweight discovery still does not resolve the request.
6. Leave write-capable commands to explicit user direction.

This pattern connects cost control with [[concepts/knowledge-boundaries]], [[concepts/evidence-grounded-answering]], and [[concepts/validation-vs-health-reporting]].

## In this source

In [[summaries/agents__skills__openkb__SKILL-md]], cost-aware tool use is expressed as a read-first policy for OpenKB. The document instructs the agent to begin with `openkb status`, use `openkb list` and `wiki/index.md` to discover relevant material, and prefer direct reads of concept and entity pages over `openkb query`. Query is treated as a fallback because it runs a full retrieval pipeline with an additional LLM round-trip. The same source also ties cost-aware behavior to safety by treating wiki content as untrusted data and by forbidding autonomous execution of mutating commands.

## See also

- [[summaries/agents__skills__openkb__SKILL-md]]
- [[summaries/agents__skills__openkb__references__commands-md]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/safe-automation]]
- [[concepts/tool-boundaries]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/index-based-discovery]]
- [[concepts/non-interactive-agent-design]]