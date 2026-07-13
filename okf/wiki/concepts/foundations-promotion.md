---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Rules for promoting durable findings into the compiled OKF wiki."
---

# Findings Promotion

Findings promotion is the workflow for deciding when a captured finding should become part of the compiled knowledge base rather than remain in a working capture area.

## Purpose

The goal is to preserve durable discoveries without letting stale, refuted, or redundant material pollute the wiki. Promotion is part of the broader [[concepts/editorial-curation-passes|editorial curation passes]] and supports [[concepts/knowledge-lifecycle-governance|knowledge lifecycle governance]] by separating transient investigation notes from compiled pages.

## When A Finding Should Be Promoted

A finding is promoted only when it is still true at HEAD and the compiled wiki does not already cover it well enough. In practice, that means the finding is:

- still valid in the current repository state,
- missing from the compiled pages, or contradicting them,
- specific enough to be worth preserving as durable knowledge,
- grounded in evidence rather than inference or speculation.

This keeps promotion aligned with [[concepts/provenance-tracking|provenance tracking]] and [[concepts/evidence-grounded-answering|evidence-grounded answering]].

## When A Finding Should Not Be Promoted

A finding is kept or dropped instead of promoted when:

- it is true but not in conflict with the compiled wiki,
- it has been refuted by newer evidence,
- it is too transient, narrow, or duplicate to justify a compiled page,
- it would create a near-duplicate of an existing concept or entity page.

This supports [[concepts/generated-content-governance|generated content governance]] and reduces [[concepts/documentation-gaps|documentation gaps]] without introducing clutter.

## Promotion Workflow

The workflow described in the build process is intentionally conservative:

1. Review findings captured under `okf/wiki/explorations/findings/`.
2. Promote only the findings that are still true and still missing from the compiled wiki.
3. Stage the promoted item as a new finding input under `okf/.okf-build/findings/`.
4. Remove the original capture page and its `index.md` entry.
5. Re-ingest the promoted findings so the hash registry can skip already-ingested content and only new material lands in the KB.

This makes promotion part of the deterministic [[concepts/source-driven-regeneration|source-driven regeneration]] loop rather than an ad hoc wiki edit.

## Relationship To Other Workflow Rules

Finding promotion is closely tied to several other policies:

- [[concepts/orphan-retraction]]: removed or moved sources should be reconciled before ingesting fresh material.
- [[concepts/manifest-authoritative-reconciliation]]: staged inputs should reflect the current repository structure.
- [[concepts/human-in-the-loop-review]]: promotion decisions are reviewed in-session rather than automated away.
- grounded answering: promoted findings must remain traceable back to the evidence chain.
- [[concepts/knowledge-capture-boundaries]]: working captures and compiled knowledge should stay distinct.

## Practical Effect

Promotion is not about increasing volume. It is a filtering step that decides which discoveries deserve a durable home in the compiled wiki and which should remain as temporary working material or be discarded.

In the OpenKB workflow, this keeps the knowledge base current, grounded, and free of obsolete investigative residue while still allowing useful discoveries to survive beyond a single run.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
