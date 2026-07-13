---
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
type: "Work"
description: "OpenKB's LLM-backed skill drafting and validation workflow"
---

# OpenKB Skill Factory

OpenKB Skill Factory is an LLM-backed workflow for drafting, validating, and evolving custom skills from OKF wiki content. In this document, it appears as the preferred path for creating new action skills when the user consents to an LLM-backed step and the repository already has suitable wiki grounding.

## What It Does

The workflow is used to:

- draft new skills from compiled wiki knowledge
- validate generated skills before adoption
- review skill history and rollback when needed
- keep generated drafts in `okf/output/skills/` until they are explicitly adopted

## Role In The Agent-Ready Context

The document treats Skill Factory as part of the broader [[concepts/agent-ready-context]] pipeline, but not as a replacement for the wiki or repository guidance. It is specifically positioned as a way to turn compiled knowledge into actionable skills when the repository already has a documented need.

It also reinforces the boundary between [[concepts/action-oriented-documentation]] and durable context: skills encode repeatable actions, while the wiki preserves the underlying knowledge.

## Adoption Rules

Key constraints from the document include:

- use Skill Factory only when the user consents to an LLM-backed command
- prefer it when the action is already well covered by `okf/wiki/`
- do not install generated drafts directly as project skills
- adopt generated skills through `adopt_generated_skill.py` and the skill standards workflow

This makes the tool a controlled bridge between compiled knowledge and reusable automation, rather than an open-ended generator.

## Related Ideas

- [[concepts/skill-adoption]]
- [[concepts/skill-authoring]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/generated-artifact-validation]]
- [[concepts/knowledge-compilation-pipeline]]

## Related Source

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/agent-skills-spec]]