---
type: "Concept"
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "How OpenKB resolves wikilinks into valid page targets and flags broken links."
---

# OpenKB Wikilink Resolution

OpenKB wikilink resolution is the rule set that turns `wikilinks` into valid page targets inside the wiki. In the validation script for `.agents/skills/agent-ready-context/scripts/validate_okf_bundle.py`, this logic is used in OpenKB wiki mode to detect broken links as structural errors and to keep the graph coherent during local validation.

## What counts as a target

The validator builds a set of valid targets from every Markdown page in the wiki. Each page contributes two forms:

- its wiki-relative path without the `.md` extension
- its bare stem

That means a page like `concepts/example-topic.md` can be linked either by its full relative path form or by its bare filename stem, as long as the target matches one of those normalized keys.

## Link parsing rules

The script applies a few normalization steps before checking a wikilink:

- `|alias` text is stripped off before resolution
- leading and trailing `/` characters are removed
- fenced code blocks and inline code are ignored during link scanning to reduce false positives

This makes link checking more tolerant of documentation formatting while still catching genuine broken links.

## OpenKB wiki mode behavior

When `--openkb-wiki` is enabled, wikilink resolution becomes part of validation rather than a soft check:

- broken wikilinks are reported as errors
- `AGENTS.md`, `SCHEMA.md`, and `log.md` are excluded from link scanning
- `sources/` and `reports/` are skipped as operational areas, but still contribute link targets
- concepts and entities missing a non-empty `sources:` frontmatter list are warned, since that usually signals a damaged citation chain or hand edit

The validator also watches for nearby health signals while it resolves links:

- unclosed code fences are warned as possible truncation or bad merges
- sibling pages whose names collapse to the same normalized slug are warned as likely near-duplicates
- root `index.md` may carry `okf_version` in frontmatter, while other reserved `index.md` files must not

This keeps the wiki graph coherent while respecting repository areas that are not meant to behave like normal concept pages.

## Why it matters

Wikilink resolution supports [[concepts/wikilink-integrity]], [[concepts/knowledge-linking-and-citations]], and [[concepts/graph-integrity-diagnostics]] by ensuring references point to real pages. In a compiled wiki, broken links usually indicate drift, incomplete ingestion, or damaged generated content.

The same validator also checks related structural signals such as [[concepts/reserved-wiki-files]], [[concepts/frontmatter-metadata]], and [[concepts/generated-content-governance]], so link resolution is one part of a broader content health model.

## Related source

- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/okf-spec]]