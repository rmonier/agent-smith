---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md"]
description: "Recording approved artifact hashes with versions and sources to verify exact dependencies."
---

# Integrity Pinning

Integrity pinning is the practice of storing a verifier for a specific dependency artifact alongside its source, version, and retrieval context so tools can confirm that the resolved content matches what was originally approved. It strengthens dependency reproducibility and helps detect tampering, substitution, mirror drift, or unintended changes in machine-managed dependency state.

## Why It Matters

Integrity pinning supports trustworthy automation by making dependency resolution checkable rather than implicit. When a lock file or setup record stores not only where a dependency comes from and which version is selected, but also an integrity value tied to the retrieved artifact, tooling can reject unexpected content even if the source identifier or version string appears correct.

The newer dependency guidance for agent-ready repositories adds an important nuance: version pinning alone is not enough. The same version from the same configured index should continue to resolve to the same approved artifact, and a mismatch should be treated as a stop-and-report event rather than silently repaired. This makes integrity pinning a concrete control inside [[concepts/dependency-management]], [[concepts/deterministic-builds]], and [[concepts/supply-chain-security]]. It also complements [[concepts/provenance-tracking]] by preserving evidence about what exact dependency payload was expected, from which index, and under what approval decision.

## In the Source Document

[[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]] presents a minimal example lock file for skills. In that example, each locked skill entry includes:

- a `name`
- a `source`
- a pinned `version`
- an `integrity` value

That document frames the lock file as tool-generated metadata and explicitly warns against hand-editing real vendor lock entries unless the managing tool supports it. That warning matters for integrity pinning because the integrity field is only useful when it is generated and interpreted consistently by the responsible toolchain. Manual edits can break trust assumptions, produce invalid verification data, or create mismatches between declared and resolved content.

[[summaries/agents__skills__agent-ready-context__references__dependencies-md]] extends the idea from lock files to repository toolchain setup. It requires pinned versions and recorded sha256 values for tools such as `openkb` and `graphifyy`, captured from the configured Python index and recorded in `AGENTS.md` together with the index source and date. The document also distinguishes first-time trust establishment from later verification: the first approved install records the baseline hash, and future installs must compare against that same recorded value instead of trusting the registry response anew.

## Core Elements

Integrity pinning usually works through a few coordinated pieces:

- A stable source identifier naming where the dependency is resolved from
- A pinned version or digest selecting the intended release
- A tool-generated integrity value bound to the fetched artifact
- The registry or index context the artifact was retrieved from
- Verification behavior in the dependency manager, installer, or bootstrap workflow

Together, these let tools distinguish between "the requested dependency name and version" and "the exact artifact bytes that were previously accepted." That distinction is especially important when environments use private mirrors, project-scoped installers, generated lock files, or offline validation workflows.

The added emphasis on index context matters because the same package/version pair may be served through different configured registries or mirrors. In that model, integrity pinning is not only artifact-specific but also tied to the approved retrieval path, which aligns with [[concepts/hash-registry-coherence]] and broader [[concepts/tooling-consent-and-pin-management]].

## Operational Implications

In practice, integrity pinning improves confidence when dependencies are restored, shared, cached, vendored, or rebuilt across environments. It is especially useful in workflows that value [[concepts/offline-first-workflows]], [[concepts/deterministic-validation]], or strong [[concepts/tooling-consent-and-pin-management]].

The newer toolchain guidance adds several practical behaviors:

- first installs establish a trust-on-first-use baseline by hashing the exact downloaded artifact
- later installs re-query the same configured index and compare against the recorded value
- a mismatch for the same version and index is treated as a security incident, not normal drift
- updates require explicit review, release-note inspection, and a fresh integrity record rather than silent pin movement

This also fits within broader [[concepts/generated-content-governance]]: lock files, pin records, and similar integrity metadata are usually outputs of dependency tools or controlled setup procedures, not free-form configuration files. Treating them as generated or tightly managed artifacts helps preserve consistency between dependency selection, user approval, and verification data.

## Limits and Assumptions

Integrity pinning does not by itself prove that a dependency is safe or appropriate; it proves that the artifact matches the expected locked value. It therefore works best as one control inside a broader trust model that may also include [[concepts/source-trust-levels]], provenance records, and supply-chain review.

The dependency reference also makes the trust model explicit: this is a trust-on-first-use approach. It can detect artifact substitution after the first approved baseline is recorded, but it cannot prove that the very first retrieved artifact was trustworthy. That makes integrity pinning a strong continuity check rather than a complete substitute for source review, package identity verification, or broader supply-chain policy.

## See Also

- [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[concepts/dependency-management]]
- [[concepts/deterministic-builds]]
- [[concepts/deterministic-validation]]
- [[concepts/generated-content-governance]]
- [[concepts/hash-registry-coherence]]
- [[concepts/provenance-tracking]]
- [[concepts/supply-chain-security]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/trust-on-first-use]]

See also: [[summaries/agents__skills__skill-creator__references__dependencies-md]]

See also: [[summaries/agents__skills__skill-creator__references__source-attribution-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/README-md]]