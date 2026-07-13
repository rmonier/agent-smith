---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Tooling that requires explicit approval before installs, routing, or repo changes."
---

# Consent-First Tooling

Consent-first tooling is a workflow model where tool installation, vendoring, backend selection, git-tracking decisions, harness adapter generation, knowledge-base bootstrap steps, and any other environment-changing or data-sending action happen only after the user explicitly approves them. It treats setup, egress, repository state changes, runtime projections, and backend routing as decision points rather than automatic side effects.

In the agent-ready repository model, consent also governs how knowledge is compiled, where repository content is staged, when a workflow may degrade instead of failing outright, and how the repository's distributable skill surface is separated from vendored toolchain copies. The goal is to keep the agent aligned with user intent while avoiding silent changes to the repository, machine state, or data destination.

The README sharpens this into a three-surface product model: `AGENTS.md` carries orientation, `okf/wiki/` carries durable compiled context, and `.agents/skills/` carries repeatable actions. Consent-first tooling is the policy that keeps those layers distinct while allowing the workflow to ask before it installs, routes, writes, or exports anything that would change the environment or move content.

## Core ideas

- Tooling changes require explicit user consent before execution.
- The agent should explain the tool, package name, configured index, upstream source, pinned version, exact command, provider or endpoint, and what content would be sent.
- Routing must be explicit: tools should not silently choose a backend or provider from available credentials.
- The user can choose to install the tool, skip it, route it locally, or handle it themselves.
- Missing optional tools should trigger graceful degradation, not failure.
- Consent applies to installation, vendoring, backend selection, later version bumps, re-vendoring steps, graph generation, KB initialization, harness adapter generation, and git-tracking choices for generated files.
- When a step would send repository content off-machine, disclosure must come before execution and include the credential source.
- If a companion skill is required to adopt a tool, that vendoring decision is part of the same approval as installing the CLI.
- For generated adapters or other harness-local files, the default consent outcome is usually local-only: write the files, exclude them via `.git/info/exclude`, and avoid committing them unless the user or team has chosen shared tracking.
- If a generated file is intended for every contributor, the policy may shift to `.gitignore` instead of local exclusion, but that is still an explicit decision rather than an assumed default.
- Harness-specific adapter generation itself is consent-sensitive because it projects current repository knowledge into runtime-native files rather than creating durable project source.
- If the active harness needs an alternate instruction filename instead of `AGENTS.md`, the preferred approach is a local symlink added to `.git/info/exclude`, and that alias should only be created after confirming the requirement from documentation or the user.
- Consent-first behavior also applies when adopting the repository's own agent-ready workflow: the core `agent-ready-context` skill checks prerequisites before installs, asks before pulling in pinned tools, and keeps degraded paths available when optional capabilities are missing.
- In that workflow, `scripts/check_prereqs.py` is the readiness authority, `uv` is the required Python toolchain, and optional tools such as `graphify` and `openkb` are treated as consented, pinned dependencies rather than ambient assumptions.
- The same approval boundary covers vendoring the matching skill before first CLI use, because the repository needs both the tool and its portable usage guidance before the workflow becomes reliable.
- The README extends this into a broader product model: only three skills are the distributable capability surface, while vendored `graphify` and `openkb` copies are toolchain artifacts that should not be carried over blindly.
- The repository's knowledge base is built as a compiled wiki, but the staging path stays deterministic and local until the user consents to a full OpenKB lifecycle run.
- Consent also shapes how stale or missing content is handled: prune, remove, and recompile operations stay consent-first, and the workflow prefers report-only checks before destructive changes.
- The same model extends to air-gapped operation: when local execution is requested, provider routing stays explicit and the repository can still build a deterministic zero-LLM skeleton if no local model is available.

## In the source document

The source page [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] makes consent-first behavior central to the `agent-ready-context` pipeline:

- It requires a prereq check before any install action.
- It frames `uv`, `graphify`, and `openkb` as pinned, user-scoped tools rather than implicit dependencies.
- It instructs the agent to present installation details and wait for the user's choice.
- It says the workflow should continue in degraded mode if a companion skill or optional tool is absent.
- It treats vendoring the matching skill as part of the same consented adoption decision as installing the CLI.
- It requires the same explicit approval before first use of vendor skills for `graphify` and `openkb`.
- It adds trust-on-first-use integrity pinning so later installs can be compared against the originally recorded artifact hash.
- It treats tool updates as consented events: detect newer versions, review release notes, then update the pin only after explicit approval.

