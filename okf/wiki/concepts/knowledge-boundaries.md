---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
description: "Rules that keep durable project knowledge separate from runtime-specific context."
---

# Knowledge Boundaries

Knowledge boundaries are the rules that separate durable project knowledge from context that is conditional, operational, generated, or tool-specific. In this wiki, the concept matters for preventing harness behavior notes, runtime adapter details, generated outputs, KB lifecycle policy, and AGENTS.md orientation material from being treated as authoritative project truth.

The boundary is made explicit across the agent-ready-context skill set: skills are the action layer, the OKF wiki is the durable context layer, and `AGENTS.md` is only the orientation/index/best-practices layer. That skill also states that the OKF wiki root is `okf/wiki/`, that generated files should not be written directly into `okf/raw/` or `okf/wiki/`, and that repository knowledge should be refreshed by staging deterministic inputs and re-ingesting rather than by patching compiled pages. The same document also makes the repo-setup boundary operational: read `okf/wiki/index.md` first when it exists, run preflight checks, keep build artifacts out of version control, and preserve a strict split between context, actions, and orientation.

This concept is illustrated directly by [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]], which defines a controlled exception for storing harness-specific tooling context while preserving a hard separation between project pages and tooling pages; by [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]], which excludes the compiled knowledge base from repository graph analysis so generated wiki artifacts do not get mistaken for source material; by [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], which makes the same distinction inside the OpenKB lifecycle by treating `okf/wiki/` as derived output and insisting that lasting fixes happen in committed source inputs rather than hand-edited generated pages; by [[summaries/agents__skills__agent-ready-context__references__workflow-md]], which turns those distinctions into an end-to-end build workflow with preflight checks, vendoring, ignore-file setup, deterministic staging, ingestion, validation, and post-generation review; by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], which stages repository sources into OpenKB-friendly inputs while preserving provenance, splitting oversized content, and avoiding churn from generated or self-referential artifacts; by [[summaries/README-md]], which frames the whole repository as a compiled knowledge system with clear surfaces for orientation, context, and actions; and by [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]], which codifies the boundary at the repo entry point by keeping operational basics in `AGENTS.md`, pointing to `okf/wiki/index.md` as the front door to durable context, and using `.agents/skills/` for executable workflows.

The subagent-profile-adapter skill adds another strong boundary layer: runtime adapters are projections for the active harness only, not a portable subagent standard. It requires explicit runtime detection, harness documentation checks, and user confirmation when the runtime is ambiguous. It also limits `.agents/` growth, prefers local aliases over tracked duplicates when a harness needs a different instruction file, and asks how generated harness-specific files should be tracked. This deepens the concept of knowledge boundaries by showing that even agent-facing runtime files need policy separation from project knowledge, action skills, and committed wiki content.

## Core idea

A knowledge boundary answers two questions:
- what kind of information belongs in the main project knowledge base
- what kind of information must remain isolated, optional, explicitly scoped, or excluded from analysis inputs

The tooling-context policy sharpens this distinction by allowing harness documentation and runtime adapter knowledge in OKF only in two cases: a required harness build record for each agent-ready pass, and optional adapter/profile documentation when a specific detected or user-selected harness is actively in use. That material is useful but non-authoritative, so it must live in a dedicated tooling area rather than in ordinary concept pages. It also treats the tooling area as user-scoped by default, with a committed navigation stub and local pages that must not be enumerated in committed indexes. The agent-ready-context skill applies the same logic at the repository level: use `AGENTS.md` for operational commands and safety notes, use the wiki for durable context, and use skills for repeatable procedures and workflows. It also adds a stronger navigation rule: `okf/wiki/index.md` is the first routed knowledge source after `AGENTS.md`, and its entries should determine what to open next.

The subagent-profile-adapter skill extends that same boundary into runtime adapter management. It says harness-specific subagent or profile files should be generated only after the repository has a refreshed `AGENTS.md`, refreshed `okf/wiki/`, and reviewed action skills; it also says adapter files should be short, should not embed long project context, and should point back to `AGENTS.md`, `okf/wiki/`, and skills instead of duplicating them. That is a direct example of knowledge boundary design: the adapter exists to route execution, not to become a second knowledge base.

