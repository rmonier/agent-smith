---
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Other"
description: "Environment variable name for Anthropic API authentication"
---

# ANTHROPIC_API_KEY

`ANTHROPIC_API_KEY` is the environment variable name used for Anthropic API authentication in OpenKB setups.

## Key facts

- OpenKB resolves credentials by checking process environment variables first, then `okf/.env`, then `~/.config/openkb/.env`.
- The document treats `ANTHROPIC_API_KEY` as a provider-specific credential that can be used alongside the universal `LLM_API_KEY`.
- For Anthropic-based harnesses, the configured model should use the `anthropic/<model>` naming pattern.
- The credential is handled under a strict hands-off rule: the agent must not read, print, copy, validate, or generate secret values.
- If credentials are already present in the process, only a minimal connectivity smoke test is allowed, and no secret-bearing output may be shown.

## Relationship to OpenKB configuration

This variable is part of the provider-routing and credential-resolution logic described in [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]. It supports [[concepts/explicit-provider-routing]] and [[concepts/configuration-precedence]] by giving OpenKB a provider-specific key that can be discovered from the environment or a local `.env` file.

## Operational notes

- The document recommends keeping `.env` files gitignored.
- It distinguishes between per-project configuration in `okf/.env` and user-wide configuration in `~/.config/openkb/.env`.
- `ANTHROPIC_API_KEY` is relevant when Anthropic access is key-based through LiteLLM rather than via any OAuth-style login flow.

## Related entities

- [[entities/anthropic]]
- [[entities/litellm]]
- [[entities/llm-api-key]]
- [[entities/openkb]]
- [[entities/okf-openkb-config-yaml]]