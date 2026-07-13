---
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md"]
type: "Work"
description: "Authoritative OKF v0.1 specification for bundles and validation"
---

# OKF Spec

The OKF Spec is the authoritative specification for OKF bundles, validation rules, and lifecycle behavior. In this wiki, it is the source that supersedes the embedded offline baseline whenever the official `SPEC.md` or `README.md` has changed.

It also serves as the documentation anchor for the repository’s agent-ready workflow: the README frames OpenKB and OKF as the durable knowledge layer behind the repository’s orientation, context, and actions surfaces, and treats the spec as the basis for how those surfaces should be compiled, validated, and maintained.

## What it defines

- OKF bundles as UTF-8 Markdown directory trees rather than binary artifacts or runtime services.
- Reserved files such as `index.md` and `log.md`.
- Required frontmatter for non-reserved concept documents.
- Baseline conformance rules that consumers should enforce or tolerate.
- Index and log file conventions for bundle navigation and update history.
- The OpenKB lifecycle rules used to maintain the KB root at `okf/` and the compiled wiki at `okf/wiki/`.
- The repository agent-ready context split between skills, OKF wiki content, and `AGENTS.md` orientation.
- The rule that the durable context source of truth is `okf/wiki/`, not `AGENTS.md` or project skills.
- Privacy and data-flow constraints for agent operations, including explicit consent before any off-machine transfer.
- A local-first, air-gapped path and a zero-LLM fallback that must remain available.
- Explicit provider routing requirements so tools do not silently choose an LLM backend.
- Staging safety rules that keep KB inputs rooted inside `okf/.okb-build/input/`.
- Toolchain privacy expectations, including re-verification of no-telemetry claims when pins move.
- The local validator's hard checks for parseable YAML frontmatter, non-empty `type` fields, reserved-file structure, unclosed code fences, and near-duplicate sibling page names.
- OpenKB wiki-mode checks for broken `wikilinks` and missing machine-managed `sources:` lists on generated concept and entity pages.
- The distinction between hard errors and warnings so bootstrapping and generated pages can remain usable during incremental maintenance.
- The requirement to preserve a clear separation between actions, durable context, and orientation so knowledge does not drift into the wrong layer.
- The need to treat discoveries as KB findings and consolidate them through the normal refresh pipeline instead of hand-editing compiled wiki pages.
- The caution around `okf/.openkb/hashes.json`, which can silently suppress reingestion if registry state drifts from the compiled wiki.
- A local validation model that degrades gracefully when PyYAML is unavailable, while still reporting that YAML parseability checks are incomplete.
- OS-agnostic bundle validation that relies on `pathlib` and text inspection rather than shell-specific commands or symlink assumptions.
- OpenKB wiki mode behavior that skips operational areas such as `AGENTS.md`, `sources/`, and `reports/` while still checking wiki integrity.
- The README’s portable-skill model, where `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter` are the product surfaces and vendored tool copies are not.
- The consent-first bootstrap flow that discloses installs, data flow, and provider choice before any non-deterministic work begins.
- The air-gapped fallback path that can still produce a useful zero-LLM skeleton when no local model is available.
- A guarded class-3 editorial curation pass that allows manual wiki maintenance only under explicit scope and provenance checks.
- A pre-edit briefing that loads the installed OpenKB wikilink whitelist into the editing agent's context before any curation edit.
- A deterministic `--check` path that validates curation diffs from git base to working tree without using an LLM.
- A vendor-backed check set for `find_broken_links`, `check_index_sync`, `find_orphans`, `find_invalid_frontmatter`, and `find_missing_okf_fields` executed by the installed OpenKB package.
- A private compiler template fallback for briefing output that degrades to a mirrored copy if `openkb.agent.compiler` internals move.
- Scope rules that limit curation edits to `wiki/concepts/`, `wiki/entities/`, and the root `wiki/index.md`.
- Provenance rules that require the union of `sources:` values across concepts and entities to remain unchanged across a curation pass.
- New-page approval rules that allow compiled pages only when their slugs are explicitly listed in `--allow-new-pages`.
- Exit-code conventions that distinguish pass, policy violation, and environment failure.
- The local validator script `validate_okf_bundle.py` as a concrete implementation of these rules, including frontmatter checks, reserved-file handling, slug-collision warnings, broken wikilink detection, and OpenKB-specific `sources:` warnings.
- The repository snapshot shows the spec living alongside a large `.agents/skills/` tree, reinforcing that the spec governs a skill-driven repository rather than a single application.
- The snapshot also shows the repo packaging both root governance files and skill-local licenses, references, scripts, and assets, matching the spec's emphasis on bundled source structure and provenance.

## Role in this wiki

