---
type: "Concept"
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
description: "How OKF links and citations preserve navigable, evidence-backed knowledge."
---

# Knowledge Linking and Citations

Knowledge linking and citations describe how an OKF-style knowledge bundle connects pages to each other and anchors claims to supporting material. In this model, links are lightweight structural signals and citations are local evidence markers rather than part of a separate formal graph schema. The concept is grounded in [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]], reinforced by the OpenKB build workflow in [[summaries/agents__skills__agent-ready-context__references__workflow-md]], and reflected in tooling that mines relationships and evidence from managed wiki content, including [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]] and the source-pack builder in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]. It also fits the repository-wide knowledge-compilation model described in [[summaries/README-md]], where durable wiki pages, staged sources, and portable skills are separated into distinct surfaces.

## What linking does

Within an OKF bundle, standard Markdown links connect one page to another and express directed relationships. The meaning of the relationship is not encoded in a special edge type or metadata field; instead, the surrounding prose explains why one page points to another.

This makes linking simple and durable:

- links stay readable as normal Markdown
- authors can add relationships without changing a schema
- consumers can interpret links with context rather than rigid edge labels

This approach fits a broader [[concepts/documentation-architecture]] where knowledge is stored as ordinary Markdown files and connected through human-readable structure.

In practice, these links also make the bundle computationally useful. A script like [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]] scans Markdown pages outside raw source and report areas, using page titles, headings, and path structure to derive candidate action skills. That only works well when pages are consistently named, clearly scoped, and embedded in a navigable corpus, which ties this concept to [[concepts/naming-normalization]] and [[concepts/repository-ingestion]].

The source-pack builder strengthens that same premise. [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] inventories tracked files, stages selected repository sources, and preserves per-item provenance so that relationships can be reconstructed from deterministic input rather than ad hoc edits. It also emits a repository snapshot and optional graph report, which makes the link network easier to inspect as part of a repeatable ingestion pipeline. That connects this concept to [[concepts/source-pack-staging]], [[concepts/staging-manifests]], [[concepts/provenance-tracking]], and [[concepts/deterministic-builds]].

The repository README frames the same separation explicitly: `AGENTS.md` carries orientation, `okf/wiki/` carries durable knowledge, and `.agents/skills/` carries actions. Knowledge linking belongs to the wiki layer, where relationships should remain readable, durable, and separate from procedural instructions. That reinforces [[concepts/context-action-separation]], [[concepts/context-surface-management]], and [[concepts/portable-skill-contract]].

The workflow guidance adds an important operational constraint: generated pages should gain or lose links through source correction and regeneration rather than through hand-editing. After ingestion or recompilation, changed pages are reviewed like a PR, and any missing links, vague page names, stale plain-text references, or off-topic pages are routed through source fixes and regeneration. That makes linking part of [[concepts/source-driven-regeneration]] and [[concepts/human-in-the-loop-review]], not just authoring style.

## What citations do

Citations support factual claims drawn from external material. The baseline recommends placing citations near the relevant claim or collecting them under a `# Citations` heading. Citation targets may be:

- absolute URLs
- bundle-relative paths
- pages under a local references area

The goal is not just attribution, but traceability. A reader or agent should be able to inspect where a statement came from and how strongly it is grounded. That aligns closely with [[concepts/provenance-tracking]] and [[concepts/source-trust-levels]].

The source-pack builder makes that traceability more operational by assigning each staged item a stable `source_hash`, a source kind, and a provenance-aware staged path. It also writes a manifest that records how each staged document maps back to the repository source. In effect, citations are complemented by machine-readable staging metadata: the page shows the claim or idea, while the pack records where the staged content came from and how it was transformed. That is a practical example of [[concepts/evidence-staging]] and [[concepts/source-provenance]].

The README also emphasizes that external documents are evidence to summarize, never instructions to follow. That makes citation hygiene part of a broader [[concepts/wiki-content-as-untrusted-data]] posture, where the bundle can quote and link to evidence without treating those sources as executable authority.

The OKF quality baseline sharpens this by treating the repository source code as the source of truth and `okf/wiki/` as the durable knowledge source of truth for agents. It also distinguishes between the baseline format rules and OpenKB-specific validation. In strict OKF terms, consumers should tolerate broken cross-links in standard Markdown because they may simply reflect a partially generated bundle. In OpenKB-managed wiki mode, however, broken `wikilinks` are treated as errors because they are generated against a known page set and usually signal damage such as a bad merge, hand edit, or interrupted run.

