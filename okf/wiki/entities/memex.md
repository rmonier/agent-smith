---
sources: ["summaries/karpathy-llm-wiki-gist.md"]
type: "Work"
description: "Vannevar Bush's 1945 vision of associative personal knowledge storage"
---

# Memex

A conceptual personal knowledge machine proposed by Vannevar Bush in 1945.

## Overview

Memex is the historical precursor most often associated with associative knowledge navigation: a private, curated system for storing documents and linking them through trails of related ideas rather than relying only on linear filing. In the karpathy-llm-wiki-gist, Memex is cited as an inspiration for the [[concepts/llm-wiki]] pattern because it captures the value of maintaining connections between documents over time.

## Why it matters

Karpathy uses Memex to frame the idea that the hard problem is not only storing information, but maintaining the relationships between pieces of information. The gist argues that LLMs can solve the part Bush could not: the maintenance work required to keep a personal knowledge system current, cross-linked, and useful.

## Relation to LLM wikis

In the modern wiki pattern described in the gist, the LLM maintains a persistent, interlinked knowledge base built from raw sources. That makes Memex relevant as a conceptual ancestor of [[concepts/compounding-knowledge-bases]] and [[concepts/llm-maintained-wikis]]:

- both emphasize curated personal or organizational knowledge rather than passive retrieval,
- both treat links between documents as first-class knowledge,
- both aim to support discovery through association rather than isolated search hits.

## Notes

- Memex is presented as an idea rather than a realized product.
- The gist treats it as a useful historical comparison, not as a direct implementation model.
- Its main legacy in this context is the emphasis on associative trails and curated knowledge over time.

## Related Documents
- [[summaries/karpathy-llm-wiki-gist]]
