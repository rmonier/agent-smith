---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Controlled wiki edits used only as a last-resort curation path."
---

# Guarded Wiki Curation

Guarded wiki curation is the narrowly scoped exception path for fixing OpenKB output when the problem is not a source document and not a discoverable knowledge gap. In the agent-ready-context workflow, it exists for semantic-lint cases where the compiled wiki has an output-only issue such as near-duplicates, overly sprawling pages, or a misfiled concept/entity, and the source material itself is not at fault.

## Why it exists

The default rule is to avoid hand-editing compiled wiki pages. The preferred repair loop is:

1. improve the committed source documents
2. re-stage deterministic input
3. re-ingest with OpenKB
4. validate the refreshed wiki

That loop preserves [[concepts/source-driven-regeneration]], [[concepts/caveat-preservation]], and [[concepts/provenance-tracking]] better than direct edits. Guarded curation is reserved for the rare case where regeneration is not the right fix.

## When it applies

This path is used when:

- the wiki output is structurally correct but needs editorial cleanup
- the issue is a pure compilation artifact rather than a source defect
- no new factual claim needs to be added
- the corrective change can be limited to concepts, entities, or the root index

The source document explicitly treats this as the last-resort channel after the correction loop and the findings channel do not fit.

## How it is controlled

Guarded curation is not an open-ended hand-edit flow. It is constrained by a deterministic review step:

- run `scripts/editorial_pass.py --brief`
- make only curation-only edits in the allowed wiki areas
- run `scripts/editorial_pass.py --check`

The check step verifies that the diff stays within scope and provenance rules before validation and re-linting. This makes the process closer to [[concepts/quality-gates]] than to freeform editing.

## Relationship to other workflows

Guarded wiki curation sits beside, but does not replace, the normal knowledge lifecycle:

- [[concepts/findings]] captures discovered knowledge that should be triaged into the KB later
- [[concepts/generated-content-governance]] covers the broader rules for handling compiled output
- [[concepts/documentation-layer-separation]] keeps action procedures, durable context, and orientation material distinct
- [[concepts/knowledge-lifecycle-governance]] frames the overall policy for when knowledge moves through the system

In other words, guarded curation is for fixing the shape of compiled knowledge, not for introducing new knowledge.

## Source context

The concept is defined in the repository's agent-ready-context skill, which establishes the repository as a managed OpenKB workspace and sets the boundary rules for wiki updates, findings capture, and editorial exceptions. See [[summaries/agents__skills__agent-ready-context__SKILL-md]] for the full workflow context.

## Key properties

- last-resort only
- deterministic and reviewable
- limited to output curation
- avoids changing source-of-truth content unless necessary
- preserves the compiled wiki as a governed artifact rather than an ad hoc note store