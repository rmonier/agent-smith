---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"]
description: "Keeping merged wiki sources citations complete and unchanged."
---

# Provenance Union Governance

Provenance union governance is the rule that when compiled knowledge pages are merged or split, their `sources:` lists must remain complete, conservative, and traceable. The goal is to preserve every original source citation across the resulting wiki graph, while preventing invented provenance from entering the compiled knowledge base.

This concept is central to guarded editorial curation passes such as [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]], which checks curation diffs for provenance loss or fabrication before changes are accepted.

## Core rule

When multiple compiled pages are consolidated, the survivor's provenance must be the union of the merged pages' `sources:` values. No source may disappear simply because content moved or was reorganized, and no new source may be added unless it already existed in the pre-edit state.

In practice, this means:

- a merge may combine `sources:` lists from several pages
- a split must preserve the original source set across the resulting pages
- every changed concepts or entities page must still have a non-empty `sources:` list
- provenance changes are allowed only if they preserve the full pre-edit union

## Why it matters

Provenance is part of the wiki's trust model. The source list is not just metadata; it is evidence of where compiled knowledge came from. If source citations are lost during a curation pass, later readers can no longer tell whether a page still reflects the same evidence base.

This governance rule supports several adjacent ideas:

- [[concepts/provenance-tracking]] for retaining evidence lineage
- [[concepts/source-provenance]] for tying claims to origin documents
- [[concepts/conservative-document-merging]] for avoiding accidental loss during consolidation
- [[concepts/generated-content-governance]] for controlling how derived wiki pages are edited
- [[concepts/read-only-kb-operations]] as the backdrop that makes provenance checks especially important during manual edits

## How the editorial pass enforces it

The `editorial_pass.py` checker computes the union of all `sources:` values across `wiki/concepts/` and `wiki/entities/` at the git base and compares that to the union after the working-tree edit. It then reports two kinds of violations:

- `provenance-lost` when a source present before the edit is no longer cited anywhere in compiled pages
- `provenance-invented` when a new source appears that was not present at the base revision

That approach treats provenance as a graph-level invariant rather than a page-by-page preference. It is specifically designed for merge-style editorial work, where the content may be reorganized but the evidence set should remain unchanged.

## Relationship to other governance checks

Provenance union governance sits alongside other validation rules in the curation workflow:

- [[concepts/wikilink-integrity]] ensures links still resolve after edits
- [[concepts/okf-validation]] covers broader schema and bundle correctness
- [[concepts/deterministic-validation]] keeps checks reproducible and non-LLM
- [[concepts/okf-wiki-governance]] provides the broader governance frame for wiki changes
- [[concepts/wiki-review-gates]] describes the approval boundary around compiled knowledge edits

## Practical implication

A curation pass can reorganize pages, tighten language, or merge duplicates, but it cannot quietly rewrite the evidence trail. Provenance union governance makes the wiki safer to maintain by requiring that edits preserve the total cited-source set of the compiled knowledge being edited.
