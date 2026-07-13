---
type: "Concept"
sources: ["summaries/graphify-report.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md", "summaries/agents__skills__skill-creator__assets__skill-template-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml.md"]
description: "Rule-based validation that produces repeatable, merge-safe results."
---

# Deterministic Validation

Deterministic validation is a validation approach that produces consistent, rule-based results for the same input, making it suitable for automation, repeatable checks, merge-blocking workflows, and controlled editorial curation passes.

## Core idea

A deterministic validator applies explicit structural, syntactic, filesystem, policy, or environment rules and exits with a clear success or failure status. Unlike advisory or model-mediated checks, it is designed to behave predictably across runs and environments. That makes it a strong fit for [[concepts/quality-gates]] and for teams that need confidence that a failing check reflects a concrete rule violation rather than a probabilistic assessment.

In agent-oriented repositories, deterministic validation is part of [[concepts/context-surface-management]] and [[concepts/agent-context-layering]]: orientation lives in `AGENTS.md`, durable context lives in the wiki, and actions live in skills. The README for agent-smith frames that separation as a compilation pipeline for an [[concepts/agent-ready-repositories|agent-ready repository]]: raw files are source material, `okf/wiki/` is the compiled knowledge surface, `AGENTS.md` is the orientation layer, and `.agents/skills/` is the action layer. Deterministic validation keeps those layers coherent by checking that each surface stays within its own boundaries and that generated or curated artifacts still match the rules that make the repository agent-ready.

Deterministic validation often overlaps with [[concepts/privacy-preserving-tooling]] because it can run locally or in CI without sending repository contents to external services. In [[concepts/offline-first-workflows]], it also provides a dependable baseline when network access is unavailable or when external references are consulted only as a secondary check. The README's consent-first bootstrap and explicit fallback commands reinforce this pattern: prerequisites are checked before anything is installed, and local validation remains available even when an agent harness or remote provider is absent.

The OKF baseline described in the OpenKB quality guidance sharpens this idea by defining a small set of hard conformance rules that can be checked mechanically: every non-reserved Markdown file must have parseable YAML frontmatter, every concept document must have a non-empty `type`, and reserved `index.md` and `log.md` files must follow their required structures. It also distinguishes those hard requirements from tolerated conditions such as unknown `type` values, extra frontmatter keys, broken standard Markdown links, or missing `index.md` files. That separation is central to deterministic validation because it keeps enforcement tied to explicit, stable rules instead of subjective interpretation.

The repository validator in `validate_okf_bundle.py` extends the same idea into a concrete merge-safe check. It validates an OKF bundle or OpenKB wiki tree with a fixed set of rules, including parseable YAML frontmatter, required `type` fields on concept pages, reserved-file structure for `index.md` and `log.md`, detection of unclosed code fences, and warnings for normalized slug collisions between sibling pages. In `--openkb-wiki` mode it also skips operational areas such as `AGENTS.md`, `sources/`, and `reports/`, and it upgrades broken wikilink integrity to errors while warning when generated concept or entity pages lack a machine-managed `sources:` list. The script also treats `index.md` and `log.md` as reserved files with their own structural rules, allows an `okf_version` block in the bundle-root `index.md`, and warns on missing headings or index links rather than failing hard. That script is a strong example of deterministic validation because it separates hard failures from warnings, uses explicit rules, and produces repeatable output across runs.

The same validator also exposes a useful implementation pattern for deterministic checks: code-fence truncation detection, normalized-slug near-duplicate detection, and link scanning that ignores fenced and inline code to reduce false positives. In OpenKB wiki mode, its link resolution mirrors the local wiki target rules by accepting page-relative paths without extensions and bare stems, while excluding operational files from scan coverage. Those details make the validation behavior stable and auditable instead of heuristic or model-driven.

