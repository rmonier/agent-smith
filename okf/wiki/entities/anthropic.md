---
sources: ["summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__NOTICE.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Organization"
description: "Open-source AI research organization shaping agent design guidance."
---

# Anthropic

Anthropic is an organization referenced in `README.md` and the skill-creator materials as a source of guidance on agent design, context engineering, and skill-based workflows.

## In this document

The repository cites Anthropic in several connected ways:

- It references Anthropic's article on effective context engineering to support the claim that agents work best with a small, curated, high-signal context surface.
- It references Anthropic's article on equipping agents for the real world with Agent Skills to support the repository's progressive disclosure model and separation of orientation, context, and actions.
- It names Anthropic's `skill-creator` as prior art adapted by the repository's own [[entities/skill-creator]] workflow.
- It credits Anthropic in `agents__skills__skill-creator__THIRD_PARTY_NOTICES-md` as one of the upstream sources for adapted passages in `SKILL.md`, alongside OpenAI.
- The third-party notice records that one adapted passage closely tracks Anthropic wording about treating ALL CAPS ALWAYS/NEVER patterns as a yellow flag that should be reframed with reasoning.
- The README also uses Anthropic's guidance to justify consent-first installs, explicit data-flow disclosure, and the progressive-disclosure model behind [[concepts/context-action-separation]] and [[concepts/progressive-disclosure]].

## Why it matters

Anthropic functions here as a key external authority shaping the repository's architecture and operational philosophy: consent-first tooling, layered documentation, and reusable actions. Its guidance helps justify the separation between [[concepts/context-action-separation]], [[concepts/agent-context-layering]], and [[concepts/portable-skill-contract]]. The notice also reinforces Anthropic's role in the repository's [[concepts/licensing-and-attribution]] and [[concepts/open-source-attribution]] practices, especially around identifying adapted passages and preserving provenance.

## Related pages

- [[summaries/README-md]]
- [[summaries/agents__skills__skill-creator__NOTICE]]
- [[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]
- [[entities/skill-creator]]
- [[entities/agent-skills]]
- [[entities/agent-smith]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]