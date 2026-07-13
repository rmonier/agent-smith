---
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "GitHub Copilot is an OAuth-style OpenKB provider option."
---

# GitHub Copilot

GitHub Copilot is a subscription-backed provider option for [[entities/openkb]] that routes through [[entities/litellm]] using `github_copilot/*` model names. In [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]], it is treated as an OAuth-style choice rather than a simple API-key provider, and it requires explicit header-based setup. That makes it part of OpenKB's broader provider-selection and configuration architecture rather than an isolated convenience setting.

## Role in OpenKB configuration

In the OpenKB provider guidance, GitHub Copilot appears as one of several valid provider paths to consider when configuring `okf/.openkb/config.yaml`.

- Use a `github_copilot/*` model name when selecting this provider.
- This option is framed as suitable for a GitHub Copilot subscription.
- Provider choice should follow the documented selection order and still require explicit user confirmation rather than assuming the active harness is the billing target.
- The committed home for the provider choice is `okf/.openkb/config.yaml`; provider details should not be duplicated into orientation files such as `AGENTS.md`, which aligns with [[concepts/single-source-of-truth]].
- The provider guidance places GitHub Copilot alongside other explicit provider-routing options, reinforcing its role within [[concepts/provider-integration]].
- The config remains user-specific and uncommitted, which fits [[concepts/local-vs-shared-configuration]] and [[concepts/explicit-provider-routing]].
- The guidance also notes that OpenKB 0.4.4 has no Claude-Code-style Anthropic OAuth flow; by contrast, GitHub Copilot remains an OAuth subscription provider with LiteLLM-based configuration.

## Required configuration details

GitHub Copilot requires extra LiteLLM header configuration rather than a basic key-only setup:

- `Editor-Version`
- `Copilot-Integration-Id`

These headers are configured under `litellm.extra_headers`. This makes GitHub Copilot distinct from key-based provider modes and places it within broader concerns around [[concepts/configuration-precedence]] and [[concepts/tool-boundaries]]. The page is also tied to the repository's general guidance that provider settings live in the local OpenKB config and should not be copied into shared documentation.

## Disclosure and workflow context

When GitHub Copilot is the chosen provider, the operator should disclose the tool, provider, model, endpoint, credential source, and what staged content will be sent before the first LLM-backed OpenKB command. That expectation aligns this entity with [[concepts/data-flow-disclosure]] and [[concepts/privacy-preserving-tooling]].

The source also recommends validating configuration with low-risk checks such as `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list` before broader ingestion, followed by a small single-file add test. This places GitHub Copilot inside the same cautious workflow used for other [[entities/openkb]] provider options and supports [[concepts/read-only-kb-operations]] and [[concepts/baseline-first-testing]].

## Related pages

- [[entities/openkb]]
- [[entities/litellm]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__openkb__SKILL-md]]
- [[concepts/provider-integration]]
- [[concepts/explicit-provider-routing]]
- [[concepts/data-flow-disclosure]]
- [[concepts/configuration-precedence]]
- [[concepts/single-source-of-truth]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/read-only-kb-operations]]
- [[concepts/baseline-first-testing]]