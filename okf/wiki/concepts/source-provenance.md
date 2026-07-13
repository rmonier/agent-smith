---
type: "Concept"
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__NOTICE.md"]
description: "How source metadata preserves traceable origin, reuse, and validation."
---

# Source Provenance

Source provenance is the practice of recording where a document, asset, or snippet came from, who created it, how it entered the knowledge base, and how it fits into a repository's broader [[concepts/knowledge-compilation-pipeline|knowledge compilation pipeline]]. It supports provenance tracking, licensing, trust assessment, and regeneration by making reuse and validation traceable.

In repositories that aim to become [[concepts/agent-ready-repositories|agent-ready repositories]], provenance also helps separate durable context from executable actions and orientation files. That matters because the repository may carry multiple surfaces at once: operational instructions in `AGENTS.md`, compiled memory in `okf/wiki/`, and reusable procedures in `.agents/skills/`. Source provenance is the connective tissue that lets those surfaces remain auditable without collapsing into one another.

## Why it matters

- It preserves attribution for reused material.
- It helps distinguish original content from upstream imports.
- It provides a basis for compliance review and trust assessment.
- It makes later validation and maintenance easier when multiple sources converge.
- It helps prevent churn when staged content is regenerated from the same source.
- It supports a repository transformation workflow where source packs, manifests, and compiled knowledge can be compared across runs.

## What provenance usually captures

- Original source or upstream repository
- Author or maintainer identity
- Copyright or license notice
- Source path inside the repository
- Commit hash or snapshot identifier
- Ingestion or staging context
- Stable content hash for the staged form
- Whether the content was copied, bundled, split, or normalized before ingestion

In a wiki-compilation workflow, provenance metadata is most useful when it travels with the staged artifact rather than living only in an external log. That makes the record durable enough to support later review, rebuilds, and removal or refresh operations.

## Evidence from this document

The repository README describes a provenance-aware architecture for agent-facing knowledge and tooling:

- `AGENTS.md` is the orientation surface, with operational basics and repo rules kept in-file.
- `okf/wiki/` is the context surface for durable OpenKB-compiled knowledge.
- `.agents/skills/` is the actions surface for repeatable procedures and scripts.
- Harness adapters are runtime projections only, not source of truth.

That structure is a practical example of provenance-conscious knowledge management because each surface has a distinct role, a distinct audience, and a distinct validation path. It also reinforces [[concepts/context-action-separation]] and [[concepts/documentation-layer-separation]]: instructions, evidence, and operational procedures are intentionally not mixed together.

The README also describes the agent-smith bootstrapping workflow in terms of a compiled knowledge base:

- Knowledge is treated as source code compiled into a wiki.
- Structural context is ingested alongside evidence and provenance.
- OpenKB is used to compile, validate, and maintain the wiki bundle.
- Deleted or moved sources are reconciled so the knowledge base stays faithful to the current repository state.

That aligns with provenance as an operational guarantee, not just a citation habit: the repository can explain where knowledge came from, how it was transformed, and whether it still matches the current source tree.

## Provenance in staged repository content

The README's installation and maintenance sections describe a pattern that strengthens provenance tracking across the repo:

- The `agent-ready-context` skill checks prerequisites, records versions, and asks before installing anything.
- Optional tools such as `graphify` and `openkb` are treated as vendored toolchain copies when needed.
- The workflow can degrade to deterministic or zero-LLM behavior when semantic compilation is unavailable.
- Air-gapped operation keeps the data flow local when requested.

These details show that provenance is not only about authorship. It also includes toolchain identity, pinning, and execution context. That makes provenance closely related to [[concepts/toolchain-pinning]], [[concepts/trust-on-first-use]], [[concepts/data-flow-disclosure]], and [[concepts/explicit-provider-routing]].

## What the README contributes

The README frames the whole repository as a transformation system that preserves provenance while compiling knowledge:

- Generated surfaces such as `AGENTS.md` and `okf/wiki/` are produced by agent-smith's own skills.
- The product skills remain portable and reusable, while vendored tool skills are explicitly marked as copies.
- The workflow keeps source metadata and evidence visible so contributors can audit what came from where.
- The project describes file-scoped licensing and third-party notice handling as part of the same traceability story.

That means source provenance here is not just a metadata field. It is part of the repository's design for [[concepts/knowledge-lifecycle-governance|knowledge lifecycle governance]] and [[concepts/generated-content-governance|generated content governance]].

## Related practices

- [[concepts/attribution-based-reuse]] — reuse should retain credit and source visibility.
- [[concepts/open-source-attribution]] — upstream authorship and licensing should remain visible.
- [[concepts/license-compliance-requirements]] — provenance helps determine how content may be reused.
- [[concepts/source-trust-levels]] — provenance is one input to judging confidence in a source.
- [[concepts/provenance-aware-tool-installation]] — tools should be installed and tracked with source awareness.
- [[concepts/deterministic-source-pack-staging]] — staged inputs should hash and reproduce consistently.
- [[concepts/source-pack-manifest]] — manifests preserve the record of what was staged.
- [[concepts/document-normalization]] — normalization helps keep provenance hashes stable.
- [[concepts/compiled-knowledge-bases]] — compiled knowledge should remain traceable back to source material.
- [[concepts/source-provenance]] also supports [[concepts/evidence-staging]] by making imported material auditable.

## Practical rule

If content is imported, copied, or derived, keep enough source metadata to answer three questions later:

1. Where did it come from?
2. Who made it?
3. Under what terms can it be reused?

For staged repository content, a useful minimum is the source path, a stable content hash, and the commit or snapshot that last touched the file. That discipline turns a document from an isolated artifact into a traceable part of the wiki's knowledge graph.

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__skill-creator__LICENSING-md]]

See also: [[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__NOTICE]]

## Related Documents
- [[summaries/README-md]]


See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/okf-spec]]