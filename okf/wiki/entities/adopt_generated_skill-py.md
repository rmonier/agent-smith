---
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"]
type: "Work"
description: "Repository skill-creation guide for reusable action workflows"
---

# skill-creator

`skill-creator` is a repository skill that defines how to create, update, validate, and adopt reusable Agent Skills under `.agents/skills/`.

## What it does

- Frames a skill as an executable action: a repeatable procedure, script, transformation, check, migration, scaffold, or workflow recipe.
- Distinguishes skills from the OKF wiki and from `AGENTS.md`:
  - skills are for action
  - the wiki is for durable context and provenance
  - `AGENTS.md` is for orientation and repo rules
- Requires skill authors to keep `SKILL.md` short and procedural, with detailed guidance moved into `references/`, deterministic logic into `scripts/`, and templates into `assets/`.
- Encourages writing the `description` field as the trigger for when the skill should be used, rather than as a workflow summary.
- Provides a standard creation path using `init_skill.py`, then baseline-first testing, then `quick_validate.py`.
- Covers both hand-scaffolded skill creation and adoption of generated skills from [[concepts/generated-artifact-adoption]] workflows.

## Safety behavior

- Recommends the minimal `allowed-tools` set needed for the action.
- Forbids silent software installation; installs must be consent-first, version-pinned, and user-scoped.
- Requires credentials to stay in environment variables rather than repo files.
- Treats fetched web content as untrusted data.
- Requires generated artifacts to be listed and gitignored in the target repository.
- Advises preserving caveats and constraints when adopting generated skills, since distillation can flatten important boundaries.

## Operational role

The skill functions as the authoring standard for [[concepts/skill-authoring]], [[concepts/skill-scaffolding]], and [[concepts/skill-validation-workflow]].
It also reinforces [[concepts/skill-structure-conventions]], [[concepts/minimal-tool-scoping]], [[concepts/consent-first-installation]], and [[concepts/wiki-context-routing]] by keeping action logic separate from background knowledge.

For OKF-derived candidates, it recommends first running the zero-LLM suggestion script, then choosing between hand scaffolding and the OpenKB Skill Factory path when the wiki coverage and user consent make that appropriate.

## Embedded guidance

The document gives practical standards for skill maintainers:

- keep skills short and procedural
- prefer scripts when reuse or correctness matters
- avoid duplicating wiki context in skills
- validate before finishing
- use naming rules that keep skill folders lowercase and hyphenated
- limit auxiliary files to the licensing exceptions explicitly allowed by the spec

It also calls out the lineage of the approach, noting adaptation from Anthropic's `skill-creator`, testing discipline from `superpowers`' `writing-skills`, and workflow shape from OpenAI's system `skill-creator`.

## Related pages

- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]
- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[entities/agent-skills]]
- [[entities/agent-smith]]
- [[entities/agents-skills]]