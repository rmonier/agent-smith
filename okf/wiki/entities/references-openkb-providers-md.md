---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
type: "Work"
description: "Repository guidance for OpenKB provider selection and configuration"
---

# OpenKB Providers

`references/openkb-providers.md` is a repository guidance document that defines how OpenKB should be configured for provider selection, model routing, and language settings when initializing or running the OKF workflow.

## Purpose

This document exists to keep OpenKB compilation reproducible and explicit about where model calls go. It is part of the repository's broader [[concepts/explicit-provider-routing]] and [[concepts/provider-integration]] practices.

## What It Covers

The skill source identifies this document as the place to read before running OpenKB compilation. It is referenced for:

- provider and model configuration
- language selection during `openkb init`
- credential handling and verification
- local versus shared configuration behavior

It also serves as a companion reference to the repo's OpenKB bootstrap and validation flow.

## Role in the Agent-Ready Workflow

The document is used when initializing or refreshing the OpenKB KB under `okf/`. It helps ensure that the agent follows the right provider setup before any LLM-backed command is run.

Relevant ideas include:

- [[concepts/consent-first-tooling]] for installing and adopting OpenKB-related tooling
- [[concepts/data-flow-disclosure]] before any step that sends content off the machine
- [[concepts/privacy-preserving-tooling]] for handling credentials and provider choice safely
- [[concepts/toolchain-pinning]] and [[concepts/version-pinning]] for reproducible setup

## Related Pages

- [[entities/openkb]]
- [[entities/openkb-cli]]
- [[entities/okf-wiki]]
- [[entities/references-openkb-lifecycle-md]]
- [[entities/references-privacy-and-data-flows-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
