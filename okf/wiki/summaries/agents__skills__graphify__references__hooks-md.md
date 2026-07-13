---
type: "Summary"
description: "Explains graphify hook installation and AGENTS.md integration options."
doc_type: short
full_text: "sources/agents__skills__graphify__references__hooks-md.md"
---

# Graphify hook and AGENTS.md integration

This document explains two ways to make `graphify` run automatically in a project: a Git post-commit hook and native `AGENTS.md` integration.

## Key points

- `graphify hook install` adds a post-commit hook that rebuilds graph artifacts after each `git commit`.
- The hook checks changed code files using `git diff HEAD~1`, re-runs AST extraction for those files, and rebuilds `graph.json` and `GRAPH_REPORT.md`.
- Documentation and image changes are ignored by the hook; those require a manual `/graphify --update` run.
- If a post-commit hook already exists, graphify appends its behavior instead of overwriting the hook.
- `graphify agents install` writes a `## graphify` section into the local `AGENTS.md` so agent sessions automatically consult and refresh the graph.
- `graphify agents uninstall` removes that section when the integration is no longer wanted.

## Operational implications

The post-commit hook provides lightweight automation for code graph maintenance without requiring a persistent background service. Its scope is intentionally limited to code-file updates, which keeps runs targeted but leaves non-code graph inputs to manual refresh.

The `AGENTS.md` path provides agent workflow integration by embedding expectations directly into the repository's agent instructions. This makes graph usage part of normal code-assistance behavior rather than a separate command the user must remember.

## Related concepts

- git hooks
- code graph maintenance
- ast based analysis
- automation
- agent workflow integration

## Related Concepts
- [[concepts/incremental-graph-maintenance]]
- [[concepts/agents-md-maintenance]]
- [[concepts/safe-automation]]
- [[concepts/action-oriented-documentation]]
- [[concepts/agent-ready-repositories]]
- [[concepts/documentation-architecture]]
- [[concepts/graph-merging]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/repo-navigation]]
- [[concepts/skill-based-automation]]

## Entities
- [[entities/graphify]]
- [[entities/agents-md]]
