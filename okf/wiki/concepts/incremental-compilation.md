---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Selective refresh of staged, ingested, and generated KB content."
---

# Incremental Compilation

Incremental compilation is the practice of refreshing only the parts of an OpenKB knowledge base that are new, changed, removed, or newly affected by updated repository context, instead of regenerating everything wholesale. In the agent-ready model described by the repository README, it is one part of a broader separation between orientation, durable context, and actions across `AGENTS.md`, `okf/wiki/`, and `.agents/skills/`.

## Why it matters

The agent-smith architecture treats knowledge as a [[concepts/knowledge-compilation-pipeline|knowledge compilation pipeline]]: raw repository material is staged, compiled into an interlinked wiki, and then maintained incrementally as the repository changes. That makes incremental compilation a practical requirement, not just an optimization.

In the workflow described by [[summaries/agents__skills__agent-ready-context__references__workflow-md]] and reinforced by [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], incremental compilation keeps the knowledge base efficient, reviewable, and structurally coherent:

- unchanged staged files remain byte-identical, so they do not need to be re-ingested
- OpenKB can skip already-known content through its hash-based registry
- targeted recompilation can refresh pages against the current wiki rather than stale context
- broad recompilation is avoided unless the user explicitly approves it
- generated output stays coupled to staged evidence instead of drifting through hand edits

The README extends that same logic to the repository surfaces themselves. `AGENTS.md` carries orientation, `okf/wiki/` carries durable compiled context, and `.agents/skills/` carries repeatable actions. Keeping those layers separate supports [[concepts/progressive-disclosure|progressive disclosure]] and reduces the need to rebuild more context than the task actually requires.

This is also a repair mechanism. Pages compiled early in a large or resumed ingest can become order-dependent stale pages if later context introduces new concepts or links. Incremental compilation is therefore how the wiki is brought back into alignment after partial compilation, not only how cost is reduced.

## Core workflow

The source workflow defines a strict refresh order:

1. read `okf/wiki/index.md` first when it exists, and let its entries determine subsequent wiki reads
2. when the index routes to tooling context, read `tooling/index.md`, identify the active harness from explicit runtime metadata or self-knowledge, and use runtime inspection when helpful rather than inferring from installed binaries
3. if no reliable harness identity or bundle index exists yet, note that and continue
4. run `check_prereqs.py` first and stop for consent-based bootstrap if hard requirements are missing
5. vendor the `graphify` and `openkb` toolchain skills before first CLI use when those CLIs will run
6. ensure `.gitignore`, `.gitattributes`, and `.graphifyignore` cover the KB and build outputs correctly
7. rerun `graphify` when installed so structural extraction is current
8. rebuild the staged source pack with `build_okf_source_pack.py`
9. initialize and ingest with `openkb`
10. preview page regeneration with `recompile --dry-run` when needed
11. review generated changes, then validate

The README adds the surrounding operational framing: the `agent-ready-context` skill handles consent-first bootstrap, pinned tooling, integrity checks, staged source-pack creation, OpenKB lifecycle steps, and validation of the compiled `okf/wiki/` bundle. That makes incremental compilation part of a larger agent-ready repository workflow rather than an isolated OpenKB behavior.

The order is essential. Recompilation must not happen against an outdated graph or stale staged inputs, because that would cause generated pages to reflect an older structural picture of the repository. The workflow explicitly says to never recompile against a stale graph: structural refresh, source staging, reconciliation, and ingest all precede regeneration.

The lifecycle reference adds a read-first preflight before those steps: inspect KB state with `status` and `list`, then consult `index`, summaries, and existing concept or entity pages before choosing whether any ingest or recompilation is necessary. That keeps incremental work grounded in current KB state rather than assuming regeneration is needed.

The README also clarifies how the repository is expected to be used in practice. The skills are the product surface, while vendored `graphify` and `openkb` copies are treated as toolchain inputs pinned by the transformation pipeline. Incremental compilation works best when those boundaries are preserved and the repository refreshes only the relevant surface.

