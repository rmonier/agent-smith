---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Captured discoveries promoted into the wiki's durable memory layer"
---

# Findings

Findings are captured discoveries that enter the wiki as durable knowledge rather than repository documentation. In the OpenKB lifecycle, they serve as the working-memory layer for observations that were learned from runtime behavior, code comments, operational issues, or other evidence that was not already stated in committed source docs.

## What a finding is

A finding is used when an agent discovers something important that should be preserved in the KB, but the knowledge did not originate in the repository's normal documentation flow. This includes:

- behavior observed while running the project
- constraints hidden in code comments or implementation details
- operational gotchas that are not documented elsewhere
- knowledge that was cropped out of staged source material

Findings are distinct from compiled repository facts: a repository fact belongs in source-driven ingestion, while a finding belongs in the exploratory capture layer.

## Capture and promotion

The lifecycle doc describes a two-step process:

1. Capture the discovery in `okf/wiki/explorations/findings/<topic>.md`.
2. Promote it only when it is still true at HEAD and conflicts with or fills a gap in compiled pages.

Promotion is done by staging the finding into `okf/.okf-build/findings/` and ingesting it with OpenKB. Once promoted, the finding becomes part of the compiled wiki and can coexist with older repository documentation if the evidence supports it.

## Why findings matter

Findings let the KB retain useful discoveries without forcing them into human-authored project docs. That separation supports evidence grounded answering, because the wiki can store observations with explicit evidence rather than silently overwriting older claims.

They also support generated content governance by keeping the compiled wiki aligned with committed source material while still allowing discovered knowledge to be recorded. In that sense, findings are a bridge between evidence staging and durable wiki content.

## Relationship to other concepts

Findings are closely related to source driven regeneration because promoted knowledge is re-ingested through the normal compilation flow, not hand-edited into generated pages. They also depend on provenance tracking and wiki content as untrusted data, since each finding should carry evidence and the KB should never treat a page as authoritative without checking its source.

The lifecycle document also ties findings to read only kb operations and consent first tooling by making capture free and promotion deliberate. That keeps the system conservative: discoveries are easy to record, but truth mutation happens only through a controlled lifecycle.

## Practical role in the wiki

Within the wiki, findings are the place to preserve:

- contradictions that should remain visible
- evidence-backed observations not present in repository docs
- interim knowledge that may later become a concept or entity page
- operational lessons that guide future maintenance

This makes findings an important part of the KB's feedback loop: they allow the wiki to absorb new knowledge without losing the distinction between observed behavior and documented intent.

## Source basis

This concept is defined by [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], which explains how findings fit into the OpenKB lifecycle, how they are captured, and how they are promoted or dropped during refresh cycles.