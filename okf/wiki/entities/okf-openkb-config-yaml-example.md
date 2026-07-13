---
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Other"
description: "Committed OpenKB config template for shared defaults and local provider setup"
---

# okf/.openkb/config.yaml.example

`okf/.openkb/config.yaml.example` is the committed OpenKB configuration template that keeps shared, versioned settings aligned while leaving provider-specific choices local.

## What it is

- The example file is the shared counterpart to the uncommitted `okf/.openkb/config.yaml`.
- New contributors copy it to create their local config, then choose a provider/model mode for their own environment.
- It is part of the OpenKB provider setup described in [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]].
- It belongs to the KB's split between committed shared defaults and local per-user runtime state, which the agent-ready workflow treats as a core boundary.
- The prerequisite checker compares it against the local config to detect drift in the shared wiki-shaping keys before compilation continues.
- The agent-ready-context skill treats `okf/` as the OpenKB KB root and keeps `okf/.openkb/` under OpenKB ownership, with the example config as the committed template and `okf/.openkb/config.yaml` as the user-local selection file.
- The workflow emphasizes that generated KB content should not be written directly into `okf/wiki/`; instead, deterministic input is staged first and then ingested, so this example config supports the broader staged-compilation pipeline.
- The privacy and data-flows guidance also frames this template as part of explicit routing and consent-first use: provider selection must never be implicit, and the configured backend is one of the key values contributors decide locally.

## Key facts

- It carries the shared wiki-shaping settings: `language`, `pageindex_threshold`, and `entity_types`.
- Those shared keys are meant to stay consistent across contributors.
- Provider details are intentionally not committed here, so each contributor can route to their own LLM stack without binding the team to one choice.
- The document treats this file as the safe place for commented provider-mode templates rather than hardcoded team instructions.
- The local runtime file, `okf/.openkb/config.yaml`, is the place for the actual model selection, timeout, and backend settings.
- When `okf/.openkb/config.yaml` is missing, the checker reports a clear setup error and points contributors back to the example file.
- If both the project-local `.env` and `~/.config/openkb/.env` exist, the workflow prefers the project file and warns about the dual credential homes.
- The privacy guidance reinforces that OpenKB should disclose the tool, provider or endpoint, model, credential source, and content before any LLM-backed step that sends repository material off the machine.
- The template fits the broader agent-ready workflow's emphasis on [[concepts/local-vs-shared-configuration]], [[concepts/explicit-provider-routing]], [[concepts/toolchain-pinning]], [[concepts/data-flow-disclosure]], and [[concepts/consent-first-tooling]] around reproducible setup.
- It also sits inside the repository's broader boundary between durable KB context and local operational state, alongside other ignored or user-scoped artifacts managed by the workflow.

## Role in workflow

- This template supports [[concepts/local-vs-shared-configuration]] by separating shared defaults from per-user provider settings.
- It also supports [[concepts/explicit-provider-routing]] because the model must be chosen explicitly before LLM-backed commands run.
- Its shared fields affect compiled wiki behavior, so drift in these settings can change ingestion and page generation outcomes.
- The file is part of the broader OpenKB configuration surface tied to [[entities/openkb]] and [[entities/okf]].
- In the agent-ready-context workflow, it sits alongside KB root staging, prerequisite checks, and validation steps that keep `okf/` consistent with the repository's compiled knowledge pipeline.
- It is one of the repository-shared artifacts checked by the preflight script that also validates tool availability, vendored skills, and writable paths.
- It helps keep the repo aligned with the workflow's split between action skills, compiled context, and orientation files.
- In the privacy policy, it is also part of the operational boundary that preserves a fully local or air-gapped path when contributors choose `ollama`-backed or zero-LLM operation.

## Related ideas

- [[concepts/configuration-precedence]] for how local files, project files, and environment variables interact.
- [[concepts/provider-integration]] for how LiteLLM model naming maps to provider backends.
- [[concepts/provenance-aware-tool-installation]] for the care taken around local, user-specific runtime setup.
- [[concepts/quality-gates]] for the verification steps recommended after configuration.
- [[concepts/consent-first-tooling]] for the install-and-configure steps that precede LLM-backed use.
- [[concepts/offline-first-workflows]] for the workflow's ability to stage and validate without immediate network dependence.
- [[concepts/preflight-checks]] for the broader class of checks this file participates in.
- [[concepts/registry-drift]] for the shared-key mismatch the checker tries to catch early.
- [[concepts/kb-root-staging]] for the rule that deterministic input is staged under `okf/.okf-build/input/` instead of writing generated pages directly.
- [[concepts/knowledge-compilation-pipeline]] for the end-to-end flow from staged source to compiled wiki output.
- [[concepts/air-gapped-operation]] for the local-only mode this template helps preserve.
- [[concepts/privacy-preserving-tooling]] for the insistence on explicit disclosure and local control over egress.
- [[concepts/provider-routing]] for the rule that backend choice must be deliberate and visible.

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]