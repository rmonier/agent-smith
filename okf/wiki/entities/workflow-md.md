---
sources: ["summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Work"
description: "Repository workflow reference for the OKF/OpenKB lifecycle"
---

# .agents/skills/agent-ready-context/references/workflow.md

`.agents/skills/agent-ready-context/references/workflow.md` is a repository workflow reference that defines how to build, ingest, validate, refresh, and curate the OpenKB OKF wiki from a source repository.

## What it covers

- The required build order for the OKF pipeline, from prerequisite checks through ingestion, validation, and post-generation review.
- Deterministic staging rules for source packs and the handling of Git history, line endings, and ignore files.
- How to use `graphify` and `openkb` in a consent-first, provenance-aware way.
- How to reconcile deleted or moved sources before ingest so stale wiki pages do not persist.
- How to treat the hash registry, raw copies, and wiki pages as one coherent lifecycle unit.
- How to review generated wiki output for missing concepts, duplicates, misclassified entities, truncation, stale findings, and output-only curation cases.
- How to keep the wiki out of the repo graph so the knowledge base does not become self-referential.

## Key ideas

- [[concepts/deterministic-builds]]: the source pack is designed to be stable across commits.
- [[concepts/provenance-tracking]]: staged input and external evidence must remain grounded in source material.
- [[concepts/self-reference-control]]: the wiki must not be included in the repo graph.
- [[concepts/consent-first-workflows]]: optional tooling and bootstrap steps require user approval when needed.
- [[concepts/deterministic-validation]]: structural validation is separated from LLM-backed health reporting.
- [[concepts/orphan-retraction]]: removed or moved sources should be reconciled before ingest.
- [[concepts/wiki-review-gates]]: post-generation review is required before accepting new wiki output.
- [[concepts/registry-drift]]: hash registry coherence must be preserved across merges and recoveries.
- [[concepts/findings-promotion]]: discovered knowledge can be captured in findings and later promoted into compiled truth.
- [[concepts/editorial-curation-passes]]: some output-only wiki cleanup belongs in a guarded curation pass rather than source correction.

## Operational guidance

The document specifies that the pipeline should:

1. Read `okf/wiki/index.md` first when present, then follow its routing.
2. Check prerequisites and stop for missing hard dependencies before proceeding.
3. Vendor the toolchain skills before first CLI use.
4. Ensure `.gitignore`, `.gitattributes`, and `.graphifyignore` are configured correctly.
5. Run `graphify` when available, but continue if it fails.
6. Build `okf/.okf-build/input/` as a deterministic source pack.
7. Initialize `openkb`, ingest staged input, and run `openkb lint`.
8. Validate the generated bundle with `validate_okf_bundle.py`.
9. Re-read `AGENTS.md` and keep its operational guidance current.
10. Reconcile deletions before ingest so removed or moved repository sources do not leave stale pages behind.
11. Treat `okf/.openkb/hashes.json` and `okf/wiki/` as a coupled registry-and-output unit.
12. Use `recompile` for stale or misgrounded pages when source truth has changed or later-ingested concepts should be linked in.
13. Route true knowledge gaps into findings capture instead of hand-editing compiled pages.
14. Reserve guarded editorial curation for output-only cleanup where no source defect or finding promotion fits.

## Relationship to the wiki

This work is part of the repository's broader wiki-generation workflow and is closely tied to [[entities/openkb-wiki]], [[entities/graphify]], and [[entities/okf]]. It also connects to the OpenKB lifecycle policy in [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]. It acts as a process reference rather than a source of domain knowledge.

## Source

See [[summaries/agents__skills__agent-ready-context__references__workflow-md]] for the document summary.

See also: [[summaries/graphify-report]]