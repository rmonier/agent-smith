---
type: "Summary"
description: "Validates one-way tooling link policy and required navigation stubs."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md"
---

# `.agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py`

This script enforces the OpenKB wiki's tooling link-direction rules so local tooling context stays isolated while still discoverable from the bundle root.

## What it does

- Scans Markdown pages under `okf/wiki` and distinguishes `okf/wiki/tooling/` pages from project pages.
- Rejects project OKF concept pages and most indexes when they link back into tooling context.
- Allows the bundle-root `index.md` and `log.md` to mention tooling because they serve navigation and history roles.
- Requires a root `index.md` reference to `tooling/` whenever tooling contains non-reserved pages.
- Requires a committed `tooling/index.md` stub when tooling has pages, since tooling is local-by-default and may be absent on other clones.

## Core policy model

The script formalizes a one-way dependency boundary:

- [[concepts/tooling-context-isolation]] can point outward to project pages.
- Project concepts and indexes must not point back inward to tooling.
- Root navigation files are exempt because they provide entry points rather than dependency edges.

This makes the wiki structure easier to lint, easier to clone safely, and less likely to accumulate hidden local-only dependencies.

## Implementation details

- Uses simple Markdown parsing helpers instead of a full parser.
- Strips fenced code blocks and inline code before scanning for links so examples do not trigger false positives.
- Detects links through both Markdown links and wiki-like path mentions such as `tooling/` and `okf/wiki/tooling/`.
- Reads minimal frontmatter to warn when local tooling pages do not declare `scope: tooling` or `type: tooling-context`.

## Key functions

- `is_tooling_link(target)`: classifies targets that refer to tooling paths.
- `parse_frontmatter(text)`: extracts simple key/value frontmatter fields.
- `strip_code_preserve_lines(text)`: removes code while preserving line numbers for diagnostics.
- `should_scan_for_project_to_tooling_links(rel)`: limits enforcement to project concept pages and navigation indexes.
- `main()`: walks the wiki tree, collects warnings/errors, and enforces the navigation stub requirements.

## Findings and behavior

- Local tooling pages without outgoing wikilinks are treated as structural problems because they risk being orphaned in OpenKB linting.
- Tooling pages that do not declare tooling scope are allowed but warned about, not failed.
- Root `index.md` must explicitly acknowledge tooling when tooling pages exist, making the bundle navigable from clean clones.
- The check is conservative: it prioritizes structure and discoverability over exhaustive Markdown semantics.

## Why it matters

This script codifies [[concepts/tooling-context-governance]] as a controlled, mostly local layer inside the wiki. It protects the main knowledge graph from accidental back-links while preserving enough navigation for users and tooling to find the local harness entry point.

## Related Concepts
- [[concepts/link-directionality]]
- [[concepts/local-by-default-tooling]]
- [[concepts/tooling-link-policy]]
- [[concepts/reserved-navigation-files]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/knowledge-boundaries]]
- [[concepts/documentation-architecture]]
- [[concepts/wikilink-integrity]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/local-tooling-boundaries]]
- [[concepts/reserved-markdown-files]]
- [[concepts/reserved-navigation-files]]
- [[concepts/wiki-context-routing]]

## Entities
- [[entities/validate_tooling_link_policy-py]]
- [[entities/okf-wiki-tooling-index-md]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-tooling]]
- [[entities/okf-wiki]]
- [[entities/openkb]]
- [[entities/okf]]
- [[entities/subagent-profile-adapter]]
- [[entities/openkb-cli]]
- [[entities/validate_okf_bundle-py]]
- [[entities/references-tooling-context-policy-md]]
- [[entities/tooling]]
- [[entities/okf-spec]]
