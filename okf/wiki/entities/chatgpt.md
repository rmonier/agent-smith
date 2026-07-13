---
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "ChatGPT is an OAuth subscription provider option for OpenKB routing."
---

# ChatGPT

ChatGPT is presented as a provider option for [[entities/openkb]] when configuring LLM-backed workflows through [[entities/litellm]]. In the provider-selection guidance summarized in [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]], ChatGPT is the recommended path for users who have a ChatGPT subscription and want to route staged content through that subscription. The guidance treats ChatGPT as an OAuth subscription provider, emphasizes explicit model selection via `chatgpt/*`, and places it within a broader decision process that asks users which provider they want to bill rather than assuming the active harness determines routing.

## Role in OpenKB provider selection

- Use a `chatgpt/*` model name when selecting ChatGPT as the provider in OpenKB configuration.
- This option is presented as an OAuth subscription provider rather than a key-based API provider.
- Unlike the Anthropic path, this route does not require an API key in the documented workflow.
- ChatGPT is one step in an ordered provider-selection process that evaluates available harnesses, subscriptions, keys, and local runtimes before falling back to an LLM-free path.
- Provider choice should still be disclosed before staged content is sent through LLM-backed commands.
- The local provider choice lives in `okf/.openkb/config.yaml`, while the committed example file remains provider-agnostic.
- For OAuth providers like ChatGPT, the guidance explicitly says not to add keys or `api_base` settings just for consistency.
- The document also notes that OpenKB 0.4.x has no Claude-Code-style Anthropic OAuth flow, which makes ChatGPT a distinct subscription-based alternative rather than a key-based model path.
- In [[summaries/graphify-report]], ChatGPT also appears as one of the named external products surfaced by the repository's structural graph, reinforcing that provider selection is a recurring repository concern rather than a passing mention.

This makes ChatGPT relevant to [[concepts/provider-integration]], [[concepts/data-flow-disclosure]], [[concepts/configuration-precedence]], and [[concepts/explicit-provider-routing]].

## Operational significance

Within this documentation, ChatGPT matters less as a standalone product description and more as a concrete billing and routing option in a multi-provider setup. The guidance stresses that the active harness should not automatically determine which provider is used; when multiple options are viable, the user should be asked which provider they want to bill. It also places ChatGPT inside a configuration model where provider selection belongs in the local OpenKB config while credentials and other sensitive runtime details remain outside the repository's general orientation files.

The same guidance frames disclosure as an operational requirement: before the first LLM-backed add, recompile, lint, query, chat, skill, or deck command, the operator should disclose the tool, provider, model, endpoint, credential source, and what content will be sent. In that workflow, ChatGPT is one possible destination for staged repository content and therefore participates directly in the repository's data-flow and consent model.

The structural evidence in [[summaries/graphify-report]] adds that ChatGPT is not isolated in the knowledge base: it is part of a broader cluster of provider, workflow, and repository-governance material. That framing connects the product not only to runtime configuration, but also to the repository's emphasis on explicit routing, disclosure, and durable operational guidance.

That framing connects ChatGPT to [[concepts/tool-boundaries]], [[concepts/tooling-consent-and-pin-management]], and [[concepts/agent-context-layering]].

## Related pages

- [[entities/openkb]]
- [[entities/litellm]]
- [[entities/anthropic]]
- [[entities/github-copilot]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]