---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Separates hard acceptance checks from advisory wiki health reporting."
---

# Validation vs Health Reporting

Validation vs health reporting is the distinction between checks that must pass to accept a knowledge-base state and checks that produce diagnostic findings without blocking progress. In this repository's OpenKB workflow, the two mechanisms are intentionally separated so deterministic structural guarantees remain enforceable, while richer semantic review can still happen as an advisory layer even when provider-backed analysis is partial, unavailable, or degraded.

This separation also matches the broader agent workflow: runtime-specific adapter generation belongs in a different lane from durable wiki governance, and harness-specific files should be treated as projections rather than project truth.

See [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], [[summaries/agents__skills__agent-ready-context__references__workflow-md]], [[summaries/agents__skills__agent-ready-context__SKILL-md]], [[summaries/agents__skills__openkb__references__commands-md]], and [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]].

## Core distinction

Validation is the pass/fail gate. It is designed to be deterministic, automation-safe, and suitable for CI or git hooks. Health reporting is an inspection layer: it surfaces issues worth reviewing, but it does not decide whether the repository state is acceptable.

The OpenKB workflow makes this split operational. Bundle validation is the structural acceptance check applied after generated wiki output is reviewed and before the KB state is accepted. `openkb lint` is the health check, and the workflow treats it as advisory: it should run when the user explicitly wants wiki health information, and it must not be used as an autonomous repair path. That keeps health reporting in its diagnostic lane and prevents it from being mistaken for the repository's authoritative acceptance contract.

This split supports [[concepts/deterministic-validation]], [[concepts/quality-gates]], [[concepts/safe-automation]], [[concepts/tool-boundaries]], and [[concepts/generated-content-governance]]. It also aligns with tooling boundary rules: project pages must not link back into tooling, while the wiki root still needs a clearly labeled harness-specific entry point when tooling pages exist.

## In the OpenKB lifecycle

The source documents define two complementary commands:

- `uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki`
- `openkb lint`

They serve different roles and are run at different points in the repository ingestion workflow. The workflow guidance treats validation as the structural acceptance check and `openkb lint` as the OpenKB health report. The validator is used after ingestion or recompilation, while lint is part of the review workflow and should be triaged, not mistaken for a gate. The command reference further narrows usage by classifying `lint` as a health-check report that should run only when the user explicitly wants wiki health information.

The workflow also requires a post-generation review pass after any `add` or `recompile` that changes `okf/wiki/`. That review checks for missing concepts, near-duplicates, misclassification, lost caveats, truncation, stale early pages, and grounding problems. The point is to route issues back through source correction and regeneration rather than hand-editing generated pages.

The subagent-profile-adapter skill extends this lifecycle by treating harness-specific adapters as runtime projections. It recommends generating adapter files only after the repository's agent-ready context exists, using the active harness's documentation rather than installed binaries as proof, and keeping those adapters short and bounded to the current environment.

### Validation

The validator is the authoritative structural gate for the wiki bundle.

Key properties:

- It is zero-LLM and deterministic
- It exits nonzero on structural violations
- It is safe for CI, hooks, and repeatable automation
- In `--openkb-wiki` mode it also checks broken `wikilinks`
- It is the recommended automation target for consented CI gates and local hooks
- It validates the generated wiki after ingestion or recompilation, before accepting the resulting KB state
- It remains usable even when no LLM provider is configured, including alongside the skeleton fallback workflow
- It performs deterministic auditability checks beyond the core OKF spec, including warnings for unclosed code fences and near-duplicate sibling pages whose names collapse to the same slug
- It tolerates absent PyYAML only by degrading YAML checks, which makes the validator useful but incomplete in minimal environments

This places validation within [[concepts/executable-validation]], [[concepts/filesystem-validation]], [[concepts/path-based-validation]], [[concepts/wikilink-integrity]], and [[concepts/okf-validation]].

The validator's structural rules include several specific checks:

