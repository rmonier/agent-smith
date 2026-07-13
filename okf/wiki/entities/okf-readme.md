---
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md"]
type: "Work"
description: "README.md documents agent-smith's agent-ready repository architecture."
---

# OKF README

The OKF README is the repository's reference document for the agent-smith architecture: it explains how the project turns a codebase into an agent-ready repository by compiling knowledge into an interlinked [[concepts/llm-wiki]]-style wiki and separating orientation, context, and actions across repo surfaces. It also frames the README as the baseline authority for OKF v0.1 offline conformance, OpenKB-style wiki maintenance guidance, and the product boundary between shipped skills and vendored tooling.

## What it covers

- Defines the agent-smith model as a repository transformation pipeline built around [[concepts/compiled-knowledge-bases]] and durable wiki context.
- Presents the wiki as a compilation target: raw sources become structured knowledge that agents can traverse, revise, and cross-link.
- Treats `AGENTS.md` as orientation, `okf/wiki/` as durable context, and `.agents/skills/` as actions, reinforcing [[concepts/context-action-separation]].
- Describes three portable product skills: `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter`.
- Distinguishes product skills from vendored toolchain copies such as `graphify` and `openkb`, which are installed as local toolchain artifacts rather than distributable product.
- Explains bootstrap and maintenance flows that check prerequisites, request consent before installs, disclose data flow, and validate the compiled wiki bundle.
- Supports air-gapped operation with local-provider routing when remote access is not desired.
- Emphasizes that the repository was transformed by the same skill pipeline it distributes.
- Links the architecture to the broader practice of [[concepts/progressive-disclosure]] and curated context surfaces.
- Describes the repository as a self-hosting example of [[concepts/agent-ready-repositories]].

## Key rules

- Knowledge that explains context stays out of files that instruct or route behavior.
- The repository should expose only the smallest useful surface to an agent at each step.
- Optional tooling may be declined, and the workflow should degrade gracefully rather than fail silently.
- Security defaults include consent-first installs, pinned dependencies, integrity recording, and explicit provider routing.
- Secrets belong in environment variables or gitignored files, not in generated pages or evidence.
- Untrusted web content and wiki pages are treated as evidence, not instructions.
- The wiki bundle and its source registry must stay coherent so deleted or moved sources do not leave stale compiled pages behind.
- Tooling pages are local-by-default and must remain outside project concept-page dependencies.

## OpenKB and wiki guidance

The README describes how OpenKB and OKF fit into the maintenance lifecycle for the repository:

- `okf/wiki/` is the durable knowledge and context source of truth.
- `okf/.okf-build/input/` is the deterministic staging area for source packs.
- `openkb add` ingests staged sources, while `openkb remove` is the deterministic inverse for deletions and moves.
- `openkb lint` is treated as a health report, while the wiki validator is the stronger pass/fail gate.
- The bundle-root `index.md` must keep `tooling/` visible when tooling pages exist.
- The repository's compiled wiki should preserve link-direction rules so project pages do not depend on tooling pages.
- The README's installed tooling references reinforce [[concepts/tooling-vendoring]], [[concepts/tooling-context-governance]], and [[concepts/tooling-link-policy]].

The document also treats knowledge capture as a lifecycle: source changes should flow through staged ingestion, validation, reconciliation, and recompile rather than hand-editing compiled outputs.

## Skill and workflow model

The README presents skills as reusable procedures and keeps them separate from durable context. It frames `skill-creator` as the template for turning repeated actions into new skills, with action triggers placed in the skill description and long-form detail pushed into scripts, references, and assets. It also describes baseline-first testing, generated-skill adoption checks, and caveat preservation as part of safe skill governance.

This reinforces [[concepts/skill-action-boundary]], [[concepts/skill-structure-conventions]], [[concepts/skill-validation-workflow]], and [[concepts/generated-artifact-adoption]] as core operational ideas.

## Notable claims

- The interlinked wiki is the repository's compiled memory.
- Agent-ready repositories reduce repeated re-derivation of codebase understanding.
- Consent, provenance, and explicit routing are necessary for safe automation.
- Tooling context belongs in a constrained boundary, not in core project knowledge pages.
- Generated knowledge should be maintained incrementally and deterministically to avoid registry drift.
- The README positions the repository as a working example of [[concepts/repository-transformation-pipelines]] and [[concepts/deterministic-validation]].

## Related pages

- [[concepts/llm-wiki]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/context-action-separation]]
- [[concepts/progressive-disclosure]]
- [[concepts/agent-ready-repositories]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/consent-first-tooling]]
- [[concepts/air-gapped-operation]]
- [[concepts/data-flow-disclosure]]
- [[concepts/explicit-provider-routing]]
- [[concepts/deterministic-validation]]
- [[concepts/okf-validation]]
- [[concepts/okf-workflow-governance]]
- [[concepts/tooling-link-policy]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/skill-action-boundary]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-validation-workflow]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/caveat-preservation]]
- [[summaries/README-md]]