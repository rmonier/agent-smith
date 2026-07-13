---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
description: "Local-first repository operation that preserves control, privacy, and resilience."
---

# Air-Gapped Operation

Air-gapped operation is a local-first workflow in which repository content, documents, and credentials stay on the machine unless the user explicitly approves an external step. In the agent-smith model, it is part of how an [[concepts/agent-ready-repositories]] stays usable in restricted environments while still supporting durable context, repeatable actions, and validated knowledge compilation.

The README makes this boundary concrete by splitting the repository transformation model into three surfaces: `AGENTS.md` for orientation, `okf/wiki/` for durable knowledge, and `.agents/skills/` for actions. Air-gapped operation is the constraint that keeps those surfaces useful even when networked processing is unavailable or disallowed.

## Core idea

The goal is to make offline use the default and networked processing the exception. That means the pipeline must support:

- a fully local execution path,
- a zero-LLM fallback for degraded environments,
- explicit consent before any content leaves the machine,
- and clear routing to a chosen backend when networked processing is unavoidable.

This is closely related to [[concepts/privacy-preserving-tooling]], [[concepts/consent-first-tooling]], [[concepts/explicit-provider-routing]], [[concepts/offline-first-workflows]], [[concepts/progressive-disclosure]], and [[concepts/agent-context-layering]]. It also fits the broader agent-ready model described in the README, where orientation lives in `AGENTS.md`, durable knowledge lives in `okf/wiki/`, and actions live in `.agents/skills/`.

The README also frames air-gapped operation as part of a broader [[concepts/knowledge-compilation-pipeline]] built around [[concepts/llm-wiki]] and [[concepts/compiled-knowledge-bases]]. The point is not just to stay offline, but to keep knowledge compilation, validation, and repository readiness functioning without assuming a networked provider.

## Key rules

- Do not set provider API keys when running in air-gapped mode.
- Avoid URL ingestion and web evidence checks, since they require network fetches.
- Use local document handling for PDFs and other sources whenever possible.
- Prefer local backends such as `ollama` when non-code sources must be processed.
- Keep staging files inside the KB root so builds remain relocatable and do not leak machine-specific paths.
- Preserve a zero-LLM fallback so the pipeline can still produce a conservative knowledge bundle when external services are unavailable.
- Re-check privacy and telemetry claims whenever a pinned tool version changes.
- Treat the generated wiki and vendored tool copies as supporting surfaces, not the product itself; the distributable product is the trio of portable skills.

## What the source document establishes

The README treats air-gapped operation as one execution mode of the repository transformation pipeline. That pipeline still needs to bootstrap orientation, compile durable context, and validate outputs even when no networked provider is available.

It also distinguishes the product from supporting artifacts. The product is the three portable skills: `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter`. Generated wiki content and vendored tool copies are supporting surfaces that help those skills operate, but they are not the core deliverable.

The source document divides the workflow into local-only stages and networked stages, and identifies the exact places where data can leave the machine.

Local-only stages include prereq checks, source packing, skeleton generation, and validators. For code repositories, `graphify` uses local tree-sitter parsing and keeps content on-device. For non-code sources such as docs, PDFs, images, and video, `graphify` may send content to the selected backend unless `--backend ollama` is used.

OpenKB commands such as `add`, `recompile`, `lint`, `query`, `chat`, `skill`, and `deck` may send staged sources, wiki pages, and prompts to the configured litellm provider. Long PDFs can remain local through PageIndex unless `PAGEINDEX_API_KEY` enables PageIndex Cloud. `openkb add <url>` fetches remote content from the target URL, so it is not an air-gapped action. External documentation evidence gathered through web tools also breaks the air-gapped boundary.

The README also distinguishes sensitive from non-sensitive external fetches: refreshes of the public OKF spec baseline are treated as non-sensitive because they read only public material.

## Data-flow implications

Air-gapped operation is not just about turning things off; it is about making data boundaries predictable.

The document emphasizes:

- preflight disclosure before any LLM-backed command,
- explicit backend selection rather than auto-detection,
- local-only handling for code extraction,
- and no hidden telemetry assumptions.

