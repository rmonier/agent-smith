---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__assets__gitattributes-template.md"]
description: "Binary file handling prevents non-text assets from being altered by text processing."
---

# Binary File Handling

Binary file handling is the practice of identifying non-text assets and ensuring version-control tooling treats them as opaque files rather than applying text-oriented transformations.

## Why It Matters

Binary files do not behave like plain text. If repository tooling applies line-ending normalization or other text conversions to images, fonts, archives, or PDFs, those files can be corrupted or produce inconsistent results across platforms. Correct handling protects file integrity and supports reliable repository operations.

This matters especially in workflows that depend on deterministic staging outputs and stable content hashes, such as [[entities/openkb]] ingestion and related automation.

## How The Source Document Uses It

The source summarized in [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]] defines a `.gitattributes` template that explicitly marks common binary extensions as `binary`.

Included examples cover several categories of non-text assets:

- Images: `png`, `jpg`, `jpeg`, `gif`, `ico`, `webp`
- Documents: `pdf`
- Archives: `zip`, `gz`, `tar`
- Fonts: `woff`, `woff2`, `ttf`, `eot`

By marking these files as binary, Git avoids applying text normalization rules to them.

## Relationship To Line Ending Rules

The same template applies `* text=auto eol=lf` to normalize text files, while separately excluding binary file types from that behavior. This division of responsibility is the core pattern:

- Text files are normalized for consistency
- Binary files are preserved exactly

That makes binary file handling closely related to [[concepts/line-ending-normalization]] and [[concepts/git-attributes]].

## Practical Effect

Explicit binary handling helps:

- Prevent accidental corruption of non-text assets
- Keep cross-platform repository behavior predictable
- Support stable hashing and reproducible staging outputs
- Separate text-processing rules from binary preservation rules

## Related Pages

- [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]]
- [[concepts/git-attributes]]
- [[concepts/line-ending-normalization]]
- [[concepts/provenance-tracking]]
- [[entities/openkb]]