The README broadens that policy into repository architecture:

- `AGENTS.md` is only an orientation surface; durable knowledge belongs in `okf/wiki/` and repeatable actions belong in `.agents/skills/`.
- `okf/` is the OpenKB root, and generated KB content should not be written directly into `okf/raw/` or `okf/wiki/`.
- Deterministic staging under `okf/.okf-build/input/` preserves a reviewable boundary before ingestion.
- Graph generation, KB initialization, and orphan pruning are deliberate steps that should be disclosed and consented to rather than assumed.
- The workflow explicitly allows report-only checks, degraded paths, and best-effort skips when reliability is low.
- Harness build records and local tooling context are only created when identification is reliable enough to justify them.
- Registry drift in `okf/.openkb/hashes.json` is treated as a sensitive state boundary because silent dedupe can hide lost wiki pages.
- The distributable product surface is only the three portable skills; vendored `graphify` and `openkb` directories are toolchain copies, not user-facing capabilities.

The workflow also extends consent into data flow and provider selection:

- Before any step that sends repository content off the machine, the agent must announce the tool, provider or endpoint, model, credential source, and content to be sent.
- OpenKB must use explicit provider configuration instead of silent routing.
- graphify must be given an explicit backend when processing non-code sources.
- External docs, web evidence, and local PDF/cloud processing are all consent-sensitive because they can move content beyond the machine.
- A fully local air-gapped path and a zero-LLM fallback must remain available.
- The consent boundary applies equally to one-time bootstrap runs and incremental maintenance runs.

The git-tracking policy for generated context adds another consent layer:

- Harness profile adapters are treated as local preferences by default, so they should be written locally and added to `.git/info/exclude` rather than `.gitignore`.
- `.gitignore` is reserved for cases where every contributor should ignore generated adapters or other generated files.
- Committing adapters is only appropriate when the team has explicitly standardized on the harness and wants shared runtime profiles.
- For `okf/wiki/tooling/` pages, the default changes because every contributor generates harness build records there: the shared-ignore case applies, so `.gitignore` is the right exclusion mechanism, with `okf/wiki/tooling/index.md` kept as the committed navigation stub.
- If the active harness needs an alternate instruction filename instead of `AGENTS.md`, the preferred approach is a local symlink added to `.git/info/exclude`, and that alias should only be created after confirming the requirement.

Together, these requirements define consent-first tooling as both a dependency policy and a data-routing policy, with an additional default toward local-only tracking for generated harness artifacts.

## Related ideas

Consent-first tooling overlaps with [[concepts/tooling-consent-and-pin-management]], [[concepts/trust-on-first-use]], [[concepts/version-pinning]], [[concepts/toolchain-pinning]], and [[concepts/graceful-degradation]]. It also depends on the distinction between [[concepts/harness-vs-local-tools]] and vendor skills, because the workflow separates agent capabilities from repository-scoped tool readiness.

It is also closely related to [[concepts/data-flow-disclosure]], [[concepts/explicit-provider-routing]], [[concepts/privacy-preserving-tooling]], [[concepts/kb-root-staging]], [[concepts/air-gapped-operation]], [[concepts/local-vs-shared-ignore]], and [[concepts/git-tracking-policy]], since consent is not just about installing software but also about controlling where data goes and how generated files are tracked.

It further connects to [[concepts/runtime-ambiguity-resolution]], [[concepts/runtime-signal-prioritization]], [[concepts/harness-native-profiles]], [[concepts/subagent-role-design]], and [[concepts/instruction-file-aliasing]] because adapter generation and harness selection both require explicit confirmation about the execution environment and its file conventions.

## Why it matters

This pattern reduces surprise, limits accidental machine changes, and makes dependency handling auditable. It is especially important in repository automation workflows where installs, vendoring, validation, content processing, harness adaptation, and generated-file tracking can affect both local state and shared project state.

In practice, consent-first tooling supports safer [[concepts/safe-automation]] and cleaner [[concepts/preflight-checks]] without forcing the pipeline to stop whenever an optional capability is missing. It also protects user trust by making routing, egress, local-only fallback, harness adapter generation, and git-tracking decisions explicit before any sensitive action runs.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/README-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
