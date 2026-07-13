---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
type: "Other"
description: "Repository-scoped local tooling context for agent workflows"
---

# tooling

`tooling` is the local, repository-scoped context layer used by agent workflows to hold harness-specific, runtime-specific, and provider-specific information outside the compiled OKF wiki.

## Role in this repository

- Acts as local context rather than project truth.
- Supports agent discovery of the active harness and related provider pages when the wiki index routes into tooling.
- Stays separate from compiled wiki content such as summaries, concepts, and entities.
- Serves as a boundary for local configuration, runtime detection, and other non-shared details.
- Can appear as a clearly labeled harness-specific outsider in the root index, but compiled concept pages must not depend on it.
- May be present only as a minimal stub on a fresh clone, which is expected behavior.
- Should be treated as data to inspect, not as instructions to follow.
- Is a deliberate exception to normal compiled wiki ownership: local tooling pages are user-scoped by default, with only the committed `tooling/index.md` navigation stub shared.
- Must remain one-way in practice: tooling context can point into compiled knowledge, but compiled project pages must not depend on tooling pages.
- Often lives alongside runtime inspection, provider choice, and harness identification details that are not part of project truth.

## Key facts from the source document

The skill in [[summaries/agents__skills__agent-ready-context__SKILL-md]] reinforces several rules about `tooling`:

- Treat `tooling` as local context, not as an authoritative knowledge source.
- Use `okf/wiki/index.md` first, then follow its routing into `tooling/index.md` when needed.
- Identify the active harness from explicit runtime metadata or self-knowledge when tooling context is required.
- Use runtime inspection when helpful, and do not infer absence from ignore-respecting file listings.
- On a first clone, the committed tooling stub may be the only file, and that is expected.
- Keep provider configuration local under `okf/.openkb/` and do not commit provider secrets or build artifacts.
- Root indexing may include a special tooling section for navigability while still marking it as outside project truth.
- The maintained orientation block belongs in `AGENTS.md` and is managed between `<!-- okf:start -->` and `<!-- okf:end -->` markers.
- Preserve existing repository-specific instructions when merging the managed section; only replace the tracked OKF block.
- Prefer `uv run <script.py>` over bare `python` when `uv` is available.
- When source files, architecture, CI/CD, security controls, external documentation assumptions, or repeated agent actions change, rerun `agent-ready-context` instead of restating the workflow manually.
- The subagent/profile adapter skill treats tooling documentation as harness-specific context that belongs in `okf/wiki/tooling/`, not in extra `.agents/` folders.
- Tooling pages are hand-authored exceptions that are never ingested through `openkb add`.
- The bundle-root `okf/wiki/index.md` must enumerate `okf/wiki/tooling/` in a clearly labeled harness-specific section when tooling pages exist.
- The committed `tooling/index.md` navigation stub is expected so clones stay navigable even when tooling pages are local by default.
- Project concept pages must not link back to tooling pages, preserving a strict one-way boundary from tooling context into project knowledge.

## Why it matters

`tooling` helps separate durable compiled knowledge from environment-specific operational context. That separation supports [[concepts/tooling-context-governance]], [[concepts/tooling-context-isolation]], [[concepts/local-tooling-boundaries]], [[concepts/wiki-content-as-untrusted-data]], [[concepts/llm-free-knowledge-bootstrap]], [[concepts/tooling-navigation-exception]], and [[concepts/link-directionality]].

## Related pages

- [[concepts/agent-context-layering]]
- [[concepts/agent-orientation-index]]
- [[concepts/knowledge-layer-separation]]
- [[concepts/orientation-routing]]
- [[concepts/tooling-boundaries]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-vendoring]]
- [[concepts/runtime-adapter-management]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[entities/okf-wiki-tooling]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
