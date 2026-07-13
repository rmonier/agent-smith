---
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md"]
type: "Work"
description: "Core repository-maintenance skill for OpenKB agent-ready workflows."
---

# Agent Ready Context

`agent-ready-context` is the core repository maintenance skill in the agent-skills set for making a project agent-ready. It defines how to separate actions, durable context, and orientation material, and it serves as the workflow backbone for keeping an OpenKB-backed repository current.

## What it does

The skill provides the end-to-end workflow for preparing and maintaining a repository knowledge surface. It is used to:

- create or refresh the compiled OKF wiki under `okf/wiki/`
- keep `AGENTS.md` aligned with the wiki as the source of truth
- stage deterministic repository evidence for ingestion
- validate the resulting OKF bundle
- manage external evidence, findings, and harness records
- support downstream runtime-specific adapter work such as [[entities/subagent-profile-adapter]]
- organize the repository snapshot and tracked-file inventory that document the current ingestable surface
- define dependency and tool-boundary policy without inventing a non-standard `dependencies` field in `SKILL.md`
- treat `scripts/check_prereqs.py` as the executable source of truth for local readiness
- keep the repository agent surface split into skills, OKF wiki context, and `AGENTS.md` orientation
- avoid writing generated files directly into `okf/raw/` or `okf/wiki/`
- rely on staged deterministic input under `okf/.okf-build/input/` for OpenKB ingestion
- preserve the role of `okf/.openkb/hashes.json` as a dedupe registry that can silently suppress later ingestion if it drifts
- handle discovered knowledge through finding pages under `okf/wiki/explorations/findings/` rather than patching compiled wiki pages by hand
- use the portable skill bundle as the repository's agent-ready surface, with `AGENTS.md`, `okf/wiki/`, and `.agents/skills/` as distinct layers
- keep operational basics in `AGENTS.md`, including primary language(s), toolchain versions, setup/build/launch commands, and test invocation
- point `AGENTS.md` to `okf/wiki/index.md` instead of deep-linking individual wiki pages
- use `okf/wiki/index.md` as the first routed context after `AGENTS.md`
- read `tooling/index.md` when the wiki index routes to tooling context, then identify the active harness from runtime metadata or self-knowledge and inspect the matching local harness page plus any relevant provider page before provider-backed work
- treat tooling as local context rather than project truth, and continue through the index if harness identification is unavailable
- inspect `okf/wiki/AGENTS.md` after OpenKB init or upgrades, and keep custom sections such as `tooling/` and `explorations/findings/` declared there
- preserve local tooling discovery methods that include ignored files, because a first-clone empty overlay is normal and should not block work
- run the repository through a consent-first bootstrap that discloses installs, pins, integrity data, and egress before any LLM-backed step
- support both online and air-gapped operation, with local-provider routing when remote egress is not wanted

## Core model

The document frames repository knowledge in three layers:

- skills as repeatable actions and automation
- the OKF wiki as durable context and provenance
- `AGENTS.md` as concise orientation and operational guidance

This separation is central to the skill's design and is closely related to [[concepts/context-action-separation]], [[concepts/durable-context]], [[concepts/agent-context-layering]], [[concepts/knowledge-boundaries]], [[concepts/documentation-architecture]], and [[concepts/progressive-disclosure]]. The README also reinforces the same model with a clearer surface split: `AGENTS.md` for orientation, `okf/wiki/` for context, `.agents/skills/` for actions, and harness adapters as runtime projections.

## Operational rules

The skill emphasizes several constraints and conventions:

