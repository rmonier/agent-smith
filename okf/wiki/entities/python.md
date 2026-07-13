---
sources: ["summaries/agent-skills-spec.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Product"
description: "Runtime and scripting language used across the OpenKB toolchain."
---

# Python

Python is the runtime and scripting layer used by the OpenKB build, validation, skill tooling, and runtime-adapter workflows for repository checks, source-pack staging, bundle validation, skill validation, orphan retraction, fallback skeleton generation, heuristic skill suggestion, alias management, runtime-context inspection, and skill creation.

## Role In The Workflow

- The workflow requires Python 3.11+ as a hard prerequisite, and missing support is treated as a blocking bootstrap issue that requires user consent before proceeding.
- `check_prereqs.py` runs early to verify that Python is available before any other OpenKB steps and reports the exact interpreter version.
- The prerequisite checker is intentionally dependency-free so it can run in a fresh repository without extra installs.
- Bundled scripts are expected to run through `uv run`, with `python3` only as a fallback if the user explicitly declines `uv`.
- Python is part of the broader toolchain used alongside `uv`, `git`, and OpenKB CLI tooling.
- `build_okf_skeleton.py` uses Python as a zero-LLM fallback path to generate a conservative OKF wiki skeleton from staged source material.
- `build_okf_source_pack.py` uses Python to build deterministic OpenKB-compatible staged input from a Git repository, including file selection, normalization, hashing, manifest writing, and optional bundling or splitting.
- In the source-pack builder, Python also handles repository inventory generation, graph-report filtering, bundle splitting, and deletion advisories for stale KB documents.
- `prune_okf_orphans.py` uses Python to reconcile the KB registry against the repository and retract orphaned pipeline-owned documents when their source files are deleted or renamed.
- The orphan-pruning script treats the manifest as authoritative when present, falls back to git-derived expectations when it is not, and includes a guard against accidental mass retractions.
- The orphan-pruning flow distinguishes deleted sources from deselected ones, and can detect renames by comparing old and new content hashes.
- `validate_okf_bundle.py` uses Python to enforce OKF conformance checks, including frontmatter parsing, reserved-file rules, unclosed fence detection, near-duplicate slug warnings, and OpenKB wiki link validation.
- In OpenKB wiki mode, `validate_okf_bundle.py` skips operational areas like `AGENTS.md`, `sources/`, and `reports/`, and treats broken wikilinks plus missing `sources:` lists on generated concept/entity pages as warnings or errors.
- `quick_validate.py` uses Python to perform a fast skill-directory preflight check by verifying `SKILL.md`, parsing basic YAML frontmatter, enforcing naming rules, and checking optional subdirectory layout.
- `check_prereqs.py` also uses Python to probe optional CLIs like `graphify` and `openkb`, with a longer timeout for first-run imports.
- `merge_agents_md_okf_section.py` uses Python to maintain a managed OKF guidance block inside `AGENTS.md` without rewriting repository-specific instructions.
- The OKF guidance merge script uses conservative document merging, replacing only the section between HTML comment markers and preserving surrounding content.
- That script encodes orientation rules for routing through `okf/wiki/index.md`, treating wiki content as data, and relying on `tooling/index.md` only when the index points there.
- `suggest_skills_from_okf.py` uses Python to scan an OKF wiki bundle for repeated action-oriented language and suggest candidate custom skills from heuristic keyword scoring.
- `ensure_local_alias.py` uses Python to create a local harness instruction-file alias to `AGENTS.md`, preferring a relative symlink and falling back to a pointer file when needed.
- `ensure_local_alias.py` also records the alias path in `.git/info/exclude` so local harness adapter files stay uncommitted by default.
- `inspect_runtime_context.py` uses Python to collect runtime-harness hints without invoking vendor CLIs, combining environment variables, parent-process inspection, and repository markers.
- `inspect_runtime_context.py` explicitly avoids treating installed binaries or repo markers as proof of the active runtime and emits decision guidance to prefer high-confidence signals.
- `skill-creator` uses Python as part of the authoring workflow for initializing, validating, adopting, and suggesting skills under `.agents/skills/`.
- `init_skill.py` initializes a new skill directory with the expected resource layout.
- `adopt_generated_skill.py` copies and validates a generated skill into the repository-owned skill tree.
- `quick_validate.py`, `suggest_skills_from_okf.py`, `ensure_local_alias.py`, and `inspect_runtime_context.py` show how Python supports the skill lifecycle, repository checks, local harness adaptation, and runtime detection together.

## Key Facts

- Python supports the deterministic OpenKB pipeline through scripts such as `check_prereqs.py`, `build_okf_source_pack.py`, `prune_okf_orphans.py`, `validate_okf_bundle.py`, `build_okf_skeleton.py`, `merge_agents_md_okf_section.py`, `quick_validate.py`, `suggest_skills_from_okf.py`, `ensure_local_alias.py`, `inspect_runtime_context.py`, `init_skill.py`, and `adopt_generated_skill.py`.
- The source-pack builder normalizes line endings, computes SHA-256 hashes over staged text, and derives stable provenance fields from Git history using Python code.
- The prerequisite checker uses Python to validate repository writability by creating and removing temporary probe files in key paths.
- The checker also compares shared OpenKB config keys against `config.yaml.example` and surfaces drift without reading secret contents from `.env` files.
- `build_okf_skeleton.py` handles git metadata lookup, filesystem output, and optional ingestion of staged external documentation.
- `validate_okf_bundle.py` models OKF v0.1 conformance locally and adds audit checks beyond the spec, such as unclosed code fences and near-duplicate slug detection.
- `quick_validate.py` keeps validation lightweight by parsing only simple frontmatter key-value pairs rather than invoking a full YAML parser.
- `quick_validate.py` enforces skill naming conventions with a regular expression, rejects double hyphens, and requires the directory name to match the declared skill name.
- `quick_validate.py` also checks that skill directories are placed under `.agents/skills` and that optional `scripts`, `references`, and `assets` entries are directories when present.
- `suggest_skills_from_okf.py` uses regex-based action patterns, skips low-signal conceptual pages, and aggregates evidence paths for each candidate suggestion.
- `suggest_skills_from_okf.py` derives candidate names from page titles or filenames, normalizes them into kebab-case slugs, and prefixes generic names with `manage-` when needed.
- `suggest_skills_from_okf.py` prints a ranked list of suggested skills with evidence and a ready-to-run initialization command.
- `ensure_local_alias.py` prefers a relative symlink so the alias stays portable within the repository, but it can fall back to a Markdown pointer file when symlinks are unavailable.
- `ensure_local_alias.py` refuses to place the alias outside the repository, avoids overwriting unexpected existing paths without `--force`, and will not replace a real directory.
- `ensure_local_alias.py` updates `.git/info/exclude` instead of repository-level ignore rules, keeping the alias local to one checkout.
- `inspect_runtime_context.py` gathers explicit environment variables, softer environment hints, parent-process chain data, and repo marker hits, then scores candidate harnesses from those signals.
- `inspect_runtime_context.py` treats explicit environment matches as high confidence, process and environment keyword matches as medium confidence, and repository markers as low confidence.
- `inspect_runtime_context.py` is designed for passive runtime-context inference and warns against using installed binaries as active harness proof.
- The skill creator formalizes the distinction between [[concepts/skill-action-boundary]], [[concepts/skill-structure-conventions]], and [[concepts/skill-validation-workflow]], using Python-backed utilities to enforce those rules.
- It also leans on [[concepts/baseline-first-testing]], [[concepts/caveat-preservation]], [[concepts/minimal-tool-scoping]], and [[concepts/consent-first-workflows]] when authoring or adopting skills.
- `inspect_runtime_context.py` reinforces [[concepts/adaptive-harness-detection]], [[concepts/non-invasive-detection]], and [[concepts/runtime-ambiguity-resolution]] by preferring layered signals over brittle CLI probing.
- `build_okf_source_pack.py`, `prune_okf_orphans.py`, `validate_okf_bundle.py`, and `merge_agents_md_okf_section.py` collectively support [[concepts/deterministic-validation]], [[concepts/orphan-retraction]], [[concepts/manifest-authoritative-reconciliation]], and [[concepts/conservative-document-merging]].
- `check_prereqs.py` and the broader bootstrap flow support [[concepts/preflight-checks]], [[concepts/consent-first-installation]], [[concepts/toolchain-pinning]], and [[concepts/graceful-degradation]].
- `ensure_local_alias.py` and `inspect_runtime_context.py` support [[concepts/local-only-repo-artifacts]], [[concepts/local-vs-shared-ignore]], [[concepts/instruction-file-aliasing]], and [[concepts/runtime-signal-prioritization]].
- Agent Skills define Python-backed skill packaging and validation rules, making Python relevant to [[concepts/agent-skill-specification]], [[concepts/skill-frontmatter-schema]], [[concepts/skill-progressive-disclosure]], [[concepts/skill-resource-organization]], and [[concepts/skill-validation-workflow]].
- The specification also frames Python as a practical implementation language for `scripts/` and a validation target for `skills-ref`, reinforcing [[concepts/executable-validation]], [[concepts/path-based-skill-validation]], [[concepts/portable-skill-contract]], and [[concepts/spec-authority]].

## Related Pages

- [[concepts/preflight-checks]]
- [[concepts/deterministic-validation]]
- [[concepts/safe-automation]]
- [[concepts/toolchain-pinning]]
- [[concepts/dependency-management]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/source-pack-staging]]
- [[concepts/graceful-degradation]]
- [[concepts/conservative-document-merging]]
- [[concepts/orphan-retraction]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/agent-ready-context]]
- [[concepts/agents-md-maintenance]]
- [[concepts/okf-bundle-validation]]
- [[concepts/okf-validation-rules]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/openkb-wikilink-resolution]]
- [[concepts/lightweight-frontmatter-validation]]
- [[concepts/path-based-skill-validation]]
- [[concepts/heuristic-skill-suggestion]]
- [[concepts/action-candidate-detection]]
- [[concepts/action-pattern-mining]]
- [[concepts/skill-action-boundary]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-validation-workflow]]
- [[concepts/baseline-first-testing]]
- [[concepts/caveat-preservation]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/consent-first-workflows]]
- [[concepts/consent-first-tooling]]
- [[concepts/instruction-file-aliasing]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/local-vs-shared-ignore]]
- [[concepts/compatibility-fallback]]
- [[concepts/symlink-fallback]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/non-invasive-detection]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/agent-skill-specification]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/skill-resource-organization]]
- [[concepts/executable-validation]]
- [[concepts/path-based-skill-validation]]
- [[concepts/portable-skill-contract]]
- [[concepts/spec-authority]]
- [[entities/uv]]
- [[entities/openkb]]
- [[entities/check-prereqs-py]]
- [[entities/build_okf_skeleton-py]]
- [[entities/build_okf_source_pack-py]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/prune_okf_orphans-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/quick_validate-py]]
- [[entities/suggest_skills_from_okf-py]]
- [[entities/ensure_local_alias-py]]
- [[entities/init_skill-py]]
- [[entities/adopt_generated_skill-py]]
- [[entities/scripts-inspect_runtime_context-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

## Related Documents
- [[summaries/agent-skills-spec]]

- [[summaries/README-md]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]
- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
