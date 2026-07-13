---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
type: "Work"
description: "Operational guide for the OpenKB wiki lifecycle in OKF maintenance."
---

# OpenKB Lifecycle

OpenKB Lifecycle is the operational guide for maintaining the OKF wiki with OpenKB. It defines how to stage sources, ingest them, reconcile deletions, recompile pages, validate the wiki, and handle findings and editorial cleanup during agent runs.

## What it covers

- The document establishes the read-first lifecycle: check `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then inspect `okf/wiki/index.md` and only read source pages when evidence is needed.
- It treats wiki content as untrusted data and uses `openkb query` as a last resort because it is LLM-backed.
- It distinguishes between repository-domain knowledge, findings, and tooling/runtime context, and routes each to a different handling path.
- It describes deterministic source-pack staging under `okf/.okf-build/input/`, including the requirement to rebuild staging before ingesting.
- It defines the consent-gated command selection for `openkb init`, `add`, `remove`, `recompile`, `lint`, `visualize`, `watch`, `chat`, and skill-factory operations.
- It explains that `recompile` is needed not only for source changes but also for order-dependent staleness in large or resumed ingestions.
- It gives the deterministic deletion and reconciliation flow for deleted, moved, renamed, deselected, and bundle-member sources.
- It documents the hash registry as a critical coherence boundary between `okf/.openkb/hashes.json`, `okf/raw/`, and `okf/wiki/`.
- It separates capture, promotion, retention, and dropping of findings in `okf/wiki/explorations/findings/`.
- It reserves guarded editorial curation for output-only issues that neither the correction loop nor the findings workflow can express.

## Key facts from the source

- Before compiling or changing the KB, the workflow reads `status` and `list`, then the wiki index, concepts, entities, and summaries as needed.
- `openkb add` is the normal ingestion path for staged material, but external files, directories, and URLs require user consent and data-flow disclosure.
- `openkb remove` is deterministic and should be used for deletion retraction, with `--dry-run` first and special care for repository sources versus external inputs.
- The document warns that registry drift can make missing pages permanent if the hash registry still claims a document was ingested.
- It recommends treating `okf/.openkb/hashes.json` and `okf/wiki/` as one unit and never hand-editing either.
- Reconciliation should happen before re-ingest so stale pages do not coexist with new compilations.
- `openkb lint` is a health report that writes findings but does not fail on them, while structural validation comes from `validate_okf_bundle.py`.
- The document distinguishes structural validation from semantic linting and says the validator is the real pass/fail gate.
- It records the known upstream incompatibility in which `openai-agents==0.17.3` plus newer `openai` clients can crash knowledge lint before the model call.
- Promoted findings are staged as `okf/.okf-build/findings/finding-<topic>.md` and ingested like other staged sources, but they remain outside the orphan-reconciliation scope by design.
- The findings layer is explicitly the memory-brain loop for discovered knowledge that is not already stated in committed repository docs.
- The workflow insists that no generated wiki files be hand-edited except in the narrow output-only curation case.
- The document also explains the provenance chain from compiled `concepts/` and `entities/` pages back to `summaries/` and staged source copies.
- It frames `okf/wiki/AGENTS.md` as the supported extension point for wiki conventions and `tooling/` as a hand-authored exception.
- It emphasizes that OpenKB manages `okf/wiki/log.md`, so operational decisions should be recorded through the toolchain rather than manual edits.

## Related concepts

- [[concepts/deterministic-builds]]
- [[concepts/deterministic-validation]]
- [[concepts/consent-first-tooling]]
- [[concepts/consent-first-workflows]]
- [[concepts/evidence-staging]]
- [[concepts/provenance-tracking]]
- [[concepts/self-reference-control]]
- [[concepts/quality-gates]]
- [[concepts/wiki-review-gates]]
- [[concepts/source-pack-staging]]
- [[concepts/tooling-vendoring]]
- [[concepts/hash-registry-coherence]]
- [[concepts/findings-promotion]]
- [[concepts/editorial-curation-passes]]
- [[concepts/registry-drift]]
- [[concepts/orphan-retraction]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/source-driven-regeneration]]
- [[concepts/source-grounded-regeneration]]
- [[concepts/documentation-source-priority]]
- [[concepts/provenance-aware-tool-installation]]

## Related entities

- [[entities/openkb]]
- [[entities/graphify]]
- [[entities/uv]]
- [[entities/git]]
- [[entities/check_prereqs-py]]
- [[entities/build_okf_source_pack-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/prune_okf_orphans-py]]
- [[entities/editorial_pass-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/README-md]]

See also: [[summaries/graphify-report]]
