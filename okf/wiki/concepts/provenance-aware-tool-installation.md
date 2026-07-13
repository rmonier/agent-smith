---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Installing tools from pinned, verified sources with consent and registry respect."
---

# Provenance-Aware Tool Installation

Provenance-aware tool installation is the practice of installing local CLIs and support tools only from a known upstream source, with an exact version pin, a recorded integrity hash, and respect for the environment's configured package index. It treats installation as part of [[concepts/supply-chain-security]] and [[concepts/trust-on-first-use]], not as a casual setup step.

## Core idea

The source documents for [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] and [[summaries/agents__skills__agent-ready-context__references__workflow-md]] frame tool installation as a controlled readiness and bootstrap workflow:

- verify the exact package identity before installation
- pin the version explicitly in any command that is left behind
- record the downloaded artifact's sha256 integrity value
- use the configured Python index or mirror instead of overriding it
- treat index mismatches and hash mismatches as stop-and-report events
- bootstrap missing tools only with user consent when they are optional
- refuse to proceed when a required vendored skill is missing for an installed CLI

This makes installation auditable and resistant to lookalike packages, mirror drift, accidental upgrades, and hidden dependency mismatches.

## Why it matters

The concept supports [[concepts/dependency-management]] by making dependencies reproducible and inspectable. It also strengthens [[concepts/version-pinning]], [[concepts/integrity-pinning]], and [[concepts/hash-registry-coherence]] by requiring both a version and an artifact digest.

The broader workflow adds two important constraints:

- provenance checks are part of the full OpenKB build sequence, alongside prereq checks, vendored skill checks, and KB initialization
- tool installation is never isolated from the knowledge pipeline, because the wiki build depends on deterministic tool availability and explicit consent for bootstrap steps

Without provenance checks, a tool may appear correct while actually coming from the wrong package name, the wrong registry, or a republished artifact. The workflow explicitly warns against:

- accepting lookalike package names
- hardcoding public registry URLs when an enterprise mirror is already configured
- silently updating versions without user approval
- reinstalling a pinned version after its recorded hash no longer matches the same index

## Practices defined in the source

### Exact pinning

Commands should use exact version constraints, such as `tool==X.Y.Z`, rather than floating versions. Floating versions are only acceptable for a one-off install the user explicitly approves.

### Integrity recording

On first install, capture the artifact hash from the configured index and store it with the version and index metadata in `AGENTS.md`. Later installs should re-check the same version against the same index.

### Registry respect

The workflow must use the environment's configured index settings, including private mirrors and proxies, and must not bypass them to reach public PyPI directly.

### Consent-first bootstrap

Optional tools such as graphify or OpenKB should be offered through a consent-first bootstrap path when missing. Required prerequisites are checked first, and hard failures stop the workflow until the environment is repaired with user approval.

### Vendored-skill gating

When installed CLIs are expected to run, their pinned vendored skill copies must already exist in the repository. If a CLI is installed but its corresponding skill is not vendored, the workflow treats that as a blocking mismatch rather than proceeding on the strength of the binary alone.

### Update discipline

A newer version should trigger a visible update workflow:

- detect the newer release
- review upstream release notes or changelog
- ask for explicit confirmation before moving the pin
- recapture the integrity hash after updating

## Relation to other concepts

This concept connects closely to [[concepts/provenance-tracking]], [[concepts/source-provenance]], and [[concepts/supply-chain-security]] because tool identity is established through source, version, and digest rather than by name alone.

It also supports [[concepts/toolchain-pinning]] and [[concepts/tooling-consent-and-pin-management]] by making installs consent-first and reproducible across machines.

In the agent-ready-context workflow, provenance-aware installation is part of the broader readiness model described in [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] and enforced by the build sequence in [[summaries/agents__skills__agent-ready-context__references__workflow-md]].

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]