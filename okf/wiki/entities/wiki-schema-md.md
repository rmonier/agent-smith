---
sources: ["summaries/okf-spec.md", "summaries/karpathy-llm-wiki-gist.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md"]
type: "Work"
description: "OpenKB wiki schema reference for compiled wiki structure and validation"
---

# wiki-schema.md

`wiki-schema.md` is the OpenKB reference that defines how the compiled wiki tree is structured, validated, linked, and safely interpreted. It describes the schema for wiki pages, the reserved navigation files, the page-type layout, and the operational constraints that keep compiled knowledge separate from mutable source material. Within the OpenKB system, it functions as a schema and policy anchor for both wiki consumption and maintenance.

## What It Defines

The document describes how an OpenKB knowledge base is organized under `wiki/`, including:

- the role of `index.md` as the top-level catalog
- the role of `log.md` as the chronological activity record
- summary, concept, entity, source, exploration, and report directories
- the separation between compiled wiki content and internal `.openkb/` state
- source storage patterns for short Markdown documents and long page-indexed JSON documents
- reserved file handling and navigation expectations inside the wiki tree

These rules make the page central to [[concepts/documentation-architecture]], [[concepts/index-based-discovery]], [[concepts/reserved-wiki-files]], and [[concepts/okf-validation]]. The lifecycle material also ties it to [[concepts/kb-root-staging]], [[concepts/hash-registry-coherence]], [[concepts/source-bundling]], and [[concepts/source-provenance]] because those rules determine how wiki content is staged, ingested, and kept consistent.

## Key Structural Rules

The document specifies that:

- source content lives under `wiki/sources/` in Markdown or paginated JSON form
- summaries describe individual documents
- concepts synthesize themes across documents
- entities accumulate information about named things across documents
- explorations preserve saved query outputs
- reports hold auto-generated lint diagnostics
- wiki pages are compiled artifacts and should be read as data, not treated as executable instruction

These rules position the document as an authority on [[concepts/llm-wiki]], [[concepts/frontmatter-metadata]], [[concepts/generated-content-governance]], [[concepts/wiki-content-as-untrusted-data]], and [[concepts/documentation-layer-separation]]. The OpenKB lifecycle guidance reinforces that role by warning agents to treat compiled pages as read-only knowledge and to prefer front-door discovery through `index.md` and `log.md` before relying on query-driven interpretation.

## Source Format Guidance

A major contribution of the document is its explanation of how OpenKB stores source material:

- short documents use Markdown source files
- long PDFs use page-indexed JSON arrays
- large JSON sources should be sliced page-by-page rather than read in full
- schema details for long-document JSON shape matter when precise page access is needed

This aligns closely with [[concepts/page-indexed-sources]], [[entities/pageindex]], [[concepts/heuristic-classification]], and [[concepts/document-normalization]]. The lifecycle reference adds operational nuance by describing when the KB should be rebuilt, when staged sources should be added deterministically, and when a source pack should be refreshed before recompilation. The repository workflow also relies on source-pack support scripts such as `build_okf_source_pack.py`, `check_prereqs.py`, and `validate_okf_bundle.py`, which depend on the schema's source conventions.

The repository snapshot adds that the tracked file surface is organized around modular agent skill packages, repository governance files, licensing artifacts, and documentation assets. That context reinforces the schema's emphasis on structural regularity, since the compiled wiki must faithfully reflect a repository that contains `.agents/skills/agent-ready-context/`, `.agents/skills/graphify/`, `.agents/skills/openkb/`, `.agents/skills/skill-creator/`, and `.agents/skills/subagent-profile-adapter/` alongside root policy files such as `AGENTS.md`, `README.md`, `LICENSE`, `NOTICE`, `REUSE.toml`, and `THIRD_PARTY_NOTICES.md`. It also strengthens the connection to [[concepts/repository-inventory]], [[concepts/skill-resource-organization]], [[concepts/agent-tooling-ecosystem]], and [[concepts/licensing-and-attribution]].

## Linking And Integrity

The document defines Obsidian-compatible wikilink forms and notes that linting removes broken links during maintenance. It also helps explain how wiki-relative links should resolve within the compiled tree and why stable internal linking matters for agent navigation.

It therefore helps establish expectations around [[concepts/wikilink-integrity]], [[concepts/knowledge-linking-and-citations]], [[concepts/validation-vs-health-reporting]], and [[concepts/graph-integrity-diagnostics]]. The lifecycle guidance reinforces this by treating linked pages as part of a provenance chain: compiled claims should be traceable back through summaries to staged sources and source hashes.

## Operational Role

`wiki-schema.md` is not a user-content page inside the wiki; it is a repository reference file that explains how wiki content should be structured and interpreted. In practice, it functions as a schema reference for maintainers, agents, and tooling that read or generate OpenKB artifacts.

The OpenKB skill summary adds that this reference should be loaded on demand when an agent needs details beyond the basic wiki model, especially for YAML frontmatter fields, long-PDF JSON structure, hash registry layout, image-path conventions, or directory-level schema questions. That makes the document part of the KB's deeper interpretation layer rather than the default first-read path.

The lifecycle reference extends that operational role by defining the maintenance workflow: start with `status` and `list`, read `index.md` and the relevant pages, use `openkb add` only through staged inputs, and prefer `openkb remove` for deletions and orphan cleanup. It also defines the read-only stance for wiki interpretation, the no-hand-edit rule for generated content, and the recommended quality gate of `openkb lint` plus the repository validator. In that sense, `wiki-schema.md` sits inside a broader control surface for [[concepts/read-only-kb-operations]], [[concepts/deterministic-validation]], and [[concepts/quality-gates]].

