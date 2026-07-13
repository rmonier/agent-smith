---
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/repo-snapshot.md", "summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
type: "Other"
description: "Compiled OpenKB wiki surface for durable project context and navigation."
---

# OpenKB Wiki

OpenKB Wiki is the compiled knowledge base for durable project context, provenance, and tooling evidence. In the repository snapshot, it is the main knowledge surface that complements `AGENTS.md` orientation and `.agents/skills/` actions.

## Role

- Serves as the durable source of truth for compiled project knowledge, external evidence, and wiki navigation.
- Separates long-lived wiki knowledge from agent orientation files like `AGENTS.md` and from repository source code.
- Supports the repository's [[concepts/llm-wiki]] approach: raw sources are compiled into an interlinked wiki so agents do not have to re-derive the same understanding repeatedly.
- Stores harness-specific documentation in `tooling/` while keeping project concept pages isolated from tooling context.
- Acts as the durable context surface alongside the repository's portable skills, including `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter`.
- Treats `okf/wiki/index.md` as the first routed knowledge source after `AGENTS.md`, with the index determining subsequent wiki reads.
- When the index routes to tooling context, reads `tooling/index.md`, identifies the active harness from explicit runtime metadata or self-knowledge, and uses runtime inspection when useful rather than inferring from installed binaries.
- Requires local tooling pages to be discovered in a way that includes ignored files, with the matching harness page and any relevant provider page read before provider-backed work.
- Treats a missing bundle index or unreliable harness identity as a normal starting condition on a first clone, then continues while noting the gap.
- Uses the KB root `okf/` and the compiled wiki under `okf/wiki/`, with staged input built through `okf/.okf-build/input/`.
- Treats `index.md` and `log.md` as reserved filenames at any directory level, with non-reserved `.md` files treated as concept documents.
- Aligns with a read-first lifecycle that starts with `openkb status` and `openkb list`, then inspects the wiki front door before any query or mutation.
- Relies on deterministic validation to enforce OKF conformance and OpenKB wiki rules before changes are accepted.
- Uses `validate_okf_bundle.py` as the repository-local checker for OKF bundle structure, reserved-file handling, frontmatter requirements, slug collisions, code-fence truncation, and optional OpenKB wiki link integrity.
- In `--openkb-wiki` mode, treats broken [[concepts/wikilink-integrity]] as errors, skips `AGENTS.md`, `sources/`, and `reports/`, and warns when compiled `concepts/` or `entities/` pages lose their machine-managed `sources:` provenance list.
- Distinguishes formal OKF checks from OpenKB-specific operational conventions, making validation both spec-aware and repository-aware.
- Frames the wiki as part of a [[concepts/knowledge-compilation-pipeline]]: source material is staged, compiled, re-linked, and validated so knowledge compounds across sessions.
- Reflects [[concepts/context-surface-management]] and [[concepts/progressive-disclosure]] by keeping only durable, high-signal knowledge in the compiled wiki.
- The repository snapshot shows the wiki is backed by a broad set of tracked files, including repository governance files, license texts, documentation assets, and multiple skill packages under `.agents/skills/`.
- The tracked file surface suggests the wiki is meant to describe and support a modular agent-tooling repository, not just a single application.
- Graphify analysis confirms the wiki is part of a large knowledge graph: the report covers 63 files, 472 nodes, 550 edges, and 54 communities, indicating that structural navigation materially improves discovery.
- Graphify also shows strong hub pages such as `README.md`, `AGENTS.md`, `OpenKB repo build workflow`, `OpenKB lifecycle for OKF maintenance`, and `OpenKB Wiki Schema`, reinforcing the wiki's role as a cross-cutting navigation layer.
- The graph report highlights `main()` and `bundle_key()` as bridge nodes between build and skill-maintenance clusters, showing that OpenKB Wiki sits in a system where generated artifacts, skills, and repo maintenance are tightly coupled.
- The same report surfaces 234 isolated nodes and several thin communities, which makes the wiki important for [[concepts/documentation-gaps]] discovery and follow-up curation.

## Governance

