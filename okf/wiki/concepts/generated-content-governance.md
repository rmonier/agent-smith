---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Governance rules for regenerating, validating, and repairing compiled KB outputs."
---

# Generated Content Governance

Generated content governance is the discipline of treating compiled knowledge-base outputs as machine-owned artifacts that must be regenerated from trusted inputs rather than edited directly. In this repository, it governs how OpenKB-generated material under `okf/` is created, reviewed, repaired, validated, and kept aligned with staged sources, citation chains, the dedupe registry, deterministic build workflows, repository graph boundaries, and fallback paths where a conservative wiki skeleton is produced without semantic compilation.

This concept is grounded in [[summaries/agents__skills__agent-ready-context__SKILL-md]], [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], [[summaries/agents__skills__agent-ready-context__references__workflow-md]], [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]], [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]], [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]], [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]], [[summaries/agents__skills__openkb__references__wiki-schema-md]], and [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]], and it is closely related to [[entities/openkb]], [[entities/graphify]], [[entities/agents-md]], [[entities/uv]], [[entities/pageindex]], [[concepts/source-driven-regeneration]], [[concepts/hash-registry-coherence]], [[concepts/knowledge-linking-and-citations]], [[concepts/provenance-tracking]], [[concepts/quality-gates]], [[concepts/evidence-staging]], [[concepts/tool-boundaries]], [[concepts/data-flow-disclosure]], [[concepts/privacy-preserving-tooling]], [[concepts/repository-overview-generation]], [[concepts/tooling-context-isolation]], [[concepts/llm-free-knowledge-bootstrap]], [[concepts/context-action-separation]], [[concepts/durable-context]], [[concepts/agent-context-layering]], [[concepts/self-reference-control]], [[concepts/knowledge-boundaries]], [[concepts/frontmatter-metadata]], [[concepts/index-based-discovery]], [[concepts/page-indexed-sources]], [[concepts/wikilink-integrity]], [[concepts/agent-ready-repositories]], [[concepts/agent-ready-context-skill]], [[concepts/llm-wiki]], [[concepts/progressive-disclosure]], [[concepts/consent-first-workflows]], [[concepts/consent-first-tooling]], [[concepts/explicit-provider-routing]], [[concepts/air-gapped-operation]], [[concepts/compiled-knowledge-bases]], [[concepts/documentation-architecture]], [[concepts/documentation-cohesion]], [[concepts/openkb-wiki-health-checks]], [[concepts/okf-validation]], [[concepts/okf-bundle-validation]], [[concepts/source-provenance]], [[concepts/single-source-of-truth]], [[concepts/wikilink-resolution]], and [[concepts/wikilink-integrity]].

## Core idea

The main rule is simple: generated wiki content is not the source of truth. The source of truth is the committed repository material that gets staged, ingested, and compiled. When generated pages are weak, incomplete, duplicated, misclassified, or damaged, the durable fix is to improve the source inputs and rerun the generation workflow.

The workflow sharpens that rule by making deterministic staging mandatory. Generated files should not be written directly into `okf/raw/` or `okf/wiki/`; repository and external evidence should first be assembled under `okf/.okf-build/input/` and then ingested through [[entities/openkb]]. That keeps the compilation surface explicit, reviewable, and repeatable, reinforcing [[concepts/evidence-staging]], [[concepts/repository-ingestion]], [[concepts/kb-root-staging]], and [[concepts/deterministic-builds]]. Staging alone does not update `okf/raw/` or `okf/wiki/`; only the controlled add or recompile path does.

The lifecycle reference adds a stricter operational boundary. Before compiling, querying, or changing the KB, the read-first sequence is to run `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then inspect `okf/wiki/index.md` and the relevant summary, concept, or entity pages. `openkb query` is a last resort because it costs an LLM call, and wiki content must be treated as untrusted data rather than instruction. That reinforces [[concepts/context-action-separation]], [[concepts/durable-context]], [[concepts/agent-context-layering]], and [[concepts/knowledge-boundaries]].

The same reference also clarifies command choice by goal: `openkb add` is for staged input, `openkb remove` is the inverse for retraction, `openkb recompile` repairs stale or damaged outputs, and `openkb lint` reports health and structural findings. This makes governance not just about where outputs live, but about which mutation path is allowed for which kind of change.

The deletion counterpart matters too. `prune_okf_orphans.py` reconciles the OpenKB registry against the repository and retracts orphaned documents when source files disappear or move. It uses a freshly built manifest when available, falls back to git-derived expectations when needed, and distinguishes `deleted`, `renamed`, and `deselected` cases so only pipeline-owned content is removed. That script is a concrete governance tool because it repairs registry drift without inventing new knowledge, uses `openkb remove` as the only sanctioned inverse mutation, and includes safety guards against mass-orphan scenarios caused by stale manifests or bundle-depth mismatches. This extends generated content governance into [[concepts/orphan-retraction]], [[concepts/manifest-authoritative-reconciliation]], [[concepts/rename-vs-delete-detection]], [[concepts/registry-drift]], and [[concepts/hash-registry-coherence]].

The bootstrap skill adds a stronger operational split around this boundary. `AGENTS.md` is a routing and rules file, `okf/wiki/` is the durable knowledge source of truth, `graphify-out/` is a structural exploration aid rather than final authority, and `.agents/skills/` contains reusable actions. That split is not just repository hygiene; it is part of generated content governance because it keeps the instructions layer, the structural layer, and the compiled knowledge layer from collapsing into one another. The same skill also insists that `AGENTS.md` stay short and that durable context move into `okf/wiki/`, which reinforces [[concepts/context-action-separation]], [[concepts/durable-context]], [[concepts/agent-context-layering]], and [[concepts/agents-md-maintenance]].

The `merge_agents_md_okf_section.py` script makes that split concrete for `AGENTS.md`. It manages only the section between `<!-- okf:start -->` and `<!-- okf:end -->`, leaving the rest of the file intact, and it appends or replaces that managed block conservatively. Its guidance explicitly positions `AGENTS.md` as orientation and best practices, `okf/wiki/index.md` as the first routed context, `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as structural aids, and `.agents/skills/` as reusable actions. It also tells agents to use `uv run` for bundled maintenance scripts, to treat `okf/wiki/AGENTS.md` as the wiki conventions manual, and to convert durable discoveries into findings instead of editing compiled pages directly.

