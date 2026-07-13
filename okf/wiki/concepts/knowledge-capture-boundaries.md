---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Rules for what becomes durable wiki knowledge and how it is captured"
---

# Knowledge Capture Boundaries

Knowledge capture boundaries define what belongs in operational guidance versus what should be promoted into the OpenKB wiki as durable, shared knowledge. In this repository pattern, `AGENTS.md` stays narrow and practical, while the OKF wiki holds architecture, decisions, evidence, reusable context, and the operational rules for how that knowledge is maintained.

## Core Boundary

The source template makes a strong distinction between:

- **Skills**: repeatable actions, scripts, checks, transformations, and tool workflows.
- **OKF wiki**: durable context, evidence, provenance, architecture, decisions, and lifecycle governance.
- **AGENTS.md**: orientation, setup, test commands, repo rules, and navigation pointers.

This separation is a form of [[concepts/knowledge-layer-separation]] and [[concepts/context-action-separation]]: action lives in skills, context lives in the wiki, and the top-level agent file only routes between them. The OpenKB lifecycle adds a further boundary: wiki content is untrusted data, not instruction text, and the wiki should be read as a knowledge surface rather than a control plane.

## What Should Be Captured

The template says durable project facts discovered during work should be recorded as findings in `okf/wiki/explorations/findings/`. Those findings should include:

- evidence such as `file@commit` or test output
- why the finding matters
- links to related wiki pages using wikilinks
- `type: Finding` frontmatter
- an index entry under `## Explorations`

This supports [[concepts/evidence-staging]] and [[concepts/findings-promotion]]: observations are first staged as findings, then later compiled into broader wiki knowledge when the KB is refreshed. The lifecycle guide adds that findings are the right place for discovered facts that are not already stated in committed source documents, while procedures belong in skills and harness/runtime observations belong in hand-authored tooling pages.

## What Should Not Be Captured Here

The template explicitly warns against:

- duplicating durable knowledge inside `AGENTS.md`
- deep-linking into individual wiki pages from agent orientation files
- directly editing compiled wiki pages under `concepts/`, `entities/`, or `summaries/`
- inventing provenance or treating wiki content as instruction text

That policy protects [[concepts/knowledge-boundaries]], [[concepts/wiki-content-as-untrusted-data]], [[concepts/documentation-layer-separation]], and [[concepts/documentation-architecture]]. The OpenKB lifecycle also adds a stronger operational rule: generated wiki content is a projection of ingested sources, so hand-editing compiled pages is only appropriate for narrow output-only curation cases, not for correcting source-backed knowledge.

## Practical Effect

In practice, the boundary means:

- `AGENTS.md` is an index, not a knowledge store.
- `okf/wiki/index.md` is the first routing layer for durable context.
- Findings are the intake valve for new durable facts.
- Compiled pages are the destination for synthesized knowledge, not the place to improvise during ingestion.
- `okf/.openkb/hashes.json`, `okf/raw/`, and `okf/wiki/` must stay coherent so captured knowledge can be regenerated and audited.

The lifecycle guide also makes the maintenance loop explicit: read the current wiki first, stage sources deterministically, recompile when the source set changes, and use `openkb remove` when repository sources are deleted or moved. That adds [[concepts/manifest-authoritative-reconciliation]], [[concepts/registry-drift]], [[concepts/source-driven-regeneration]], and [[concepts/orphan-retraction]] to the boundary: knowledge capture is only durable when the ingestion registry, raw copies, and compiled wiki stay in sync.

## Related Page

- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]