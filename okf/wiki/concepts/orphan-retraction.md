---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md"]
description: "Deterministic removal of KB content whose source file no longer exists."
---

# Orphan Retraction

Orphan retraction is the process of removing OpenKB documents that remain in the knowledge base after their repository source has been deleted, moved, or no longer selected for staging. In the OpenKB workflow, this is the inverse of ingestion: it cleans up stale registry entries, raw copies, and derived pages so the KB stays aligned with the repository.

This concept is implemented by [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]], which drives `openkb remove` directly as the only sanctioned deterministic mutation step in the reconciliation path.

## What it covers

- Documents that were created from repository sources but no longer have a matching expected staged name.
- Pipeline-owned registry entries only; user-added external documents are excluded.
- Cleanup of orphaned `okf/raw/` copies, summary pages, and downstream concept/entity pages seeded by the removed source.
- Distinguishing between true deletion, rename/move, and deselection by the current staging rules.

## Why it matters

Without orphan retraction, the KB accumulates stale content after repository changes. That creates registry drift, misleading search results, and lingering derived pages that no longer reflect the source tree. Retraction keeps the KB consistent with [[concepts/deterministic-source-pack-staging]], [[concepts/hash-registry-coherence]], and [[concepts/source-driven-regeneration]].

## How detection works

The script first checks whether a fresh source-pack manifest exists. If so, it treats that manifest as the authority for expected staged names, while optionally cross-checking against a git-derived view for drift. If no manifest is present, it falls back to re-deriving the expected names from git-tracked files using the same selection and slugging logic as the builder.

That workflow depends on several related ideas:

- [[concepts/manifest-authoritative-reconciliation]] for preferring the built manifest over re-derivation.
- [[concepts/rename-vs-delete-detection]] for separating true deletion from path movement.
- [[concepts/source-pack-manifest]] for the staged-name inventory that anchors reconciliation.
- [[concepts/git-tracking-policy]] for deciding what the repository still owns.

## Orphan categories

- `deleted` - the repository path is gone, so the KB page has no source file left to point to.
- `renamed` - the content still exists under a new path, identified by comparing content hashes.
- `deselected` - the file still exists in git, but the current selection policy would no longer stage it.

Only `deleted` and `renamed` entries are automatically removable. `deselected` entries are reported but left for explicit human confirmation because they may reflect an intentional policy change rather than a source removal.

## Safety model

Orphan retraction is intentionally conservative and aligns with [[concepts/safe-automation]] and [[concepts/read-only-kb-operations]] as long as it is only reporting. When applying changes, it uses guardrails to prevent accidental mass deletion:

- Rejects non-pipeline documents by checking for the staging marker.
- Ignores pseudo-documents that are always regenerated, such as `repo-snapshot` and `graphify-report`.
- Refuses to auto-apply if too many documents appear orphaned, which usually signals a stale manifest or wrong bundle depth.
- Requires explicit `--apply` and `--yes` for destructive action.

## Key implementation detail

Rename detection uses the content hash of the previous committed file to see whether the same text has reappeared at another path. When that happens, `openkb remove --keep-empty` is used so shared derived pages are not prematurely discarded if the new document will repopulate them.

## Related ideas

- [[concepts/source-grounded-regeneration]] - regenerated knowledge should stay tied to source state.
- [[concepts/source-provenance]] - the origin of a KB page determines whether it should persist.
- [[concepts/deterministic-validation]] - reconciliation is designed to be repeatable and predictable.
- [[concepts/registry-drift]] - orphan retraction is a corrective response to registry mismatch.
- [[concepts/knowledge-lifecycle-governance]] - documents move through creation, retention, and removal policies.

## Practical effect

Orphan retraction closes the loop in the repository-to-KB lifecycle. It is the mechanism that prevents deleted or moved repository files from leaving behind stale OpenKB state, while preserving manual and externally sourced content that the pipeline did not create.