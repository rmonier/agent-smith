---
type: "Concept"
sources: ["summaries/okf-spec.md"]
description: "Validation rule requiring parseable frontmatter with a non-empty type field."
---

# Frontmatter Validation

Frontmatter validation is the requirement that Markdown documents begin with parseable YAML frontmatter and include a non-empty `type` field. In OKF v0.1, this is the minimum structural check needed for a file to count as conformant, making frontmatter the primary machine-readable contract for each document.

## Why it matters

OKF is intentionally minimal, so frontmatter validation carries most of the responsibility for structural integrity. It lets tools distinguish valid knowledge documents from plain Markdown, while still leaving room for optional metadata and flexible content bodies. This supports [[concepts/bundle-conformance]], [[concepts/lightweight-frontmatter-validation]], and [[concepts/generated-content-governance]].

## What the spec requires

From [[summaries/okf-spec]], every non-reserved `.md` file in a bundle must have:

- Parseable YAML frontmatter
- A non-empty `type` field

Optional fields may be present, including:

- `title`
- `description`
- `resource`
- `tags`
- `timestamp`

The body of the file remains normal Markdown and may contain schemas, examples, and citations.

## Validation scope

The specification treats validation as intentionally narrow:

- Reserved Markdown files are exempt from the rule
- Missing optional fields should not cause failure
- Unknown `type` values should be tolerated by consumers
- Broken links should be handled gracefully rather than treated as fatal

This makes frontmatter validation part of a broader permissive parsing approach rather than a strict schema-enforcement system.

## Relationship to other concepts

Frontmatter validation connects closely to:

- [[concepts/frontmatter-metadata]] for the meaning of metadata fields
- [[concepts/reserved-markdown-file-rules]] for files excluded from validation
- [[concepts/okf-validation]] for the broader validation model
- [[concepts/okf-validation-rules]] for implementation-level checks
- [[concepts/deterministic-validation]] for repeatable validation behavior

## Practical implication

For OKF tooling, frontmatter validation is the first gate in content processing. If a document cannot be parsed or lacks `type`, it should be treated as structurally invalid. If the frontmatter is valid, downstream tools can continue with link resolution, indexing, and content extraction.