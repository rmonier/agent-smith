---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md"]
description: "Compact wiki pages for harness-specific tool facts kept separate from project knowledge."
---

# Tooling Context Pages

Tooling context pages are compact wiki records that capture the specific tool or harness details needed to safely configure or generate adapters without copying full upstream documentation. They support [[concepts/tooling-context-isolation]] by separating environment-specific tool facts from broader skill or workflow guidance, and they reinforce [[concepts/documentation-source-priority]] by requiring these pages to be grounded in the best available official documentation.

## Purpose

A tooling context page exists to preserve only the facts that matter for implementation in the current environment, and only when a specific harness is actively in use. In the source guidance, this page is written under a harness-specific path such as `okf/wiki/tooling/harnesses/<harness>.md` and acts as a concise operational reference for adapter creation rather than as part of the project's core knowledge base.

This approach helps maintain:

- focused, implementation-ready documentation rather than full doc mirrors;
- clear provenance for tool assumptions;
- reproducible adapter generation decisions;
- compatibility with wiki indexing and validation rules;
- a strict boundary between harness behavior and project truth.

It also prevents tooling notes from being created during normal repository bootstrap, which keeps baseline wiki state minimal and aligns with [[concepts/tool-boundaries]] and [[concepts/knowledge-boundaries]].

## What a tooling context page should contain

From [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]], the expected contents are the minimum adapter-relevant fields drawn from current documentation:

- official source URL or local documentation reference;
- retrieval timestamp;
- supported profile or subagent paths;
- required frontmatter fields;
- permissions or tool model, when documented;
- instruction-file behavior, when documented;
- the generation policy chosen by the user.

The policy guidance adds that these pages should explicitly signal their special status through metadata such as tooling scope, harness-oriented title, and a one-way link policy from tool context into project materials. The emphasis is on high-signal operational facts, especially where adapter behavior depends on current harness semantics, not on storing broad explanatory prose.

Because these pages are hand-authored operational context rather than generated knowledge, they should stay concise and declarative. They summarize what the harness requires now, not everything the tool can do, and they should avoid duplicating content that belongs in generated `concepts/`, `entities/`, or `summaries/` pages.

## Source and evidence expectations

Tooling context pages should be created only after checking current documentation in priority order:

1. official local documentation available in the environment;
2. official web documentation;
3. user-provided documentation;
4. community examples as secondary evidence only.

This makes tooling pages a practical expression of both [[concepts/documentation-source-priority]] and source trust levels. They are not speculative notes; they are evidence-backed summaries for configuration work. The policy also makes clear that tooling pages are not source material for project knowledge ingestion and should not be added through normal repository ingestion flows.

The OpenKB lifecycle sharpens that boundary further: generated wiki content under `okf/wiki/` is ordinarily owned by OpenKB and regenerated from staged inputs, but `okf/wiki/tooling/` is a documented exception specifically for hand-authored harness context. That exception exists so tool facts can be preserved without polluting the repository knowledge corpus or being overwritten by normal recompilation.

## Relationship to wiki governance

The source documents tie tooling context pages to broader wiki maintenance requirements. After adding one, the wiki must also:

- keep the page under `okf/wiki/tooling/harnesses/` rather than creating ad hoc folders;
- update the bundle-root `okf/wiki/index.md` so tooling content appears in a clearly labeled harness-specific section;
- ensure `okf/wiki/AGENTS.md` declares the custom `tooling/` section, with user consent for that conventions change.

This means tooling context pages participate in [[concepts/reserved-wiki-files]], [[concepts/index-based-discovery]], and [[concepts/okf-validation]]. A tooling page is not complete if it exists without the supporting convention and index updates required by validation policy.

The OpenKB lifecycle adds an important ownership rule: `okf/wiki/tooling/` may be hand-authored, but it still lives inside a bundle whose root navigation and conventions files are managed with care. The root index may point to tooling so the bundle remains discoverable, but tooling pages must remain outside normal ingestion and recompilation flows, and they should not be treated as project-source evidence in the same citation chain as generated summaries.

The governance rule is deliberately asymmetric: the root `index` may point to tooling so the bundle remains discoverable, but project concept pages and subdirectory indexes must not depend on tooling pages. Tooling context may reference project pages; project knowledge must not rely on tooling context.

## Why the concept matters

Without a dedicated tooling context page, adapter work can drift into stale assumptions, undocumented environment behavior, or scattered notes. A well-maintained page creates a narrow, auditable interface between external tool documentation and local generation workflows while keeping harness-specific behavior separate from stable project concepts.

The newer lifecycle guidance sharpens this further by treating tooling context as a deliberate exception to generated-content governance, not a default wiki layer. Since OpenKB owns normal generated pages and can overwrite them during recompile, tool-specific operational notes need a clearly reserved home where they can remain hand-maintained without desynchronizing the repository knowledge model. This makes tooling pages a practical mechanism for [[concepts/provenance-tracking]], [[concepts/progressive-disclosure]], and [[concepts/minimal-tool-scoping]].

## Practical takeaway

Tooling context pages are concise, evidence-based implementation references for tool-specific behavior. They should summarize only the fields needed for current adapter creation, cite authoritative sources, live in the reserved tooling location, and follow a one-way dependency model where tooling context can reference project material but project knowledge does not depend on tooling context. They should be created only on demand, not during baseline bootstrap, and they must remain clearly outside the normal OpenKB ingest-and-recompile path that governs generated wiki content.

## Related pages

- [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[concepts/documentation-source-priority]]
- [[concepts/tooling-context-isolation]]
- [[concepts/knowledge-boundaries]]
- [[concepts/tool-boundaries]]
- [[concepts/index-based-discovery]]
- [[concepts/okf-validation]]
- [[concepts/provenance-tracking]]
- [[concepts/progressive-disclosure]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/generated-content-governance]]
- [[concepts/source-driven-regeneration]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]