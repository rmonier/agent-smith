---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Record-and-verify artifacts from the first trusted index fetch."
---

# Trust on First Use

Trust on First Use (TOFU) is a supply-chain practice where the first fetched artifact from a configured source becomes the baseline for later verification. In this wiki context, the first approved install or download is not treated as inherently safe forever; instead, its exact version, integrity hash, and source index are recorded so later runs can detect substitution or unexpected drift.

## What it means here

The `dependencies.md` document uses TOFU to make tool adoption auditable without assuming a global signature system. The workflow:

- installs tools only from the environment's configured index
- records the exact pinned version
- captures the artifact's sha256 integrity value
- stores the index it came from and the date it was recorded
- re-checks later installs against the same recorded values

This turns the first successful fetch into a durable baseline for [[concepts/integrity-pinning]] and [[concepts/provenance-tracking]].

## Why it matters

TOFU is a practical compromise between usability and security. It does not prove the first artifact was honest, but it does let the system detect if the same version later resolves to a different binary or wheel.

That matters for:

- [[concepts/supply-chain-security]] when packages are installed through mirrors or proxies
- [[concepts/provenance-aware-tool-installation]] when exact package identity must be verified before use
- [[concepts/toolchain-pinning]] when CLI behavior depends on a stable release
- [[concepts/hash-registry-coherence]] when the same version and index should continue to resolve to the same digest

## Operational rules from the source

The source document treats TOFU as part of a broader pinning policy:

- exact versions are required in install commands
- hashes are recorded in `AGENTS.md`
- later installs must compare against the recorded hash
- a mismatch for the same version and index is a stop-and-report event
- if the environment changes mirrors, the baseline should only be reset with explicit user acknowledgement

The document also stresses that TOFU is not a substitute for upstream trust guarantees. It is an audit trail for the configured index, not a universal signature verification system.

## Related workflow behavior

TOFU supports [[concepts/consent-first-workflows]] and [[concepts/quality-gates]] by forcing explicit review before tool upgrades. It also fits with [[concepts/graceful-degradation]] because readiness checks can report missing or unverified tools without breaking the entire workflow.

In the same document, TOFU is paired with optional tooling like `openkb` and `graphify`, making the point that local readiness should be verified before compiled knowledge work begins. That ties this concept to [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] and the broader [[concepts/agent-ready-context-skill]] workflow.

## In practice

A TOFU-based install process usually has three steps:

1. fetch the exact pinned artifact from the configured index
2. compute and record its integrity hash
3. verify future installs against that recorded baseline

If the digest changes without a version change, the safe response is to stop and investigate rather than silently update the record.

## Connection to other concepts

TOFU is one part of a larger cluster around safe dependency handling: [[concepts/version-pinning]], [[concepts/dependency-management]], [[concepts/trust-on-first-use]] is the baseline capture mechanism, and [[concepts/supply-chain-security]] is the broader threat model it serves.