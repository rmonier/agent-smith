---
type: "Concept"
sources: ["summaries/okf-spec.md"]
description: "OKF's minimal rules for bundle structure, frontmatter, and linking."
---

# OKF Specification

OKF Specification defines the minimal rules that make an Open Knowledge Format bundle readable, traversable, and valid for agents and humans. It centers on Markdown files with YAML frontmatter in a directory tree, with just enough structure to support portable knowledge exchange without imposing a rigid taxonomy.

## Core Idea

The specification treats knowledge as a filesystem-native bundle: content lives in Markdown, metadata lives in frontmatter, and organization comes from directories plus optional index and log files. That keeps the format simple to inspect manually while still supporting machine parsing and validation.

This aligns closely with [[concepts/frontmatter-validation]], [[concepts/bundle-conformance]], and [[concepts/reserved-markdown-files]].

## Main Requirements

An OKF bundle conforms when every non-reserved `.md` file has parseable YAML frontmatter with a non-empty `type` field. Optional metadata includes:

- `title`
- `description`
- `resource`
- `tags`
- `timestamp`

The body remains standard Markdown, so documents can include schemas, examples, and citations without changing the underlying file format.

## Bundle Organization

The spec allows a hierarchical directory structure with optional `index.md` files for directory listings and `log.md` files for chronological updates. This supports [[concepts/knowledge-base-navigation]] and [[concepts/index-based-discovery]] while keeping the bundle portable and easy to traverse.

## Linking Rules

OKF supports two link forms:

- Absolute bundle-relative links beginning with `/`, recommended for stability
- Standard relative paths

This makes link resolution part of the specification's portability story and connects to [[concepts/wikilink-resolution]] and [[concepts/link-directionality]].

## Conformance Philosophy

The spec is strict about the minimum validation surface, but permissive in consumption. Implementations should gracefully handle:

- Missing optional fields
- Unknown `type` values
- Broken links

That balance reflects a [[concepts/graceful-degradation]] approach and supports [[concepts/deterministic-validation]] without making the format brittle.

## Why It Matters

OKF Specification is the authority for tools that validate, generate, or consume OKF bundles. It defines the compatibility contract for implementations such as `okf/wiki/` and `validate_okf_bundle.py`, and it establishes the baseline for future knowledge-bundle workflows.

## Related Source

- [[summaries/okf-spec]]