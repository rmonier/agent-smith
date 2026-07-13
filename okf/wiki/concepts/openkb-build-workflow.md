---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Governed pipeline for compiling deterministic OpenKB wiki builds."
---

# OpenKB Build Workflow

[[summaries/agents__skills__agent-ready-context__references__workflow-md]] defines the end-to-end process for turning a repository into a compiled OpenKB knowledge base under `okf/wiki/`. The workflow is built around deterministic builds, explicit prerequisites, consent-first tooling, and a strict separation between source material, staged input, generated wiki output, and operational orientation.

## What The Workflow Does

The build workflow orchestrates the repository-to-wiki pipeline:

- verifies runtime and repository prerequisites before any KB work begins,
- reads repository and wiki orientation files in a prescribed order,
- stages source material into a deterministic input pack,
- initializes and ingests the OpenKB wiki,
- runs linting and structural validation,
- preserves reports and triages findings,
- supports incremental refreshes without breaking provenance or determinism,
- keeps the durable context source of truth in `okf/wiki/` rather than in `AGENTS.md`,
- treats repository skills as action surfaces and the compiled wiki as context.

This makes it a practical example of [[concepts/deterministic-builds]], [[concepts/provenance-tracking]], [[concepts/source-bundling]], and [[concepts/agent-context-layering]].

## Core Workflow Principles

### Deterministic staging
The pipeline builds `okf/.okf-build/input/` as a repeatable source pack rather than modifying the wiki directly. Unchanged files should produce byte-identical staged outputs, which supports [[concepts/hash-registry-coherence]] and [[concepts/incremental-compilation]]. The workflow also warns against writing generated files directly into `okf/raw/` or `okf/wiki/`, because staged input is the approved regeneration boundary.

### Explicit toolchain checks
Before any OpenKB actions, the workflow runs prerequisite checks for required tools such as `git`, `uv`, and Python 3.11+. Missing core tools stop the process; optional tools can be bootstrapped only with user consent. This reflects [[concepts/preflight-checks]], [[concepts/consent-first-installation]], and [[concepts/consent-first-tooling]].

### Vendored skill requirements
If `graphify` or `openkb` will be used, pinned vendored copies of their skills must already exist locally before first CLI use. The document treats skill vendoring as part of safe and reproducible tool adoption, linking to [[concepts/skill-vendoring]], [[concepts/vendor-skills]], and [[concepts/vendor-skill-adoption]].

### Repository hygiene
The workflow requires ignore rules and line-ending normalization so that staging hashes remain stable. It also expects `.graphifyignore` to exclude the KB root, preventing the wiki from entering its own graph. These rules connect to [[concepts/local-vs-shared-ignore]], [[concepts/git-attributes]], [[concepts/self-reference-control]], and [[concepts/self-referential-ingestion-loops]].

### Context separation
The skill reinforces a three-way split: skills are repeatable actions, the OKF wiki is durable context, and `AGENTS.md` is a concise orientation layer. That separation is central to [[concepts/context-action-separation]], [[concepts/documentation-layer-separation]], and [[concepts/documentation-architecture]].

## Ordered Build Phases

1. Read root `AGENTS.md`, then `okf/wiki/index.md` when available, and follow the index to any required tooling context.
2. Run prerequisite checks and stop for missing hard requirements.
3. Vendor required skills before first CLI use when needed.
4. Ensure ignore and normalization files are in place.
5. Require Git history for source-pack creation.
6. Optionally refresh Graphify, then build the deterministic source pack.
7. Materialize any external URLs as evidence before ingestion.
8. Initialize OpenKB with the chosen model and language.
9. Ingest staged input into the KB.
10. Run `openkb lint`, preserve the report, and triage all findings.
11. Validate the compiled bundle.
12. Re-read `AGENTS.md` and reconcile any operational guidance.

This ordering is central to [[concepts/source-driven-regeneration]] and [[concepts/knowledge-lifecycle-governance]]. It also depends on [[concepts/orientation-routing]] and [[concepts/index-based-discovery]] because the workflow uses the wiki index as the navigation front door when it exists.

## Incremental Refresh Rules

The document is especially strict about refresh order:

- rerun Graphify first when installed,
- rebuild the source pack,
- reconcile deletions before ingest,
- triage findings from `okf/wiki/explorations/findings/`,
- ingest both refreshed input and promoted findings,
- preview recompilation with `--dry-run` before accepting changes.

This protects against stale pages, orphaned content, and ordering artifacts, aligning with [[concepts/orphan-retraction]], [[concepts/registry-drift]], [[concepts/knowledge-graph-feedback-loops]], and [[concepts/manifest-authoritative-reconciliation]].

The workflow also highlights a hash-registry hazard: `okf/.openkb/hashes.json` can cause future `add` runs to skip content that once existed, even if wiki pages were lost. That makes deletion reconciliation and source-chain review part of safe incremental maintenance.

## Review And Validation

The workflow treats generated wiki output like a reviewed change set. After any ingestion or recompilation that changes the wiki, it calls for a post-generation review pass that checks for:

- missing or vague concepts,
- duplicate or misclassified pages,
- off-topic distillation from example files,
- lost caveats and weakened constraints,
- truncation,
- stale early pages caused by order dependence,
- grounding failures,
- stale promoted findings.

This is an explicit instance of [[concepts/human-in-the-loop-review]], [[concepts/wiki-review-gates]], [[concepts/caveat-preservation]], and [[concepts/editorial-curation-passes]]. The workflow also distinguishes validation from health reporting: linting and bundle checks are executable gates, while reports are records of what happened, not the gate itself.

## Safety And Provenance

The workflow treats external content as evidence, not instruction. It requires:

- preserving URLs and timestamps for external sources,
- keeping repository snippets short,
- avoiding credential leakage,
- storing provider configuration locally rather than in committed files,
- never mixing unsourced web claims into compiled concept pages.

That makes the build process an example of [[concepts/wiki-content-as-untrusted-data]], [[concepts/external-documentation]], [[concepts/data-flow-disclosure]], [[concepts/provenance-tracking]], and [[concepts/privacy-preserving-tooling]].

The workflow also formalizes consent-first tooling and provenance-aware installation: optional tools are introduced only with user approval, and pinned versions plus integrity expectations are part of the build contract. This connects the workflow to [[concepts/provenance-aware-tool-installation]], [[concepts/integrity-pinning]], [[concepts/toolchain-pinning]], and [[concepts/version-pinning]].

## Self-Reference Constraint

A central rule is that the wiki must stay out of the repository graph. The source document explains why self-reference breaks deterministic convergence, grounding chains, and discovery quality. Instead, self-knowledge should come from the wiki front door, the source chain, or one-off analysis outside the main pipeline.

This is closely related to [[concepts/self-reference-control]], [[concepts/repo-scoped-graph-partitioning]], [[concepts/single-source-of-truth]], and [[concepts/self-referential-ingestion-loops]].

## Related Concepts

- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-repositories]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/evidence-staging]]
- [[concepts/okf-bundle-validation]]
- [[concepts/okf-workflow-governance]]
- [[concepts/provenance-aware-tool-installation]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/wikilink-integrity]]
- [[concepts/knowledge-base-navigation]]

In short, the OpenKB build workflow is a governed pipeline for producing a grounded, repeatable, and reviewable knowledge base from repository sources while keeping the generated wiki separate from the system that compiles it.

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