The repository snapshot places the document inside the `openkb` skill alongside command documentation, within a repository organized around modular skill packages with consistent `SKILL.md`, `references/`, and script-based support patterns. That placement reinforces that the document is part of a broader system of [[concepts/skill-structure-conventions]], [[concepts/skill-based-automation]], and [[concepts/documentation-cohesion]] rather than a standalone specification.

The graphify report adds another layer of context: `OpenKB Wiki Schema` appears as a central node in the repository graph, connected to navigation and validation workflows. That supports its role as a schema anchor for [[concepts/graph-structure-analysis]] and [[concepts/cross-community-bridges]].

The embedded OKF quality baseline extends this role by describing the broader conformance model the wiki schema needs to support. It treats an OKF bundle as a UTF-8 Markdown knowledge tree, identifies `index.md` and `log.md` as reserved at any level, requires parseable YAML frontmatter on every non-reserved Markdown file, and requires a non-empty `type` field on concept documents. It also distinguishes the repository's durable knowledge source of truth from code, explains that `tooling/` is a local OpenKB wiki exception that must be declared in `okf/wiki/AGENTS.md`, and defines how the root `index.md` must enumerate tooling when present.

That baseline also clarifies validation behavior for OpenKB-managed wikis: `--openkb-wiki` skips root `AGENTS.md`, `sources/`, and `reports/`, warns on missing `title` or `description` in places where OpenKB commonly omits them, treats broken `wikilinks` as errors, and applies additional checks for missing machine-managed `sources:` lists and truncation signals. In that sense, `wiki-schema.md` is not just a structural reference but also a practical guide to [[concepts/deterministic-validation]], [[concepts/progressive-disclosure]], [[concepts/tooling-navigation-exceptions]], and [[concepts/quality-gates]].

The lifecycle document adds another important operational layer: it defines the KB root as `okf/`, recommends reading `okf/wiki/index.md` before using `openkb query`, and explains how source staging, recompile order, and registry drift shape the maintenance workflow. It also formalizes the findings loop for discovered knowledge, the correction loop for weak compilation results, and the provenance chain that ties compiled pages back to staged documents and source commits. Those rules make the page especially relevant to [[concepts/agent-ready-repositories]], [[concepts/knowledge-base-discovery]], [[concepts/incremental-compilation]], [[concepts/provenance-tracking]], [[concepts/findings]], and [[concepts/registry-drift]].

It is closely related to [[entities/openkb]] and helps support [[concepts/agent-ready-repositories]], [[concepts/knowledge-base-discovery]], and [[concepts/incremental-compilation]]. It also supports safe KB interpretation by reinforcing [[concepts/read-only-kb-operations]] and the distinction between validated wiki content and operational tooling. The lifecycle reference further connects it to [[concepts/evidence-staging]], [[concepts/source-trust-levels]], [[concepts/generated-artifact-adoption]], and [[concepts/validation-vs-health-reporting]].

## Privacy and Data Flow Guidance

The privacy and data-flows reference extends `wiki-schema.md` into a security and operational policy document. It makes transparency and consent mandatory before any step that sends repository content off the machine, requiring the agent to announce the tool, provider or endpoint, model, credential source, and the content to be transmitted. That policy aligns strongly with [[concepts/consent-first-tooling]] and [[concepts/data-flow-disclosure]].

It also requires explicit provider routing so tools do not silently choose a backend. OpenKB must use explicit litellm configuration, and graphify must receive an explicit `--backend` for non-code sources. This directly reinforces [[concepts/explicit-provider-routing]] and [[concepts/provider-integration]], and it reduces ambiguity in automated runs.

The document further commits the pipeline to a fully local air-gapped path and a zero-LLM fallback. In practice, that means local-only handling should remain available for prerequisite checks, source packing, skeleton generation, validators, code-only graphify runs, and the zero-LLM OpenKB build path. This makes the schema page relevant to [[concepts/air-gapped-operation]], [[concepts/offline-first-workflows]], [[concepts/graceful-degradation]], and [[concepts/llm-free-knowledge-bootstrap]].

A second major addition is the explicit staging rule: all staging must live inside the KB root at `okf/.okf-build/input/`, never outside it. The document explains that staging outside the KB root can leak absolute machine paths into the registry, creating privacy risks and noisy diffs. That strengthens the page's role in [[concepts/kb-root-staging]], [[concepts/path-safety]], [[concepts/source-provenance]], and [[concepts/hash-registry-coherence]].

The telemetry section records the claimed status of the relevant toolchain: graphify has no telemetry or usage tracking, OpenKB has no analytics or update checks, and `uv` has no telemetry. The page treats those claims as version-sensitive and instructs maintainers to re-check them whenever a pin changes, which connects it to [[concepts/telemetry-auditing]], [[concepts/toolchain-pinning]], and [[concepts/version-pinning]].

Finally, the document specifies a disclosure requirement before the first OpenKB LLM-backed command or graphify run over non-code sources. The agent must state the tool, provider, model, endpoint, credential source, and the content being sent, then repeat the disclosure whenever those details change. That requirement ties the page to [[concepts/progressive-disclosure]], [[concepts/minimal-tool-scoping]], and [[concepts/tooling-consent-and-pin-management]].

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__openkb__references__wiki-schema-md]]
- [[summaries/agents__skills__openkb__SKILL-md]]
- [[entities/openkb]]
- [[entities/pageindex]]
- [[summaries/repo-snapshot]]
- [[summaries/graphify-report]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]


See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/karpathy-llm-wiki-gist]]

See also: [[summaries/okf-spec]]