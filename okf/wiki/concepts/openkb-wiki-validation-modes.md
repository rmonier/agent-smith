---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "Validation modes split bundle, repo, and wiki health checks."
---

# OpenKB Wiki Validation Modes

OpenKB uses distinct validation modes to separate strict OKF bundle conformance, repository prerequisite checks, wiki health checks, and tooling-link policy checks. The split fits a [[concepts/quality-gates]] approach: some rules are hard failures, while others are warnings meant to detect damaged, incomplete, or drifting content. It also supports [[concepts/documentation-layer-separation]] and [[concepts/context-action-separation]] by keeping structural bundle checks distinct from wiki-graph checks, environment readiness checks, local tooling boundaries, and operational workflows.

## Core Modes

### OKF bundle validation

This mode checks a bundle against local OKF conformance rules. It focuses on structural correctness and deterministic parsing before the wiki is treated as a compiled knowledge base.

- non-reserved Markdown files are treated as concept documents
- concept pages must have parseable YAML frontmatter
- concept pages must include a non-empty `type` field
- `index.md` and `log.md` follow reserved-file rules
- the root `index.md` may declare `okf_version`
- the validator catches deterministic issues such as unclosed code fences and near-duplicate sibling page names
- in OpenKB wiki mode, reserved operational areas such as root `AGENTS.md`, `sources/`, and `reports/` are skipped because they are not compiled content
- in OpenKB wiki mode, broken wikilinks are errors and link resolution accepts both wiki-relative paths and bare stems
- in OpenKB wiki mode, `concepts/` and `entities/` pages are expected to carry a machine-managed non-empty `sources:` list

This mode is the offline conformance check for the compiled wiki bundle, aligning with [[concepts/okf-bundle-validation]] and [[concepts/deterministic-validation]]. The validator also degrades clearly when PyYAML is unavailable, reporting that YAML validation cannot be completed locally instead of silently guessing. That makes YAML parseability part of the overall validation contract rather than an implicit dependency.

### Repository prerequisite checks

Before validation can be trusted, the `agent-ready-context` workflow performs a preflight pass over the repository and local toolchain. These checks are not wiki-content validation themselves, but they determine whether validation can run predictably and whether the environment matches the repository's expectations.

- required runtime support is checked first, including Python 3.11+, `git`, and `uv`
- the repository must be inside a Git worktree
- optional tooling such as `graphify` and `openkb` is detected with generous timeouts to account for slow first launches
- writable paths are probed for `okf/.okf-build/input`, `okf`, and `.agents/skills`
- vendored tool skills are checked so installed CLIs have matching pinned skill copies in the repo
- OpenKB config drift is detected by comparing shared keys in `okf/.openkb/config.yaml` with `config.yaml.example`
- credential homes are reported carefully, including the project-local `okf/.env` and the user-global `~/.config/openkb/.env`
- the workflow prefers `uv run` for bundled scripts and treats missing `uv` as a prerequisite gap rather than silently degrading
- `okf/.openkb/hashes.json` is treated as a dedupe registry and must be handled carefully because registry drift can suppress future ingest runs
- repository evidence is staged deterministically under `okf/.okf-build/input/` rather than written directly into compiled KB directories
- root `AGENTS.md` is expected to stay aligned with the OKF wiki as an orientation surface, not as a long-form knowledge store

This mode sits closer to [[concepts/preflight-checks]], [[concepts/graceful-degradation]], and [[concepts/configuration-precedence]] than to content linting. It also reflects [[concepts/vendor-skills]] and [[concepts/skill-vendoring]] because the repository treats tool skills as part of the runnable surface, not as incidental local state.

### OpenKB wiki validation

This mode adapts validation to the OpenKB repository layout and operational conventions. It skips wiki-internal infrastructure areas such as root `AGENTS.md`, `sources/`, and `reports/`, then applies wiki-specific checks that reflect the compiled knowledge base surface.

- broken wikilinks are treated as errors
- `concepts/` and `entities/` pages should carry a machine-managed non-empty `sources:` list
- link resolution matches OpenKB's wiki-relative path and bare-stem behavior
- fenced code and inline code are ignored during wikilink scanning to reduce false positives
- `log.md` accepts OpenKB's timestamped heading format in wiki mode while still rejecting frontmatter and malformed headings
- explorations pages are treated specially because saved queries and findings may not follow the same frontmatter shape as compiled concept pages
- validation is run after source staging and ingestion so the wiki is checked against the current repository shape, not a stale graph
- lint findings are meant to be reviewed and triaged rather than treated as silent success
- the workflow distinguishes between compiled knowledge, source staging, and local tooling so each namespace can be validated with the right rules

