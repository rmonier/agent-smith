---
type: "Summary"
description: "Python validator for OKF bundles and OpenKB wiki conformance rules."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"
---

# `validate_okf_bundle.py`

This script validates an OKF bundle or OpenKB wiki tree against local conformance rules, with optional stricter checks for OpenKB-specific wiki structure.

## What it does

- Checks that non-reserved Markdown files behave like concept documents under OKF rules.
- Validates YAML frontmatter parsing and requires a non-empty `type` field for concept pages.
- Treats `index.md` and `log.md` as reserved files with their own structural rules.
- Optionally enforces OpenKB wiki conventions with `--openkb-wiki`.
- Supports `--strict-warnings` to turn warnings into errors.

## Validation model

The script encodes the core assumptions of okf conformance:

- every non-reserved Markdown file is a concept document;
- concept pages must have parseable YAML frontmatter;
- concept frontmatter must include a non-empty `type` field;
- `index.md` may carry an `okf_version` field at the bundle root;
- `log.md` has its own heading format rules.

It also adds audit-oriented checks that are not part of the formal spec but help catch damaged content:

- unclosed code fences at end of file;
- sibling page names that normalize to the same slug, suggesting near-duplicates.

## OpenKB wiki mode

When run with `--openkb-wiki`, the validator adapts to OpenKB's repository layout and conventions:

- skips `AGENTS.md`, `sources/`, and `reports/` as operational areas rather than compiled wiki content;
- flags broken wikilinks as errors, using OpenKB-style link resolution;
- warns when `concepts/` or `entities/` pages are missing the machine-managed `sources:` list;
- ignores fenced and inline code when scanning for links to reduce false positives.

## Implementation details

- Uses `pathlib`, `argparse`, and `re` for portable filesystem and text handling.
- Optionally uses `PyYAML` for frontmatter parsing; without it, YAML validation degrades with an explicit warning.
- Handles CRLF input by normalizing line endings before parsing.
- Separates page-specific validation into `validate_index`, `validate_log`, and `validate_concept`.
- Builds a wiki-target index from all Markdown files so wikilinks can be resolved without external dependencies.

## Key ideas

- [[concepts/frontmatter-metadata]]: YAML metadata is the primary structural contract for pages.
- [[concepts/wikilink-integrity]]: link integrity is treated as an important wiki health signal.
- [[concepts/okf-offline-conformance]]: the validator combines formal rules and practical checks.
- [[concepts/openkb-wiki-validation-modes]]: some paths are excluded because they are infrastructure, not content.
- [[concepts/validation-vs-health-reporting]]: warnings such as truncated fences and duplicate slugs help detect hidden damage.

## Notable behavior

- `index.md` without headings or Markdown links only triggers warnings, not hard failure.
- `log.md` accepts either the plain OKF date heading form or OpenKB's timestamped log headings in wiki mode.
- Exploration pages are treated specially in OpenKB mode because saved queries and findings do not always follow the same frontmatter shape as compiled pages.
- Missing `sources:` on generated concept/entity pages is treated as a warning, signaling possible loss of provenance.

## Why it matters

This script is both a validator and a codified statement of repository expectations. It bridges formal OKF conformance with OpenKB's local operational rules, making it useful for detecting malformed pages, broken navigation, and provenance loss before content is published or compiled further.

## Related Concepts
- [[concepts/okf-bundle-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/reserved-markdown-files]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/okf-validation-rules]]
- [[concepts/okf-validation]]
- [[concepts/okf-wiki-governance]]
- [[concepts/path-based-validation]]
- [[concepts/graph-integrity-diagnostics]]
- [[concepts/generated-content-governance]]
- [[concepts/quality-gates]]
- [[concepts/wiki-review-gates]]

## Entities
- [[entities/validate_okf_bundle-py]]
- [[entities/openkb-cli]]
- [[entities/okf-spec]]
- [[entities/okf-wiki-agents-md]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-tooling-index-md]]
- [[entities/knowledge-catalog]]
- [[entities/google-cloud-platform]]
- [[entities/pyyaml]]
- [[entities/python]]
- [[entities/uv]]
- [[entities/openkb-wiki]]
- [[entities/okf]]
- [[entities/agents-md]]
- [[entities/okf-wiki]]
- [[entities/openkb]]
- [[entities/graphify]]