The subagent-profile-adapter skill extends that layering into runtime-specific execution. It treats harness adapters as projections of the active environment, not as a portable standard, and requires explicit runtime detection before writing any adapter files. It also keeps the boundary strict between compiled OKF knowledge, repository orientation in `AGENTS.md`, reusable actions in `.agents/skills/`, and harness-specific projections written only for the current runtime. That adds a clearer operational frame for [[concepts/runtime-adapter-management]], [[concepts/adaptive-harness-detection]], [[concepts/harness-native-profiles]], and [[concepts/subagent-role-design]].

The wiki schema adds an important structural version of the same rule: the compiled `wiki/` tree has fixed page roles and machine-managed support files, so governance applies not just to prose pages but to the shape of the knowledge artifact itself. `index.md` is the machine-maintained catalog, `log.md` is the chronological operation record, `summaries/` bridge individual sources into synthesis, `concepts/` hold cross-document ideas, `entities/` hold named things, `sources/` hold converted source text, and `explorations/` hold saved query outputs. Treating those locations as governed surfaces prevents users from silently turning machine-owned navigation, provenance, or routing files into hand-maintained documentation.

This remains true even when the system falls back to a conservative skeleton generator. A minimal bundle created without an LLM may be useful for navigation and evidence preservation, but it is still a derived artifact that must be validated and enriched from trusted inputs rather than hand-corrected into seeming authority.

The same source-first rule also extends to the repository's orientation layer: `AGENTS.md` can point agents toward generated context, but it must not be mistaken for the durable knowledge base itself. The managed `AGENTS.md` section explicitly frames the file as routing and operational guidance, while `okf/wiki/` remains the compiled context layer and `okf/` remains the owned KB root. That separation reinforces [[concepts/context-action-separation]], [[concepts/durable-context]], [[concepts/agent-context-layering]], and [[concepts/agents-md-maintenance]].

Generated content governance also includes keeping the compiled wiki out of structural graph inputs. The `.graphifyignore` template excludes `okf/` so the knowledge base is treated as a map of the repository rather than part of the repository being mapped. Without that boundary, generated pages could be pulled back into graph analysis and then re-ingested, creating a recursive feedback loop that distorts repository structure and never cleanly converges. The workflow states the reasons explicitly: no fixed point for deterministic builds, circular grounding in citation chains, and discovery pollution where generated summaries overwhelm source material. This makes graph exclusion part of the same governance model, not a separate housekeeping rule, and ties the concept directly to [[concepts/self-reference-control]], [[concepts/knowledge-graph-analysis]], and [[concepts/knowledge-boundaries]].

The read path is governed too. Before compiling, querying, or repairing the KB, the lifecycle requires a read-first sequence: inspect status and document listings, read `index.md`, then consult relevant concept, entity, and summary pages before reaching for raw sources or LLM-backed query. The wiki schema reinforces this by defining `index.md` as the stable top-level catalog and by making section persistence and document-type labels part of the artifact contract. Generated content governance is therefore not only about how outputs are written, but also about how derived knowledge is consumed: as useful data, never as unquestioned instruction.

The editorial pass script turns these rules into a guarded curation loop. Its `--brief` mode loads the vendor's own wikilink whitelist middleware into the agent context, using the installed OpenKB package's private compiler template when available and falling back to a mirrored copy only if that private surface drifts. Its `--check` mode then validates a completed curation diff deterministically with a zero-LLM combination of vendor lint checks and git-based policy checks. The vendor side looks for broken links, stale index entries, orphans, invalid frontmatter, and missing OKF fields; the local side restricts curation to `wiki/concepts/`, `wiki/entities/`, and `wiki/index.md`, preserves source provenance unions, blocks unapproved new compiled pages, and requires changed concept/entity pages to keep a non-empty `sources:` list. That makes curation a constrained maintenance path rather than a freeform editing channel and reinforces [[concepts/deterministic-validation]], [[concepts/executable-validation]], [[concepts/okf-validation]], [[concepts/provenance-union-governance]], and [[concepts/editorial-curation-passes]].

