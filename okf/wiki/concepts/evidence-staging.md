---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md"]
description: "Structured evidence collected before ingestion and wiki compilation."
---

# Evidence Staging

Evidence staging is the practice of collecting source-derived facts into structured intermediate files before adding them to the knowledge base. It creates a controlled handoff between source retrieval and wiki compilation so facts can be reviewed, attributed, filtered for relevance, regenerated from the same source path later, and inspected before any provider-backed processing occurs.

## What this concept means

In this workflow, staged evidence is neither the final wiki page nor the original source. It is a deliberate intermediate artifact that captures the facts needed for a repository task or OpenKB topic. This supports [[concepts/source-driven-regeneration]] by keeping the path from source material to generated knowledge explicit and repeatable.

For external sources, the staged artifact is typically one Markdown file per fetched URL. Each file records the source, why it matters, and the relevant facts in paraphrased form. For repository material, staging also serves as the safe input boundary before compilation into [[entities/openkb]]: the staged pack is what gets added, while generated wiki pages and raw OpenKB internals are tool-owned outputs rather than hand-edited working files.

The workflow guidance expands this meaning in two important ways. First, staging is the point where the repository snapshot becomes deterministic enough for repeatable ingestion: the source pack is built from tracked files, and unchanged inputs should produce unchanged staged bytes across later commits, not just across repeated runs of the same checkout. Second, staging is explicitly upstream of any LLM-backed compilation, so it is the main place to inspect evidence quality before semantic generation begins.

The source-pack builder makes this concrete by showing exactly what gets staged and why. It produces a repository snapshot, selected per-file Markdown wrappers, an optional normalized Graphify report, and a manifest that records source path, staged path, source hash, source kind, and origin. In that design, staging is not just a directory of copied files; it is a normalized, provenance-carrying evidence layer built specifically to remain stable when unrelated repository commits happen. That ties evidence staging directly to [[concepts/repository-ingestion]], [[concepts/document-normalization]], and [[concepts/deterministic-builds]].

The script also sharpens the meaning of staging as a content-addressed handoff. It computes `source_hash` from normalized UTF-8 text, classifies staged material heuristically as markdown, text, code, or other, and writes all staged files with normalized line endings. These choices show that staging is not merely a transport step; it is the layer where repository material is converted into a repeatable evidence format suitable for downstream indexing and deduplicated ingest. This connects staging to [[concepts/heuristic-classification]], [[concepts/frontmatter-metadata]], and [[concepts/line-ending-normalization]].

The lifecycle guidance adds an equally important operational meaning: only staged inputs should be fed into normal OpenKB maintenance, and staging alone does not update `okf/raw/` or `okf/wiki/`. The expected maintenance path is to inspect KB status first, rebuild the staged input deterministically, ingest only that staged path, and use recompile when generated pages need refreshing. This makes staging the canonical handoff layer between repository evidence and generated knowledge, and it keeps maintenance aligned with [[concepts/incremental-compilation]], [[concepts/hash-registry-coherence]], and [[concepts/generated-content-governance]].

The repository skill strengthens this further by defining `okf/wiki/` as the durable context surface and by forbidding routine direct writes into `okf/raw/` or `okf/wiki/`. Instead, deterministic input belongs under `okf/.okf-build/input/`, and that staged path is the normal route into the KB. The same policy also makes staging the place where weak generated pages are repaired indirectly: fix committed inputs, rebuild the staged pack, and re-ingest rather than patching derived wiki pages. That makes evidence staging a core part of [[concepts/durable-context]], [[concepts/context-action-separation]], and [[concepts/single-source-of-truth]].

The repository skeleton builder adds a useful lower-bound interpretation of the same idea. In environments without provider credentials, the staged source pack can still be compiled into a conservative wiki skeleton: repository metadata, a Graphify report excerpt, and copied external evidence become the seed material for an initial knowledge bundle. This reinforces staging as the canonical handoff layer whether downstream compilation is semantic, minimal, or entirely offline, connecting it directly to [[concepts/llm-free-knowledge-bootstrap]] and [[concepts/offline-first-workflows]].

