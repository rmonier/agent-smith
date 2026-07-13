---
type: "Summary"
description: "Defines when tooling context may be stored in OKF and how it must be linked."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"
---

# Tooling Context Policy

This document defines strict rules for when harness and adapter knowledge may be stored inside OKF/wiki and how that tooling content must be organized, linked, and kept out of project truth.

## Main policy

Tooling context is allowed in only two cases:

1. **Harness build record** - a required-but-best-effort record for each agent-ready build or refresh pass, stored under `okf/wiki/tooling/harnesses/<harness>.md`.
2. **Adapter/profile tooling context** - fuller harness documentation, but only when the subagent-profile-adapter is actively used for a detected or user-selected harness.

The document warns against speculative tooling pages beyond these two cases and treats tooling knowledge as interchangeable runtime context rather than project knowledge.

## Harness build records

Each harness record should capture:

- harness name and version
- how it was identified, using [[concepts/runtime-ambiguity-resolution]] rules
- date of the pass
- harness-specific quirks observed during the pipeline, such as sandbox limits, background-task behavior, or timeout needs

If the harness cannot be identified reliably, the record should be skipped, the run report should explain why, and the pipeline should continue. The document emphasizes that the record is informational, not a gate.

## Tooling storage layout

The recommended location is `okf/wiki/tooling/` with:

- `index.md` as a committed, user-neutral navigation stub
- `harnesses/` for one page per harness
- `providers/` for optional provider or model runtime notes

This section is framed as a local, hand-authored exception inside the wiki rather than a separate storage system.

## Governance and constraints

The policy says to:

- declare the `tooling/` section in `okf/wiki/AGENTS.md`
- avoid ingesting tooling pages through `openkb add`
- avoid creating extra non-standard folders under `.agents/`
- keep tooling pages out of the normal project ingestion flow

It also states that `AGENTS.md` should not contain long tooling explanations, only mention that harness-specific profile adapters may exist.

## Git and index behavior

Tooling context is described as **user-scoped** and local by default. The document specifies a `.gitignore` pattern that keeps everything under `okf/wiki/tooling/` local except the committed `index.md` stub.

It also requires the bundle-root `okf/wiki/index.md` to include a labeled tooling entry whenever non-reserved tooling pages exist, so the wiki remains coherent across clones. The stub is intended to point to the local directory without enumerating local pages.

## Link policy

The document allows links from tooling pages to:

- `AGENTS.md`
- `.agents/skills/`
- project pages under `okf/wiki/`

It forbids the reverse direction: project concept pages must not link back into tooling pages, and subdirectory indexes must not point to `okf/wiki/tooling/`.

A key lint rule is that every local tooling page must include at least one outgoing wikilink to durable project knowledge, so local pages are not treated as orphans.

## Validation and default artifact rule

A validator script is specified for enforcing the policy:

- it checks that project concept pages do not link to tooling
- it checks that committed indexes reference tooling when needed
- it checks that the `tooling/index.md` stub exists
- it checks that local tooling pages have at least one wikilink

The default artifact rule says a baseline bootstrap should create only the minimal harness build record and, on first use, the committed `tooling/index.md` stub plus the root index entry. Other runtime hints or policy outputs should stay temporary unless explicitly requested.

## Key idea

The central idea is to keep runtime harness knowledge available for debugging and reproducibility while preventing it from becoming part of the project knowledge graph or creating broken links across clones. This is a clear boundary between [[concepts/wikilink-integrity]], [[concepts/git-tracking-policy]], and project-side wiki content.

## Related Concepts
- [[concepts/local-tooling-boundaries]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-stub-resolving]]
- [[concepts/tooling-context-governance]]
- [[concepts/link-directionality]]
- [[concepts/reserved-navigation-files]]
- [[concepts/okf-wiki-governance]]
- [[concepts/knowledge-boundaries]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/harness-native-profiles]]
- [[concepts/tooling-boundaries]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-link-policy]]
- [[concepts/tooling-context-pages]]
- [[concepts/tooling-navigation-exceptions]]
- [[concepts/local-by-default-tooling]]
- [[concepts/reserved-markdown-files]]
- [[concepts/reserved-markdown-file-rules]]
- [[concepts/index-based-discovery]]
- [[concepts/knowledge-capture-boundaries]]

## Entities
- [[entities/okf-wiki-tooling-index-md]]
- [[entities/okf-wiki-tooling]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-agents-md]]
- [[entities/references-tooling-context-policy-md]]
- [[entities/runtime-detection-md]]
- [[entities/gitignore]]
- [[entities/git-info-exclude]]
- [[entities/openkb-cli]]
- [[entities/openkb]]
- [[entities/okf]]
- [[entities/tooling]]
- [[entities/okf-wiki]]
- [[entities/openkb-wiki]]
- [[entities/git]]
- [[entities/uv]]
