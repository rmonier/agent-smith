---
type: "Summary"
description: "Defines the OpenKB wiki tree, page formats, and wikilink rules."
doc_type: short
full_text: "sources/agents__skills__openkb__references__wiki-schema-md.md"
---

# Summary

This document defines the structure and operating conventions of the OpenKB `wiki/` tree, including where compiled knowledge lives, how page types are organized, what metadata each page carries, and how to navigate content safely.

## Core Structure

OpenKB separates original ingested files from the compiled knowledge artifact:

- `raw/` stores original source files and should not be modified.
- `wiki/` stores the compiled knowledge base used for reading, linking, and synthesis.
- Internal runtime state lives in `.openkb/` and should not be read directly; operational queries should go through CLI commands such as `openkb status` and `openkb list`.

Within `wiki/`, the main areas are:

- `index.md` as the top-level catalog
- `log.md` as the chronological activity log
- `summaries/` for one summary per ingested document
- `concepts/` for cross-document synthesis
- `entities/` for named things such as people, organizations, and works
- `sources/` for converted source content
- `explorations/` for saved query outputs
- `reports/` for auto-generated lint results

This establishes a clear distinction between documentation architecture, source preservation, and synthesized knowledge.

## Index Conventions

`wiki/index.md` is organized into four persistent top-level sections:

- Documents
- Concepts
- Entities
- Explorations

Each entry includes a one-line description. Document entries also include a type tag of either `(short)` or `(pageindex)`, explicitly representing reading mode rather than file extension. Section order is stable and insertion-based rather than alphabetical.

This reflects an emphasis on [[concepts/index-based-discovery]] and predictable catalog structure.

## Summary Pages

A summary page in `wiki/summaries/<doc>.md` contains managed metadata describing:

- the originating source path
- a one-line description
- document type as `short` or `pageindex`
- the path to the converted full text in `sources/`

The body contains an LLM-generated summary plus a `## Related Concepts` section. Summary pages therefore act as the primary bridge between raw source content and higher-level synthesis, connecting closely to document summarization.

## Concept Pages

Concept pages in `wiki/concepts/<slug>.md` aggregate ideas across multiple summaries. They include source references and a one-line description, then use free-form sections plus a `## Related Documents` section.

The document explicitly identifies multi-source synthesis as a high-value part of the compile pipeline. This makes cross-document synthesis central to the OpenKB model.

## Entity Pages

Entity pages in `wiki/entities/<slug>.md` represent named things accumulated across documents. Supported types include:

- person
- organization
- place
- product
- work
- event
- other

Each entity page includes source references, a short description, a `type` field, and a `## Related Documents` section. These pages are intended as the first stop for “who/what is X” questions about named things, tying them to entity-centric knowledge.

## Source Content Formats

OpenKB stores converted source text differently depending on document size:

- Short documents use `wiki/sources/<doc>.md`
- Long PDFs use `wiki/sources/<doc>.json`

Short documents are stored as converted Markdown, including image references under `sources/images/<doc>/`.

Long PDFs are stored as arrays of page objects, each containing:

- `page`
- `content`
- `images`

Because these JSON files can be very large, the document recommends slicing them by page with `jq` rather than reading the entire file. This captures a practical pattern for large-document handling and [[concepts/page-indexed-sources]].

## Wikilink Rules

The wiki uses Obsidian-compatible `wikilink` syntax. Supported forms include:

- direct links such as `attention`
- summary links such as `paper`
- aliased links such as `alias`

Broken links are generally cleaned up by `openkb lint --fix`, so unresolved links usually indicate a manual edit or an in-progress update rather than a system defect. This establishes expectations around [[concepts/wikilink-integrity]] and lint-driven maintenance.

## Short vs Long Classification

The schema distinguishes short documents from long PageIndex documents:

- Non-PDFs and PDFs under 20 pages are treated as short
- PDFs at 20 pages or more are treated as long PageIndex documents
- Short documents map to Markdown source files
- Long documents map to paginated JSON source files

The threshold is configurable, but the recommended way to determine type operationally is via `openkb list`. This reinforces the importance of heuristic classification and CLI-mediated inspection.

## Key Takeaways

- The OpenKB wiki is a structured compiled layer separate from raw content and internal state.
- Summaries, concepts, entities, and explorations each have distinct roles in knowledge organization.
- Long-form sources are page-indexed JSON objects designed for selective access rather than full-file reading.
- Wikilinks are first-class navigation primitives and are expected to resolve after linting.
- Cross-document concept synthesis is treated as one of the most valuable outputs of the system.

## Related Concepts
- [[concepts/generated-content-governance]]
- [[concepts/reserved-wiki-files]]
- [[concepts/llm-wiki]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/incremental-compilation]]
- [[concepts/document-normalization]]
- [[concepts/source-driven-regeneration]]
- [[concepts/path-based-validation]]

- [[concepts/documentation-architecture]]
- [[concepts/index-based-discovery]]
- [[concepts/page-indexed-sources]]
- [[concepts/wikilink-integrity]]
- [[concepts/heuristic-classification]]
- [[concepts/frontmatter-metadata]]

## Entities
- [[entities/wiki-schema-md]]
- [[entities/openkb]]
- [[entities/pageindex]]
- [[entities/okf-spec]]
- [[entities/vectifyai-openkb]]
