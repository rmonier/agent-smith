---
type: "Summary"
description: "Guidance for fetching harness docs and recording adapter-relevant tooling context."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__references__harness-docs-md.md"
---

# Summary

This document defines how to handle harness documentation when building or updating a subagent profile adapter, especially when profile semantics are unclear or may have changed.

## Key points

- Retrieve current harness documentation before writing adapters if profile behavior is unknown or potentially outdated.
- Follow a clear evidence order for documentation sources:
  1. Official local harness documentation available in the current environment.
  2. Official web documentation.
  3. User-provided documentation URLs or snippets.
  4. Community examples only as secondary support.
- Create a concise tooling-context record at `okf/wiki/tooling/harnesses/<harness>.md`.
- The tooling page should capture only adapter-relevant facts, not large copied excerpts from source docs.

## Required tooling-context contents

The tooling page should include:

- official source URL or local documentation reference;
- retrieval timestamp;
- supported profile or subagent paths;
- required frontmatter fields;
- permissions or tool model, if documented;
- instruction-file behavior, if documented;
- the generation policy selected by the user.

## Wiki maintenance requirements

After creating the tooling page:

- update `okf/wiki/index.md` so `tooling/` appears in the harness-specific section;
- record the change in `okf/wiki/log.md`;
- ensure `okf/wiki/AGENTS.md` declares the custom section.

The document notes that `references/tooling-context-policy.md` governs this behavior and that a link-policy validator will fail if tooling pages exist without the required index entry.

## Likely concepts

- [[concepts/documentation-source-priority]]
- [[concepts/tooling-context-pages]]
- [[concepts/runtime-adapter-management]]
- [[concepts/reserved-wiki-files]]
- [[concepts/wikilink-integrity]]

## Takeaway

The main contribution is a compact workflow for [[concepts/runtime-adapter-management]]: verify current documentation from authoritative sources, extract only adapter-critical metadata into a tooling page, and keep related wiki index and log structures synchronized.

## Related Concepts
- [[concepts/tooling-context-isolation]]
- [[concepts/agents-md-maintenance]]
- [[concepts/external-documentation]]
- [[concepts/source-trust-levels]]
- [[concepts/provenance-tracking]]
- [[concepts/okf-validation]]
- [[concepts/path-based-validation]]
- [[concepts/frontmatter-metadata]]
- [[concepts/documentation-architecture]]
- [[concepts/knowledge-linking-and-citations]]

## Entities
- [[entities/agents-md]]
- [[entities/openkb]]
- [[entities/okf-spec]]
- [[entities/okf-readme]]