This avoids several classes of failure:

- Local fixes that disappear on the next regeneration.
- Silent divergence between generated pages and the hash/provenance records that track how they were created.
- Regeneration against stale structural context, where the wiki reflects an old repository graph instead of the current codebase.
- Governance drift, where review and validation are skipped because generated output is treated like ordinary hand-authored Markdown.
- False confidence in fallback-generated summaries or overview pages that explicitly disclaim semantic completeness.
- Confusion between orientation instructions in `AGENTS.md`, durable compiled context in `okf/wiki/`, executable procedures in skills, and structural graph outputs that should never recursively absorb generated wiki content.
- Citation-chain loss, where a concept or entity page loses the machine-managed source links that ground it back to staged evidence.
- Order-dependent staleness, where pages compiled early never learn about concepts discovered later unless their document is explicitly recompiled.
- Misuse of long-document source files, where page-indexed JSON is treated like hand-readable Markdown instead of a machine-sliced source surface.
- Registry drift, where the hash registry says a source is already present even though the corresponding compiled pages are missing or stale.
- Misrouted provider assumptions, where a workflow silently depends on a compiler or harness that has not been identified through explicit runtime context.
- Curation-side regression, where a merge or split accidentally widens scope, invents provenance, or leaves dangling wikilinks behind.
- Invalid manual edits to managed concept or entity pages that break the required non-empty `sources:` contract or the whitelist of valid wikilink targets.
- Orphan retention, where deleted or renamed repo sources keep stale KB pages alive because the registry was not reconciled against the current repository state.
- Over-aggressive cleanup, where a stale bundle or wrong `--bundle-depth` would otherwise make a whole registry look orphaned and trigger unintended retraction.

## What is governed

In the OpenKB lifecycle, generated content governance applies to:

- OpenKB-managed ingested content and machine-owned storage under `okf/`.
- Generated pages under `okf/wiki/`, especially `summaries/`, `concepts/`, `entities/`, and machine-maintained support files.
- Machine-managed citation and provenance metadata such as source references and staged-source links.
- Build artifacts and staging areas that feed generation, including `okf/.okf-build/input/` and generated structural context such as Graphify output.
- Ignore and boundary controls that keep generated knowledge artifacts out of repository graph analysis, including the exclusion of `okf/` from Graphify inputs.
- Fallback-generated bundles that create minimal concepts, copied references, `index.md`, and `log.md` outputs when no provider-backed semantic compiler is available.
- Managed orientation content inserted into `AGENTS.md` that governs how agents should discover, interpret, and refresh compiled repository knowledge.
- OpenKB-owned state under `okf/.openkb/` and generated downstream output under `okf/output/`, which are part of the same governed system even when not all files are committed.
- Converted source artifacts under `wiki/sources/`, including short-document Markdown and long-document page-index JSON plus extracted images.
- Machine-managed metadata contracts such as page descriptions, type fields, document classification, and structured section roles in the compiled wiki.
- Dedupe registry state and normalized staging records that decide whether a source is treated as new, changed, or already ingested.
- Validation and review artifacts that report whether the generated knowledge base remains coherent, grounded, and structurally safe.
- Curated editorial diffs that modify concepts/entities pages and the root index while preserving target whitelists, provenance unions, and source lists.
- Harness-specific adapters produced from current runtime context, because they are generated projections that must stay separate from compiled project knowledge.
- Orphan retraction workflows that compare the registry to current repository state and remove pipeline-owned KB pages whose sources were deleted, moved, or intentionally deselected.
- Source-pack manifests and git-derived fallback expectations, because they decide what the current repository would stage and therefore what counts as stale.
- Safety-guard thresholds for bulk cleanup, because governance includes preventing an incorrect invocation from turning reconciliation into mass deletion.

The source documents make a strong boundary between generated material and hand-authored material. Generated outputs belong to the tool, while a small set of explicitly documented locations may be edited by humans with care. The managed `AGENTS.md` workflow text adds a further governance boundary: `AGENTS.md` is an index and rule surface, the wiki is durable context, Graphify is structural guidance, and skills are reusable actions. Treating those layers distinctly is part of generated content governance, not a separate concern.

The lifecycle reference adds two more governed surfaces that are easy to overlook: the dedupe registry in `okf/.openkb/hashes.json` and the machine-managed citation chain that connects concept and entity pages to summary pages to staged source copies to repository paths, hashes, and commits. Governance therefore covers not just visible Markdown pages, but the bookkeeping structures that make regeneration, repair, and traceability possible.

The wiki schema clarifies that generated governance also includes respecting the difference between short sources and PageIndex sources. Short documents are meant to be read through converted Markdown; long documents are represented as paginated JSON arrays that should be sliced by page rather than opened wholesale. That means governance applies to how source artifacts are inspected, not just how summary pages are written.

The source pack workflow extends governance to repository discovery itself: the KB root must be excluded from the repository graph, and the source pack builder refuses to stage a graph report that references it. That makes self-reference control part of the governed surface rather than a downstream stylistic preference.

