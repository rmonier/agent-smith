---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
description: "Offline rules for validating and using an OKF bundle without network access."
---

# OKF Offline Conformance

OKF offline conformance is the baseline for creating, refreshing, and validating an OKF bundle when web access is unavailable. It treats the bundle as a durable Markdown knowledge tree and defines the minimum rules an agent should follow to keep the bundle usable, navigable, and structurally valid without consulting the live spec.

## What it means

- An OKF bundle is a directory tree of UTF-8 Markdown files, not a binary package or runtime service.
- The bundle may live in a repository, subdirectory, archive, or plain directory transport.
- When offline, agents should continue using the embedded baseline and report that validation used the offline OKF v0.1 rules.
- When web access is available, the offline baseline should be refreshed against the official OKF spec, and the official spec takes precedence if it has changed.

## Core conformance rules

- Every non-reserved `.md` file must have parseable YAML frontmatter.
- Every concept page must include a non-empty `type` field.
- Reserved `index.md` and `log.md` files have special structures and are not concept documents.
- Unknown `type` values and extra frontmatter keys are allowed and should be tolerated.
- Broken cross-links are tolerated by the base OKF spec, because bundles may be partially generated.

## Bundle structure and reserved files

- Producers can organize subdirectories however they want.
- A typical agent-ready layout includes `index.md`, `log.md`, `AGENTS.md`, and topic areas like `concepts/`, `summaries/`, `entities/`, `sources/`, `explorations/`, `reports/`, and `tooling/`.
- `index.md` files are navigation bodies, and subdirectory indexes should not have frontmatter.
- `log.md` files record date-grouped updates using `YYYY-MM-DD` headings.
- `index.md` and `log.md` are reserved at every directory level and must not be repurposed as concept documents.

## OpenKB-specific validation behavior

- In `--openkb-wiki` mode, a body H1 can satisfy the optional `title` recommendation when frontmatter title is missing.
- Missing `description` is advisory rather than a hard failure.
- OpenKB validation skips root `AGENTS.md`, `sources/`, and `reports/`, but still validates the main wiki areas and hand-authored tooling pages.
- Broken `wikilinks` are treated as errors in OpenKB-managed wikis.
- Missing machine-managed `sources:` lists on `concepts/` and `entities/` pages are warnings.
- `explorations/` pages are treated leniently because exported query pages may omit `type`.
- `explorations/findings/` pages should use `type: Finding` and must be listed in the bundle-root index under `## Explorations`.

## Tooling boundary

- The repository policy allows `tooling -> project` references but forbids `project concept pages -> tooling` references.
- The bundle-root `index.md` is the exception because navigation must enumerate the bundle.
- Tooling pages are local by default, and the committed `tooling/index.md` acts as a shared navigation stub.
- Each local non-reserved tooling page must include at least one outgoing wikilink to durable project knowledge.
- This is a repository policy layered on top of OKF conformance, not a core OKF rule.

## Validation workflow

- The baseline recommends `uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki` for bundle validation.
- `--strict-warnings` is meant for local quality gates, not for spec conformance.
- A separate tooling policy validator checks the local tooling-link constraints.
- The overall approach combines spec compliance, OpenKB conventions, and repository-specific guardrails.

## Why it matters

Offline conformance makes OKF bundles reliable in air-gapped or network-limited environments. It preserves enough structure for agents to navigate knowledge, validate content, and keep the bundle consistent even when the live spec or external resources are unavailable. It also reinforces [[concepts/okf-offline-conformance]], [[concepts/deterministic-validation]], [[concepts/reserved-markdown-file-rules]], [[concepts/frontmatter-metadata]], [[concepts/wikilink-integrity]], and [[concepts/tooling-link-policy]].

## Source

Derived from [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]].

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]