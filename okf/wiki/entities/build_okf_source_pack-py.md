---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md"]
type: "Work"
description: "Deterministic source-pack builder for OpenKB staging and reconciliation"
---

# build_okf_source_pack.py

`build_okf_source_pack.py` is the deterministic source-pack builder that turns repository files into staged OpenKB input for ingestion, reconciliation, and graph-aware maintenance.

## What it does

- Selects repository files according to the pack builder's rules.
- Generates staged document names through slugging and bundling logic.
- Produces a manifest that downstream tooling can treat as the authoritative expected set of staged names.
- Supplies the expected name/hash mapping used by `prune_okf_orphans.py` when reconciling deletions and renames.
- Stages repository evidence under `okf/.okf-build/input/` instead of writing directly into `okf/raw/` or `okf/wiki/`.
- Keeps staging inside the KB root so OpenKB records KB-relative paths rather than leaking absolute machine paths into `.openkb/hashes.json`.
- Supports the broader agent-ready workflow that keeps [[concepts/deterministic-source-pack-staging]], [[concepts/source-pack-staging]], [[concepts/manifest-authoritative-reconciliation]], and [[concepts/compiled-knowledge-bases]] aligned.
- Acts as part of the repository agent-ready workflow that treats `okf/wiki/` as durable context and uses staged input as the only ingestion path.
- Shows up as a major hub in the graphify report, connecting build and skill-maintenance areas through `main()` and bridging into the wider OpenKB workflow.

## Why it matters

This script is the reference implementation that `prune_okf_orphans.py` must mirror on its fallback path. If its selection, slug, or bundle logic drifts, orphan detection can misclassify documents or miss deletions entirely. That makes it central to [[concepts/manifest-authoritative-reconciliation]], [[concepts/source-pack-staging]], [[concepts/deterministic-source-pack-staging]], [[concepts/rename-vs-delete-detection]], and [[concepts/orphan-retraction]].

It also sits inside a larger workflow that treats the OpenKB wiki as durable context, favors deterministic input staging, and avoids writing generated content directly into compiled KB areas. The surrounding workflow explicitly routes repository knowledge through [[concepts/deterministic-validation]], [[concepts/knowledge-compilation-pipeline]], and [[concepts/knowledge-lifecycle-governance]].

The privacy and data-flow guidance adds two more constraints to this role: staging must stay inside the KB root, and any path that leaves the machine for an LLM-backed step must be disclosed before use. For OpenKB, that means this builder should feed `okf/.okf-build/input/` rather than any outside staging directory, and any later OpenKB or graphify step that uses the staged pack must follow [[concepts/data-flow-disclosure]] and [[concepts/explicit-provider-routing]].

The graph report reinforces that role by placing this script inside a dense build community and identifying an inferred relationship from `main()` toward `bundle_key()`, which links `build_okf_source_pack.py` to `prune_okf_orphans.py`. That makes the file not just a staging utility, but a cross-community bridge in the repository's [[concepts/knowledge-graph-analysis]] and [[concepts/cross-community-bridges]].

## Key facts from the document

- The agent-ready workflow uses this builder before OpenKB ingestion so source packs stay reproducible.
- Never write generated files directly into `okf/raw/` or `okf/wiki/`; stage deterministic input under `okf/.okf-build/input/` and ingest it with OpenKB.
- The documented workflow treats `okf/` as the OpenKB KB root, with `okf/wiki/` as compiled durable context.
- Staging outside the KB root can cause absolute machine paths to be written into `.openkb/hashes.json`, so the pack builder should keep all staged input inside `okf/`.
- The source pack builder is paired with `prune_okf_orphans.py`, which relies on its manifest or re-derives the expected staged names if the manifest is absent.
- The broader skill treats `okf/.openkb/hashes.json` as a sensitive dedupe registry, so deterministic staging matters for safe incremental refreshes.
- Pseudo-documents like `repo-snapshot` and `graphify-report` are regenerated and are not real repo-backed sources.
- The workflow emphasizes re-ingesting corrected source documents rather than hand-editing compiled wiki pages when generated output is weak or wrong.
- The builder is part of a broader agent-ready context surface that also includes AGENTS.md orientation, OpenKB-compiled wiki context, and validation.
- In graph terms, `main()` is one of the highest-centrality nodes in the corpus, and this script participates in that structural hub.

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[concepts/source-pack-manifest]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/orphan-retraction]]
- [[entities/openkb]]
- [[entities/prune_okf_orphans-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/graphify-report]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/README-md]]