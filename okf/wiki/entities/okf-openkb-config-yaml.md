---
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Other"
description: "Local OpenKB config file that controls provider routing and runtime settings"
---

# `okf/.openkb/config.yaml`

`okf/.openkb/config.yaml` is the local, uncommitted OpenKB configuration file that defines the active model, provider routing, and other runtime settings for a repository. It is the per-user counterpart to the shared example file `entities/okf-openkb-config-yaml-example` and is central to [[concepts/provider-routing]], [[concepts/local-vs-shared-configuration]], [[concepts/configuration-precedence]], [[concepts/tooling-consent-and-pin-management]], and the broader [[concepts/agent-ready-context]] workflow.

## Role

This file controls how OpenKB routes LLM-backed commands through LiteLLM and which provider mode is active for the current contributor. The skill documents that the model name must be set explicitly here before any LLM-backed command runs, and that this file is where each contributor chooses their own provider mode. It is also part of the broader agent-ready workflow that separates project knowledge in [[concepts/compiled-knowledge-bases]] from local execution settings and keeps the durable context source of truth in `okf/wiki/`.

The file is treated as local, per-user OpenKB state. The prereq checker flags its absence when `okf/.openkb/config.yaml.example` exists but the active config does not, and it compares a small shared subset of keys against the example file so repository-wide settings drift is surfaced early while provider-specific choices remain local. The workflow also emphasizes that generated files should not be written directly into `okf/raw/` or `okf/wiki/`, reinforcing the separation between staged input, compiled wiki content, and local runtime configuration.

The privacy and data-flow guidance adds two important constraints: before any step that sends repository content off the machine, the agent must disclose the tool, provider or endpoint, model, credential source, and what content will be sent; and OpenKB must keep a fully local air-gapped path available. This makes `okf/.openkb/config.yaml` the place where the user can intentionally select a local-only setup such as `model: ollama/<local-model>` while keeping external egress explicit and consent-based. The same guidance also notes that `openkb use` writes only local global config under `~/.config/openkb/global.yaml`.

## Key facts

- The file is local and should not be committed.
- It stores the chosen `model`, plus non-secret settings like `language`, `pageindex_threshold`, and `entity_types`.
- It can point to different provider styles, including Anthropic, ChatGPT OAuth, GitHub Copilot OAuth, OpenAI-compatible gateways, and local Ollama-based runtimes.
- Provider credentials are not stored here; they come from environment variables or `.env` files according to the documented precedence.
- The shared project template lives in `entities/okf-openkb-config-yaml-example`, while this file holds the contributor-specific active configuration.
- The prereq script treats `okf/.openkb/` as local OpenKB state, with `config.yaml` as the per-user provider choice and `hashes.json` as the dedupe registry.
- Shared keys in the committed example are expected to stay aligned across contributors; the prereq check specifically watches `language`, `pageindex_threshold`, and `entity_types` for drift.
- The workflow explicitly keeps `okf/.openkb/` local except for the example config and hash registry, and warns that registry drift around `okf/.openkb/hashes.json` can cause silent skips on future ingest runs.
- The privacy policy requires explicit disclosure before any OpenKB LLM-backed command that may send staged sources, wiki pages, or prompts to the configured litellm provider.
- In air-gapped or local-only setups, this file should select a local model and avoid `PAGEINDEX_API_KEY`, URL ingestion, and other network-dependent paths.

## Configuration behavior

The document describes `okf/.openkb/config.yaml` as the place where the active provider mode is chosen:

- `anthropic/<model>` for Anthropic-based access.
- `chatgpt/<model>` for ChatGPT subscription access.
- `github_copilot/*` for GitHub Copilot access.
- `openai/<model-id>` for OpenAI-compatible gateways.
- `ollama_chat/<model>` or `ollama/<model>` for local Ollama-style use, depending on the mode described.

It also notes that `litellm.api_base` may be needed for some modes, while OAuth-based modes should not be forced to include an API key or endpoint just for consistency. The skill frames these settings as part of [[concepts/provider-routing]] and [[concepts/local-vs-shared-configuration]], not as repository knowledge to compile into the wiki.

The prereq script adds a second layer of guardrails by reading top-level YAML scalars without a YAML dependency, which is enough to compare the shared keys in the local file against the example template while leaving nested provider blocks alone. This fits the broader emphasis on [[concepts/preflight-checks]], [[concepts/deterministic-validation]], and [[concepts/provenance-tracking]].

## Operational guidance

Before running OpenKB commands, the file should be configured to match the intended provider and harness. The related summary page also recommends cheap verification steps such as `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list` before adding content. The broader workflow emphasizes keeping provider configuration local, respecting configured package indexes, and treating credentials as hands-off.

The prereq script also checks for a writable `okf` tree and distinguishes between a project-local `.env` file and a user-global `~/.config/openkb/.env`, noting that either can satisfy credential lookup but that having both may cause confusion. That guidance aligns with [[concepts/consent-first-tooling]], [[concepts/local-only-repo-artifacts]], [[concepts/configuration-precedence]], [[concepts/privacy-preserving-tooling]], [[concepts/explicit-provider-routing]], and [[concepts/air-gapped-operation]].

The privacy-and-data-flows reference further states that a zero-LLM path must remain available, and that `build_okf_skeleton.py` can write a conservative bundle directly to `okf/wiki/` when OpenKB is not used. In that mode, `okf/.openkb/config.yaml` becomes part of the handoff from local bootstrap to later reconciliation with OpenKB linting or recompilation.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[entities/okf-openkb-config-yaml-example]]
- [[concepts/provider-routing]]
- [[concepts/configuration-precedence]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/local-by-default-tooling]]
- [[concepts/explicit-provider-routing]]
- [[concepts/tooling-context-governance]]
- [[concepts/preflight-checks]]
- [[concepts/registry-drift]]
- [[concepts/agent-ready-context]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/air-gapped-operation]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]