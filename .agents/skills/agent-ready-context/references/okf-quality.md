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
├── quickstart.md
├── INSTRUCTIONS.md
├── <concern or module subdirectories>/
└── tooling/
    └── harnesses/
```

`tooling/` is valid OKF because it is just a normal concept grouping. It must still obey the concept rules: files such as `tooling/harnesses/opencode.md` need YAML frontmatter and a non-empty `type`, while `tooling/index.md` and `tooling/log.md` remain reserved files. In this repository policy, `tooling/` is the hand-authored user-scoped exception and must be declared in `okf/wiki/INSTRUCTIONS.md` so updates preserve it.

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

## OpenWiki producer mapping

OpenWiki output is validated as an ordinary strict OKF v0.1 bundle plus this repository's producer contract, enforced by `scripts/validate_openwiki_bundle.py` on top of the generic validator:

- the bundle-root `index.md` is the canonical front door and must route to an existing `quickstart.md`;
- generated directory indexes are normalized deterministically during candidate mapping: the root `index.md` keeps only the `okf_version` declaration in frontmatter, and subdirectory `index.md` files carry no frontmatter (producer-typed index frontmatter is removed, bodies preserved);
- `quickstart.md` and `INSTRUCTIONS.md` are non-reserved concept documents and therefore need valid frontmatter with a non-empty `type`;
- every generated knowledge page must carry citations in a machine-checkable form (frontmatter `sources` or `## Citations` bullets with backticked staged paths), and the staged runner rejects citations that were not present in the immutable pre-run stage;
- unknown `type` values and additional metadata are valid and must survive normalization and unrelated updates;
- timestamps change only when the body changes.

The accepted repository producer gate is deliberately stronger than the base spec on links: all internal links must resolve deterministically before promotion. This is a producer quality rule, not a claim that broken links violate OKF. Deterministic checks establish structure and grounding, not semantic correctness — review changed pages against source evidence before promotion (see `references/openwiki-lifecycle.md`).

## Local validation command

```bash
uv run .agents/skills/agent-ready-context/scripts/validate_openwiki_bundle.py --repo .
```

Validate the mapped staged candidate at `okf/.okf-build/<run-id>/candidate/wiki` before promotion and canonical `okf/wiki/` afterward.

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

Tooling pages are **local by default** (user-scoped, gitignored except the committed `tooling/index.md` navigation stub — git scope rules in `subagent-profile-adapter`'s tooling context policy). The root entry points at the committed stub, never at individual local pages, so the committed bundle and any committed-plus-local overlay are each a valid, navigable OKF bundle: the spec allows arbitrary subdirectories and index files in any directory, and committed content never links to local pages, so link integrity holds on every clone.

Each local non-reserved tooling page must contain at least one outgoing standard relative Markdown link to durable project knowledge. This preserves the local-by-default boundary while keeping the bundle connected; never solve it by enumerating ignored local pages in a committed index.

The root `index.md` and root `log.md` are reserved navigation/history files; linking or mentioning tooling there does not create a project-to-tooling dependency. Everywhere else the direction stays strict.

Validate it with:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .
```
