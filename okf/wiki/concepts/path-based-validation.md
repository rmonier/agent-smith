---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md"]
description: "Validation that uses filesystem location and naming as correctness signals."
---

# Path-Based Validation

Path-based validation uses a file or directory's location and name as part of correctness checking. Instead of validating only file contents, it treats placement in the repository and path shape as meaningful signals about whether an artifact follows expected conventions.

This concept appears directly in [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]], where a lightweight validation script checks not just `SKILL.md` frontmatter, but also whether a skill directory is named correctly and placed under `.agents/skills`. It also appears in [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]], which uses path rules to keep harness-specific tooling context isolated from ordinary project knowledge. The same idea also shows up in [[summaries/agents__skills__graphify__references__github-and-merge-md]], where Graphify workflow guidance distinguishes between running a skill pipeline from the current working directory and running direct extraction inside specific subfolders so outputs land in the correct location. In [[summaries/agents__skills__openkb__references__wiki-schema-md]], path and staging rules also define which files are valid KB inputs and which locations are reserved for generated wiki content. The tooling-link validator in [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]] extends this pattern by using page location to govern allowed link direction between project content and tooling pages. The OKF bundle validator in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] adds another layer by treating reserved filenames, bundle-root layout, OpenKB wiki directories, and sibling slug collisions as structural signals. The prereq checker in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] extends the same logic to setup state by validating repository writability at specific paths, confirming `okf/.openkb/config.yaml` lives where project-shared config expects it, and recognizing that `~/.config/openkb/.env` and `okf/.env` are alternative credential homes with different precedence.

## Core Idea

A path can encode policy. Validation logic can use that policy to reject resources that are technically present but structurally misplaced.

Common path-based checks include:

- requiring a resource to live under a specific root directory
- requiring directory names to match declared identifiers
- requiring expected subpaths to be directories rather than files
- using path segments to infer role, scope, or allowed behavior
- reserving certain paths for navigation or history rather than domain content
- forbidding links or dependencies across path-defined boundaries
- requiring generated outputs to be written under the intended repository or subfolder rather than a shared working directory
- requiring staged inputs to live in the KB root so registry entries remain portable and non-leaky
- requiring the root wiki index to expose a harness-specific navigation stub when tooling pages exist
- requiring committed tooling navigation files to exist so local-only pages remain discoverable on fresh clones
- treating reserved filenames like `index.md` and `log.md` as special structural cases rather than ordinary concepts
- warning when sibling file names normalize to the same slug, since that often signals near-duplicate pages or naming drift
- checking that repository paths intended for build inputs, generated content, or configuration files are writable and present
- distinguishing between per-user and project-shared config files by where they live on disk
- treating credential-home placement as a signal for configuration precedence rather than reading secret values directly
- validating that a candidate skill directory is a directory, contains `SKILL.md`, and uses a directory name that matches the frontmatter `name`
- requiring optional subdirectories such as `scripts`, `references`, and `assets` to be directories when present

This makes path structure part of a broader validation contract alongside [[concepts/frontmatter-metadata]] and [[concepts/filesystem-validation]]. In practice, path rules often express [[concepts/knowledge-boundaries]], [[concepts/tooling-context-isolation]], and [[concepts/kb-root-staging]] in a way that automation can enforce.

## How It Works in the Skill Validator

In [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]], the validator applies path-based rules in several ways:

- it reads a skill directory path from the command line and first confirms the path is a directory
- it requires the directory to contain `SKILL.md`
- it parses the frontmatter in `SKILL.md` and checks the required `name` and `description` fields
- it compares the directory name to the `name` field in frontmatter and rejects mismatches
- it checks that the skill is located under `.agents/skills`
- it verifies that `scripts`, `references`, and `assets`, if present, are directories
- it rejects names that violate the repo's slug pattern, including names with double hyphens or length over 64 characters
- it caps description and compatibility field lengths to keep skill metadata compact

These checks show that validation is not limited to document contents. The surrounding filesystem layout is treated as evidence of whether a skill has been scaffolded and stored correctly, which aligns with [[concepts/project-scaffolding]], [[concepts/skill-governance]], and [[concepts/quality-gates]].

The same pattern becomes stricter in [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]], where path policy defines not just where a file belongs, but what kind of knowledge it is allowed to contain. Tooling pages are valid only under `okf/wiki/tooling/harnesses/`, root wiki files have special reserved roles, and project-side pages must not point into tooling paths except through the reserved root index and log. Here, path placement functions as both structural validation and dependency control.

