---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md"]
description: "Improve skills by fixing observed agent failures through targeted iteration."
---

# Failure-Driven Development

Failure-Driven Development is the practice of improving an agent skill by testing it against real failure cases, recording how it breaks, and adding only the smallest changes needed to prevent those specific failures.

## Overview

In this workflow, failure is not treated as an exception to hide or explain away. Instead, it becomes the primary design input. A skill is exercised on a realistic task that has already exposed weaknesses such as skipped steps, fragile rewrites, blurred context and action, direct editing of vendor-managed assets, or missing validation. The observed breakdowns then determine what the skill must say and how explicit it needs to be.

This makes the concept closely related to [[concepts/baseline-first-testing]], [[concepts/context-action-separation]], [[concepts/executable-validation]], and [[concepts/quality-gates]].

## Core pattern

The source document describes a baseline-first loop:

1. Run the pressure scenario without the skill and capture the exact failure behavior.
2. Write the minimal skill guidance needed to address those observed failures.
3. Rerun the same scenario with the skill in place.
4. When the agent still slips through, add explicit counters that explain the reasoning behind the rule rather than only forbidding the behavior.
5. Validate the resulting skill with the required checks.

This keeps the process grounded in evidence instead of speculation. It also prevents a skill from turning into a large, generic rule set that tries to anticipate every possible mistake.

## Why it matters

Failure-Driven Development helps keep skills precise and durable:

- it ties guidance to demonstrated failure modes rather than hypothetical concerns
- it reduces overfitting to broad policy language by focusing on concrete breakdowns
- it encourages narrow, testable corrections instead of sprawling instructions
- it reveals loopholes through reruns, which makes refinement iterative and evidence-based
- it reinforces validation as part of authoring, not as an optional final step

In practice, this supports disciplined skill creation within [[concepts/skill-based-automation]]. It also aligns with [[concepts/deterministic-validation]] when a skill depends on scripts or checks that can be executed and verified.

## Pressure scenarios as inputs

A key mechanism in Failure-Driven Development is the pressure scenario: a realistic prompt or task that previously caused the agent to fail in a recognizable way. These scenarios are valuable because they expose recurring weaknesses under realistic conditions rather than idealized tests.

Examples from the source include cases where the agent:

- forgets a required step
- rewrites fragile code instead of using a deterministic script
- mixes explanatory context with operational instructions
- edits vendor skills directly
- writes durable knowledge into `AGENTS.md`
- omits validation or provenance details

These examples connect the concept to [[concepts/tool-boundaries]], [[concepts/durable-context]], and [[concepts/provenance-tracking]].

## Minimal change principle

An important constraint in this approach is to add only what the observed failures justify. The source emphasizes resisting the urge to write rules for problems that have not actually been seen. This keeps the skill lean, improves readability, and makes the resulting behavior easier to test and maintain.

That principle also works well with [[concepts/progressive-disclosure]] and [[concepts/agents-md-maintenance]] by discouraging unnecessary rule growth and misplaced durable knowledge.

## Validation and evidence

Failure-Driven Development does not stop at rewriting instructions. The updated skill should be rerun against the same scenario, and if scripts are involved, those scripts should be executed on a temporary sample with the command and result included in the handoff. The source also requires running the relevant validator.

This makes validation evidence part of the development loop, not a separate concern, and connects directly to [[concepts/executable-validation]] and [[concepts/okf-validation]].

## Source basis

This concept is derived from [[summaries/agents__skills__skill-creator__references__testing-skills-md]], which frames skill completion around realistic pressure testing, observed failure capture, targeted fixes, reruns, and explicit validation.

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]