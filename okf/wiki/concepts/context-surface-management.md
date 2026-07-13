---
type: "Concept"
sources: ["summaries/README-md.md"]
description: "Managing repo knowledge across distinct context, action, and orientation surfaces."
---

# Context Surface Management

Context surface management is the practice of separating repository knowledge into distinct surfaces so each one serves a different agent need: orientation, durable context, and repeatable actions. In the `README.md` source, this is presented as the core design principle behind making a repository agent-ready.

## Why it matters

Agents often re-derive the same understanding of a repository from scratch in every session. That wastes context, increases retrieval noise, and makes conclusions easy to lose when the session ends. Context surface management addresses that by keeping each kind of information in the place where it is most useful.

This aligns with [[concepts/progressive-disclosure]], [[concepts/context-action-separation]], and [[concepts/documentation-layer-separation]]: load only the surface needed for the current task, rather than mixing everything into one file.

## Surfaces described in the source

The README divides repository knowledge into four surfaces:

- `AGENTS.md` for orientation: routing, setup, toolchain basics, and repo rules
- `okf/wiki/` for durable context: compiled knowledge, evidence, provenance, and cross-links
- `.agents/skills/` for actions: repeatable procedures and scripts
- Harness adapters for runtime-specific projections only

The key rule is that context should stay out of action files and orientation files. That keeps the repository aligned with [[concepts/context-action-separation]] and helps preserve a small, high-signal context surface.

## Design goals

The README frames this separation as a way to:

- reduce repeated exploration of the same codebase
- keep operational instructions concise and current
- store durable knowledge in a compiled wiki rather than scattered notes
- let each surface load only when needed
- support portable behavior across different agent harnesses

This is also tied to [[concepts/durable-context]] and [[concepts/compiled-knowledge-bases]], since the wiki becomes the persistent memory layer for the repository.

## How the README applies it

The document uses the concept directly in its repository architecture:

- `AGENTS.md` carries the operational basics expected by the instruction-file convention
- `okf/wiki/` holds the OpenKB-compiled knowledge base
- `.agents/skills/` contains the three distributable product skills
- vendored toolchain copies are kept separate from the product skills

That partition is part of the repository's broader [[concepts/repository-transformation-pipelines]] and [[concepts/agent-ready-context]] workflow.

## Related ideas

- [[concepts/knowledge-boundaries]] — keeping knowledge in the right place
- [[concepts/documentation-architecture]] — organizing docs by function
- [[concepts/knowledge-layer-separation]] — separating context layers by purpose
- [[concepts/orientation-routing]] — using a front door for repo navigation
- [[concepts/skill-action-boundary]] — separating procedures from durable knowledge

## Source connection

This concept is central to the repository overview in [[summaries/README-md]], where it serves as one of the main arguments for why the project can make a repository easier for agents to understand, maintain, and extend.