---
type: "Summary"
description: "Offline OKF quality rules and OpenKB validation guidance for agent-ready bundles."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__references__okf-quality-md.md"
---

# OKF Quality and Offline Conformance Baseline

This document defines the embedded offline baseline for OKF v0.1 and explains how agents should create, refresh, and validate an OKF bundle without network access. It treats the OKF wiki as a durable knowledge source, separate from repository source code, and provides repository-specific guidance for OpenKB-managed wikis.

## Core ideas

- An OKF bundle is a directory tree of UTF-8 Markdown files, not a binary artifact or service runtime.
- Bundles can be delivered as a Git repository, subdirectory, archive, or plain directory.
- The repository source code remains the source of truth for code, while `okf/wiki/` is the durable knowledge/context source of truth for agents.
- The baseline is intended to be practical enough for offline creation, refresh, and validation.

## Bundle structure

- The spec allows arbitrary subdirectories, so producers may organize concepts flexibly.
- A typical agent-ready layout includes `index.md`, `log.md`, `AGENTS.md`, and grouped areas such as `concepts/`, `summaries/`, `entities/`, `sources/`, `explorations/`, `reports/`, and `tooling/`.
- In this repository policy, `tooling/` is a hand-authored OpenKB wiki exception and must be declared in `okf/wiki/AGENTS.md`.
- The document distinguishes between OKF conformance and this repository's local semantic separation rule that allows tooling to reference project knowledge, while project concept pages must not depend on tooling.

## Reserved files and concept pages

- `index.md` and `log.md` are reserved filenames at any directory level and must not be used as concept documents.
- Every other `.md` file is treated as a concept document.
- Concept documents require YAML frontmatter with a non-empty `type` field.
- Recommended frontmatter includes `title`, `description`, `resource`, `tags`, and `timestamp`, but these are optional.
- Unknown `type` values and extra frontmatter keys are allowed and should be tolerated by consumers.

## Navigation and logs

- `index.md` files are navigation bodies; subdirectory indexes have no frontmatter.
- The bundle-root `index.md` may include `okf_version: "0.1"` when declaring the targeted spec version.
- `log.md` files record date-grouped updates using `YYYY-MM-DD` headings.
- Broken links are tolerated by OKF consumers, since partially generated bundles are expected.

## OpenKB wiki mapping

- OpenKB-generated concept pages use fields such as `type`, `description`, and `sources`.
- Summary pages use `sources`, `brief`, `doc_type`, and `full_text`.
- In `--openkb-wiki` mode, a body H1 can satisfy the optional `title` recommendation when frontmatter title is absent.
- Missing `description` is advisory, not a hard error.
- Validating an OpenKB wiki should skip root `AGENTS.md`, `sources/`, and `reports/`, but still validate the main wiki areas and hand-authored `tooling/` pages.

## Quality checks and warnings

- In `--openkb-wiki` mode, broken `wikilinks` are treated as errors.
- Missing machine-managed `sources:` lists on `concepts/` and `entities/` pages are warnings.
- `explorations/` pages are treated leniently because OpenKB query exports may omit `type`.
- `explorations/findings/` pages should use `type: Finding` and be listed in the root `index.md` under `## Explorations`.
- The validator also warns on unclosed code fences and same-directory names that collapse to the same slug.

## Tooling policy

- The local tooling policy is: `tooling -> project` is allowed, but `project concept pages -> tooling` is forbidden.
- The root `index.md` is an exception because bundle navigation must enumerate the bundle, including tooling context.
- Tooling pages are local by default, while the committed `tooling/index.md` serves as the shared navigation stub.
- Each local non-reserved tooling page must include at least one valid outgoing wikilink to durable project knowledge.
- The document provides a harness-specific index pattern that clearly labels tooling context as not being project truth.

## Validation commands

- OKF bundles can be checked with `uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki`.
- `--strict-warnings` is recommended only for local quality gates, not for OKF conformance.
- Tooling link policy can be validated with `uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .`.

## Key takeaway

This reference combines the core OKF v0.1 offline rules with OpenKB-specific validation behavior, especially around reserved files, frontmatter requirements, navigation coverage, wikilink integrity, and the special handling of tooling pages. It is the baseline for [[concepts/okf-offline-conformance]], [[concepts/openkb-wiki-validation-modes]], [[concepts/tooling-link-policy]], and [[concepts/okf-bundle-validation]].

## Related Concepts
- [[concepts/reserved-markdown-file-rules]]
- [[concepts/okf-validation-rules]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/spec-authority]]
- [[concepts/reserved-markdown-files]]
- [[concepts/wikilink-integrity]]
- [[concepts/local-by-default-tooling]]
- [[concepts/offline-first-workflows]]
- [[concepts/knowledge-layer-separation]]
- [[concepts/documentation-layer-separation]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-context-governance]]
- [[concepts/index-based-discovery]]

## Entities
- [[entities/okf-quality-md]]
- [[entities/references-official-okf-spec-web-check-md]]
- [[entities/okf-spec]]
- [[entities/okf]]
- [[entities/openkb-wiki]]
- [[entities/openkb-cli]]
- [[entities/validate_okf_bundle-py]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-tooling-index-md]]
- [[entities/okf-wiki-tooling]]
- [[entities/tooling]]
- [[entities/agents-md]]
- [[entities/google-cloud-platform]]
- [[entities/openkb]]
