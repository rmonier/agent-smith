---
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "Local LLM app used as an optional offline provider for agent-smith."
---

# LM Studio

LM Studio is a local LLM application used as an optional offline provider in the agent-smith workflow.

## Role in the document

The README describes LM Studio as one of the local runtimes that can support air-gapped operation. In that mode, the agent keeps repository content on the machine, explains the resulting data flow, and can route LLM-backed work through an explicitly selected local provider when one is available. If no local LLM is available, the workflow can still fall back to a deterministic zero-LLM skeleton.

## Key facts

- It is treated as a local model-serving option rather than a source of repository truth.
- It supports the repository's [[concepts/air-gapped-operation]] and [[concepts/local-by-default-tooling]] posture.
- It fits into the repository's [[concepts/explicit-provider-routing]] model, where the active provider is chosen deliberately instead of being auto-detected.
- It is one of the local-provider examples mentioned in the README's discussion of offline workflows.
- It participates in the README's broader privacy model, where data-flow disclosure and optional local routing are emphasized before any LLM-backed work.

## Related pages

- [[summaries/README-md]]
- [[concepts/air-gapped-operation]]
- [[concepts/explicit-provider-routing]]
- [[concepts/local-by-default-tooling]]
- [[concepts/provider-integration]]
- [[concepts/privacy-preserving-tooling]]
- [[entities/openkb]]