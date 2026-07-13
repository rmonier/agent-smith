---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Keeps generated KB output out of its own ingestion and graph inputs."
---

# Self-Reference Control

Self-reference control is the practice of keeping generated knowledge artifacts out of the pipelines that produce them, so a wiki or graph never becomes its own source of truth. In the OpenKB workflow, this means the KB root `okf/` stays outside the repository graph and remains a boundary rather than an input, while deletion reconciliation also stays outside the normal LLM-driven compilation flow.

## What it protects against

The workflow guards against several failure modes that appear when wiki output is allowed to feed back into the repository analysis pipeline:

- **No fixed point** - if wiki output re-enters the graph on every build, unchanged input can still produce changed output, so incremental compilation never stabilizes.
- **Circular grounding** - pages about the wiki end up citing report output that was itself generated from the wiki, which breaks provenance chains.
- **Discovery pollution** - generated pages begin to outnumber source material, so graph queries return summaries of the repo instead of the repo itself.
- **Hash churn** - if staged artifacts embed run-dependent data such as `HEAD` or timestamps, the source pack changes even when the underlying content has not.
- **Deletion feedback loops** - cleanup logic that re-ingests the wiki instead of reconciling against the repository can create orphaned pages or accidental retractions.

## How the workflow enforces it

The source pack builder, graph workflow, and orphan-retraction tooling all encode this boundary explicitly:

- `build_okf_source_pack.py` refuses to stage a graph report that appears to reference the KB root too heavily, preventing a self-referential ingestion loop.
- The builder strips generated timestamp noise from `GRAPH_REPORT.md` so unchanged analysis output does not churn staged hashes.
- It stages a repository snapshot and selected source files with normalized text, stable SHA-256 content hashes, and last-touch commit provenance, but it does not stamp the snapshot with the current `HEAD` commit.
- `source_commit` is derived from the newest commit that touched each file, so provenance changes only when the file itself changes.
- `.graphifyignore` must exclude the KB root `okf/`, keeping the compiled wiki out of graph extraction entirely.
- Graphify can still be run for one-off analysis against `okf/wiki/`, but that analysis must remain separate from the ingestion pipeline.
- The committed wiki is self-describing through `okf/wiki/index.md`, `okf/wiki/AGENTS.md`, and `sources:` chains, so it does not need to be part of the source graph.
- The workflow also requires graph and wiki operations to stay ordered: graph refresh first, then source packing, then ingestion, so the KB never recompiles against a stale structural view.
- If Graphify is unavailable or fails, the pipeline can continue without it, but the self-reference boundary still applies; the wiki must not be pulled into the graph by accident.
- `prune_okf_orphans.py` applies the same boundary in reverse: it reconciles the KB registry against the repository, treats only pipeline-owned entries as eligible, and retracts stale documents when their source files disappear.
- That orphan pruner prefers a fresh source-pack manifest when available, falls back to git-derived staging rules when necessary, and uses `openkb remove` as the deterministic inverse of ingestion.
- Its safety guard refuses to auto-apply when too many documents appear orphaned at once, which helps catch stale manifests, wrong bundle depths, or mistaken repository targets before destructive cleanup.
- Rename detection in the pruner uses content hashes to distinguish a move from a true deletion, so retractions can preserve shared downstream pages with `--keep-empty` when a replacement document already exists.
- The pruner also excludes pseudo-documents such as `repo-snapshot` and `graphify-report`, because they are regenerated artifacts rather than repository-backed sources.
- The same boundary is reinforced in the broader agent-ready workflow by keeping `okf/.okf-build/` as deterministic staging space, avoiding direct writes to `okf/raw/` or `okf/wiki/`, and treating `okf/.openkb/hashes.json` as a dedupe registry that can silently suppress re-ingestion if it drifts from the wiki.

## Related ideas

Self-reference control overlaps with [[concepts/self-referential-ingestion-loops]], [[concepts/knowledge-graph-feedback-loops]], [[concepts/repo-scoped-graph-partitioning]], and [[concepts/generated-content-governance]]. It also depends on [[concepts/local-vs-shared-ignore]] for the ignore-file boundary and on [[concepts/deterministic-builds]] for stable, repeatable outputs. It is closely tied to [[concepts/graph-integrity-diagnostics]], [[concepts/source-pack-staging]], [[concepts/source-provenance]], [[concepts/source-pack-manifest]], [[concepts/incremental-graph-maintenance]], [[concepts/orphan-retraction]], [[concepts/manifest-authoritative-reconciliation]], and [[concepts/rename-vs-delete-detection]] because each of those assumes the graph does not absorb its own generated wiki and can be cleaned back to source truth safely.

## Why it matters

Without this boundary, the build loses determinism and the wiki starts compounding its own artifacts. With it, the repository keeps a clean separation between source material, staged inputs, compiled knowledge, and any one-off analysis of the wiki itself. The same separation also makes it safe to remove stale KB content when repository files are deleted or renamed, without turning cleanup into another source of drift.

## Source

This concept is grounded in [[summaries/agents__skills__agent-ready-context__references__workflow-md]], [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]], and [[summaries/agents__skills__agent-ready-context__SKILL-md]].

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]