The repository README makes the same pattern explicit in product form. `AGENTS.md` is the orientation surface, `okf/wiki/` is the compiled knowledge surface, `.agents/skills/` is the action surface, and harness adapters are projections for the active runtime only. The point is not just organizational neatness; it is to ensure that each surface is loaded only when useful and never asked to carry the responsibilities of the others.

The source-pack builder extends this into a practical staging boundary. It creates a repository snapshot without embedding the current `HEAD`, because that would churn hashes on every commit and defeat OpenKB deduplication. It then stages selected repository files with provenance metadata, optionally groups them into directory bundles, and splits oversized markdown or code files into full-content parts instead of truncating them. That means the staging layer preserves evidence while still keeping generated input deterministic and bounded.

The agent-ready-context workflow also strengthens the boundary by describing maintenance as incremental rather than regenerative: `openkb status`, `openkb list`, staged source-pack creation, `openkb add`, `openkb lint`, and `validate_okf_bundle.py` form a controlled lifecycle. The boundary here is procedural as well as structural — knowledge is updated through explicit, ordered steps rather than by ad hoc edits to compiled output.

The workflow document extends this into a practical build order. It requires a preflight check, consent-first bootstrap for missing hard requirements, vendoring of toolchain skills before CLI use, ignore-file setup, source-pack creation, optional graph update, deterministic ingestion, and validation before the wiki is treated as ready. That sequence is itself a knowledge boundary: structure and tooling state must be established before the compiled knowledge base is allowed to speak for the repository.

The graph ignore template in [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]] applies the same principle to generated artifacts: the wiki is a map of the repository, not part of the territory being mapped. If generated wiki pages are fed back into repository graph analysis, the system starts analyzing derivative knowledge as if it were primary evidence.

[[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]] extends that boundary into KB maintenance itself. It draws a hard line between committed repository knowledge, which may be staged and ingested, and OpenKB-managed outputs under `okf/raw/` and `okf/wiki/`, which must be regenerated rather than edited. It also distinguishes repository-domain knowledge from pipeline meta-knowledge: project facts belong in committed docs, while harness-scoped or workflow-specific context belongs in `AGENTS.md`, tooling pages, or runtime instructions instead of the target repo's main knowledge layer.

This makes knowledge boundaries closely related to [[concepts/tooling-context-isolation]], [[concepts/tool-boundaries]], [[concepts/minimal-tool-scoping]], [[concepts/self-reference-control]], and [[concepts/generated-content-governance]].

## Why knowledge boundaries matter

Without explicit boundaries, project knowledge bases tend to absorb operational details that are true only in a narrow runtime context, or generated outputs that should remain downstream from source material. That creates several risks:
- temporary harness behavior can be mistaken for stable project facts
- concept pages can become dependent on a specific execution environment
- agents may overgeneralize from tool-specific notes
- navigation structures may blur the difference between core knowledge and runtime support material
- generated wiki content may be re-ingested as if it were repository evidence
- graph analysis can enter a self-reinforcing loop that never converges
- hand edits to generated pages can desynchronize evidence, citations, and registry state
- pipeline guidance can leak into project knowledge and then persist as if it were domain truth
- staging can accidentally promote transient graph or build artifacts into durable inputs
- local tooling pages can become effectively invisible or orphaned if committed indexes try to enumerate them
- runtime adapter files can accumulate project context that should stay in the wiki instead of in harness-specific projections

The source policies address these risks by insisting that tooling context is conditional, not default; discoverable, but not central; and allowed to reference project knowledge without allowing project knowledge to depend on it. They also insist that generated knowledge products stay outside the analysis graph when the graph is meant to describe the repository itself. The source-pack builder strengthens this by keeping snapshot content, file selection, bundle grouping, commit provenance, and line-based splitting deterministic, so staged inputs remain evidence-like rather than environment-like. The OpenKB lifecycle document adds a stronger operational warning: once generated outputs and registry state drift apart, future ingestion may silently skip missing material, so a broken boundary can become durable rather than merely messy.

