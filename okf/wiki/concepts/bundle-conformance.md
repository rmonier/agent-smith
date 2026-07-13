---
type: "Concept"
sources: ["summaries/okf-spec.md"]
description: "Minimal rules for an OKF bundle to be considered valid."
---

# Bundle Conformance

Bundle conformance in OKF is the rule set that determines whether a knowledge bundle meets the minimum structural requirements of the format. The specification treats conformance as intentionally lightweight: it validates the core shape of the bundle without forcing strict opinions about every field, type, or link target.

## What Must Be Present

A bundle conforms to OKF v0.1 when every non-reserved `.md` file contains parseable YAML frontmatter with a non-empty `type` field. That `type` field is the only required frontmatter field at the bundle level.

Reserved Markdown files are handled separately under the format's reserved-file rules, so conformance focuses on ordinary content pages rather than index or log files.

## What Is Optional

The specification allows several optional fields in frontmatter:

- `title`
- `description`
- `resource`
- `tags`
- `timestamp`

A conforming bundle may omit any of these fields. Consumers are expected to tolerate those omissions rather than reject the bundle.

## How Consumers Should Behave

OKF conformance is not the same as strict correctness of every detail. The spec requires consumers to be permissive when reading bundles:

- Missing optional fields should not break ingestion
- Unknown `type` values should still be accepted
- Broken links should be handled gracefully

This makes bundle conformance compatible with [[concepts/graceful-degradation]] and [[concepts/permissive-open-source-licensing]]-style robustness, though in a documentation sense rather than a licensing one.

## Why It Matters

Bundle conformance provides the baseline that tooling can rely on for validation, traversal, and downstream processing. It gives agents and validators a clear minimum bar while preserving flexibility for domain-specific content.

This is the foundation for [[concepts/okf-bundle-validation]], [[concepts/okf-validation-rules]], and the broader OKF workflow described in [[summaries/okf-spec]].

## Practical Interpretation

In practice, conformance means:

- Markdown files are parseable
- Frontmatter exists where required
- `type` is always populated
- Optional metadata stays optional
- Read-time failures are minimized through permissive handling

That balance keeps OKF usable as a portable knowledge format without turning it into a rigid schema system.