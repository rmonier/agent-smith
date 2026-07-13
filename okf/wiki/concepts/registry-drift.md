---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Registry drift is a mismatch between OpenKB's registry and generated wiki state."
---

# Registry Drift

Registry drift is the state where OpenKB's hash registry says a document is still ingested, but the corresponding `okf/raw/`, `summaries/`, or generated wiki pages are missing, stale, or out of sync. It is a lifecycle failure that can make knowledge disappear, stop updating, or become permanently stuck even though the source content still exists.

This concept is central to [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], which treats the registry and wiki as one coupled system that must be repaired together. It also sits inside the broader lifecycle of [[concepts/manifest-authoritative-reconciliation]], [[concepts/hash-registry-coherence]], and [[concepts/source-driven-regeneration]]. The orphan-pruning script in `agents__skills__agent-ready-context__scripts__prune_okf_orphans-py` is the deletion-side companion to that lifecycle: it compares the registry against current repository expectations and uses `openkb remove` to retract stale documents when their source files are gone, renamed, or no longer selected.

## Why it matters

OpenKB deduplicates ingested material by hash through `okf/.openkb/hashes.json`. If that registry still claims a document is present, later `openkb add` operations may silently skip the source, so a broken wiki state can persist indefinitely. Lost pages do not heal themselves, and the KB can stop reflecting the repository without an obvious failure.

Registry drift is especially dangerous after merges, reverts, interrupted ingests, or hand edits under `okf/`, because the registry and generated pages are supposed to move in lockstep. A mismatch can leave stale knowledge in place, prevent regeneration of pages that should exist, or make future adds no-ops even when the source is still available.

The lifecycle reference also warns that the registry can become a permanent blind spot: if `hashes.json` says a document is already ingested but its wiki pages were lost, subsequent `add` runs skip it and the hole never heals on its own. The orphan-retraction flow addresses the opposite failure mode as well: when the repository source disappears, the registry can still hold onto now-invalid documents unless they are explicitly removed.

## Typical symptoms

- `hashes.json` lists a document, but its wiki pages are gone.
- `okf/raw/` exists without matching generated pages.
- A later ingest appears to do nothing because the content hash is already registered.
- Validation reports hint at registry, raw, and wiki incoherence.
- After a merge or revert touching `okf/`, the wiki and registry no longer agree on what should exist.
- Repository files were deleted or renamed, but the KB still contains the old documents because no inverse removal ran.

## Recovery paths

The lifecycle reference recommends two main repairs:

- If `okf/raw/` still contains the source, use `openkb recompile` to regenerate the wiki pages.
- If raw is gone too, use `openkb remove` first to clear the registry entry, then re-`add` the source.

For deleted, moved, or deselected repository sources, the preferred fix is to rebuild the source pack and run the reconciliation flow before adding new input, so stale pages are removed before fresh ones are compiled. `openkb remove` is the deterministic inverse of ingestion: it prunes source references, deletes pages whose only source was removed, updates `index.md`, clears the registry hash, and runs scoped lint fixes. The orphan-pruning script automates that reconciliation for pipeline-owned content, with report-only, preview, and apply modes, plus a safety guard that refuses mass removal when the invocation looks inconsistent.

The script also distinguishes between three cleanup cases:

- `deleted` - the repository path is gone
- `renamed` - the content still exists under a different path, detected by comparing content hashes
- `deselected` - the file still exists, but current selection rules no longer include it

That distinction matters because not every orphan should be retracted the same way. Renames can preserve downstream pages with `--keep-empty`, while deselected files usually indicate a policy or bundle-depth change rather than content loss. The script also treats manifest-backed source packs as authoritative when available, and falls back to git-based derivation only when the manifest is absent.

The document also recommends running `openkb lint` after any merge, revert, or conflict resolution touching `okf/`, and actually reading the report rather than treating it as a cosmetic check. In practice, the structural validator is the pass/fail gate, while `openkb lint` is the health report that can reveal registry drift, broken wikilinks, and other coherence failures.

## Related ideas

Registry drift is closely tied to [[concepts/hash-registry-coherence]], [[concepts/incremental-compilation]], [[concepts/source-driven-regeneration]], [[concepts/orphan-retraction]], [[concepts/okf-validation]], and [[concepts/provenance-tracking]]. It also connects to [[concepts/wikilink-integrity]] because stale registry state often surfaces as broken or missing navigation paths in the compiled wiki. It is also part of the boundary between source-driven regeneration and cleanup-oriented reconciliation, where the system must remove documents as reliably as it adds them.

## Practical rule

Treat `okf/.openkb/hashes.json` and `okf/wiki/` as one unit: never hand-edit either, and never merge, revert, or restore one without the other. After any operation that can desynchronize them, verify the registry, raw copies, and wiki pages together instead of assuming one source of truth can repair the rest automatically. When repository files are removed or renamed, run the orphan-retraction flow promptly so the KB does not accumulate stale documents that future ingests will never touch.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
