---
type: "Concept"
sources: ["summaries/graphify-report.md", "summaries/agent-skills-spec.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/README-md.md"]
description: "Layered information delivery that reveals only the needed detail at each step."
---

# Progressive Disclosure

Progressive disclosure is the practice of arranging information in layers so each layer carries only the detail needed for its immediate role. In agent-oriented repositories, it keeps orientation, durable context, and executable actions distinct so an agent can load a small, high-signal surface first and pull in deeper material only when necessary.

## Why it matters

The repository’s graph structure reinforces this pattern. The graph report shows a large enough corpus for structural navigation to matter, with hundreds of nodes and many communities, plus a high number of isolated nodes and thin communities that signal where information may still be fragmented. In other words, progressive disclosure is not just a writing style; it is a way to make a large knowledge base navigable, maintainable, and less cognitively expensive for agents.

The README frames agent-smith around a recurring failure mode: coding agents repeatedly re-derive repository knowledge from raw files, spending context on re-exploration and losing conclusions between sessions. Progressive disclosure addresses that by preventing everything from being loaded into one place. Instead, the repository is split into surfaces that answer different questions:

- `AGENTS.md` provides orientation, routing, and operational basics.
- `okf/wiki/` stores durable compiled context, evidence, and provenance.
- `.agents/skills/` stores repeatable actions and procedures.
- Harness adapters provide runtime-specific projections only.

That layering supports [[concepts/context-action-separation]], [[concepts/documentation-layer-separation]], [[concepts/agent-context-layering]], and [[concepts/context-surface-management]]. It also fits the broader idea of an [[concepts/agent-ready-repositories|agent-ready repository]]: a codebase that gives agents just enough structure to act without forcing them to ingest everything at once.

Progressive disclosure is also central to the Agent Skills specification. A skill is not a single monolithic document; it is a directory whose required `SKILL.md` carries the core instructions, while optional `scripts/`, `references/`, and `assets/` directories hold code, deeper documentation, and reusable resources. The spec explicitly describes this as progressive disclosure: metadata is loaded first, the main skill body is loaded when the skill activates, and supporting files are pulled in only on demand. That makes skills easier to scan, safer to activate, and less expensive for agents to load.

The graph report also highlights why this matters for maintenance. Core nodes such as `main()`, `bundle_key()`, `detect_orphans()`, and `OpenKB lifecycle for OKF maintenance` act as cross-community bridges, while many other nodes remain weakly connected. Progressive disclosure helps control that complexity by making the highest-signal paths obvious first and keeping deeper material available without forcing it into the initial surface.

## How the repository applies it

The repository applies progressive disclosure at both the document and workflow level:

- The high-level project story comes first, before implementation details or operational commands.
- The three portable product skills are described separately from the vendored `graphify` and `openkb` toolchain copies, so readers can distinguish what is meant to be adopted from what is only pinned for internal pipeline support.
- Installation instructions tell the user to copy only the three product skills, while the extra `.agents/skills/` contents are explicitly labeled as vendored toolchain copies.
- Maintenance instructions route the user to a simple request first, with direct commands shown only as fallback for manual or CI use.
- Air-gapped operation is described as a specialized mode, with local-provider behavior and egress constraints only introduced when relevant.
- Security and privacy notes disclose data flow, install behavior, and tool routing before any LLM-backed action occurs.
- Skill authors are encouraged to keep `SKILL.md` under 500 lines and move long reference material into separate files so the main activation surface stays compact.
- Validation is separated from authoring: the spec recommends using `skills-ref validate ./my-skill` to check naming and frontmatter rules without burdening the skill itself with enforcement logic.
- Graph analysis suggests a similar maintenance strategy for documentation itself: strongly connected hubs deserve concise entry surfaces, while isolated or thinly connected material may need either clearer linking or promotion into more deliberate concept pages.

This is not just a documentation style choice; it is a control mechanism. The system avoids premature detail, reduces accidental misuse, and keeps agent attention on the smallest useful surface at each step.

## Related ideas

Progressive disclosure is closely connected to:

- [[concepts/durable-context]] — only stable, reusable knowledge should be promoted into the wiki layer.
- [[concepts/compiled-knowledge-bases]] — compiled knowledge is meant to be navigated selectively, not dumped wholesale.
- [[concepts/orientation-routing]] — orientation files point agents toward the right surface instead of embedding everything locally.
- [[concepts/consent-first-workflows]] — agents should ask before taking actions that have side effects.
- [[concepts/non-interactive-agent-design]] — the workflow should still function when the agent cannot rely on step-by-step human supervision.
- [[concepts/context-surface-management]] — each repository surface should stay narrowly scoped so agents can move between layers deliberately.

## Source anchor

The clearest statement of this pattern appears in [[summaries/README-md]], where the repository is described as a layered system built around orientation, context, and actions, with knowledge kept out of files that are not meant to carry it.

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

## Related Documents
- [[summaries/graphify-report]]
- [[summaries/agent-skills-spec]]