The privacy and data-flow guidance adds another defining property: staging is the last reviewable boundary before content may leave the machine. Local prerequisite checks, source-pack construction, validators, and code-only structural extraction remain local, but non-code graph extraction and OpenKB compilation may route staged material to a configured provider. That makes staging not just a format boundary but a consent and routing boundary linked to [[concepts/data-flow-disclosure]], [[concepts/explicit-provider-routing]], and [[concepts/privacy-preserving-tooling]].

The workflow document sharpens this further by placing staging inside a larger build discipline. Before ingestion, the repo must have prerequisite tools, vendored tool skills when their CLIs will be used, ignore rules for tool-owned outputs, line-ending normalization, and a graph ignore rule that keeps the KB root out of structural analysis. In that sequence, staging is not an isolated prep step; it is the midpoint where source material has been normalized enough to trust as compilation input, but has not yet become generated knowledge.

## Why staging matters

Evidence staging improves quality and safety in several ways:

- It limits imported material to facts relevant to the repo and the requested topic.
- It preserves source attribution and retrieval context through metadata.
- It separates untrusted fetched content from downstream wiki generation.
- It makes review possible before evidence becomes part of the KB.
- It supports regeneration by ensuring fixes happen in source inputs rather than generated outputs.
- It helps keep the staged input, generated wiki, and registry state aligned during normal maintenance.
- It creates the disclosure point where operators can state what content will be sent if provider-backed compilation is about to begin.

These benefits connect evidence staging to [[concepts/provenance-tracking]], [[concepts/quality-gates]], [[concepts/deterministic-validation]], and [[concepts/hash-registry-coherence]]. The workflow document also makes staging the boundary that keeps repository structure current before recompilation: Graphify refresh, source-pack rebuild, and `openkb add` must happen before any recompile so generated pages are based on the latest staged evidence rather than stale repository context.

The source-pack script sharpens this point by making staging itself a reproducible build product. It removes stale staged outputs before rebuilding, inventories all tracked files for the repository snapshot, selects only important repository files for deeper staging, and writes a sorted manifest so downstream tools see a stable input set. Staging therefore matters not only as a review checkpoint, but also as the place where the repository is converted into a controlled evidence package suitable for repeated ingestion without unnecessary churn.

It also matters because the staged layer is where self-reference can still be prevented before ingestion. The source-pack builder inspects an optional Graphify report and refuses to stage it if it appears to describe generated KB paths under `okf/`, because that would feed generated wiki structure back into future compilation. In this sense, evidence staging is a practical enforcement point for [[concepts/self-reference-control]] and broader [[concepts/knowledge-boundaries]].

The lifecycle policy adds a stronger maintenance reason: OpenKB deduplicates by hash, so evidence staging is what lets repeated `add` operations remain predictable instead of accidental. If the staged bytes are stable, unchanged material is skipped cleanly; if the staging mode or contents change, OpenKB sees new hashes and re-ingests. This is why the guidance recommends choosing a per-file or bundled staging strategy early and keeping it stable for large repositories, tying staging directly to [[concepts/repository-ingestion]] and [[concepts/deterministic-builds]].

The skeleton-generation fallback adds a second perspective: even non-semantic outputs still depend on staged evidence quality. If the staged Graphify report or external documents are incomplete, the resulting overview and evidence pages will also be incomplete. Staging therefore matters not only for high-quality concept synthesis, but also for producing trustworthy conservative outputs when the system can only bootstrap a minimal wiki.

The privacy guidance adds a stronger operational reason as well: staging is where local-only and air-gapped options stay viable. By keeping source preparation separate from provider-backed compilation, the same staged pack can feed a local Ollama-backed run, a zero-LLM bootstrap path, or a remote provider path chosen with user consent. That makes staging central to [[concepts/offline-first-workflows]] and to tooling that preserves user control over egress.

The workflow guidance adds one more reason: staging is where generated output can still be corrected through a proper source loop. After `openkb add` or recompile changes `okf/wiki/`, the review process checks for missing concepts, near-duplicates, entity-versus-concept mistakes, off-topic pages created from examples, lost caveats, truncation, stale early pages, and broken grounding. But every fix still routes back through source correction, staged rebuild, and re-ingestion rather than direct edits to generated pages. That makes staging the practical repair boundary for semantic drift as well as the intake boundary for new evidence.