## No-hand-edit rule

A central policy is the no-hand-edit rule:

- Do not manually write or patch generated wiki pages.
- Do not hand-edit OpenKB-owned raw or machine-managed storage.
- Do not repair semantic defects by editing derived pages in place.
- Regenerate through the official workflow instead.

The reason is not only that changes may be overwritten. Manual edits can also break internal coherence across generated pages, citation metadata, staged evidence, and the hash registry that deduplicates and tracks ingested material. This is why generated content governance is tightly coupled to [[concepts/hash-registry-coherence]].

The bootstrap skill makes the write boundary explicit: never write generated files directly into `okf/raw/` or `okf/wiki/`; stage deterministic input under `okf/.okf-build/input/` and ingest it with OpenKB instead. Only narrow exceptions are allowed: tooling pages under `okf/wiki/tooling/`, user-approved edits to `okf/wiki/AGENTS.md` conventions, and the clearly reported zero-LLM skeleton fallback.

The rule also applies to conservative fallback outputs. A generated repository overview, copied external evidence listing, or machine-built index may look simple enough to patch safely, but direct edits still bypass the source-first model and can desynchronize the generated bundle from its staged inputs and commit context.

The same governance mindset explains why the managed `AGENTS.md` section is bounded by explicit markers and maintained by script rather than by ad hoc manual edits. Operational routing text can be updated, but it should be updated through controlled regeneration of the managed section so that repository-specific instructions outside the block remain intact and the workflow policy stays standardized. This connects generated content governance with [[concepts/agents-md-maintenance]].

The workflow adds a stronger review rule around generated pages: even when pages are clearly weak, duplicated, off-topic, truncated, or misclassified, the repair path is still to improve committed source material and re-ingest it, not to patch `okf/wiki/` directly. The documented review pass explicitly routes findings through a correction loop rather than direct edits.

The no-hand-edit rule also has a graph boundary implication: if generated wiki pages are not meant to be hand-maintained source, they also should not be treated as structural input to tools that map the repository. Excluding `okf/` from graph analysis preserves the same source-versus-derivation boundary in tooling that the no-edit rule preserves in authoring.

The lifecycle reference sharpens this further by stating that `okf/raw/`, generated wiki pages, and `log.md` are machine-managed. Even a seemingly harmless repair to a missing source list or broken summary backlink is governance-breaking, because those fields are part of a machine-maintained provenance system and must be regenerated, not patched.

The wiki schema adds a page-type-specific version of this rule. Summary pages, concept pages, entity pages, `index.md`, and converted source representations each carry distinct machine-assigned responsibilities and metadata expectations. Hand-editing any one of them risks corrupting not just the local prose but the routing assumptions that make the wiki readable through [[concepts/index-based-discovery]], [[concepts/frontmatter-metadata]], and [[concepts/wikilink-integrity]].

## Approved path for change

The documents describe a source-first correction loop:

1. Add or improve a committed repository document that expresses the missing concept, clarification, constraint, or boundary.
2. Ensure the file is tracked in git so it enters deterministic staging.
3. Refresh structural context first when available, such as rerunning [[entities/graphify]].
4. Rebuild staged inputs and ingest them through the OpenKB workflow.
5. Preview retraction or recompilation when needed, regenerate affected documents, then validate the resulting wiki.
6. Review generated changes like a pull request and route any findings back into source fixes rather than patching generated pages.

The bootstrap skill makes that path more operational and consent-aware. Check prerequisites first, vendor the needed skills before first CLI use, ensure ignore and normalization files are installed or merged, require a Git repository, and use `uv run` for bundled scripts. If Graphify is available, run it before source-pack creation; if it fails, continue in degraded mode but report the failure. If external URLs are used, materialize them as evidence files or add them only with user approval. This sequencing ties governance to [[concepts/tooling-context-isolation]], [[concepts/external-documentation]], [[concepts/tooling-consent-and-pin-management]], [[concepts/git-attributes]], [[concepts/skill-vendoring]], [[concepts/cross-platform-tooling]], and [[concepts/preflight-checks]].

The graph boundary policy now belongs in that same loop. Structural context should be refreshed from repository sources while keeping `okf/` excluded, so the graph reflects the territory rather than prior generated interpretations of it. Re-running graph analysis without that exclusion would undermine the source-first workflow by feeding derivative outputs back into repository structure discovery.

In degraded environments, the same principle still holds: if only a conservative skeleton can be built, the right response is to improve staged repository material, external evidence, or structural context and rerun generation, not to manually promote fallback pages into durable documentation.

The lifecycle reference also contributes two important refinements. First, recompilation is not only for ordinary regeneration but also for repairing order-dependent staleness: if a document was compiled before related concepts existed in the wiki, recompile regenerates it against the current knowledge surface. Second, all high-impact maintenance actions should be previewed first where supported, especially removal and recompilation, because governance includes making destructive or expensive changes legible before they become state.

The wiki schema contributes another operational refinement: the approved read path for sources depends on document class. Short documents should be read through the converted Markdown in `wiki/sources/<doc>.md`, while long documents should be inspected through page-sliced JSON access rather than whole-file reads. That usage pattern is part of governance because it preserves practical access to large compiled sources and prevents ad hoc handling that bypasses the intended PageIndex model.

