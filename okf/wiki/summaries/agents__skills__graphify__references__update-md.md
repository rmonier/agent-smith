---
type: "Summary"
description: "Incremental and cluster-only rules for updating Graphify outputs."
doc_type: short
full_text: "sources/agents__skills__graphify__references__update-md.md"
---

# Summary

This document defines the special update flow for Graphify when invoked with `--update` or `--cluster-only`, rather than a first-time full build. Its main purpose is to make [[concepts/incremental-graph-maintenance]] cheaper, safer, and more accurate by reprocessing only changed inputs and preserving the existing graph correctly.

## Key Points

- `--update` triggers [[concepts/incremental-compilation]]: Graphify detects newly added, modified, and deleted files since the last manifest and writes the result to `.graphify_incremental.json`.
- The incremental state is then copied into `.graphify_detect.json` so later pipeline steps, which always read that file, operate on the changed subset while still retaining full-corpus context via `all_files`.
- A fast path for code-only changes exists: if every changed file has a recognized code extension, Graphify skips semantic extraction and LLM/subagent work, runs only AST processing, then merges and continues with downstream graph steps.
- If any changed file is non-code, the normal semantic pipeline runs. For changed video files specifically, transcription must happen first so raw media paths are replaced with transcript paths before semantic extraction.
- Deletions-only updates create an empty extraction file so the merge phase can still prune removed sources from the graph.

## Merge Behavior

The document gives detailed merge rules for [[concepts/graph-merging]]:

- Before merging, the old graph is backed up to `.graphify_old.json`.
- The merge uses `build_merge()` directly against `graphify-out/graph.json` to avoid lossy graph reconstruction and to preserve directed edge semantics.
- `prune_sources` must include only genuinely deleted files, not changed files, because changed sources are replaced through re-extraction logic.
- `root='INPUT_PATH'` is required so source paths are relativized consistently during pruning and manifest saving.
- The `directed` flag must match the invocation mode; otherwise a directed incremental update can silently collapse into an undirected graph.
- Hyperedges are preserved from both the existing graph and the new extraction when writing the merged output back to `.graphify_extract.json`.

## Incremental Correctness Concerns

The file emphasizes several correctness safeguards tied to prior bug reports:

- Re-extracted changed files should replace stale content rather than be additionally pruned.
- Deleted files must be pruned using paths relativized to the same root as stored graph metadata.
- Manifest saving after merge is necessary so future updates diff against the latest state rather than an outdated baseline.
- Video inputs require transcript substitution before semantic extraction to avoid feeding unreadable media paths into downstream agents.
- Graph diff output after Step 4 provides a lightweight verification layer by reporting summary changes, new nodes, and new edges.

## For `--cluster-only`

`--cluster-only` is treated as a self-contained reclustering operation:

- Steps 1–3 are skipped.
- The command `graphify cluster-only .` re-clusters the existing graph, renames communities, and regenerates `GRAPH_REPORT.md`, `graph.json`, and `graph.html`.
- Steps 5–9 must not be re-run afterward because cleanup from prior builds may already have removed intermediate files those steps expect.
- The expected final user-facing output is the refreshed `GRAPH_REPORT.md` summary.

## Related Concepts
- [[concepts/transcription-pipeline-design]]
- [[concepts/source-provenance]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/action-oriented-documentation]]
- [[concepts/deterministic-builds]]
- [[concepts/graceful-degradation]]

## Entities
- [[entities/graphify]]
- [[entities/graphifyy]]
