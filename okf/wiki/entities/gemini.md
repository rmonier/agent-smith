---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__graphify__SKILL-md.md"]
type: "Product"
description: "Gemini is the optional semantic extraction backend used by graphify."
---

# Gemini

Gemini is the optional semantic extraction backend referenced in [[summaries/agents__skills__graphify__SKILL-md]] for processing non-code corpus content in [[entities/graphify]]. In this document, it is treated as a product integration that can analyze documents, papers, and images when the appropriate environment variables are already set.

## Role in graphify

Within the graphify workflow, Gemini is used only for semantic extraction, not for structural code analysis. Code extraction is handled separately through AST-based processing, while Gemini is reserved for content that benefits from model-based interpretation.

Key facts from this source:
- Gemini is used only if `GEMINI_API_KEY` or `GOOGLE_API_KEY` is already set.
- If configured, graphify should call Gemini directly for semantic extraction rather than dispatching host-agent subagents.
- The default model named in the document is `gemini-3-flash-preview`.
- The model can be overridden with `GRAPHIFY_GEMINI_MODEL` or a CLI `--model` flag in headless flows.
- Gemini is explicitly not required for code-only corpora.

## Configuration behavior

The source presents Gemini as an optional acceleration path rather than a hard dependency. If Gemini credentials are not present, the workflow continues without blocking and falls back to the host agent for semantic work. This makes Gemini part of a [[concepts/graceful-degradation]] strategy and reflects [[concepts/explicit-provider-routing]] and [[concepts/configuration-precedence]].

The document also states that graphify does not rely on unrelated provider keys for this step. That design narrows ambiguity around which backend should run and supports clearer [[concepts/tool-boundaries]].

## Relationship to graphify features

Gemini appears in the part of the pipeline concerned with:
- semantic extraction from documents, papers, and images
- optional provider-backed parallel extraction
- token-tracked graph construction for [[concepts/multimodal-knowledge-graphs]]
- preserving forward progress when no provider is configured

This places Gemini in the provider layer around [[concepts/provider-integration]] rather than the core graph-building logic itself.

## Related pages

- [[entities/graphify]]
- [[summaries/agents__skills__graphify__SKILL-md]]
- [[concepts/provider-integration]]
- [[concepts/explicit-provider-routing]]
- [[concepts/graceful-degradation]]
- [[concepts/multimodal-knowledge-graphs]]
- [[concepts/tool-boundaries]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]