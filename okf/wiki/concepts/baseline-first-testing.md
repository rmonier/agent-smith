---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md"]
description: "Testing skills by capturing unaided failures before writing fixes."
---

# Baseline-First Testing

[[concepts/baseline-first-testing]] is the practice of evaluating a task before introducing a skill, capturing the exact points of failure, and then writing the skill to address those observed gaps rather than imagined ones.

## Core idea

The concept treats the no-skill run as the baseline. Instead of starting from a preferred workflow or a speculative template, the author first asks the agent to perform the target task without the skill. The resulting mistakes, omissions, rationalizations, and inefficient workarounds become the evidence for what the skill actually needs to contain.

This keeps the skill grounded in demonstrated need:

- record what fails without the skill
- identify which failures are recurring, costly, or easy for the agent to rationalize away
- add only the instructions, checks, scripts, or structure needed to close those gaps
- rerun the task and refine until the remaining failure modes are addressed with explicit counters

In the skill-creation guidance, this baseline is framed through a pressure scenario: a realistic task that has previously caused the agent to slip. Typical failures include skipping required steps, rewriting fragile logic instead of using deterministic scripts, mixing durable context with action guidance, editing vendor skills directly, putting long-lived knowledge into `AGENTS.md`, using overly broad tool access, omitting validation and provenance, or flattening conditional caveats into unconditional steps.

## Why it matters

Baseline-first testing improves skill quality in several ways:

- It reduces unnecessary instructions, which supports [[concepts/progressive-disclosure]] and helps preserve limited model attention.
- It makes the skill evidence-driven rather than preference-driven, aligning with [[concepts/deterministic-validation]] and [[concepts/quality-gates]].
- It exposes whether a problem belongs in the skill at all, or whether it is really a context, tooling, or repository-structure issue related to [[concepts/context-action-separation]].
- It helps avoid vague or decorative skill content, such as narrative examples or generic guidance that does not fix a demonstrated failure.
- It turns pressure-scenario failures into concrete test cases, which supports [[concepts/failure-driven-development]] and [[concepts/executable-validation]].
- It keeps skills short and procedural by proving which details deserve to stay in `SKILL.md` and which belong in scripts, references, or assets.
- It provides evidence for matching the skill's degree of specificity to task fragility: destructive or brittle actions need narrower, more deterministic guidance, while open-ended tasks can stay principle-led.

## In the source documents

[[summaries/agents__skills__skill-creator__references__source-attribution-md]] identifies baseline-first testing as a major influence inherited from [[entities/superpowers-writing-skills]]. The source describes the discipline as:

- run the target task without the skill first
- record the exact failures
- write the skill against those failures
- close remaining loopholes through iteration

[[summaries/agents__skills__skill-creator__references__testing-skills-md]] expands this into a full testing loop built around realistic pressure scenarios. It describes a baseline-red, write-green, close-loopholes-refactor cycle, followed by running `uv run scripts/quick_validate.py <skill-dir>`. It also stresses that the goal is to respond to observed failures rather than hypothetical ones, and that each remaining loophole should be closed by stating the reasoning behind the constraint, not just adding a prohibition.

[[summaries/agents__skills__skill-creator__SKILL-md]] reinforces the same method at the top-level workflow for creating or updating skills. It makes baseline-first testing the default creation discipline: run a pressure scenario without the skill, record the actual failures, write the skill against them, and then validate the finished skill. It also adds several important constraints:

- test each skill individually rather than batch-creating several at once
- use the baseline to decide whether the needed fix belongs in `SKILL.md`, `scripts/`, `references/`, or outside the skill entirely
- treat the baseline as a way to confirm the trigger is a repeatable action, not merely durable context better kept in OpenKB or `AGENTS.md`
- use validation as a required finish condition rather than an optional cleanup step

Taken together, these sources present baseline-first testing as both a design method and a validation discipline: a skill should be as small as possible while still correcting the failures seen in practice and proving that it does so under pressure.

## Practical implications for skill creation

When applying baseline-first testing to a new skill:

- Start with the real task, not the intended documentation structure.
- Use at least one realistic pressure scenario that has previously caused failure.
- Capture concrete failure evidence before drafting instructions.
- Prefer targeted corrections over broad policy text.
- Validate whether each added section fixes a known failure mode.
- Add explicit reasoning where the agent still finds loopholes.
- Create and test one skill at a time instead of batching multiple new skills together.
- Use the baseline to decide when deterministic behavior should move into `scripts/` rather than being repeatedly described in prose.
- Keep `SKILL.md` short and procedural, pushing heavy detail into references only when the baseline shows it is needed.
- Use the baseline to verify whether generated or adopted skill content preserved important boundaries, conditions, and "never do" caveats.
- Let the observed failures guide security defaults such as narrowing tool scope, avoiding silent installs, keeping secrets out of repo files, and treating fetched content as untrusted data.

This makes the concept closely related to [[concepts/skill-based-automation]], [[concepts/okf-validation]], and [[concepts/generated-content-governance]] because it ties authored guidance to observable outcomes and repeatable checks.

## Relationship to adjacent concepts

Baseline-first testing complements several nearby ideas:

- [[concepts/progressive-disclosure]]: both discourage unnecessary content, but baseline-first testing decides what is necessary by experiment.
- [[concepts/context-action-separation]]: baseline runs can reveal when a failure comes from missing durable context rather than poor action guidance.
- [[concepts/quality-gates]]: the baseline provides the before-state that later validation can measure against.
- [[concepts/deterministic-validation]]: captured failures make evaluation more concrete and reproducible.
- [[concepts/failure-driven-development]]: both use observed breakdowns as the input to improvement, but baseline-first testing focuses specifically on skill authoring.
- [[concepts/executable-validation]]: pressure scenarios are strongest when they end with a concrete validation step rather than a purely descriptive check.
- [[concepts/minimal-tool-scoping]]: baseline failures can show whether broad tool permissions are unnecessary and can be narrowed safely.
- [[concepts/skill-structure-conventions]]: the baseline helps determine what belongs in `SKILL.md` versus `scripts/`, `references/`, and `assets/`.
- [[concepts/caveat-preservation]]: baseline and post-adoption checks can reveal when distilled or generated guidance has lost important conditions.
- [[concepts/generated-artifact-adoption]]: adoption should be tested against real failure modes instead of assuming generated output is already operationally safe.

## Takeaway

Baseline-first testing is an evidence-led method for authoring skills: observe unaided failure first, confirm the problem is really an action problem, write only what fixes those failures, keep the skill as small and procedural as possible, test the result against realistic pressure scenarios, and iterate until the skill reliably improves the task without accumulating unnecessary instruction or losing important caveats.