The editorial curation pass in `editorial_pass.py` applies the same philosophy to a narrower, hand-edited workflow. Its `--brief` mode prints a pre-edit briefing that loads the current whitelist of valid wikilink targets from the installed OpenKB toolchain, so the editing agent sees the same target constraints the compiler uses. If the private compiler middleware cannot be imported, the script falls back to a mirrored template captured from OpenKB 0.4.4 and warns loudly that the wording may be stale. Its `--check` mode then validates the resulting curation diff deterministically with vendor lint plus git-derived policy rules: only `wiki/concepts/`, `wiki/entities/`, and the root `wiki/index.md` may change; the union of `sources:` values across concepts and entities must be preserved; new compiled pages require explicit approval; and every changed concept or entity page must retain a non-empty `sources:` list. This is deterministic validation at the editorial boundary: it turns a risky manual pass into a repeatable, rule-based gate.

The preflight checker in `check_prereqs.py` extends the same approach to repository readiness. It verifies hard prerequisites such as Python 3.11+, `git`, `uv`, and git worktree membership, then records optional tooling, vendored skill presence, OpenKB config drift, credential-home ambiguity, and writable paths. The script treats these as explicit pass/fail or advisory conditions with stable outputs, which makes it a practical example of deterministic validation at the environment and repository-scaffolding level.

The orphan-retraction script in `prune_okf_orphans.py` applies deterministic validation to repository deletion reconciliation. It reads `.openkb/hashes.json`, filters to pipeline-owned entries, and compares the registry against expected staged names derived from a freshly built manifest when present or from git-tracked files otherwise. That lets it classify stale KB documents as `deleted`, `renamed`, or `deselected` and decide whether `openkb remove` should run, whether `--keep-empty` is needed for a rename, and when a safety guard should block a suspiciously large cleanup. It also avoids touching pseudo-documents such as `repo-snapshot` and `graphify-report`, and it refuses to treat user-added external documents as orphans if their registry path does not point under the pipeline staging area. This is deterministic validation used as a destructive-operation gate: it preserves registry coherence, keeps the compiled wiki aligned with source deletions, and prevents accidental retraction of content the pipeline did not create.

The agent-ready-context skill itself is structured around deterministic workflow boundaries: it distinguishes actions in skills from durable context in the wiki and from orientation material in `AGENTS.md`, requires staged input instead of direct writes into compiled wiki areas, and specifies exact commands for prerequisite checks, source-pack building, ingestion, linting, and validation. The README also describes how the repository gains and maintains that structure through consent-first bootstrap, incremental regeneration, and a validated wiki bundle. That is deterministic validation at the process level, because the workflow is only considered ready when a defined sequence of checks has been satisfied.

The OpenKB lifecycle guidance in `summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md` adds an important operational dimension: deterministic validation is not just about page format, but about preserving coherence between generated wiki pages, staged source material, and the OpenKB hash registry. In that workflow, validation is part of the safety model that catches repository damage after merges, reverts, or interrupted ingest operations, especially when the wiki and the registry can drift out of sync. The README's emphasis on deterministic source staging, deletion reconciliation, and bundle validation reinforces this as a repository-integrity mechanism, not just a document-schema check.

The same lifecycle guidance also clarifies the boundary between deterministic enforcement and broader health reporting. `openkb lint` is useful for structural diagnostics and knowledge review, but it is not the pass/fail gate; the repository validator is the merge-safe check. That distinction keeps deterministic validation focused on clear enforcement while allowing separate, richer reporting for wiki health and knowledge quality.

The skill template captured in `summaries/agents__skills__skill-creator__assets__skill-template-md` extends the same idea into action-skill authoring. Its structure requires a named skill, a concrete description of when to use it, explicit workflow steps, a commands section, and an edge-cases section. That template does not itself define a validator, but it shows how deterministic validation depends on stable document shapes: if teams want to check that skills are complete, reusable, and safe to automate, they first need a predictable schema to validate against. In practice, deterministic validation works best when procedural documents are written in formats that separate required sections from optional guidance and make validation targets mechanically identifiable.

