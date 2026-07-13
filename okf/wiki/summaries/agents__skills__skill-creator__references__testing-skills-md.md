---
type: "Summary"
description: "Guidance for testing new skills with realistic failure-driven pressure scenarios."
doc_type: short
full_text: "sources/agents__skills__skill-creator__references__testing-skills-md.md"
---

# Summary

This document describes how to validate a newly created skill by testing it against at least one realistic pressure scenario: a prompt or task that has previously caused the agent to fail in a specific, repeated way.

## Core idea

A skill should not be considered complete until it has been exercised under conditions where the agent is likely to:

- forget a required step
- replace a deterministic script with a fragile manual rewrite
- confuse planning or context with concrete action
- edit vendor-managed skills directly
- move large bodies of durable knowledge into `AGENTS.md`
- skip validation or fail to preserve provenance

This frames skill testing as a response to observed failure modes rather than hypothetical best practices, linking closely to [[concepts/context-action-separation]], [[concepts/deterministic-validation]], and [[concepts/provenance-tracking]].

## Baseline-first cycle

The document proposes a three-stage improvement loop plus validation:

1. **Baseline (red):** Run the pressure scenario without the skill and record the exact failure behavior.
2. **Write (green):** Add only the minimal skill content needed to address those observed failures.
3. **Close loopholes (refactor):** Rerun with the skill, identify remaining slips, and add explicit counters that explain the reasoning behind the constraint.
4. Run `uv run scripts/quick_validate.py <skill-dir>`.

This approach emphasizes [[concepts/baseline-first-testing]], [[concepts/failure-driven-development]], and minimal rules.

## Authoring guidance

Several practical principles shape the recommended workflow:

- test against real failures, not speculative ones
- avoid adding rules for problems that have not been seen
- explain why a behavior is wrong, not only that it is prohibited
- create and test one skill at a time rather than batching multiple new skills together

The rationale is that batch-created skills often carry untested failure modes, while single-skill iteration improves traceability and learning. This connects to incremental workflows and agent discipline.

## Script-specific expectation

When a skill involves scripts, the script should be run against a temporary sample, and the command plus result should be included in the handoff summary. This reinforces [[concepts/executable-validation]] and evidence-based handoffs.

## Key takeaway

The document's main contribution is a disciplined method for testing skills under realistic pressure, using observed failures to drive minimal fixes, explicit safeguards, and concrete validation evidence.

## Related Concepts
- [[concepts/skill-based-automation]]
- [[concepts/agents-md-maintenance]]
- [[concepts/quality-gates]]

## Entities
- [[entities/uv]]
- [[entities/agents-md]]
