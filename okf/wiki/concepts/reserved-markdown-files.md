---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "Markdown files with fixed navigation, log, and validation roles in OKF/OpenKB."
---

# Reserved Markdown Files

Reserved Markdown files are Markdown pages that do not behave like ordinary concept documents. In the OKF/OpenKB bundle model, these files have fixed roles, special structural rules, and validation exceptions that distinguish them from regular content pages.

## What counts as reserved

The validator described in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] treats `index.md` and `log.md` as reserved files. They are excluded from the normal concept-document rules and are checked with file-specific logic instead.

The OKF offline baseline also treats these names as reserved at any level of the hierarchy, not just at the bundle root. They are never concept documents, while every other `.md` file is a concept document that must carry YAML frontmatter with a non-empty `type` field.

## Reserved file roles

- `index.md` serves as the directory catalog and progressive-disclosure navigation file.
- `log.md` serves as the chronological operation log for its scope.
- At the bundle root, `index.md` is the main navigation surface and may declare `okf_version: "0.1"` in frontmatter.
- In OpenKB wiki mode, the root `index.md` may also reflect repository organization, including the distinction between compiled wiki content and operational areas such as tooling and reports.
- Both files are structural metadata pages rather than ordinary knowledge pages.

## Structural rules

The source validator enforces these distinctions:

- Bundle-root `index.md` may contain YAML frontmatter, but only for declaring the targeted OKF version.
- Non-root `index.md` files must not contain YAML frontmatter.
- `log.md` files are Markdown history files and should follow date-grouped headings, using `YYYY-MM-DD` headings in the baseline OKF format.
- In OpenKB wiki mode, `log.md` follows the OpenKB log conventions while remaining a reserved navigation/history file.
- Both files should still contain visible Markdown structure, such as headings and links, so they remain readable and useful.

The validator also applies soft checks to reserved files rather than hard failures when the content is merely incomplete: `index.md` should contain at least one heading and should enumerate entries with Markdown links, while `log.md` should contain a visible Markdown heading.

## Why they are treated differently

Reserved Markdown files are part of the wiki's control plane, not its concept graph. They support documentation architecture, index-based discovery, and validation vs health reporting by providing navigation, chronology, and machine-checkable structure.

The validator also uses these reserved files as exceptions when checking for:

- missing YAML frontmatter on concept pages,
- broken structure in generated content,
- near-duplicate slugs among ordinary pages.

In OpenKB, reserved-file handling is part of broader repository hygiene. The wiki validator skips operational areas like `sources/` and `reports/` in wiki mode, but still expects reserved files to keep their special semantics. This reinforces generated content governance and knowledge base discovery while keeping the core content graph clean.

## OpenKB-specific context

The OKF baseline distinguishes strict spec conformance from OpenKB wiki validation mode. In `--openkb-wiki` mode, reserved files remain reserved, but the validator also applies OpenKB-specific checks: broken `wikilinks` are errors, missing machine-managed `sources:` lists on concept and entity pages are warnings, and exploration pages are handled with repository-aware flexibility.

This means reserved Markdown files sit at the boundary between spec-level structure and OpenKB's practical wiki rules. They support navigation, logging, and validation without becoming part of the substantive knowledge graph.

## Related ideas

- frontmatter metadata
- documentation architecture
- index based discovery
- generated content governance
- validation vs health reporting
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]