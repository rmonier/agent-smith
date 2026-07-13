---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md"]
description: "Separating orientation, context, and actions keeps agent repositories reliable."
---

# Context-Action Separation

Context-action separation is the practice of keeping durable knowledge, operational instructions, and executable procedures in different places so each can be loaded, updated, and reasoned about independently. In agent-smith, this is a core architectural rule for making a repository more reliable for agents and easier to maintain over time.

## What It Separates

The README.md describes three distinct surfaces:

- `AGENTS.md` for orientation, repository rules, setup, build, launch, and test commands
- `okf/wiki/` for durable context, decisions, evidence, provenance, and compiled knowledge
- `.agents/skills/` for repeatable actions, procedures, and reusable workflows

This division keeps durable context out of instruction files, keeps procedures out of knowledge pages, and reduces the chance that agents confuse what to remember with what to do. It also leaves harness-specific adapters as runtime-only projections rather than source of truth.

## Why It Matters

The repository argues that agents repeatedly re-derive the same understanding of a codebase. If everything is mixed together, they burn context on re-exploration and lose useful conclusions between sessions. By separating context from actions, the system supports [[concepts/progressive-disclosure]] and makes it easier to load only the smallest useful surface for the task at hand.

The README frames this as part of a broader compilation model: raw repository files are source material, the wiki is compiled knowledge, and skills are executable behavior. That separation helps produce [[concepts/agent-ready-repositories]] that are easier for agents to navigate, validate, and extend.

## How It Appears in agent-smith

The document's structure reinforces the boundary:

- `AGENTS.md` carries orientation and operational basics in-file, while deeper knowledge stays routed to the wiki
- `okf/wiki/` holds cross-linked documentation, evidence, provenance, and the compiled OpenKB bundle
- `.agents/skills/` contains reusable workflows such as bootstrap, skill creation, and harness adaptation
- Vendored toolchain copies like `graphify` and `openkb` are treated as pinned dependencies, not product skills

The README explicitly says that knowledge that explains should stay out of files that instruct or route. That rule mirrors [[concepts/documentation-layer-separation]] and [[concepts/knowledge-layer-separation]], but applies it concretely to agent workflows. It also depends on [[concepts/context-surface-management]] and [[concepts/knowledge-compilation-pipeline]] to keep the repository agent-ready without turning every file into a catch-all.

## Related Practices

Context-action separation connects to several other governance ideas in the wiki:

- [[concepts/action-oriented-documentation]] for writing instructions that are procedural rather than explanatory
- [[concepts/agent-context-layering]] for organizing information by how and when agents consume it
- [[concepts/skill-action-boundary]] for keeping skills focused on repeatable actions
- [[concepts/tooling-boundaries]] for limiting what belongs in runtime tools versus knowledge pages
- [[concepts/portable-skill-contract]] for making skills self-contained and reusable

## Source Note

This concept is directly reflected in [[summaries/README-md]], which presents the repository as a three-part system of orientation, context, and actions. The README treats that separation as a prerequisite for an agent-ready repository rather than a stylistic preference.

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]