---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
type: "Product"
description: "The OpenKB feedback channel used to send browser feedback to the team."
---

# OpenKB Feedback

OpenKB Feedback is the user-facing feedback channel in the OpenKB workflow. The document describes it as one of the few remaining network egress paths in the toolchain: when a user submits feedback through `openkb feedback`, the browser connects to the feedback destination and sends the user's input there.

## Key facts

- It is part of the OpenKB toolchain, alongside commands such as `add`, `recompile`, `lint`, `query`, `chat`, `skill`, and `deck`.
- Unlike most local-only stages, feedback is not purely local; the document treats it as a browser-mediated external destination.
- It is mentioned as one of the places where privacy and disclosure rules matter, because user content may leave the machine.
- The document frames it as a permitted egress path, but still subject to the same transparency expectations as other networked operations.

## Related concepts

- [[concepts/privacy-preserving-tooling]]
- [[concepts/data-flow-disclosure]]
- [[concepts/consent-first-tooling]]
- [[concepts/provider-routing]]
- [[concepts/local-by-default-tooling]]
- [[concepts/tool-boundaries]]
- [[concepts/air-gapped-operation]]
- [[concepts/explicit-provider-routing]]

## Related entities

- [[entities/openkb]]
- [[entities/openkb-cli]]
- [[entities/openkb-feedback]]
- [[entities/references-privacy-and-data-flows-md]]

## Source context

This page is grounded in [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], which documents OpenKB's privacy commitments, local-first defaults, and the specific network paths that remain available.