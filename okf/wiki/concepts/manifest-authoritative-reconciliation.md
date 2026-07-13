---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md"]
description: "Using the built manifest as the authority for reconciliation decisions."
---

# Manifest-Authoritative Reconciliation

Manifest-authoritative reconciliation is a workflow pattern where a freshly built manifest is treated as the source of truth for deciding what should exist, even when the current repository state can also be re-derived locally. It reduces drift between a build pipeline and cleanup logic by making both sides agree on the same staged document set.

This concept appears in [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]], where the orphan-pruning script prefers `source-pack-manifest.json` when it exists. The manifest is used verbatim to determine the expected staged names and the source-path mapping for newly generated documents. Only when the manifest is absent does the script fall back to reconstructing expectations directly from git-tracked files.

## Why it matters

- It keeps cleanup logic aligned with the builder that created the KB artifacts.
- It avoids re-deriving selection and slugging rules in multiple places when a manifest is available.
- It makes reconciliation safer by reducing the chance that cleanup and build disagree about which documents belong in the KB.
- It supports deterministic recovery after repository changes, especially when deletions or renames have occurred.

## How it works in practice

The orphan-pruning script first checks for a manifest produced by the source-pack build. If present, it:

- reads the staged names directly from the manifest,
- uses the manifest's source-hash-to-path mapping when checking for renames,
- treats the manifest as authority even if the live repository would produce a different answer,
- emits an advisory when the manifest and current repository disagree.

If the manifest is missing, the script falls back to [[concepts/source-pack-staging]] and repo-derived name reconstruction using the same selection and slug rules as the builder. That fallback is a compatibility path, not the preferred mode.

## Related ideas

- [[concepts/source-pack-manifest]] — the manifest that carries the authoritative staged-document inventory.
- [[concepts/deterministic-builds]] — manifests only work well when the build is reproducible.
- [[concepts/manifest-authoritative-reconciliation]] — this page's core pattern for cleanup and drift handling.
- [[concepts/registry-drift]] — the failure mode this pattern helps detect and contain.
- [[concepts/orphan-retraction]] — the downstream action taken once a document is identified as stale.
- [[concepts/rename-vs-delete-detection]] — distinguishing true removal from path moves during reconciliation.
- [[concepts/hash-registry-coherence]] — keeping registry entries consistent with staged source truth.

## Source tie-in

The script's design shows a narrow but important rule: when a curated build artifact exists, cleanup should trust that artifact instead of guessing from the repository. That makes the pipeline more robust, especially when the current repo view is incomplete, stale, or otherwise out of sync with the KB state.