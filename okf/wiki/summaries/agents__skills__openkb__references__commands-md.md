---
type: "Summary"
description: "Reference for safe OpenKB CLI usage and command restrictions."
doc_type: short
full_text: "sources/agents__skills__openkb__references__commands-md.md"
---

# OpenKB CLI reference

This document defines how an agent should safely use the OpenKB CLI, with a strong distinction between read-only inspection commands and commands that mutate the knowledge base.

## Core guidance

- Treat `openkb status` as the first command to establish the active knowledge base path before reading files.
- Prefer direct inspection commands over `openkb query` when a document or page can be located deterministically.
- Avoid interactive or background commands during autonomous operation.
- Never run write-capable OpenKB commands autonomously.
- Never directly edit files under the knowledge base's `wiki/` or `.openkb/` directories.

## Command behaviors

### `openkb status`

- Provides a knowledge base overview.
- The first output line contains the absolute path of the active knowledge base and must be parsed before any file read.
- Resolution walks upward from the current directory, then falls back to the default set by `openkb use`.
- If no knowledge base exists, it prints a setup message and the agent should stop rather than guessing paths.

This command establishes a pattern of [[concepts/knowledge-base-discovery]] and safe read-before-write workflows.

### `openkb list`

- Lists documents and concepts.
- Exposes user-facing type labels rather than raw file extensions.
- Long PDFs appear as `pageindex`; shorter documents appear as `short`.
- `Pages` is populated only for long PDFs.

This supports index-based discovery and type abstraction in CLI output.

### `openkb query "<question>"`

- Runs the full RAG pipeline.
- Incurs an internal LLM call, so it should be used only when direct reads and obvious slug matches are insufficient.
- Returns free-form text plus cited wiki paths such as `...` and `...`.
- `--save` persists the result to `wiki/explorations/<slug>.md`, but only when explicitly requested.

This frames query as a fallback mechanism within retrieval-augmented generation and [[concepts/cost-aware-tool-use]].

## Commands the skill should avoid

The document explicitly marks several read-only but unsuitable commands as off-limits for autonomous use:

- `openkb chat` because it opens an interactive REPL.
- `openkb watch` because it runs as a daemon.
- `openkb lint` unless the user explicitly asks about wiki health.

These restrictions reinforce [[concepts/non-interactive-agent-design]] and user-directed maintenance.

## Write commands forbidden for autonomous execution

The document lists mutation-capable commands that the agent must not run on its own:

- `openkb add <path>` ingests a document and modifies the wiki.
- `openkb remove <doc>` removes content destructively.
- `openkb lint --fix` auto-edits wiki pages.
- `openkb init` performs initial knowledge base setup.
- `openkb use <path>` changes the default knowledge base.

The expected behavior is to describe these commands briefly and let the user choose whether to run them. This is a clear statement of human-in-the-loop operations and write-safety boundaries.

## Important operational boundary

A final rule prohibits directly editing anything under `<kb>/wiki/` or `<kb>/.openkb/`, because these locations contain curated user knowledge and OpenKB internal state.

This establishes a strong separation between agent assistance and protected repository state, connected to knowledge-base integrity and [[concepts/tool-boundaries]].

## Takeaway

The main contribution of the document is a safety policy for OpenKB CLI usage: discover the active knowledge base first, prefer direct read paths over expensive query flows, and leave all mutating operations and curated wiki state under explicit user control.

## Related Concepts
- [[concepts/human-in-the-loop-review]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/permission-scoped-agents]]
- [[concepts/safe-automation]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/action-oriented-documentation]]
- [[concepts/agent-ready-repositories]]
- [[concepts/knowledge-boundaries]]
- [[concepts/path-safety]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/tooling-consent-and-pin-management]]

## Entities
- [[entities/openkb]]
- [[entities/pageindex]]
- [[entities/litellm]]
- [[entities/vectifyai-openkb]]
