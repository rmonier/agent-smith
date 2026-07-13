---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"]
description: "Bounded file regions automation can update without owning the whole document."
---

# Managed Document Sections

Managed document sections are bounded blocks inside a larger file that automation may update without taking ownership of the entire document. The pattern lets a tool maintain a specific region while preserving surrounding human-authored content.

This concept appears in `merge_agents_md_okf_section.py`, which inserts or replaces a guidance block inside `AGENTS.md` using HTML comment markers. The script is intentionally conservative: it only edits the managed section and leaves repository-specific setup, policy, and instructions untouched.

The same idea also shows up in the subagent/profile adapter workflow, where generated harness-specific files should stay short and delegate most context to `AGENTS.md`, `okf/wiki/`, and reusable skills. In that setting, a managed section acts as a narrow, replaceable projection layer rather than a place to store durable project knowledge.

## Core Pattern

A managed section usually has three parts:

- a start marker
- the generated or maintained content block
- an end marker

In this source, the markers are `<!-- okf:start -->` and `<!-- okf:end -->`. The script uses them to locate the section that belongs to OpenKB guidance and to avoid rewriting the rest of the file.

The same marker-driven approach fits harness adapter generation: the adapter can be rewritten when runtime details change, while the surrounding repo guidance stays stable.

## Why It Matters

Managed sections support [[concepts/conservative-document-merging]] and [[concepts/documentation-layer-separation]] by making it possible to combine stable automation output with local edits. They also reduce accidental drift in files that serve both as human orientation documents and machine-maintained indexes.

This is especially useful for [[concepts/agents-md-maintenance]], where `AGENTS.md` must stay concise and current while still preserving repository-specific rules. It is also important for [[concepts/runtime-adapter-management]], where subagent/profile adapters should remain runtime-specific projections instead of becoming a source of truth.

## Key Properties

- The managed block is replaceable by automation, but the rest of the file is preserved.
- The section is meant to be a routing layer, not the full knowledge base.
- The technique is marker-driven and deterministic.
- The update behavior is conservative: replace, append, or initialize depending on file state.
- The surrounding file can still carry human policy, repo orientation, or harness notes.
- The pattern works best when the generated block stays short and points outward to deeper context.

## Source Example

In `merge_agents_md_okf_section.py`, the managed section encodes operational guidance such as:

- read `AGENTS.md` first for local rules and setup
- use `okf/wiki/index.md` to reach compiled wiki context
- consult `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as structural maps
- use `.agents/skills/` for reusable automation skills
- prefer `uv run` for bundled scripts
- keep compiled wiki pages read-only
- capture durable facts as findings rather than editing compiled pages directly

The summary page for that script is [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]].

The subagent/profile adapter document extends this pattern into runtime-specific files: it recommends short native adapter files that point back to repo orientation and wiki context, plus explicit validation that generated files do not leak project knowledge into harness-specific outputs.

## Related Ideas

- [[concepts/documentation-architecture]] for how different document layers serve different purposes
- [[concepts/documentation-cohesion]] for keeping guidance aligned across files
- [[concepts/generated-content-governance]] for rules around machine-authored text
- [[concepts/orientation-routing]] for using one file to point to the next source of truth
- [[concepts/context-action-separation]] for keeping routing, instructions, and durable knowledge distinct
- [[concepts/runtime-adapter-management]] for generated harness-specific projections

## Practical Use

This pattern is useful when a file must remain partly hand-edited and partly machine-maintained. It gives automation a safe insertion point and gives humans confidence that local additions will survive refreshes outside the managed block.

It is especially valuable in repo-maintenance flows where `AGENTS.md` or harness adapters need periodic regeneration, because it keeps updates localized, predictable, and easy to validate.

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
