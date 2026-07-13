---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "Rules for validating OKF structure, metadata, links, and tooling boundaries."
---

# OKF Validation Rules

OKF validation rules define how an OKF bundle or wiki tree is checked for structural correctness, metadata completeness, link integrity, and boundary discipline before it is accepted as valid. They combine the hard conformance rules of [[concepts/okf-validation]] with practical health checks used by OpenKB and related tooling, including offline baseline rules in `okf-quality-md` and the repository-specific separation of local tooling context from compiled project knowledge.

## Core Rules

- Every non-reserved Markdown file is treated as a content page subject to validation.
- Every content page must contain parseable YAML frontmatter.
- Every content page must declare a non-empty `type` field.
- Reserved navigation files such as `index.md` and `log.md` follow separate structural rules.
- The bundle-root `index.md` may include an `okf_version` frontmatter field when declaring the targeted OKF version.
- Unknown `type` values and extra frontmatter keys are tolerated rather than treated as fatal errors.

These rules reflect the baseline OKF model described in [[concepts/okf-offline-conformance]] and the broader validation framing in [[concepts/deterministic-validation]] and [[concepts/quality-gates]].

## Structural Checks

The validation workflow also looks for evidence of malformed or incomplete content:

- Unclosed code fences at end of file are reported as warnings because they often indicate truncation or a bad merge.
- Sibling pages whose names normalize to the same slug are flagged as likely near-duplicates.
- Invalid UTF-8 content is rejected.
- Missing Markdown files cause the bundle to fail validation.
- Broken cross-links may be tolerated by the base OKF model, but OpenKB-managed validation treats broken `wikilinks` as errors.

These checks support [[concepts/deterministic-validation]] and [[concepts/quality-gates]] by making the output predictable and auditable.

## OpenKB Wiki Mode

When run in `--openkb-wiki` mode, the validator applies additional wiki-specific rules:

- Root `AGENTS.md`, plus `sources/` and `reports/`, are skipped as operational areas rather than content pages.
- Concept and entity pages are warned if they do not contain the machine-managed `sources:` frontmatter list.
- Pages in `explorations/` receive lenient treatment because OpenKB query exports may omit `type`.
- Finding pages under `explorations/findings/` should use `type: Finding` and must be enumerated in the bundle-root `index.md` under `## Explorations`.
- Pages with neither `query:` nor `type:` are warned about, since they are likely incomplete or malformed.

This mode reflects [[concepts/openkb-wiki-health-checks]], [[concepts/openkb-wikilink-resolution]], and [[concepts/generated-content-governance]], while also honoring the OpenKB reality-over-ideal treatment of generated exploration pages.

## Frontmatter Handling

Frontmatter validation is central to the script's behavior:

- YAML is parsed with PyYAML when available.
- If PyYAML is missing, YAML validation degrades instead of silently pretending success.
- The validator distinguishes between required fields, recommended fields, and advisory metadata.
- Root `index.md` frontmatter is restricted to `okf_version`, with extra keys warned about.
- Body H1 headings can satisfy the optional `title` recommendation in OpenKB wiki mode when frontmatter `title` is absent.
- Tooling pages remain part of the OpenKB wiki exception and must still be declared in `okf/wiki/AGENTS.md` under the repository policy.

This aligns with [[concepts/frontmatter-metadata]], [[concepts/graceful-degradation]], and [[concepts/spec-authority]].

## Link and Naming Integrity

The validator treats links and file names as part of the knowledge graph's integrity:

- Wikilink targets are resolved against all Markdown pages in the tree.
- Code blocks and inline code are stripped before scanning links to avoid false positives.
- Normalized slug collisions are reported to help prevent confusing page duplication.
- Broken `wikilinks` are producer-side quality failures in OpenKB-managed wikis, even though base OKF tolerates broken standard Markdown links.

These behaviors connect to [[concepts/wikilink-integrity]], [[concepts/naming-normalization]], and [[concepts/graph-integrity-diagnostics]].

## Tooling Link Policy

A specialized validation rule set governs the relationship between compiled wiki content and local tooling context:

- Pages under `okf/wiki/tooling/` may link outward to project pages.
- Project concept pages and subdirectory indexes must not link back into `okf/wiki/tooling/`.
- The bundle-root `index.md` and `log.md` are exempt from that reverse-link restriction because they serve navigation and history roles.
- If `okf/wiki/tooling/` contains non-reserved pages, the root `index.md` must reference tooling in a clearly labeled harness-specific section.
- If `okf/wiki/tooling/` contains non-reserved pages, the committed `okf/wiki/tooling/index.md` stub must exist so the root-index link resolves on clones without local tooling pages.
- Each local non-reserved tooling page must include at least one valid outgoing wikilink to durable project knowledge.
- Tooling pages are treated as local-by-default context, so the committed stub exists specifically to make the root index link portable across clones that do not have user-scoped local tooling pages.

This rule set reinforces [[concepts/tooling-link-policy]], [[concepts/link-directionality]], [[concepts/local-by-default-tooling]], [[concepts/tooling-context-governance]], and [[concepts/reserved-navigation-files]]. It also reflects the separation between [[concepts/harness-vs-local-tools]] and compiled project knowledge.

## Why It Matters

OKF validation rules provide a local safety net for repository ingestion and wiki maintenance. They help catch schema drift, broken references, malformed content, generation damage, and incomplete offline baselines early, while also preventing accidental dependencies on local tooling context. That improves [[concepts/documentation-cohesion]], [[concepts/repository-ingestion]], [[concepts/source-grounded-regeneration]], and [[concepts/knowledge-boundaries]].

## Related Source

- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]