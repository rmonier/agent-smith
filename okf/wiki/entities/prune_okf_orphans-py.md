---
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Work"
description: "Repository maintenance script that prunes orphaned OpenKB documents."
---

# prune_okf_orphans.py

`prune_okf_orphans.py` is a repository maintenance script in `.agents/skills/agent-ready-context/scripts/` that reconciles the OpenKB hash registry with the current repository state and retracts KB documents whose source files have disappeared.

## What it does

- Scans `okf/.openkb/hashes.json` for pipeline-owned documents created through the staged source-pack flow.
- Compares registry entries against the set of documents the current repository should still stage.
- Classifies missing entries as `deleted`, `renamed`, or `deselected`.
- Uses `openkb remove` to retract orphaned documents, optionally with `--keep-empty` for rename cases.
- Defaults to report-only mode, with `--preview` for dry-run plans and `--apply` for execution.
- Is invoked during the agent-ready workflow before ingestion so deletions are reconciled first.
- Appears in graph analysis as a bridge between source-pack staging and the broader skill-maintenance workflow.

## Why it matters

The script closes the loop in [[concepts/orphan-retraction]] for the OpenKB ingestion pipeline. It prevents stale raw files, summary pages, and downstream concept or entity pages from lingering after repository deletions or moves, supporting [[concepts/hash-registry-coherence]] and [[concepts/manifest-authoritative-reconciliation]].

It also reflects the broader agent-ready workflow: keep generated context under `okf/.okf-build/input/`, treat `okf/wiki/` as the durable knowledge source, and use deterministic validation and mutation paths instead of hand-editing compiled pages. The graph report also places it near [[concepts/source-pack-staging]], [[concepts/source-pack-manifest]], and [[concepts/deterministic-source-pack-staging]] behavior.

## Key behaviors

- Prefers the current source-pack manifest when available, so orphan detection stays aligned with the builder.
- Falls back to git-based reconstruction when no manifest exists.
- Mirrors the builder's selection and slugging logic to avoid drift.
- Treats pseudo-documents like `repo-snapshot` and `graphify-report` as non-orphans.
- Rejects bulk retraction when the orphan set looks suspiciously large, acting as a safety check against a wrong repo, wrong KB, or bundle-depth mismatch.
- Integrates with the agent-ready-context policy that staging and reconciliation stay deterministic and locally driven.
- Relies on `openkb remove` as the only deterministic, LLM-free OpenKB mutation for this task.
- Acts as a cross-community bridge in the graph, connecting build utilities to skill and maintenance tooling.

## Notable implementation details

- It reads source paths from the orphaned document's raw staged copy when possible, because reversing slugs is not always lossless.
- It uses content hashes to distinguish a true deletion from a rename or move.
- It only targets documents marked as pipeline-owned, leaving user-added content alone.
- It sits within a skill that treats `okf/.openkb/hashes.json` as a dedupe registry and warns that registry drift can cause later `add` runs to skip content silently.
- It is part of the documented deletion-reconciliation step that runs report-only first and only applies after consent.
- The graph report links it to `main()` as part of a larger maintenance path, suggesting it is one of the key nodes in the OpenKB lifecycle.

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[entities/openkb-remove]]
- [[entities/openkb-cli]]
- [[entities/build_okf_source_pack-py]]
- [[entities/prune-okf-orphans-py]]
- [[concepts/source-pack-manifest]]
- [[concepts/source-pack-staging]]
- [[concepts/registry-drift]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/safe-automation]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/hash-registry-coherence]]
- [[concepts/orphan-retraction]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/read-only-kb-operations]]
- [[concepts/deterministic-validation]]
- openkb workflow governance

## Related Documents

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/graphify-report]]