---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/okf-spec.md", "summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md"]
type: "Work"
description: "Validator script for OKF bundles and OpenKB wiki conformance checks"
---

# validate_okf_bundle.py

`validate_okf_bundle.py` is a repository script for validating an OKF bundle or OpenKB wiki tree against local conformance rules. In the workflow documented in [[summaries/agents__skills__agent-ready-context__references__workflow-md]], it is used as a deterministic post-build gate after ingestion, compilation, and editorial checks.

## What It Does

- Validates Markdown files in an OKF bundle and treats non-reserved pages as concept documents.
- Checks YAML frontmatter parseability and requires a non-empty `type` field on concept pages.
- Applies special rules to reserved `index.md` and `log.md` files.
- Warns about unclosed code fences and sibling page names that normalize to the same slug.
- Supports `--openkb-wiki` to apply OpenKB-specific checks for operational directories and wikilink integrity.
- Uses `--strict-warnings` to promote warnings to errors when a tighter gate is needed.
- Implements the official OKF v0.1 conformance rule that every non-reserved `.md` file must have parseable YAML frontmatter with a non-empty `type` field.
- Fits the broader agent-ready pipeline that stages deterministic input, ingests it into OpenKB, and then validates the generated wiki.
- Complements the agent-ready workflow's emphasis on [[concepts/deterministic-validation]], [[concepts/executable-validation]], and [[concepts/okf-bundle-validation]].
- Helps enforce the separation between local validation and any content that may have been routed through explicit LLM-backed tooling.

## Role In The Workflow

The workflow treats this script as a required verification step after earlier content and lint passes:

- It runs after source compilation and editorial curation checks.
- It validates the compiled bundle before the build is considered complete.
- It supports the broader [[concepts/okf-bundle-validation]] and [[concepts/deterministic-validation]] practices.
- It fits the editorial loop where `editorial_pass.py --check` is followed by `validate_okf_bundle.py --openkb-wiki` and then the final verification lint.
- It is part of the repository's agent-ready context surface, alongside `AGENTS.md`, the OpenKB wiki, and the source-pack staging pipeline.
- It sits downstream of the OKF bundle structure rules that allow optional `index.md` and `log.md` files at any directory level.
- It is also one of the local gates that should run after any privacy-sensitive routing decisions have already been disclosed under [[concepts/data-flow-disclosure]] and [[concepts/explicit-provider-routing]].

## Related Pages

- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[entities/okf-wiki]]
- [[entities/openkb]]
- [[entities/agents-skills]]
- [[concepts/okf-bundle-validation]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/wikilink-integrity]]
- [[concepts/executable-validation]]
- [[concepts/editorial-curation-passes]]
- [[concepts/deterministic-validation]]
- [[concepts/agent-ready-context]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/data-flow-disclosure]]
- [[concepts/explicit-provider-routing]]
- [[concepts/privacy-preserving-tooling]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

## Related Source Pack Staging

`build_okf_source_pack.py` is a companion repository script that prepares deterministic staged input for OpenKB ingestion from a Git repository. It does not validate the compiled wiki directly; instead, it assembles the source pack that later feeds the build and validation workflow.

- Builds `okf/.okf-build/input` from tracked repository files.
- Normalizes content and hashes source text so staged output is reproducible.
- Emits a manifest for staged items, supporting [[concepts/source-pack-manifest]] and [[concepts/staging-manifests]] style reconciliation.
- Can stage a repository snapshot and an optional graph report, while guarding against [[concepts/self-referential-ingestion-loops]].
- Splits oversized markdown or code sources instead of cropping them, preserving full content for [[concepts/source-partitioning]].
- Supports directory-based bundling for non-markdown sources to reduce staging sprawl.

The graph report reinforces that this script sits in a dense validation and build cluster: `build_okf_source_pack.py` is one of the community hubs, and `validate_okf_bundle.py` is another major hub in the graph. The report also highlights a surprising bridge from `main()` to `bundle_key()` across the source-pack and pruning scripts, which suggests the validation path is tied to broader build and skill-packaging logic.

## Why It Matters

- It provides a deterministic, OS-agnostic validation gate that relies on `pathlib`, `tempfile`, and subprocess-friendly behavior rather than shell-specific assumptions.
- It validates frontmatter structure even when PyYAML is missing, but degrades with an explicit warning so local environments stay honest about what was checked.
- It records provenance and structure concerns through warnings for duplicate slugs, truncated fences, and missing metadata.
- It separates repository validation from content staging: this script checks the compiled bundle, while source-pack scripts prepare the staged inputs.
- It helps preserve bundle health in OpenKB wiki mode by checking broken wikilinks and missing `sources:` lists on generated concept and entity pages.
- It acts as a local health check within the larger okf wiki health checks and [[concepts/validation-vs-health-reporting]] pattern.
- It belongs to the broader agent-ready context workflow that treats durable wiki content as the repository's source of truth and keeps generated artifacts out of hand-edited paths.
- It aligns with the OKF spec's permissive consumption model: consumers should tolerate missing optional fields, unknown types, and broken links even when validation is strict about the required `type` field.
- The graph report shows that validation tooling is central to the corpus structure, with `validate_okf_bundle.py` forming its own strong community and linking into larger governance areas such as [[concepts/okf-validation]] and [[concepts/documentation-cohesion]].

## Related Pages

- [[entities/build_okf_source_pack-py]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/source-pack-staging]]
- [[concepts/source-bundling]]
- [[concepts/document-normalization]]
- [[concepts/line-ending-normalization]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/source-provenance]]
- [[concepts/provenance-union-governance]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/deterministic-okf-staging]]
- [[concepts/managed-document-sections]]
- [[concepts/reserved-navigation-files]]
- [[concepts/reserved-markdown-file-rules]]
- [[concepts/frontmatter-validation]]
- [[concepts/lightweight-frontmatter-validation]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/graphify-report]]
- [[summaries/okf-spec]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

## Validation Rules

`validate_okf_bundle.py` encodes a mix of formal OKF checks and practical OpenKB health checks.

- It requires a non-reserved Markdown file to contain parseable YAML frontmatter.
- It requires concept frontmatter to contain a non-empty `type` field.
- It allows the root `index.md` to carry an `okf_version` field, while warning about extra keys.
- It treats `log.md` as a reserved file with a specific heading format.
- It warns about empty bodies, missing `title` or `description`, and unclosed fences.
- In OpenKB mode, it skips `AGENTS.md`, `sources/`, and `reports/` and turns broken wikilinks into errors.
- In OpenKB mode, it warns when `concepts/` or `entities/` pages are missing the machine-managed `sources:` list.
- It supports the workflow's split between deterministic validation and broader wiki-health reporting.
- It reinforces [[concepts/quality-gates]] and [[concepts/okf-validation-rules]] as distinct from broader editorial review.
- It directly embodies the OKF v0.1 conformance requirement that every non-reserved `.md` file must have parseable YAML frontmatter with a non-empty `type` field.
- It also codifies the privacy-relevant boundary that validation should be able to run locally, even when upstream ingestion or extraction workflows may have required explicit consent and explicit backend selection.
- The graph report's omission of thin communities and the large isolated-node count also underscore why this validator matters: it is one of the few nodes that concentrates structure, health checks, and link integrity in a single deterministic pass.

## Agent Skills Specification Context

This validator now has a clearer connection to the official Agent Skills format specification summarized in [[summaries/agent-skills-spec]]. The spec defines the skill directory layout that `validate_okf_bundle.py` helps enforce indirectly when validating skills compiled into an OKF bundle.

- Agent Skills are directory-based packages that must contain a `SKILL.md` file at minimum.
- `SKILL.md` uses YAML frontmatter plus Markdown body content.
- Required frontmatter fields include `name` and `description`; optional fields include `license`, `compatibility`, `metadata`, and `allowed-tools`.
- The `name` field must be lowercase, hyphenated, unique to the directory, and match the parent folder name.
- The body is freeform, but the spec recommends step-by-step instructions, examples, and edge cases.
- Supporting `scripts/`, `references/`, and `assets/` directories are optional and intended for progressive disclosure.
- The spec recommends keeping `SKILL.md` under 500 lines and validating skills with `skills-ref validate ./my-skill`.

In practice, that makes this script relevant not only to compiled wiki bundles but also to skill-authoring workflows that depend on [[concepts/skill-frontmatter-schema]], [[concepts/skill-progressive-disclosure]], [[concepts/skill-structure-conventions]], and [[concepts/skill-validation-workflow]].

## Orphan Retraction Role

`prune_okf_orphans.py` extends the same deterministic workflow by reconciling the OpenKB registry with the repository after source deletion or renaming. It is the inverse of source-pack ingestion: instead of adding new material, it retracts orphaned KB documents that no longer map to tracked repository sources.

- Uses the freshly built source-pack manifest when available so orphan detection stays aligned with the builder.
- Falls back to git-derived expected names when the manifest is absent.
- Classifies stale entries as `deleted`, `renamed`, or `deselected` so the operator can distinguish removal from a selection-policy change.
- Calls `openkb remove` directly, with `--dry-run` preview support and `--keep-empty` for rename cases where shared pages should remain.
- Protects against accidental mass retractions with a safety guard that detects mismatched bundle depth or wrong-repo invocations.

This makes bundle validation part of a broader lifecycle: source-pack staging creates deterministic input, `validate_okf_bundle.py` verifies the compiled wiki, and `prune_okf_orphans.py` removes stale registry state when the source repo changes.

## Related Pages

- [[entities/prune_okf_orphans-py]]
- [[entities/openkb-remove]]
- [[concepts/orphan-retraction]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/hash-registry-coherence]]
- [[concepts/safe-automation]]
- [[concepts/read-only-kb-operations]]
- [[concepts/registry-drift]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/deterministic-validation]]
- [[concepts/deterministic-source-pack-staging]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/README-md]]

## Privacy And Routing Context

`validate_okf_bundle.py` itself is a local validator, but it sits downstream of workflows that may have sent content to an LLM provider or a local backend.

- It should run after any disclosure step required for `openkb` commands that use a configured litellm provider.
- It should not be treated as a substitute for the transparency rules in [[concepts/data-flow-disclosure]].
- It benefits from explicit backend selection in upstream extraction workflows, especially when graphify processes non-code sources.
- It fits the broader distinction between local validation, local-only artifacts, and content that may already have crossed a provider boundary.
- It is part of the governance stack that keeps the KB aligned with [[concepts/air-gapped-operation]], [[concepts/explicit-provider-routing]], and [[concepts/privacy-preserving-tooling]].