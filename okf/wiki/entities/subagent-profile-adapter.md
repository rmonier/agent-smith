---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
type: "Work"
description: "Companion skill for runtime/tooling context and adapter generation"
---

# subagent-profile-adapter

`subagent-profile-adapter` is a companion skill paired with [[entities/agent-ready-context-skill]] to handle runtime and tooling context for agent-ready repositories.

## Role

The skill is described as an optional companion that supports:

- runtime/tooling context inspection
- adapter generation for harness-specific profiles
- operational context policy for local tooling

It is not the primary context source; that role belongs to [[entities/okf-wiki]]. Instead, it helps bridge repository context into harness-aware runtime behavior.

## Relationship to Agent-Ready Context

In the agent-ready-context skill, `subagent-profile-adapter` appears as one of two companion skills:

- `skill-creator` for optional action-skill extraction
- `subagent-profile-adapter` for optional runtime/tooling context and adapter generation

This places it in the broader [[concepts/context-action-separation]] model, where skills, wiki context, and orientation files carry different responsibilities.

## Notable References

The document links `subagent-profile-adapter` to several specific files and scripts:

- `subagent-profile-adapter/scripts/inspect_runtime_context.py`
- `subagent-profile-adapter/references/tooling-context-policy.md`
- `subagent-profile-adapter/references/runtime-detection.md`
- `subagent-profile-adapter/references/harness-docs.md`
- `subagent-profile-adapter/scripts/validate_tooling_link_policy.py`

Those references suggest the skill focuses on detecting the active harness, organizing local tooling context, and validating link policy for tooling pages.

## Why It Matters

The skill supports [[concepts/tooling-context-governance]] and [[concepts/local-by-default-tooling]] by keeping harness-specific context separate from compiled project knowledge. It also reinforces [[concepts/tooling-link-policy]] and [[concepts/tooling-context-isolation]] through explicit tooling pages and validation scripts.

## Related Pages

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[entities/agent-ready-context-skill]]
- [[entities/skill-creator]]
- [[entities/agents-skills]]
- [[entities/tooling]]