The editorial-pass script adds a curation-specific refinement here. `--check` is intended to run on a diff range that contains only the curation, with any unrelated KB work committed or stashed first. It then verifies the completed edit against the installed OpenKB vendor checks and local git policy, and its exit codes separate cleanly into pass, violation, and environment failure. That means the approved path for change includes isolating the curation diff itself before validation, not just producing a corrected page.

The orphan retraction script adds another approved maintenance path: use the built manifest when present, fall back to git-derived expected names only when necessary, and treat retraction as a scoped inverse of ingestion rather than as generic cleanup. It explicitly refuses to auto-apply when the orphan set is too large or when the registry intersects the expected set too weakly, because those symptoms usually mean the invocation is wrong rather than the KB truly being full of orphans.

This is the practical expression of [[concepts/source-driven-regeneration]], [[concepts/evidence-staging]], and [[concepts/incremental-compilation]]. The important governance principle is that semantic corrections belong in the source material, not in the generated interpretation layer.

## Why source-first fixes matter

Source-first regeneration preserves several important properties:

- Repeatability: the same source set can regenerate the same knowledge bundle.
- Auditability: readers can trace claims back through staged copies to repository files and commit metadata.
- Durability: future recompiles retain the improvement because it lives in the source.
- Tool compatibility: lint, recompile, and validation operate on expected machine-managed structures.
- Structural freshness: recompilation happens against current repository structure rather than stale context.
- Honest confidence levels: fallback outputs can clearly remain provisional instead of being silently upgraded by manual edits.
- Layer clarity: operational instructions, compiled knowledge, structural maps, and executable skills remain distinct.
- Self-reference control: generated outputs do not recursively become inputs to graph analysis or later ingest cycles.
- Navigational stability: catalog, page-role, and wikilink conventions remain consistent across rebuilds.
- Registry coherence: hash state, staged sources, and compiled pages continue to describe the same source set.
- Safe cleanup: orphaned pages can be retracted deterministically when their source files disappear or move.
- Rename awareness: moved content can preserve downstream pages when the new path still represents the same source.

These properties connect generated content governance to [[concepts/provenance-tracking]], [[concepts/deterministic-validation]], [[concepts/knowledge-linking-and-citations]], [[concepts/incremental-compilation]], [[concepts/llm-free-knowledge-bootstrap]], [[concepts/context-action-separation]], [[concepts/self-reference-control]], and [[concepts/index-based-discovery]].

The workflow adds a stronger determinism guarantee around this logic: staged files carry the last commit that touched each file rather than repository `HEAD`, and unchanged files therefore produce byte-identical staged outputs across commits. That means source-first fixes are not only philosophically cleaner; they are what lets the hash registry, staged evidence, and generated pages stay aligned under [[concepts/deterministic-builds]].

The current skill description adds another source-first reason: generated pages are reviewed for duplicates, vague concepts, lost caveats, and entity-versus-concept mistakes after `add` or `recompile`, but the fix route still runs back through source improvement. Human review is mandatory, but human patching of machine-owned outputs is not.

The lifecycle reference adds another reason source-first fixes matter: the citation chain is deterministic and machine-kept from concept or entity page to summary page to staged source copy to repository path, hash, and commit. Fixing the input preserves that entire chain; patching the output bypasses it and can leave the wiki looking plausible while no longer being properly grounded.

The wiki schema reinforces this by defining summary pages as bridges to full-text source artifacts and concept pages as explicitly cross-document synthesis surfaces. If those outputs are patched in place, they stop being reliable products of the documented pipeline and become untracked editorial hybrids.

## Registry and wiki must stay in sync

The source documents highlight a critical failure mode: if the OpenKB hash registry records a document as already ingested but the corresponding generated wiki pages are lost or damaged, future adds may skip the document without repairing the missing outputs. This creates a persistent gap.

Generated content governance therefore includes a synchronization rule:

- Treat the registry state, staged source pack, and generated wiki state as one system.
- Do not restore, merge, revert, or edit one side independently.
- Rebuild staged inputs before regeneration so the hash view and structural context match the code being compiled.
- After operations that touch `okf/`, run validation and inspect health signals.
- Keep generated indexes, logs, copied references, and overview pages aligned with the exact staged inputs and commit snapshot used to produce them.
- Reconcile orphaned registry entries against the repository state before relying on the registry to suppress future ingest work.

The managed `AGENTS.md` workflow now states this coupling explicitly: `okf/.openkb/hashes.json` and `okf/wiki/` are one unit, and merges or reverts touching `okf/` should be followed by lint review. That turns registry coherence from an implementation detail into repository policy and reinforces [[concepts/hash-registry-coherence]], [[concepts/wikilink-integrity]], [[concepts/quality-gates]], and [[concepts/registry-drift]].

The workflow also clarifies that hash-registry drift can silently suppress future ingest work if the registry believes content is already present. Governance therefore includes careful handling of dedupe state during merges, repairs, and cleanup, not just of visible Markdown outputs.

