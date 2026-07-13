---
type: "Summary"
description: "Template excludes the compiled knowledge base from repository graphing."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__assets__graphifyignore-template.md"
---

# Summary

This source file is a `.graphifyignore` template used by the `agent-ready-context` workflow to prevent the compiled OpenKB knowledge base from being included in repository graph analysis.

## Key Points

- The template ignores the `okf/` directory.
- Its purpose is to keep generated knowledge-base artifacts out of the repository graph.
- The file frames the wiki as a representation of the repository rather than part of the repository itself.
- Including generated wiki pages in graph analysis would create a self-reinforcing ingestion cycle in which generated outputs are re-analyzed and re-ingested.
- The comment explicitly identifies this as a non-converging feedback loop and points readers to a workflow reference for the self-reference policy.

## Main Idea

The document encodes a boundary between source material and generated artifacts. This supports [[concepts/generated-content-governance]], [[concepts/self-reference-control]], and [[concepts/knowledge-boundaries]] by ensuring that graph-based analysis operates only on the underlying repository content, not on derivative knowledge products.

## Implications

- Helps preserve the integrity of graph reports by avoiding recursive contamination from generated files.
- Establishes an operational rule for knowledge-base compilation workflows.
- Serves as a practical safeguard against runaway or misleading graph expansion in automated documentation pipelines.

## Related Concepts
- [[concepts/knowledge-graph-analysis]]
- [[concepts/repository-ingestion]]
- [[concepts/llm-wiki]]
- [[concepts/source-driven-regeneration]]
- [[concepts/okf-validation]]

## Entities
- [[entities/graphify]]
- [[entities/openkb]]
- [[entities/agent-ready-context]]
