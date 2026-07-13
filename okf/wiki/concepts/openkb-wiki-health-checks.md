---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
description: "Validation rules that keep OpenKB wiki structure, metadata, and tooling boundaries sound."
---

# OpenKB Wiki Health Checks

OpenKB wiki health checks are the validation rules and hygiene checks that detect structural damage, missing metadata, broken internal references, and policy violations before compiled content is treated as trustworthy wiki output. They sit between source ingestion and compiled knowledge, helping preserve [[concepts/generated-content-governance]], [[concepts/wiki-review-gates]], [[concepts/wikilink-integrity]], and [[concepts/tooling-context-isolation]]. In the agent-ready compilation flow, they also support the broader build workflow that keeps repository context split between actions, compiled knowledge, and orientation.

## What These Checks Protect

- Reserved navigation files such as `index.md` and `log.md`
- Required frontmatter on generated concept and entity pages
- Internal wiki links that must resolve to existing pages
- Signs of truncation or merge failure, such as an unclosed code fence
- Duplicate or near-duplicate page names that normalize to the same slug
- Machine-managed `sources:` provenance on compiled pages
- One-way link boundaries between compiled project pages and local tooling context
- The committed root navigation stub that keeps local tooling discoverable across clones
- The separation between orientation files, durable wiki context, and repeatable action surfaces described in the build workflow
- The offline OKF v0.1 baseline used when web access is unavailable
- The distinction between strict spec conformance and the more practical `--openkb-wiki` validation mode
- The requirement to keep generated wiki content out of direct hand edits and instead route fixes through source updates, staged input, and re-ingestion
- The need to preserve registry coherence in `okf/.openkb/hashes.json` so deduped content does not silently disappear from future runs
- The use of `okf/wiki/index.md` as the first OKF page after root `AGENTS.md`, with downstream reads driven by index entries
- The expectation that local harness context is discovered from explicit runtime metadata or self-knowledge, not by guessing from installed binaries
- The rule that tooling pages under `okf/wiki/tooling/` may link outward, but project concept pages and subdirectory indexes must not link back into tooling except for the reserved bundle-root `index.md` and `log.md`

## Core Validation Ideas

The source script `[[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]` implements a local validator for OKF bundles and OpenKB wiki trees. Its behavior combines spec conformance checks with OpenKB-specific hygiene checks.

The companion script `[[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]` adds a narrower policy layer for tooling-context boundaries. It ensures that pages under `okf/wiki/tooling/` can point outward, while project concept pages and navigation indexes do not link back into tooling, except for the reserved bundle-root `index.md` and `log.md`. It also requires a clearly labeled harness-specific section in the bundle-root index when tooling pages exist, and it requires a committed `tooling/index.md` stub so that the root link resolves cleanly on clones without local tooling pages.

The OKF baseline is intentionally offline-friendly. It treats a bundle as a UTF-8 Markdown directory tree, allows arbitrary subdirectories, and defines a small hard conformance set: every non-reserved `.md` file must have parseable YAML frontmatter, every concept frontmatter must include a non-empty `type`, and reserved `index.md` and `log.md` files must follow their own structures. When web access is available, the baseline should be refreshed against the official OKF spec and README; when it is not, validation should continue against the embedded OKF v0.1 rules and report that mode explicitly.

The build workflow clarifies why this boundary matters: repository state is intentionally split into actions under `.agents/skills/`, durable compiled context under `okf/wiki/`, and orientation in `AGENTS.md`. Health checks help keep those layers distinct so compiled knowledge does not absorb runtime-only harness details, tool-specific state, or action procedures.

The workflow also establishes ordering constraints that health checks protect indirectly: root metadata is read first, optional tooling is only bootstrapped with consent, vendored toolchain skills must exist before CLI use, `.gitattributes` and `.graphifyignore` must be kept in sync with the pipeline, and Git history is required for deterministic source-pack construction.

### OKF-facing rules

- Every non-reserved Markdown file is treated as a concept document.
- Concept pages must contain parseable YAML frontmatter.
- Concept frontmatter must include a non-empty `type` field.
- `index.md` and `log.md` are reserved files with their own rules.
- The bundle-root `index.md` may declare `okf_version` in frontmatter.
- Consumers should tolerate unknown `type` values, extra frontmatter keys, and broken cross-links in plain OKF mode.
- The bundle index should be the first OKF page read after root `AGENTS.md`, and its entries should drive later wiki reads.
- If the bundle routes to tooling context, the local harness must be identified from runtime evidence rather than inferred from binaries alone.

### OpenKB-specific rules

