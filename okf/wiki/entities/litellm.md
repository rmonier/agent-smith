---
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "Model routing layer used by OpenKB for provider configuration"
---

# LiteLLM

LiteLLM is the model-routing layer OpenKB uses for provider configuration in `okf/.openkb/config.yaml`. OpenKB expects LiteLLM-style model names and uses LiteLLM settings to connect to Anthropic, ChatGPT, GitHub Copilot, OpenAI-compatible gateways, and local runtimes.

## Role in OpenKB

- OpenKB stores the active model choice in `okf/.openkb/config.yaml` using LiteLLM naming conventions.
- The document treats LiteLLM as the mechanism that routes requests to the selected provider.
- Provider-specific settings such as `api_base`, `drop_params`, `num_retries`, and `timeout` can be passed through via the `litellm:` section.
- The same provider choice should not be committed into shared orientation files, because each contributor may use a different provider stack.
- OpenKB's privacy rules require explicit disclosure before any LLM-backed command that uses LiteLLM to send staged sources, wiki content, or prompts off the machine.

## Key facts from the document

- Anthropic access can be configured with `anthropic/<model>` and `ANTHROPIC_API_KEY` or `LLM_API_KEY`.
- OpenAI-compatible gateways use `openai/<model-id>` with a gateway base URL and an `LLM_API_KEY` stored in a `.env` home.
- Local Ollama usage can be configured with `ollama/<model>` or `ollama_chat/<model>`, depending on the connection mode.
- ChatGPT and GitHub Copilot subscription providers are also available through LiteLLM-style model names.
- OpenKB uses LiteLLM model naming as the user-facing abstraction even when the underlying provider differs.
- The privacy-and-data-flows policy treats LiteLLM as the configured provider layer for commands like `add`, `recompile`, `lint`, `query`, `chat`, `skill`, and `deck`.
- When OpenKB operates locally, LiteLLM can be pointed at `ollama/<model>` so content stays on-device.

## Configuration and behavior

- `okf/.openkb/config.yaml.example` carries the shared project settings, while `okf/.openkb/config.yaml` is local and uncommitted.
- The document notes that `litellm.api_base` may be set explicitly or via LiteLLM-related environment variables.
- The document also notes that `timeout` can be specified at the root or under `litellm.timeout`, with the nested value taking precedence.
- For local runtimes, `litellm.drop_params: true` is recommended in the example config.
- LiteLLM sits inside the broader [[concepts/provider-routing]] and [[concepts/local-vs-shared-configuration]] patterns used by OpenKB.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[entities/openkb]]
- [[entities/ollama]]
- [[entities/anthropic]]
- [[entities/chatgpt]]
- [[entities/github-copilot]]
- [[concepts/provider-integration]]
- [[concepts/explicit-provider-routing]]
- [[concepts/configuration-precedence]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/privacy-preserving-tooling]]