The README widens this argument from a KB-maintenance concern into a repository design principle: agent-ready repositories perform best when the context surface is intentionally small, curated, and high-signal. That is essentially a boundary policy for information density as well as for storage and analysis. It aligns with [[concepts/context-action-separation]], [[concepts/documentation-architecture]], [[concepts/progressive-disclosure]], [[concepts/knowledge-graph-analysis]], [[concepts/hash-registry-coherence]], and [[concepts/registry-drift]].

## Boundary rules in practice

The source documents express knowledge boundaries through concrete structural rules.

### Scoped storage

Harness-specific documentation belongs under a dedicated tooling subtree rather than among normal project concepts. This turns isolation into a filesystem rule, not just a writing guideline.

The tooling-context policy makes this explicit: `okf/wiki/tooling/` is a hand-authored OpenKB wiki exception with exactly two permitted uses, and it must not grow into a speculative documentation dump. When used, it needs a committed `index.md` stub and a root `index.md` entry that points at the stub without enumerating local pages. That keeps tooling context visible without turning local runtime notes into shared project truth.

The same storage rule appears in the OpenKB lifecycle and workflow docs: OpenKB owns `okf/raw/` and generated wiki pages, while human-authored corrections belong in committed source locations such as `docs/`, README files, architecture docs, or code comments. Tooling context may be hand-authored in a reserved area, but source-derived and generated content must not be mixed together casually.

The source-pack builder adds another storage discipline by staging source material into `okf/.okf-build/input` and placing generated per-file or per-bundle documents under `repo-files/`. It also creates a repo snapshot and optional graph report as distinct staged documents rather than folding them into ordinary source pages. That separation keeps inventory, analysis, and source content distinguishable.

The workflow document adds a repo-level bootstrap sequence that protects this separation: verify prerequisites first, vendor required skills, normalize line endings with `.gitattributes`, exclude the KB root from graph analysis, build the source pack deterministically, then ingest into `okf/`. That makes the boundary enforceable before any semantic compilation happens.

The repository README's installation and usage sections reinforce the same storage distinction by separating product skills from vendored toolchain copies, and by keeping operational setup, maintenance, and air-gapped operation in the repository docs rather than in the compiled wiki. `AGENTS.md` carries operational basics and repo rules, while conventions and rationale should move into `okf/wiki/index.md` and other compiled pages after refresh. That keeps the orientation file small, current, and non-authoritative for durable project knowledge.

The agent-ready-context skill adds one more storage rule: vendor skills installed by a skill manager are read-only, custom project skills belong only under `.agents/skills/`, and the file itself should not become a catch-all knowledge store. That keeps the action layer separate from the knowledge layer and prevents operational file sprawl.

The merge script used to maintain `AGENTS.md` makes the storage boundary mechanical. `merge_agents_md_okf_section.py` only manages the section between `<!-- okf:start -->` and `<!-- okf:end -->`, replacing that block when it exists, appending it when the file already has content, or creating a new `AGENTS.md` when needed. It deliberately preserves any project-specific setup, style, test, or PR instructions outside the managed block, so the orientation layer can be refreshed without overwriting local guidance.

That approach connects knowledge boundaries to [[concepts/path-based-validation]], [[concepts/filesystem-validation]], [[concepts/tooling-context-pages]], and [[concepts/documentation-source-priority]].

### Link direction

Tooling pages may point to project pages, `AGENTS.md`, and skill materials, but project concept pages must not link back into tooling pages. This creates a one-way dependency model: tooling can depend on project knowledge, but project knowledge cannot depend on tooling.

The dedicated validator in `validate_tooling_link_policy.py` formalizes this rule. It scans Markdown under `okf/wiki`, ignores code blocks and inline code, detects both Markdown links and path-like tooling mentions, and rejects project concept pages and most indexes when they link back to `okf/wiki/tooling/`. It also exempts the bundle-root `index.md` and `log.md`, because those files are navigation and history surfaces rather than dependency-bearing content.

