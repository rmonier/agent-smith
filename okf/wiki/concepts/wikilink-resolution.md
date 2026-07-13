---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "How wiki links are resolved against local page targets."
---

# Wikilink Resolution

Wikilink resolution is the process of mapping `...` references to existing wiki pages using the local page inventory, so internal links can be validated without relying on external systems.

## Core Rule Set

The validator in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] implements a local resolution model that mirrors OpenKB behavior closely enough for linting.

A wikilink target is considered valid when it matches one of these forms:

- the page's wiki-relative path without the `.md` extension
- the page's bare filename stem

This means a page such as `concepts/example-page.md` can be referenced as either `example page` or `example page`.

## Normalization

Before checking links, the validator strips away non-target syntax:

- alias text after `|` is ignored
- surrounding whitespace is trimmed
- a leading or trailing `/` is removed

The scanner also ignores links found inside fenced code blocks and inline code spans, which reduces false positives from examples and documentation snippets.

## Validation Behavior

In `--openkb-wiki` mode, broken wikilinks are treated as errors rather than warnings. That makes link integrity part of the structural health of the wiki, not just a cosmetic issue.

The validator builds the set of valid targets from every Markdown file in the bundle, then compares each parsed wikilink against that set. If a target is missing, it reports a broken link.

## Why It Matters

Wikilink resolution supports several broader wiki goals:

- [[concepts/wikilink-integrity]] by catching broken references early
- [[concepts/openkb-wikilink-resolution]] by enforcing OpenKB-specific link rules
- [[concepts/wiki-review-gates]] by making link health part of validation
- [[concepts/document-normalization]] by standardizing how references are interpreted
- [[concepts/graph-integrity-diagnostics]] by surfacing structural damage in the knowledge graph

## Practical Implications

This resolution model is intentionally simple and local:

- it does not require network access
- it works on the filesystem snapshot in front of the validator
- it favors deterministic checks over heuristic guessing
- it treats link correctness as a compile-time property of the wiki bundle

That makes it useful for [[concepts/deterministic-validation]] and for maintaining [[concepts/compiled-knowledge-bases]] where references must remain traceable.

## Related Checks

Wikilink resolution is paired with other safeguards in the source validator:

- frontmatter validation ensures pages are structurally parseable
- reserved-file handling keeps `index.md` and `log.md` separate from ordinary concept pages
- unclosed fence detection helps catch truncated pages before they produce misleading links
- near-duplicate slug detection warns when names may collapse to the same target shape

Together, these checks keep the wiki's internal graph coherent and reduce the chance that a link points to a page that exists in name only.