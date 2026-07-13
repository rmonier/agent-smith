---
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "Local LLM runtime for explicit, offline provider routing"
---

# Ollama

Ollama is a local large language model runtime used as an offline provider for agent tooling.

## Why it matters here

In `README.md` and the OpenKB privacy guidance, Ollama is the named local provider for air-gapped operation when the repository is made agent-ready without sending content off the machine. It supports [[concepts/air-gapped-operation]], [[concepts/local-by-default-tooling]], [[concepts/offline-first-workflows]], and [[concepts/privacy-preserving-tooling]] by keeping LLM-backed work local when possible.

It also serves as the explicit fallback backend for graphify when non-code sources are processed in a local-only path, and it is part of the zero-LLM or no-network strategy described for KB compilation workflows.

## Key facts from the documents

- Ollama is named as the local runtime option for agent workflows and air-gapped configuration.
- It can be selected explicitly as `ollama/<model>` for OpenKB and as `--backend ollama` for graphify on non-code sources.
- The privacy guidance treats it as the local path that avoids provider egress when remote LLMs are not desired or available.
- Its use is tied to explicit disclosure and consent-first operation, aligning with [[concepts/data-flow-disclosure]], [[concepts/explicit-provider-routing]], and [[concepts/consent-first-workflows]].
- The document positions it as a practical choice for running repository processing without network egress, while preserving a fully local and air-gapped route.

## Related pages

- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[concepts/air-gapped-operation]]
- [[concepts/explicit-provider-routing]]
- [[concepts/provider-integration]]
- [[concepts/offline-first-workflows]]
- [[concepts/local-by-default-tooling]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/data-flow-disclosure]]
- [[concepts/consent-first-workflows]]