The repository skill adds a governance reason that broadens all of these. It treats the staged input as the normal maintenance boundary for `okf/` itself, warns against silent registry drift around `okf/.openkb/hashes.json`, and frames staging as the place where KB updates remain observable before tool-owned outputs change. In that sense, staging is not only an evidence-prep step; it is the operational checkpoint that keeps repository context, generated knowledge, and deduplication state coherent.

## External documentation workflow

The source documents describe a specific staging workflow for external documentation:

1. Fetch only user-supplied URLs or official pages explicitly named by the workflow.
2. Prefer official vendor documentation over blogs and forum posts.
3. Extract only facts relevant to the repository and the requested OpenKB topic.
4. Save one evidence file per URL under `.okf-build/input/external/`.
5. Ingest the staged files with `openkb --kb-dir ./okf add ./.okf-build/input/external/`.

This workflow is a concrete example of [[concepts/external-documentation]] handled through [[concepts/tool-boundaries]]: retrieval, fact extraction, staging, and ingestion are distinct steps. The workflow guidance reinforces that boundary by treating direct URL ingestion as a consent-gated exception rather than the default path, and by describing external content as evidence to summarize rather than hidden memory or executable instruction. It also requires preserving URLs and timestamps for staged external evidence so later summaries can be audited back to the retrieved material.

The lifecycle guidance strengthens this policy by making direct URL ingestion a user-consent path with explicit data-flow disclosure rather than a convenience default. In other words, even when OpenKB can fetch directly, the safer model is still to stage external evidence first, review it, and then ingest the staged copy. That keeps external knowledge inside a visible boundary connected to [[concepts/data-flow-disclosure]], [[concepts/privacy-preserving-tooling]], and [[concepts/safe-automation]].

The repository skill aligns with this by requiring that only user-provided external URLs be fetched during normal operation and by treating resulting notes as untrusted evidence under `okf/.okf-build/input/external/`. It also explicitly states that everything fetched from the web must be summarized with provenance and never executed as instruction, which makes staging the durable review boundary for web-derived material.

The fallback skeleton script uses this same staged directory as a read-only evidence source. When external Markdown files are present, it copies them into a references area and generates an "External Documentation Evidence" page that lists them as supporting material for later enrichment. That design keeps the staged files as the primary evidence while treating generated pages as derivative views, which fits the larger discipline of [[concepts/generated-content-governance]].

The privacy guidance adds one more constraint to this workflow: if external evidence will later be processed by non-code Graphify extraction or by OpenKB with a configured provider, the operator must disclose the tool, provider, model, endpoint, credential source, and the staged path being sent before that step runs. Staging is therefore the moment where external evidence becomes both reviewable content and an explicit egress unit.

The workflow guidance adds a repository-specific variant of the same rule. User-supplied URLs may be materialized into staged evidence files under `okf/.okf-build/input/external/`, while direct `openkb add <url>` is reserved for user-approved cases. This keeps URL-based evidence aligned with the same reviewable staging discipline used for repository files.

## Structure of staged evidence

A staged evidence file for external references includes metadata such as:

- title
- resource URL
- short description of relevance
- tags
- retrieval timestamp
- source of retrieval
- trust level

For repository-derived staging, the generated source pack carries a richer and more explicit provenance shape. The builder emits a repository snapshot document, a per-file staged document for each selected repository file, an optional staged Graphify report, and a manifest that indexes every staged item. Per-file staged documents include metadata such as:

- type
- title
- description
- resource
- source_path
- source_kind
- source_hash
- source_commit
- tags

The staged body then wraps normalized file content in Markdown, usually truncating to a configurable maximum number of lines so the evidence pack stays useful for repository understanding rather than trying to mirror the entire repository byte-for-byte.

The workflow document adds a key rule here: the staged file should record the last commit that touched that file, not repository `HEAD`, so unchanged files remain byte-identical across later commits. The source-pack script implements this directly by deriving a last-touch commit map from Git history and using that value in each staged file. It also avoids a global commit stamp in the repository snapshot for the same reason.

