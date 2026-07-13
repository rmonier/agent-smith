---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
description: "Rules for choosing explicit LLM backends without silent auto-routing."
---

# Provider Routing

Provider routing is the practice of choosing an LLM backend explicitly, rather than letting tools silently auto-detect a provider from available credentials or environment state. In this wiki, it is a core part of [[concepts/consent-first-workflows]], [[concepts/privacy-preserving-tooling]], and [[concepts/explicit-provider-routing]].

## Why it matters

Routing decisions affect both privacy and reproducibility. If a tool picks a backend implicitly, the user may not know where repository content is being sent, which model is being used, or what credential source is authorizing the request. Explicit routing keeps the workflow transparent and makes it possible to preserve a local-only path alongside hosted providers.

## What the source document requires

The referenced policy document makes provider routing a hard requirement for the OpenKB and graphify pipeline:

- Tools must announce the tool, provider or endpoint, model, credential source, and content being sent before any off-machine transfer.
- A tool must not silently choose a provider.
- OpenKB uses explicit litellm configuration.
- graphify requires an explicit `--backend` for non-code sources.
- A fully local path must remain available, including `ollama`-backed execution and zero-LLM fallback modes.

This means routing is not just a configuration preference; it is part of the consent and disclosure model described in [[concepts/data-flow-disclosure]] and [[concepts/air-gapped-operation]].

## Practical rules

- Use explicit backend selection whenever content may leave the machine.
- Prefer local-only extraction for code repositories, since it avoids provider routing entirely.
- Avoid relying on auto-detected keys or ambient environment state to choose a backend.
- Re-state the routing choice whenever the provider, model, endpoint, or credential source changes.
- Record the chosen policy in the relevant `AGENTS.md` so future runs follow the same path.

## Related risks and safeguards

Provider routing is closely tied to several other governance concerns:

- [[concepts/local-by-default-tooling]]: local execution should be the default where possible.
- [[concepts/consent-first-tooling]]: users should approve any off-machine transfer before it happens.
- [[concepts/tooling-consent-and-pin-management]]: pinned toolchains should be reviewed when routing behavior may change.
- [[concepts/telemetry-auditing]]: routing assumptions should be checked against upstream claims about telemetry and network behavior.
- [[concepts/air-gapped-operation]]: local routing policies must still support a fully disconnected mode.

## Summary

Provider routing is the discipline of making backend choice explicit, visible, and repeatable. It prevents silent escalation to a remote provider, supports local-first and air-gapped workflows, and gives users the information they need to consent to any content leaving their machine.

See also [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]].