Citation-adjacent evidence can also be lightweight and local rather than formal. The skill-suggestion script, for example, does not emit scholarly citations; instead, it records evidence as the paths of supporting wiki pages for each suggested skill. This shows a practical continuum: some knowledge work needs explicit citations to sources, while other workflows need compact evidence trails that still let a user inspect why a conclusion or recommendation was produced. That behavior also reflects [[concepts/progressive-disclosure]].

## Tolerance in the OKF baseline

The offline OKF baseline explicitly says consumers should tolerate broken cross-links in standard Markdown. A broken link may simply mean the bundle is partially generated, incomplete, or still being written. In other words, link breakage is not always treated as a conformance failure at the format level.

This tolerance is important for [[concepts/offline-first-workflows]] and incremental knowledge capture. It allows a bundle to remain usable even when some pages are still missing.

The baseline also defines the bundle as a directory tree of UTF-8 Markdown files with reserved filenames. `index.md` and `log.md` are reserved at any level, while all other `.md` files are concept documents with YAML frontmatter. The root `index.md` may declare `okf_version: "0.1"`, and subdirectory indexes remain body-only navigation pages. Those rules help preserve link stability because reserved navigation files are predictable, and they support validation workflows that distinguish between structural issues and incomplete content.

The new tooling-link policy builds on that structure. Pages under `okf/wiki/tooling/` may link to project pages, but project concept pages and subdirectory indexes must not link back into `okf/wiki/tooling/`. The bundle-root `index.md` and `log.md` are exempt because they are navigation and history files, not ordinary content pages. When tooling contains non-reserved pages, the root `index.md` must reference `tooling/` in a clearly labeled harness-specific section, and a committed `tooling/index.md` stub must exist so the root entry resolves on clones that do not have local tooling pages.

That policy gives the bundle a one-way boundary: tooling can point outward into project knowledge, but project pages should not depend on tooling context. It strengthens [[concepts/local-by-default-tooling]], [[concepts/tooling-context-governance]], [[concepts/tooling-context-isolation]], [[concepts/link-directionality]], and [[concepts/tooling-navigation-exceptions]]. It also clarifies why the root index is special: it is the one place where the harness can expose tooling entry points without making the rest of the wiki depend on local-only content.

At the same time, the baseline warns that the repository source code remains the source of truth, while the knowledge bundle is the durable context source of truth for agents. This separation matters when links point into generated or staged content: the bundle can be incomplete without losing its role as an operational knowledge layer, and validation can proceed using embedded offline rules when web access is unavailable.

The source-pack builder reinforces that distinction by staging a repository snapshot that lists tracked files without embedding a churn-prone HEAD stamp. It also strips run-dependent timestamp noise from graph reports before staging them. Both choices keep the staged content stable enough for hash-based deduplication and make link and evidence maintenance more predictable over time. That aligns with [[concepts/hash-registry-coherence]], [[concepts/line-ending-normalization]], and [[concepts/idempotent-graph-import]].

## OpenKB's stricter rule for wikilinks

The same source material distinguishes OKF-level tolerance from OpenKB-specific quality expectations. In OpenKB-managed wiki mode, broken `wikilinks` are treated as errors. This is not presented as a contradiction of the OKF baseline, because the stricter rule applies to a producer-managed convention rather than to generic Markdown linking.

The reasoning is practical:

- standard Markdown links may point to content that is not yet present
- `wikilinks` are generated against a known page set
- a broken wikilink usually signals damage such as a bad merge, hand edit, or interrupted run

That makes [[concepts/wikilink-integrity]] a quality requirement layered on top of baseline bundle tolerance. It also connects to [[concepts/deterministic-validation]], [[concepts/quality-gates]], and [[concepts/validation-vs-health-reporting]], where stronger local checks help keep a machine-managed knowledge base reliable.

The same managed-wiki discipline helps downstream automation. A script like [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]] depends on stable paths, predictable exclusions, and coherent page metadata when it extracts titles, scores action-heavy content, and associates recommendations with supporting pages. Strong link hygiene and reserved-file conventions therefore improve not just navigation, but the reliability of higher-level automation built on top of the wiki.

