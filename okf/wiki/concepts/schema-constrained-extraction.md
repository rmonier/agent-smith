---
type: "Concept"
sources: ["summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md"]
description: "Constraining extraction outputs to a strict schema for reliable graph ingestion."
---

# Schema-Constrained Extraction

Schema-constrained extraction is the practice of requiring an extraction agent to emit data in a fixed, validated structure so the result can be merged, checked, and consumed without manual cleanup. In this wiki, it is closely tied to graph-building workflows where extraction output must be precise enough for downstream automation to trust. See [[summaries/agents__skills__graphify__references__extraction-spec-md]].

## Why it matters

Unconstrained extraction tends to drift in small but costly ways:

- field names vary across runs
- optional values disappear unpredictably
- identifiers become inconsistent
- confidence values collapse to vague defaults
- provenance gets shortened or normalized incorrectly

A strict schema turns extraction into a contract rather than a suggestion. That supports [[concepts/deterministic-validation]], [[concepts/okf-validation]], and [[concepts/idempotent-graph-import]].

## Core pattern

In the referenced extraction spec, the subagent is instructed to output only valid JSON with exact top-level keys for `nodes`, `edges`, `hyperedges`, and token counts. The allowed fields, relation types, and value sets are explicitly enumerated. This reduces ambiguity at generation time instead of trying to repair output later.

The pattern combines several controls:

- exact output format requirements
- closed sets of valid enum-like values
- required fields on every object
- deterministic identifier rules
- fixed provenance copying rules
- explicit write-path behavior

Together these make extraction compatible with [[concepts/generated-content-governance]] and [[concepts/single-source-of-truth]].

## Constraints used in practice

The source document shows that schema constraints are not only about shape, but also about semantics.

### Closed value sets

The extraction spec limits `file_type` to exactly six values: `code`, `document`, `paper`, `image`, `rationale`, and `concept`. Any other value is invalid. Likewise, edges may only use a fixed set of relations, and confidence labels are restricted to `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`.

Closed sets improve consistency and make downstream validation simpler. This aligns with [[concepts/path-based-validation]] and [[concepts/filesystem-validation]] in spirit: the system prefers explicit allowed forms over heuristic acceptance.

### Required fields

Every edge must include a `confidence_score`, and omission is not allowed. This is especially important because confidence is part of the decision logic for review and graph trust. The spec also requires provenance fields such as `source_file`, with exact handling rules.

This reflects a broader commitment to [[concepts/provenance-tracking]] and [[concepts/source-provenance]].

### Deterministic identifiers

The spec requires node IDs derived from the full repo-relative path plus normalized entity name, with all path segments preserved and chunk suffixes forbidden. This prevents duplicate or orphaned graph nodes across reruns and chunk boundaries.

This directly supports [[concepts/naming-normalization]], [[concepts/incremental-graph-maintenance]], and [[concepts/deterministic-builds]].

### Semantic constraints

The schema is reinforced by domain rules. For example:

- `calls` edges must point from caller to callee
- cross-language `calls` edges must never be emitted
- imports should not be re-extracted if AST tooling already captures them
- rationale should be attached to concept-like nodes rather than modeled as a separate free-floating node type

These rules show that schema-constrained extraction is not just formatting discipline; it encodes model behavior boundaries. That relates to [[concepts/link-directionality]], [[concepts/tool-boundaries]], and [[concepts/knowledge-boundaries]].

## Confidence as a schema concern

A notable detail from the source is the use of a discrete scoring rubric for inferred edges. Instead of allowing arbitrary continuous values, the spec limits inferred confidence scores to a small approved set and explicitly forbids `0.5` as a default. Ambiguous edges must use a low score band instead of being silently dropped.

This is a strong example of schema design shaping model behavior. By constraining score choices, the system reduces score collapse and improves comparability across runs. See [[concepts/confidence-calibration]].

## Provenance fidelity

The extraction spec requires `source_file` to be copied exactly as listed in the input file list, without shortening, re-relativizing, or changing separators. It also propagates selected frontmatter metadata onto every node from a file when present.

This level of strictness preserves build consistency and merge correctness during updates. It connects schema-constrained extraction to [[concepts/frontmatter-metadata]], [[concepts/document-normalization]], and [[concepts/incremental-compilation]].

## Hyperedges and bounded flexibility

The schema allows richer structures such as hyperedges, but only in a tightly bounded way: they must be used sparingly, capped per chunk, and reserved for group relationships that add information beyond pairwise edges. This is an example of controlled expressiveness: the schema expands capability without allowing arbitrary structure growth.

That balance reflects [[concepts/quality-gates]] and [[concepts/safe-automation]].

## Design implications

Schema-constrained extraction works best when the prompt and the validator agree on the same contract. In the source document, this shared contract covers:

- what can be emitted
- how it must be named
- which values are legal
- how uncertainty is represented
- how provenance is preserved
- where output must be written

This reduces repair work, makes failures easier to diagnose, and improves reliability in automated knowledge-graph pipelines. It is especially useful in systems that need repeatable ingestion rather than one-off summarization.

## Related pages

- [[summaries/agents__skills__graphify__references__extraction-spec-md]]
- [[concepts/confidence-calibration]]
- [[concepts/deterministic-validation]]
- [[concepts/idempotent-graph-import]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/source-provenance]]
- [[concepts/provenance-tracking]]
- [[concepts/naming-normalization]]
- [[concepts/link-directionality]]
- [[concepts/safe-automation]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]