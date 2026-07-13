---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "An orientation index that routes agents to repo rules, tools, and wiki context."
---

# Agent Orientation Index

An agent orientation index is the first-stop guide that tells automated agents where to look next in a repository. It does not try to store full project knowledge; instead, it points to the right layer of information and keeps the boundaries between action, context, and durable documentation clear.

## What It Does

- Gives agents a lightweight entry point for setup, rules, and navigation.
- Directs agents to the correct source of truth based on the task.
- Prevents duplication by keeping operational basics separate from durable context.
- Supports [[concepts/documentation-layer-separation]] and [[concepts/knowledge-boundaries]] by assigning each repository surface a distinct role.

## In the Source Template

The template in `[[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]` treats `AGENTS.md` as the orientation index for the repo. It says that:

- `AGENTS.md` should hold only operational basics such as primary language, toolchain versions, setup/build/launch commands, and tests.
- The OKF wiki should hold durable context, evidence, architecture, decisions, and provenance.
- Skills should hold repeatable actions, scripts, and workflows.
- `okf/wiki/index.md` should be the first routed context after `AGENTS.md`, and should determine which wiki pages to open next.
- Tooling context should be discovered through `tooling/index.md` and related local harness pages when needed.

This makes the index a navigation layer rather than a knowledge store, which is a central pattern in [[concepts/agent-context-layering]] and [[concepts/knowledge-base-navigation]].

## Why It Matters

A good orientation index reduces confusion for both humans and agents:

- It creates a predictable starting point for repo work.
- It limits context overload by staging information progressively.
- It keeps generated knowledge, local tooling, and executable skills from collapsing into one file.
- It helps maintain [[concepts/durable-context]] while preserving the repo's operational surface.

## Related Ideas

- [[concepts/action-oriented-documentation]]
- [[concepts/context-action-separation]]
- [[concepts/progressive-disclosure]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/wiki-context-routing]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/tooling-context-governance]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

See also: [[summaries/README-md]]