The lightweight skill validator described in `summaries/agents__skills__skill-creator__scripts__quick_validate-py` makes this idea concrete at the directory level. It checks whether a skill path is a directory, whether `SKILL.md` exists, whether a YAML-style frontmatter block starts and closes correctly, whether required metadata such as `name` and `description` is present, whether the skill name matches a constrained pattern and the directory name, whether text fields stay within fixed length limits, whether the skill sits under `.agents/skills`, and whether optional `scripts`, `references`, and `assets` paths are directories when present. That combination shows deterministic validation in its most practical form: a finite set of explicit rules over filesystem layout and metadata shape, with no ambiguity about what passes or fails. It also connects the concept directly to [[concepts/filesystem-validation]], [[concepts/frontmatter-metadata]], [[concepts/path-based-validation]], and [[concepts/naming-normalization]].

The adoption workflow described in `summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py` adds another layer: deterministic validation can serve as the promotion gate between generated output and project-owned artifacts. In that script, a generated skill is copied into `.agents/skills/` only after basic source checks and is then immediately passed through `quick_validate.py`. If validation fails, a fresh copy is removed automatically, while a forced replacement is left in place with an explicit warning to fix or remove it. This shows deterministic validation not just as a passive checker, but as an operational control that governs when generated content is considered safe to adopt under [[concepts/generated-artifact-adoption]] and [[concepts/human-in-the-loop-review]].

The tooling-context policy in `summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md` extends the idea into repository-boundary management. It defines explicit rules for when harness-specific tooling pages may exist, where they may live, how they must be indexed, and which link directions are allowed or forbidden. Here deterministic validation is not merely checking file syntax; it is enforcing that optional tooling context remains compartmentalized from project knowledge, that reserved navigation files are the only permitted project-side entry points, and that hidden or back-linked tooling pages are treated as structural violations. This ties deterministic validation directly to [[concepts/tooling-context-isolation]], [[concepts/tooling-context-pages]], [[concepts/knowledge-boundaries]], [[concepts/index-based-discovery]], and [[concepts/reserved-wiki-files]].

The README's installation and maintenance guidance adds a practical operational context for these checks. It treats `git` and `uv` as hard bootstrap requirements, requires consent before installing missing tools, and provides explicit fallback commands for direct invocation without an agent harness. That is another deterministic pattern: the path from an incomplete environment to a usable one is governed by fixed checks, explicit commands, and clear failure modes instead of hidden setup logic.

## Role in CI workflows

In `summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml`, deterministic validation is used as the basis for an OpenKB validation gate in GitHub Actions. The workflow runs on pull requests affecting `okf/**` and executes a structural validator against `okf/wiki` using:

`uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki`

The document frames this validator as zero-LLM and suitable for gating merges because it exits nonzero on structural violations. That behavior is what makes the check deterministic in operational terms: the workflow can reliably enforce repository rules without depending on interpretation, network access to a model, or non-repeatable outputs.

`summaries/agents__skills__agent-ready-context__references__okf-quality-md` adds important detail about what the validator is actually enforcing in OpenKB mode. In `--openkb-wiki`, the validator skips operational areas such as `sources/`, `reports/`, and the root `AGENTS.md`, while still validating `index.md`, `log.md`, `concepts/`, `entities/`, `summaries/`, `explorations/`, and hand-authored tooling pages. It also layers OpenKB-specific checks on top of baseline OKF rules, treating broken wikilink integrity as errors and missing machine-managed `sources:` lists on concept and entity pages as warnings. This shows how deterministic validation can support both general conformance and repository-specific policy without losing predictability.

`summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md` treats local validation as the standard enforcement mechanism even when checking the latest official guidance from `entities/okf-spec`. In that workflow, web lookups are optional and informative, while the local validator remains the concrete tool used to verify whether an OKF bundle conforms to the expected structure.

`summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md` makes the same split explicit in day-to-day maintenance: `openkb lint` is useful as a health report, but the repository's validator is the pass/fail gate suitable for CI and hooks. The lifecycle guidance recommends running both because they serve different purposes. The validator is deterministic and merge-safe; `openkb lint` is broader and informative, including structural cross-checks and an LLM-backed knowledge review that still produces a report even when findings exist.