That coupling also matters for graph-derived structure. If Graphify or similar structural outputs are regenerated from a repository graph polluted by `okf/`, the staged context feeding OpenKB can drift even when hash state appears coherent. Registry coherence therefore depends not only on content hashes, but on maintaining clean structural inputs that respect the generated-versus-source boundary.

The lifecycle repair guidance makes the remedy concrete. If the raw document still exists, recompiling that document is the proper way to regenerate missing wiki pages. If raw content is gone too, the stale registry entry must be removed before the source is re-added. Governance therefore includes knowing that dedupe is not self-healing: once registry drift exists, ordinary add operations may preserve the damage rather than fix it.

The new orphan-retraction script makes that remedy operational. It uses the raw staged `source_path` when available, falls back to reverse-slug decoding only as a last resort, and checks for rename-by-content-hash before labeling a document deleted. That matters because a `git mv` should not be treated as loss of knowledge if the same content reappears elsewhere; instead, the old page can be removed with `--keep-empty` while the new page repopulates shared outputs. This turns rename-vs-delete detection into a first-class governance concern rather than an accidental side effect.

The wiki schema adds one more synchronization surface: `index.md` and `log.md` are part of the compiled contract, not optional conveniences. Missing or stale catalog entries, incorrect document type labels, or malformed operation logs are signs that the machine-owned wiki state is no longer coherent with the registry and source set.

## Exceptions and boundaries

The source material allows narrow exceptions to the no-hand-edit rule:

- Hand-authored operational or tooling pages in explicitly designated locations.
- User-approved edits to `okf/wiki/AGENTS.md` conventions after the documented merge step.
- Temporary degraded workflows where a conservative skeleton bundle is produced because no provider is available, with later reconciliation through normal regeneration.

These exceptions do not weaken the general rule. Instead, they clarify [[concepts/tool-boundaries]]: some pages are operational context or harness configuration, while others are generated knowledge artifacts. Governance depends on keeping those categories separate.

The managed `AGENTS.md` section adds a useful boundary model for the whole repository: `AGENTS.md` is orientation and best practices, `okf/wiki/` is compiled context, `graphify-out/` is navigational structure, and `.agents/skills/` contains action workflows. That division prevents compiled knowledge from being mistaken for instructions and prevents instructions from being mistaken for source evidence. It also helps preserve [[concepts/tooling-context-isolation]] and [[concepts/documentation-architecture]].

The fallback skeleton script makes this boundary explicit by keeping project-facing concept pages separate from harness-specific tooling context and by labeling tooling material as outsider context that must not be treated as project truth.

The workflow also clarifies that external documentation fetched from the web remains untrusted evidence, not executable instruction. Governance therefore covers not only where generated content is written, but also how source trust levels are preserved during enrichment and summarization. This connects to [[concepts/source-trust-levels]], [[concepts/external-documentation]], [[concepts/web-evidence-ingestion]], [[concepts/prompt-injection-defense]], and [[concepts/data-flow-disclosure]].

The `.graphifyignore` template adds a sharper version of the same boundary logic: the wiki is not part of the territory being graphed. Structural tooling must therefore treat `okf/` as outside the graphable repository corpus, preserving a clean separation between generated representation and primary source. That makes graph exclusion a concrete instance of [[concepts/knowledge-boundaries]].

The lifecycle reference adds a practical boundary around command choice as well. URL ingestion, broad recompilation, auto-fixing lint, saved query output, visualization, watch loops, and chat-style sessions all require extra intent or approval because governance includes limiting how generated surfaces grow and how external or LLM-backed inputs enter the system.

The wiki schema contributes a final boundary distinction: entity pages are for named things, concept pages are for recurring ideas, and source pages are not synthesis surfaces at all. Respecting those roles is part of governance because category drift weakens navigation, provenance, and downstream query behavior.

## Relationship to human documentation

Generated content governance also affects how repository docs coexist with human-facing documentation systems. Curated knowledge pages may live in committed docs, but generated site output and intermediate build material must stay ignored or otherwise outside the primary source corpus. Committed generated docs are discouraged because they can be re-ingested as if they were primary evidence, creating churn, duplication, and derivation loops.

The fallback skeleton pattern adds an important nuance: even when a script copies external Markdown into a references area or creates a repository overview from staged metadata, those outputs remain machine-arranged evidence surfaces rather than primary human-authored documentation. Their value is navigational and provisional, not authoritative.

The managed OpenKB insertion for `AGENTS.md` adds another coexistence rule: the orientation document should remain concise and act as a routing map rather than becoming a shadow knowledge base. Durable repository understanding belongs in committed source docs and their compiled wiki outputs, not in an ever-growing operational handbook. This makes the concept relevant to [[concepts/documentation-architecture]] and [[concepts/documentation-cohesion]] as a repository-wide discipline, not only an OpenKB-specific rule.

The current skill description adds a stronger anti-duplication policy here: do not create a parallel repository wiki, and do not move long-form repository knowledge into `AGENTS.md`. Governance includes preserving that single compiled context surface so that readers and tools know where durable knowledge actually lives. This strengthens [[concepts/single-source-of-truth]] and [[concepts/durable-context]].

