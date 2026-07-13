---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Other"
description: "API key that enables PageIndex Cloud for PDF processing"
---

# PageIndex API Key

`PageIndex API Key` is the credential that enables optional PageIndex Cloud handling for long PDFs in the OpenKB pipeline.

## Key facts

- If `PAGEINDEX_API_KEY` is unset, long PDF processing stays local by default through PageIndex.
- If `PAGEINDEX_API_KEY` is set, the pipeline may use PageIndex Cloud instead of the local-only path.
- Its presence is treated as a privacy-relevant toggle because it changes where PDF content may be processed.
- The document recommends leaving it unset for [[concepts/air-gapped-operation]] and other local-first workflows.

## Related context

- The handling rule is documented in [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]].
- This credential is part of the broader [[concepts/provider-routing]] and [[concepts/privacy-preserving-tooling]] concern set.
- It also relates to [[entities/pageindex]] and [[entities/pageindex-cloud]].

## Practical implication

- Unset means local-only PDF handling is preferred.
- Set means PDF processing may involve a cloud service, so the operator should expect a different data flow.
