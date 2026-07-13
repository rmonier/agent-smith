---
sources: ["summaries/okf-spec.md", "summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "OpenKB's command-line interface for knowledge-base compilation and validation"
---

# OpenKB CLI

OpenKB CLI is the command-line interface for the [[entities/openkb]] workflow used to inspect, configure, ingest, validate, regenerate, and reconcile a knowledge base.

In the `agent-smith` repository README, it appears as part of the broader agent-ready transformation stack: OpenKB is the semantic knowledge compiler that powers durable context in `okf/wiki/`, while the surrounding skills and scripts keep the repository aligned with [[concepts/compiled-knowledge-bases]], [[concepts/progressive-disclosure]], and [[concepts/agent-ready-repositories]]. It is also framed as a toolchain component that supports incremental, consent-first repository knowledge compilation and air-gapped operation when a local provider is available.

The graphify structural report shows OpenKB CLI as a major connective layer in the repository's knowledge-compilation ecosystem. Its related scripts and workflow nodes sit near core hubs such as `build_okf_source_pack.py`, `validate_okf_bundle.py`, `build_okf_skeleton.py`, `main()`, `detect_orphans()`, and `names_from_git()`, and it bridges communities around workflow automation, validation, adapter generation, and graph tooling. The report also places it alongside [[concepts/openkb-build-workflow]], [[concepts/tooling-context-governance]], [[concepts/agents-md-maintenance]], and openkb wiki governance, while noting a large set of isolated nodes that likely need stronger cross-linking or more explicit documentation.

## What it does

- Runs prerequisite and readiness checks before heavier operations, including repo, Git, Python, and toolchain validation.
- Uses a preflight script (`check_prereqs.py`) to report required, optional, vendored, and writable-path checks in a single diagnostics payload.
- Prefers `uv` for isolated execution but can fall back to bare `python3` in degraded mode.
- Reads `okf/wiki/index.md` first when present, then follows its routing to determine which wiki and tooling pages to load next.
- Supports staged source-pack ingestion into `okf/.okf-build/input/` before any OpenKB mutation.
- Adds staged source material to the KB with commands like `openkb --kb-dir ./okf add <file>`.
- Supports LLM-backed commands for recompilation, linting, querying, chatting, skill generation, and deck workflows.
- Uses `okf/.openkb/config.yaml` for local model and provider settings, while keeping committed example config separate from user-specific choices.
- Requires explicit provider disclosure before the first LLM-backed command and treats external URLs as evidence, not instructions.
- Provides the pinned OpenKB tooling that the editorial curation pass relies on for deterministic checks and whitelist rendering.
- Validates OKF bundles and OpenKB wikis with a local conformance script that checks frontmatter, reserved files, code fences, slug collisions, and, in wiki mode, broken wikilinks.
- Serves as the CLI layer for the [[concepts/agent-ready-context]] workflow that keeps `okf/wiki/` as the durable repository context surface.
- Supports the broader repository agent-ready pipeline, including source-pack staging, orphan pruning, and bundle validation.
- Enforces the tooling boundary in the wiki workflow by keeping harness/runtime knowledge in local tooling pages only when the tooling-context policy allows it.
- Supports the tooling-context workflow that records harness build notes under `okf/wiki/tooling/` without letting those pages become project truth.
- Relies on the committed `okf/wiki/tooling/index.md` stub and root index entry when local tooling pages exist, so the tooling overlay stays navigable across clones.
- Adapts to the active harness as a runtime-specific projection rather than defining a portable subagent standard.
- Writes native adapter files only after checking real harness documentation and confirming whether the active environment supports local subagents or profiles.
- Keeps generated profile files short and bounded, with pointers back to `AGENTS.md`, `okf/wiki/`, and relevant skills instead of embedding large project context.
- Requires a tracking decision for generated harness-specific files, with local-only as the default unless the user chooses shared or ignored tracking.
- In the README's framing, it is one of the pinned toolchain components that help make a repository agent-ready, alongside `graphify` and the OpenKB-associated pipeline pieces.
- Its role is intentionally distinct from the three distributable product skills described in the README: OpenKB CLI belongs to the compiled knowledge and validation layer, not the portable skill surface itself.
- The repository snapshot reinforces that OpenKB CLI sits inside a larger skill ecosystem, alongside agent-ready context, graphify, skill-creator, and subagent-profile-adapter materials.
- The tracked file inventory also shows that OpenKB CLI is supported by repository-level configuration such as `.gitattributes`, `.gitignore`, and `.graphifyignore`, which shape ingestion and validation behavior.
- The graphify structural report identifies OpenKB CLI-related scripts as major hubs in the repository graph, especially `build_okf_source_pack.py`, `validate_okf_bundle.py`, `build_okf_skeleton.py`, `main()`, `detect_orphans()`, and `names_from_git()`.
- The report also places OpenKB CLI near the center of the repository's documentation architecture, alongside `OpenKB lifecycle for OKF maintenance`, `OpenKB repo build workflow`, `Tooling context policy`, `AGENTS.md`, and `OpenKB Wiki Schema`.
- Graph analysis shows the CLI's ecosystem is split across communities for workflow automation, validation, adapter generation, and graph tooling, indicating that OpenKB CLI serves as a connective layer across several documentation clusters.
- The report highlights a large number of isolated nodes, suggesting that some OpenKB CLI-adjacent components may need stronger cross-linking or more explicit documentation.
- OpenKB CLI is the operational surface for the KB lifecycle rules described in [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], including deterministic staging, registry-drift recovery, reconciliation, and guarded curation.
- The workflow reference adds that Graphify should run before source-pack creation when installed, that the source pack is deterministic across commits, and that deletions must be reconciled before ingesting refreshed input.
- It also requires lint reports to be preserved and triaged, and it treats the wiki as out of bounds for the repo graph to avoid self-reference loops and non-deterministic rebuilds.
- A dedicated orphan-retraction script extends that lifecycle by removing KB documents whose repository source no longer exists, using `openkb remove` as the deterministic inverse of ingestion.
- That script treats manifest-backed reconciliation as authoritative when available, falls back to git-derived staging names when needed, and flags mismatches as advisories to detect stale packs or selection-rule drift.
- It distinguishes deleted, renamed, and deselected documents, and it applies a safety guard when the orphan set is unexpectedly large so accidental mass retraction is less likely.
- It also prefers raw staged `source_path` metadata over slug reversal when mapping registry entries back to repository files, because slugging can be lossy for paths containing `__`.

## Key facts from the source

- The preflight script checks Python 3.11+, Git, `uv`, worktree status, optional `graphify` and `openkb` binaries, vendored tool skills, OpenKB config drift, credential-home ambiguity, and writable repository paths.
- OpenKB CLI and the check script are designed to fail hard only on true prerequisites; optional tools and companion skills are reported separately.
- The script treats `okf/.openkb/config.yaml` as user-specific and compares only shared keys such as `language`, `pageindex_threshold`, and `entity_types` against `config.yaml.example`.
- If both `okf/.env` and `~/.config/openkb/.env` exist, the project file is reported as the one that wins for shared keys.
- The preflight output is structured as `required`, `optional`, `vendored_tool_skills`, `openkb_config`, `companion_skills`, `writable_paths`, and `notes`.
- The script uses `shutil.which` plus a resolved executable path so Windows command shims can be launched reliably.
- `graphify` and `openkb` are given long startup timeouts because first invocation may be slow.
- The check script is intentionally dependency-free so it can run in a fresh repository without relying on the target environment.
- The installed OpenKB package exposes the public lint API used by the editorial pass, including `list_existing_wiki_targets`, `find_broken_links`, `find_orphans`, `check_index_sync`, `find_invalid_frontmatter`, and `find_missing_okf_fields`.
- Private compiler internals such as `_KNOWN_TARGETS_USER` and `_format_known_targets` are used only for briefing text and can fall back to a mirrored copy if the installed version changes.
- The editorial pass enforces curation-only edits, provenance preservation across concepts and entities, and a no-unapproved-new-pages rule for compiled wiki pages.
- The pass also treats `reports/` orphans as a documented false positive and filters them out during checks.
- The OKF bundle validator follows the local OKF v0.1 conformance rules: every non-reserved Markdown file is treated as a concept document, concept frontmatter must be parseable and include a non-empty `type`, and reserved `index.md` and `log.md` files follow their own structure rules.
- In OpenKB wiki mode, the validator skips root `AGENTS.md`, `sources/`, and `reports/`, warns on missing `sources:` lists for `concepts/` and `entities/` pages, and escalates broken wikilinks to errors.
- The validator also emits warnings for unclosed code fences and sibling page names that collapse to the same normalized slug.
- If PyYAML is unavailable, YAML frontmatter validation degrades with an explicit warning rather than failing silently.
- The agent-ready-context skill treats OpenKB as part of the repository's durable context pipeline, not as a parallel wiki or a place for generated files to be written directly.
- OpenKB operations are expected to respect staged input, deterministic validation, and the correction loop instead of patching compiled wiki pages by hand.
- Tooling pages remain local by default and must not be enumerated in committed indexes, except for the committed navigation stub and root tooling entry required by the policy.
- Non-reserved local tooling pages need at least one outgoing wikilink to durable project knowledge so they do not become intentional orphans in OpenKB.
- Runtime detection should prioritize explicit harness signals, process and environment hints, and local or official docs before asking the user to resolve ambiguity.
- The harness adapter workflow distinguishes between the current runtime and merely installed tools, and it avoids using `--version` checks as proof of the active environment.
- The tooling context policy says to keep project concepts from linking back into tooling pages, while still allowing tooling pages to point outward to project knowledge.
- The README adds a broader operational claim: OpenKB is meant to support incremental, consent-first repository knowledge compilation, including air-gapped operation when a local provider is available.
- The README also treats OpenKB as part of a source-driven regeneration loop, where the KB is rebuilt from staged inputs and validated rather than edited as an ad hoc artifact.
- The repository snapshot adds an inventory-level fact: OpenKB CLI is surrounded by dedicated reference, script, and asset files, indicating that it is maintained as a structured tool rather than a single executable.
- The lifecycle reference also frames OpenKB CLI around read-first inspection, staged ingestion, deterministic removal, and registry-aware recovery when wiki pages and hash records drift out of sync.
- It distinguishes query-heavy and graph-heavy tasks: meaning questions should go through the wiki and `openkb query` last, while structure questions belong to local graph analysis tools.
- It treats `openkb lint` as a non-gating health report and the repository validator as the actual structural pass/fail gate.
- It establishes a clear boundary between repository truth, discovered findings, and output-only curation, each with a different maintenance path.
- The workflow reference further requires `.gitattributes` normalization, `.graphifyignore` self-reference exclusion, and Git-backed history for deterministic source-pack creation.
- It also notes that missing Graphify or OpenKB can be handled through consent-first bootstrap paths, but degraded operation should be reported clearly.
- The orphan-retraction script adds a deterministic cleanup path for deleted repository sources, preserving the KB's coherence without manual registry edits.
- Its manifest-first behavior reduces drift between the builder and the retraction script, while the git fallback preserves usability in a fresh clone or manifest-less environment.
- Its rename detection prevents unnecessary downstream page loss when the same source content reappears under a new path.
- Its mass-orphan safety guard is a practical safeguard against misconfiguration, especially when bundle depth or repository selection is wrong.
- The privacy-and-data-flows reference adds that OpenKB CLI must preserve user transparency and consent before any LLM-backed operation, explicitly disclose provider/model/endpoint/credential source, and keep a fully local or zero-LLM path available.
- It also clarifies that OpenKB's telemetry surface is minimal: no analytics, no telemetry, and no update checks, with remaining egress limited to configured providers, optional PageIndex Cloud, user-approved URL ingestion, and browser feedback.
- The same reference emphasizes that KB staging must live inside the KB root to avoid absolute-path leakage in `.openkb/hashes.json`, and it warns that local ignore mechanisms outside `.gitignore` and `.graphifyignore` do not protect graphify scans.
- For air-gapped operation, OpenKB CLI can be paired with a local `ollama` model, unset API keys, skipped URL ingestion, and local external docs under `okf/.okf-build/input/external/`.
- A zero-LLM fallback remains available through `build_okf_skeleton.py`, which can generate a conservative bundle that is later reconciled through OpenKB validation and recompilation.

## Related concepts

- [[concepts/explicit-provider-routing]] for selecting the correct provider and model explicitly.
- [[concepts/configuration-precedence]] for environment and file-based configuration order.
- [[concepts/privacy-preserving-tooling]] for avoiding exposure of secret values.
- [[concepts/preflight-checks]] for status and readiness verification before heavier actions.
- [[concepts/deterministic-validation]] for repeatable checks on the configured KB.
- [[concepts/local-vs-shared-configuration]] for separating user-specific settings from project-shared ones.
- [[concepts/consent-first-tooling]] for disclosure before sending content to a provider.
- [[concepts/editorial-curation-passes]] for the guarded hand-edit workflow used on compiled wiki content.
- [[concepts/provenance-union-governance]] for preserving the union of `sources:` values across merges.
- [[concepts/openkb-wiki-health-checks]] for the vendor lint and structural checks used by the CLI.
- [[concepts/okf-bundle-validation]] for validating OKF bundles against local conformance rules.
- [[concepts/openkb-wiki-validation-modes]] for the operational differences between bundle mode and wiki mode.
- [[concepts/openkb-wikilink-resolution]] for the target matching rules used when checking wiki links.
- [[concepts/reserved-markdown-file-rules]] for the special handling of `index.md` and `log.md`.
- [[concepts/quality-gates]] for gating edits on structural and link-integrity checks.
- [[concepts/agent-ready-context]] for the broader repository-ready workflow this CLI supports.
- [[concepts/source-pack-staging]] for preparing deterministic input before ingestion.
- [[concepts/orphan-retraction]] for removing compiled pages whose sources were deleted.
- [[concepts/okf-wiki-governance]] for the rules around compiled wiki maintenance.
- [[concepts/tooling-context-governance]] for the policy that constrains harness and runtime notes.
- [[concepts/tooling-context-isolation]] for keeping user-scoped tooling separate from project knowledge.
- [[concepts/tooling-navigation-exception]] for the committed stub and root-index entry that make local tooling discoverable.
- [[concepts/tooling-link-policy]] for the allowed direction of links between tooling pages and project pages.
- [[concepts/local-by-default-tooling]] for the local overlay model used by tooling pages.
- [[concepts/runtime-adapter-management]] for generating harness-specific subagent or profile adapters.
- [[concepts/adaptive-harness-detection]] for detecting the active runtime from signals rather than installed binaries.
- [[concepts/subagent-role-design]] for choosing task-scoped adapter roles.
- [[concepts/permission-scoped-agents]] for keeping generated adapters bounded to the minimum needed capabilities.
- [[concepts/air-gapped-operation]] for the README's local-only mode when no repository content should leave the machine.
- [[concepts/source-driven-regeneration]] for rebuilding the KB from staged sources instead of hand-editing outputs.
- [[concepts/durable-context]] for the README's emphasis on retaining repository knowledge across sessions.
- [[concepts/repository-inventory]] for the tracked-file snapshot that reveals how OpenKB CLI fits into the repo's structure.
- [[concepts/repository-structure-overview]] for the broader file-layout pattern shown by the inventory.
- [[concepts/agent-tooling-ecosystem]] for the surrounding skill and tooling set that supports OpenKB CLI.
- [[concepts/graph-structure-analysis]] for the community and centrality findings in the graphify report.
- [[concepts/documentation-gaps]] for the many isolated nodes and thin communities the report surfaces.
- [[concepts/cross-community-bridges]] for the high-betweenness nodes that connect workflow clusters.
- [[concepts/registry-drift]] for the mismatch risk between hash records and compiled wiki pages.
- [[concepts/rename-vs-delete-detection]] for separating true deletions from path moves when pruning orphans.
- [[concepts/findings]] for the capture-and-promote loop used for discovered repository knowledge.
- [[concepts/findings-promotion]] for moving a captured finding into compiled truth.
- [[concepts/knowledge-lifecycle-governance]] for the broader policy that separates source correction, knowledge capture, and curation.
- [[concepts/manifest-authoritative-reconciliation]] for using a built manifest as the primary source of truth during reconciliation.
- [[concepts/hash-registry-coherence]] for keeping registry entries aligned with staged and compiled documents.
- [[concepts/data-flow-disclosure]] for the required pre-run disclosure of tool, provider, model, endpoint, credential source, and content scope.
- [[concepts/local-artifact-leakage]] for the risk of local files entering committed graph artifacts rather than leaving to a provider.
- [[concepts/kb-root-staging]] for the rule that staged KB inputs must stay inside the KB root.
- [[concepts/telemetry-auditing]] for re-checking no-telemetry claims when toolchain pins move.

## Source

- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/README-md]]
- [[summaries/repo-snapshot]]
- [[summaries/graphify-report]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__LICENSES__Apache-2-0-txt]]

See also: [[summaries/agents__skills__agent-ready-context__LICENSING-md]]


See also: [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]


See also: [[summaries/agent-skills-spec]]

See also: [[summaries/okf-spec]]