- Project knowledge is compiled into the wiki rather than treated as ad hoc agent state.
- Tooling context is allowed to point into project knowledge, but project concept pages must not link back to tooling pages.
- The root `index.md` should enumerate tooling pages in a clearly labeled harness-specific section when they exist.
- `tooling/index.md` acts as the committed navigation stub for local tooling pages.
- The wiki is meant to preserve [[concepts/provenance-tracking]], [[concepts/durable-context]], and [[concepts/knowledge-lifecycle-governance]] for the repository.
- The compiled bundle should remain aligned with source changes through [[concepts/incremental-compilation]] and [[concepts/deterministic-validation]].
- The wiki should support [[concepts/knowledge-base-navigation]] and [[concepts/index-based-discovery]] by routing readers from `index.md` into the right compiled pages.
- Generated pages should remain within the boundary of [[concepts/generated-content-governance]] and [[concepts/read-only-kb-operations]], with findings used for durable new observations.
- OpenKB owns `okf/raw/` and generated wiki pages; changes should flow through staged input, `openkb add`, or `openkb recompile` rather than hand edits.
- The lifecycle distinguishes deterministic ingestion, registry coherence, deletion reconciliation, and source-grounded regeneration as separate concerns.
- Findings are captured in `okf/wiki/explorations/findings/`, promoted only when they are still true and missing from compiled truth, and kept or dropped otherwise.
- The KB should preserve citation chains through machine-managed `sources:` lists and verbatim staged copies under `okf/wiki/sources/`.
- Validation is split between `openkb lint` as a health report and repository validation as a pass/fail gate.
- The local validator treats unclosed fences and normalized slug collisions as warning signs of truncation, bad merges, or near-duplicate pages.
- `index.md` has soft structural expectations in the validator: it should include at least one heading and at least one Markdown link, but missing either is warned rather than failed.
- `log.md` is validated as a reserved file with heading-format rules, and the OpenKB wiki mode accepts the timestamped log headings used by the repository.
- Known upstream dependency issues in OpenKB are treated as installation or resolution problems, not wiki-content problems.
- Curation-only edits are a bounded exception for output-only cleanup when sources are already correct and findings do not fit.
- The build workflow starts by reading `okf/wiki/index.md` after `AGENTS.md`, then follows the index into tooling or project pages as appropriate.
- Hard prerequisites are checked before other work, and missing Git, `uv`, or Python 3.11+ must be handled before proceeding through the pipeline.
- Optional tools like Graphify and OpenKB are bootstrapped consent-first when missing, and vendored skill copies must exist before the corresponding CLI is used.
- The workflow requires `.gitignore`, `.gitattributes`, and `.graphifyignore` coverage for the KB root and build outputs, with normalization choices preserved unless the user approves changes.
- Graphify runs with `GRAPHIFY_NO_BACKUP=1 graphify update . --force` when available, but failures degrade gracefully instead of blocking the rest of the pipeline.
- Source-pack staging is deterministic and commit-aware, with `source_commit` pinned to the last commit that touched each file rather than `HEAD`.
- External URLs are treated as evidence and staged separately before ingestion, never as hidden memory or executable instructions.
- Incremental refreshes rebuild the source pack, reconcile deletions before ingesting, and recompile only after the wiki's structural picture matches the current repository.
- Post-generation review checks for missing concepts, duplicate pages, misclassification, lost caveats, truncation, stale early pages, grounding gaps, and stale promoted findings.
- `openkb lint` remains a semantic health report, while validation scripts provide the deterministic gate for CI and local hooks.
- `AGENTS.md` should keep operational pointers in the file itself and point deeper rationale back to `okf/wiki/index.md` instead of duplicating wiki content.
- The wiki's self-reference boundary is deliberate: `okf/` stays out of the repo graph to avoid feedback loops, circular grounding, and discovery pollution.
- The managed OKF guidance in `AGENTS.md` is maintained by `.agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py`, which only inserts or replaces the section between `<!-- okf:start -->` and `<!-- okf:end -->` markers.
- That script treats the section as a routing map rather than a knowledge base, preserves repository-specific instructions outside the managed block, and can initialize a new `AGENTS.md` when none exists.
- The managed section explicitly routes agents to `okf/wiki/index.md`, `tooling/index.md`, `graphify-out/GRAPH_REPORT.md`, `.agents/skills/`, and `okf/wiki/AGENTS.md` as layered sources of orientation and workflow guidance.
- It also encodes maintenance rules that favor `uv run` for bundled scripts, discourage direct edits to OpenKB-managed compiled pages, and ask agents to capture durable observations as findings instead of mutating compiled truth.

## Related entities

- [[entities/okf]]
- [[entities/openkb]]
- [[entities/agents-md]]
- [[entities/agent-skills]]
- [[entities/subagent-profile-adapter]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/readme-md]]
- [[entities/agent-smith]]
- [[entities/openkb-wiki]]
- [[entities/agent-ready-context]]
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/prune-okf-orphans-py]]
- [[entities/prune_okf_orphans-py]]
- [[entities/validate_okf_bundle-py]]

## Related concepts

- [[concepts/compiled-knowledge-bases]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-link-policy]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/link-directionality]]
- [[concepts/single-source-of-truth]]
- [[concepts/context-action-separation]]
- [[concepts/progressive-disclosure]]
- [[concepts/source-grounded-regeneration]]
- [[concepts/agent-context-layering]]
- [[concepts/knowledge-boundaries]]
- [[concepts/source-provenance]]
- [[concepts/findings]]
- [[concepts/okf-offline-conformance]]
- [[concepts/okf-validation]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/reserved-markdown-file-rules]]
- [[concepts/wikilink-integrity]]
- [[concepts/hash-registry-coherence]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/orphan-retraction]]
- [[concepts/registry-drift]]
- [[concepts/findings-promotion]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/generated-content-governance]]
- [[concepts/read-only-kb-operations]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/deterministic-builds]]
- [[concepts/deterministic-validation]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/source-pack-manifest]]
- [[concepts/source-pack-staging]]
- [[concepts/safe-automation]]
- [[concepts/non-interactive-agent-design]]
- [[concepts/graph-structure-analysis]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/documentation-gaps]]
- [[concepts/cross-community-bridges]]

## Related Documents
- [[summaries/repo-snapshot]]

- [[summaries/README-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__LICENSING-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

See also: [[summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt]]

See also: [[summaries/README-md]]

See also: [[entities/okf]]

See also: [[entities/openkb]]

See also: [[entities/agent-smith]]

See also: [[entities/agent-ready-context]]

See also: [[entities/agents-md]]

See also: [[entities/agent-skills]]

See also: [[entities/subagent-profile-adapter]]


See also: [[summaries/karpathy-llm-wiki-gist]]
