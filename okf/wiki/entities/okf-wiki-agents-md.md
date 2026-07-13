---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
type: "Work"
description: "Wiki governance file that orients agents and anchors OKF workflow"
---

# OKF Wiki AGENTS.md

`OKF Wiki AGENTS.md` is the wiki orientation and governance file that tells agents how to work inside the OpenKB wiki. In this document, it is treated as the canonical repo guide for agent-facing behavior, separate from durable knowledge in [[concepts/compiled-knowledge-bases]] and runtime-specific adapter outputs.

## Role In The Workflow

The `agent-ready-context` skill depends on `AGENTS.md` being present, refreshed, and aligned with the OKF wiki before it can safely run repository agentification tasks. It treats the file as the repository's orientation layer: a short, stable guide that agents consult before using skills or writing runtime-specific projections.

The file also sits inside a broader agent-ready workflow that keeps three surfaces distinct:

- skills for repeatable actions and validations
- the OKF wiki for durable repository knowledge and provenance
- `AGENTS.md` for concise operational orientation and routing

That separation is central to [[concepts/context-action-separation]] and [[concepts/documentation-layer-separation]].

## Key Facts From The Document

- `AGENTS.md` is the canonical orientation file for agent behavior in the repository.
- It should remain distinct from OKF wiki content, skills, and generated runtime adapters.
- The `agent-ready-context` skill expects this file to exist before agent-ready setup, KB refresh, or adapter generation begins.
- The document frames `okf/wiki/` as the durable context source of truth and warns against creating a parallel repository wiki.
- Generated files should not be written directly into `okf/raw/` or `okf/wiki/`; deterministic source packs should be staged under `okf/.okf-build/input/` first.
- The workflow emphasizes a correction loop: fix source documents and re-ingest rather than patching compiled wiki pages.
- Findings discovered during work belong under `okf/wiki/explorations/findings/` when they are agent-discovered rather than source-read knowledge.
- The wiki governance layer should declare a custom `tooling/` section, and that declaration belongs in wiki governance rather than runtime adapters.
- The file is part of the layer separation that keeps project knowledge, orientation, and runtime projections from collapsing into one another.

## Related Ideas

- [[concepts/agent-orientation-index]] for the idea of a short agent-facing entrypoint.
- [[concepts/agent-context-layering]] for separating orientation, durable knowledge, and actions.
- [[concepts/documentation-layer-separation]] for keeping different documentation roles distinct.
- [[concepts/tooling-context-governance]] for the rules around tooling-specific wiki content.
- [[concepts/runtime-adapter-management]] for generating harness-specific runtime files from repo context.
- [[concepts/subagent-role-design]] for choosing bounded, task-specific runtime roles.
- [[concepts/deterministic-okf-staging]] for staging inputs before compilation.
- [[concepts/findings]] for capturing discovered knowledge in a dedicated namespace.
- [[concepts/knowledge-lifecycle-governance]] for the broader refresh-and-correction loop.

## Relationship To The Summarized Skill

The summarized [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]] treats `AGENTS.md` as a prerequisite and a canonical anchor. The `agent-ready-context` skill strengthens that role by tying `AGENTS.md` to the OKF workflow: it should point agents toward the wiki front door, preserve operational basics, and stay short enough that durable knowledge remains in the wiki instead of the orientation file.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
