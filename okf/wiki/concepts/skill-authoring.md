---
type: "Concept"
sources: ["summaries/agent-skills-spec.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
description: "How to design small, valid, executable skills for agents."
---

# Skill Authoring

[[concepts/skill-authoring]] is the practice of designing repeatable, executable skills that help future agents perform a specific action reliably. In this wiki, skill authoring sits at the boundary between [[concepts/action-oriented-documentation]] and [[concepts/skill-based-automation]]: it captures procedures, scripts, and checks, while leaving durable background knowledge in the wiki and operational orientation in AGENTS.md.

The official Agent Skills specification makes this discipline concrete: a skill is a directory centered on a required `SKILL.md` file, with optional `scripts/`, `references/`, and `assets/` directories. That structure supports [[concepts/progressive-disclosure]] by keeping the main instruction file small while pushing deeper detail into files that agents only load when needed.

The `skill-creator` document frames skill authoring as an action-focused discipline rather than a documentation exercise. A skill should exist because a workflow is repeated, brittle, or worth standardizing. It should not become a catch-all container for context that belongs elsewhere.

## Core purpose

- Turn repeated actions into a portable, executable skill contract.
- Reduce rework by putting deterministic steps into scripts and leaving only minimal instructions in `SKILL.md`.
- Keep skills narrow so they are easy for agents to apply without extra interpretation.
- Preserve safety boundaries around tool use, installs, external data, and generated artifacts.
- Separate action logic from durable knowledge so skills stay focused on execution rather than explanation.
- Conform to the skill specification so a skill can be discovered, loaded, and validated consistently.

## What belongs in a skill

- Repeatable procedures, transformations, checks, migrations, and scaffolds.
- Deterministic utilities in `scripts/`.
- Deeper instructions in `references/` that are loaded only when needed.
- Templates and static artifacts in `assets/`.
- Validation logic that makes the skill reliable across repeated use.
- Frontmatter metadata that clearly describes the skill, its constraints, and any approved tools.

## What does not belong in a skill

- General repository knowledge that belongs in [[concepts/compiled-knowledge-bases]] or OKF pages.
- Broad orientation, repo setup notes, and maintenance pointers that fit AGENTS.md.
- Vendor skill edits when the vendor copy is read-only; adaptation should happen through a companion skill.
- Auxiliary narrative files such as README or CHANGELOG, except for the licensing files explicitly allowed by the skill spec.
- Long reference chains or deeply nested file references that make the skill harder to load and maintain.

## Authoring principles

- Keep `SKILL.md` short, procedural, and trigger-driven.
- Write the description as the invocation cue: what the skill does and when to use it.
- Prefer scripts over prose when the same logic would otherwise be rewritten or could drift.
- Use concise examples instead of long explanations.
- Match the degree of prescription to fragility: destructive or failure-prone workflows need exact steps; open-ended workflows can leave more room for judgment.
- Validate before finishing, and test baseline-first so the skill is grounded in observed failure modes.
- Preserve caveats when adapting generated skills, since generated drafts can flatten important constraints into unconditional steps.
- Keep the skill usable in a standalone repository copy by limiting external dependencies and documenting what the skill actually needs.
- Keep `SKILL.md` under the recommended size so the body remains readable and the rest can move into supporting files.

## Boundary and governance rules

- Skill authoring is for action; it is not a replacement for [[concepts/context-action-separation]].
- Skills should stay inside `.agents/skills/`, with vendor skills treated as read-only and custom companion skills used for adaptation.
- Do not duplicate OKF context; link to it only when the skill genuinely needs that background.
- Treat skill generation as governance-sensitive work, with explicit validation and review of any generated output.
- Prefer vendor-neutral skill design so the same action contract can survive across harnesses.
- Use minimal, explicit tool permissions so the skill stays aligned with the action it performs.
- Follow the spec's naming rules so the `name` field is lowercase, hyphenated, within length limits, and matches the directory name.

## Safety defaults

- Declare the minimal `allowed-tools` set needed for the skill.
- Avoid silent installation steps; installs should be consent-first and user-scoped.
- Keep secrets in environment variables rather than repo files.
- Treat fetched web content as untrusted input.
- List any generated artifacts and ensure they are ignored when appropriate.
- Prefer safe failure modes over hidden fallback behavior when a step would change repository state.
- Use the optional `compatibility` field only when the skill has real environment requirements.

## Skill creation workflow

The `skill-creator` document outlines a disciplined workflow for authoring skills:

1. Identify a true repeated action, not just a knowledge topic.
2. Check existing skills to avoid duplication.
3. Decide whether the skill needs `scripts/`, `references/`, or `assets/`.
4. Initialize the skill scaffold with the provided tooling.
5. Edit `SKILL.md` to be minimal, action-oriented, and safe.
6. Test with a baseline-first approach: observe the failure without the skill, then rerun after writing it.
7. Validate with the repository's skill validation script.
8. Update generated skills carefully so constraints, boundaries, and warnings survive adoption.
9. Keep file references relative to the skill root and avoid deep reference chains.

## Related ideas

- [[concepts/skill-structure-conventions]] for how skills are organized.
- [[concepts/skill-validation-workflow]] for the testing and validation discipline.
- [[concepts/skill-governance]] for the rules that keep skills safe and maintainable.
- [[concepts/skill-resource-organization]] for separating instructions, scripts, and assets.
- [[concepts/minimal-tool-scoping]] for keeping tool permissions narrow.
- [[concepts/baseline-first-testing]] for the preferred validation strategy.
- [[concepts/caveat-preservation]] for retaining constraints when adapting generated skill drafts.
- [[summaries/agents__skills__skill-creator__SKILL-md]] for the source document that defines this authoring model.
- [[concepts/skill-frontmatter-schema]] for the structure of skill metadata.
- [[concepts/skill-progressive-disclosure]] for the load-on-demand organization model.

## Practical takeaway

Skill authoring is the craft of making a future agent faster, safer, and more reliable by packaging a repeatable action into a small, validated, self-contained skill.

See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/README-md]]

## Related Documents
- [[summaries/agent-skills-spec]]