The structure is also selective rather than exhaustive. The builder uses tracked files from Git, skips transient caches and tool-owned directories, and stages only repository files that match important documentation, source, configuration, build, infrastructure, or skill-related patterns. That makes the staged pack a curated evidence layer rather than a blind filesystem dump, which further connects staging to [[concepts/repository-ingestion]], [[concepts/knowledge-boundaries]], and [[concepts/heuristic-classification]].

The lifecycle guidance adds another structural constraint around privacy and portability: the OpenKB hash registry records a `path` field, and if staging happens outside the KB root that field can become an absolute host path. Staging inside `okf/` avoids leaking machine-local paths into a committed registry and keeps the evidence package more portable. That detail makes staging structure matter not only for provenance but also for [[concepts/privacy-preserving-tooling]], [[concepts/path-safety]], and [[concepts/kb-root-staging]].

Repository staging may also include derived structural evidence such as a refreshed Graphify report when [[entities/graphify]] is installed. The source-pack builder stages that report only after normalizing away run-dependent timestamps and date suffixes in headings, so the structural evidence remains informative without becoming a source of daily hash churn. That report becomes part of the staged input only after the graph is updated, which keeps structural context synchronized with the repository state seen by later compilation.

The source-pack builder also supports an alternate structure for scale: bundled staging. Instead of emitting one staged document per selected file, it can group files by directory prefix and build a per-directory digest document containing member file sections, per-member hashes, per-member last-touch commits, and a bundle hash for the group. This keeps the handoff deterministic while changing the evidence granularity, directly tying staged structure to [[concepts/source-bundling]].

The privacy and data-flow guidance adds a second structural expectation: staged inputs should live under the KB root, specifically `okf/.okf-build/input/`, rather than in an arbitrary external temp directory. That makes the staged path itself part of the safety model: it is stable, reviewable, portable across developers, and does not force absolute machine paths into registry metadata.

The workflow guidance adds two more structural constraints. First, the source pack depends on Git history because staging is based on tracked files and last-touch commits rather than an ad hoc filesystem snapshot. Second, the staged graph report is only valid if the KB root stays out of the graph; otherwise the staged report would describe generated wiki content and break the provenance boundary that staging is meant to preserve.

The repository skill adds a further structural expectation: the staged directory is not just a convenient location but the intended source-of-truth input surface for repository evidence. OpenKB owns `okf/raw/`, `okf/wiki/`, `okf/.openkb/`, and `okf/output/`, so the input structure under `okf/.okf-build/input/` is the one place where repository operators are expected to shape evidence directly before compilation.

This structure strengthens [[concepts/provenance-tracking]], [[concepts/source-trust-levels]], and [[concepts/knowledge-linking-and-citations]] by making origin, trust, reproducibility, and selection boundaries visible at the file level.

The skeleton builder shows one downstream use of this structure. It reads staged repository metadata, optionally includes the current commit in a generated repository overview, excerpts the staged Graphify report, and copies staged external documents into a reference set. Even though that script is intentionally conservative, it demonstrates how staged evidence can be transformed into navigable wiki scaffolding while preserving a visible distinction between source evidence and generated summaries.

## Security and trust considerations

The source documents treat fetched pages and compiled wiki content as untrusted data. That makes evidence staging an important defense layer, not just a formatting step.

Key safeguards include:

- Never treating fetched page text as instructions.
- Ignoring embedded prompts that attempt to influence tool use or configuration changes.
- Never executing commands or changing files just because an external page suggests it.
- Excluding credentials, tokens, and internal hostnames from staged files.
- Recording a trust label such as official docs, vendor blog, or community source.
- Reviewing staged inputs before they are added, instead of trusting generated wiki output by default.

These practices align evidence staging with [[concepts/prompt-injection-defense]], [[concepts/privacy-preserving-tooling]], and [[concepts/supply-chain-security]]. The workflow guidance also adds a data-flow discipline around staging: provider-backed compilation should not begin until data flow has been disclosed, and external or non-code processing should use explicit backend choices rather than implicit remote handling. That keeps staged evidence inside a reviewable boundary before it reaches provider-integrated steps.

