---
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__NOTICE.md", "summaries/agents__skills__skill-creator__LICENSING-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/repo-snapshot.md", "summaries/README-md.md"]
type: "Work"
description: "Work page for the skill-creator OpenKB companion skill"
---

# skill-creator

`skill-creator` is a companion OpenKB skill for authoring, updating, validating, and adopting custom skills. In the agent-ready-context workflow, it is the preferred route when a repeated action can be turned into a durable skill instead of remaining ad hoc.

## What it does

- Drafts new skills from wiki-grounded context when the user wants a repeatable action captured as a skill.
- Validates and iterates on skill structure, dependencies, and tests.
- Suggests skill candidates from refreshed OKF content.
- Supports adoption of generated skills into the repository's `.agents/skills/` area.
- Encodes Agent Skills format expectations such as `SKILL.md` frontmatter, directory layout, and progressive disclosure.

## Role in the agent-ready-context workflow

The `agents__skills__agent-ready-context__SKILL-md` document treats `skill-creator` as the tool for identifying repeated actions and turning them into reusable automation. It is part of a broader separation between [[concepts/skill-based-automation]], [[concepts/context-action-separation]], and [[concepts/skill-governance]].

The workflow also distinguishes `skill-creator` from [[entities/subagent-profile-adapter]], which is used for harness-specific runtime and tooling context rather than action-skill extraction.

## Key facts from the source

- `skill-creator` is listed as an optional companion skill for action-skill extraction.
- It prefers OpenKB Skill Factory when OpenKB is adopted, the needed knowledge already exists in `okf/wiki/`, and the user consents to the LLM-backed call.
- Generated drafts land under `okf/output/skills/` and are not installed directly.
- Adoption requires an explicit `adopt_generated_skill.py` step and a review for source attribution and caveat preservation.
- The skill is part of the repository's safe automation and skill governance model, not a replacement for the wiki or `AGENTS.md`.
- The Agent Skills specification requires each skill to be a directory with a mandatory `SKILL.md` file and optional `scripts/`, `references/`, and `assets/` directories.
- `SKILL.md` frontmatter must include a valid `name` and `description`; optional fields include `license`, `compatibility`, `metadata`, and `allowed-tools`.
- Skill naming must be lowercase, hyphenated, and match the parent directory name, with no consecutive hyphens.
- The specification recommends progressive disclosure: metadata at startup, full `SKILL.md` on activation, and supporting files only when needed.
- Skills should be validated with `skills-ref validate ./my-skill` before adoption or publication.

## Related pages

- skill creator
- [[concepts/skill-authoring]]
- [[concepts/skill-validation-workflow]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/generated-content-governance]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/skill-scaffolding]]
- [[concepts/portable-skill-contract]]
- [[concepts/path-based-skill-validation]]
- [[concepts/executable-validation]]
- [[entities/adopt_generated_skill-py]]
- [[entities/openkb-skill-factory]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agent-skills-spec]]