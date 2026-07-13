---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md"]
description: "Running required checks to prove workflows and skills work in practice."
---

# Executable Validation

Executable validation is the practice of confirming instructions, skills, or workflows by actually running the commands, scripts, or checks they require, rather than treating compliance as a purely written claim.

## Why it matters

Executable validation turns guidance into evidence. Instead of assuming a skill is correct because it sounds complete, the agent demonstrates that the skill works in a real task or sample environment. This reduces silent failure, catches missing steps, and supports stronger [[concepts/quality-gates]] and [[concepts/deterministic-validation]].

In skill authoring, executable validation is especially important when an agent might otherwise skip verification, substitute a fragile manual process, or report success without proof. It complements [[concepts/failure-driven-development]] by ensuring that fixes are tested through real execution rather than only described. The skill-creation guidance also makes validation a required finishing step, reinforcing that a skill is incomplete until its documented checks have actually run.

## In testing skills

In [[summaries/agents__skills__skill-creator__references__testing-skills-md]], executable validation appears as part of the recommended testing loop for new skills:

1. Run a pressure scenario without the skill to observe the actual failure.
2. Add the minimum skill content needed to address that failure.
3. Rerun the scenario with the skill and close any remaining loopholes.
4. Run `uv run .agents/skills/skill-creator/scripts/quick_validate.py .agents/skills/<skill-name>`.

This makes validation an explicit completion step rather than an optional extra. The concept is closely aligned with [[concepts/baseline-first-testing]], because both require observing behavior under real conditions and then checking that the revised guidance changes that behavior.

The new skill guidance also adds an important scope rule: test each skill individually rather than batch-creating multiple skills and validating them loosely. That keeps failures attributable, preserves causality between changes and outcomes, and strengthens [[concepts/quality-gates]].

## Scripts and evidence

The source document adds a stricter expectation for script-related skills: deterministic logic should move into scripts when correctness matters, and those scripts should be executed as part of validation rather than trusted on inspection alone. For bundled Python tools, the preferred execution path is `uv run`, with `python3` only as a fallback, which ties executable validation to [[concepts/tooling-context-isolation]] and [[entities/uv]].

Executable validation also implies preserving enough evidence for another person or agent to understand what was tested and what happened. That ties the concept to [[concepts/evidence-staging]] and [[concepts/provenance-tracking]]: the agent should not only run the check, but also retain the command, target, and result in a reviewable form.

## What executable validation prevents

Executable validation helps prevent several common failure patterns:

- claiming a workflow works without running it
- omitting required validation steps
- preferring ad hoc edits over deterministic scripts
- hiding uncertainty behind natural-language assurances
- shipping skills that have not been exercised under realistic conditions
- adopting generated skills without checking whether their commands, caveats, and constraints still hold in the project context

Because of this, executable validation also reinforces [[concepts/tool-boundaries]], [[concepts/skill-based-automation]], and [[concepts/caveat-preservation]] by keeping operational claims tied to actual tool use and by forcing review of what may have been flattened or lost during skill generation or adoption.

## Practical standard

A workflow follows executable validation when it:

- names the command, script, or check to run
- executes it in a realistic sample or target context
- prefers the documented execution path, such as `uv run` for bundled Python scripts when available
- records the outcome in a way that can be reviewed
- treats failed execution as feedback for revising the skill or instructions
- does not consider the work finished until the required validation command has passed

Used this way, executable validation is not just testing at the end; it is a discipline for turning procedural guidance into verifiable behavior.

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]


See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]