The graph exclusion rule reinforces this coexistence model. If generated wiki pages are committed or left visible to repository graph tooling, they can be mistaken for human-authored primary documentation and recursively influence future structure reports. Ignoring `okf/` helps preserve the distinction between authoritative repository docs and machine-compiled context.

The lifecycle reference contributes a further coexistence rule for `docs/`: curated repository knowledge may live there naturally, but human site build outputs must remain gitignored, and generated documentation should not be committed into human documentation trees because committed generated docs become ingestion candidates. The governance goal is not to isolate the KB from documentation, but to keep authored documentation and generated derivatives from collapsing into each other.

The wiki schema sharpens this by making the compiled wiki's role explicit: `sources/` preserve converted evidence, `summaries/` condense documents, `concepts/` synthesize ideas, and `entities/` answer named-thing questions. Human-authored docs can feed these layers, but they should not be casually rewritten to impersonate them, nor should compiled layers be treated as the hand-maintained documentation system of record.

## Validation role

Governance is enforced partly through workflow and partly through checks:

- The deterministic validator acts as the pass/fail gate for structural correctness.
- `openkb lint` provides a health report over structure and knowledge quality, but it is not a blocking gate.
- Post-generation review checks generated pages for missing ideas, near-duplicates, weakened caveats, misclassified entity-versus-concept pages, off-topic distillations from example files, truncation, stale early pages, and grounding back to staged sources.
- Missing source metadata, broken links, and related issues are treated as signals that generated content has become unreliable.
- Fallback-generated pages should be reviewed with extra care because they may intentionally provide only a conservative excerpt, copied evidence list, or minimal index rather than a semantically complete interpretation.
- Validation must cover not only the wiki bundle but also the workflow assumptions around staging, registry coherence, consent boundaries, orientation-layer accuracy, and graph-boundary accuracy.

The workflow strengthens this by requiring status inspection before generation, dry-run previews for destructive operations, explicit review of generated pages for duplicates and weak grounding, and a final validator pass over `okf/wiki/`. These checks make governance an end-to-end process spanning source preparation, generation, review, and maintenance. This is why generated content governance is inseparable from [[concepts/quality-gates]], [[concepts/deterministic-validation]], [[concepts/executable-validation]], and [[concepts/okf-validation]] as an operating discipline.

The workflow also explicitly distinguishes health checking from auto-repair: `openkb lint` is approved, but broad fix-up actions like `lint --fix` or broad `recompile` require extra consent and review. Governance therefore includes restraint about which maintenance commands may run automatically.

The graph boundary input adds another validation concern: structural reports should be checked to ensure generated wiki paths are excluded, because a clean-looking graph can still be governance-breaking if it includes machine-owned knowledge artifacts as repository nodes.

The lifecycle reference makes the split sharper still. `openkb lint` mixes deterministic structural checks with an LLM-backed knowledge lint and always completes with a report, while the repository validator is the actual pass/fail gate suitable for CI. Governance therefore depends on understanding the difference between a health report and an executable quality gate, not treating all validation commands as equivalent. This matches [[concepts/validation-vs-health-reporting]] and [[concepts/okf-validation]].

The editorial-pass script is especially important here because it codifies curation review as a guarded, deterministic validation loop. It uses the installed OpenKB runtime to check compiled page health, link integrity, frontmatter validity, and missing OKF fields, while its local policy layer enforces scope, provenance preservation, and new-page approval. On success it reports that the curation diff obeys scope, provenance, and vendor structural checks; on failure it enumerates violations. That makes editorial curation part of the validation surface, not just an informal editing aid.

The wiki schema adds concrete validation expectations around page shape and navigation: `index.md` should preserve its four sections even when empty, document entries should use `(short)` or `(pageindex)` rather than file extensions, source pages should resolve through wikilinks, and long-document source access should respect paginated JSON structure. These details matter because governance is partly about preserving the contract readers and tools rely on.

The orphan-retraction script adds one more validation dimension. Its manifest-vs-git advisory warns when a freshly built manifest disagrees with the current repository's staged names, because that mismatch can mean stale pack inputs or drift in the mirrored selection logic. That warning is itself a governance signal: if the expected staged names disagree, do not trust the current cleanup or compile plan until the source pack is rebuilt or the invocation is corrected.

## Practical implications

When working with generated KB content:

