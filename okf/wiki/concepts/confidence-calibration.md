---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md"]
description: "Using explicit score rules so graph confidence values stay meaningful and consistent."
---

# Confidence Calibration

Confidence calibration is the practice of assigning confidence labels and scores with an explicit rubric so extracted knowledge graph relationships remain interpretable, comparable, and operationally useful. In [[summaries/agents__skills__graphify__references__extraction-spec-md]], calibration is treated as a schema-level requirement rather than a stylistic preference.

## Why it matters

When extraction systems assign confidence loosely, scores drift toward habitual defaults and stop carrying clear meaning. That makes downstream review, filtering, and graph maintenance less reliable. Confidence calibration addresses this by tying each score to a specific kind of evidence.

In the extraction spec, calibrated scoring supports:

- consistent handling of explicit versus inferred relationships
- clearer review of uncertain edges
- better downstream use in graph merge, filtering, and analysis
- reduced ambiguity in model behavior under structured output constraints

This makes confidence calibration closely related to [[concepts/schema-constrained-extraction]], [[concepts/deterministic-validation]], and [[concepts/knowledge-graph-analysis]].

## Confidence model in the source

The source document defines three confidence classes for edges:

- `EXTRACTED` for relationships directly stated in the source
- `INFERRED` for relationships derived from interpretation
- `AMBIGUOUS` for uncertain but potentially useful relationships that should be surfaced instead of silently omitted

Each class is paired with score rules:

- `EXTRACTED` edges must always use `1.0`
- `INFERRED` edges must use one value from a fixed discrete set: `0.95`, `0.85`, `0.75`, `0.65`, or `0.55`
- `AMBIGUOUS` edges must use a low score in the `0.1` to `0.3` range
- every edge must include `confidence_score`
- `0.5` must never be used as a default

This is a strong example of [[concepts/spec-authority]]: the allowed values are mandated by the specification, not left to model intuition.

## What calibration prevents

The source explains that models tend to collapse vague numeric guidance into a few overused values. In particular, the spec notes undesirable production behavior around default-like scores such as `0.5` and broad clustering at high-confidence values. The discrete rubric is introduced to counter that tendency.

This avoids several failure modes:

- confidence inflation, where too many inferred edges look overly certain
- default-score drift, where one value becomes a catch-all for weak reasoning
- inconsistent interpretation across chunks or runs
- reduced usefulness of confidence as a review and ranking signal

In this sense, confidence calibration contributes to [[concepts/idempotent-graph-import]] and [[concepts/incremental-graph-maintenance]] by making repeated extraction outputs more stable and comparable.

## Evidence tiers

The source document gives a meaning to each allowed inferred score:

- `0.95`: direct structural evidence without an explicit edge
- `0.85`: strong inference with clear functional alignment
- `0.75`: reasonable inference requiring interpretation
- `0.65`: weak thematic relation without shape evidence
- `0.55`: speculative but plausible co-occurrence

A key design choice is that if no score above fits, the extractor should mark the relationship `AMBIGUOUS` rather than inventing a lower inferred score. This preserves the distinction between weak inference and true uncertainty.

That separation aligns with [[concepts/human-in-the-loop-review]] and [[concepts/quality-gates]]: uncertain material is still captured, but clearly flagged for later judgment.

## Calibration as extraction governance

Confidence calibration is not just a scoring trick; it is a governance mechanism for structured extraction. It tells the extractor:

- what counts as explicit evidence
- what kinds of inference are acceptable
- when uncertainty should be preserved rather than hidden
- how to encode those decisions in machine-usable form

This also supports [[concepts/provenance-tracking]] and [[concepts/source-provenance]], because the graph preserves not only where an edge came from but how strongly the system believes it is supported.

## Relationship to ambiguous edges

A notable feature of the source is that ambiguity is not treated as extraction failure. Instead, ambiguous edges should be emitted with low confidence when they are plausible enough to merit review. This reflects a calibrated balance between precision and recall.

That design is useful in settings where omitting uncertain links may hide important relationships, but overstating them would pollute the graph. The result is a graph that remains reviewable without pretending to certainty.

## Practical implications

In practice, confidence calibration improves graph quality when combined with strict schema rules and deterministic extraction behavior. It helps keep scores meaningful across documents, chunk boundaries, and update cycles.

For the graphify extraction prompt, calibrated confidence particularly matters for:

- inferred semantic relationships such as `conceptually_related_to`
- non-obvious `semantically_similar_to` edges
- cross-file code or document interpretations not directly stated in syntax
- uncertain multimodal interpretations from images or diagrams

## See also

- [[summaries/agents__skills__graphify__references__extraction-spec-md]]
- [[concepts/schema-constrained-extraction]]
- [[concepts/deterministic-validation]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/provenance-tracking]]
- [[concepts/source-provenance]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/quality-gates]]
- [[concepts/spec-authority]]

See also: [[summaries/agents__skills__graphify__references__query-md]]