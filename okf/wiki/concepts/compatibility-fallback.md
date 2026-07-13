---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md"]
description: "Fallback code that preserves behavior when a private API cannot be imported."
---

# Compatibility Fallback

A compatibility fallback is a best-effort alternative implementation used when an expected dependency or private API is unavailable. It aims to preserve user-facing behavior closely enough that the surrounding workflow still functions, while accepting a narrower scope or slight wording differences.

## What it looks like in practice

In [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]], the fallback is described for `scripts/editorial_pass.py`:

- It activates only when `openkb.agent.compiler` cannot be imported from the installed tool environment.
- It mirrors the upstream `_KNOWN_TARGETS_USER` string and reimplements `_format_known_targets` behavior as `_format_targets_mirrored`.
- It changes only the wording of the `--brief` briefing text, not the correctness of `editorial_pass.py --check`.

## Why it matters

Compatibility fallbacks support graceful degradation by keeping tools usable across different runtime environments. They are especially useful when:

- the code depends on a private or underscore-prefixed API,
- the runtime environment may differ from the development environment,
- the main path should remain strict, but the auxiliary path should still work.

## Relationship to other ideas

This concept is closely connected to:

- graceful degradation for continuing operation under partial failure,
- clean room reimplementation when behavior is recreated without directly depending on the original implementation,
- provenance tracking when copied or mirrored behavior needs explicit documentation,
- license compliance requirements when reused code or strings come from upstream sources.

## In the source document

The third-party notices page records the fallback as a formal provenance entry. It identifies:

- the local file and symbols involved,
- the upstream repository and source file,
- the exact release and commit verified against the upstream code,
- the Apache-2.0 license and copyright attribution,
- the distinction between verbatim reuse and from-scratch reimplementation.

That framing makes the fallback a documented, bounded exception rather than an opaque copy.

## Practical takeaway

Use a compatibility fallback when you need resilience across environments, but keep the fallback narrow, explicit, and provenance-aware so it does not quietly become the primary implementation.