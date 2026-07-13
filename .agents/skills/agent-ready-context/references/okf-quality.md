# OKF quality and offline conformance baseline

This reference is the embedded offline baseline for OKF v0.1. It is intentionally sufficient for an agent to create, refresh, and validate a practical OKF bundle without network access.

When web access is available, refresh this baseline against the official Google OKF `SPEC.md` and `README.md` using `references/official-okf-spec-web-check.md`. The official spec wins if it has changed. When web access is unavailable, continue with this baseline and report that validation used the embedded OKF v0.1 rules.

## Core model

An OKF bundle is a directory tree of UTF-8 Markdown files. It is a knowledge bundle, not a binary artifact and not a required service runtime.

A bundle may be distributed as:

- a Git repository or subdirectory in a repository;
- a zip or tarball;
- another plain directory transport.

The repository source code remains the code source of truth. `okf/wiki/` is the durable knowledge/context source of truth for agents.

## Bundle structure

The spec allows arbitrary subdirectories. Producers organize concepts however makes sense for the knowledge being captured.

Typical local layout for an agent-ready repository:

```text
okf/wiki/
├── index.md
├── log.md
├── AGENTS.md
├── concepts/
├── summaries/
├── entities/
├── sources/
├── explorations/
├── reports/
└── tooling/
    └── harnesses/
```

`tooling/` is valid OKF because it is just a normal concept grouping. It must still obey the concept rules: files such as `tooling/harnesses/opencode.md` need YAML frontmatter and a non-empty `type`, while `tooling/index.md` and `tooling/log.md` remain reserved files. In this repository policy, `tooling/` is a hand-authored OpenKB wiki exception and must be declared in `okf/wiki/AGENTS.md`.

The local `tooling -> project allowed / project -> tooling forbidden` rule is not an OKF conformance rule. It is this repository's semantic separation policy for harness/tooling context.

## Reserved filenames

The following filenames are reserved at any level of the hierarchy and must not be used as concept documents:

- `index.md` — directory listing / progressive-disclosure navigation;
- `log.md` — chronological update history for that scope.

All other `.md` files are concept documents.

## Concept documents

Every non-reserved `.md` file is a concept document. It has:

1. a YAML frontmatter block at the start of the file, delimited by `---` lines;
2. a free-form Markdown body.

Required frontmatter:

```yaml
type: <short descriptive type name>
```

Recommended frontmatter:

```yaml
title: <human-readable display title>
description: <one-line summary>
resource: <canonical URI or repo path, when applicable>
tags: [<tag>, <tag>]
timestamp: <ISO 8601 datetime>
```

Extra frontmatter keys are allowed. Unknown `type` values are allowed and must be tolerated by consumers.

## Index files

An `index.md` may appear in any directory. It enumerates the directory's contents with Markdown headings and links.

Baseline rule:

- subdirectory `index.md` files contain no frontmatter;
- the bundle-root `index.md` may contain an `okf_version: "0.1"` frontmatter block when declaring the targeted OKF version;
- otherwise, index files are Markdown navigation bodies.

Example:

```markdown
# Concepts

* [Repository overview](concepts/repository-overview.md) - High-level project map.
```

## Log files

A `log.md` may appear at any level to record date-grouped updates. Date headings must use `YYYY-MM-DD`.

Example:

```markdown
# Directory Update Log

## 2026-07-03
* **Creation**: Initialized repository OKF bundle.
```

## Links and citations

Standard Markdown links between concepts express directed relationships. The relationship type is conveyed by surrounding prose, not by a separate OKF edge schema.

Consumers should tolerate broken cross-links. Broken links can represent partially generated or not-yet-written knowledge.

When concept bodies make claims from external material, include citations near the relevant claim or under a `# Citations` heading. Citation links may point to absolute URLs, bundle-relative paths, or concepts under `references/`.

## Hard conformance rules

A conformant OKF v0.1 bundle must satisfy:

1. Every non-reserved `.md` file has parseable YAML frontmatter.
2. Every concept frontmatter has a non-empty `type` field.
3. Reserved `index.md` and `log.md` files follow their reserved structures when present.

Consumers should not reject a bundle only because of:

- missing optional frontmatter fields;
- unknown `type` values;
- unknown additional frontmatter keys;
- broken cross-links;
- missing `index.md` files.

