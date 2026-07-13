---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"]
description: "Using AGENTS.md as a routing index to repo knowledge sources"
---

# Repository Orientation Indexing

Repository orientation indexing is the practice of keeping `AGENTS.md` short and using it as a navigation layer that points agents to the right source of truth for setup, rules, and deeper context. Instead of packing all knowledge into one file, the repository preserves a clear separation between orientation, executable actions, and compiled context.

This concept is strongly reflected in [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]], which generates a managed OKF section for `AGENTS.md` and explicitly frames that file as a routing map rather than a knowledge base.

## Core idea

A repository orientation file should help an agent answer three questions quickly:

- Where are the local rules and setup steps?
- Where is the compiled repository context?
- Where are reusable actions and maintenance workflows?

The script encodes that navigation order directly:

1. `AGENTS.md` for repository rules, setup, tests, and local pointers.
2. `okf/wiki/index.md` for compiled wiki discovery and routing.
3. `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` for structure-aware inspection.
4. `.agents/skills/` for repeatable agent workflows.

## What makes it an indexing pattern

The managed section does not try to duplicate the whole knowledge base. It acts as an index with routing hints:

- It points to [[concepts/knowledge-base-discovery]] and [[concepts/index-based-discovery]] behavior by making the wiki index the front door.
- It reinforces [[concepts/documentation-layer-separation]] by distinguishing AGENTS.md, skills, and wiki content.
- It supports [[concepts/context-action-separation]] by separating durable context from executable procedures.
- It uses [[concepts/documentation-source-priority]] to order which sources to consult first.

## Source-specific details

The script is conservative about maintenance:

- It only replaces the section between `<!-- okf:start -->` and `<!-- okf:end -->`.
- It preserves existing project-specific setup, style, test, and PR instructions.
- It creates a minimal `AGENTS.md` if one does not exist.
- It normalizes the file into a stable orientation surface that can be refreshed without rewriting unrelated content.

That behavior aligns with [[concepts/conservative-document-merging]] and [[concepts/managed-document-sections]].

## Repository knowledge boundaries

The generated guidance also establishes knowledge boundaries:

- `AGENTS.md` is for orientation, not truth storage.
- `okf/wiki/index.md` routes to compiled context.
- Wiki content is treated as data for navigation, not as instructions.
- Findings belong in staged evidence pages rather than being invented or embedded directly.

Those rules connect to [[concepts/wiki-content-as-untrusted-data]], [[concepts/findings]], and [[concepts/findings-promotion]].

## Why it matters

Repository orientation indexing helps agents:

- avoid overloading one file with mixed responsibilities
- find the correct workflow or context faster
- keep local instructions stable across refreshes
- reduce accidental edits to generated or compiled knowledge
- make repository onboarding more reliable for both humans and automation

In short, it turns `AGENTS.md` into a durable pointer system for the repo's knowledge architecture, while keeping deeper content in the appropriate layer.

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

See also: [[summaries/repo-snapshot]]