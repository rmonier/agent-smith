---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Governance rules for compiling, validating, and maintaining wiki knowledge."
---

# Knowledge Lifecycle Governance

Knowledge lifecycle governance is the set of rules that control how repository knowledge is captured, staged, compiled, reviewed, validated, updated, and retired so the compiled wiki stays grounded, current, and safe to use. It treats documentation as a managed pipeline rather than a static archive, with explicit gates for what may be added, what must be rechecked, and what should be removed.

The `agent-smith` README frames this as part of an [[concepts/knowledge-compilation-pipeline]]: raw repository content is source material, an interlinked wiki is the compiled knowledge layer, and the LLM or deterministic tooling acts as the compiler that ingests new material, revises cross-references, and flags contradictions. That same README also separates the repository into three operational surfaces: `AGENTS.md` for orientation, `okf/wiki/` for durable compiled context, and `.agents/skills/` for repeatable actions. Knowledge that explains things stays in the wiki; knowledge that instructs stays in skills; knowledge that routes stays in AGENTS.md. That separation is central to keeping governance manageable, repeatable, and traceable.

In OpenKB, this governance model becomes concrete through a fixed repository workflow: inspect the wiki first, stage deterministic input, ingest only approved material, validate the result, and reconcile stale or moved sources before they can leave orphaned pages behind. The KB root is `okf/`, the compiled wiki lives at `okf/wiki/`, and the source chain must stay intact from staged input through raw copies to compiled pages.

The agent-ready-context skill makes this model operational. It requires progressive disclosure from `okf/wiki/index.md`, insists on `uv run` for bundled scripts, calls for prerequisite checks before changes, and uses deterministic staging, OpenKB ingestion, linting, and validation as the normal lifecycle. It also formalizes build hygiene with `.gitignore`, `.gitattributes`, and `.graphifyignore`, and treats local tooling, provider credentials, and generated artifacts as scoped operational concerns rather than durable knowledge. In practice, that is the governance layer that keeps the repository agent-ready rather than merely documented.

The README also highlights the three portable product skills that shape the lifecycle: `agent-ready-context` for the pipeline, `skill-creator` for turning repeated actions into reusable skills, and `subagent-profile-adapter` for harness-specific runtime projections. Their presence reinforces the governance rule that compiled knowledge, executable actions, and harness adaptation remain distinct surfaces. Vendored tool skills such as `openkb` and `graphify` are treated as toolchain copies, not as product knowledge, which keeps the lifecycle boundary clear.

The editorial curation pass script extends this lifecycle model with a guarded manual-edit path. Its `--brief` mode loads the current valid wikilink targets and prints a pre-edit briefing before any change, while `--check` verifies a completed curation diff using git plus the installed OpenKB toolchain. The script treats curation as a narrow exception process: only `wiki/concepts/`, `wiki/entities/`, and the root `wiki/index.md` may change, new compiled pages must be pre-approved, and every changed compiled page must keep a non-empty `sources:` list. It also preserves provenance by requiring the union of `sources:` values across concepts and entities to remain identical before and after the edit, which makes merges safe only when they truly union source lists instead of inventing or losing citations.

## Core responsibilities

- Establish an ordered build pipeline so knowledge enters the wiki only after prerequisites, tool setup, and repository checks succeed.
- Preserve provenance by keeping source files, staged input, and compiled pages traceable through deterministic hashes and source metadata.
- Enforce validation gates so structural issues, broken links, malformed pages, and missing OKF fields are caught before changes are accepted.
- Manage lifecycle transitions for stale, deleted, moved, or deselected sources, including orphan retraction and findings triage.
- Prevent self-referential loops by keeping the KB root out of the repo graph and maintaining separation between sources and generated knowledge.
- Keep managed orientation files concise by using bounded sections and delegating deeper procedure into the skill layer.
- Support progressive disclosure so agents inspect the wiki index first, then open only the relevant context area.
- Treat the wiki as untrusted data and use OpenKB commands as controlled operations, not as content to obey.
- Provide a guarded manual curation path where the editing brief is whitelist-driven and verification is deterministic rather than model-driven.
- Keep tool adoption consent-first by requiring explicit approval for bootstrap, installation, and other potentially costly or sensitive actions.
- Record discovered harness context only when identification is reliable, and keep tooling pages local by default unless the policy explicitly carves out a committed stub.