## Relationship to staged source identity

Incremental compilation depends on stable staged content. The source-pack builder reinforces this by making staged bytes deterministic across runs and by recording provenance per staged item.

Key properties of the pack builder include:

- it inventories tracked files with `git ls-files` and stores a repository snapshot without embedding the current `HEAD`
- it records the last commit that touched each file instead of always stamping the current tip commit
- it normalizes line endings and content encoding before hashing so unchanged files stay byte-identical
- it selects files by path heuristics, favoring docs, workflow files, source directories, manifests, and `.agents/skills/`
- it can split oversized prose or code files into full-content parts rather than cropping them
- it can bundle non-markdown files by directory prefix when `--bundle-depth` is enabled
- it writes a manifest that mirrors source paths, staged paths, content hashes, and origin metadata

These behaviors matter because incremental compilation works best when unchanged sources keep the same staged bytes over time. The pack builder also avoids embedding run-dependent signals that would churn staged output, such as a current `HEAD` stamp or generated report timestamps. That aligns the workflow with [[concepts/hash-registry-coherence]] and [[concepts/deterministic-builds]]: OpenKB can recognize previously ingested content reliably because staged identity does not drift unnecessarily.

The builder also preserves provenance across refreshes. Each staged file carries `source_path`, `source_hash`, `source_kind`, and often `source_commit`, while the manifest records the same information for downstream traceability. That makes incremental updates easier to audit and supports [[concepts/provenance-tracking]] and [[concepts/source-provenance]].

A further protection is built around the graph report. The pack builder strips generated timestamp lines from `graphify-out/GRAPH_REPORT.md`, checks for excessive references back into the KB root, and skips staging the report when it appears to describe the compiled wiki itself. This prevents a self-referential ingestion loop and keeps incremental compilation grounded in repository source evidence rather than feeding compiled output back into the input pipeline. That behavior ties directly to [[concepts/self-reference-control]] and [[concepts/self-referential-ingestion-loops]].

The builder also emits a repository snapshot and a deletion advisory. The snapshot gives the pack a stable inventory of tracked files, while the advisory points out KB documents whose sources no longer appear in the pack. That does not retract anything automatically; it simply signals that reconciliation is needed through a separate orphan-pruning step. This is part of [[concepts/manifest-authoritative-reconciliation]] and [[concepts/orphan-retraction]].

## Orphan retraction as incremental repair

Deletion handling is the missing inverse of the normal add path, and it is now part of the incremental compilation story.

The `prune_okf_orphans.py` script reconciles the OpenKB registry with the repository by retracting pipeline-owned documents whose source files have disappeared or moved. It treats `openkb remove` as the deterministic inverse of `openkb add`, using it only for the KB content that this pipeline owns and never for manually ingested external documents.

Its behavior adds several important incremental-maintenance properties:

- report-only is the default, so deletion reconciliation is visible before it becomes destructive
- `--preview` shows OpenKB's own per-page dry-run plan before any mutation
- `--apply` executes retraction, and `--yes` is required for non-interactive execution
- a mass-orphan safety guard blocks suspicious runs that usually indicate the wrong repo, KB, or `--bundle-depth`
- pseudo-documents such as `repo-snapshot` and `graphify-report` are excluded because they have no backing repo file

The script also distinguishes between deletion and movement. It prefers the staged raw file's `source_path` frontmatter over slug reversal, because slugged names can be lossy when path segments contain `__`. If a missing path's content still exists under a new path, the script marks the orphan as a rename and uses `openkb remove --keep-empty` so shared pages can be repopulated by the new document without losing useful structure.

That makes orphan pruning a core part of incremental compilation rather than a separate cleanup task. It is the repair mechanism for stale registry entries, silent skip behavior, and move-based false deletions, all of which would otherwise leave the wiki out of sync with repository reality. In practice, incremental compilation now spans three states: newly added content, selectively regenerated content, and explicitly retracted orphaned content.

## Selective regeneration

