---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
description: "How OpenKB selects and configures LLM providers per harness."
---

# Provider Integration

Provider integration is the pattern OpenKB uses to connect a chosen harness, model family, and credential source to the local wiki workflow. The source document frames this as a deliberate configuration step, not an automatic default: the active provider must be selected explicitly in `okf/.openkb/config.yaml`, and the choice should be disclosed before any LLM-backed command runs.

## What this concept covers

- Mapping a harness to a LiteLLM model name such as `anthropic/<model>`, `chatgpt/*`, `github_copilot/*`, `openai/<model>`, or `ollama/<model>`.
- Choosing whether the provider is key-based, OAuth-based, gateway-based, or local-only.
- Routing credentials through the right location without exposing secrets.
- Keeping the committed template provider-neutral while leaving the user’s local config uncommitted.
- Verifying configuration before bulk ingestion or other semantic operations.

## Key integration rules

- OpenKB resolves credentials in a fixed order: process environment, `okf/.env`, then `~/.config/openkb/.env`.
- The document treats credential placement as a setup question for the user, not something the agent should infer.
- Provider selection depends on the active harness, but the user should be asked when more than one provider is plausible.
- The local `okf/.openkb/config.yaml` is per-user and uncommitted, while `okf/.openkb/config.yaml.example` carries the shared settings.
- Shared settings such as `language`, `pageindex_threshold`, and `entity_types` are part of the project contract and should remain aligned across contributors.

## Provider modes

The source describes three broad backend shapes:

- **Anthropic-based or key-present**: use `anthropic/<model>` with `ANTHROPIC_API_KEY` or `LLM_API_KEY`.
- **ChatGPT or GitHub Copilot subscription**: use `chatgpt/*` or `github_copilot/*` with OAuth-style access and no API key.
- **OpenAI-compatible gateway or corporate endpoint**: use `openai/<model>` with the gateway’s base URL and key conventions.
- **Local runtime**: use `ollama/<model>` or `ollama_chat/<model>` with a local endpoint and no API auth.
- **No provider**: fall back to a zero-LLM skeleton path when semantic completeness is limited.

This makes provider integration a [[concepts/explicit-provider-routing]] concern: the model name, base URL, and credential source must match the chosen runtime rather than being guessed from the environment.

## Configuration boundaries

Provider-specific details stay local so they do not force one contributor’s stack onto everyone else. The committed example config captures the shared wiki-shaping settings, while the per-user config stores the selected model and backend mode.

The document also emphasizes that provider details should not be copied into orientation files like `AGENTS.md`. That separation supports [[concepts/local-vs-shared-configuration]] and [[concepts/tooling-boundaries]] by keeping user-specific runtime decisions out of shared instructions.

## Verification and disclosure

Before using the configured provider, the workflow recommends cheap read-only checks first:

- `openkb --kb-dir ./okf status`
- `openkb --kb-dir ./okf list`
- a single-file `openkb --kb-dir ./okf add <file>` test before bulk ingestion

The first LLM-backed command should include a disclosure of the tool, provider, model, endpoint, credential source, and the content that will be staged. That disclosure aligns with [[concepts/data-flow-disclosure]] and [[concepts/privacy-preserving-tooling]].

## Failure interpretation

A notable warning in the source is that some failures are not provider failures at all. If an LLM-backed command fails while constructing token-usage metadata, the issue may come from the local Python dependency environment rather than from the chosen provider or model.

That distinction matters for [[concepts/dependency-management]] and [[concepts/quality-gates]]: semantic failures should not be dismissed as mere configuration noise, but provider-independent toolchain errors should be handled at the dependency layer first.

## Related ideas

- [[concepts/configuration-precedence]] for how environment, project-local files, and user-global files are ordered.
- [[concepts/local-vs-shared-configuration]] for the split between per-user runtime choice and shared project settings.
- [[concepts/preflight-checks]] for status and list checks before ingestion.
- [[concepts/deterministic-validation]] for the recommendation to verify with small, cheap commands before broader runs.
- [[concepts/consent-first-workflows]] for the rule that credentials and provider selection should not be handled implicitly.

## Source

- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]