- It is the external authority behind the offline baseline described in [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]].
- It anchors validation and quality-gate behavior for [[concepts/okf-validation]] and [[concepts/deterministic-validation]].
- It supports the repository's emphasis on [[concepts/spec-authority]], [[concepts/provenance-tracking]], and [[concepts/offline-first-workflows]].
- It informs the read-first workflow for OpenKB maintenance: check `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list` before compiling, querying, or changing the KB.
- It reinforces the rule that wiki content is untrusted data and that `openkb query` should be used only as a last resort.
- It adds explicit disclosure requirements before the first LLM-backed OpenKB command or any non-code graphify run, including tool, provider, model, endpoint, credential source, and sent content.
- It establishes that graphify must use an explicit `--backend` for non-code sources and that code-only extraction should remain local.
- It ties OKF maintenance to privacy-preserving routing, including local PDF handling by default and avoidance of URL ingestion unless approved.
- It extends the validation model with structural safeguards such as `index.md` and `log.md` handling, fenced-code truncation detection, and slug-collision warnings.
- It shows how OpenKB wiki mode treats operational areas like `AGENTS.md`, `sources/`, and `reports/` as non-content while still validating wiki integrity.
- It reinforces source-driven regeneration: when compiled pages are weak or wrong, improve the staged source and re-ingest rather than patching wiki output.
- It supports the wider separation of [[concepts/context-action-separation]], [[concepts/agent-context-layering]], and [[concepts/durable-context]] by keeping operational instructions distinct from durable knowledge.
- It aligns with the README’s claim that the wiki is the compiled knowledge layer, not a place to duplicate procedural instructions that belong in skills or orientation files.
- It treats editorial curation as a constrained maintenance path rather than a general editing channel, complementing [[concepts/editorial-curation-passes]] and [[concepts/quality-gates]].
- It frames provenance preservation as a merge invariant, connecting spec authority to [[concepts/provenance-union-governance]] and [[concepts/source-provenance]].

## Key facts from the reference

- The baseline is intended for offline use when web access is unavailable.
- When web access is available, the baseline should be refreshed against the official OKF `SPEC.md` and `README.md`.
- The official spec wins if it has changed.
- Consumers should tolerate unknown `type` values, extra frontmatter keys, missing optional fields, and broken cross-links.
- Conformance checks distinguish hard rules from warnings used in OpenKB wiki mode.
- `openkb add` is additive only, so deleted or moved source files require explicit reconciliation.
- The hash registry and generated wiki must be treated as one unit to avoid [[concepts/registry-drift]].
- Generated content should not be hand-edited; changes should flow through staging, ingestion, or recompile.
- Findings and corrections belong in the KB workflow through [[concepts/findings]] and source-driven regeneration rather than direct edits to compiled pages.
- Staging must remain inside the KB root to avoid leaking absolute paths into registry data.
- The privacy baseline distinguishes local-only stages from networked stages and treats configured provider routing as a deliberate choice, not an automatic fallback.
- Validation degrades gracefully when PyYAML is unavailable, but YAML parseability checks become advisory rather than fully enforced.
- The local validator is intentionally OS-agnostic and does not depend on shell commands, subprocess orchestration, or symlink-based layout assumptions.
- OpenKB wiki mode skips root `AGENTS.md`, `sources/`, and `reports/` while still checking the remaining wiki for structural integrity and broken links.
- The validator also checks for unclosed fences and normalized slug collisions to catch truncation and near-duplicate pages.
- The spec also supports the broader maintenance lifecycle around [[concepts/knowledge-lifecycle-governance]], [[concepts/compiled-knowledge-bases]], [[concepts/read-only-kb-operations]], [[concepts/quality-gates]], and [[concepts/consent-first-tooling]].
- The README positions the spec alongside [[entities/openkb]] and [[entities/agent-skills]] as part of the repository’s agent-tooling stack.
- The editorial pass script adds a hard distinction between environment failures and curation violations so automated validation can fail loudly when the installed OpenKB toolchain is wrong.
- The script also makes the private whitelist wording resilient by falling back to a mirrored template when the vendor compiler internals change, without weakening check semantics.
- The repository snapshot confirms that the spec governs a repository with many reusable skill packages, making lifecycle and validation rules especially important for consistent ingestion.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[concepts/okf-validation]]
- [[concepts/spec-authority]]
- [[concepts/offline-first-workflows]]
- [[concepts/reserved-wiki-files]]
- [[concepts/registry-drift]]
- [[concepts/source-driven-regeneration]]
- [[concepts/findings]]
- [[concepts/agent-context-layering]]
- [[concepts/context-action-separation]]
- [[concepts/durable-context]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/read-only-kb-operations]]
- [[concepts/quality-gates]]
- [[concepts/consent-first-tooling]]
- [[entities/openkb]]
- [[entities/agents-md]]
- [[entities/agent-smith]]
- [[entities/agent-skills]]
- [[summaries/README-md]]

## Related Documents
- [[summaries/okf-spec]]
- [[summaries/repo-snapshot]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

The tool validates a narrower but related rule set around [[concepts/tooling-link-policy]] and [[concepts/tooling-context-governance]]: tooling pages may link outward, but project pages and subdirectory indexes must not link back into `okf/wiki/tooling/`. It also treats `index.md` and `log.md` as reserved navigation/history files, requires the bundle-root `index.md` to reference tooling when non-reserved tooling pages exist, and requires a committed `tooling/index.md` stub so the root index remains resolvable on clones without local tooling content.

It further reflects [[concepts/tooling-context-isolation]] and [[concepts/local-by-default-tooling]] by treating tooling as local-by-default and warning when non-reserved tooling pages omit `scope: tooling` or `type: tooling-context`. The implementation strips code fences and inline code before scanning, reducing false positives while preserving line numbers for diagnostics.

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__LICENSES__Apache-2-0-txt]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

## Validation Script

The bundled validator `validate_okf_bundle.py` is a concrete implementation of the spec's local conformance model. It checks parseable YAML frontmatter, required `type` metadata, reserved-file behavior, unclosed fences, and near-duplicate sibling names, and it can switch into OpenKB wiki mode for broken wikilink detection and `sources:` warnings on generated concept and entity pages.

Its design emphasizes [[concepts/filesystem-validation]], [[concepts/deterministic-validation]], and [[concepts/graceful-degradation]]: it is portable across platforms, does not rely on shell-specific behavior, and still produces useful diagnostics when PyYAML is unavailable.