This mode is tightly connected to [[concepts/openkb-wikilink-resolution]], [[concepts/openkb-wiki-health-checks]], and [[concepts/documentation-architecture]] because it evaluates whether the compiled wiki remains navigable and internally coherent.

### Tooling link policy validation

This mode enforces the boundary between the compiled wiki and local tooling context. It checks that the navigation surfaces stay intact without letting project pages depend on local tooling pages.

- pages under `okf/wiki/tooling/` may link to project pages
- project concept pages and subdirectory indexes must not link back to `okf/wiki/tooling/`
- the bundle-root `index.md` and `log.md` are exempt because they are navigation and history files rather than content dependencies
- when `okf/wiki/tooling/` contains non-reserved pages, the bundle-root `index.md` must reference `tooling/` in a clearly labeled harness-specific section
- when `okf/wiki/tooling/` contains non-reserved pages, the committed stub `okf/wiki/tooling/index.md` must exist so the root-index reference resolves on clones that do not have local tooling pages
- local tooling pages are expected to declare `scope: tooling` or `type: tooling-context`, and missing declarations are warned about rather than failed
- local tooling pages must contain at least one outgoing wikilink so they are not treated as orphaned structural dead ends
- code blocks and inline code are stripped before link scanning so examples do not trigger false positives

This mode reinforces [[concepts/tooling-link-policy]], [[concepts/tooling-context-isolation]], [[concepts/tooling-context-governance]], [[concepts/local-by-default-tooling]], and [[concepts/tooling-navigation-exception]]. It expresses a one-way relationship: tooling can point outward, but project content should not depend on tooling context.

## Validation Philosophy

The mode split keeps the repository's rules understandable and actionable:

- OKF validation asks whether the bundle is structurally valid
- repository prerequisite checks ask whether the local environment is ready for the workflow
- OpenKB validation asks whether the wiki graph is healthy and navigable
- tooling-link validation asks whether local tooling stays isolated while remaining discoverable
- agent-ready context work keeps actions, compiled knowledge, and orientation separate so each layer can evolve independently
- all four rely on explicit rules, predictable filesystem traversal, and local-only parsing
- when PyYAML is unavailable, the validator degrades clearly instead of guessing
- linting is required even though it does not serve as the final pass/fail gate, so its findings must be triaged rather than treated as a silent success
- validation is run after source staging and ingestion so the wiki is checked against the current repository shape, not a stale graph
- warnings such as unclosed fences, missing recommended frontmatter fields, or near-duplicate slugs help catch damage without turning every irregularity into a hard failure
- repository knowledge is expected to live in the OpenKB wiki, while AGENTS.md stays concise and operational

This reflects [[concepts/deterministic-validation]], [[concepts/reserved-markdown-file-rules]], and [[concepts/documentation-layer-separation]]. It also supports [[concepts/air-gapped-operation]] and [[concepts/offline-first-workflows]] by avoiding hidden network dependencies in the validation path.

## Why It Matters

Mode-aware validation helps OpenKB balance strictness and practicality:

- generated content can be checked without editing the source documents directly
- operational folders can be excluded from content validation
- link breakage can be surfaced as structural damage
- health warnings can flag issues without blocking every workflow
- validation can stay deterministic while still adapting to the wiki's compiled shape
- prerequisite checks can catch configuration drift, missing tools, and writable-path problems before deeper validation begins
- the workflow can preserve reports and triage findings before moving on to later steps
- provenance loss is surfaced when compiled pages lose their machine-managed `sources:` chain
- agent-facing guidance can stay short and current while the wiki carries durable context
- the repository can preserve a clean boundary between executable actions, curated knowledge, and local tooling context

This is especially useful in a repository that combines compiled knowledge, operational tooling, and source staging areas, and it reinforces [[concepts/generated-content-governance]] and [[concepts/wiki-review-gates]].

## Source Document

- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

## Related Concepts

- [[concepts/okf-validation]]
- [[concepts/okf-bundle-validation]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/openkb-wikilink-resolution]]
- [[concepts/quality-gates]]
- [[concepts/deterministic-validation]]
- [[concepts/preflight-checks]]
- [[concepts/configuration-precedence]]
- [[concepts/vendor-skills]]
- [[concepts/skill-vendoring]]
- [[concepts/openkb-build-workflow]]
- [[concepts/agent-ready-context]]
- [[concepts/agent-context-layering]]
- [[concepts/context-action-separation]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/tooling-link-policy]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-context-governance]]
- [[concepts/local-by-default-tooling]]
- [[concepts/tooling-navigation-exception]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]