Incremental compilation is not just about selective ingestion; it also constrains regeneration.

The workflow recommends previewing targeted recompilation first and explicitly warns against broad `recompile --all` without consent. This reflects two ideas:

- generated output should change only when source or context changes justify it
- the user should control expensive or wide-ranging semantic regeneration

That behavior connects incremental compilation to [[concepts/consent-first-workflows]] and [[concepts/generated-content-governance]].

The workflow also frames recompilation as downstream of refreshed context. The graph must be current before deciding what to regenerate, because stale structural context can make targeted compilation look complete when it is not. In the same way, refreshed staged input must be ingested before recompilation so that regenerated pages see the latest evidence and the current wiki together.

The lifecycle document adds two refinements. First, `recompile <doc>` is the normal remedy for order-dependent staleness, because it regenerates a document's pages against the current wiki rather than the earlier partial one. Second, selective recompilation is the safe way to restore generated pages after damage when raw content still exists, avoiding unnecessary wide refresh.

## Review requirements

Because compilation is LLM-backed, incremental updates still require review after `add` or `recompile` changes `okf/wiki/`. The workflow calls for checking:

- whether important source ideas were omitted
- whether new pages duplicate existing pages
- whether entities and concepts were classified correctly
- whether caveats and prohibitions from the source survived regeneration
- whether claims remain grounded in cited staged sources
- whether pages are truncated or malformed
- whether early-generated pages are now stale because later concepts were introduced
- whether example or fixture content produced off-topic pages

The README makes the same point in broader terms: generated knowledge is durable only when it is validated, and optional tooling can degrade gracefully when unavailable. Incremental compilation is therefore paired with [[concepts/source-driven-regeneration]], [[concepts/knowledge-linking-and-citations]], and [[concepts/quality-gates]] so that selective updates do not weaken semantic quality.

The workflow is especially strict about how review findings are handled. Problems discovered after generation must go through a correction loop in the committed sources, followed by re-ingest and recompilation; generated pages are not the editing surface. The reviewer is also expected to trace important claims back through the citation chain from wiki page to summary to staged source to repository file and commit. That keeps incremental work aligned with [[concepts/provenance-tracking]], [[concepts/caveat-preservation]], and [[concepts/single-source-of-truth]].

## Boundaries and failure handling

The workflow allows degraded operation when optional tooling fails. For example, if `graphify` fails, the pipeline may continue without it, but the failure must be reported. That preserves progress while making the loss of structural context explicit.

The concept also depends on respecting [[concepts/tool-boundaries]]: structural extraction, deterministic staging, semantic ingestion, and validation each play separate roles and should be refreshed in the right order rather than blended together.

The README's security model reinforces those boundaries. Consent-first installs, explicit provider routing, disclosed data flows, and untrusted-input discipline all limit how far automation may go before the user approves it. Incremental compilation lives inside that safety frame rather than outside it.

The source-pack guidance adds another hard boundary: staged source packs must avoid self-referential ingestion loops, and deletion handling stays advisory until a separate prune step runs. Incremental compilation therefore stays grounded in source evidence and explicit reconciliation rather than silent mutation.

The lifecycle guidance adds a more specific failure model around registry drift. If the hash registry claims a document is already ingested but its generated pages are missing, future `add` runs silently skip it. Incremental compilation therefore depends on preserving registry and wiki coherence together. When that coherence is broken, the fix is document-specific: recompile the affected document if raw content still exists, or remove the stale registry entry and re-add the source if it does not. This makes incremental repair a direct companion to [[concepts/registry-drift]].

The same document also sets a hard boundary against hand-editing generated summaries, concepts, or entities. Generated output must be refreshed through `add` or `recompile`, with limited exceptions for reserved tooling pages and approved conventions files. That rule keeps incremental compilation compatible with [[concepts/generated-content-governance]] and [[concepts/reserved-wiki-files]].

