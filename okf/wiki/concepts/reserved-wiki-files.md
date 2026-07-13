---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
description: "Reserved Markdown files that get special handling in OKF and OpenKB wiki validation."
---

# Reserved Wiki Files

Reserved wiki files are Markdown filenames that receive special handling in an OKF bundle and must not be treated like ordinary concept pages. In the embedded OKF baseline, `index.md` and `log.md` are reserved names at any directory level. The tooling policy adds a narrow exception: `tooling/index.md` is a committed navigation stub, but it is still a reserved navigation file rather than a normal content page.

## Core rule

- `index.md` is used for directory listing and progressive-disclosure navigation.
- `log.md` is used for chronological update history.
- `tooling/index.md` is the committed navigation stub for user-scoped tooling context, and it exists to anchor local tooling pages without turning them into project knowledge.
- Every other `.md` file is treated as a concept document and must include YAML frontmatter with a non-empty `type` field.

## Structural behavior

- A subdirectory `index.md` contains no frontmatter and acts as navigation.
- The bundle-root `index.md` may include an `okf_version: "0.1"` frontmatter block.
- `log.md` files are organized by date headings in `YYYY-MM-DD` format.
- Reserved filenames apply at any level of the hierarchy, not just at the root.
- The OpenKB validator treats `index.md` and `log.md` as reserved files even when it is scanning an OpenKB wiki tree, and it skips operational areas like `AGENTS.md`, `sources/`, and `reports/` in `--openkb-wiki` mode.
- The OpenKB validator also skips fenced code blocks and inline code when scanning for wikilinks, so documentation examples do not create false positives.

## Validation behavior

- Non-reserved Markdown files must be parseable and frontmatter-bearing.
- Concept pages must have parseable YAML frontmatter and a non-empty `type` field.
- `index.md` files are checked for a heading and for Markdown links that enumerate entries.
- `log.md` files are checked for date headings and for reserved-file structure instead of concept-page structure.
- The validator warns when it finds an unclosed code fence at end of file, because that often signals truncation or a bad merge.
- The validator warns when sibling page names collapse to the same normalized slug, because that suggests near-duplicate concepts.
- In OpenKB wiki mode, broken wikilinks are errors, and concept/entity pages missing a machine-managed non-empty `sources:` list are warned.
- The root `index.md` may carry `okf_version`, but any other reserved index file must not contain YAML frontmatter.

## Why this matters

Reserved names separate navigation and history from content pages. That distinction supports progressive disclosure, documentation architecture, and repo navigation while keeping concept pages focused and machine-validated.

This distinction also supports tooling-context governance: the tooling subtree is intentionally isolated from project truth, and its committed stub prevents dangling references while keeping local harness pages out of the main knowledge graph. That boundary aligns with [[concepts/progressive-disclosure]], [[concepts/tooling-context-isolation]], and [[concepts/local-tooling-boundaries]].

The OKF baseline also treats reserved-file handling as part of overall [[concepts/okf-validation]] and [[concepts/validation-vs-health-reporting]], since bundles should be checked for correct structure rather than only for content completeness. In practice, the validator combines structural errors with advisory warnings so reserved-file checks can participate in broader [[concepts/deterministic-validation]] and [[concepts/quality-gates]].

## Related validation rules

- OpenKB wiki validation still checks the reserved files, but applies special scope rules for items like `sources/`, `reports/`, and hand-authored `tooling/` pages.
- When `tooling/` contains non-reserved pages, the bundle-root `index.md` must include a clearly labeled harness-specific tooling entry that points to the committed stub rather than to local pages.
- The tooling validator strips inline code and fenced code blocks before scanning so examples do not falsely trigger the boundary check.
- Concept pages and subdirectory indexes must not link into `tooling/`, preserving the one-way boundary between project content and local runtime context.
- If `tooling/` contains non-reserved pages, the committed `tooling/index.md` stub must exist so the root index link resolves on clones that do not have local tooling pages.
- Tooling pages themselves may link outward to project pages, but they are still expected to carry tooling-specific metadata such as `scope: tooling` or `type: tooling-context` when they are not reserved pages.
- The validator's reserved-file handling is intentionally conservative: it errs on the side of structural fidelity, while still allowing bootstrap states where the root index is sparse or generated content is incomplete.

## Relationship to the source

This concept is defined by the offline OKF quality baseline in [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]], which documents the reserved-filename rules, OKF bundle structure, and validation expectations for OpenKB wikis. The tooling extension is defined by [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]], which narrows tooling storage to a committed stub plus local harness records and optional provider pages.

The OpenKB bundle validator in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] reinforces those rules by enforcing frontmatter requirements, checking reserved-file structure, warning on unclosed fences and slug collisions, and gating broken wikilinks in wiki mode. That makes reserved-file handling part of both [[concepts/tooling-link-policy]] and [[concepts/tooling-context-governance]].

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]