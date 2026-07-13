---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__skill-creator__NOTICE.md"]
description: "Tracking source origin, modification history, and reuse constraints."
---

# Provenance Tracking

Provenance tracking is the practice of recording where content, code, or ideas came from, how they were modified, and what upstream sources or licenses govern reuse. It helps preserve trust, enable auditability, and make downstream attribution clear.

## Why it matters

Provenance tracking supports:

- clear attribution for reused material
- license compliance and reuse boundaries
- traceability from compiled artifacts back to source material
- review of whether content was copied, adapted, or newly authored

This is especially important in curated knowledge systems and reusable skill bundles, where small upstream passages may be incorporated into larger generated or maintained artifacts.

## In the source documents

The notices in [[summaries/agents__skills__skill-creator__NOTICE]] and [[summaries/agents__skills__subagent-profile-adapter__NOTICE]] show provenance tracking as a deliberate documentation layer, not just a legal formality.

Across those notices, the repository source files record:

- the component or directory identity, such as `agent-smith — skill-creator` or `agent-smith — subagent-profile-adapter`
- copyright attribution to Romain Monier
- the original upstream repository, `https://github.com/rmonier/agent-smith`
- pointers to third-party notices or licensing files when reused passages are involved

The `skill-creator` notice also says its `SKILL.md` includes a small number of passages adapted from Anthropic's and OpenAI's skill-creator materials, and directs readers to `THIRD_PARTY_NOTICES.md` for exact excerpts and sources. The `subagent-profile-adapter` notice is simpler, but it still establishes the same core provenance chain: named component, copyright holder, and upstream origin.

Together, these patterns show provenance tracking at both the package level and the file level.

## Related ideas

- [[concepts/attribution-based-reuse]] — reuse that preserves source credit and adaptation context
- [[concepts/licensing-and-attribution]] — connecting source provenance to licensing obligations
- [[concepts/license-compliance-requirements]] — ensuring reused material stays within permitted terms
- [[concepts/source-provenance]] — documenting the origin and lineage of source material
- [[concepts/provenance-aware-tool-installation]] — installing tools with awareness of where they came from and what governs them

## Practical pattern

A strong provenance record usually includes:

- the original source or upstream project
- the specific artifact or file being referenced
- the type of reuse or adaptation
- the license or notice that applies
- a pointer to exact third-party notices when excerpts are reused

When maintained consistently, provenance tracking makes it easier to inspect trust, resolve questions about ownership, and rebuild artifacts from their documented sources.