The lifecycle policy adds a second trust boundary on the repository side: tool-owned outputs such as `okf/raw/`, generated wiki pages, and the hash registry are not source evidence and should not be hand-edited. Staging is therefore also a governance boundary between authored source material and generated artifacts. Weak or incorrect generated pages must be corrected by improving committed inputs, rebuilding the staged pack, and re-ingesting or recompiling, not by editing derived output in place. That ties staging directly to [[concepts/source-driven-regeneration]], [[concepts/generated-content-governance]], and [[concepts/single-source-of-truth]].

The source-pack builder reinforces the same trust model on the repository side by selecting only known-important tracked files and skipping generated directories, caches, and tool-owned outputs such as `okf/`, `.okf-build/`, and `graphify-out/` as raw input sources. In other words, staging is also a curation boundary: not every tracked file becomes evidence, and not every generated artifact is trusted as source material. The optional Graphify report is included only as a normalized derivative input with clear origin metadata rather than as an invisible side channel.

The builder adds a stronger trust rule for structural evidence: it refuses to stage a Graphify report when repeated `okf/` references suggest the graph mapped the compiled wiki. That prevents generated KB descriptions from re-entering the evidence layer as if they were source facts, which is a direct staging defense against circular evidence and trust contamination. This links evidence staging to [[concepts/self-reference-control]] and [[concepts/knowledge-boundaries]].

The fallback path preserves the same trust model. The skeleton script copies and repackages staged evidence but does not claim semantic authority; its generated pages explicitly warn that they must be validated and enriched before being treated as authoritative. That warning is an important governance signal: generation does not upgrade trust, and staging remains the place where evidence quality and safety must be judged.

The privacy guidance sharpens this boundary by insisting that tools must not silently choose providers, and that the selected backend for non-code processing must always be explicit. In practice, this means staging is where operators confirm not only that evidence is relevant and safe, but also that the next processing route matches the chosen privacy policy. That links staging directly to [[concepts/explicit-provider-routing]], [[concepts/provider-integration]], and [[concepts/tooling-consent-and-pin-management]].

The workflow guidance adds a structural trust rule that matters for generated structural evidence: the KB root must stay out of Graphify analysis. If the graph report includes `okf/`, then staged structural evidence begins describing generated wiki artifacts rather than repository sources, creating a circular citation path and discovery pollution. Staging therefore protects against self-reference as well as prompt injection and provider misuse.

The repository skill adds another trust layer around tool adoption itself. It requires explicit user consent before installing or invoking optional tooling in new contexts, demands provenance and pinning details, and treats vendor skill copies as part of safe tool adoption. In that broader operating model, staged evidence is the data boundary that sits next to tooling-consent controls: even when the tools are approved, the evidence they will consume must still pass through a visible, reviewable staging surface.

## Determinism and exceptions

Most repo-derived staged files avoid timestamps to preserve deterministic outputs, but web-fetched evidence is an explicit exception. Retrieval time is part of the provenance of external material, so including a timestamp is necessary even when other staged artifacts avoid time-based variation. This creates a practical boundary between [[concepts/deterministic-validation]] and accurate source recording.

The workflow document adds a stronger determinism rule for repository staging: the source pack must be deterministic across commits, not merely within one run. Each staged file should therefore reflect the last commit that touched it, and unchanged repository files should produce byte-identical staged outputs. This works together with OpenKB's hash registry so repeated ingestion skips already-known material instead of churning identical evidence.

The source-pack builder provides the implementation details behind that rule. It normalizes UTF-8 text and line endings before hashing, computes `source_hash` from normalized text, sorts manifest entries, and strips volatile lines from staged Graphify reports. It also uses the last-touch commit for each file instead of repository `HEAD`, and omits a global commit stamp from the repository snapshot. Together these choices show that determinism in staging is not a vague principle but a concrete set of normalization, provenance, and naming rules.

The builder also makes deterministic cleanup part of the process. It removes stale staged repository file directories and old snapshot or graph-report outputs before rebuilding, so the resulting input pack reflects the current selected evidence set rather than an accumulation of old artifacts. This keeps the staged handoff aligned with [[concepts/generated-content-governance]] as well as [[concepts/deterministic-builds]].

