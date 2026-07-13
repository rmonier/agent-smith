---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md"]
description: "Governance rules for compiling and maintaining OKF wiki context"
---

# OKF Wiki Governance

OKF wiki governance is the set of rules that controls how compiled repository knowledge is created, updated, reviewed, and kept consistent inside the OpenKB wiki. It defines what belongs in the wiki, how changes should flow through source documents, and which edits are allowed to happen directly versus through regeneration, staged evidence, or tightly scoped exceptions.

## Core principles

- The wiki is a compiled knowledge base, not a freeform scratchpad.
- Source documents are the authoritative inputs; wiki pages are derived outputs.
- Generated content should usually be corrected by updating source material and re-ingesting, not by hand-editing compiled pages.
- Governance also includes clear boundaries between durable context, executable skills, AGENTS.md orientation, and local tooling context.
- The durable context source of truth is `okf/wiki/`, while the OpenKB KB root is `okf/`.
- Project skills are for repeatable actions; the wiki is for durable knowledge and provenance; `AGENTS.md` is for concise orientation and routing.

## Governance rules from the source

The `agent-ready-context` skill describes a strict split across repository surfaces:

- **Skills** contain repeatable actions, checks, workflows, and tooling orchestration.
- **OKF wiki** contains durable context, provenance, architecture notes, and cross-agent memory.
- **AGENTS.md** contains concise operational orientation and routing guidance.
- **Tooling context** is user-scoped runtime knowledge that can live under `okf/wiki/tooling/` only in the narrow cases defined by the tooling policy.

This separation is a central governance rule because it prevents long-term knowledge from being mixed with action procedures or short-lived guidance. It also keeps local harness notes out of the project knowledge graph while still allowing them to support reproducible runs. See [[concepts/context-action-separation]], [[concepts/documentation-layer-separation]], and [[concepts/documentation-architecture]].

## Allowed update paths

The document emphasizes that wiki governance depends on controlled update channels:

- Stage deterministic source input under `okf/.okf-build/input/` instead of writing directly into `okf/raw/` or `okf/wiki/`.
- Ingest staged input with OpenKB so compiled pages remain reproducible.
- Run bundled scripts with `uv run` and treat missing tooling as a prerequisite issue, not something to silently bypass.
- Use the correction loop when generated pages are weak, vague, or misclassified.
- Capture discovered-but-not-yet-compiled knowledge as findings pages rather than patching compiled pages by hand.

These rules connect OKF governance to [[concepts/source-driven-regeneration]], [[concepts/source-grounded-regeneration]], [[concepts/evidence-staging]], [[concepts/findings]], [[concepts/editorial-curation-passes]], and [[concepts/deterministic-source-pack-staging]].

## Exception handling

The source also describes narrow exceptions where direct wiki intervention is allowed:

- user-approved edits to `okf/wiki/AGENTS.md` conventions
- local `okf/wiki/tooling/` pages that are user-scoped
- zero-LLM skeleton fallback output
- findings capture pages
- a guarded editorial pass for output-only semantic lint issues

These exceptions are governed by policy, not convenience. They preserve the default rule that compiled wiki pages should not be edited casually. Tooling pages are especially constrained: they are local by default, must not become speculative documentation, and must stay separate from project truth. This ties into [[concepts/generated-content-governance]], [[concepts/tooling-context-governance]], [[concepts/local-by-default-tooling]], and [[concepts/tooling-navigation-exception]].

## Consistency and safety concerns

The document highlights several governance risks the wiki must defend against:

- registry drift in `okf/.openkb/hashes.json`
- self-referential ingestion loops if KB roots are graph-included
- stale or orphaned pages when source files are removed
- supply-chain risk from unpinned or mismatched tooling
- accidental leakage of local credentials or provider settings
- broken navigation if local tooling pages are created without a committed stub or without required links to durable project pages

These concerns connect to [[concepts/hash-registry-coherence]], [[concepts/self-reference-control]], [[concepts/orphan-retraction]], [[concepts/integrity-pinning]], [[concepts/privacy-preserving-tooling]], [[concepts/tooling-navigation-exception]], and [[concepts/wikilink-integrity]].

## Relationship to the source document

The source skill uses OKF wiki governance as a practical operating model for agent-ready repositories. It treats the wiki as the durable knowledge layer, positions `AGENTS.md` as the entry-point orientation layer, and constrains all updates to controlled, reproducible workflows.

The tooling policy adds an important refinement: harness and adapter context can exist, but only as a carefully bounded local overlay with explicit validation, committed navigation stubs where needed, and no dependence from project pages back into tooling. That makes this concept a good fit for the broader idea of [[concepts/knowledge-lifecycle-governance]] and for the source document [[summaries/agents__skills__agent-ready-context__SKILL-md]].

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]