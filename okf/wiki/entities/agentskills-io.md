---
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
type: "Organization"
description: "Official site publishing the Agent Skills specification"
---

# agentskills.io

`agentskills.io` is the official website that publishes the Agent Skills specification referenced by [[summaries/agent-skills-spec]]. It serves as the source of the format rules for Agent Skills and the documentation used to validate skill directories.

## Key facts

- Hosts the official Agent Skills specification at `https://agentskills.io/specification`.
- Defines the required `SKILL.md` structure for agent skills.
- Describes directory layout, frontmatter fields, progressive disclosure, and validation guidance.
- Is treated as an official-docs source in the referenced document.

## What it specifies

The specification documented on agentskills.io covers:

- A skill as a directory centered on a required `SKILL.md` file
- Optional `scripts/`, `references/`, and `assets/` subdirectories
- Frontmatter requirements such as `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`
- Naming rules for skills, including lowercase hyphenated names that match the parent directory
- Progressive disclosure, where metadata is loaded broadly and deeper resources are loaded only when needed
- Validation using the `skills-ref` reference library

## Related concepts

- [[concepts/agent-skill-specification]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/skill-validation-workflow]]
- [[concepts/external-documentation]]
- [[concepts/spec-authority]]
- [[concepts/path-based-skill-validation]]