---
sources: ["summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"]
type: "Work"
description: "OpenKB's lint module for wiki structural validation"
---

# openkb.lint

`openkb.lint` is the OpenKB module that provides the read-only validation APIs used by the editorial curation pass. In `[[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]`, it supplies the public checks that verify wiki integrity without reimplementing OpenKB's own logic.

## What it does

This module exposes the stable lint functions that the curation script invokes through the installed OpenKB environment:

- `list_existing_wiki_targets`
- `find_broken_links`
- `find_orphans`
- `check_index_sync`
- `find_invalid_frontmatter`
- `find_missing_okf_fields`

These checks cover link integrity, orphan detection, index consistency, and frontmatter/schema validity.

## Role in curation

The editorial pass uses `openkb.lint` as the vendor-backed validation layer for `[[concepts/deterministic-validation]]` and `[[concepts/vendor-backed-validation]]`. Its results help enforce:

- no dangling or invented wiki links
- no stale or missing index entries
- no invalid frontmatter
- no missing OKF-required fields
- no unapproved structural drift in compiled knowledge pages

## Behavior in the script

The script treats `openkb.lint` as a stable public API and fails loudly if those imports or calls break. That makes the environment itself part of the safety guarantee for `[[concepts/editorial-curation-passes]]` and `[[concepts/quality-gates]]`.

## Related concepts

- [[concepts/openkb-wiki-health-checks]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/deterministic-validation]]
- [[concepts/vendor-backed-validation]]
- [[concepts/wikilink-integrity]]
- [[concepts/frontmatter-metadata]]
- [[concepts/okf-validation]]

See also: [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]]