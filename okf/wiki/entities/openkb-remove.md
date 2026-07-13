---
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md"]
type: "Work"
description: "OpenKB command that retracts KB documents from the registry"
---

# openkb remove

`openkb remove` is the OpenKB command that retracts documents from a knowledge base registry. In this repository it is treated as the inverse of `openkb add`: when a source file disappears or is no longer supposed to be ingested, `remove` cleans up the corresponding KB entry and its derived pages.

## What it does

- Removes a KB document by `doc_name` from the OpenKB registry.
- Prunes the associated source metadata and derived pages in a deterministic way.
- Supports `--dry-run` for previewing the page-level plan before mutation.
- Supports `--keep-empty` when a renamed source should preserve shared downstream pages.
- Supports `--yes` to apply the retraction non-interactively.

## Why it matters

The script [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]] uses `openkb remove` as the only direct OpenKB mutation in the cleanup path. That choice depends on the command being deterministic and not requiring an LLM call, which makes it suitable for safe automation and [[concepts/orphan-retraction]].

## Key behavior in this workflow

- Only pipeline-owned documents are eligible for retraction; manually added external documents are excluded.
- Pseudo-documents such as `repo-snapshot` and `graphify-report` are never considered orphans.
- The command is used in three modes: report-only, preview, and apply.
- The orphan-pruning flow distinguishes deleted files, renamed files, and deselected files before deciding whether to call `remove`.

## Related concepts

- [[concepts/orphan-retraction]]
- [[concepts/safe-automation]]
- [[concepts/hash-registry-coherence]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/read-only-kb-operations]]

## Related entities

- [[entities/openkb]]
- [[entities/openkb-add]]
- [[entities/openkb-lint]]
- [[entities/openkb-cli]]