The tooling-link validator in [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]] makes that policy executable. It scans wiki Markdown, strips code blocks and inline code so examples do not cause false positives, and then flags project pages that link into `okf/wiki/tooling/`. It treats `index.md` and `log.md` as reserved navigation and history files, allowing them to mention tooling when needed. When tooling contains non-reserved pages, it also requires the root `index.md` to reference `tooling/` in a clearly labeled harness-specific section and requires a committed `tooling/index.md` stub so clones without local tooling pages can still resolve the navigation entry. The script also warns when tooling pages do not declare expected scope metadata, showing how path policy and content metadata can reinforce one another.

The prereq checker in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] uses path-based validation earlier in the workflow, before deeper bundle checks run. It probes writable paths such as `okf/.okf-build/input`, `okf`, and `.agents/skills` to make sure the repository can actually support the expected workflow. It also checks for `okf/.openkb/config.yaml` beside the committed example file and compares only the shared keys that should stay consistent across contributors. If both project and user-global credential homes exist, it reports the ambiguity rather than trying to read secrets, since file location alone already determines which source will win. That makes path placement part of readiness validation, not just artifact validation.

The OKF bundle validator in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] extends this style of checking to bundle-wide wiki conformance. It treats `index.md` and `log.md` as reserved files, applies different structural rules to each, and validates frontmatter only where it is expected. For regular Markdown pages it requires parseable YAML frontmatter and a non-empty `type` field. In OpenKB wiki mode it skips operational areas like `AGENTS.md`, `sources/`, and `reports/`, then treats broken wikilinks as errors and warns when generated concept or entity pages lack a machine-managed `sources:` list. It also emits warnings for unclosed code fences and for sibling pages whose names collapse to the same normalized slug, since both can indicate structural damage rather than simple content issues. That makes path-based validation part of a broader [[concepts/okf-bundle-validation]] and [[concepts/openkb-wiki-health-checks]] workflow.

A related operational form appears in [[summaries/agents__skills__graphify__references__github-and-merge-md]]. There, the workflow notes that the skill pipeline writes to `graphify-out/` in the current working directory, while direct `graphify extract` writes `graphify-out/` inside the scanned path. That distinction matters because running the same workflow separately on multiple local subfolders from one location would clobber outputs. The recommended approach treats path placement as a correctness condition: each subfolder's graph should be generated inside that subfolder before merge. This connects path-based validation to [[concepts/graph-merging]], [[concepts/repository-ingestion]], and [[concepts/repo-scoped-graph-partitioning]].

The OpenKB lifecycle reference extends the same idea to KB operations: `okf/` is the KB root, staged inputs should be rebuilt deterministically under `okf/.okf-build/input/`, and the registry, raw copies, and generated wiki must stay aligned. It also treats path placement as a safety signal for ownership, because only staged documents under the expected input path are candidates for automated orphan pruning. That makes path-based validation part of [[concepts/hash-registry-coherence]], [[concepts/source-provenance]], and [[concepts/read-only-kb-operations]].

## Why It Matters

Path-based validation helps repositories stay navigable and automatable.

Benefits include:

- reducing ambiguity about where resources belong
- making tooling simpler because expected locations are standardized
- catching drift between declared metadata and actual repository structure
- supporting repeatable checks in local scripts and automation
- separating kinds of knowledge that should not be treated as equivalent
- preventing accidental coupling between project documentation and tool-specific context
- avoiding output collisions when several extraction runs operate over related folders
- keeping KB staging portable by ensuring registry paths stay relative to the KB root
- preserving navigability when tooling content is local-by-default but still needs a committed entry point
- making link direction itself part of the repository contract
- surfacing likely truncation or bad merges through fence-state checks
- catching near-duplicate pages before they become confusing sources of truth
- confirming that setup artifacts are writable before more expensive validation begins
- distinguishing per-user configuration from shared repository defaults by location alone
- validating skill metadata and directory layout together so a generated or hand-authored skill is self-consistent

When repository layout is stable, other tools can rely on deterministic discovery and predictable behavior, connecting this concept to [[concepts/deterministic-validation]], [[concepts/executable-validation]], and [[concepts/index-based-discovery]]. In extraction workflows, stable placement also supports predictable merge behavior and reuse of generated artifacts.

## Relationship to Metadata Validation

Path-based validation is often complementary to metadata checks rather than a replacement for them.

In the source script, the path and the frontmatter must agree:

- the path says where the skill lives
- the directory name says what the skill is called
- the frontmatter `name` confirms the same identity in content form
- the frontmatter `description` must be present and remain within size bounds so the skill stays concise

In the tooling-context policy, the same idea appears at a different layer:

- the path says whether a page is project knowledge or tooling context
- reserved locations such as the root index and log define limited exceptions for navigation and history
- metadata such as `type`, `scope`, and `link_policy` reinforce what the path already signals

In the Graphify reference, the path also helps define operational scope:

- a GitHub clone path identifies which repository later extraction steps should target
- a subfolder path determines where per-folder `graphify-out/` artifacts should be written
- a merged graph path distinguishes reusable combined output from per-source intermediate results