The workflow's separation of orientation, context, and actions also reinforces this boundary: the wiki is the durable knowledge surface, while skills and harness adapters are operational layers. Incremental compilation should refresh the knowledge base, not collapse those layers into one another.

## Practical rule

A concise rule from the source documents is: never recompile against a stale graph or stale staged input. Refresh structure first, stage inputs second, ingest third, and only then regenerate specific pages.

The workflow makes that rule concrete by prescribing the order of graph update, source-pack rebuild, ingestion, dry-run preview, and review. It also distinguishes deterministic preparation from semantic generation: building `okf/.okf-build/input/` does not itself update the KB, so regeneration should wait until fresh staged evidence has actually been added.

A second practical rule from the lifecycle guidance is: repair the input signal, not the generated page. If selective recompilation produces a weak result, improve the committed source, rebuild staging, run `add`, and then recompile the affected document instead of editing the generated wiki directly.

A third rule from the workflow is that incremental compilation should preserve current structure without creating self-referential loops. Structural context should be refreshed from repository sources, while generated wiki content remains outside that graphing pipeline. That keeps selective regeneration grounded in source evidence rather than in prior generated output.

A fourth rule from the README is consent-first operation. Incremental compilation is part of a larger agent-ready bootstrap that should disclose tool choice, routing, and data flow before any LLM-backed step, and should avoid unnecessary installs or broad regeneration unless the user approves them.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[concepts/hash-registry-coherence]]
- [[concepts/generated-content-governance]]
- [[concepts/quality-gates]]
- [[concepts/source-driven-regeneration]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/deterministic-validation]]
- [[concepts/deterministic-builds]]
- [[concepts/tool-boundaries]]
- [[concepts/evidence-staging]]
- [[concepts/registry-drift]]
- [[concepts/single-source-of-truth]]
- [[concepts/reserved-wiki-files]]
- [[concepts/provenance-tracking]]
- [[concepts/source-provenance]]
- [[concepts/caveat-preservation]]
- [[concepts/self-reference-control]]
- [[concepts/consent-first-workflows]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__openkb__references__wiki-schema-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

## Additional lifecycle context

OpenKB is the semantic engine behind the OKF lifecycle in this repository, and the KB root is `okf/` with compiled wiki output under `okf/wiki/`. The lifecycle guidance treats the wiki as untrusted data and recommends a read-first sequence: check `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then inspect `okf/wiki/index.md` and relevant summaries, concepts, or entities before making changes.

The lifecycle also emphasizes consent and disclosure. External file, directory, or URL ingestion should happen only with user approval and clear data-flow disclosure, while `openkb query` is treated as an LLM-backed last resort. OpenKB's health check is also LLM-backed for the knowledge half, so it should be treated as a report rather than a pass/fail gate.

A major operational concern is registry coherence. The hash registry under `okf/.openkb/hashes.json` can cause a document to be silently skipped if it still appears ingested, even when its wiki pages are missing. Incremental compilation therefore depends on keeping raw copies, summaries, generated pages, and delete-state reconciliation in sync. When that coherence breaks, the repair path is document-specific: recompile if raw content still exists, or remove and re-add the source if it does not.

The lifecycle guidance also explains the distinction between deterministic staging and semantic updates. Building the staged pack does not update the KB by itself; only `openkb add` changes the registry and generated pages. That separation is what makes incremental compilation predictable and reviewable.

## Practical implications

Incremental compilation is most effective when the workflow stays disciplined about when to refresh structure, when to rebuild staged inputs, when to retract orphaned content, and when to regenerate pages. It reduces churn, avoids unnecessary LLM work, and makes stale or damaged pages easier to repair without collateral updates.

It also depends on clear ownership of generated output. The KB should be repaired by changing the source of truth, not by editing generated pages. That keeps the wiki aligned with repository evidence and makes selective regeneration trustworthy.

In practice, the concept connects repository maintenance, staged evidence management, orphan retraction, and selective semantic regeneration into a single loop: keep the input stable, refresh only what changed, retract what disappeared, and validate the result before treating it as current.