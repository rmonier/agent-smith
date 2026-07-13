---
type: "Summary"
description: "OpenKB provider setup, credential precedence, and backend mode guidance."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__references__openkb-providers-md.md"
---

# OpenKB Provider Configuration by Harness

This document explains how to configure OpenKB models in `okf/.openkb/config.yaml`, how credentials are resolved, and how to choose a provider for the active harness. It also records practical verification steps and a known dependency-related failure mode.

## Main ideas

- OpenKB uses LiteLLM model names in `okf/.openkb/config.yaml`, so the model must be set explicitly before any LLM-backed command.
- The provider choice should match the active harness, but the user should be asked when more than one provider is viable.
- Credentials are resolved in a fixed order: process environment, `okf/.env`, then `~/.config/openkb/.env`.
- The agent must stay hands-off with secrets: do not read, print, copy, validate, or generate API keys or `.env` contents.
- Shared project settings belong in the committed example config, while provider-specific choices stay local and uncommitted.

## Credential handling

- The document emphasizes that credential location is a setup question, not an agent decision.
- `okf/.env` and `~/.config/openkb/.env` are both valid homes, with the project file winning when both exist.
- The global path is hardcoded as `~/.config/openkb/` even on Windows.
- Recommend `~/.config/openkb/.env` for one key used across projects, and `okf/.env` for project-specific provider choice.
- If credentials already exist in the environment, a minimal connectivity smoke test is allowed, but no secret-bearing output may be shown.

## Provider selection

The document lays out a provider decision order for OpenKB:

- [[concepts/explicit-provider-routing]]: use `anthropic/<model>` when using an Anthropic-based harness or key.
- [[concepts/explicit-provider-routing]]: use `chatgpt/*` for ChatGPT subscription access with no API key.
- [[concepts/explicit-provider-routing]]: use `github_copilot/*` and configure the required extra headers.
- [[concepts/provider-integration]]: use `openai/<model>` for corporate gateways with LiteLLM-compatible base URLs.
- [[concepts/local-by-default-tooling]]: use `ollama/<model>` or another local runtime for air-gapped use.
- If no provider is available, fall back to the zero-LLM skeleton generator with limited semantic completeness.

## Configuration model

- `okf/.openkb/config.yaml` is local and uncommitted so each contributor can choose their own provider.
- `okf/.openkb/config.yaml.example` is the shared committed template.
- Shared settings include `language`, `pageindex_threshold`, and `entity_types`.
- Provider-mode templates are left commented in the example file rather than hardcoded into team-facing instructions.
- The document warns against copying provider or model choices into `AGENTS.md` or similar orientation files.

## Backend modes

The file distinguishes three backend connection styles:

- **Mode A:** `ollama_chat/<model>` with a native Ollama root endpoint and no auth.
- **Mode B:** `openai/<model-id>` with an OpenAI-compatible gateway and `LLM_API_KEY` stored in a `.env` home.
- **Mode C:** `chatgpt/<model>` or `github_copilot/*` with OAuth access and no `api_base` or API key.

It also notes that:

- `timeout:` can be set at the root or under `litellm.timeout`, with the nested value winning.
- `litellm:` passes through settings such as `api_base`, `drop_params`, and `num_retries`.
- `concurrency:` can cap concurrent LLM calls during PageIndex indexing and concept/entity compilation.
- Graphify’s Ollama backend uses an OpenAI-compatible path, which is different from OpenKB’s native Ollama path.

## Example configuration

A representative local config includes:

- a per-user `model` choice,
- `language: en`,
- `pageindex_threshold: 20`,
- optional `concurrency: 5`,
- `timeout: 1200`,
- `litellm.drop_params: true`.

The document also notes that `language` defaults to `en` and that `PAGEINDEX_API_KEY` is only needed to opt into PageIndex Cloud.

## Verification workflow

Suggested checks after configuration:

- run `openkb --kb-dir ./okf status`,
- run `openkb --kb-dir ./okf list`,
- test with a single-file `openkb --kb-dir ./okf add <file>` before bulk ingestion.

Before the first add, recompile, lint, query, chat, skill, or deck command, the user should be told which tool, provider, model, endpoint, credential source, and staged content will be used. The disclosure format is defined in [[concepts/data-flow-disclosure]].

## Known failure mode

- Some LLM-backed failures are caused by the local Python dependency environment, not by the provider or model.
- The cited example is a Pydantic error such as `InputTokensDetails.cache_write_tokens` being required.
- The document says not to classify that as a provider failure and not to bypass the failed phase.
- The remedy is to follow the known incompatibility note in [[entities/openkb-lifecycle]] and reinstall the tool under the recorded transitive constraint if needed.

## Takeaway

This document is a practical configuration guide for OpenKB provider selection, secret handling, and safe verification. Its strongest themes are [[concepts/configuration-precedence]], [[concepts/provider-integration]], and [[concepts/local-by-default-tooling]].

## Related Concepts
- [[concepts/air-gapped-operation]]
- [[concepts/cross-platform-tooling]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/provenance-tracking]]
- [[concepts/tooling-context-governance]]
- [[concepts/openkb-wiki-health-checks]]

## Entities
- [[entities/litellm]]
- [[entities/ollama]]
- [[entities/openkb-cli]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/llm-api-key]]
- [[entities/anthropic-api-key]]
- [[entities/pageindex-api-key]]
- [[entities/pageindex-cloud]]
- [[entities/openkb-add]]
- [[entities/validate_okf_bundle-py]]
- [[entities/check_prereqs-py]]
- [[entities/references-official-okf-spec-web-check-md]]
- [[entities/references-tooling-context-policy-md]]
- [[entities/runtime-detection-md]]
