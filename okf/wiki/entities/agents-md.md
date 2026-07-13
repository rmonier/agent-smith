---
sources: ["summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"]
type: "Other"
description: "Repository orientation file for agent-facing operational basics."
---

# AGENTS.md

`AGENTS.md` is the repository's orientation file: a top-level instruction surface for agents that records the basics needed to work in the repo without embedding deeper context.

## Role in the repository

In the README's architecture, `AGENTS.md` serves the [[concepts/orientation-routing|orientation routing]] surface. It is meant to hold setup, build, launch, and test basics, along with repo rules and toolchain versions, while deferring durable knowledge to [[entities/okf-wiki|okf/wiki/]] and executable procedures to [[entities/agents-skills|.agents/skills/]].

The agent-ready-context skill sharpens that division of labor: skills are for repeatable actions, the OpenKB wiki is for durable context and provenance, and `AGENTS.md` is for concise operational guidance. It also treats `AGENTS.md` as the repository's routing map for agents, not a place for long-form documentation.

## Key facts from the README

- It is one of the three main surfaces that make a repository agent-ready.
- It should contain operational basics such as language and toolchain versions, setup commands, build commands, launch commands, and test invocation.
- It should not inline deeper knowledge; that belongs in the wiki.
- The README treats it as the repo's routing map for agents.
- It is part of the project's [[concepts/context-action-separation|context/action separation]] and [[concepts/context-surface-management|context surface management]] approach.
- In the agent-ready-context workflow, it should stay concise and be refreshed alongside the wiki when the repository's operational guidance changes.
- The workflow explicitly re-runs the `AGENTS.md` merge/update step when root guidance needs the latest commands or pins.

## Why it matters

The README presents `AGENTS.md` as a way to reduce repeated rediscovery by agents while keeping instructions concise and high-signal. It supports [[concepts/progressive-disclosure|progressive disclosure]] by pointing agents toward the right surface instead of overloading a single file.

The agent-ready-context skill adds that this file should stay aligned with the compiled OKF wiki and avoid becoming a parallel knowledge base. It is the front door for operations; the wiki remains the durable source of truth for repository knowledge.

## Related pages

- [[summaries/README-md]]
- [[entities/okf-wiki]]
- [[entities/agents-skills]]
- [[concepts/agent-ready-context]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/agent-orientation-index]]

See also: [[summaries/repo-snapshot]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