- the durable source of truth is `okf/wiki/`
- generated files should not be written directly into `okf/raw/` or `okf/wiki/`
- `uv run` should be used for bundled scripts when `uv` is available
- dependency bootstrap should use `uv sync` when project metadata is present
- tooling should be installed only with explicit user consent
- fetched web content is treated as untrusted evidence
- generated artifacts should stay out of version control
- runtime-specific subagent or profile adapters are projections, not a portable standard
- active harness detection must rely on runtime signals and documentation, not just installed binaries
- the repository snapshot should reflect the current git-tracked files so ingestion stays aligned with what is actually versioned
- `allowed-tools` is only a permission hint, while `compatibility` and `metadata.*` are the proper places for environment and local-tool hints
- companion skills are optional follow-up capabilities, so missing `skill-creator` or `subagent-profile-adapter` must not block the workflow
- required local tools include `git`, `uv`, Python 3.11+, and writable repository paths for `okf/.okf-build/`, `okf/`, and `.agents/skills/`
- `openkb` and `graphify` are optional, with graceful degradation when they are unavailable
- vendored skill copies are immutable vendor content and should be refreshed by re-vendoring, not edited in place
- the dependency and install policy must preserve package-name accuracy, index provenance, version pinning, and integrity hashes
- supply-chain trust is handled with trust-on-first-use and recorded sha256 values from the configured index
- first-time adoption should be consent-first, including showing the exact command, upstream source, and pin details before installation
- the active harness for any harness-wide install must be detected from runtime guidance, not inferred from installed binaries
- the workflow treats web-fetched documentation as untrusted and only summarizes it as evidence
- OpenKB tooling runs are gated by explicit provider and privacy rules before any LLM-backed command
- bundle validation and review are expected after ingestion so generated wiki pages can be checked for classification, grounding, and duplicate issues
- `AGENTS.md` should collapse into pointers after OKF refreshes whenever context has a wiki home
- OpenKB lifecycle policy adds a read-first loop: check `openkb status` and `openkb list`, then inspect `okf/wiki/index.md` and only use `openkb query` as a last resort
- OpenKB ingestion is hash-deduplicated through `okf/.openkb/hashes.json`, so registry drift can silently suppress later ingestion if the registry and wiki diverge
- OpenKB deletion is not automatic, so removed or moved repository sources require reconciliation before ingesting again
- findings are captured in `okf/wiki/explorations/findings/` and can be promoted only when they remain true and conflict with compiled knowledge or leave a real gap
- `openkb lint` is a health report, not a hard gate, while deterministic validation remains the pass/fail check
- curation-only edits are allowed only as a bounded exception when neither source repair nor findings capture can express the fix

It also highlights special handling for `okf/.openkb/hashes.json`, because the dedupe registry can suppress later ingestion if it incorrectly claims content is already present. The README adds that the repo-level security model also depends on no silent installs, registry-agnostic commands, explicit data-flow disclosure, no telemetry assumptions, secret hygiene, and untrusted-input discipline.

## Workflow coverage

The skill documents an end-to-end workflow that includes:

- prerequisite checks and repository layout confirmation
- dependency bootstrap and vendor-skill adoption
- ignore-rule and hash-registry hygiene
- Graphify graph generation
- source-pack staging for OpenKB
- OpenKB initialization and ingestion
- orphan retraction and findings triage
- linting, review, and bundle validation
- `AGENTS.md` maintenance and tooling-harness records
- harness detection, adapter design, and validation for native profile files when the active environment supports them
- repository inventory capture as a baseline for future comparisons and regeneration
- local readiness checks that can fall back to stdlib-only execution in degraded mode when the user declines `uv`
- project-scoped skill vendoring for `graphify` and `openkb` before the corresponding CLIs are used
- release-note review and explicit approval before any pin update
- run-report discipline that explicitly states whether repeated actions warrant new skills, whether profile adapters were created, and whether a harness build record was written
- air-gapped operation that can still produce a useful deterministic skeleton when no local LLM is available
- onboarding behavior that starts from `AGENTS.md`, then routes through `okf/wiki/index.md`, then uses graph maps and skills to select the right local context
- OpenKB-specific read-first and lifecycle hygiene, including status/list before ingest, reconciliation before add, and lint/validate after changes
- repository inventory capture from git-tracked files as a baseline for the ingestable surface and a check against drift between source reality and compiled knowledge
- initial root-index routing that uses `okf/wiki/index.md` as the first OKF page, then `tooling/index.md` when the index points into tooling context
- local tooling discovery that includes ignored files, so an empty first-clone overlay is treated as normal rather than blocking work
- source-pack construction that remains deterministic across commits by recording the last commit that touched each staged file instead of HEAD
- a requirement to refuse broad `recompile --all` without consent and to preview recompiles with `--dry-run`
- a post-generation review pass that checks for missing concepts, duplicates, misclassification, caveat loss, truncation, stale early pages, grounding problems, and stale promoted findings
- preservation of `openkb lint` reports under `okf/.okf-build/reports/` with semantic triage even when lint exits successfully

