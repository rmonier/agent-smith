---
sources: ["summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__NOTICE.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md"]
type: "Work"
description: "OpenAI-authored system skill-creator source adapted in SKILL.md"
---

# OpenAI System Skill Creator

OpenAI System Skill Creator is an upstream system-level skill-creation source that influenced the `skill-creator` document's guidance for building reusable Agent Skills.

## Relation To This Document

The third-party notices file identifies OpenAI's system `skill-creator` as one of the exact upstream sources consulted when reviewing adapted passages in `SKILL.md`. It is cited alongside Anthropic's `skill-creator` and `superpowers`' `writing-skills` as part of the conceptual and textual lineage behind the current skill specification.

## Key Facts

- It is named as an upstream source for the adapted passages recorded in `[[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]`.
- The notice attributes two of the three adapted passages to this source, including guidance about the context window and task-specific degrees of freedom.
- The document states that the comparison found `SKILL.md` overwhelmingly independent expression overall, with only a few short passages closely tracking upstream wording.
- The notice records the upstream licence as Apache-2.0, but also notes that the upstream `LICENSE.txt` ships as an unfilled template without a specific copyright holder stated in the source itself.
- The notice emphasizes re-verification against current upstream state before relying on the document for a new adaptation, reinforcing [[concepts/source-provenance]] and [[concepts/license-compliance-requirements]].

## Why It Matters

This source helps justify the attribution treatment in `SKILL.md`: the guidance is presented as an adaptation of existing skill-authoring practice rather than a standalone invention. The notice also shows how the wiki distinguishes broad conceptual influence from short passages that require explicit attribution, supporting [[concepts/attribution-based-reuse]], [[concepts/licensing-and-attribution]], and [[concepts/open-source-attribution]].