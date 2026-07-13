---
sources: ["summaries/okf-spec.md", "summaries/karpathy-llm-wiki-gist.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Other"
description: "The compiled OKF wiki knowledge base surface for agent-smith."
---

# OKF wiki

The `OKF wiki` is the compiled knowledge base surface for `agent-smith`, located at `okf/wiki/`. It serves as the repository's durable context layer, separate from orientation files like `AGENTS.md` and action files under `.agents/skills/`.

## Role

The wiki is the project's long-lived knowledge store: it holds summaries, concepts, entities, explorations, and supporting documentation derived from repository sources and external evidence. In the README's architecture, it is where compiled context lives so agents can reuse prior understanding instead of re-deriving it from raw files on every session.

The `agent-ready-context` skill makes this separation explicit: skills are for repeatable actions, the wiki is for durable context, and `AGENTS.md` stays a concise orientation layer. It also treats `okf/wiki/` as the durable source of truth for repository context, with staged input and OpenKB ingestion used to produce compiled pages rather than direct hand editing.

This supports [[concepts/context-surface-management]], [[concepts/durable-context]], [[concepts/knowledge-compilation-pipeline]], and [[concepts/context-action-separation]].

## Key Facts

- It is the OpenKB-backed knowledge surface for the repository.
- It is stored under `okf/wiki/`.
- It is distinct from `AGENTS.md`, which provides orientation, and `.agents/skills/`, which provide repeatable actions.
- The `agent-ready-context` skill says the wiki is the durable context source of truth and that generated pages should come from staged input, not direct edits.
- The skill also frames `okf/wiki/` as the place for architecture notes, decisions, provenance, external evidence, and cross-agent memory.
- The wiki is intended to be validated as a compiled bundle, with `okf/wiki/index.md`, `okf/wiki/log.md`, and `okf/wiki/AGENTS.md` as part of the navigable root.
- OKF v0.1 requires every non-reserved Markdown file in the bundle to carry parseable YAML frontmatter with a non-empty `type` field, while consumers are expected to tolerate missing optional fields, unknown types, and broken links.
- The OKF specification also defines bundle-relative `/` links as the recommended stable cross-linking form, alongside standard relative paths.
- The skill emphasizes that project concept pages should not depend on tooling context pages, even though tooling pages may be indexed for navigation.
- It includes a narrow exception for guarded editorial curation when semantic-lint output is pure curation noise and not source-backed knowledge.

## Relationship to the Repository

The wiki is one of the three core repository surfaces described in [[summaries/README-md]]:
- orientation in `AGENTS.md`
- context in `okf/wiki/`
- actions in `.agents/skills/`

It is central to the repository's agent-ready design because it preserves knowledge across sessions and supports incremental compilation, validation, reconciliation of deleted or moved sources, and findings triage.

## Related Concepts

- [[concepts/compiled-knowledge-bases]]
- [[concepts/context-action-separation]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/okf-wiki-governance]]
- [[concepts/progressive-disclosure]]
- [[concepts/source-grounded-regeneration]]
- [[concepts/wiki-context-routing]]
- [[concepts/deterministic-okf-staging]]
- [[concepts/findings-promotion]]
- [[concepts/guarded-wiki-curation]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/okf-spec]]

See also: [[summaries/karpathy-llm-wiki-gist]]


See also: [[summaries/graphify-report]]