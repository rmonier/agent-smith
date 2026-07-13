---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "Validation of OKF bundles and OpenKB wikis against structural rules."
---

# OKF Bundle Validation

OKF bundle validation is the process of checking a Markdown-based knowledge bundle against the structural and content rules expected by OKF and, in OpenKB mode, the repository's own wiki conventions. It combines strict conformance checks with softer health checks so a bundle can be treated as both a spec artifact and a living knowledge base.

## What It Checks

The validator enforces several layers of correctness:

- non-reserved `.md` files are treated as concept pages
- concept pages must have parseable YAML frontmatter
- concept pages must include a non-empty `type` field
- `index.md` and `log.md` follow reserved-file rules rather than concept rules
- the bundle-root `index.md` may declare `okf_version`
- code fences must not be left open at end of file
- sibling pages that normalize to the same slug are flagged as likely duplicates

These checks align with [[concepts/okf-validation]], [[concepts/okf-validation-rules]], and [[concepts/reserved-markdown-file-rules]]. The script also reflects [[concepts/frontmatter-metadata]], [[concepts/filesystem-validation]], and [[concepts/path-based-validation]] by validating page structure directly from the repository tree.

## OpenKB Wiki Mode

When run with `--openkb-wiki`, the script adapts to OpenKB's repository layout and graph rules:

- root `AGENTS.md` is skipped
- `sources/` and `reports/` are skipped as operational areas
- broken wikilinks become errors
- `concepts/` and `entities/` pages should carry a non-empty `sources:` frontmatter list
- link scanning ignores fenced and inline code to reduce false positives

This makes the validator useful for [[concepts/openkb-wiki-validation-modes]] and [[concepts/openkb-wiki-health-checks]], especially where [[concepts/wikilink-integrity]] matters. It also fits [[concepts/tooling-navigation-exception]] and [[concepts/knowledge-boundaries]] by treating operational wiki areas differently from compiled content.

## Validation Philosophy

The script mixes hard failures with advisory warnings.

Hard errors cover cases that imply structural invalidity or broken content, such as:

- missing or invalid frontmatter
- missing required `type`
- malformed reserved-file structure
- broken wikilinks in OpenKB mode
- invalid UTF-8 content

Warnings cover issues that may still be acceptable during staged generation or bootstrapping, such as:

- missing `title` or `description`
- empty body content
- missing `sources:` lists on generated pages
- near-duplicate slug collisions
- unclosed code fences
- non-string `type` values that are present but not ideal

This split reflects [[concepts/deterministic-validation]] and [[concepts/graceful-degradation]]: validate reliably, but avoid blocking valid intermediate states unless the rule is structural. It also supports [[concepts/preflight-checks]] and [[concepts/quality-gates]] by separating hard conformance from health signals.

## Implementation Details

The validator is implemented as a standalone Python script with a few notable design choices:

- uses `pathlib` for OS-agnostic filesystem traversal
- uses PyYAML when available, but reports a clear limitation when YAML parsing is unavailable
- strips fenced and inline code before scanning for wikilinks to reduce false positives
- normalizes CRLF to LF when parsing frontmatter
- builds the set of allowed wikilink targets from the wiki's Markdown files
- supports `--strict-warnings` to promote warnings into errors

Its link checking mirrors OpenKB's resolution model by accepting both wiki-relative paths and bare stems, which connects it to [[concepts/openkb-wikilink-resolution]] and [[concepts/knowledge-linking-and-citations]]. The implementation also models [[concepts/deterministic-builds]] and [[concepts/portable-skill-contract]] by keeping the validator portable and repeatable across environments.

## Why It Matters

OKF bundle validation acts as a quality gate for generated or staged knowledge content. It helps detect truncation, merge damage, frontmatter drift, broken graph references, and malformed reserved pages before content is promoted into the compiled wiki.

That makes it part of a broader pipeline involving [[concepts/source-bundling]], [[concepts/source-driven-regeneration]], [[concepts/compiled-knowledge-bases]], [[concepts/knowledge-lifecycle-governance]], and openkb workflow governance. It also supports [[concepts/validation-vs-health-reporting]] by distinguishing conformance failures from recoverable warnings.

## Related Source

- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]