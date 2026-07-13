---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
description: "Explicitly tells users what data will move, where, and under whose control."
---

# Data Flow Disclosure

Data flow disclosure is the practice of explicitly telling the user what tool, provider, model, backend, credential source, and content scope will be involved before any LLM-backed or data-moving action begins. It is a [[concepts/consent-first-workflows]] pattern that supports [[concepts/privacy-preserving-tooling]], [[concepts/safe-automation]], [[concepts/durable-context]], and broader governance around provenance and source trust.

In repository transformation workflows, disclosure is not a formality: it is what keeps deterministic staging, local-only execution, and provider-backed compilation visibly separate. The README for `agent-smith` makes that separation explicit by splitting the repository into three operational surfaces: `AGENTS.md` for orientation, `okf/wiki/` for durable knowledge, and `.agents/skills/` for actions. Data flow disclosure is the mechanism that tells the user which of those surfaces is being touched, when content is being staged, and when a step crosses into model-backed work.

## Why it matters

When an agent stages content for a model, indexes a repository, routes data to an external backend, initializes a knowledge workflow, or refreshes an agent-ready repository, the user needs to know:

- which tool will run,
- which provider or model will receive the content,
- whether the request uses local or remote infrastructure,
- where credentials are expected to come from,
- what content scope is about to be sent,
- and whether the action is still in a deterministic staging phase or has crossed into LLM-backed compilation.

That disclosure reduces surprise, supports [[concepts/consent-first-tooling]], and aligns with [[concepts/provenance-tracking]] and source trust rules. In the OpenKB workflow, this becomes especially important because the pipeline separates repository inspection, source-pack staging, knowledge-base initialization, ingestion, linting, and validation into distinct steps, and the first LLM-backed command must be preceded by an explicit notice.

The README extends the same idea into a repository-level architecture: orientation lives in `AGENTS.md`, durable knowledge lives in `okf/wiki/`, actions live in `.agents/skills/`, and harness adapters remain runtime-only projections. Disclosing data flow is what keeps those layers distinct and makes progressive disclosure workable in practice.

## Core practices

- State the tool, provider, and model before the first add, compile, lint, query, chat, skill, or deck command.
- Name the backend or execution mode when the request leaves the local machine or switches away from a local-only path.
- Identify the credential source by location or variable name, without exposing secret values.
- Describe the content class being sent, such as a single file, staged source pack, evidence bundle, wiki bundle, or indexed repository.
- Distinguish deterministic staging from ingestion or generation so the user can see when the workflow becomes provider-backed.
- Keep the disclosure concise but complete enough for the user to understand the data path.

In `agent-smith`'s repository transformation flow, this also means disclosing whether the task is operating on repository sources, on compiled wiki output, or on both. The README explicitly treats fetched web content and wiki pages as evidence rather than instructions, so the disclosure should make that boundary visible whenever such material is being routed onward.

## Source-specific details

In [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]], the disclosure rule is tied to OpenKB configuration and provider selection:

- OpenKB uses LiteLLM model names in `okf/.openkb/config.yaml`.
- The active provider may be Anthropic, ChatGPT, GitHub Copilot, an OpenAI-compatible gateway, Ollama, or a zero-LLM fallback.
- Credentials are resolved in a fixed order: process environment, `okf/.env`, then `~/.config/openkb/.env`.
- The agent must not read, print, validate, or move secret values.
- Before the first LLM-backed command, the user must be told the tool, provider, model, endpoint, credential source, and what content will be sent.

The README adds that this disclosure also applies when the repository is being made agent-ready or refreshed. The `agent-ready-context` skill checks prerequisites, explains missing dependencies before installation, and only then proceeds into OpenKB and graph-based work. It also states that in air-gapped operation the agent should explain the resulting data flow and route through a local provider such as Ollama when available, or else fall back to a deterministic zero-LLM skeleton. In other words, disclosure covers not just provider choice, but also whether the workflow is local, remote, or degraded.

## Related boundaries

Data flow disclosure is especially important where a local tool can switch between local and remote execution paths. That includes cases covered by [[concepts/local-vs-shared-configuration]], [[concepts/harness-vs-local-tools]], [[concepts/explicit-provider-routing]], and [[concepts/knowledge-capture-boundaries]]. It also supports [[concepts/knowledge-base-navigation]] and [[concepts/wiki-context-routing]] by clarifying when the system is reading local material, staging it for later use, or transmitting it to a provider.

It also connects to the workflow's self-reference policy: the KB root stays out of the graph, so the user should know when analysis is happening against repository sources versus against compiled wiki output. That boundary keeps data movement transparent and avoids confusing source evidence with generated knowledge.

The repository-level architecture in the README reinforces the same boundary by splitting orientation, context, and actions into separate surfaces. That separation depends on users understanding which surface is being touched at each step, especially when a skill is about to create, revise, or validate compiled knowledge.

## Practical shape

A good disclosure usually answers four questions:

1. What action is about to happen?
2. Which provider or runtime will handle it?
3. Where will the model credentials come from?
4. What data will be transmitted or staged?

If those four are answered up front, the user can decide whether to proceed without guessing about hidden data movement. In this workflow, that also means stating when the system is only building deterministic input, when it is initializing OpenKB, and when it is sending content to an LLM-backed step.

The strongest disclosures make the transition points explicit: repository inspection, source staging, knowledge compilation, and validation are safe to describe as deterministic steps, while provider-backed ingestion, generation, or indexing should always name the external path involved.

## Related Documents
- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]