- Read generated pages as useful but derived artifacts.
- Verify important claims through the provenance chain when needed.
- Improve source documents when the generated output is weak.
- Refresh structural context before recompiling so generation is not based on stale repository understanding.
- Keep `okf/` out of repository graph analysis so compiled context does not feed back into structural discovery.
- Use regeneration, review, and validation instead of manual patching.
- Be especially careful during merges, restores, and cleanup inside `okf/`.
- Treat external material as evidence only, and keep disclosure and privacy constraints in force during LLM-backed steps.
- Treat conservative skeleton outputs as a floor for continuity, not as a substitute for later semantic compilation and review.
- Keep `AGENTS.md` concise and use it as an index into rules, compiled context, structure, and skills rather than as a duplicate knowledge store.
- Use managed scripts and pinned tooling paths, especially `uv`-driven maintenance commands, so governance remains repeatable across environments.
- Respect the consent-first boundaries around installing tooling, ingesting large sources, querying with LLM-backed commands, running broad recompiles, and changing provider-backed compilation behavior.
- Vendor tool-shipped skills before first use of their CLIs when the workflow requires it, because tool adoption and tool guidance are governed together.
- Keep generated artifacts and local state out of version control according to the documented ignore policy so that governed outputs do not pollute source history or graph reports.
- Treat missing or empty machine-managed source links on concept or entity pages as repair signals, not as invitations to fill them in by hand.
- Remember that dedupe is stateful: if registry entries survive while pages do not, ordinary add operations may silently preserve the gap.
- Prefer staging inside `okf/` so registry metadata stays portable and does not leak absolute host paths.
- Use query and exploration features sparingly and treat saved outputs as an explicit publishing choice rather than a default side effect.
- Use `index.md` as the normal entry point into the wiki, then follow summaries, concepts, and entities according to their defined roles.
- Read short converted sources as Markdown, but inspect PageIndex sources by slicing page JSON rather than loading whole files.
- Treat broken or missing wikilinks as governance signals, because compiled navigation is supposed to resolve after normal linting.
- Avoid collapsing page roles: named things belong in entities, recurring ideas belong in concepts, and converted source text belongs in sources.
- Keep graph and wiki boundaries aligned so the repo graph never consumes the compiled wiki as if it were source material.
- When doing curation edits, isolate the diff, run the guarded brief/check loop, and do not widen scope beyond approved concepts, entities, or the root index.
- Treat harness-specific adapters as generated projections that should stay short, local to the active runtime, and separate from project knowledge.
- Run orphan cleanup only after confirming the pack state, bundle depth, and target KB root, because the wrong invocation can make a healthy registry look orphaned.
- Use preview mode for deletions when available so page-level removal plans are visible before any irreversible cleanup.

## See also

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]]
- [[summaries/agents__skills__openkb__references__wiki-schema-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[entities/openkb]]
- [[entities/graphify]]
- [[entities/agents-md]]
- [[entities/uv]]
- [[entities/pageindex]]
- [[concepts/source-driven-regeneration]]
- [[concepts/hash-registry-coherence]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/provenance-tracking]]
- [[concepts/evidence-staging]]
- [[concepts/quality-gates]]
- [[concepts/tool-boundaries]]
- [[concepts/tooling-context-isolation]]
- [[concepts/repository-overview-generation]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/wikilink-integrity]]
- [[concepts/data-flow-disclosure]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/context-action-separation]]
- [[concepts/durable-context]]
- [[concepts/agent-context-layering]]
- [[concepts/agents-md-maintenance]]
- [[concepts/deterministic-builds]]
- [[concepts/repository-ingestion]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/external-documentation]]
- [[concepts/source-trust-levels]]
- [[concepts/self-reference-control]]
- [[concepts/knowledge-boundaries]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/kb-root-staging]]
- [[concepts/registry-drift]]
- [[concepts/executable-validation]]
- [[concepts/okf-validation]]
- [[concepts/preflight-checks]]
- [[concepts/cross-platform-tooling]]
- [[concepts/skill-vendoring]]
- [[concepts/single-source-of-truth]]
- [[concepts/documentation-architecture]]
- [[concepts/documentation-cohesion]]
- [[concepts/web-evidence-ingestion]]
- [[concepts/prompt-injection-defense]]
- [[concepts/frontmatter-metadata]]
- [[concepts/index-based-discovery]]
- [[concepts/page-indexed-sources]]
- [[concepts/editorial-curation-passes]]
- [[concepts/provenance-union-governance]]
- [[concepts/deterministic-validation]]
- [[concepts/okf-bundle-validation]]
- [[concepts/wikilink-resolution]]
- [[concepts/runtime-adapter-management]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/harness-native-profiles]]
- [[concepts/subagent-role-design]]
- [[concepts/orphan-retraction]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/rename-vs-delete-detection]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]]

See also: [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/README-md]]

## README Contributions

The README reinforces this concept by describing `agent-smith` as a repository transformation system whose product is three portable skills: `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter`. The README makes the separation between orientation, context, actions, and runtime adapters explicit, which strengthens the governance model around where knowledge belongs and how it should be maintained.

It also clarifies that `AGENTS.md` is a routing surface, `okf/wiki/` is compiled durable knowledge, and `.agents/skills/` is the action layer, while vendored toolchain copies of `graphify` and `openkb` are not part of the distributable product. That distinction supports [[concepts/skill-vendoring]], [[concepts/tooling-context-governance]], [[concepts/runtime-adapter-management]], and [[concepts/generated-artifact-adoption]].

The README further emphasizes consent-first bootstrapping, explicit provider routing, air-gapped operation, and no silent installs. Those details strengthen the governance model by showing that generated content is only one part of a broader agent-control system that also governs tool acquisition, data flow, and local-vs-remote execution choices.

The README also defines a clear boundary against recursive self-reference: generated wiki pages should not become graph inputs, and the compiled knowledge base should not be treated as the thing being structurally mapped. This aligns with the existing policy that `okf/` is excluded from Graphify inputs and should remain a derived, not recursive, surface.
