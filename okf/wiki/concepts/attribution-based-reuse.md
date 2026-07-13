---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__LICENSING-md.md"]
description: "Reuse model that permits adaptation with attribution and license compliance."
---

# Attribution-Based Reuse

Attribution-based reuse is a content and code reuse model where material can be adapted, redistributed, and incorporated into new work as long as the original source is credited and the applicable license terms are preserved. It sits between fully permissive reuse and stricter proprietary control, and it is central to how this repository handles borrowed documentation and upstream adaptation.

## Core idea

The key requirement is not just permission to reuse, but responsibility to preserve provenance. That usually means:

- retaining copyright notices where required
- naming upstream sources clearly
- respecting license-specific conditions
- distinguishing original work from adapted material

This makes reuse auditable and lowers the risk of accidental license drift.

## In the source document

The licensing page for [[summaries/agents__skills__skill-creator__LICENSING-md]] shows attribution-based reuse in practice:

- original documentation such as `SKILL.md`, plus original files under `references/` and `assets/`, are licensed under [[concepts/creative-commons-attribution-4-0]]
- executable files under `scripts/` are licensed separately under [[concepts/apache-license-2-0]]
- `SKILL.md` is presented as original work overall, but it incorporates a small number of passages adapted from Apache-2.0 upstream skill-creator material
- the exact borrowed passages, upstream sources, and copyright notices are tracked in `THIRD_PARTY_NOTICES.md`
- conceptual lineage is documented in `references/source-attribution.md`
- full license texts are stored in `LICENSES/`

## Why it matters

Attribution-based reuse supports collaborative knowledge work because it lets a project:

- reuse useful upstream material without hiding its origin
- keep legal obligations visible to downstream users
- separate conceptual influence from direct copying
- maintain trust in generated or curated documentation

In wiki and knowledge-base workflows, this also reinforces [[concepts/provenance-tracking]] and [[concepts/knowledge-linking-and-citations]], since reuse is most reliable when the source trail stays visible.

## Related concepts

- [[concepts/licensing-and-attribution]]
- [[concepts/open-source-attribution]]
- [[concepts/permissive-open-source-licensing]]
- [[concepts/license-conditions]]
- [[concepts/provenance-tracking]]
- [[concepts/knowledge-linking-and-citations]]


See also: [[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]]

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt]]

See also: [[summaries/agents__skills__subagent-profile-adapter__NOTICE]]