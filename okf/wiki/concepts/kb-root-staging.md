---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Staging OpenKB inputs inside the KB root to preserve portability and privacy."
---

# KB Root Staging

KB root staging is the practice of keeping staged OpenKB inputs inside the KB root, typically under `okf/`, so ingestion, registry paths, and generated wiki artifacts remain portable, predictable, and easier to reconcile. It also defines a privacy boundary: when staging stays inside the KB root, the registry can keep KB-relative paths; when staging happens outside it, OpenKB may record absolute machine paths and leak local directory details into committed metadata.

It is a core part of the OpenKB lifecycle described in the openkb lifecycle reference, where the KB root serves as the durable boundary for source staging, generated output, and controlled disclosure to tools.

## Why it matters

Staging inside the KB root reduces path leakage in the registry, because OpenKB records KB-relative paths for content staged within `okf/` but may record absolute host paths for content staged outside it. That difference matters for privacy, reproducibility, and portability.

It also supports hash registry coherence and registry drift prevention by keeping staged inputs, registry entries, and compiled wiki pages aligned as one managed unit. The privacy-and-data-flows guidance makes this a hard rule: staging must live inside `okf/.okf-build/input/`, never outside, and any stray outside-stage registry entry should be corrected by re-staging inside the KB root or rebuilding the KB.

The same boundary also simplifies consent-first tooling and data-flow disclosure, because the sendable input set is bounded and inspectable before any LLM-backed command or external transfer.

## How it works

The lifecycle and privacy guidance recommend:

- creating or using the KB root at `okf/`
- staging deterministic inputs under `okf/.okf-build/input/`
- rebuilding the staged pack before `openkb add`
- ingesting only the staged path or explicitly approved external material
- keeping `okf/raw/` and `okf/wiki/` under OpenKB control rather than editing them directly
- ensuring `--out` and `openkb add` never point at a staging directory outside `okf/`
- using the KB root as the boundary for any content that may be disclosed to a provider, so the agent can announce exactly what content leaves the machine
- treating any registry entry with an absolute path as evidence that the document was staged from outside the KB root
- re-staging inside the KB root, re-adding, or rebuilding the KB instead of hand-editing the registry outside a deliberate, hash-preserving migration

This makes staging an intermediate, disposable layer between repository sources and compiled wiki pages, while preserving a clear disclosure trail when content is sent to an LLM-backed command.

## Operational benefits

- Preserves a clean provenance chain from repository file to staged source to compiled page
- Keeps registry metadata machine-portable when staging stays inside the KB root
- Supports deterministic ingestion and incremental rebuilds
- Helps isolate user-approved external ingestion from repository-derived knowledge
- Reduces the chance of stale or orphaned wiki pages after source changes
- Prevents absolute path leakage from outside-KB staging and the resulting diff noise
- Makes privacy disclosures simpler, because the staged input set is bounded and inspectable
- Supports local-only and air-gapped workflows by keeping a clear boundary for what may leave the machine

## Related ideas

KB root staging connects closely to evidence staging, source provenance, compiled knowledge bases, incremental compilation, and deterministic builds. It also depends on [[concepts/consent-first-tooling]] and [[concepts/privacy-preserving-tooling]] when external sources are brought in, and it reinforces [[concepts/data-flow-disclosure]] by keeping the sendable input set inside a known boundary. It is also closely tied to [[concepts/hash-registry-coherence]], [[concepts/registry-drift]], [[concepts/path-safety]], and [[concepts/air-gapped-operation]].

## In the broader lifecycle

In the OpenKB workflow, KB root staging is the first durable boundary that separates raw repository material from generated knowledge. It is what makes later steps like add, recompile, lint, and reconciliation operate on a stable, inspectable input set rather than on arbitrary filesystem state. When staging stays inside the KB root, the pipeline can remain portable, deterministic, and privacy-aware; when it does not, registry entries can capture machine-specific absolute paths and undermine that contract.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]