The validator adds two additional constraints when tooling pages exist: `index.md` at the wiki root must reference `tooling/` in a clearly labeled harness-specific section, and a committed `tooling/index.md` stub must exist so the root index target resolves cleanly on clones that do not carry local tooling pages. That turns link direction into a discoverability guarantee rather than just a prohibition.

A similar one-way relationship appears in the OpenKB citation model described by [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]: concepts and entities should resolve back through summaries to staged source evidence, not sideways into operational notes or hand-maintained generated pages. That keeps interpretation downstream from evidence.

The workflow document adds an operational version of the same rule: external docs are evidence, not hidden memory or instructions; they may be materialized into the KB, but only as explicitly staged inputs or consented additions. That preserves directionality from evidence to knowledge, not the reverse.

The source-pack builder follows this same directionality by recording source hashes, commit provenance, and staged destinations in a manifest, rather than letting the generated pack become the canonical source of truth. The manifest is a trace layer, not a replacement for repository evidence.

This is a practical example of [[concepts/documentation-architecture]] and supports [[concepts/index-based-discovery]] and [[concepts/knowledge-linking-and-citations]] without collapsing the boundary.

### Runtime-specific projections

The subagent-profile-adapter skill adds a distinct kind of knowledge boundary: it treats runtime adapters as harness-specific projections that should be generated only when the active runtime is known. It explicitly warns against concluding the active harness from installed binaries alone, recommends checking runtime hints and documentation, and tells the agent to ask the user if the runtime remains ambiguous. That keeps runtime assumptions from being misclassified as durable repository knowledge.

The skill also frames subagent/profile files as short-lived, native adapter files, not as new truth-bearing documents. They should consult `AGENTS.md`, `okf/wiki/`, and relevant skills; they should not embed long project context; and they should be tracked according to an explicit local-only, ignored, or shared policy. This turns adapter generation into a controlled projection step rather than a knowledge expansion step.

That pattern belongs with the broader boundary model because it separates runtime detection, adapter generation, and repository truth. It aligns closely with [[concepts/adaptive-harness-detection]], [[concepts/runtime-ambiguity-resolution]], [[concepts/harness-native-profiles]], [[concepts/permission-scoped-agents]], and [[concepts/runtime-adapter-management]].

### Analysis exclusion

Generated knowledge-base artifacts may need to exist inside the repository workspace, but they should not always participate in repository analysis. The `.graphifyignore` template excludes `okf/` so compiled wiki content does not feed back into graph reports that OpenKB later re-ingests.

The workflow document makes that exclusion part of the standard build path by requiring the KB root to be ignored before graph updates and by warning that self-reference causes structural loops, circular grounding, and discovery pollution. The OpenKB lifecycle reinforces the same rule from the ingestion side: staging alone does not update the KB, only explicit ingestion does, and generated wiki outputs are not valid substitutes for staged evidence. The boundary therefore applies both to graph analysis inputs and to KB compilation inputs.

The source-pack builder enforces the same idea in a different place: it strips volatile timestamps from generated reports, skips graph reports that reference KB paths too heavily, and avoids embedding volatile HEAD-based metadata in staged snapshots. That keeps derivative artifacts from cycling back into the evidence stream as if they were stable inputs.

The README adds a related exclusion rule at the product level: the vendored `graphify` and `openkb` directories in `.agents/skills/` are copies of toolchains, not products to be passed around as project context. Copy only the three core skills. In other words, generated or vendored material may be necessary for operation, but it should not be recast as durable project knowledge.

This expresses a different kind of boundary: not just where information is stored, but whether derivative artifacts count as valid inputs to a given analysis step. It keeps repository mapping focused on source material rather than on the generated map itself.

That practice connects knowledge boundaries to [[concepts/generated-content-governance]], [[concepts/repository-ingestion]], [[concepts/source-driven-regeneration]], and [[concepts/evidence-staging]].

### Reserved exceptions

