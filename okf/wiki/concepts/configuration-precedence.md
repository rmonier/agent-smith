---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md"]
description: "Rules that determine which config source overrides another."
---

# Configuration Precedence

Configuration precedence is the rule set that decides which value wins when the same setting appears in more than one place. It matters when tooling supports multiple config homes, shared example files, per-user overrides, and repository-local state.

## Why it matters

When precedence is unclear, different contributors can run the same workflow with different effective settings. That can lead to drift in compiled artifacts, confusing diagnostics, and hard-to-reproduce behavior. Clear precedence supports [[concepts/local-vs-shared-configuration]], [[concepts/single-source-of-truth]], and [[concepts/provenance-tracking]].

## In `check_prereqs.py`

The preflight script for [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] encodes precedence in a few places:

- It treats `okf/.openkb/config.yaml` as the active project-local config when present.
- It compares that file against `okf/.openkb/config.yaml.example` only for shared keys like `language`, `pageindex_threshold`, and `entity_types`.
- It explicitly allows provider-specific settings such as `model`, `litellm`, and `timeout` to vary per user.
- It checks two credential homes, `okf/.env` and `~/.config/openkb/.env`, and reports when both exist.
- When both credential homes exist, the project file is described as winning for shared keys, making the precedence explicit to the user.

## Key pattern

The script distinguishes between:

- Shared repository contract values that should stay aligned across contributors.
- User-specific provider and credential values that may legitimately differ.

That split is a practical example of [[concepts/local-vs-shared-configuration]] and [[concepts/configuration-precedence]] working together.

## Related ideas

- [[concepts/consent-first-tooling]] for installation choices that remain user-controlled.
- [[concepts/progressive-disclosure]] for surfacing only the precedence details that matter.
- [[concepts/validation-vs-health-reporting]] for treating drift as a diagnostic rather than an immediate failure in every case.
- [[concepts/registry-drift]] for broader mismatch detection across expected and local state.

## Takeaway

Good configuration precedence makes repository tooling predictable: shared settings stay consistent, local overrides remain intentional, and diagnostics explain exactly which source is authoritative.