---
type: "Concept"
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
description: "Validation rules for OKF bundles and OpenKB wiki quality gates."
---

# OKF Validation

OKF validation is the set of checks used to confirm that an OKF bundle is structurally sound, navigable, and fit for offline agent use. It covers both the core OKF conformance model and the stronger OpenKB wiki checks that support practical knowledge-base maintenance, including the lifecycle rules that govern ingestion, retraction, registry coherence, and deterministic refresh order.

## What gets validated

- The bundle is a directory tree of UTF-8 Markdown files.
- Non-reserved Markdown files must have parseable YAML frontmatter.
- Every concept document must define a non-empty `type`.
- Reserved files like `index.md` and `log.md` must follow their special roles.
- In OpenKB wiki mode, the validator also checks wiki-specific conventions such as broken `wikilinks`, unclosed code fences, near-duplicate slugs, and machine-managed metadata.
- Repository-specific policy checks can also verify tooling-context boundaries, local exceptions for `tooling/` pages, and the KB-root self-reference rule.
- In an OpenKB KB, validation also helps guard the lifecycle contract between staged sources, compiled wiki pages, and the hash registry.

## Core OKF rules

The baseline OKF rules treat the bundle as a knowledge artifact rather than a runtime artifact. A conformant bundle must satisfy:

- every non-reserved `.md` file has valid frontmatter;
- every concept frontmatter includes a non-empty `type`;
- reserved files keep their special structures;
- the root `index.md` may optionally declare `okf_version` in frontmatter;
- consumers tolerate missing optional fields, unknown `type` values, and broken standard Markdown links.

The validator is intentionally OS-agnostic and uses `pathlib`-based traversal rather than shell commands. If PyYAML is unavailable, YAML checks degrade gracefully instead of crashing, but that also means frontmatter validation is incomplete.

## OpenKB wiki validation

When validating an OpenKB wiki, the rules become more opinionated:

- root `AGENTS.md` is skipped because it is a conventions manual;
- `sources/` and `reports/` are skipped because they are operational areas;
- broken `wikilinks` are errors;
- missing machine-managed `sources:` lists on `concepts/` and `entities/` pages are warnings;
- unclosed code fences are warned because they often indicate truncation or a bad merge;
- sibling pages whose names collapse to the same normalized slug are warned because they likely represent near-duplicates.

This reflects the idea that wikilink integrity, frontmatter metadata, and generated content governance matter more in a curated wiki than in a generic Markdown bundle.

The link checker mirrors OpenKB's local resolution behavior: it compares against wiki-relative paths without extensions and bare stems, strips `|alias` suffixes, and ignores fenced or inline code so that code examples do not trigger false positives.

OpenKB lifecycle rules make the validator more than a structural checker. It sits alongside `openkb lint`, `openkb remove`, `openkb recompile`, and the staged-source workflow to catch issues such as registry drift, missing citation chains, stale pages after source moves, and order-dependent staleness that can arise when a page compiles before later concepts exist in the wiki.

## Validation modes

OKF validation distinguishes between conformance and quality gates:

- `--openkb-wiki` enables the OpenKB-specific rules on top of the base spec.
- `--strict-warnings` promotes warnings to errors for local quality gates.
- Missing titles or descriptions are warned because OpenKB often stores them in the body heading instead of frontmatter.
- `explorations/` is allowed some flexibility because saved queries may not fully match the ideal concept-page schema.
- The workflow is designed for deterministic auditing, so validation stays reproducible across runs and environments.
- In OpenKB maintenance, validation is part of a broader read-first and disclose-first process: inspect the KB state, then validate staged content rather than relying on wiki pages as instructions.

This separation aligns with [[concepts/deterministic-validation]], [[concepts/quality-gates]], [[concepts/executable-validation]], and [[concepts/graceful-degradation]].

## Tooling and policy checks

OKF validation also supports repository policy around tooling context and repository hygiene:

- `tooling/` is treated as a local OpenKB exception that must be declared in `okf/wiki/AGENTS.md`.
- A separate validator checks the local rule that `tooling -> project` links are allowed while `project -> tooling` links are forbidden.
- Validation is part of a larger workflow that also checks prerequisites, enforces vendored toolchain skills, and keeps the KB root out of the graph.
- The same workflow assumes deterministic staged inputs under `okf/.okf-build/input/` rather than hand-edited generated pages.
- It also treats the OpenKB hash registry as sensitive state whose drift can cause silent dedupe issues if source content changes underneath it.
- Health reporting and pass/fail validation are distinct: `openkb lint` is a report, while structural validators are the gate.
- The workflow starts by reading root `AGENTS.md`, then `okf/wiki/index.md` when present, then any routed tooling context before later wiki reads.
- The build sequence also requires prerequisite checks, optional Graphify updates, source-pack staging, OpenKB initialization, ingestion, linting, and bundle validation in that order.
- If required toolchain skills are not vendored, the workflow stops rather than proceeding with a mismatched installed CLI.
- The KB root must stay out of the repo graph so the wiki does not become its own source.

These checks connect validation to [[concepts/tooling-context-pages]], [[concepts/tooling-navigation-exceptions]], [[concepts/tooling-context-isolation]], [[concepts/reserved-wiki-files]], [[concepts/preflight-checks]], [[concepts/skill-vendoring]], [[concepts/self-reference-control]], [[concepts/hash-registry-coherence]], and [[concepts/source-pack-staging]].

## Related ideas

- [[concepts/deterministic-validation]] for repeatable, predictable validation behavior.
- [[concepts/filesystem-validation]] for checking structure directly from the on-disk bundle.
- [[concepts/path-based-validation]] for scope-limited validation of specific locations.
- [[concepts/executable-validation]] for validation performed by runnable scripts rather than manual review.
- [[concepts/offline-first-workflows]] for running checks without network access.
- [[concepts/spec-authority]] for preferring the official spec when it changes.
- [[concepts/openkb-wikilink-resolution]] for the wiki's target-matching rules.
- [[concepts/okf-bundle-validation]] for bundle-level conformance checks.
- [[concepts/okf-wiki-governance]] for the broader rules that govern wiki maintenance.
- [[concepts/registry-drift]] for the failure mode where registry state and wiki pages diverge.
- [[concepts/orphan-retraction]] for deterministic cleanup when repository sources are removed or moved.
- [[concepts/source-driven-regeneration]] for the rule that wiki output should be corrected by fixing sources and recompiling.
- [[concepts/source-pack-staging]] for the deterministic build input that validation checks after staging.
- [[concepts/deterministic-builds]] for the ordered, reproducible workflow that keeps validation meaningful.
- [[concepts/data-flow-disclosure]] for explaining the KB path before the first LLM-backed command.

## Practical takeaway

OKF validation is both a spec conformance mechanism and a wiki-quality system. The baseline rules keep bundles portable and parseable, while OpenKB mode adds stronger checks for link integrity, metadata completeness, repository-specific tooling boundaries, deterministic build sequencing, and the staged workflow that feeds the wiki. In the OpenKB lifecycle, it is one of the main safeguards against stale registry state, missing provenance, broken knowledge-base navigation, and self-referential graph contamination.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/okf-spec]]