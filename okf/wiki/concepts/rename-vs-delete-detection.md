---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md"]
description: "Heuristics for telling a moved source from a true deletion during reconciliation."
---

# Rename vs Delete Detection

Rename vs delete detection is the process of deciding whether a missing repository source should be treated as a true deletion or as a move to a new path. In the OpenKB reconciliation flow, this distinction matters because deletion should retract stale KB content, while a rename should preserve continuity and avoid over-pruning shared derived pages.

This concept is central to [[concepts/orphan-retraction]] and appears in the orphan reconciliation script documented in [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]].

## Why it matters

Repository changes are not always simple removals. A file can disappear from one path and reappear elsewhere with the same content. If a pipeline assumes deletion too early, it can remove KB pages that are still valid. If it assumes rename too often, it can leave stale content behind.

The goal is to classify missing sources conservatively, using evidence from git and the KB registry before invoking destructive operations.

## How the detection works

The script uses a layered decision process:

1. Check whether the staged document name is still expected from the current repository.
2. Resolve the original repository path from the orphan's raw staged copy when possible.
3. Determine whether that path still exists in git-tracked files.
4. If the path is gone, compare content hashes from git history against newly staged content.
5. If the content matches a new path, classify the orphan as a rename rather than a deletion.

This lets the system distinguish between:

- a file that was removed and has no replacement, and
- a file that moved but still represents the same underlying content.

## Signals used

### Path existence
If the source path still exists in the tracked repository, the missing KB entry is usually treated as deselected rather than deleted. That means the file is still present but no longer selected by the source-pack rules.

### Content identity
For missing paths, the script computes a content hash from the last committed version of the old path and compares it to hashes for current staged sources. A match suggests the document was renamed or moved.

### Raw staged metadata
The script prefers the `source_path` recorded in the orphan's raw staged copy instead of reversing the slugged staged name. This is important because slug reversal can be lossy for paths containing `__`.

## Rename handling

When the script identifies a rename, it marks the orphan for removal with `--keep-empty`. That preserves empty shared structures when the replacement document is expected to repopulate them.

This behavior reflects a broader [[concepts/conservative-document-merging]] and [[concepts/safe-automation]] approach: make the cleanup precise, but do not over-delete derived structures that may still be needed.

## Failure modes and safeguards

Rename-vs-delete logic is easy to get wrong, so the script includes guardrails:

- It prefers a freshly built manifest when available, to reduce drift.
- It falls back to git-derived staging only when necessary.
- It emits advisories when manifest and repository expectations disagree.
- It refuses large-scale automatic cleanup when the orphan set looks suspiciously broad.

These checks support [[concepts/manifest-authoritative-reconciliation]], [[concepts/registry-drift]], and [[concepts/deterministic-validation]].

## Related ideas

- [[concepts/source-pack-manifest]] - authoritative expected document names when present
- [[concepts/deterministic-source-pack-staging]] - keeping staging rules aligned with the builder
- [[concepts/hash-registry-coherence]] - matching registry entries to current repository state
- [[concepts/path-safety]] - avoiding unsafe or ambiguous path interpretation
- [[concepts/source-grounded-regeneration]] - preferring source evidence over inference

## Practical takeaway

Rename detection should be treated as an evidence-based exception to deletion. The safest workflow is to classify a missing source as deleted only after path checks fail and content continuity cannot be established. That keeps OpenKB cleanup accurate while preserving continuity across repository moves.