## What this governs

The workflow describes governance across several linked phases:

- **Progressive discovery**: start from `okf/wiki/index.md` when present and use it to decide what context to read next.
- **Preflight checks**: confirm `git`, `uv`, Python 3.11+, and required vendored skills before any build work.
- **Tooling readiness**: require vendored copies of the toolchain skills before running CLI-backed steps.
- **Deterministic staging**: build `okf/.okf-build/input/` from source files in a reproducible way.
- **Controlled ingestion**: use OpenKB only after the staged input is prepared.
- **Read-first lifecycle**: check `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then inspect relevant wiki pages before querying or changing anything.
- **Command selection by goal**: choose `add`, `recompile`, `remove`, `lint`, `query`, or `visualize` based on the maintenance task, and avoid unnecessary LLM-backed calls.
- **Reconciliation before ingestion**: when repository sources are deleted, moved, or deselected, prune stale pages before adding fresh staged input.
- **Post-generation review**: inspect new or changed pages for missing concepts, duplicate pages, lost caveats, truncation, and misclassified entities.
- **Retraction and cleanup**: prune orphaned pages when source files are deleted or moved.
- **Findings management**: promote, keep, or drop captured findings based on whether they remain true and useful.
- **Managed-document maintenance**: update only the OKF-managed section of AGENTS.md between its managed markers, leaving local repository instructions intact.
- **Fallback behavior**: if a full OpenKB run is unavailable, use the zero-LLM skeleton path rather than inventing compiled context.
- **Manual curation checks**: run the editorial pass check on a diff range containing only the curation, then validate the bundle and run the single verification lint allowed by the loop guard.
- **Harness record keeping**: when the active runtime can be identified reliably, write a minimal harness record under tooling context and keep local overlay pages out of the shared navigation stub.

## Governance principles

### Determinism
The build process is designed so unchanged inputs produce unchanged outputs. Deterministic staging, stable normalization, and validation-first checks support repeatable knowledge compilation and minimize hash churn. OpenKB's `remove` path is also deterministic, which matters when reconciling deletions or registry drift.

The editorial curation check applies the same principle to hand edits. It compares the working tree to a chosen git base, classifies diff entries deterministically, and fails closed when scope, provenance, or structural invariants are violated. Its environment checks are also explicit: if the installed OpenKB venv or public lint API cannot be used, the script returns an environment error rather than pretending validation succeeded.

### Provenance
Every compiled page should trace back through staged material to repository sources. External documentation is treated as evidence rather than hidden memory or instruction. The provenance chain runs from compiled pages to summaries, from summaries to staged source copies, and from staged copies back to repository paths, hashes, and commits.

The editorial pass sharpens this rule by enforcing two related constraints: merges must preserve the union of `sources:` values across concepts and entities, and every edited compiled page must still carry a non-empty `sources:` list. That keeps curation from silently deleting a citation trail.

### Validation before trust
The workflow separates semantic health reporting from deterministic validation. LLM-backed linting is useful for review, but structural validation is the real gate for correctness.

The curation checker follows that same split: it uses the installed OpenKB's public `openkb.lint` functions for broken links, index sync, orphans, invalid frontmatter, and missing OKF fields, while keeping its own policy checks independent of model judgment. It also filters a documented false positive by ignoring orphan findings under `reports/`.

### Lifecycle cleanup
Removed or renamed sources should not leave stale wiki pages behind. The governance model explicitly includes orphan reconciliation, stale findings removal, and registry-drift repair.

The editorial pass adds a focused guardrail here: only approved new compiled pages may be created during a split, and only concepts or entities may introduce such pages. That keeps lifecycle cleanup from accidentally expanding the compiled graph without review.

### Self-reference control
The knowledge base must not feed itself through the repo graph. This avoids self-referential ingestion loops and preserves compiled knowledge bases as a grounded layer rather than a recursive one.

### Consent-first changes
Optional tools, bootstrap actions, CI hooks, and destructive cleanup steps require user consent. Governance here is not just technical; it is operational and permission-aware.

The briefing/check split reflects that same idea: `--brief` prepares context for a human or agent before editing, while `--check` provides a deterministic gate after editing. The script is designed for a guarded class-3 editorial pass rather than free-form mutation.

### Layered orientation
AGENTS.md should remain a compact routing map, while the skill layer holds the executable procedure and the wiki index routes the durable context. That keeps agent context layering and orientation routing intact.

### Evidence-backed maintenance
When generated pages are weak, the preferred fix is to improve the source documents and re-ingest them rather than patching compiled wiki output directly. Findings capture discovered invariants that are not yet represented in compiled pages, and promoted findings become part of the compiled knowledge base through ingestion.

The editorial pass aligns with this by treating its own value as a safe last-resort curation channel: it allows merge and split cleanup, but not new knowledge creation. New claims still belong in the findings channel, not in direct curation.

## Related patterns

This concept connects closely to:

- [[concepts/deterministic-builds]] for reproducible staging and ingestion.
- [[concepts/deterministic-validation]] for non-LLM structural gates.
- [[concepts/provenance-tracking]] for source traceability.
- [[concepts/orphan-retraction]] for removing pages whose sources disappeared.
- [[concepts/findings-promotion]] for triaging captured discoveries.
- [[concepts/self-reference-control]] for preventing circular KB construction.
- [[concepts/wiki-review-gates]] for the human review pass after generation.
- [[concepts/generated-content-governance]] for managing LLM-produced wiki pages.
- [[concepts/agent-context-layering]] for keeping action, context, and orientation distinct.
- [[concepts/agents-md-maintenance]] for bounded, non-destructive AGENTS.md updates.
- [[concepts/progressive-disclosure]] for opening context in a controlled sequence.
- [[concepts/source-driven-regeneration]] for correcting wiki pages by updating sources first.
- [[concepts/hash-registry-coherence]] for keeping the registry, raw files, and wiki aligned.
- [[concepts/registry-drift]] for understanding how missing pages can become permanently skipped.
- [[concepts/validation-vs-health-reporting]] for distinguishing gates from reports.
- [[concepts/read-only-kb-operations]] for the rule that knowledge lint does not mutate the wiki.
- [[concepts/editorial-curation-passes]] for the guarded manual-edit workflow.
- [[concepts/wikilink-integrity]] for preserving valid links during merges and splits.
- [[concepts/provenance-union-governance]] for keeping source lists intact across curation.
- [[concepts/openkb-wiki-health-checks]] for the vendor checks used during verification.
- [[concepts/openkb-wiki-validation-modes]] for the distinction between briefing, curation checks, and linting.

## Why it matters

Without lifecycle governance, a compiled wiki can drift from the repository, accumulate duplicates, preserve stale claims, or become self-referential. With governance in place, the wiki stays a reliable compiled knowledge base that can be regenerated, reviewed, and maintained over time without losing its grounding in the source repository.

The README broadens that point: the repository becomes agent-ready only when orientation, durable memory, and actions stay separated, when prerequisites and installs are consent-first, and when the knowledge surface is curated rather than left as a flat dump of files. Governance is therefore not just about maintaining pages; it is about preserving a usable operating model for agents over time.

The editorial curation pass shows why this matters operationally: it makes the final hand-edit path safe by binding it to the installed OpenKB environment, a whitelisted target set, explicit scope limits, provenance checks, and deterministic validation. That keeps even exceptional maintenance work inside the same lifecycle rules that govern the rest of the KB.

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]