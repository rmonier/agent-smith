---
sources: ["summaries/okf-spec.md"]
type: "Product"
description: "Command-line product for working with OKF bundles"
---

# OpenKB CLI

OpenKB CLI is a command-line product for creating, validating, and managing OKF bundles. It sits in the OpenKB/OKF toolchain as a local-first interface for working with Markdown-based knowledge bundles and related validation workflows.

## Role in the OKF ecosystem

The CLI is one of the concrete implementations expected to conform to the Open Knowledge Format (OKF) v0.1 specification. In that context, it helps operationalize the format's core rules around bundle structure, frontmatter requirements, and link handling.

The specification emphasizes that OKF bundles are directory trees of Markdown files with YAML frontmatter, optional `index.md` and `log.md` files, and a required non-empty `type` field in every non-reserved Markdown file. OpenKB CLI supports that model by providing a practical way to inspect and validate bundle conformance.

## Spec-aligned behavior

The OKF spec defines several behaviors that shape the CLI's expected responsibilities:

- Validate parseable YAML frontmatter in non-reserved Markdown files
- Ensure the required `type` field is present and non-empty
- Tolerate missing optional fields such as `title`, `description`, `resource`, `tags`, and `timestamp`
- Handle unknown types and broken links gracefully
- Support bundle-relative links beginning with `/` as the preferred cross-link form

These expectations align OpenKB CLI with [[concepts/okf-validation]] and [[concepts/bundle-conformance]].

## Relationship to other pages

OpenKB CLI is closely related to the broader OKF tooling stack, including [[entities/okf]], [[entities/okf-cli]], and [[entities/validate_okf_bundle-py]]. It also connects to the compiled knowledge pages describing OKF governance and validation workflows, especially [[concepts/okf-specification]] and [[concepts/okf-workflow-governance]].

## Notes

- The OKF spec treats Markdown as the primary storage format for knowledge content.
- The format is intentionally permissive for consumers, even when producers enforce stricter checks.
- The CLI should therefore favor useful validation feedback over hard failure where possible.

## Related Documents
- [[summaries/okf-spec]]
