---
type: "Summary"
description: "Template enforces LF normalization and binary handling for stable repository staging."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__assets__gitattributes-template.md"
---

# Summary

This document defines a `.gitattributes` template for repository setup focused on deterministic file handling across platforms.

## Key Points

- Sets `* text=auto eol=lf` so text files normalize to LF line endings.
- Explains that LF normalization helps keep OKF staging hashes stable and deterministic across operating systems.
- Marks common binary formats as `binary` so Git does not apply text normalization to them.
- Covers image, archive, font, and PDF file types including `png`, `jpg`, `gif`, `webp`, `pdf`, `zip`, `gz`, `tar`, `woff`, `woff2`, `ttf`, and `eot`.

## Main Idea

The template reduces cross-platform inconsistency by combining text normalization with explicit binary exclusions, supporting reliable repository ingestion and content hashing.

## Related Concepts
- [[concepts/quality-gates]]
- [[concepts/provenance-tracking]]

- [[concepts/line-ending-normalization]]
- deterministic hashing
- [[concepts/git-attributes]]
- cross-platform repository consistency
- [[concepts/binary-file-handling]]

## Entities
- [[entities/openkb]]
