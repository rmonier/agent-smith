---
sources: ["summaries/karpathy-llm-wiki-gist.md"]
type: "Product"
description: "Markdown knowledge editor and wiki browser"
---

# Obsidian

Obsidian is a markdown-based knowledge base editor used as the front-end for the LLM wiki workflow described in [[summaries/karpathy-llm-wiki-gist]]. It serves as the human-facing interface for browsing, editing, and inspecting an LLM-maintained wiki.

## Role in the wiki pattern

In the gist, Obsidian is described as the practical workspace where the wiki becomes visible and navigable. The LLM acts as the maintainer, while Obsidian is the IDE for the knowledge base: pages are read, linked, revised, and explored there in real time.

## Why it matters

Obsidian supports the core [[concepts/llm-wiki]] pattern by making the compiled wiki easy to inspect and curate. Its graph view helps reveal the structure of the knowledge base, including hubs, orphans, and clusters of related pages.

## Associated uses

- Browsing and editing generated wiki pages
- Following wikilinks between summaries, concepts, and entities
- Inspecting graph structure to understand coverage and connectivity
- Supporting local, markdown-first knowledge workflows

## Related concepts

- [[concepts/compiled-knowledge-bases]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/graph-structure-analysis]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/llm-maintained-wikis]]
