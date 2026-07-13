---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md"]
description: "Rules for one-way wiki links that keep tooling isolated from project knowledge."
---

# Link Directionality

Link directionality is the rule that wiki links should flow in a controlled way across layers of the knowledge base, rather than forming arbitrary back-links. In OpenKB, it keeps local tooling context isolated while still leaving the bundle navigable, and it also reflects the separation between durable wiki knowledge, repository orientation, and runtime-specific adapter files described by the subagent profile adapter skill.

## Core idea

The source script `validate_tooling_link_policy.py` enforces a one-way boundary:

- pages under `okf/wiki/tooling/` may link outward to project pages;
- project concept pages and subdirectory indexes must not link back to tooling;
- the bundle-root `index.md` and `log.md` are exempt because they are navigation/history files;
- when tooling has non-reserved pages, the root `index.md` must mention `tooling/` in a clearly labeled harness-specific section;
- when tooling has pages, a committed `tooling/index.md` stub must exist so the root reference resolves on clones that lack local tooling pages.

This makes link direction part of the wiki's [[concepts/tooling-context-isolation]] and [[concepts/tooling-link-policy]] governance model, while preserving the broader layering between [[concepts/agent-orientation-index]], [[concepts/agent-ready-context]], and runtime adapters.

## Why it matters

Directional linking prevents local-only artifacts from becoming hidden dependencies in the shared wiki graph. That supports:

- [[concepts/local-by-default-tooling]]
- [[concepts/knowledge-boundaries]]
- [[concepts/repo-scoped-graph-partitioning]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/runtime-adapter-management]]
- [[concepts/knowledge-layer-separation]]

It also helps preserve navigability without turning navigation files into ordinary dependency edges, which is important when runtime-specific adapters are derived from repository context but are not themselves a source of truth.

## How the validator applies it

The script walks Markdown files under `okf/wiki`, classifies tooling paths, and scans for links using both Markdown link syntax and path-like mentions. It strips code blocks and inline code before scanning so examples do not cause false positives.

It also performs a small amount of frontmatter inspection:

- tooling pages should declare `scope: tooling` or `type: tooling-context`;
- missing outgoing wiki links in local tooling pages are treated as structural errors because they can be orphaned by OpenKB linting.

The same policy is reinforced by the subagent-profile-adapter workflow, which treats harness docs as local tooling context, keeps generated adapter files short, and requires explicit validation before runtime-specific files are accepted.

## Practical effect

Link directionality turns wiki structure into an enforceable policy rather than a convention. The result is a cleaner separation between shared project knowledge and local harness context, with explicit exceptions for the pages whose job is navigation.

## Related source

- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
