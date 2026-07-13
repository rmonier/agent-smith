---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"]
description: "How agents follow a staged map from orientation files to deeper context."
---

# Orientation Routing

Orientation routing is the practice of guiding an agent from a shallow entrypoint, such as `AGENTS.md`, to progressively deeper and more specialized context sources in a controlled order. It helps keep repository guidance concise while still making the right knowledge easy to find.

This concept is expressed in `summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py`, where the managed `AGENTS.md` section acts as a routing map rather than a knowledge base.

## Core idea

Orientation routing separates:

- **Orientation**: the first-stop files that explain where to look next.
- **Context**: durable knowledge captured in the OKF wiki.
- **Actions**: executable procedures and scripts in skills.

That separation supports [[concepts/context-action-separation]], [[concepts/documentation-layer-separation]], and [[concepts/knowledge-layer-separation]].

## Routing order in the source document

The script injects guidance that tells agents to consult sources in this sequence:

1. `AGENTS.md` for repository rules, setup, and local pointers.
2. `okf/wiki/index.md` as the front door to wiki discovery.
3. `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` for structural mapping.
4. `.agents/skills/` for reusable action-oriented automation.

This is a concrete example of [[concepts/index-based-discovery]] and [[concepts/knowledge-base-navigation]]: start with an index, then follow its links instead of scanning blindly.

## What makes the routing safe

The managed section is designed to preserve repository-authored content and avoid overreach:

- It replaces only the block between `<!-- okf:start -->` and `<!-- okf:end -->`.
- It appends the managed section when those markers are missing.
- It creates a minimal `AGENTS.md` only when needed.
- It explicitly tells agents not to treat wiki content as instructions.

These behaviors align with [[concepts/conservative-document-merging]], [[concepts/managed-document-sections]], and [[concepts/wiki-content-as-untrusted-data]].

## Why it matters

Orientation routing reduces confusion in agent-facing repositories by making the first steps deterministic. Instead of embedding all guidance in one file, it provides a staged path from orientation to durable context to executable actions.

That supports [[concepts/agent-orientation-index]], [[concepts/agent-context-layering]], and [[concepts/progressive-disclosure]]. It also helps maintain [[concepts/documentation-cohesion]] by keeping each layer focused on a different job.

## Related source behavior

The script also embeds maintenance guidance that reinforces the routing model:

- Refresh agent-ready context when source files, architecture, CI/CD, or security assumptions change.
- Read `okf/wiki/AGENTS.md` after initialization or upgrades.
- Use `uv run` for bundled scripts when `uv` is available.
- Capture durable discoveries as findings instead of editing compiled wiki pages directly.

Those rules connect orientation routing to [[concepts/agents-md-maintenance]], [[concepts/agent-ready-context-skill]], [[concepts/findings]], and [[concepts/generated-content-governance]].

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[concepts/agent-orientation-index]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/wiki-context-routing]]
- [[concepts/managed-document-sections]]