- Every non-reserved Markdown file is treated as a concept document
- Every concept document must have parseable YAML frontmatter
- Every concept frontmatter must contain a non-empty `type` field
- Reserved `index.md` and `log.md` files are handled separately and must follow their own structural rules
- Root `index.md` may declare `okf_version` in frontmatter, but no other keys are expected there
- In OpenKB wiki mode, `concepts/` and `entities/` pages are also expected to carry a machine-managed non-empty `sources:` frontmatter list

Those checks make validation the hard gate for repository structure and provenance integrity.

The implementation in `.agents/skills/agent-ready-context/scripts/validate_okf_bundle.py` shows how that gate is made portable and deterministic:

- it uses `pathlib`, `argparse`, and `re` instead of shell-specific commands;
- it accepts CRLF input by normalizing line endings;
- it optionally uses PyYAML for frontmatter parsing, but degrades explicitly when PyYAML is unavailable;
- it treats `index.md` and `log.md` as reserved files with dedicated rules;
- it warns on unclosed code fences at end of file;
- it warns on sibling page names that normalize to the same slug;
- in OpenKB mode it scans wikilinks while ignoring fenced and inline code to reduce false positives.

Those details reinforce validation as a reliable filesystem-level and document-structure gate rather than a semantic review system.

### Health reporting

`openkb lint` is a health report rather than a gate.

Key properties:

- It is the OpenKB health check rather than the authoritative acceptance test
- It produces findings for review without making those findings merge-blocking by default
- It is run after ingestion as part of the review workflow, alongside bundle validation
- It should be used locally when a semantic audit is wanted, not as a CI or hook gate
- Its role is diagnostic even when structural or semantic issues are found
- Its usefulness may depend on provider availability, so it belongs to the advisory layer rather than the hard gate
- The command reference says agents should run it only when the user explicitly asks about wiki health
- The workflow explicitly avoids `lint --fix` without additional consent, reinforcing that lint output is for inspection and judgment rather than unattended repair

This behavior aligns with [[concepts/graceful-degradation]], [[concepts/human-in-the-loop-review]], [[concepts/minimal-tool-scoping]], and [[concepts/tool-boundaries]].

Health reporting is strongest when it highlights issues such as weak synthesis, missing caveats, vague classifications, and other content-level problems that require human judgment. Unlike validation, it does not define whether the repository is acceptable; it informs the decision.

The validator and the health report are intentionally asymmetrical: validation can fail a change on structural grounds alone, while health reporting can still be useful when provider-backed analysis is partial or unavailable. That means the repository can preserve a hard acceptance contract even when the diagnostic layer is degraded.

## Why the separation matters

Separating validation from health reporting avoids mixing two different guarantees.

- Structural integrity must be machine-enforceable and stable across runs
- Knowledge-quality review may depend on heuristics or provider-backed analysis and is therefore less suitable as a hard gate
- A repository can block merges on deterministic breakage without blocking work on advisory findings
- Teams can automate validation confidently while keeping semantic review in the human loop
- The workflow can degrade safely when provider-backed checks are unavailable without losing the enforceable structural gate
- Health checks can guide review of duplicates, vague page names, entity or concept misclassification, weakened caveats, and other generated-content defects without changing the acceptance contract
- Restricting `openkb lint` and forbidding autonomous `lint --fix` preserves clear boundaries between diagnosis, user consent, and mutation

The separation also supports [[concepts/source-driven-regeneration]] and [[concepts/generated-content-governance]]: deterministic gates protect the generated wiki's structure, while health reports help spot content-level issues that must be corrected through source fixes and regeneration rather than hand edits.

## Tooling context boundary

The tooling-link policy adds another layer to this split by governing how tooling-related pages are connected to the rest of the wiki.