The skill template summary adds a useful CI-facing implication: when repositories standardize skill documents around a fixed frontmatter block and required sections like Workflow, Commands, and Edge cases, those documents become good candidates for deterministic completeness checks. That means validation can move beyond low-level syntax and into enforceable documentation contracts, as long as the contract stays explicit and machine-checkable.

The quick skill validator adds a more local but important CI pattern. Because it aggregates multiple errors, prints each concrete failure, and returns exit status `1` on any violation and `0` only on success, it behaves like a compact preflight gate for skill directories. This is especially useful in repositories that want a fast, deterministic check before broader automation runs, reinforcing the role of [[concepts/executable-validation]] as an early filter rather than a post hoc diagnostic.

The preflight checker in `check_prereqs.py` shows the same CI logic applied before compilation or ingestion begins. It verifies that the environment has the minimum required runtime and command-line tools, checks whether vendor skills are present when their CLIs are installed, warns when shared OpenKB config keys drift from the committed example, and probes writable paths before the workflow proceeds. This broadens deterministic validation from content-shape enforcement to repository readiness and toolchain preconditions.

The generated-skill adoption script adds a related CI and release-management implication. By validating immediately after copying and by failing with different cleanup behavior depending on whether the destination was new or forcibly replaced, it models how deterministic checks can be inserted at promotion boundaries inside a repository. This helps teams enforce that generated artifacts cannot silently become maintained assets without first passing an executable validation step.

The tooling-context policy adds an especially clear CI example of deterministic structural enforcement. Its dedicated validator checks whether project pages improperly link into tooling context and whether the bundle-root `index.md` exposes the tooling subtree when tooling pages exist. Those checks make repository compartment rules executable: optional harness-specific knowledge can be allowed, but only if discoverability, link direction, and placement requirements are all satisfied in a repeatable way.

The orphan-retraction script expands that same CI logic into cleanup and repair. Its manifest-first behavior prevents drift between the source-pack builder and the retraction step, while its advisory cross-check warns if the manifest and the current repository disagree about staged names. That pattern is especially important because deterministic validation is only reliable when the validator and the builder share the same selection, slugging, and bundling rules.

## Deterministic validation vs. advisory checks

The source documents draw an important boundary between deterministic validation and non-gating health reporting. `summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml` explicitly excludes `openkb lint` from the CI gate because that command is described as an LLM-backed report that always completes without failing the build. `summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md` makes a related distinction by treating official web documentation as something to compare against the embedded baseline, not as the enforcement mechanism itself.

`summaries/agents__skills__agent-ready-context__references__okf-quality-md` makes this boundary more precise by separating hard conformance rules from stricter local quality checks. For example, `--strict-warnings` is presented as useful for local quality gates but not as part of OKF conformance itself. The same document also notes that validators may warn about unclosed code fences or near-duplicate slug collisions without treating those conditions as baseline conformance failures. This distinction helps preserve deterministic enforcement while still allowing richer quality feedback.

`summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md` extends that distinction by defining `openkb lint` as a health report rather than a gate. Its structural half can surface broken links, orphaned pages, index drift, frontmatter issues, and registry coherence problems, while its knowledge half depends on the configured model and may degrade to a failure note when no provider is available. That makes it useful for diagnosis and maintenance, but still different from a deterministic validator whose exit status directly controls CI outcomes.

The quick skill validator illustrates the same boundary on a smaller scale. Its checks are intentionally narrow: it validates naming rules, file presence, basic frontmatter structure, fixed length limits, expected placement, and directory shape. It does not attempt to judge whether a skill's instructions are useful, whether its workflow is safe, or whether the metadata expresses the best possible description. That narrowness is a strength, because it keeps enforcement stable and understandable.

The preflight checker follows the same pattern. It does not attempt to prove that the repository is ready for every possible workflow; instead, it checks a compact set of hard prerequisites and emits clear notes for optional or ambiguous conditions such as missing vendor skills, dual credential homes, or absent companion skills. This keeps the tool deterministic while still preserving room for informational guidance.

