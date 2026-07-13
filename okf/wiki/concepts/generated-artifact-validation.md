---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"]
description: "Validating generated artifacts before adoption to catch broken outputs early."
---

# Generated Artifact Validation

Generated artifact validation is the practice of checking a synthesized file or directory immediately after creation or adoption, before it is accepted as part of the durable repository state. It reduces the chance that machine-produced output becomes a long-lived broken asset.

## Why it matters

Generated content can be structurally plausible while still violating local rules, missing required files, or depending on invalid assumptions. Validation acts as a quality gate that separates tentative generation from repository-owned content. This aligns with [[concepts/quality-gates]], [[concepts/human-in-the-loop-review]], and [[concepts/deterministic-validation]].

## In the skill adoption workflow

The source script `[[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]` shows a concrete adoption flow:

- It copies a generated skill from `okf/output/skills/` into `.agents/skills/`.
- It checks that the source contains `SKILL.md` before copying.
- It validates the skill by running `quick_validate.py` on the adopted destination.
- If validation fails on a fresh copy, it deletes the copied destination to avoid leaving a broken artifact behind.
- If validation fails after replacing an existing skill with `--force`, it preserves the replacement and instructs the user to fix or remove it manually.

This is a practical example of [[concepts/generated-artifact-adoption]] paired with [[concepts/generated-artifact-validation]].

## Core properties

- **Immediate**: validation happens right after generation or copy, not later in a separate cleanup pass.
- **Local**: checks are performed against the artifact in its intended repository location.
- **Fail-safe**: invalid fresh output is removed rather than silently retained.
- **Policy-aware**: validation is tied to repository-specific conventions, such as required files and naming rules.
- **Human-reviewed**: the script still tells the user to inspect the adopted result against skill-creator standards.

## Related checks

Generated artifact validation often overlaps with [[concepts/filesystem-validation]], [[concepts/path-based-validation]], and [[concepts/executable-validation]] when the artifact must satisfy both structural and behavioral rules. In repository workflows, it also supports [[concepts/safe-automation]] by limiting the damage from bad machine-generated output.

## Distinctions

- Validation is not the same as generation: generation produces the artifact, while validation decides whether it is acceptable.
- Validation is not the same as review: review can catch semantic issues, but validation enforces concrete rules.
- Validation is not the same as adoption: adoption is the act of making the artifact part of the project; validation is the gate before or during that move.

## Practical takeaway

A generated artifact should not be treated as trustworthy merely because it was produced by an internal tool. The adoption pipeline should verify required structure, enforce naming and location constraints, and reject or roll back invalid output. That pattern keeps generated content aligned with repository standards and reduces drift between intended and actual state.

See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]