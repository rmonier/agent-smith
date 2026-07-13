---
type: "Summary"
description: "GitHub Actions template for zero-LLM OKF structural validation in CI."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__assets__okf-validate-ci-yml.md"
---

# Summary

This document is a GitHub Actions workflow template for validating an OpenKB/OKF wiki bundle during pull requests.

## What the file does

- Defines a CI workflow named `okf-validate`.
- Triggers on `pull_request` events when files under `okf/**` change.
- Checks out the repository and installs `uv`.
- Runs `validate_okf_bundle.py` against `okf/wiki` with the `--openkb-wiki` flag.

## Key ideas

### Zero-LLM validation gate

The workflow is explicitly designed as a structural validation step that does not require an API key and does not send data to external services. Its purpose is to enforce repository and bundle correctness in CI, making it suitable as a merge gate. This connects to ideas such as [[concepts/quality-gates]], [[concepts/deterministic-validation]], and [[concepts/privacy-preserving-tooling]].

### Separation of strict validation from advisory linting

The file emphasizes that `openkb lint` is intentionally excluded from CI gating because it is an LLM-backed health report that always completes without failing the build. Instead, only the deterministic validator is used in CI. This reflects a distinction between [[concepts/deterministic-validation]] and advisory linting.

### Consent-first installation model

The comments frame the workflow as a template to be copied into `.github/workflows/okf-validate.yml` in a target repository rather than assumed to be active by default. This suggests a [[concepts/tooling-consent-and-pin-management]] approach to repository automation.

## Operational details

- Uses `actions/checkout@v4` to fetch repository contents.
- Uses `astral-sh/setup-uv@v5` to install the Python package manager/runtime tool.
- Invokes:
  `uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki`
- Notes that action versions are pinned only to major tags and may need full commit SHA pinning depending on organizational policy, relating to [[concepts/tooling-consent-and-pin-management]].

## Why it matters

This file provides a minimal, reproducible pattern for enforcing OpenKB wiki structure in pull requests without relying on LLM services. It serves as a practical example of [[concepts/quality-gates]] for knowledge-base artifacts and of keeping mandatory CI checks deterministic, privacy-preserving, and failure-capable.

## Related Concepts
- [[concepts/source-driven-regeneration]]
- [[concepts/provenance-tracking]]
- [[concepts/documentation-architecture]]

## Entities
- [[entities/openkb]]