The root `index.md` and `log.md` may mention tooling so the bundle remains visible and auditable. These files act as navigation and history surfaces rather than concept-level endorsements, which preserves the separation between discovery and dependency.

The OpenKB lifecycle document adds two more controlled exceptions: `okf/wiki/AGENTS.md` is a supported conventions extension point, and `okf/wiki/tooling/` may be hand-authored as harness context rather than ingested source material. These are explicit exceptions because they remain scoped, documented, and structurally separate from the main project knowledge layer.

The agent-ready-context skill adds a complementary exception model for the source repository: vendor skills are read-only and custom project skills belong only under `.agents/skills/`, with the file itself acting as an orientation index instead of a catch-all knowledge store.

This connects to [[concepts/reserved-wiki-files]], [[concepts/tooling-navigation-exceptions]], and [[concepts/wikilink-integrity]].

### Validation and enforcement

The policy is not merely advisory. The dedicated validator checks for forbidden project-to-tooling links, required root references to tooling when local tooling pages exist, and the presence of a committed `tooling/index.md` stub. The graph ignore template likewise encodes an operational enforcement rule by keeping `okf/` out of graph traversal. That means the boundary is machine-enforced in both navigation structure and analysis inputs.

[[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]] adds another enforcement layer: `openkb lint` reports structural and knowledge issues, while `validate_okf_bundle.py --openkb-wiki` acts as the pass/fail gate for wiki structure, broken links, and citation-chain expectations. The workflow document fits into this enforcement stack by placing validation after ingestion and by requiring a review pass over any generated `okf/wiki/` changes. The boundary is therefore preserved not just by author discipline but by executable checks over paths, links, registry coherence, and generated page structure.

The source-pack builder complements those checks with deterministic staging: it records stable hashes, preserves the last-touch commit where possible, splits oversized files into reproducible parts, and emits a manifest that can be linted or reconciled later. That makes boundary enforcement reproducible instead of ad hoc.

This makes knowledge boundaries part of [[concepts/executable-validation]], [[concepts/okf-validation]], [[concepts/deterministic-validation]], [[concepts/quality-gates]], and [[concepts/validation-vs-health-reporting]].

## Relationship to project truth

A key detail from [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]] is that tooling pages describe interchangeable harness behavior, not project truth. The distinction matters because the same project may be used through different harnesses over time. If harness notes are merged into ordinary concept pages, the wiki starts encoding contingent execution assumptions as if they were universal facts.

The dedicated validator extends the same logic into the page graph. If project pages can freely point into tooling pages, those pages start to function as hidden dependencies instead of scoped exceptions, and a local runtime note can quietly become part of the project's durable semantic fabric.

The graph ignore template extends the same logic to generated outputs. If compiled wiki pages are treated as graph inputs, derivative descriptions of the repository start masquerading as repository truth. The system then loses the distinction between evidence and interpretation.

[[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]] sharpens this further by stating that weak pages should be fixed by improving committed source inputs, never by polishing generated outputs in place. It also warns against seeding pipeline meta-concepts into a target repository's KB, because guidance about OpenKB or the harness may be true for the workflow without being part of the repository's domain knowledge.

The workflow document reinforces the same separation by making consent, disclosure, and deterministic staging prerequisites to semantic ingestion. It treats external URLs as evidence, requires data-flow disclosure before the first LLM-backed command, and insists that the compiled wiki is a product of the repo, not a substitute for it.

The README reinforces that same separation by describing the wiki as compiled durable knowledge and the skill directories as the operational layer. That framing makes the project's truth surfaces explicit: source files tell the compiler what exists, the wiki records the compiled understanding, and actions remain in skills. The source-pack builder reinforces that separation by deriving staged output from repository state while preserving source hashes and source paths in the manifest. The stage is intentionally downstream from the repository, so the generated pack can be rebuilt, compared, or discarded without altering the source truth that produced it.

The agent-ready-context skill reinforces the same separation by telling maintainers to keep the operational basics in `AGENTS.md` and move conventions and rationale into the wiki after each OKF refresh. That is a practical guardrail against letting orientation notes become authoritative project truth.

