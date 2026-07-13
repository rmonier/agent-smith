---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/README-md.md"]
description: "Vendored tooling is pinned helper code kept separate from product skills."
---

# Tooling Vendoring

Tooling vendoring is the practice of copying external tools into a repository as pinned, local copies so the project can use them without treating them as part of the core product. In the `agent-smith` README, this appears as a deliberate distinction between the three distributable skills and the extra `graphify` and `openkb` directories that were brought in as vendored toolchain copies during transformation.

## What It Means

Vendored tooling is meant to support a repository's workflows while staying clearly separated from the project-owned capabilities. The README draws a hard line between:

- product skills that users should copy or install
- toolchain copies that were pinned for this repository's own pipeline
- runtime adapters that are projections for a specific harness

This separation keeps the distributable surface small and predictable and supports [[concepts/tool-boundaries]] and [[concepts/skill-vendoring]]. It also fits the README's broader [[concepts/progressive-disclosure]] model: orientation, durable context, and executable actions stay in different layers, so helper tools do not blur into user-facing capability.

## How It Appears in the Source

In [[summaries/README-md]], the repository explains that only three skills are the actual product:

- `agent-ready-context`
- `skill-creator`
- `subagent-profile-adapter`

The other `.agents/skills/` entries, specifically the `graphify` and `openkb` directories, are described as vendored toolchain skills. They were installed by the repository's own transformation pipeline, and the README says they should not be copied into another repository as if they were part of the product.

That distinction is reinforced in the installation instructions: users are told to copy only the three product skills, not the vendored tool copies. The README also frames those tool copies as part of a consent-first, pinned workflow, where the pipeline discloses what it is doing and why before installing anything.

## Why It Matters

Tooling vendoring reduces ambiguity about what a repository actually ships. It supports:

- [[concepts/integrity-pinning]] by keeping a local, versioned copy of a tool
- [[concepts/toolchain-pinning]] by locking the exact tool version used during transformation
- [[concepts/local-tooling-boundaries]] by preventing bundled helpers from becoming accidental policy sources
- [[concepts/generated-artifact-adoption]] by letting the pipeline use tools to generate durable outputs without promoting the tool itself into the product layer
- [[concepts/consent-first-tooling]] by keeping installation and reuse explicit rather than implicit

The README also uses vendoring to reinforce [[concepts/documentation-architecture]]: the user-facing instructions stay focused on the distributable skills, while implementation details about pinned tool copies are kept as explanatory context. That helps preserve clear [[concepts/knowledge-boundaries]] between compiled knowledge, runtime projections, and distributable actions.

## Practical Rule

If a directory exists because the repository pipeline needs a specific external program at a specific pinned version, that directory is vendored tooling, not product content. It may be necessary for builds and maintenance, but it should not be treated as the canonical capability the repository offers to others.

## Related Ideas

- [[concepts/skill-vendoring]]
- [[concepts/toolchain-pinning]]
- [[concepts/tool-boundaries]]
- [[concepts/local-tooling-boundaries]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/consent-first-tooling]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]