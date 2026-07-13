---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md"]
description: "Distillation can strip constraints when context becomes executable instructions."
---

# Knowledge Distillation Risks

[[concepts/knowledge-distillation-risks]] describes what can go wrong when rich contextual knowledge is compressed into shorter operational instructions, templates, or generated skills. The main risk is that important conditions, caveats, and prohibitions get flattened into simplified steps that appear universally applicable.

## Why this matters

Distillation is useful because it turns large bodies of context into faster, more reusable action guidance. But the compression process can remove the very details that made the original guidance safe and correct. In practice, this means a generated procedure may preserve the headline action while losing the boundaries that say when not to do it, what assumptions must hold, or which exceptions require human review.

This makes the concept especially relevant to [[concepts/skill-based-automation]], [[concepts/durable-context]], and [[concepts/context-action-separation]]. Context often carries nuance; action instructions tend to favor brevity and decisiveness. The gap between those two forms is where distillation failures appear.

## What the source document adds

[[summaries/agents__skills__skill-creator__SKILL-md]] treats this as a concrete operational hazard during skill adoption. When wiki knowledge is turned into an executable skill, the document warns that the resulting instructions may become overly unconditional. It explicitly calls for a caveat-preservation review after adoption so the new skill is compared back against the originating OKF pages and any lost constraints are restored.

The source frames this as more than a wording issue:

- distillation can erase conditional logic,
- safety boundaries can disappear,
- “never do” guidance can be omitted,
- generated instructions can sound more certain than the evidence supports.

That makes [[concepts/caveat-preservation]] a direct mitigation rather than an editorial preference.

## Typical failure modes

Knowledge distillation risks often show up as:

- missing preconditions, where a step is presented without the setup assumptions it depends on;
- lost exceptions, where edge cases from the source context disappear;
- safety erosion, where warnings are dropped because they are not seen as part of the “core” workflow;
- overgeneralization, where a procedure valid in one repository or environment is presented as universally valid;
- false confidence, where a concise artifact appears authoritative even though it is a lossy summary.

These patterns connect to [[concepts/confidence-calibration]], [[concepts/evidence-grounded-answering]], and [[concepts/generated-content-governance]].

## In skill creation workflows

In the skill-authoring context, this concept explains why generated or adapted skills cannot be accepted solely because they are syntactically valid. A skill may pass structural checks yet still fail semantically by omitting the conditions that governed the source material.

This is why the source document pairs generation with review:

- use the wiki as the durable source of context;
- generate or adopt a skill only for true actions;
- compare the adopted result against the original context pages;
- restore constraints, boundaries, and prohibitions that were lost in compression;
- validate the finished skill after those repairs.

That workflow links [[concepts/generated-artifact-adoption]], [[concepts/okf-validation]], [[concepts/executable-validation]], and [[concepts/failure-driven-development]].

## Relationship to context and action

A recurring theme in the source is that context and action should not be collapsed into one artifact. Rich explanation belongs in durable knowledge stores; concise procedures belong in skills. [[concepts/knowledge-distillation-risks]] appears when this separation is respected structurally but handled carelessly procedurally: the action artifact is created, but the translation from context to action drops too much meaning.

This makes the concept closely related to [[concepts/documentation-architecture]], [[concepts/documentation-cohesion]], and [[concepts/knowledge-boundaries]]. Good boundaries help, but they do not eliminate the need for careful transfer between layers.

## Practical mitigations

Useful protections include:

- preserving source links and provenance during generation;
- treating generated artifacts as drafts until reviewed;
- performing side-by-side comparison with the original context;
- explicitly restoring caveats, exclusions, and exception handling;
- validating behavior with realistic scenarios, not just format checks.

These mitigations align with [[concepts/provenance-tracking]], [[concepts/human-in-the-loop-review]], [[concepts/quality-gates]], and [[concepts/baseline-first-testing]].

## Takeaway

[[concepts/knowledge-distillation-risks]] is the risk that compression from knowledge to action removes the limits that made the original knowledge safe and accurate. In [[summaries/agents__skills__skill-creator__SKILL-md]], this is treated as a first-class governance problem: generated skills must be reviewed against their source context so caveats survive the transition from explanation to execution.