- Pages under `okf/wiki/tooling/` may link to project pages
- Project OKF concept pages and subdirectory indexes must not link back to `okf/wiki/tooling/`
- The bundle-root `index.md` and `log.md` are exempt because they serve navigation and history roles
- When `okf/wiki/tooling/` contains non-reserved pages, the bundle-root `index.md` must reference `tooling/` in a clearly labeled harness-specific section
- When `okf/wiki/tooling/` contains non-reserved pages, the committed `tooling/index.md` stub must exist so the root-index entry resolves on clones without local tooling pages
- Tooling context is local-by-default, so the committed stub is the portable navigation surface while the rest of tooling can remain user-scoped and uncommitted

This policy fits with [[concepts/local-by-default-tooling]], [[concepts/tooling-context-governance]], [[concepts/tooling-context-isolation]], [[concepts/reserved-navigation-files]], and [[concepts/link-directionality]]. It also clarifies that validation and health reporting live in the project workflow, while tooling pages remain a constrained support layer.

## Typical examples

Validation should catch issues such as:

- Broken internal links
- Missing required structural files or metadata
- Path or bundle layout violations
- Invalid wiki structure detectable from files alone
- Other deterministic violations that should fail automation immediately
- Unclosed code fences at the end of a page, which often indicate truncation or a bad merge
- Sibling pages whose names normalize to the same slug, which can signal near-duplicate concepts
- Missing or malformed frontmatter on concept pages, including absent `type` values

Health reporting should highlight issues such as:

- Questionable knowledge synthesis
- Semantic inconsistencies
- Content-level warnings that need human judgment
- Lost caveats or weakened constraints in generated pages
- Missing, vague, duplicated, or misclassified generated pages identified during review
- Problems worth inspecting locally before deciding whether source corrections and regeneration are needed
- Situations where provider-backed analysis is partial or unavailable and the report should still provide useful, non-blocking diagnostics

The concept complements [[concepts/hash-registry-coherence]], [[concepts/generated-content-governance]], and [[concepts/okf-validation]].

## Operational guidance

In practice, use both layers together:

1. Run validation as the required gate before accepting KB changes
2. Run health reporting to inspect findings after `add` or `recompile`
3. Treat validator failures as blockers
4. Treat lint findings as review inputs unless project policy explicitly elevates a subset of them
5. Use consented CI or local hooks for validation only, because it is deterministic and failure-enforcing
6. Ask for explicit user intent before running `openkb lint`, since it is a health-reporting command rather than a default autonomous step
7. Never use `openkb lint --fix` autonomously, because advisory diagnostics and mutating repair must remain separate
8. When health findings reveal bad synthesis, fix the staged or committed source inputs and regenerate rather than hand-editing generated pages
9. Use health reporting together with direct review of `okf/wiki/` pages, because the workflow expects humans to inspect duplicates, vague naming, classification errors, and citation grounding after generation
10. Keep tooling references inside the allowed boundary: project pages should not point back into tooling, and the wiki root should provide the sanctioned harness entry when tooling pages exist
11. For harness-specific adapter work, detect the active runtime from environment and documentation, not from tool presence alone, and keep generated profiles short and permission-bounded
12. Prefer local-only tracking for generated harness adapters unless the user chooses a shared policy

This workflow fits the repository's broader patterns around [[concepts/incremental-compilation]], [[concepts/repository-ingestion]], [[concepts/generated-content-governance]], [[concepts/source-driven-regeneration]], and [[concepts/safe-automation]].

## Related concepts

- [[concepts/deterministic-validation]]
- [[concepts/executable-validation]]
- [[concepts/quality-gates]]
- [[concepts/graceful-degradation]]
- [[concepts/okf-validation]]
- [[concepts/wikilink-integrity]]
- [[concepts/hash-registry-coherence]]
- [[concepts/generated-content-governance]]
- [[concepts/source-driven-regeneration]]
- [[concepts/tool-boundaries]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/local-by-default-tooling]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/link-directionality]]
- [[concepts/runtime-adapter-management]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/subagent-role-design]]
- [[concepts/permission-scoped-agents]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__openkb__references__commands-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]