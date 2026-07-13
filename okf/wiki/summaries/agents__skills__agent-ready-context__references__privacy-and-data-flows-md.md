---
type: "Summary"
description: "Privacy and routing rules for keeping KB pipelines local or explicitly consented"
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"
---

# Summary

This document sets the privacy and data-flow rules for OpenKB and graphify pipelines, with a strong emphasis on transparency, explicit provider routing, and keeping fully local or air-gapped paths available.

## Key commitments

- Before any step that sends repository content off the machine, the agent must disclose the tool, provider or endpoint, model, credential source, and what content will be sent, then wait for consent.
- Provider selection must be explicit; tools must not silently auto-detect a backend.
- A fully local path and a zero-LLM fallback must always remain available.
- The pinned toolchain should not rely on telemetry, and claims should be re-verified whenever versions change.

## Data-flow map

The document breaks down what leaves the machine at each stage:

- Prereq checks, source packing, skeleton generation, and validators stay local.
- `graphify` on code files stays local because tree-sitter AST extraction runs on the machine.
- `graphify` on docs, PDFs, images, and video can send document content to the chosen LLM backend unless `--backend ollama` is used.
- OpenKB commands such as `add`, `recompile`, `lint`, `query`, `chat`, `skill`, and `deck` may send staged sources, wiki pages, and prompts to the configured litellm provider.
- Long PDFs use local PageIndex by default, but PageIndex Cloud is used if `PAGEINDEX_API_KEY` is set.
- `openkb add <url>` sends the URL and fetched page content during ingestion/compilation.
- External evidence gathered via web tools depends on the fetched site content.
- OKF spec baseline refresh touches only public GitHub content.

## Local-only and leakage risks

- Local caches and generated artifacts such as `graphify-out/cost.json`, `graphify-out/cache/`, `okf/output/`, and `okf/wiki/reports/` are intended to remain local and gitignored.
- A separate risk is local files accidentally entering committed graph artifacts, even without provider egress.
- The document warns that `graphify update` only respects `.gitignore` and `.graphifyignore`, not `.git/info/exclude` or global excludes, so a locally excluded file can still be scanned and end up in committed outputs.
- This is framed as a local-artifact leakage problem, not an LLM privacy problem.

## Staging rule for the KB root

A major rule is that staging must live inside the KB root, specifically under `okf/.okf-build/input/`.

- In OpenKB 0.4.4 and main, documents ingested from outside the KB root are recorded in `.openkb/hashes.json` with absolute machine paths.
- That leaks username and directory structure into committed metadata and causes unnecessary diff noise.
- The document says anything staged from outside the KB root should be re-staged inside and re-added, or the KB should be rebuilt if an old registry already contains absolute paths.

## Tool-specific privacy status

- `graphify` is described as having no telemetry, no usage tracking, and no analytics; video/audio transcription runs locally via faster-whisper.
- `openkb` is described as having no analytics, telemetry, or update checks; OpenAI Agents tracing is disabled at startup.
- `uv` is also documented as having no telemetry.
- The main remaining egress points are the configured LLM provider, optional PageIndex Cloud, URL ingestion, and browser-based feedback.

## Explicit backend rule for graphify

- `graphify` can auto-detect a provider from exported API keys, which is unsafe on machines with multiple keys.
- The document requires an explicit `--backend <provider>` whenever non-code sources are processed.
- For code-only repositories, code-only extraction is preferred because it needs no key and no content leaves the machine.
- The chosen backend must be announced before running.

## Secret handling and sourcing pattern

When graphify needs a key for semantic extraction of non-code sources:

- It reads only process environment variables, not `.env` files directly.
- The recommended pattern is to source `okf/.env` into the shell so secrets stay in a gitignored file and do not enter the agent context.
- The agent must not print, cat, or otherwise expose the file or variable values.
- The document also notes that the source-pack builder only stages tracked files, so an untracked gitignored `.env` cannot be ingested.

## Air-gapped mode and zero-LLM fallback

The document provides an air-gapped configuration using `model: ollama/<local-model>` and no API keys.

- URL ingestion and web baseline checks should be skipped.
- `graphify` should use `--backend ollama` for non-code sources.
- External docs should be provided as local files under `okf/.okf-build/input/external/`.
- A zero-LLM fallback exists via `build_okf_skeleton.py`, which writes a conservative bundle directly to `okf/wiki/` and can be reconciled later with OpenKB lint/recompile.

## Disclosure before first compile

Before the first LLM-backed OpenKB command or any graphify run over non-code sources, the agent must disclose:

- the tool;
- the provider;
- the model;
- the endpoint;
- the credential source;
- the content being sent.

The disclosure must be repeated whenever any of those change, and the chosen provider policy should be recorded in the target `AGENTS.md`.

## Main takeaway

This document is a policy reference for [[concepts/privacy-preserving-tooling]], [[concepts/data-flow-disclosure]], [[concepts/air-gapped-operation]], and [[concepts/provider-routing]]. It defines how to keep the pipeline transparent, local-first, and auditable, while avoiding both provider egress surprises and accidental leakage into committed artifacts.

## Related Concepts
- [[concepts/telemetry-auditing]]
- [[concepts/local-artifact-leakage]]
- [[concepts/consent-first-workflows]]
- [[concepts/offline-first-workflows]]
- [[concepts/toolchain-pinning]]
- [[concepts/non-interactive-agent-design]]
- [[concepts/prompt-injection-defense]]

## Entities
- [[entities/pageindex-api-key]]
- [[entities/openkb-feedback]]
- [[entities/git-info-exclude]]
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/openkb]]
- [[entities/openkb-cli]]
- [[entities/pageindex]]
- [[entities/pageindex-cloud]]
- [[entities/litellm]]
- [[entities/ollama]]
- [[entities/uv]]
- [[entities/gitignore]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/build_okf_source_pack-py]]
- [[entities/build_okf_skeleton-py]]
- [[entities/validate_okf_bundle-py]]