## OpenKB wiki mapping

OpenKB-generated concept pages carry fields such as `type`, `description`, and `sources`; summary pages carry `sources`, `brief`, `doc_type`, and `full_text`. OpenKB normally supplies the human-readable title as the body H1 rather than duplicating it in frontmatter. In `--openkb-wiki` mode, a non-empty body H1 satisfies the optional OKF `title` recommendation; a page with neither frontmatter `title` nor body H1 is still warned about. Missing `description` remains advisory.

When validating an OpenKB wiki, use `--openkb-wiki`. That mode skips root `AGENTS.md` because it is OpenKB's wiki-conventions manual, and skips `sources/` and `reports/` because they are operational/evidence areas. It still validates `index.md`, `log.md`, `concepts/`, `entities/`, `summaries/`, `explorations/`, and hand-authored `tooling/` pages. Report genuine spec deviations instead of silently passing them.

`--openkb-wiki` also applies OpenKB-convention checks on top of the spec: broken `[[wikilinks]]` are errors, and missing machine-managed `sources:` lists on `concepts/`/`entities/` pages are warnings. `explorations/` gets the same reality-over-ideal treatment as titles: OpenKB's own `query --save` writes only a `query:` frontmatter header with no `type` — a genuine deviation from hard rule 2 that the mode reports as a warning rather than silently passing or failing CI on native OpenKB output. Finding capture pages under `explorations/findings/` carry `type: Finding` (an unknown-but-tolerated type value) plus title/description/observed, so they conform fully; a page with neither `query:` nor `type:` is warned about. Without `--openkb-wiki`, strict conformance applies and a missing `type` stays an error everywhere. Finding pages must also be enumerated in the bundle-root `index.md` under `## Explorations` — same rationale as the tooling rule below: OKF navigation must enumerate the bundle. This does not contradict the spec's "tolerate broken cross-links" rule — that rule concerns standard Markdown links and consumer-side tolerance of partially written bundles. `[[wikilinks]]` are OpenKB's own convention, generated against a compile-time whitelist and repaired by `lint --fix`, so in an OpenKB-managed wiki a broken one always means damage (bad merge, hand edit, interrupted run); gating them is a producer-side quality bar, not an OKF conformance verdict. In all modes the validator additionally warns on unclosed code fences (truncation signal) and same-directory names that collapse to one slug (near-duplicates).

## Local validation command

```bash
uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki
```

Use `--strict-warnings` only for local quality gates, not for OKF conformance.

## Tooling link policy

For tooling context, preserve the local policy for **concept pages**:

```text
tooling -> project is allowed
project concept pages -> tooling is forbidden
```

The bundle-root `index.md` is the exception, because OKF navigation must enumerate the bundle. When `okf/wiki/tooling/` contains pages, the root `index.md` **must** list it in a clearly labeled harness-specific section so the bundle stays spec-navigable, for example:

```markdown
## Tooling context (harness-specific — do not treat as project truth)

* [Tooling](tooling/index.md) - User-scoped runtime/harness context, local by default. Project concept pages must not depend on it.
```

Tooling pages are **local by default** (user-scoped, gitignored except the committed `tooling/index.md` navigation stub — git scope rules in `subagent-profile-adapter`'s tooling context policy). The root entry points at the committed stub, never at individual local pages, so the committed bundle and any committed-plus-local overlay are each a valid, navigable OKF bundle: the spec allows arbitrary subdirectories and index files in any directory, and committed content never links to local pages, so wikilink integrity holds on every clone.

Because OpenKB defines an orphan as a page with neither incoming nor outgoing `[[wikilinks]]`, each local non-reserved tooling page must contain at least one valid outgoing wikilink to durable project knowledge. This preserves the local-by-default boundary while keeping structural lint clean; never solve it by enumerating ignored local pages in a committed index. Some OpenKB releases also include prior generated `wiki/reports/lint_*.md` files in orphan detection even though reports are operational and ignored. Treat only that exact report path as a tool-generated false positive; for a clean final report, preserve any needed evidence outside the wiki and remove stale ignored lint reports before the approved final lint run.

The root `index.md` and root `log.md` are reserved navigation/history files; linking or mentioning tooling there does not create a project-to-tooling dependency. Everywhere else the direction stays strict.

Validate it with:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .
```