The orphan-retraction script also preserves this boundary. It does not try to infer every possible historical state of a repository or explain the intent behind a deletion; it only classifies stale entries based on explicit file and content-hash evidence, then applies a conservative safety guard before any mutation. Its output is therefore deterministic and operationally useful, even though it can only approximate whether a missing document was deleted, renamed, or merely deselected by the current selection rules.

The skill template material reinforces this boundary from another angle. A template can recommend that authors validate the result, document edge cases, and keep workflows deterministic, but those recommendations only become deterministic validation when a tool converts them into explicit checks. In other words, document guidance supports validation design, but guidance alone is still advisory until encoded as rules.

The generated-skill adoption workflow sharpens that distinction in an operational setting. The script's post-copy validator determines whether the skill can remain in the destination at all, while its printed reminders about trigger-style descriptions, minimal tool scope, untrusted-content handling, secrets, and wiki fidelity remain human review tasks. In other words, deterministic validation can enforce structural readiness for adoption, but it does not replace judgment about caveat preservation, tool scoping, or whether a generated skill preserved the intent of its source material.

The tooling-context policy adds another useful contrast. It encodes hard boundaries around where harness-specific pages may live, when they may exist, and how they may be linked, but it does not claim to validate whether the tooling guidance itself is complete, current, or strategically wise. Deterministic validation can prove that the compartment rules were followed; it cannot prove that the harness advice inside the compartment is the best possible advice.

This contrast highlights a practical distinction:

- Deterministic validation is appropriate for enforcement.
- Advisory analysis is appropriate for local review and improvement.
- External specification review is appropriate for keeping local rules current.
- Local warning policies are appropriate for stricter team-level quality standards.
- Health reports are appropriate for broad repository inspection without changing merge semantics.
- Templates are appropriate for standardizing documents so future validation can be made mechanical.
- Human review is appropriate for checking whether generated outputs preserved caveats, boundaries, and safe operational intent.

This separation helps keep CI reliable while still allowing richer feedback channels outside the merge path. It also aligns with [[concepts/spec-authority]] by recognizing that deterministic local checks may need periodic adjustment when the official specification changes.

## Why teams use it

Teams adopt deterministic validation when they need:

- repeatable pass/fail outcomes
- fast structural checks in CI
- safe merge gates for documentation or knowledge artifacts
- minimal external dependencies
- clear remediation paths when checks fail
- a stable offline baseline that can be compared against newer upstream rules
- a reliable way to detect generated-content drift or registry/wiki inconsistencies
- a way to enforce required document sections and metadata in standardized templates
- a promotion gate for moving generated artifacts into maintained, project-owned locations
- a lightweight local validator for filesystem layout, path placement, and frontmatter correctness before deeper automation runs
- an executable way to preserve [[concepts/knowledge-boundaries]] between project truth and optional harness-specific tooling context
- a repeatable mechanism for enforcing repository navigation and compartment rules such as root-index visibility for tooling pages
- an explicit repository readiness check that surfaces missing runtime tools, absent vendor skills, config drift, and unwritable paths before the main workflow starts
- a deterministic way to keep staged source packs, compiled wiki output, and hash registry state aligned during regeneration and repair
- a safe pre-edit briefing for editorial curation passes that constrains the set of valid wikilink targets before any hand edit
- a post-edit diff checker that enforces curation scope, provenance union, and non-empty sources lists on changed concept and entity pages
- a conservative deletion reconciler that can retract orphaned documents without accidentally removing user-authored content or regenerating the wrong pages

For knowledge-base workflows, deterministic validation is especially useful when content must conform to a required structure before downstream tooling can safely process it. It also helps teams distinguish between formal spec violations, local policy violations, and advisory quality concerns. In the OKF/OpenKB workflow described by the OKF quality guidance and the OpenKB lifecycle guidance, that means a team can consistently enforce baseline rules for frontmatter and reserved files, add stricter repository expectations such as valid wikilink integrity, and still preserve a clear boundary between conformance, repository health reporting, and convenience warnings.

It is also valuable in workflows shaped by [[concepts/generated-content-governance]] and [[concepts/source-driven-regeneration]]. When generated wiki pages should not be hand-edited, deterministic validation provides a mechanical way to verify that regeneration preserved the required structure and that the compiled output still matches repository expectations after ingest, recompile, merge, or cleanup activity.

