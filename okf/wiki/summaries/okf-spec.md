---
type: "Summary"
description: "Official OKF v0.1 spec defining the bundle format, fields, links, and conformance."
doc_type: short
full_text: "sources/okf-spec.md"
---

# Open Knowledge Format (OKF) v0.1

This document is the official specification for Open Knowledge Format (OKF) v0.1, a minimal, human- and agent-friendly knowledge representation format built from Markdown files with YAML frontmatter in a directory structure. It defines the intended scope of OKF, the required document fields, the supported bundle layout, and the conformance rules that implementations such as `okf/wiki/` and `validate_okf_bundle.py` are expected to follow.

## Purpose

OKF is designed to make knowledge easy to read, write, traverse, diff, and exchange. The specification frames the format around four goals:

- Let enrichment agents write into a universal format
- Help consumption agents read and traverse knowledge bundles
- Support knowledge exchange across organizations
- Standardize only the minimal fields needed for meaningful consumption

The spec explicitly avoids becoming a rigid ontology or a replacement for specialized serialization formats like Avro or Protobuf.

## Bundle Structure

An OKF bundle is a directory tree of Markdown files. The format allows optional `index.md` files for directory-level listings and `log.md` files for chronological updates at any level in the tree.

This makes OKF a lightweight knowledge bundle format with simple filesystem-based organization rather than a custom storage layer.

## Document Requirements

The core requirement is that every non-reserved `.md` file must contain parseable YAML frontmatter with a non-empty `type` field.

Optional frontmatter fields include:

- `title`
- `description`
- `resource` for a canonical URI
- `tags`
- `timestamp`

The body of a document remains Markdown and can include schemas, examples, and citations.

## Linking Model

The specification supports two cross-link styles:

- Absolute bundle-relative links beginning with `/`, recommended for stability
- Standard relative paths

This establishes a cross linking model meant to survive movement and traversal across bundles.

## Conformance Rules

A bundle conforms to OKF v0.1 if every non-reserved Markdown file has valid YAML frontmatter and a non-empty `type` field.

Consumers are still expected to be permissive in practice:

- Missing optional fields should be handled gracefully
- Unknown `type` values should not break parsing
- Broken links should not cause hard failure

That combination of strict minimal validation and flexible consumption reflects the spec's permissive parsing philosophy.

## Why It Matters

This specification is the compatibility anchor for OKF tooling and content. It defines the minimum shape that enables interoperability while leaving room for domain-specific structures, editorial style, and future extensions.

It is especially relevant as the reference point for validating bundles, generating summaries, and designing downstream consumers that need to read OKF content reliably.

## Related Concepts
- [[concepts/okf-specification]]
- [[concepts/frontmatter-validation]]
- [[concepts/bundle-conformance]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/okf-validation]]
- [[concepts/lightweight-frontmatter-validation]]
- [[concepts/openkb-wikilink-resolution]]
- [[concepts/reserved-markdown-file-rules]]
- [[concepts/source-provenance]]

## Entities
- [[entities/google-cloud-platform]]
- [[entities/knowledge-catalog]]
- [[entities/okf-spec]]
- [[entities/okf-cli]]
- [[entities/validate_okf_bundle-py]]
- [[entities/okf-wiki]]
- [[entities/openkb-cli]]
- [[entities/openkb]]
- [[entities/wiki-schema-md]]
- [[entities/references-official-okf-spec-web-check-md]]
- [[entities/okf-quality-md]]
