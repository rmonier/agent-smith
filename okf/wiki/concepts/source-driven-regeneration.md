---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Use source updates and re-ingestion to fix generated knowledge deterministically."
---

# Source-Driven Regeneration

Source-driven regeneration is the practice of correcting or improving generated knowledge by updating the underlying source materials and then rerunning the ingestion or compilation workflow, rather than manually editing generated outputs. In OpenKB-style maintenance, that usually means improving committed repository sources, staged evidence, or deterministic source packs, then rebuilding the KB so the generated pages converge on the new inputs.

## Why it matters

Generated wiki pages are derivative artifacts. Their reliability depends on the quality, clarity, and provenance of the source documents that feed the pipeline. Direct edits to generated pages can break traceability, introduce drift from the evidence base, and create changes that will be overwritten on the next rebuild.

The lifecycle guidance makes this operational: generated wiki pages, raw ingested content, and the OpenKB hash registry must stay coherent. If the registry says a document has already been ingested, later `add` operations can silently skip it. That means a bad manual edit, partial restore, merge mistake, or damaged wiki can persist unless repair happens through the supported regeneration path. This makes source-driven regeneration a practical safeguard for [[concepts/hash-registry-coherence]] and a direct response to [[concepts/registry-drift]].

The managed `AGENTS.md` guidance reinforces the same boundary. It keeps repository orientation in `AGENTS.md`, durable context in the compiled wiki, and reusable procedures in skills, then tells agents to fix weak generated pages by improving committed source documents or staged evidence and re-ingesting rather than editing `okf/wiki/` directly. That makes source-driven regeneration part of [[concepts/agent-context-layering]], [[concepts/context-action-separation]], and [[concepts/documentation-source-priority]] rather than just a local repair preference.

The updated skill guidance sharpens that split. It defines the durable context source of truth as `okf/wiki/`, says the OpenKB KB root owns `okf/raw/`, `okf/wiki/`, `okf/.openkb/`, and `okf/output/`, and forbids creating a parallel repository wiki. It also says generated files should be staged under `okf/.okf-build/input/` and ingested with OpenKB rather than written directly into KB-owned directories. Those rules make regeneration a bounded maintenance path, not an informal edit style.

The same skill also makes regeneration consent-first and dependency-aware. It requires `uv`, expects pinned tooling, and treats Graphify and OpenKB as optional but governed tools whose read-only vendor skills should be copied into `.agents/skills/` before first use. That aligns source-driven regeneration with [[concepts/consent-first-tooling]], [[concepts/tooling-consent-and-pin-management]], [[concepts/preflight-checks]], and [[concepts/tooling-vendoring]].

