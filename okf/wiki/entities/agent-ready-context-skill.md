---
sources: ["summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__NOTICE.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
type: "Work"
description: "OpenKB skill for creating harness-specific subagent/profile adapters"
---

# agent-ready-context skill

The `agent-ready-context` skill is the OpenKB workflow package for creating, refreshing, repairing, and validating agent-ready context in a repository. It provides the executable source of truth for maintaining `AGENTS.md` guidance, routing agents into the OKF wiki, and keeping repository orientation aligned with compiled knowledge.

The related `subagent-profile-adapter` skill extends that workflow into harness-specific runtime adapters. It generates native subagent or profile files for the active agent harness without turning those adapters into a source of truth.

## What It Does

This skill defines how agents should manage the boundary between repository instructions, compiled wiki context, reusable automation, and runtime-specific projections. It is the upstream workflow referenced by the script documented in [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]], which uses a conservative managed-section merge to update `AGENTS.md`.

It also acts as a meta-skill for authoring and maintaining other skills: it frames skills as action-oriented capabilities, recommends short procedural `SKILL.md` files, and pushes detailed guidance into `references/`, deterministic behavior into `scripts/`, and reusable static material into `assets/`.

When used for harness adapter work, it adds a stricter runtime boundary: detect the active harness from environment or documentation, confirm whether local subagents or profiles are supported, and write only the native adapter files that the harness expects. It also emphasizes that harness documentation belongs in `okf/wiki/tooling/`, while project concept pages must not depend on tooling context.

## Key Facts

- It is the authoritative procedure for agent-ready context maintenance.
- It tells agents to treat `okf/wiki/index.md` as the front door to the wiki.
- It separates repository orientation in `AGENTS.md` from durable context in the OKF wiki.
- It instructs agents to use `uv run` for bundled maintenance scripts when available.
- It requires durable project facts to be captured as findings rather than patched into compiled wiki pages.
- It emphasizes not editing OpenKB-managed compiled pages directly.
- It defines skills as repeatable actions, not as general knowledge or narrative memory.
- It recommends minimal tool scopes, consent-first installs, and environment-based secrets handling for skill design.
- It validates skills before use and prefers baseline-first testing for fragile workflows.
- It treats harness-specific subagent/profile adapters as runtime projections, not portable standards.
- It requires runtime detection to use explicit harness signals, not installed binaries alone.
- It prefers local-only or otherwise explicitly tracked handling for generated harness-specific files.
- It keeps tooling context isolated from project concepts and validates that link direction stays one-way.

## Relationship To The Script

The script `merge_agents_md_okf_section.py` implements one piece of this workflow: inserting or replacing the managed OKF section inside `AGENTS.md` without disturbing repo-specific guidance. That makes the script a mechanical companion to this skill, not a replacement for it.

The skill also governs the broader creation and update flow for custom skills, including initialization, validation, and adoption from OpenKB-generated drafts when the wiki has enough coverage to support them.

For harness adapter generation, it additionally points to runtime inspection helpers and tooling-policy validation so that generated adapters remain small, native to the harness, and aligned with repository documentation boundaries.

## Related Concepts

- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/agents-md-maintenance]]
- [[concepts/agent-orientation-index]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/managed-document-sections]]
- [[concepts/conservative-document-merging]]
- [[concepts/wiki-context-routing]]
- [[concepts/source-grounded-regeneration]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/skill-authoring]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-validation-workflow]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/consent-first-installation]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/harness-native-profiles]]
- [[concepts/runtime-adapter-management]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-link-policy]]
- [[concepts/local-by-default-tooling]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/subagent-role-design]]
- [[concepts/permission-scoped-agents]]

## Related Entities

- [[entities/agent-ready-context]]
- [[entities/agents-skills]]
- [[entities/agents-md]]
- [[entities/okf-wiki-index-md]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/skill-creator]]
- [[entities/quick_validate-py]]
- [[entities/init_skill-py]]
- [[entities/adopt_generated_skill-py]]
- [[entities/suggest_skills_from_okf-py]]
- [[entities/scripts-inspect_runtime_context-py]]
- [[entities/scripts-ensure_local_alias-py]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/subagent-profile-adapter]]

## Why It Matters

This skill keeps agent behavior consistent across repository refreshes and prevents the OKF guidance from drifting into a bloated, duplicated, or contradictory state. It is central to the repository's orientation workflow and to the maintenance of accurate agent-facing instructions.

It also matters because it encodes how reusable operational skills should be discovered, shaped, tested, and validated without collapsing back into context pages. In its subagent-profile-adapter role, it extends that discipline to the runtime layer so harness-specific adapters stay lightweight, explicit, and bounded.

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]