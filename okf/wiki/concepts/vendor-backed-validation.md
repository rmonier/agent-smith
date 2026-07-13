---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"]
description: "Validation that delegates checks to the pinned vendor implementation."
---

# Vendor-Backed Validation

Vendor-backed validation is a validation pattern that relies on the installed upstream tool's own checks as the authoritative execution path, rather than reimplementing those checks locally. In this wiki, it is used to keep curation verification aligned with the pinned OpenKB environment while still adding repository-specific policy gates.

## What it does

The pattern combines two layers:

- vendor execution: call the installed `openkb.lint` API directly for structural checks
- local policy checks: apply repository rules that OpenKB does not enforce itself

In `editorial_pass.py`, this means the script runs the pinned OpenKB interpreter from `uv tool dir`, imports `openkb.lint`, and executes the vendor functions for broken links, index synchronization, orphan detection, invalid frontmatter, and missing OKF fields.

## Why it matters

Vendor-backed validation reduces drift between the wiki's checks and the behavior of the real toolchain that produces and validates the wiki. It also makes failures more meaningful:

- if the public vendor API fails to import or execute, the environment is broken
- if the validation passes, the result reflects the installed OpenKB implementation
- if local policy rules fail, the issue is specific to curation scope or provenance, not the vendor checker

This supports deterministic validation and quality gates by making the validation path explicit and reproducible.

## Source-linked behavior

The script summarized in [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]] uses vendor-backed validation in two distinct ways:

- `--check` executes stable public vendor functions from `openkb.lint`
- `--brief` attempts to render the vendor's private whitelist prompt template, but falls back to a mirrored copy if that private API changes

That split is important: the validation gate itself depends only on stable vendor APIs, while the briefing text is allowed to degrade gracefully because it affects prompt wording rather than correctness.

## Core checks performed by the vendor

The vendor portion of the check runs these functions:

- `find_broken_links`
- `find_orphans`
- `check_index_sync`
- `find_invalid_frontmatter`
- `find_missing_okf_fields`

These checks cover core structural health of the wiki and help enforce openkb wiki health checks and okf validation.

## Local policy added on top

`editorial_pass.py` layers additional rules over the vendor checks:

- only `wiki/concepts/`, `wiki/entities/`, and `wiki/index.md` may change during curation
- new compiled pages require explicit approval through `--allow-new-pages`
- the union of `sources:` values across concepts and entities must remain unchanged
- changed concept and entity pages must keep a non-empty `sources:` list

This makes validation not just syntactic, but also governance-aware, reinforcing provenance tracking and provenance union governance.

## Failure model

The script uses exit codes to separate environment failure from content failure:

- `0` = pass
- `1` = validation or policy violations
- `2` = environment or vendor-tooling failure

That distinction keeps vendor problems visible and prevents silent fallback in the checks that matter.

## Related ideas

- deterministic validation
- quality gates
- openkb wiki health checks
- okf validation
- provenance tracking
- provenance union governance

See also: [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]]