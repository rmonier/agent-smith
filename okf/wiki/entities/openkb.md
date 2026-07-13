---
sources: ["summaries/okf-spec.md", "summaries/karpathy-llm-wiki-gist.md", "summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__agent-ready-context__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/repo-snapshot.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__transcribe-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml.md", "summaries/agents__skills__agent-ready-context__assets__gitattributes-template.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md"]
type: "Product"
description: "OpenKB is the local-first KB product that compiles durable wiki context."
---

# OpenKB

OpenKB is the knowledge-base product used in this repository workflow to compile durable context into `okf/wiki/`. In the agent-ready-context skill, it is treated as the source of truth for long-lived repository knowledge, provenance, and cross-agent memory.

## Role in the Workflow

OpenKB sits between staged repository evidence and the compiled wiki:

- repository and external source material is staged first
- OpenKB ingests that staged input
- compiled pages are written under `okf/wiki/`
- validation and review happen after generation

This makes OpenKB part of the repository's [[concepts/knowledge-compilation-pipeline]] and [[concepts/durable-context]] strategy.

The privacy and data-flow rules add an important constraint to that workflow: OpenKB must disclose any LLM-backed command before it sends staged content off the machine, and it must keep a fully local path available. The document also defines `okf/.okf-build/input/` as the required staging area inside the KB root, so that ingested paths remain KB-relative and do not leak absolute machine paths into the registry. That connects OpenKB directly to [[concepts/data-flow-disclosure]], [[concepts/provider-routing]], [[concepts/air-gapped-operation]], [[concepts/kb-root-staging]], and [[concepts/privacy-preserving-tooling]].

The graphify structural report reinforces OpenKB's role by showing it as part of a large, connected documentation system. It highlights communities around build workflow, OKF maintenance, wiki schema, tooling boundaries, and skill authoring, which suggests OpenKB is not just a target output but a central coordination point across [[concepts/graph-structure-analysis]], [[concepts/knowledge-graph-analysis]], and [[concepts/cross-community-bridges]].

## Key Facts From the Skill

- The skill treats `okf/wiki/` as the durable context source of truth.
- OpenKB owns the KB root `okf/`, including `okf/raw/`, `okf/wiki/`, `okf/.openkb/`, and `okf/output/`.
- Generated files should not be written directly into `okf/raw/` or `okf/wiki/`.
- Deterministic input is staged under `okf/.okf-build/input/` and then ingested.
- `openkb lint` is used as the main health check after ingestion.
- The workflow includes a correction loop: if generated pages are weak or wrong, improve the source and re-ingest instead of hand-editing compiled wiki pages.
- OpenKB is also presented as a broader knowledge-base product whose workflow emphasizes staged input, compiled output, and post-generation validation.
- The graphify report shows a corpus of 63 files, 472 nodes, 550 edges, and 54 communities, confirming that OpenKB operates in a documentation space large enough to benefit from graph-based navigation.
- The report identifies `OpenKB lifecycle for OKF maintenance`, `OpenKB repo build workflow`, and `OpenKB Wiki Schema` as important hubs, suggesting OpenKB is tightly coupled to [[concepts/wiki-lifecycle-governance]], [[concepts/openkb-build-workflow]], and [[concepts/repository-structure-overview]].
- Several graph hubs such as `README.md`, `AGENTS.md`, `build_okf_source_pack.py`, and `validate_okf_bundle.py` indicate that OpenKB depends on explicit build and validation tooling, not informal manual curation.
- The privacy-and-data-flows document adds that OpenKB commands such as `add`, `recompile`, `lint`, `query`, `chat`, `skill`, and `deck` may route staged content through the configured litellm provider, so backend selection and consent are operational requirements.
- For long PDFs, OpenKB uses local PageIndex by default and only reaches PageIndex Cloud when `PAGEINDEX_API_KEY` is set.
- `openkb add <url>` is a deliberate networked ingestion path and should only be used with user approval.
- OpenKB's telemetry status is documented as clean: no analytics, telemetry, or update checks, with tracing disabled at startup.

## Operational Boundaries

The skill describes several important controls around OpenKB use:

- use `uv` for running bundled scripts
- initialize OpenKB with explicit model and language settings when needed
- treat web-fetched material as untrusted evidence
- keep local OpenKB state and generated artifacts out of version control
- avoid broad or destructive commands without consent

The privacy document sharpens those boundaries:

- announce tool, provider or endpoint, model, credential source, and outgoing content before any LLM-backed step
- never let tools silently auto-select a backend
- keep a fully local air-gapped path and zero-LLM fallback available
- leave `PAGEINDEX_API_KEY` unset when local-only PDF handling is desired
- avoid `openkb add <url>` unless the URL fetch is explicitly approved
- keep cost and cache artifacts gitignored so they do not leak environment details

These rules support [[concepts/consent-first-workflows]], [[concepts/deterministic-validation]], [[concepts/local-only-repo-artifacts]], [[concepts/explicit-provider-routing]], [[concepts/page-indexed-sources]], and [[concepts/local-by-default-tooling]]. The Agent Skills specification also adds a closely related constraint model for skills themselves: `SKILL.md` is the required entry file, frontmatter must declare a valid lowercase hyphenated `name` and a non-empty `description`, optional `allowed-tools` can scope execution, and supporting files should be organized under `scripts/`, `references/`, and `assets/` to keep the main skill body compact. That aligns with [[concepts/skill-frontmatter-schema]], [[concepts/skill-progressive-disclosure]], [[concepts/skill-resource-organization]], and [[concepts/skill-validation-workflow]].

The graphify report adds a maintenance-oriented perspective here too: `main()` is a high-centrality bridge node, `bundle_key()` unexpectedly connects build and skill-creator flows, and there are 234 isolated nodes plus 9 omitted thin communities. That reinforces the need for [[concepts/documentation-gaps]] and [[concepts/documentation-cohesion]] work around OpenKB's surrounding ecosystem.

## Related Pages

- [[concepts/compiled-knowledge-bases]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/okf-validation]]
- [[concepts/repository-ingestion]]
- [[concepts/source-pack-staging]]
- [[concepts/deterministic-okf-staging]]
- [[concepts/graph-structure-analysis]]
- [[concepts/documentation-gaps]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agent-skills-spec]]
- [[entities/openkb-wiki]]

See also: [[summaries/karpathy-llm-wiki-gist]]

See also: [[summaries/okf-spec]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/graphify-report]]