The lifecycle guidance adds a second determinism rule: staging must be rebuilt from committed or otherwise clearly tracked source inputs before `openkb add`, because staging alone does not update the KB and because repeated ingestion depends on registry-backed deduplication. Determinism here is not only about file contents but also about preserving a repeatable compile path.

That same guidance also describes an important exception in scale management: for very large repositories, the main control point is the staging layer itself. Per-file evidence may be too granular, so bundled staging can be used to concatenate related files into stable digest documents. This changes evidence granularity without changing the principle that all KB updates should flow through a deterministic staged handoff.

The skeleton builder introduces a small but useful contrast. Its output is intentionally conservative and can include the current repository `HEAD` in a generated overview page, while the staged source pack aims to remain stable at the file level. This highlights an important distinction: evidence staging is where determinism is enforced most strictly, while generated presentation layers may include convenience metadata so long as they remain clearly derivative and non-authoritative.

The privacy guidance adds a final determinism-related rule around location: the staged handoff should remain inside the KB root so the registry records KB-relative paths rather than absolute machine paths. This does not change deduplication semantics, but it does change whether repeated collaboration produces portable, low-noise metadata. In that sense, path locality is part of deterministic staging practice, not just a storage preference.

The workflow guidance adds one more exception boundary: external evidence intentionally keeps retrieval timestamps, while repository staging strips volatile data and avoids daily graph backup churn. Determinism is therefore applied selectively according to whether a field is part of the evidence itself or merely an artifact of the build process.

The repository skill adds one more operational exception: a zero-LLM skeleton fallback may write directly into `okf/wiki/`, but only as a clearly reported fallback rather than the normal compilation path. That exception confirms the rule: evidence staging remains the standard deterministic handoff, and direct wiki generation is special-case recovery behavior rather than ordinary maintenance.

## Relationship to OpenKB workflows

Evidence staging helps [[entities/openkb]] ingest curated, well-scoped inputs instead of raw browsing output. The lifecycle guidance makes this the preferred path for repository maintenance: rebuild the staged input, add that staged path, and use recompilation when generated pages need to be refreshed.

The workflow document makes this relationship more explicit by placing staging in the middle of the full repository build sequence: prerequisites, ignore rules, line-ending normalization, graph refresh, source-pack build, KB initialization, staged ingest, lint, and validation. In that sequence, staging is the last source-controlled checkpoint before generated wiki output begins.

The source-pack script clarifies what the repository side of that checkpoint looks like in practice. It writes the staged pack under `.okf-build/input`, stores per-file evidence under `repo-files/`, emits a machine-readable manifest, and prints the next-step `openkb add` command while reminding the operator that staging alone does not update `okf/raw/` or `okf/wiki/`. That operational reminder matters: evidence staging is the handoff contract, not the final compilation result.

It also shows that the staged handoff is broader than a file mirror. The pack always includes a repository snapshot, may include a normalized Graphify report, and can switch between per-file and bundled evidence modes. In OpenKB workflow terms, staging is therefore both an ingestion payload and a policy surface where evidence granularity, provenance fidelity, and structural context are chosen before compilation begins.

The lifecycle guidance further explains why staging remains central after initial ingest. OpenKB deduplicates by hash through its registry, so damaged generated pages are not automatically healed by re-adding unchanged evidence. If the registry says a document is already present, `add` may silently skip it even when the corresponding wiki pages are missing. That is why staging belongs to a larger maintenance discipline tied to [[concepts/hash-registry-coherence]] and [[concepts/registry-drift]]: repair must happen through controlled recompile or remove-and-readd flows, not by hand-editing generated wiki pages.

The post-generation review pass in the workflow reinforces the same principle from the opposite direction. After `openkb add` or recompile changes the wiki, the generated pages are reviewed for missing concepts, near-duplicates, lost caveats, truncation, grounding, and entity-versus-concept mistakes. But corrections still route back through source fixes, rebuild, and re-ingest. In other words, staged evidence is both the preferred input to compilation and the preferred place to repair the knowledge pipeline when outputs are wrong.

