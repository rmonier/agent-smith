---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
description: "Tooling that minimizes unintended data exposure through explicit, local, auditable flows."
---

# Privacy-Preserving Tooling

Privacy-preserving tooling is an approach to building and operating agent workflows so repository content, documents, prompts, credentials, and runtime signals stay under user control unless disclosure and consent are explicit. It emphasizes local-first execution, transparent routing, deterministic build paths, careful handling of any step that could move data off the machine, and a local-only fallback that remains available even when networked tooling exists.

## Core ideas

- **Consent-first disclosure**: before any step that sends content off-machine, the agent should announce the tool, provider or endpoint, model, credential source, and the exact content to be sent.
- **Explicit provider routing**: tooling should not silently choose a backend from environment state or defaults; the chosen provider must be stated directly.
- **Local-first operation**: a fully local path should always exist, including air-gapped operation and zero-LLM fallback modes.
- **Telemetry skepticism**: claims about no telemetry or no analytics should be treated as version-specific and re-verified when tool pins change.
- **Context separation**: documentation should keep orientation, durable knowledge, and actions in separate surfaces so operational instructions do not absorb explanatory context.
- **Consent-aware packaging**: setup instructions should distinguish the repository's portable product from vendored toolchain copies so contributors do not accidentally propagate implementation details.
- **Non-invasive runtime detection**: environment inspection should rely on existing process, repository, and configuration hints rather than executing vendor CLIs to probe the active harness.

## Data-flow controls

Privacy-preserving workflows distinguish between local-only stages and stages that may transmit data.

- Local-only stages include prerequisite checks, source packing, skeleton generation, and validators.
- Code-only extraction can remain local when the tooling uses AST-based processing.
- Non-code processing may require an LLM backend, so the backend must be chosen explicitly and disclosed first.
- URL ingestion, web evidence gathering, and hosted PDF services are treated as optional egress points, not defaults.
- Repository transformation should keep knowledge compilation incremental, so updates can be staged and validated without regenerating the entire bundle unnecessarily.
- Staging should stay inside the KB root to avoid leaking absolute machine paths into registries or build artifacts.
- Generated caches and reports should remain local and gitignored when they might reveal environment details.
- Runtime inspection should prefer passive signals such as explicit environment keys, parent-process chains, and repo markers, while treating installed binaries as insufficient proof of the active harness.

## Repository safety

A key privacy boundary is the KB root. Staging content inside the KB root avoids leaking absolute machine paths into registries and reduces cross-developer noise. The same principle applies to any source bundle, manifest, or build artifact: keep generated and cached files local and gitignored when they may reveal environment details.

This aligns with [[concepts/kb-root-staging]], [[concepts/path-safety]], [[concepts/source-provenance]], and [[concepts/registry-drift]].

The repository's documentation split also reinforces a stricter separation of surfaces: `AGENTS.md` holds orientation, `okf/wiki/` holds durable knowledge, and `.agents/skills/` holds repeatable actions. That split supports privacy by limiting where context is stored, reducing accidental duplication, and making it clearer which files are source truth versus runtime projections.

## Tooling rules from the source document

The source document for this concept, [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], sets out several concrete operating rules:

- Announce disclosures before any OpenKB or graphify action that could send content externally.
- Use explicit backend selection for graphify, especially for non-code sources.
- Keep an air-gapped recipe available using local models and no API keys.
- Leave `PAGEINDEX_API_KEY` unset unless cloud processing is intentionally accepted.
- Avoid `openkb add <url>` unless the user has approved fetching remote content.
- Preserve a zero-LLM fallback so the knowledge base can still be created or repaired offline.
- Re-check telemetry and egress claims whenever pinned tool versions change.
- Record the chosen provider policy in the target `AGENTS.md` so future agents follow the same routing.
- Inspect runtime context with passive heuristics, including explicit environment variables, environment hints, parent-process metadata, and repository markers, rather than probing the harness by executing vendor commands.

## Why it matters

Privacy-preserving tooling reduces accidental leaks, makes data movement auditable, and prevents hidden routing decisions from violating user expectations. It is especially important in agent workflows, where automation can otherwise turn implicit defaults into unintended disclosure.

It also improves trust in [[concepts/consent-first-tooling]], supports [[concepts/offline-first-workflows]], and reinforces [[concepts/tool-boundaries]] and [[concepts/data-flow-disclosure]]. In the agent-smith model, it also helps preserve the distinction between durable knowledge and the repository's portable skills, which is a core part of [[concepts/agent-ready-repositories]].

## Related concepts

- [[concepts/consent-first-tooling]]
- [[concepts/data-flow-disclosure]]
- [[concepts/explicit-provider-routing]]
- [[concepts/air-gapped-operation]]
- [[concepts/offline-first-workflows]]
- [[concepts/tool-boundaries]]
- [[concepts/kb-root-staging]]
- [[concepts/path-safety]]
- [[concepts/telemetry-auditing]]
- [[concepts/context-action-separation]]
- [[concepts/progressive-disclosure]]
- [[concepts/local-by-default-tooling]]
- [[concepts/agent-ready-repositories]]
- [[concepts/non-invasive-detection]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
- [[summaries/README-md]]