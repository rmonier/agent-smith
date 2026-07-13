---
sources: ["summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
type: "Work"
description: "OpenKB's compiled knowledge-base context for agent-ready repositories"
---

# OKF

OKF is the OpenKB knowledge-base layer used as the durable context source of truth for agent-ready repository workflows.

## What It Does

The `agent-ready-context` skill treats OKF as the repository's compiled context surface, with the wiki under `okf/wiki/` serving as the place for durable knowledge, evidence, provenance, and cross-agent memory.

## Key Facts

- OKF is the OpenKB KB root for repository context management.
- The compiled wiki lives under `okf/wiki/` and is treated as the source of truth for durable context.
- Generated content should be staged under `okf/.okf-build/input/` and ingested into OKF rather than edited directly.
- OKF separates context from action skills and from `AGENTS.md` orientation content.
- The workflow uses validation, linting, and review passes to keep the compiled wiki coherent and grounded.
- Findings that are discovered during work can be captured in the wiki as a separate memory channel before being promoted into compiled truth.

## Relationship To The Skill

The `[[summaries/agents__skills__agent-ready-context__SKILL-md]]` document frames OKF as the durable context layer in a three-part repository model:

- skills = actions
- OKF wiki = context
- `AGENTS.md` = orientation and routing

That makes OKF the main repository knowledge base for cross-agent continuity and documentation governance.

## Related Concepts

- [[concepts/compiled-knowledge-bases]]
- [[concepts/durable-context]]
- [[concepts/knowledge-compilation-pipeline]]
- context layer separation
- [[concepts/deterministic-okf-staging]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/okf-wiki-governance]]
- [[concepts/orientation-routing]]
- [[concepts/findings]]
- [[concepts/source-grounded-regeneration]]

## Related Entities

- [[entities/openkb]]
- [[entities/okf-wiki]]
- [[entities/okf-spec]]
- [[entities/okf-readme]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-agents-md]]
