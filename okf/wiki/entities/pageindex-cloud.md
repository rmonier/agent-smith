---
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
type: "Product"
description: "Optional hosted PageIndex service for PDF processing in OpenKB"
---

# PageIndex Cloud

PageIndex Cloud is the optional hosted OpenKB service used for PDF OCR and markdown conversion when a user explicitly opts in with `PAGEINDEX_API_KEY`.

## What it does

- Handles PageIndex processing in the cloud instead of locally.
- Uploads PDFs for OCR and conversion when enabled.
- Stays off by default; the local PageIndex pipeline is the normal path.
- Fits into the broader consent-first tooling model described in the repository, where cloud-backed tools are explicit and user-approved rather than always-on dependencies.

## Key facts from the source

- `pageindex_threshold` controls when PageIndex handling is triggered.
- The local PageIndex flow is the default behavior.
- `PAGEINDEX_API_KEY` is the switch that opts into PageIndex Cloud.
- The source treats this as a configuration choice, not a required dependency.
- Long PDFs through PageIndex stay local by default, and PageIndex Cloud is only used when `PAGEINDEX_API_KEY` is set.
- Leaving `PAGEINDEX_API_KEY` unset preserves the local-only path.
- Cloud PDF handling is one of the few explicit data-flow exceptions in the pipeline, alongside other consent-gated external services.

## Related knowledge

- The provider guidance lives in [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]].
- This service fits into [[concepts/provider-integration]] and [[concepts/page-indexed-sources]].
- Its opt-in nature aligns with [[concepts/consent-first-tooling]] and [[concepts/offline-first-workflows]].
- It also touches [[concepts/privacy-preserving-tooling]] because cloud processing sends document content off-machine.
- The privacy and data-flow guidance frames PageIndex Cloud as an explicit routing choice with a local default, not a silent fallback.

## Notes

- PageIndex Cloud is separate from the local OpenKB runtime.
- The document presents it as an optional acceleration/processing path rather than a default requirement.
- In the repository's model, it belongs to the class of explicit, user-approved external services that support the agent-ready pipeline without becoming the source of truth.

## Related Documents
- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]