- In `--openkb-wiki` mode, `AGENTS.md`, `sources/`, and `reports/` are skipped as operational areas.
- Broken wikilinks are treated as errors.
- Concepts and entities should carry a non-empty machine-managed `sources:` list.
- Fenced and inline code are ignored during link scanning to reduce false positives.
- Project pages must not link into `okf/wiki/tooling/`, preserving a one-way dependency from tooling context to compiled knowledge.
- If `okf/wiki/tooling/` contains non-reserved pages, the root `index.md` must reference tooling in a clearly labeled harness-specific section.
- If local tooling pages exist, a committed `okf/wiki/tooling/index.md` stub must exist so the root index resolves cleanly on clones that do not include user-scoped tooling pages.
- Tooling pages that are not reserved navigation files should declare their scope clearly, using the repository’s tooling conventions.
- Compiled project knowledge should remain separate from vendored toolchain copies and harness-specific adapters.
- In `--openkb-wiki` mode, exploration pages are handled pragmatically because OpenKB query exports can deviate from hard spec expectations, while finding pages under `explorations/findings/` are expected to be fully enumerated and evidence-backed.
- The root index should remain the front door for tooling discovery, but only with clearly labeled sections and no reverse-link leakage from project pages.

## Health Signals

These checks distinguish between hard failures and softer warning signals.

- Errors block validation when a page is malformed, missing required metadata, contains a broken wikilink, or violates tooling-link policy.
- Warnings flag likely quality issues such as missing recommended fields, empty bodies, suspicious filename collisions, or tooling pages that do not declare their scope clearly.
- `--strict-warnings` can promote warnings into errors when a tighter gate is needed.
- Validation also warns on unclosed code fences and same-directory names that collapse to one slug, since both often indicate truncation or merge damage.
- Registry drift in `okf/.openkb/hashes.json` is a special hazard because future `add` runs may silently skip content that the registry already believes is present.
- A missing or unreliable harness identity is not a page failure, but it is a health concern because the workflow should not guess the runtime context from installed binaries.
- If Graphify fails, the pipeline continues with degraded coverage, so the health model must tolerate that fallback while still reporting the failure.
- A missing `tooling/index.md` stub is a structural failure once local tooling pages exist, because the bundle-root link must resolve in clones that do not have user-scoped tooling content.

## Why It Matters

OpenKB depends on [[concepts/deterministic-validation]] to keep generated wiki content stable and auditable. Health checks reduce the risk of:

- silent content corruption,
- broken navigation graphs,
- orphaned or untraceable pages,
- low-confidence knowledge entering the compiled wiki,
- accidental coupling between compiled knowledge and local tooling context,
- drift between source documents, compiled wiki pages, and the repository’s agent-ready surfaces,
- validation gaps when the wiki must be checked offline,
- registry mismatch that causes later ingest runs to miss pages silently,
- and build-order failures where later compilation steps run against stale structure.

That makes them part of [[concepts/quality-gates]], [[concepts/provenance-tracking]], [[concepts/knowledge-lifecycle-governance]], and [[concepts/link-directionality]]. They also support the broader compilation model, where durable wiki knowledge is expected to stay synchronized with source changes and preserve evidence rather than re-deriving context from scratch. The same role extends to the agent-ready workflow’s insistence on consent-first tooling, deterministic staging, and correction loops instead of ad hoc wiki edits.

## Related Patterns

- [[concepts/frontmatter-metadata]] for structured page metadata
- [[concepts/reserved-wiki-files]] for special-case file handling
- [[concepts/filesystem-validation]] for path-based bundle checks
- [[concepts/openkb-wikilink-resolution]] for how wiki links resolve locally
- [[concepts/source-provenance]] for source traceability on generated pages
- [[concepts/graceful-degradation]] for partial validation when PyYAML is unavailable
- [[concepts/local-by-default-tooling]] for user-scoped tooling that is not always part of the shared bundle
- [[concepts/tooling-link-policy]] for the one-way boundary between tooling pages and project pages
- [[concepts/tooling-navigation-exceptions]] for the reserved navigation files that remain exempt from the reverse-link rule
- [[concepts/compiled-knowledge-bases]] for the broader compiled wiki bundle this validation protects
- [[concepts/okf-offline-conformance]] for the embedded offline ruleset this page summarizes
- [[concepts/generated-content-governance]] for the rule that compiled output should be reviewed and corrected through source-driven regeneration
- [[concepts/registry-drift]] for the hash-registry mismatch risk that can cause silent ingest skips
- [[concepts/consent-first-tooling]] for the install-and-adopt discipline around `openkb` and `graphify`
- [[concepts/deterministic-builds]] for the repeatable staging and validation model that health checks support
- [[concepts/openkb-build-workflow]] for the ordered repository-to-wiki pipeline that these checks guard
- [[concepts/preflight-checks]] for the prerequisite verification that happens before build work begins
- [[concepts/tooling-stub-resolving]] for discovering the correct local harness page when the bundle index routes to tooling
- [[concepts/okf-bundle-validation]] for the local bundle validator that enforces these rules
- [[concepts/openkb-wiki-validation-modes]] for the difference between strict spec validation and wiki-mode validation
- [[concepts/validation-vs-health-reporting]] for the distinction between hard errors and softer health warnings

## Operational Role

OpenKB wiki health checks are useful both during local authoring and in automated pipelines. They provide a baseline gate before more expensive or downstream processes such as graph import, regeneration, or publication. In the agent-ready model, they help maintain a wiki that is structurally coherent, traceable, safely partitioned, and navigable even when local tooling pages are present only on the current machine. That makes them a practical part of the repository’s maintenance loop, alongside consent-first setup, deterministic compilation, staged evidence ingestion, and incremental reconciliation of changed sources.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]