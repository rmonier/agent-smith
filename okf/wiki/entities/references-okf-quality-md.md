---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
type: "Work"
description: "OpenKB guidance for OKF quality and validation"
---

# OKF Quality

`references/okf-quality.md` is the OpenKB reference used to evaluate the quality of generated OKF output and the correctness of compiled wiki pages.

## Role

This document serves as a validation baseline for `okf/wiki/` and is read before validating or reviewing generated OKF. It helps determine whether compiled pages meet the expected structure, grounding, and conformance rules.

## What It Covers

The page is part of the validation path for:

- [[concepts/okf-validation]] and [[concepts/okf-bundle-validation]]
- [[concepts/okf-offline-conformance]]
- [[concepts/okf-validation-rules]]
- generated generated artifact validation
- [[concepts/wiki-review-gates]]

It is used alongside `references/official-okf-spec-web-check.md` when web access is available, so the offline baseline can be refreshed against the upstream spec.

## Related Workflow

The guidance around this page fits into a broader pipeline for building and checking the repository knowledge base:

- stage deterministic source input first
- ingest into OpenKB rather than editing compiled pages directly
- review generated wiki pages for duplicates, vague naming, missing caveats, and misclassification
- validate the resulting `okf/wiki/` bundle with the appropriate script

## Notes

This page is referenced as a quality and validation authority rather than as a repository knowledge topic itself. It supports the broader [[concepts/okf-workflow-governance]] and [[concepts/knowledge-compilation-pipeline]] patterns by defining what counts as acceptable compiled output.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
