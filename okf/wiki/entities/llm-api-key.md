---
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Other"
description: "Universal API key variable used for OpenKB provider access"
---

# LLM_API_KEY

`LLM_API_KEY` is the universal API key variable used by OpenKB and LiteLLM to authenticate against supported LLM providers.

## Role in OpenKB

- OpenKB resolves credentials in priority order, and `LLM_API_KEY` can satisfy provider access when a provider-specific key is not required.
- It is routed through [[entities/litellm]] to the detected provider.
- The document treats it as one of the acceptable key names for Anthropic-based access, alongside `ANTHROPIC_API_KEY`.
- It is not tied to a single provider; it can be used in OpenAI-compatible gateway setups and other provider flows that accept a universal key.

## Handling rules

- The agent must not read, print, copy, validate, generate, or move this key.
- The key should be supplied through environment variables or a `.env` file, depending on the user's setup choice.
- Secrets belong in `okf/.env` or `~/.config/openkb/.env`, not in committed config files.
- The document emphasizes that credentials are hands-off for the agent, even when a smoke test is allowed.

## Related configuration facts

- OpenKB uses `LLM_API_KEY` as part of its provider-routing model in `okf/.openkb/config.yaml`.
- For authenticated OpenAI-compatible backends, the key is expected in a `.env` home rather than embedded in the config file.
- The actual provider and model should be disclosed before LLM-backed commands that send staged content.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[concepts/explicit-provider-routing]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/consent-first-tooling]]
- [[entities/anthropic-api-key]]