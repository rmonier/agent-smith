---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
type: "Work"
description: "Reference on privacy and data flow rules for the agent-ready workflow."
---

# Privacy and Data Flows

`references/privacy-and-data-flows.md` defines the privacy and data handling rules for the agent-ready repository workflow.

## Purpose

The document explains how repository content may move off the machine, which tools may receive it, and what must stay local. It is part of the policy surface for [[concepts/consent-first-tooling]], [[concepts/data-flow-disclosure]], and [[concepts/privacy-preserving-tooling]].

## Main Rules

- Treat repository content as sensitive by default and only send it to approved providers.
- Disclose data flows before any LLM-backed step that may transmit content externally.
- Keep provider credentials in shell environment variables or gitignored `.env` files.
- Never read, print, validate, or write secret values; only refer to variable names and file locations.
- Do not block agentification just because a credential is missing.

## Role in the Workflow

This reference is used before steps that may involve external services or model routing, especially during OpenKB compilation and validation. It supports [[concepts/explicit-provider-routing]] and [[concepts/provider-integration]] by making privacy expectations explicit.

## Related Pages

- [[concepts/agent-ready-context]]
- [[concepts/provenance-tracking]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/toolchain-pinning]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