It also adds a crucial staging rule: all KB staging must live inside `okf/.okf-build/input/`, never outside it. When files are staged from outside the KB root, registry metadata can capture absolute machine paths, which leaks usernames and directory structure into committed files and creates avoidable diff noise. The preferred remediation is to re-stage inside the KB root or rebuild the KB, not to hand-edit the registry casually.

The source document further notes that cost and cache artifacts such as `graphify-out/cost.json`, `graphify-out/cache/`, `okf/output/`, and `okf/wiki/reports/` should remain local-only and gitignored.

These constraints connect directly to [[concepts/data-flow-disclosure]], [[concepts/tool-boundaries]], [[concepts/tooling-consent-and-pin-management]], [[concepts/telemetry-auditing]], [[concepts/kb-root-staging]], and [[concepts/path-safety]]. They also align with [[concepts/deterministic-validation]] and [[concepts/deterministic-builds]] because predictable offline behavior depends on reproducible inputs and known execution paths.

## Telemetry and routing posture

The source document records a version-sensitive verification of the toolchain:

- `graphify` claims no telemetry, no usage tracking, and no analytics, with transcription running locally.
- `openkb` is verified as having no analytics, telemetry, or update checks, with tracing disabled at startup.
- `uv` has no telemetry per upstream documentation.

That means there is nothing to disable for OpenKB telemetry itself. Instead, the privacy-relevant controls are operational: leave `PAGEINDEX_API_KEY` unset for local-only PDF handling, avoid `openkb add <url>` unless the user approves the URL fetch, and keep routing explicit.

The document warns that `graphify` can auto-detect a provider from exported API keys. On a developer machine with multiple keys, that can silently route documents to an unintended backend. For that reason, non-code sources must always pass `--backend <provider>`, while code-only repositories should use code-only extraction with no key at all.

When graphify does need a key, the document recommends sourcing it from a gitignored file through the shell so the secret persists locally and never crosses the agent context. It also notes two structural safeguards: `build_okf_source_pack.py` only stages `git ls-files` output, and graphify treats `.env` files as secret stores to exclude from extraction.

## Air-gapped recipe

A concrete local-only configuration is given for `okf/.openkb/config.yaml`:

```yaml
model: ollama/<local-model>
language: en
litellm:
  timeout: 1200
  drop_params: true
```

In this mode:

- do not set `LLM_API_KEY`, provider-specific API keys, or `PAGEINDEX_API_KEY`;
- skip URL ingestion and web baseline checks;
- run graphify with `--backend ollama` when non-code sources are processed;
- let the user provide external documents as local files under `okf/.okf-build/input/external/`.

The zero-LLM fallback is `build_okf_skeleton.py`, which can write a conservative bundle directly to `okf/wiki/`. That mode is intentionally degraded, so the limitation should be reported and later reconciled with OpenKB `lint` or `recompile` if OpenKB is adopted.

## Disclosure rule

Before the first OpenKB LLM-backed command (`add`, `recompile`, `lint`, `query`, `chat`, `skill`, or `deck`) or any graphify run over non-code sources, the agent must disclose in one short block:

- tool,
- provider,
- model,
- endpoint,
- credential source,
- and what content is being sent.

The document says this disclosure must be repeated whenever any of those change, and the chosen provider policy should be recorded in the target `AGENTS.md` so future agents follow the same routing.

## Why it matters

Air-gapped operation protects against accidental exfiltration, provider ambiguity, and environment-specific leakage. It also keeps the workflow usable for restricted networks, sensitive repositories, and users who need strong guarantees that nothing leaves the machine without a deliberate decision.

In the README’s model, this matters because the repository is meant to be agent-ready without becoming network-dependent: agents can still bootstrap orientation, durable context, and actions while respecting local-only constraints. The source page that defines these rules is [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]].

## Related concepts

- [[concepts/privacy-preserving-tooling]]
- [[concepts/consent-first-tooling]]
- [[concepts/explicit-provider-routing]]
- [[concepts/offline-first-workflows]]
- [[concepts/graceful-degradation]]
- [[concepts/data-flow-disclosure]]
- [[concepts/tool-boundaries]]
- [[concepts/agent-ready-repositories]]
- [[concepts/kb-root-staging]]
- [[concepts/path-safety]]

## Related Documents

- [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
