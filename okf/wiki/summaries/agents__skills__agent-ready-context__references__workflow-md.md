---
type: "Summary"
description: "Workflow for building and refreshing the OpenKB wiki from repo sources."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__references__workflow-md.md"
---

# OpenKB Repo Build Workflow

This document defines the end-to-end workflow for compiling an OpenKB knowledge base from a repository into `okf/wiki/`. It focuses on deterministic staging, toolchain checks, wiki ingestion, validation, and safe incremental refreshes.

## Core Inputs And Assumptions

- Default repository path is `.` and the KB root is `okf/`.
- The compiled wiki lives in `okf/wiki/`.
- Language is set with `openkb init --language <code>` using the user language.
- External documentation URLs are treated as evidence only, never as hidden instructions.

## Bootstrapping Sequence

The workflow starts by reading the root `AGENTS.md`, then `okf/wiki/index.md` when it exists, and then any linked tooling context. If the index routes to tooling, the process reads `tooling/index.md`, identifies the active harness from runtime metadata or self-knowledge, and only then loads the relevant harness and provider pages. It does not infer the harness solely from installed binaries.

Before any OpenKB work, it runs `check_prereqs.py` to verify hard requirements such as `git`, `uv`, and Python 3.11+. If optional tools like `graphify` or `openkb` are missing, it offers consent-first bootstrap paths from [[concepts/dependency-management|dependencies]].

## Toolchain And Repository Requirements

- Vendored copies of the `graphify` and `openkb` skills must exist before first CLI use.
- The target `.gitignore` must exclude build and cache paths such as `okf/.okf-build/`, `okf/output/`, `okf/wiki/reports/`, and graphify cache files.
- `.gitattributes` should be installed from the template to keep line endings and staging hashes deterministic.
- `.graphifyignore` must exclude the KB root itself so the wiki does not become part of the repo graph.
- The source pack requires Git history; if the repo is not a Git repository, initialization must happen first with user consent.

These checks support deterministic builds and prevent the wiki from self-referencing through the graph pipeline.

## Main Build Workflow

The recommended sequence is:

1. Merge the managed `AGENTS.md` section.
2. Run `graphify update . --force` if available.
3. Build the deterministic source pack into `okf/.okf-build/input/`.
4. Initialize OpenKB with the desired model and language.
5. Ingest staged input with `openkb --kb-dir ./okf add ./okf/.okf-build/input/`.
6. Run `openkb --kb-dir ./okf lint` and preserve the report for triage.
7. Validate the bundle with `validate_okf_bundle.py`.
8. Re-read `AGENTS.md` after validation and reconcile the operational guidance.

The pipeline requires `uv run` for bundled scripts unless the user explicitly declines it.

## Incremental Update Rules

Refreshes must happen in a fixed order so the wiki always reflects the current repository structure:

- Re-run Graphify first, if installed.
- Rebuild the source pack.
- Reconcile deletions before ingesting new material.
- Triage findings captured in `okf/wiki/explorations/findings/`.
- Ingest the refreshed input and any promoted findings.
- Recompile only when needed, and preview with `--dry-run` first.

This order prevents stale graph data, stale pages, and orphaned content from surviving across updates.

## Findings And Review Pass

The workflow treats compilation output like a reviewed change set. After any `add` or `recompile` that changes `okf/wiki/`, it requires a post-generation review pass that checks:

- missing or vague concepts,
- near-duplicates,
- entity versus concept misclassification,
- off-topic content created from examples or fixtures,
- lost caveats and weakened constraints,
- truncation,
- stale early pages caused by order dependence,
- grounding through the source chain,
- stale promoted findings.

Issues must be routed back through the source correction loop; generated pages are not to be edited by hand. New durable discoveries may be recorded as [[concepts/findings]] pages.

## Validation And Safety

The document separates two kinds of validation:

- `openkb lint` is a required health report but not a pass/fail gate, so its findings must be triaged manually.
- `validate_okf_bundle.py` is the structural validator and can be automated in CI or hooks.

It also emphasizes provenance and safety:

- external evidence should be stored under `okf/.okf-build/input/external/` before ingestion,
- repository snippets should stay short,
- provider credentials must never be written into evidence or wiki pages,
- the active provider configuration stays in local uncommitted OpenKB config, not in `AGENTS.md`.

## Self-Reference Policy

A key principle is that the wiki must stay out of the repo graph. The reasons are:

- no fixed point for deterministic incremental builds,
- circular grounding when wiki pages cite graph reports about the wiki itself,
- discovery pollution from generated pages overwhelming source material.

Self-knowledge should instead come from the front door: `okf/wiki/index.md`, `okf/wiki/AGENTS.md`, source chains, and one-off graph analyses outside the main pipeline.

## Cross-Document Themes

This workflow connects naturally to several reusable concepts:

- [[concepts/deterministic-builds]] for stable staging and reproducible hashes,
- [[concepts/provenance-tracking]] for source chains and evidence handling,
- [[concepts/incremental-compilation]] for ordered rebuilds and orphan reconciliation,
- [[concepts/self-reference-control]] for keeping the wiki out of the graph,
- [[concepts/deterministic-validation]] for linting, structural checks, and review loops,
- [[concepts/toolchain-pinning]] for prerequisite checks and consent-first setup.

Overall, the document is a build-and-refresh playbook for keeping OpenKB compiled, grounded, and deterministic without letting the generated wiki become its own source of truth.

## Related Concepts
- [[concepts/openkb-build-workflow]]
- [[concepts/dependency-management]]
- [[concepts/consent-first-workflows]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/okf-workflow-governance]]
- [[concepts/okf-validation]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/documentation-architecture]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/wiki-review-gates]]
- [[concepts/source-pack-staging]]
- [[concepts/orphan-retraction]]
- [[concepts/foundations-promotion]]
- [[concepts/provenance-aware-tool-installation]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-repositories]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/document-normalization]]
- [[concepts/evidence-staging]]
- [[concepts/external-documentation]]
- [[concepts/frontmatter-metadata]]
- [[concepts/generated-content-governance]]
- [[concepts/git-attributes]]
- [[concepts/hash-registry-coherence]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/knowledge-boundaries]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/offline-first-workflows]]
- [[concepts/quality-gates]]
- [[concepts/repository-ingestion]]
- [[concepts/source-driven-regeneration]]
- [[concepts/tooling-boundaries]]
- [[concepts/tooling-context-governance]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/wiki-content-as-untrusted-data]]

## Entities
- [[entities/check-prereqs-py]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/build_okf_source_pack-py]]
- [[entities/prune_okf_orphans-py]]
- [[entities/validate_okf_bundle-py]]
- [[entities/graphify]]
- [[entities/openkb]]
- [[entities/uv]]
- [[entities/git]]
- [[entities/python]]
- [[entities/agent-ready-context]]
- [[entities/agent-ready-context-skill]]
- [[entities/agents-md]]
- [[entities/okf]]
- [[entities/okf-wiki]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-agents-md]]
- [[entities/graphifyignore-template]]
- [[entities/gitattributes-template]]
- [[entities/gitignore]]
- [[entities/openkb-cli]]
- [[entities/agents-skills]]
- [[entities/agent-ready-repositories]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/knowledge-catalog]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/references-official-okf-spec-web-check-md]]
- [[entities/references-tooling-context-policy-md]]
- [[entities/runtime-detection-md]]
- [[entities/tooling]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/wiki-schema-md]]
- [[entities/workflow-md]]