In the OpenKB lifecycle reference, the same pattern appears in KB management:

- staged input paths identify which documents are owned by the pipeline
- registry metadata records whether a path is KB-relative or absolute
- raw copies, summaries, and generated wiki pages remain linked through the staged document's provenance chain

The tooling-link validator adds a further example:

- project pages may not link to tooling paths
- root navigation pages may do so only as explicit exceptions
- the presence of tooling content triggers requirements on the root index and the committed tooling stub

The OKF bundle validator adds one more layer:

- reserved files are validated by their role, not by the same rules as concept pages
- root `index.md` may carry limited `okf_version` metadata
- OpenKB mode separates operational directories from compiled content
- link targets are checked against the full wiki path inventory rather than only against text structure

The prereq checker adds a setup-oriented counterpart:

- repo readiness depends on whether specific paths are writable
- shared configuration is validated by file location and selective key comparison
- credential homes are interpreted through precedence rules, not by inspecting secret contents

This cross-check reduces inconsistency between filesystem state and document-declared identity or scope. That pattern is closely related to [[concepts/naming-normalization]], [[concepts/frontmatter-metadata]], [[concepts/reserved-wiki-files]], and [[concepts/provenance-tracking]].

## Limits and Tradeoffs

Path-based validation is useful, but it can be too strict or too loose depending on implementation.

The source script illustrates both the value and the tradeoff:

- it clearly enforces a preferred `.agents/skills` layout
- its placement check is somewhat permissive because any path containing `.agents` can satisfy part of the condition
- its frontmatter parser is intentionally lightweight, so it skips full YAML semantics in favor of simple key/value extraction

The tooling-context policy shows a more opinionated approach:

- it sharply restricts where harness-specific pages may live
- it disallows additional ad hoc folders for tooling context
- it permits only narrowly defined project-to-tooling navigation through reserved root files

The Graphify workflow adds a different tradeoff:

- shared output conventions make the default skill pipeline simple
- that same simplicity becomes risky when several subfolders are processed independently from one working directory
- path-aware extraction avoids collisions, but requires users to understand the difference between working-directory outputs and scanned-path outputs

The OpenKB lifecycle adds another constraint: path rules can be safety-critical, because a registry entry, raw copy, and wiki page can drift apart if source staging or retraction is done inconsistently. If the rule is underspecified, the validator may accept layouts that only partially match the intended standard. If overspecified, it may reject valid alternative workflows. Designing these checks well is part of [[concepts/tool-boundaries]], [[concepts/graceful-degradation]], and [[concepts/minimal-tool-scoping]].

The OKF bundle validator shows a related tradeoff in warning design:

- core conformance errors gate the run
- structural anomalies like open fences and duplicate-normalized slugs remain warnings unless `--strict-warnings` is used
- OpenKB-specific checks must balance spec compliance with practical repository hygiene
- optional dependencies like PyYAML affect how much validation can happen locally, so the script degrades rather than failing immediately when YAML parsing support is missing

The prereq checker follows the same pattern by distinguishing hard failures from advisory notes:

- missing Python, git, uv, or writable paths fail the check
- missing optional CLIs like graphify and openkb are reported separately
- missing companion skills become notes instead of hard blockers
- configuration drift and credential-home ambiguity are surfaced for the user to resolve

## Practical Use

Path-based validation is especially helpful when a repository uses convention-driven organization, such as skill directories, generated bundles, source ingestion pipelines, or isolated tooling context. In such systems, location is part of meaning.

A good path-based validator typically:

- checks only conventions that are stable and intentional
- reports path errors clearly so users can fix them quickly
- combines path checks with content checks
- supports lightweight local feedback before heavier validation stages
- treats special directories and reserved files as explicit parts of the policy
- validates not only file placement but also whether links cross forbidden path boundaries
- distinguishes between shared output roots and per-target output paths when generated artifacts are involved
- keeps KB inputs under the expected staging root so ownership and provenance remain machine-portable
- enforces reserved navigation files when local-only tooling content must remain discoverable
- treats fenced-code balance and slug collisions as audit signals worth warning about
- lets warnings escalate when a stricter review gate is needed
- probes repository writability early so follow-on steps do not fail later for avoidable filesystem reasons
- compares config files by shared keys rather than assuming all values are comparable across users
- checks skill directory naming, frontmatter, and subdirectory layout together so the whole package is internally consistent

That makes it a good fit for developer-facing validation scripts, early [[concepts/quality-gates]], and broader [[concepts/okf-validation]]. It also pairs naturally with [[concepts/provenance-tracking]] and [[concepts/source-provenance]], since path checks should reinforce source ownership rather than replace it.

See also: [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]], [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__graphify__references__github-and-merge-md]]

See also: [[summaries/agents__skills__openkb__references__wiki-schema-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__openkb__references__commands-md]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