The orphan-retraction script adds an important corollary: deterministic validation is just as useful for removal as it is for generation. If a repository standardizes how source packs are built and how registry entries are written, then a validator can also determine when a document should be removed, whether it should be kept empty because it was renamed, and when a cleanup is too risky to apply automatically. That keeps the compiled knowledge base coherent without turning deletion handling into a probabilistic decision.

The same logic applies to reusable operational documents such as skill definitions. When a repository standardizes an action-skill format with expected frontmatter and required sections, deterministic validation helps ensure that automation-facing instructions stay complete, consistently structured, and ready for safe reuse under [[concepts/skill-based-automation]]. The generated-skill adoption workflow in `summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py` shows this especially clearly: validation is the minimum bar for adoption, while human review still checks whether constraints, warnings, and source-derived caveats survived the distillation process.

The quick skill validator adds a more granular operational example. Even without a full schema engine, a repository can still get most of the practical value of deterministic validation by codifying a small set of stable rules: where a skill may live, what metadata it must declare, how its name must be normalized, and which supporting paths must remain directories. That kind of compact validator is often enough to prevent common repository-shape errors early, before they become harder-to-debug failures in higher-level tooling.

The preflight checker shows that this principle also works for environment readiness. By treating Python version, `git`, `uv`, worktree state, optional CLI availability, vendored skill presence, OpenKB config drift, and write probes as explicit checks, it turns setup assumptions into predictable outcomes. The result is a deterministic readiness signal rather than a vague environment report, which is exactly what teams need before invoking more complex ingest or compilation workflows.

The editorial pass script adds a strong curation-specific use case. It makes manual wiki editing safer by checking that curation remains inside the allowed scope, that provenance is preserved across concept and entity pages, and that the set of valid wikilinks shown to the editor comes from the installed OpenKB whitelist machinery. This is a useful pattern for teams that want to allow rare human edits without losing machine-enforced invariants.

The orphan-retraction script shows the same principle at the maintenance boundary. By combining manifest authority, git-derived fallback logic, rename detection, and a large-change safety guard, it turns deletion reconciliation into a deterministic operation instead of a brittle manual cleanup. That helps keep the repository's hash registry and compiled wiki aligned after source removal, branch cleanup, or bundle reshaping.

The tooling-context policy shows that deterministic validation is also useful for optional, exception-based repository areas. If a repository permits special-purpose tooling pages, deterministic rules can ensure those exceptions remain explicit, discoverable, and isolated rather than silently turning into an ungoverned second knowledge base. In that sense, deterministic validation does not only protect schema compliance; it also protects documentation architecture.

## Related concepts

- [[concepts/quality-gates]]
- [[concepts/context-surface-management]]
- [[concepts/agent-context-layering]]
- [[concepts/agent-ready-repositories]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/offline-first-workflows]]
- [[concepts/spec-authority]]
- [[concepts/wikilink-integrity]]
- [[concepts/hash-registry-coherence]]
- [[concepts/generated-content-governance]]
- [[concepts/source-driven-regeneration]]
- [[concepts/skill-based-automation]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/caveat-preservation]]
- [[concepts/filesystem-validation]]
- [[concepts/frontmatter-metadata]]
- [[concepts/path-based-validation]]
- [[concepts/naming-normalization]]
- [[concepts/executable-validation]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-context-pages]]
- [[concepts/index-based-discovery]]
- [[concepts/reserved-wiki-files]]
- [[concepts/knowledge-boundaries]]
- [[concepts/source-pack-staging]]
- [[concepts/staging-manifests]]
- [[concepts/repository-ingestion]]
- [[concepts/okf-bundle-validation]]
- [[concepts/okf-validation]]
- [[concepts/orphan-retraction]]
- [[summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml]]
- [[summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__skill-creator__assets__skill-template-md]]
- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__skill-creator__references__testing-skills-md]]

See also: [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__graphify__references__extraction-spec-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

## Related Documents
- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/graphify-report]]