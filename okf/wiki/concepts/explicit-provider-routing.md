---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
description: "Routing rules that require explicit backend and data-flow disclosure."
---

# Explicit Provider Routing

Explicit provider routing means an agent must name the exact backend, endpoint, model, and credential source before any tool sends content off the machine. The goal is to prevent silent defaults, make consent meaningful, and keep privacy posture stable across machines and runs.

## Core idea

Some tools can infer a provider from whatever API keys happen to be present in the environment. That is convenient, but risky: the same command can route content to a service the user did not choose. Explicit routing removes that ambiguity by requiring the agent to declare the destination up front and to repeat that disclosure whenever the route changes.

This concept is central to [[concepts/privacy-preserving-tooling]], [[concepts/consent-first-tooling]], and [[concepts/data-flow-disclosure]]. It also supports [[concepts/tool-boundaries]] by making routing decisions part of the command contract rather than an implementation detail.

The README for `agent-smith` extends that idea into a broader repository transformation workflow: routing is part of a larger split between orientation (`AGENTS.md`), durable context (`okf/wiki/`), and actions (`.agents/skills/`). In that model, provider choice is not just a local tool setting; it is part of how the repository is made [[concepts/agent-ready-repositories|agent-ready]] without hiding where knowledge or content will go.

## What the source document requires

The referenced policy document, [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], states that:

- OpenKB must use explicit litellm configuration rather than silent provider selection.
- graphify must receive an explicit `--backend` for non-code sources.
- The chosen backend, model, endpoint, and credential source must be announced before execution.
- Auto-detection from exported keys is not acceptable for privacy-sensitive workflows.
- A fully local air-gapped path and a zero-LLM fallback must always remain available.
- Staging must stay inside the KB root so registry metadata does not leak absolute machine paths.

The README adds a related operational rule: when the active harness does not support a safe local install or local provider, the agent should stop with a precise manual fallback rather than silently changing route. That keeps provider choice aligned with [[concepts/consent-first-installation]], [[concepts/local-by-default-tooling]], and [[concepts/graceful-degradation]].

In practice, this means the agent should never rely on implicit provider discovery when documents, PDFs, images, videos, or other non-code sources are involved. For code-only extraction, local AST-based processing remains the preferred no-egress path.

## Why it matters

Explicit provider routing protects against several failure modes:

- accidental transmission to the wrong vendor
- inconsistent behavior across machines with different environment variables
- hidden changes in privacy posture when keys are added or removed
- unclear consent boundaries for repository content
- path leakage when staged content is built outside the KB root

It also improves reproducibility. When the provider, endpoint, model, and credential source are part of the declared workflow, the same inputs are more likely to produce the same compilation path, which reinforces [[concepts/deterministic-builds]] and [[concepts/tooling-consent-and-pin-management]].

In the broader agent-smith design, this also supports the README's [[concepts/context-surface-management|context surface management]] and [[concepts/progressive-disclosure|progressive disclosure]] goals: keep routing transparent, keep context durable, and keep actions narrowly scoped.

## Related operational patterns

Explicit routing works alongside other control points:

- [[concepts/air-gapped-operation]] keeps a local-only path available.
- [[concepts/offline-first-workflows]] reduces reliance on remote services.
- [[concepts/configuration-precedence]] clarifies which settings win when multiple sources exist.
- [[concepts/source-trust-levels]] helps decide whether a source is safe to route externally.
- [[concepts/provider-integration]] describes how providers are wired into the toolchain.
- [[concepts/agent-ready-context-skill]] covers the repository bootstrap workflow where routing disclosure is enforced during knowledge compilation.

## Practical rule

When a tool may use an LLM or remote backend, state the route explicitly before running it. If the route is not known or not approved, stop and ask rather than allowing the tool to choose on its own. For privacy-sensitive commands, include the tool, provider or endpoint, model, credential source, and what content will be sent.

In an agent-ready repository, this rule applies across the whole transformation pipeline: the agent should disclose how repository content is staged, whether processing is local or remote, and what fallback exists if the preferred route is unavailable.

## Source context

This concept is grounded in the privacy and data flow guidance in [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], which treats routing transparency as a hard requirement rather than a preference. The same source also establishes the local-only and zero-LLM fallback rule, plus the requirement to keep staging inside the KB root to avoid registry leakage.

The README reinforces that posture by presenting explicit routing as part of the repository's operating model: portable skills, pinned toolchains, consent-first installs, and harness-aware adapters are all designed so the agent's execution path is visible rather than inferred.

## Related Documents
- [[summaries/README-md]]