The newer lifecycle guidance adds a stronger operational frame. It recommends starting with `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then reading `okf/wiki/index.md` and relevant wiki pages before compiling, querying, or changing the KB. It also treats `openkb query` as a last resort because it costs an LLM call, insists that wiki content be treated as untrusted data, and warns that `okf/.openkb/hashes.json` and `okf/wiki/` must be handled as one unit. That turns source-driven regeneration into a discipline of preflight inspection, scoped repair, and registry-aware maintenance.

The same lifecycle guidance also clarifies that the supported repair path differs depending on the problem. If raw content still exists, `recompile` can regenerate missing or damaged wiki pages. If raw content is gone, `remove` plus a fresh `add` can clear stale registry state and ingest the source again. This means source-driven regeneration is not just for weak prose; it is also the recovery strategy for registry-backed damage.

The source-pack builder extends the same principle into staging itself. It turns a Git repository into deterministic OpenKB input by inventorying tracked files, selecting likely knowledge-bearing paths, writing a repository snapshot, optionally staging a safe graph report, and emitting a manifest that records source paths, hashes, staged destinations, and provenance. Because OpenKB dedupes by staged bytes, the script deliberately avoids embedding the current HEAD commit in the snapshot and uses last-touch commit metadata only where it will not churn unchanged content. That makes regeneration dependent on stable staged inputs, not on incidental repository state.

The source-pack builder also encodes the same repair logic in its structure. It uses path heuristics to stage docs, workflows, manifests, source directories, and `.agents/skills/` content; it can bundle files by directory prefix; and it splits oversized markdown or code files into full-content parts instead of cropping them. It warns when bundle groups grow too large, advises deeper splitting when possible, and preserves provenance in a manifest so the staged pack can be reconstructed deterministically. In practice, that means source-driven regeneration begins before wiki compilation: weak or incomplete outputs should be fixed by improving the staged pack or upstream repository sources, then rebuilding the pack and re-ingesting.

The source-pack builder also includes a self-reference guard. If the graph report appears to reference KB-root paths, it refuses to stage the report to avoid a feedback loop where wiki content changes the graph, the graph changes the report, and the report is ingested back into the wiki. That guard makes source-driven regeneration part of [[concepts/self-reference-control]] and [[concepts/knowledge-graph-feedback-loops]] as well as content maintenance.

The conservative skeleton builder adds a related constraint at the earliest stage of compilation. Its output is explicitly a non-authoritative baseline, built from repository metadata, a Graphify report excerpt, and any staged external documents. Because those pages are intentionally incomplete and tool-generated, improving them durably still means changing the staged evidence or committed repository sources and then rebuilding the skeleton or downstream wiki.

The workflow guidance strengthens this further by making regeneration the normal maintenance path for the whole pipeline. Graph updates, source-pack rebuilding, ingestion, recompilation, review, and validation all happen in a fixed order so generated pages always reflect the current repository state. That order matters because recompiling against stale staged inputs or an outdated graph can preserve weak pages even when the repository has already been corrected. In that sense, source-driven regeneration is not just about where edits belong; it is also about when they must flow through the pipeline.

The same managed guidance also treats the wiki as data rather than instructions, requires deterministic staged inputs, requires review of generated pages before acceptance, and directs agents to validate the final wiki bundle. Together those rules make source-driven regeneration part of a broader operating discipline rather than an isolated editing preference.

The managed `AGENTS.md` updater script adds the same idea at the file level. It creates or refreshes a bounded OKF-managed section between HTML comments, replacing only the managed block and preserving project-specific setup, style, test, and PR instructions outside it. The injected section tells agents to read `AGENTS.md` first, then `okf/wiki/index.md`, then graph artifacts, then skills; it frames wiki pages as durable context rather than instructions; it tells agents to use the skill for OKF generation and `AGENTS.md` maintenance; and it directs them to fix weak generated wiki output by improving source documents or staged evidence and re-ingesting rather than editing compiled wiki pages directly. That makes source-driven regeneration part of [[concepts/managed-document-sections]], [[concepts/agents-md-maintenance]], and [[concepts/wiki-context-routing]].

This makes source-driven regeneration a core discipline within documentation architecture, a practical safeguard for [[concepts/provenance-tracking]], and a direct support for [[concepts/llm-free-knowledge-bootstrap]] by treating fallback-generated structure as a starting point to regenerate from sources, not a destination for manual patching.

## Core principle

If a generated page is weak, ambiguous, misplaced, incomplete, or missing expected links back to evidence, the preferred fix is:

1. Improve the committed source document, staged evidence, or source pack.
2. Rebuild the staged inputs when needed.
3. Re-ingest or recompile the knowledge base.
4. Review and validate the regenerated output.

The goal is to keep the source layer authoritative and the generated layer reproducible.

In OpenKB maintenance, this means treating `okf/raw/`, generated wiki pages, the registry-managed ingestion state, and fallback skeleton outputs as tool-owned outputs rather than editing surfaces. The same principle applies when external documentation has been materialized into evidence Markdown: the durable fix belongs in the evidence selection, normalization, staging, or source-pack construction workflow, not in hand-edits to generated synthesis pages.

The source-pack builder makes that boundary concrete. It produces deterministic staged documents from repository content, records a manifest for traceability, and deliberately separates inventory, bundling, splitting, and provenance capture from later wiki compilation. That separation keeps regeneration reproducible and limits the blast radius of source changes to the staged inputs that actually changed.

The updated lifecycle guidance also clarifies command discipline around this principle. Agents should inspect KB state first, use deterministic staged inputs, refresh repository structure before recompiling, prefer document-scoped recompilation over broad rebuilds, and use dry runs before destructive or large-scope actions. Regeneration is not just a content strategy; it is the supported maintenance path.

The updated skill guidance sharpens this principle further by making staged input mandatory for normal generation work and by warning that generated wiki defects should route back through committed sources rather than direct wiki edits. It also makes `okf/.openkb/hashes.json` a first-class part of the maintenance model: if content is marked as already ingested while wiki pages are missing, future `add` runs may skip that content silently. That turns source-driven regeneration into both a content-quality rule and a recovery strategy for registry-backed builds.

The managed `AGENTS.md` guidance adds the same principle in repository-facing language: review generated pages for duplicates, vague names, classification mistakes, lost caveats, and weak grounding, then fix those issues by improving committed source documents or staged evidence and re-ingesting rather than editing `okf/wiki/` directly. It also places final validation after regeneration as a required closing step, which ties the concept to [[concepts/deterministic-validation]] and [[concepts/okf-validation]].

## Guidance from the source document

[[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]] states that agents should review generated wiki changes for issues such as:

- duplicate pages
- vague names
- entity versus concept misclassification
- lost caveats
- weak grounding through the citation chain

It then gives a strong rule: weak pages should be fixed by improving committed source documents and re-ingesting, not by editing `okf/wiki/` pages directly.

That same template broadens the workflow around the rule. It says agents should read the knowledge base state before querying or compiling, build staged input deterministically, ask before expensive or destructive operations, and validate the final wiki before finishing. It also warns that `okf/.openkb/hashes.json` and `okf/wiki/` are one unit, so repairs after merges or reverts should go through supported linting and regeneration steps rather than manual patching.

[[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]] sharpens that guidance into an explicit lifecycle policy. It says generated pages under `okf/wiki/` and tool-managed raw content are owned by OpenKB, and that durable corrections should begin in committed repository documentation, typically under `docs/` or another natural source location. The recommended correction loop is to improve the source, ensure it is git-tracked, rebuild staged input, run `openkb add`, dry-run recompilation for affected documents, and then validate the results.

That lifecycle document also adds several important operational details:

- read `status`, `list`, and existing wiki pages before compiling or querying
- treat `openkb query` as a last resort because it consumes an LLM call
- keep staging deterministic and preferably inside `okf/` to avoid absolute-path leakage in registry metadata
- treat `lint` as a health report and the repository validator as the pass/fail gate
- repair registered-but-missing documents through `recompile` when raw content remains, or `remove` plus re-`add` when it does not
- avoid hand-editing `okf/wiki/log.md`, which OpenKB manages

These details make regeneration not only the durable content fix, but also the safe operational route for preserving provenance and structural integrity.

[[summaries/agents__skills__agent-ready-context__references__workflow-md]] extends the same logic from lifecycle policy into an end-to-end build workflow. It requires prerequisite checks, consent-aware tool bootstrap, vendoring of toolchain skills before CLI use, deterministic source-pack creation, and validation after generation. It also makes explicit that Graphify refresh must happen before source-pack rebuilding and that recompile steps must follow graph refresh and ingestion so pages are never regenerated against stale repository structure.

That workflow adds a stronger review model for generated changes. After every `openkb add` or `recompile` that changes `okf/wiki/`, the generated pages should be inspected like a pull request for missing or vague concepts, near-duplicates, entity or concept misclassification, off-topic pages created from examples, lost caveats, truncation, stale early pages caused by order-dependent compilation, and weak grounding through the citation chain. Every finding still routes back through the same correction loop: fix the source, re-ingest, recompile, and validate. The workflow explicitly forbids hand-deleting wiki pages or silently dropping offending staged files as a shortcut.

The workflow also adds a structural reason to prefer source-driven regeneration: the wiki must stay out of the repository graph. Excluding the KB root from Graphify prevents self-reference loops in which wiki pages change the graph report, the changed report is re-ingested, and the wiki changes again. By keeping generated knowledge out of graph extraction and forcing fixes back into committed sources or staged evidence, regeneration preserves deterministic outputs, non-circular grounding, and useful discovery.

[[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]] extends the same logic to zero-LLM bootstrap workflows. That script generates a conservative wiki skeleton from staged inputs, copies external documentation into references, writes a repository overview from git metadata and a Graphify report excerpt, and warns that the result must be validated and enriched. Its design makes clear that even baseline concept pages are derivative build artifacts whose quality depends on the staged source pack and evidence selection, not on after-the-fact editing.

[[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]] adds a repository-policy enforcement layer to the same idea. The script creates or updates a managed section in `AGENTS.md` without rewriting project-specific guidance outside that section. Inside the managed block, it instructs agents to read `AGENTS.md` first, then the compiled wiki, then structural graph outputs, and finally reusable skills. It explicitly states that wiki pages should be treated as durable context and as data rather than instructions, and that weak generated pages should be corrected by improving source documents and re-ingesting rather than editing `okf/wiki/` directly. It also bakes the regeneration sequence into repository guidance: confirm prerequisites, refresh graph data first, materialize external docs as evidence, build deterministic staged input, inspect KB state, ingest, preview broad or destructive changes, review generated pages, and validate the final wiki. By managing this guidance as a replaceable bounded section, the script helps keep regeneration rules current without overwriting local repository instructions.

[[summaries/agents__skills__agent-ready-context__SKILL-md]] consolidates these same rules into the top-level operating policy for making a repository agent-ready. It says the durable context source of truth is `okf/wiki/`, forbids creating a parallel repository wiki, warns not to put long-form repository knowledge into `AGENTS.md`, and says generated files should be staged under `okf/.okf-build/input/` and ingested rather than written directly into OpenKB-owned directories. It also calls out `okf/.openkb/hashes.json` as the dedupe registry whose drift can make missing wiki pages silently persist, and directs agents to fix weak outputs through source improvement and re-ingestion instead of patching compiled pages. This turns source-driven regeneration from a local correction pattern into the central maintenance rule for the entire context pipeline.

The same lifecycle and workflow guidance also explains why output editing is unsafe: it can desynchronize generated pages from the registry and citation chain, and future recompilation can overwrite the edits anyway. The skeleton builder reinforces this by labeling its output as a generated floor for later enrichment and by separating raw evidence from synthesized pages. The source-pack builder extends that discipline to the staging layer by making file selection, bundling, splitting, and provenance explicit and deterministic. Together with the `AGENTS.md` template, the maintenance script, and the skill's emphasis on deterministic staging, review before acceptance, and final validation, these sources establish source-driven regeneration as the normal repair path for generated knowledge.

## What this protects

Source-driven regeneration helps preserve:

- reproducibility of generated outputs
- alignment between evidence and summaries
- stable provenance chains
- consistency across repeated builds
- coherence between generated pages, raw content, and registry state
- confidence during review
- the distinction between evidence files and synthesized pages
- the policy boundary between repository orientation, reusable actions, and durable context
- safe recovery paths after merges, reverts, or partial KB damage
- privacy and portability benefits when staged inputs and registry entries are managed predictably
- fixed build ordering between graph refresh, staged input rebuilding, ingestion, recompilation, and validation
- protection against self-referential graph feedback from generated wiki content
- repository-level maintenance rules that can be refreshed in `AGENTS.md` without normalizing away project-specific guidance
- the separation between OpenKB-owned directories and the deterministic staging area that feeds them
- stable source-pack manifests that make re-ingestion traceable and repeatable
- safe handling of oversized files through splitting rather than truncation
- predictable staging hashes that avoid needless re-ingestion churn
- a controlled path from generated skeletons to durable knowledge by improving source inputs instead of patching the baseline
- coordinated handling of the hash registry and wiki pages as a single maintenance unit

It also reduces the risk that a manual edit in a generated file will disappear during the next compile or leave the knowledge base in a partially damaged state.

## Relationship to other concepts

This concept depends on [[concepts/agent-context-layering]]: source evidence, guidance files, and generated wiki pages have different roles, and agents should not confuse them.

It is tightly connected to [[concepts/evidence-staging]] because regeneration should flow through the staged source bundle rather than ad hoc edits to generated artifacts.

It reinforces [[concepts/generated-content-governance]] by treating generated wiki content as tool-owned output with narrow exceptions.

It also supports [[concepts/quality-gates]] because review and validation become more meaningful when outputs are expected to be reproducible from inputs.

The `AGENTS.md` template and maintenance script also tie it to [[concepts/documentation-source-priority]] and [[concepts/context-action-separation]]: repository rules point agents to the right context sources in order, but durable corrections still belong in source documents and evidence inputs rather than in downstream generated pages.

The workflow guidance strengthens its relationship to [[concepts/deterministic-builds]], [[concepts/incremental-compilation]], and [[concepts/self-reference-control]]. Regeneration works best when unchanged staged inputs remain byte-stable, recompilation follows fresh structural analysis, and generated wiki content is kept out of the graph so the pipeline has a stable fixed point.

The updated skill also connects this concept more directly to [[concepts/kb-root-staging]], [[concepts/durable-context]], and [[concepts/single-source-of-truth]] by making `okf/.okf-build/input/` the deterministic handoff point, `okf/wiki/` the durable context layer, and regeneration the mechanism that keeps compiled context aligned with authoritative inputs.

Finally, it works with [[concepts/tool-boundaries]] and [[concepts/tooling-consent-and-pin-management]]: agents should respect which files are managed by OpenKB, use supported commands such as `add`, `remove`, `recompile`, and `lint`, and run the workflow in a controlled environment. The skeleton builder's warning that tooling context is harness-specific and should not be treated as project truth also complements [[concepts/tooling-context-isolation]]. The lifecycle split between a structural validator and a non-gating health report also closely matches [[concepts/validation-vs-health-reporting]].

The managed `AGENTS.md` workflow further connects this concept to [[concepts/repo-navigation]], [[concepts/index-based-discovery]], and [[concepts/safe-automation]] by enforcing a stable order for where agents look first and by embedding approval and review checkpoints directly into repository guidance.

## Practical signals for using it

Source-driven regeneration is the right approach when a generated page has:

- an unclear title or description
- missing caveats or nuance
- poor factual grounding
- incorrect classification
- duplicated content
- stale or incomplete evidence
- missing or weakened citation links back to summaries or sources
- signs of registry or generated-output drift after merges or restores
- fallback skeleton content that reflects only partial metadata or a truncated report excerpt
- external evidence that was copied into references but not properly incorporated through recompilation
- generated output that conflicts with the current source-priority rules in `AGENTS.md`
- validation or lint results that indicate the wiki and registry need coordinated repair
- pages that were compiled too early and missed later-discovered concepts or links, making document-scoped recompilation necessary to refresh them against the current wiki state
- large-repository staging changes where bundle granularity or hash changes cause broad re-ingestion and require careful regeneration planning
- graph reports or staged inputs that were rebuilt out of order, leaving generated pages based on stale structure
- off-topic pages created from examples or fixtures that should instead be corrected at the source or evidence-selection layer
- repository guidance that has drifted from current OpenKB maintenance practice and needs a managed `AGENTS.md` refresh so future regeneration follows the supported sequence
- situations where OpenKB-owned directories were patched directly instead of being rebuilt from staged input
- source packs whose repository snapshot, bundle layout, or manifest no longer matches the current tracked files
- oversized code or prose sources that need split-not-crop handling to preserve content without exceeding staging limits
- a missing or damaged wiki page whose registry entry may still suppress reinsertion until the source is restaged or the document is removed and re-added

In these cases, the fix should begin in the source materials or evidence collection workflow, then flow forward through regeneration. If the issue is damage rather than weak content, the repair still follows tool-supported paths such as recompiling from raw content or removing and re-adding the affected document instead of patching generated files by hand.

## In this wiki

This concept is directly grounded in [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]], which presents source improvement and re-ingestion as the preferred method for maintaining OpenKB-derived wiki quality. It also contributes the surrounding operational frame: deterministic input building, preflight inspection of KB state, review of generated changes, and final validation.

[[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]] adds the lifecycle policy behind that rule: read the KB first, stage evidence deterministically, treat generated outputs and registry data as a coherent tool-managed unit, prefer dry-run and document-scoped maintenance actions, and use recompile or re-ingest to recover from weak or damaged pages.

[[summaries/agents__skills__agent-ready-context__references__workflow-md]] adds the repository build sequence that makes regeneration reliable in practice: check prerequisites, vendor required skills before CLI use, refresh Graphify before rebuilding staged inputs, ingest before recompiling, review every generated change, validate structurally, and keep the wiki out of the repository graph so the pipeline remains deterministic and non-circular.

[[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]] adds the bootstrap case: when the system generates only a conservative skeleton from git state, Graphify output, and staged external docs, improvements still belong in the sources and evidence inputs so the next regeneration produces a better baseline.

[[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]] adds the repository-policy case: when an `AGENTS.md` file is created or refreshed, the managed section explicitly encodes context and action boundaries, source priority, deterministic OKF maintenance steps, review expectations, and the rule that weak wiki pages must be repaired through committed sources and regeneration rather than direct edits.

[[summaries/agents__skills__agent-ready-context__SKILL-md]] adds the top-level policy statement for the full pipeline: `okf/wiki/` is the durable context source of truth, OpenKB owns the KB directories, deterministic input belongs under `okf/.okf-build/input/`, generated wiki defects should route back through source improvements and re-ingestion, and the hash registry must stay coherent with generated outputs.

The source-pack builder adds the staging-layer implementation of the same idea: it inventories the repository, selects only relevant source material, normalizes line endings, computes stable hashes, and preserves provenance in a manifest so regeneration starts from a reproducible, auditable input set.

See also: [[summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]]

See also: [[summaries/agents__skills__openkb__references__wiki-schema-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]