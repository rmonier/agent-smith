---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
description: "Local files can leak into shared git artifacts even without provider egress."
---

# Local Artifact Leakage

Local artifact leakage is the risk that content kept private on a machine still gets copied into generated outputs, committed history, or shared repositories. It is distinct from LLM or network egress: the data never leaves the machine through a provider, but it can still become visible to collaborators through build artifacts.

## Why it matters

This concept is central to [[concepts/privacy-preserving-tooling]] and [[concepts/local-only-repo-artifacts]]. A workflow can be fully air-gapped and still leak sensitive material if local files are scanned, transformed, and written into tracked outputs.

The source document emphasizes this as a different leak class from provider exposure. The danger is not that a tool phones home, but that a file excluded only by local developer settings can still be captured by pipeline-generated artifacts and then committed.

## Source-driven findings

From [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]:

- `graphify update` only respects `.gitignore` and `.graphifyignore` when deciding what to scan.
- It does not read `.git/info/exclude` or a user's global excludes file.
- A file excluded only through those local mechanisms can still be scanned.
- If the file produces graph nodes, its content can end up in `graphify-out/graph.json` or `GRAPH_REPORT.md`.
- Those outputs are committed and pushed, so the leaked content becomes visible in every clone.

The document explicitly treats this as a committed-history risk rather than an egress-to-provider risk.

## Operational implications

- Exclusions must be expressed in repository-visible ignore files when they are meant to prevent ingestion.
- Local developer-only exclusions are not enough to prevent artifact generation.
- Pre-commit review is needed for generated graph outputs when local-only files may have been scanned.
- The fix should be reactive and deliberate, not a preemptive broad exclusion that hides legitimate source material.

## Related boundaries

Local artifact leakage connects closely to [[concepts/source-pack-staging]], [[concepts/kb-root-staging]], and [[concepts/deterministic-source-pack-staging]] because staging rules determine which files enter the compilation path. It also relates to [[concepts/registry-drift]] and [[concepts/hash-registry-coherence]] when generated metadata records paths that should not have been captured.

## Practical takeaway

A privacy-safe pipeline must guard against both external disclosure and internal propagation. Even when a workflow keeps data local, generated artifacts can still become a durable shared leak path if local-only exclusions are not accounted for.