Knowledge boundaries protect against that drift by keeping project truth durable, keeping runtime-specific context explicitly scoped, keeping generated artifacts from contaminating source analysis, and keeping lifecycle policy distinct from repository subject matter. This supports [[concepts/durable-context]], [[concepts/source-trust-levels]], [[concepts/frontmatter-metadata]], and [[concepts/provenance-tracking]].

## Default-minimal behavior

Another important part of the source policy is the default artifact rule: do not create tooling pages or related diagnostic artifacts during baseline bootstrap. Tooling context appears only when specifically needed.

The tooling-context policy makes this minimalism explicit by allowing only the required harness build record and the optional harness-specific context page, while forbidding speculative accumulation beyond those cases. The workflow document makes that restraint operational. It begins with a prerequisite check, offers optional-tool bootstrap only on consent, proceeds through vendoring and ignore-file setup only when needed, and falls back to a skeleton bundle when no provider is available. That keeps the build usable without pretending the full semantic pipeline is always present.

The same minimal principle is visible in the graph ignore template. The repository may contain generated wiki output for practical reasons, but analysis should exclude it unless there is a deliberate reason to make it part of the graph.

The source-pack builder follows the same restraint by only staging files that pass selection and skip rules, by limiting inventory to tracked files, and by leaving deletion handling to a separate reconciliation step. It stages enough to compile, but not so much that transient or out-of-scope material gets treated as durable knowledge.

The OpenKB lifecycle document applies the same discipline to ingestion and repair: read the existing wiki first, use query only as a last resort, ingest only deterministic staged inputs or explicitly approved external material, and avoid broad recompilation or destructive cleanup without consent. A good boundary therefore limits not only storage and participation by default, but also the kinds of maintenance actions that are treated as routine.

The README mirrors that restraint by keeping the file focused on setup, build, and testing basics rather than expanding it into a full knowledge dump. Durable context moves into the wiki; repeatable actions move into skills; and context that is only conditionally useful stays scoped.

This shows that a boundary is not just about where information goes, but also about when it should exist at all, when it should be considered valid evidence, and when it should be allowed to trigger regeneration. In that sense, knowledge boundaries reinforce [[concepts/generated-content-governance]], [[concepts/generated-artifact-adoption]], [[concepts/baseline-first-testing]], [[concepts/safe-automation]], and [[concepts/data-flow-disclosure]].

## Practical takeaway

Knowledge boundaries let a wiki include operationally useful context without confusing that context for the project itself. In the tooling-context policy, dedicated validator, graph ignore template, source-pack builder, OpenKB lifecycle policy, workflow document, README, AGENTS.md template, and subagent-profile-adapter skill, the boundary is maintained through scoped storage, one-way linking, reserved navigation exceptions, validator-backed enforcement, explicit exclusion of generated knowledge artifacts from repository graph analysis, deterministic staging, consent-first bootstrap steps, runtime-aware adapter generation, and a strict rule that durable corrections must be made in committed sources rather than generated outputs.

The `merge_agents_md_okf_section.py` script shows how that policy can be applied mechanically to repository orientation. It manages only a bounded OKF section inside `AGENTS.md`, preserving local instructions while keeping the orientation layer aligned with the wiki front door and the active skill workflow. That makes the boundary repeatable instead of purely editorial.

Use this concept whenever a repository needs to preserve core knowledge as stable, reusable, and harness-independent while still allowing narrowly scoped runtime notes, KB lifecycle conventions, and generated outputs to exist in controlled ways.

## See also

- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tool-boundaries]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/context-action-separation]]
- [[concepts/documentation-architecture]]
- [[concepts/index-based-discovery]]
- [[concepts/executable-validation]]
- [[concepts/self-reference-control]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/hash-registry-coherence]]
- [[concepts/registry-drift]]
- [[concepts/source-driven-regeneration]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/harness-native-profiles]]
- [[concepts/permission-scoped-agents]]
- [[concepts/runtime-adapter-management]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__openkb__references__commands-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
