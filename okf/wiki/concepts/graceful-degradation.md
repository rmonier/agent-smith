---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md"]
description: "Fallback behavior that preserves useful output when preferred capabilities are missing."
---

# Graceful Degradation

Graceful degradation is a design approach where a system keeps producing a useful, lower-fidelity result when preferred capabilities are missing or unavailable. In the OpenKB workflow, that means a pipeline can still initialize checks, surface actionable diagnostics, preserve a navigable knowledge base path, and record provenance even when optional tooling, credentials, or semantic compilation are not fully available.

This concept is directly illustrated by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]] and [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]. It is also reinforced by [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]], which documents a compatibility fallback in `scripts/editorial_pass.py` that mirrors OpenKB behavior only when a private upstream API cannot be imported.

## Core idea

- Prefer a usable partial result over total failure.
- Preserve traceability so fallback output can be reviewed and improved later.
- Limit claims: the fallback should not pretend to be semantically complete.
- Keep degraded paths compatible with later enrichment, regeneration, or manual repair.
- Separate hard requirements from optional capabilities so users can proceed with clear guidance.
- Record provenance when fallback behavior depends on copied or mirrored upstream logic.

## How the source scripts apply it

The workflow uses graceful degradation in complementary ways.

The skeleton builder applies it by switching from semantic compilation to structural scaffolding:

- It generates a repository overview from repository metadata and a `graphify-report.md` excerpt.
- It copies staged external markdown files into `references/` as evidence material.
- It creates a root `index.md` and `log.md` so the wiki remains navigable and time-stamped.
- It avoids inventing deeper content, labeling the result as a skeleton rather than authoritative knowledge.

The prereq checker applies it by making readiness visible without over-failing:

- It checks required runtime basics such as Python 3.11+, `git`, and `uv`.
- It distinguishes optional tools like `graphify` and `openkb` from hard requirements.
- It validates whether the repository is inside a Git worktree before relying on repository-local operations.
- It verifies writable paths so later build steps can proceed safely.
- It reports config drift in `okf/.openkb/config.yaml` only for shared keys, while leaving provider-specific settings to the user.
- It treats missing `.env` files as acceptable for OAuth-based setups and warns only when key-based providers may need credentials.
- It detects when both project-local and user-global credential homes exist, because that ambiguity can affect which settings win.
- It checks for vendored skill copies alongside installed CLIs, but does not fail when the CLI is absent and the vendor copy is not yet required.

A third example appears in `scripts/editorial_pass.py`: if `openkb.agent.compiler` cannot be imported, the script falls back to a mirrored constant and a from-scratch formatting helper so the brief briefing text still works. The notice records that the mirrored string is copied verbatim from `openkb/agent/compiler.py`, while the formatter is a clean-room reimplementation of upstream behavior. That fallback is explicitly scoped to wording differences in `--brief` output and does not affect the correctness gates of `editorial_pass.py --check`.

This behavior connects closely to [[concepts/llm-free-knowledge-bootstrap]], [[concepts/source-grounded-regeneration]], [[concepts/evidence-staging]], [[concepts/preflight-checks]], [[concepts/deterministic-validation]], [[concepts/configuration-precedence]], [[concepts/compatibility-fallback]], [[concepts/clean-room-reimplementation]], [[concepts/provenance-tracking]], and [[concepts/license-compliance-requirements]]. It also supports [[concepts/compiled-knowledge-bases]] by ensuring that a knowledge base can still be initialized before richer compilation is available.

## Why it matters

Graceful degradation reduces workflow brittleness. In documentation and knowledge-compilation systems, the alternative to a fallback often is no output at all. A conservative skeleton, a clear prereq report, and explicit provenance notes give maintainers:

- a stable starting point,
- a place to attach evidence,
- a visible signal that deeper enrichment is pending,
- and a path toward [[concepts/incremental-compilation]].

That makes the overall system more resilient and easier to validate under constrained conditions, especially in [[concepts/offline-first-workflows]] or other environments with limited provider access, missing optional tools, or mismatched local configuration.

## Related design patterns

- [[concepts/deterministic-builds]] for reproducible fallback output.
- [[concepts/executable-validation]] for checking that the degraded path still works.
- [[concepts/confidence-calibration]] for making it clear that the result is provisional.
- [[concepts/documentation-layer-separation]] for keeping source material, evidence, and compiled pages distinct.
- [[concepts/knowledge-boundaries]] for avoiding overreach when semantic context is incomplete.
- [[concepts/consent-first-tooling]] for keeping optional tools optional.
- [[concepts/local-vs-shared-configuration]] for handling per-user config without conflating it with shared project settings.
- [[concepts/skill-vendoring]] for ensuring toolchain dependencies are pinned in-repo when required.
- [[concepts/attribution-based-reuse]] for documenting when mirrored upstream material informs a fallback.

## Practical takeaway

A well-designed fallback does not try to be clever; it tries to stay useful. In this case, the scripts keep the wiki pipeline alive by either producing a minimal, reviewable bundle or by clearly explaining what is missing and what can still continue. When upstream private APIs are unavailable, the editorial pass can still degrade safely, provided the provenance is documented and the behavior remains scoped. That preserves momentum without hiding uncertainty, and it leaves a clean path for later enrichment into full compiled knowledge.