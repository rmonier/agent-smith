---
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/graphify-report.md", "summaries/README-md.md"]
type: "Work"
description: "Official specification for the Agent Skills file format"
---

# Agent Skills

Agent Skills is the official specification for a portable skill format that packages instructions and optional resources in a directory centered on `SKILL.md`. The spec defines how agents should discover, validate, and load skills, and it is the format implemented by this repository's product skills under `.agents/skills/`.

## What it defines

The specification standardizes a skill as a directory containing at minimum a `SKILL.md` file, with optional `scripts/`, `references/`, and `assets/` directories for code, supporting documentation, and static resources. It also defines the required frontmatter schema for `SKILL.md`, including `name` and `description`, plus optional fields such as `license`, `compatibility`, `metadata`, and `allowed-tools`.

## Key rules

- `name` must be lowercase, hyphenated, unique to the directory, and match the parent folder name.
- `description` must explain what the skill does and when to use it.
- The body of `SKILL.md` contains the actual instructions and can be organized freely.
- Skills should be structured for [[concepts/skill-progressive-disclosure]], loading metadata first and deeper resources only when needed.
- Reference paths should stay relative and shallow to keep files easy to resolve.
- Validation is recommended with `skills-ref validate ./my-skill`.

## Why it matters

This work provides the contract that makes Agent Skills interoperable across agent implementations. It supports [[concepts/portable-skill-contract]], [[concepts/skill-frontmatter-schema]], [[concepts/skill-validation-workflow]], and [[concepts/progressive-disclosure]]. It also connects to the broader [[entities/agent-skills]] ecosystem and the repository's skill authoring practices.

## Related source

- [[summaries/agent-skills-spec]]