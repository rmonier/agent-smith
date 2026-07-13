---
type: "Concept"
sources: ["summaries/README-md.md"]
description: "A compiled wiki memory layer that lets agents reuse durable repository context."
---

# LLM Wiki

## Concept

An LLM Wiki is a compiled knowledge system where raw repository material is turned into an interlinked wiki so an agent can reuse durable context instead of re-deriving it in every session. In the `agent-smith` README, this idea is the foundation of the repository transformation model: source files are treated as inputs, the wiki becomes the compiled knowledge surface, and the agent acts as the compiler that ingests, revises, and cross-links knowledge over time.

## How It Works

The model treats knowledge as a compilation pipeline:

- source files act like source code
- the wiki acts like compiled output
- the agent compiles, revises, and cross-links knowledge
- contradictions, deletions, and missing links become maintenance signals

The README extends this into a broader repository workflow: durable context lives in `okf/wiki/`, operational orientation lives in `AGENTS.md`, and repeatable procedures live in `.agents/skills/`. The wiki is therefore not just a note store; it is the compiled memory layer within a larger [[concepts/agent-context-layering]] design.

## Why It Matters

The README argues that an LLM Wiki improves agent performance because it supports:

- [[concepts/durable-context]] across sessions
- [[concepts/knowledge-linking-and-citations]] for multi-hop traversal
- [[concepts/progressive-disclosure]] by loading only the right surface at the right time
- [[concepts/context-action-separation]] by keeping orientation, knowledge, and actions distinct
- [[concepts/agent-ready-repositories]] by making a repository easier for agents to operate in

It presents the wiki not as a dump of notes, but as a compact, navigable memory layer that compounds knowledge instead of losing it when a session ends.

## Relation to the Repository Design

In `agent-smith`, the LLM Wiki is implemented through the `okf/wiki/` surface described in [[summaries/README-md]]. That surface holds durable OpenKB knowledge, while `AGENTS.md` provides orientation and `.agents/skills/` provides repeatable actions. The README frames this as an agent-ready repository architecture: the three surfaces are deliberately separated so each one carries only the kind of information it is meant to hold.

The wiki also sits inside a consent-first, validation-heavy pipeline. The repository checks prerequisites before work begins, discloses data flow before any LLM call, supports air-gapped operation when needed, and validates the compiled wiki bundle before treating it as ready. In that sense, the LLM Wiki is not just an output format; it is the central artifact of an [[concepts/agent-ready-context]] workflow.

## Core Properties

An effective LLM Wiki emphasizes:

- [[concepts/compiled-knowledge-bases]] instead of ad hoc context chunks
- [[concepts/incremental-compilation]] as the repository changes
- [[concepts/source-provenance]] so compiled knowledge remains traceable
- [[concepts/wikilink-integrity]] so links stay navigable and useful
- [[concepts/wiki-content-as-untrusted-data]] so evidence is summarized, not obeyed blindly
- [[concepts/deterministic-validation]] so compiled knowledge can be checked reliably
- [[concepts/orphan-retraction]] so stale knowledge is removed when sources disappear

These properties make the wiki durable rather than brittle: it can be updated, validated, and trimmed without losing its role as the repository's reusable memory.

## Practical Outcome

The result is a repository that carries its own memory. Agents can enter with less cold-start cost, find the right orientation quickly, and build on prior conclusions instead of starting over. In the README's framing, that is what makes the repository agent-ready: knowledge is compiled once, maintained incrementally, and surfaced through the right layer at the right time.