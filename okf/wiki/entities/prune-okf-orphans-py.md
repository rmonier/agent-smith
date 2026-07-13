---
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md"]
type: "Work"
description: "OpenKB reconciliation script for pruning orphaned KB documents"
---

# prune_okf_orphans.py

`prune_okf_orphans.py` is a repository-side maintenance script that reconciles an OpenKB knowledge base with the current git tree by finding pipeline-owned documents whose source files no longer exist and retracting them with `openkb remove`.

## What it does

- Reads the KB registry from `.openkb/hashes.json` and filters to documents produced by this pipeline's staging flow.
- Ignores pseudo-documents such as `repo-snapshot` and `graphify-report`, which are always regenerated.
- Determines the expected staged names from the source-pack manifest when available, or falls back to git-based derivation.
- Classifies stale entries as deleted, deselected, or renamed based on repository state and content hashes.
- Uses `openkb remove` as the deterministic inverse of ingestion, with no LLM call.

## Operational behavior

- Default mode is report-only.
- `--preview` shows the per-page `openkb remove --dry-run` plan.
- `--apply` performs the retraction, and `--yes` confirms non-interactive execution.
- A safety guard blocks suspiciously large retraction sets, which usually indicates a bundle-depth mismatch or wrong target.
- Deselect cases are reported but not auto-removed, since they may reflect an intentional selection-policy change.

## Key implementation ideas

- Mirrors the selection, slugging, and bundling rules from `build_okf_source_pack.py` so orphan detection stays aligned with ingestion.
- Prefers a freshly built staging manifest as the authority when present, while still issuing an advisory if it disagrees with the current repo.
- Uses git history plus content hashing to distinguish a rename from a true deletion.
- Treats manual, non-pipeline OpenKB additions as out of scope.

## Related concepts

- [[concepts/orphan-retraction]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/hash-registry-coherence]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/safe-automation]]
- [[concepts/source-pack-staging]]
- [[concepts/registry-drift]]
- [[concepts/deterministic-validation]]

## Related pages

- [[entities/openkb]]
- [[entities/build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

## Why it matters

The script prevents stale KB content from lingering after repository deletions while preserving manual documents and reducing the risk of accidental bulk removals.