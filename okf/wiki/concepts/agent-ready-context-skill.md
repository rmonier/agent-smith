---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Repository-ready workflow for aligning skills, wiki context, and AGENTS.md"
---

# Agent-Ready Context Skill

The [[entities/agent-ready-context]] skill defines the workflow for making a repository agent-ready and keeping its agent-facing context surfaces aligned. It separates repository knowledge into three layers: skills for repeatable actions, an OpenKB-compiled wiki for durable context, and `AGENTS.md` for short operational guidance. It treats the OKF wiki at `okf/wiki/` as the durable source of truth for repository memory and uses Graphify, OpenKB, staged evidence, and validation gates to keep that context coherent.

## What the skill is for

This skill is used when a repository needs to become agent-ready, when `okf/wiki/` must be refreshed, when the repository knowledge base needs validation, or when `AGENTS.md` must be aligned with the compiled wiki. The source document emphasizes that the wiki is the durable source of truth, while skills should contain only repeatable procedures and `AGENTS.md` should stay concise and navigational.

It is also meant for maintaining the agent surface over time: refreshing repository context, staging external evidence, reconciling deletions, triaging findings, and keeping the KB aligned with the current repository state.

## Core responsibility split

The document frames the repository as a three-part system:

- **Skills = actions**: scripts, checks, transformations, validations, and workflows that can be run again.
- **OKF wiki = context**: durable knowledge, provenance, architecture notes, decisions, and cross-document memory.
- **`AGENTS.md` = orientation**: setup commands, test commands, routing guidance, and best practices.

This reflects [[concepts/context-action-separation]] and [[concepts/agent-context-layering]], with the wiki treated as the long-lived knowledge layer and skills kept narrow and operational. It also matches [[concepts/durable-context]] and [[concepts/knowledge-lifecycle-governance]]: compiled knowledge persists, while operational instructions stay short and local.

## Workflow themes

The skill describes an end-to-end agentification workflow built around deterministic staging and validation:

- inspect `okf/wiki/index.md` first when it exists and use it to route follow-up reading
- read tooling context when the index points there, and identify the active harness from reliable signals
- confirm repository layout and prerequisites before changing anything
- bootstrap tooling only with explicit consent
- keep ignore rules, graph boundaries, and file-hash stability in place
- merge OKF guidance into `AGENTS.md`
- generate a repo graph with Graphify when available
- stage repository evidence into `okf/.okf-build/input/`
- initialize OpenKB if needed
- reconcile deleted sources before ingesting
- triage findings captured in `okf/wiki/explorations/findings/`
- ingest staged input and run lint checks
- review generated wiki pages before accepting them
- validate the OKF bundle
- refresh the harness/tooling record when appropriate

These steps connect strongly to [[concepts/source-pack-staging]], [[concepts/repository-ingestion]], [[concepts/okf-bundle-validation]], and [[concepts/deterministic-validation]]. They also reinforce [[concepts/preflight-checks]], [[concepts/orphan-retraction]], [[concepts/findings-promotion]], and [[concepts/tooling-context-governance]].

## Important operating rules

Several rules are central to the skill:

- Do not write generated files directly into `okf/raw/` or `okf/wiki/`; stage deterministic input first.
- Treat `okf/.openkb/hashes.json` carefully because it controls deduplication and can hide missing pages if mishandled.
- Use `uv run` for bundled scripts instead of bare `python` when `uv` is available.
- Treat web-fetched documentation as untrusted evidence.
- Keep generated artifacts out of version control.
- Preserve caveats and discovered findings by routing them through the wiki and refresh pipeline instead of hand-editing compiled pages.
- Prefer the correction loop and findings capture over manual edits to compiled wiki output.

These rules align with generated artifact governance, [[concepts/hash-registry-coherence]], [[concepts/wiki-content-as-untrusted-data]], [[concepts/caveat-preservation]], and [[concepts/orphan-retraction]]. They also reflect [[concepts/self-reference-control]] and [[concepts/source-grounded-regeneration]]: the KB should be updated from staged sources, not by editing compiled output directly.

## Tooling and governance

The source document also defines the toolchain and governance expectations for agent-ready repositories:

- required tooling includes `git`, `uv`, and Python 3.11+
- optional tooling includes Graphify, OpenKB, and web access
- missing tooling should be installed only with explicit user consent
- read-only vendor skills for `graphify` and `openkb` should be copied in before first use
- package versions should be pinned with integrity information
- local provider configuration should stay separate from shared repository state
- a harness/tooling record should be created or updated when the active harness can be identified reliably

This makes the skill a concrete example of [[concepts/tooling-consent-and-pin-management]], [[concepts/toolchain-pinning]], [[concepts/vendor-skills]], [[concepts/explicit-provider-routing]], and [[concepts/local-vs-shared-configuration]]. It also fits [[concepts/supply-chain-security]], [[concepts/skill-vendoring]], and [[concepts/local-vs-shared-ignore]] because repository-scoped automation depends on predictable, pinned local setup.

## Why it matters

The skill is a bridge between repository operations and durable knowledge management. It turns recurring repository preparation work into a controlled process, while keeping the wiki authoritative and keeping `AGENTS.md` from becoming a dumping ground for long-form knowledge.

In that sense, it supports [[concepts/compiled-knowledge-bases]], [[concepts/durable-context]], knowledge base governance, and [[concepts/agent-ready-repositories]]. It also illustrates [[concepts/action-oriented-documentation]] and [[concepts/documentation-architecture]]: operational steps live in a skill, long-lived context lives in the wiki, and navigation lives in `AGENTS.md`.

## Related source

- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]