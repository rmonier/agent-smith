---
type: "Concept"
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md"]
description: "Long documents stored as page-addressable JSON for selective wiki access."
---

# Page-Indexed Sources

Page-indexed sources are long documents stored as structured, page-addressable JSON instead of a single Markdown file. In OpenKB, this format is used for long PDFs so readers and tools can retrieve only the pages they need rather than loading the entire document at once.

## Role in the wiki

Within the wiki layout, source content lives under `wiki/sources/`. Short documents are stored as Markdown, while long PDFs are stored as `wiki/sources/<doc>.json`. This split supports [[concepts/document-normalization]] while preserving an efficient access pattern for large files.

The page-indexed format is part of the compiled knowledge artifact described in [[summaries/agents__skills__openkb__references__wiki-schema-md]]. It complements the summary layer by keeping the full source available in a machine-friendly structure, while concept and summary pages provide higher-level entry points into the same evidence.

## Structure

A page-indexed source is a JSON array of per-page objects. Each entry includes:

- `page`: the 1-indexed page number
- `content`: extracted text for that page
- `images`: references to images associated with that page

This design makes the source directly navigable by page number and gives downstream tools a stable shape for page-level access. It is closely related to [[concepts/schema-constrained-extraction]] because the source is stored in a predictable structured form rather than free-form text.

## Why it exists

The main purpose of page-indexed storage is to support selective reading of very large documents. The OpenKB skill guidance explicitly recommends reading only the needed page from a long-document JSON source, rather than loading the full file, because large compiled sources can be expensive to inspect wholesale.

This makes page-indexed sources useful for:

- targeted evidence lookup
- bounded tool usage on large files
- page-specific inspection of extracted text and images
- efficient workflows for long PDFs
- keeping retrieval focused when answering a narrow question

As a result, the concept aligns with [[concepts/cost-aware-tool-use]], [[concepts/progressive-disclosure]], and [[concepts/evidence-staging]].

## Operational guidance

The recommended access pattern is to retrieve a narrow slice of the JSON array for the relevant page, for example by using `jq '.[N-1]'` where page `N` maps to zero-based array index `N-1`. If `jq` is unavailable, the same page-targeted read can be done with a small Python command.

The important behavior is not the exact command but the access model: retrieve a specific page, not the entire document. This keeps evidence gathering bounded and makes large sources practical to use in agent workflows.

The OpenKB guidance also treats data read from `wiki/` as untrusted content. In that model, output from page-indexed JSON should be handled as source material to inspect, not as instructions to execute. That connects page-level retrieval to [[concepts/wiki-content-as-untrusted-data]] and [[concepts/knowledge-boundaries]].

This is also an example of [[concepts/tool-boundaries]] and [[concepts/safe-automation]] in practice. The format encourages agents and users to work within manageable context windows and avoid wasteful reads.

## Relationship to document classification

Page-indexed sources are the storage format associated with long documents, labeled as `pageindex` in the wiki. The schema distinguishes:

- short documents, stored as Markdown
- long PDFs, stored as paginated JSON

This connection ties the concept to [[concepts/heuristic-classification]] and makes `pageindex` a practical reading-mode signal rather than just a file-format detail.

## Relationship to summaries

A summary page records whether a document is `short` or `pageindex` and points to the corresponding full-text source path. In this way, summaries act as the discovery layer, while page-indexed sources provide the detailed underlying material. This supports [[concepts/index-based-discovery]] and [[concepts/knowledge-base-discovery]] by separating overview from full evidence.

The OpenKB reading workflow reinforces that separation: users and agents typically discover relevant material through the index, summaries, or concept pages first, then open a specific page from a page-indexed source only when deeper evidence is needed.

## Implications for knowledge workflows

Page-indexed sources help OpenKB balance completeness and usability:

- full source content remains available
- long documents stay inspectable without full-file reads
- page-level evidence can be retrieved when needed
- summaries and concepts can reference large documents without embedding all detail
- agents can stage evidence gradually instead of overloading context early

This makes them a key part of scalable document-ingestion and retrieval workflows, especially where large PDFs must remain queryable inside a structured wiki.

## Related pages

- [[summaries/agents__skills__openkb__references__wiki-schema-md]]
- [[summaries/agents__skills__openkb__SKILL-md]]
- [[concepts/document-normalization]]
- [[concepts/schema-constrained-extraction]]
- [[concepts/cost-aware-tool-use]]
- [[concepts/progressive-disclosure]]
- [[concepts/evidence-staging]]
- [[concepts/tool-boundaries]]
- [[concepts/safe-automation]]
- [[concepts/heuristic-classification]]
- [[concepts/index-based-discovery]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/knowledge-boundaries]]