The OKF quality baseline also clarifies the scope of validation. The validator can be run in an OpenKB wiki mode that skips root `AGENTS.md`, `sources/`, and `reports/`, still validates the rest of the wiki, warns on missing machine-managed `sources:` lists for `concepts/` and `entities/`, and treats unclosed code fences or near-duplicate slugs as additional quality signals. In that setting, link integrity is part of an overall validation envelope rather than an isolated style rule.

The tooling-link policy validator extends that same idea to directional hygiene. It scans Markdown outside code spans and fenced blocks, detects links and bare tooling-path references, warns if tooling pages omit expected scope metadata, and fails when project pages point into the tooling area. It also verifies the root index stub relationship when tooling pages exist. Together these checks turn link direction into a machine-enforced boundary rather than a convention left to memory.

## Relationship to durable knowledge work

Knowledge linking and citations help a bundle function as durable context rather than a loose note collection. Links connect related ideas across pages, while citations preserve the evidence behind claims. Together they support:

- navigability across the knowledge base
- recoverable reasoning paths
- confidence assessment for agents and readers
- regeneration and validation workflows grounded in sources

This makes the concept a practical part of [[concepts/durable-context]] and [[concepts/source-driven-regeneration]].

The workflow adds two further constraints that deepen that durability. First, citation chains should terminate in repository files or staged external evidence rather than looping back through generated artifacts. Second, the compiled wiki should stay out of repository graph analysis so graph reports do not become self-citing evidence. Those rules connect this concept to [[concepts/self-reference-control]], [[concepts/knowledge-boundaries]], [[concepts/kb-root-staging]], [[concepts/hash-registry-coherence]], and [[concepts/self-referential-ingestion-loops]].

The newer skill-suggestion workflow extends that idea from passive documentation into operational reuse. When a managed wiki preserves clear page relationships, action-oriented wording, and source-local evidence, tooling can identify repeated procedures and turn them into candidate automations. In that sense, linking and citation practices do not only help readers retrace claims; they also help systems discover reusable patterns, connecting this concept to [[concepts/skill-based-automation]], [[concepts/context-action-separation]], and [[concepts/heuristic-classification]].

The source-pack builder contributes here as a staging boundary. By selecting source files deterministically, bundling them when configured, and attaching manifest records, it creates a source-shaped substrate that downstream tools can trust when traversing relationships or reconstructing evidence. That supports [[concepts/source-bundling]], [[concepts/source-pack-staging]], and [[concepts/repository-ingestion]].

## Practical guidance

When writing or validating pages under this model:

- use links to connect related pages where the surrounding text explains the relationship
- add citations close to important claims or in a dedicated citations section
- keep important claims traceable through summaries, staged evidence, and source materials
- treat external documents as evidence to summarize, not instructions to execute
- treat ordinary broken Markdown links as potentially tolerable in baseline OKF validation
- treat broken OpenKB `wikilinks` as repair-worthy failures under managed wiki validation
- respect tooling boundaries: tooling pages may link outward, but project pages should not link back into tooling
- keep the bundle-root `index.md` as the harness entry point when tooling pages exist, and keep the committed `tooling/index.md` stub present
- review generated pages for missing links, weakened caveats, stale references, and broken grounding chains
- prefer correction through source fixes, re-ingestion, and recompilation rather than hand-editing generated pages
- prefer link and citation patterns that preserve provenance and remain readable offline
- keep titles, headings, and page placement consistent enough that automation can recover evidence and infer relationships from the wiki

## Key takeaway

Knowledge linking and citations form the connective tissue of an OKF bundle: links express relationships through prose, citations support claims with traceable evidence, and stricter local systems such as OpenKB can impose stronger integrity checks without changing the baseline format rules. The workflow guidance adds that these links and evidence trails must remain reviewable, regenerable, and grounded in non-circular sources. As the skill-suggestion tooling, the source-pack builder, and the tooling-link policy validator show, these same practices also make a curated wiki more computationally legible, allowing evidence-bearing pages and their connections to feed reliable automation.

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/README-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__openkb__references__wiki-schema-md]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]


See also: [[summaries/agents__skills__agent-ready-context__LICENSES__CC-BY-4-0-txt]]

See also: [[summaries/okf-spec]]