That workflow connects strongly to [[concepts/repository-ingestion]], [[concepts/source-pack-staging]], [[concepts/okf-bundle-validation]], [[concepts/orphan-retraction]], [[concepts/tooling-consent-and-pin-management]], [[concepts/skill-vendoring]], [[concepts/supply-chain-security]], [[concepts/air-gapped-operation]], [[concepts/explicit-provider-routing]], [[concepts/consent-first-workflows]], [[concepts/hash-registry-coherence]], [[concepts/manifest-authoritative-reconciliation]], [[concepts/findings-promotion]], [[concepts/openkb-wiki-health-checks]], and [[concepts/openkb-wiki-validation-modes]]. It also ties directly to [[concepts/repository-inventory]] and [[concepts/repository-structure-overview]] through the tracked-file snapshot that defines the current repository surface.

## Script behavior

`merge_agents_md_okf_section.py` is the helper that enforces the managed `AGENTS.md` section. It:

- reads an existing file or starts from empty content
- replaces the text between the two HTML markers when both are present
- appends the managed section to existing content when no managed block exists yet
- initializes a new `AGENTS.md` with a heading when the file does not exist
- writes the merged content back as UTF-8 text and prints the resulting path

This makes the script a conservative document merger rather than a full-file generator. Its main role is to keep repository-specific instructions intact while refreshing the OpenKB routing and maintenance guidance.

## Related pages

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/repo-snapshot]]
- [[entities/openkb]]
- [[entities/uv]]
- [[entities/graphify]]
- [[entities/agents-md]]
- [[entities/subagent-profile-adapter]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/check_prereqs-py]]
- [[entities/skill-creator]]
- [[entities/agent-smith]]
- [[entities/readme-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

## Why it matters

`agent-ready-context` serves as the procedural backbone for repository agentification: it keeps actions, evidence, and documentation routes distinct while ensuring the compiled wiki remains the authoritative context layer.

The repo snapshot adds that this role is grounded in a real tracked-file inventory. The skill is not just a workflow description; it is anchored in the repository's current surface, including `.agents/skills/`, licensing files, documentation assets, and the governance files that define how ingestion, provenance, and local tooling should behave.

It also establishes the conditions that later adapter skills depend on: a refreshed `AGENTS.md`, a maintained OKF wiki, and a clear boundary between durable project knowledge and harness-specific runtime projections. The README makes that boundary explicit by describing `AGENTS.md` as orientation, `okf/wiki/` as context, `.agents/skills/` as actions, and harness adapters as runtime-specific projections.

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

## New Harness Adapter Guidance

The companion [[entities/subagent-profile-adapter]] skill adds runtime-specific adapter work on top of this repository-maintenance workflow. It treats subagent or profile files as projections for the active harness only, not as a portable standard, and it relies on the same layered split between `AGENTS.md`, OKF wiki context, and Agent Skills.

The skill further tightens harness handling by requiring explicit runtime detection, documentation-based confirmation of subagent support, and conservative generation of short native adapter files. Those adapters should stay minimal, point back to `AGENTS.md`, `okf/wiki/`, and relevant skills, and be validated with the tooling link policy before use.

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[concepts/runtime-adapter-management]]

See also: [[concepts/harness-native-profiles]]

See also: runtime detection md

See also: [[concepts/tooling-link-policy]]

See also: [[concepts/tooling-context-governance]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
