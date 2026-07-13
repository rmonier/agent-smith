---
type: "Summary"
description: "How to clone GitHub repos and merge Graphify outputs into one graph."
doc_type: short
full_text: "sources/agents__skills__graphify__references__github-and-merge-md.md"
---

# Summary

This reference explains how to use Graphify when the input is one or more GitHub repositories, or several local subfolders that should be combined into a single graph.

## Main points

- Use this workflow when the user provides `https://github.com/...` URLs or asks to merge several local code folders into one Graphify graph.
- For a single GitHub repository, run `graphify clone <github-url> [--branch <branch>]` and use the returned local path for the rest of the pipeline.
- For multiple repositories, clone each repo, run the normal Graphify pipeline on each one to produce separate `graph.json` files, then combine them with `graphify merge-graphs`.
- Graphify stores cloned repositories under `~/.graphify/repos/<owner>/<repo>` and reuses those clones on repeated runs.
- In merged outputs, each node includes a `repo` attribute so the resulting graph can be filtered by repository origin.

## Multiple local subfolders

The document distinguishes local multi-folder projects from multi-repo workflows.

- The skill pipeline writes outputs to a shared `graphify-out/` in the current working directory.
- Running the skill separately on several subfolders would overwrite that shared output.
- To avoid clobbering, run `graphify extract` directly on each subfolder instead.
- Direct CLI extraction writes `graphify-out/` inside each scanned folder, such as `./core/graphify-out/graph.json`.
- After extracting each subfolder, merge those graphs at the project root with `graphify merge-graphs`.

## Operational guidance

- For local subfolder extraction, the backend can be selected with `--backend gemini|kimi|openai|deepseek|claude-cli`, depending on available API credentials.
- After a merged `graphify-out/graph.json` exists, later codebase questions can use the fast path by querying the merged graph directly.
- This avoids re-extraction and bypasses the normal size-gating behavior once the merged graph has already been built.

## Key ideas

- [[concepts/repository-ingestion]]
- [[concepts/graph-merging]]
- [[concepts/repo-scoped-graph-partitioning]]

## Takeaway

The reference provides a practical branching workflow for single-repo, multi-repo, and multi-subfolder Graphify usage, with special emphasis on preventing output collisions and producing a reusable merged graph for later querying.

## Related Concepts
- [[concepts/incremental-graph-maintenance]]
- [[concepts/path-based-validation]]
- [[concepts/action-oriented-documentation]]
- [[concepts/cross-platform-tooling]]
- [[concepts/graceful-degradation]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/offline-first-workflows]]
- [[concepts/preflight-checks]]
- [[concepts/repo-navigation]]
- [[concepts/safe-automation]]
- [[concepts/skill-based-automation]]
- [[concepts/source-provenance]]

## Entities
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/github-copilot]]
- [[entities/openkb]]
- [[entities/uv]]
