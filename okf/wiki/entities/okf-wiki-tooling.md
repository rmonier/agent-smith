---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
type: "Other"
description: "User-scoped wiki area for local harness and provider context in OKF"
---

# okf/wiki/tooling/

`okf/wiki/tooling/` is the user-scoped wiki area reserved for local harness and provider context in OKF.

## What it is

This directory is a special wiki exception for hand-authored tooling pages. It is not project source material and should not be ingested through normal wiki compilation flows. The validation script treats it as local-by-default tooling context that may be absent on other clones, while still requiring the wiki to remain navigable when local pages exist.

It also serves as the home for harness-specific evidence when the active runtime has been identified and persisted intentionally. The subagent-profile-adapter skill uses it for optional harness documentation, but only after checking runtime signals and current docs rather than assuming a harness from installed tools.

The subagent-profile-adapter skill frames this directory as runtime-specific projection space: it helps generate harness-native subagent or profile adapters, but it does not create a portable subagent standard. Instead, it writes short native adapter files that point back to `AGENTS.md`, `okf/wiki/`, and skills while keeping the project knowledge base separate from harness details.

The OpenKB lifecycle guidance reinforces this directory as a deliberate exception: tooling pages are hand-authored context, not repo source evidence, and they must remain outside the normal `openkb add` / `openkb recompile` content flow unless a user explicitly approves a tooling-page edit.

## Key facts

- It is local by default and meant to vary per user and clone.
- It may contain a committed `index.md` navigation stub plus local pages under `harnesses/` and `providers/`.
- It must stay outside ordinary project knowledge boundaries and follow [[concepts/tooling-boundaries]] and [[concepts/local-by-default-tooling]].
- Tooling pages are intended to support runtime context, not project truth, which aligns with [[concepts/knowledge-boundaries]] and [[concepts/documentation-layer-separation]].
- Project OKF concept pages and subdirectory indexes must not link back into `okf/wiki/tooling/`.
- The bundle-root `index.md` and `log.md` are reserved navigation/history files and are exempt from the forbidden direction.
- When non-reserved tooling pages exist, the bundle-root `index.md` must reference `tooling/` in a clearly labeled harness-specific section.
- When non-reserved tooling pages exist, a committed `tooling/index.md` stub must also exist so the root reference resolves on clones that do not have local tooling pages.
- Local tooling pages are expected to carry at least one outgoing wikilink so they are not classified as orphaned by structural lint.
- Tooling context should stay narrow and short, with profile files pointing back to `AGENTS.md`, `okf/wiki/`, and skills instead of embedding long project context.
- OpenKB-managed pages under `concepts/`, `entities/`, and `summaries/` should never be hand-edited to route into tooling; any tooling-specific content belongs here instead.

## Policy role

The referenced policy makes `okf/wiki/tooling/` the home for:

- required harness build records when a harness can be identified
- optional harness documentation when the subagent-profile-adapter is in use
- a committed root stub that keeps navigation coherent across clones
- a one-way link model where tooling can point outward, but project pages do not point back inward
- a narrow exception to the normal OpenKB lifecycle, since tooling pages are curated context rather than compiled repository knowledge

It also requires that local tooling pages link outward to durable project knowledge, and that project pages do not link back into tooling. That makes this directory a controlled exception within [[concepts/tooling-context-governance]] and [[concepts/tooling-link-policy]]. The implementation enforces that exception with regex-based markdown scanning, reserved-file handling, and root-index checks that activate whenever tooling contains non-reserved pages.

The OpenKB lifecycle document further treats tooling as separate from compiled knowledge maintenance: the wiki's normal ingest/recompile/remove/reconcile flow is for repository sources and promoted findings, while tooling pages remain hand-authored runtime context. In that lifecycle, tooling is one of the few sanctioned places where the wiki is not a pure projection of ingested source material.

The subagent-profile-adapter script adds concrete enforcement details: it scans Markdown under `okf/wiki`, ignores code fences and inline code, warns when tooling pages lack `scope: tooling` or `type: tooling-context`, and treats `index.md` and `log.md` as reserved navigation files. It also distinguishes between tooling pages and project pages when deciding where tooling links are forbidden.

When tooling contains non-reserved pages, the validator requires both a root `index.md` reference to `tooling/` and a committed `tooling/index.md` stub. That ensures the bundle remains navigable on clones that do not have any local tooling pages, while still making the local harness area visible to curated users.

The subagent-profile-adapter skill further treats this directory as part of a broader runtime-adapter workflow: detect the active harness, confirm support for local subagents or profiles, choose how generated files are tracked, then validate that tooling pages remain isolated from project concept pages.

## Related pages

- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[entities/okf-wiki-tooling-index-md]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki]]
- [[entities/subagent-profile-adapter]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/openkb-lifecycle]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]