The conservative skeleton path fits into the same lifecycle. Instead of replacing staging, it consumes the same staged pack to produce a minimal `okf/wiki` baseline when richer compilation is unavailable. Its generated repository overview, copied references, root index, and log file show that staging is the stable contract between source preparation and any downstream build mode, whether provider-backed, local-only, or reduced to a bootstrap scaffold.

With user consent, OpenKB can fetch a URL directly. Even then, the staging model remains the safer conceptual standard for deciding what should be captured, how it should be attributed, and what review and safety checks should apply.

The privacy and data-flow guidance makes this lifecycle boundary more explicit. Before the first OpenKB LLM-backed command or any Graphify run over non-code sources, the operator should disclose the tool, provider, model, endpoint, credential source, and the staged content path being sent. Repeat the disclosure whenever those routing details change. In that workflow, staging is the named payload boundary for consent, auditing, and provider selection, not just the filesystem path that happens to be ingested.

The workflow guidance also establishes staging as the point where degraded modes stay well-defined. If Graphify fails, the pipeline can continue without structural evidence; if no provider is available, the system can still produce a skeleton bundle. In both cases the staged evidence layer remains the stable input contract, which is why staging sits at the center of both normal and degraded OpenKB workflows.

The repository skill adds a repository-wide framing for this relationship. It defines the split between actions, durable context, and orientation; positions `okf/wiki/` as the long-term context surface; and makes staged ingest the normal path by which repository evidence enters that context. In practice, this means evidence staging is not an isolated OpenKB convenience but a central part of making a repository agent-ready under [[concepts/agent-ready-repositories]] and [[concepts/agent-context-layering]].

## Source basis

This concept is derived from [[summaries/agents__skills__agent-ready-context__references__external-docs-md]], which defines the external documentation evidence process, the evidence file template, and the safety rules for handling fetched content; from [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], which defines the staged-ingest and regeneration policy for maintaining an OpenKB-backed OKF; from [[summaries/agents__skills__agent-ready-context__references__workflow-md]], which defines the end-to-end repository build workflow, deterministic source-pack rules, self-reference controls, and the review process around staged ingest and recompilation; from [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]], which shows how the staged source pack can drive a conservative zero-LLM wiki skeleton and clarifies the boundary between evidence, references, and generated pages; from [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], which shows how repository evidence is normalized, selected, wrapped, manifested, and optionally bundled into a deterministic OpenKB-ready source pack, including graph-report normalization and self-reference guards; from [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], which defines the disclosure, explicit-routing, air-gapped, and KB-root staging constraints that make staged evidence the main privacy boundary before provider-backed processing; and from [[summaries/agents__skills__agent-ready-context__SKILL-md]], which defines staged input under `okf/.okf-build/input/` as the normal repository-to-OKF handoff, formalizes the split between durable context and executable actions, and warns against repairing generated wiki output by editing tool-owned files directly.

## Related pages

- [[concepts/external-documentation]]
- [[concepts/provenance-tracking]]
- [[concepts/source-trust-levels]]
- [[concepts/prompt-injection-defense]]
- [[concepts/deterministic-validation]]
- [[concepts/tool-boundaries]]
- [[concepts/hash-registry-coherence]]
- [[concepts/generated-content-governance]]
- [[concepts/data-flow-disclosure]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/offline-first-workflows]]
- [[concepts/tooling-context-isolation]]
- [[concepts/repository-ingestion]]
- [[concepts/deterministic-builds]]
- [[concepts/document-normalization]]
- [[concepts/incremental-compilation]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/path-safety]]
- [[concepts/safe-automation]]
- [[concepts/single-source-of-truth]]
- [[concepts/registry-drift]]
- [[concepts/explicit-provider-routing]]
- [[concepts/kb-root-staging]]
- [[concepts/provider-integration]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/self-reference-control]]
- [[concepts/knowledge-boundaries]]
- [[concepts/frontmatter-metadata]]
- [[concepts/heuristic-classification]]
- [[concepts/line-ending-normalization]]
- [[concepts/source-bundling]]
- [[concepts/durable-context]]
- [[concepts/context-action-separation]]
- [[concepts/agent-ready-repositories]]
- [[concepts/agent-context-layering]]
- [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]