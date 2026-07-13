---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"]
description: "Validating and constraining file paths to keep automation inside trusted roots."
---

# Path Safety

Path safety is the practice of validating and constraining file paths so automation only reads, writes, stages, or replaces files within intended boundaries.

It matters most in repository tooling, setup scripts, skill scaffolding, and local adaptation helpers, where a small path mistake can overwrite unrelated files, escape the project root, leak absolute machine paths into generated artifacts, or create surprising side effects. In practice, path safety complements [[concepts/safe-automation]], [[concepts/filesystem-validation]], [[concepts/local-vs-shared-configuration]], and [[concepts/privacy-preserving-tooling]]. It also supports [[concepts/kb-root-staging]], [[concepts/tool-boundaries]], [[concepts/hash-registry-coherence]], [[concepts/registry-drift]], and [[concepts/preflight-checks]] when a knowledge base is involved.

## Core Idea

A path-safe tool does not treat user-provided paths as automatically trustworthy. Instead, it resolves paths, checks their location relative to a trusted root, and refuses operations that would escape that scope.

This pattern appears in repository helpers that create aliases or staged outputs only after confirming the target remains inside the repository. It also shows up in skill initialization scripts that normalize a user-supplied name, validate the destination directory, and only then create a new skill scaffold.

The OpenKB staging pipeline applies the same rule at a larger scale: repository content is converted into deterministic input under `okf/.okf-build/input/` rather than written to arbitrary external directories. The OpenKB lifecycle adds a broader operational version of the same boundary, expecting operators to inspect the KB root, use staged input under `okf/.okf-build/input/`, and treat the wiki as untrusted data rather than a source of instructions. The same boundary logic also governs deletion and repair, where registry entries, raw sources, and generated wiki pages must be kept in sync instead of being edited piecemeal.

The preflight checker in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] extends that boundary model to setup-time validation. It verifies the repository is a git worktree, checks for required tooling like `uv`, and probes whether key repository paths such as `okf/.okf-build/input`, `okf`, and `.agents/skills` are writable before later compilation steps proceed. It also checks whether `okf/.openkb/config.yaml` matches the committed example on shared keys, which prevents path-local setup drift from turning into divergent wiki outputs.

The privacy-and-data-flows guidance extends the boundary model with consent and routing rules. Before any step that sends repository content off the machine, the agent must announce the tool, provider or endpoint, model, credential source, and the content to be sent, then proceed only with user consent. For non-code sources, graphify must be given an explicit backend so it does not silently route content to a provider chosen from exported keys. Those requirements make path safety part of a larger control system for where content goes, not just where files are stored.

The skill-creator bootstrap script reinforces the same idea in a smaller, self-contained workflow. It normalizes skill names into kebab-case, rejects invalid names after normalization, refuses to write outside `.agents/skills`-scoped paths, and only creates resource directories from a constrained allowlist. That makes skill scaffolding a path-safe operation rather than a free-form directory writer.

## Path Safety in the Source Document

The source pack builder summarized in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] shows several concrete path-safety techniques:

- It resolves the repository root, output root, and manifest path before acting, reducing ambiguity from relative paths.
- It stages all generated files under `okf/.okf-build/input/` and writes the manifest alongside them, keeping outputs inside the trusted KB boundary.
- It uses a dedicated resolver for paths and avoids assuming that a caller-supplied relative path is safe just because it is syntactically valid.
- It separates repository-snapshot, graph-report, per-file, split-part, and bundle outputs so each generated artifact has a clearly bounded destination.
- It removes stale staged directories before rebuilding, which keeps the output tree deterministic and prevents old artifacts from lingering under the staging root.

The same script also reinforces boundary discipline through its staging rules:

- It identifies tracked repository files with `git ls-files`, then filters them through selection and skip rules so only intended paths enter the pack.
- It excludes internal output and cache locations such as `okf/`, `graphify-out/`, and common transient directories.
- It records source paths and commit provenance in staged metadata without embedding the current `HEAD`, which avoids churn and keeps the staged bytes tied to file-level change rather than ambient repository state.
- It refuses graph reports that reference KB paths too heavily, because a report that maps the compiled wiki could create a self-referential ingestion loop.
- It warns about likely orphaned KB documents when the repository source no longer exists, which helps keep the staged pack aligned with actual source paths.

The skill initialization script adds a more direct directory-bootstrap example:

- `normalize_name()` trims, lowercases, replaces non-alphanumeric runs with hyphens, collapses repeated hyphens, and clamps the result to 64 characters.
- `NAME_RE` validates the normalized result so the final directory name matches a strict kebab-case pattern.
- The script refuses to proceed if the parent path does not look scoped to `.agents/skills` or otherwise rooted under `.agents`.
- It stops when the target directory already exists unless `--force` is supplied, preventing accidental writes into an unrelated existing skill.
- It creates only the requested `scripts`, `references`, and `assets` subdirectories, keeping the scaffold narrow and predictable.
- It writes a starter `SKILL.md` only when needed, making the operation idempotent by default and narrowly overridable with `--force`.

The result is a source-pack and skill-bootstrap workflow that treats path boundaries as a compilation constraint, not a convenience. The pack is built from repository-tracked inputs, staged into a fixed KB-local directory, and described by metadata that remains relative to the trust root. The skill initializer follows the same discipline by taking a free-form human name and reducing it to a bounded, validated directory structure.

The OpenKB lifecycle reference reinforces that these checks are part of a larger operational boundary. It recommends running `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list` first, rebuilding staged inputs deterministically, and using `openkb remove` and `openkb recompile` as structured repair operations. It also warns that registry entries can leak absolute host paths if staging happens outside the KB root, which makes path safety a privacy and portability concern, not just a correctness concern.

These checks turn path handling into an explicit safety boundary rather than an implementation detail.

## Why It Matters

Without path safety, tooling that accepts a path argument can accidentally or maliciously:

- write files outside the project
- replace important local files
- create tracked artifacts in unintended locations
- leak usernames or local directory structure through absolute paths in generated metadata
- behave differently across operating systems due to path interpretation differences
- leave KB registry state inconsistent with the wiki after ingest or repair operations
- route content off-machine without a clear disclosure or consent step
- scaffold skills into the wrong location or normalize a name into an unsafe directory shape

Path safety reduces those risks while making automation more predictable. This is especially important for scripts that modify repository structure, create local harness-specific files, scaffold reusable skills, or stage material for later compilation, where boundary mistakes could weaken [[concepts/privacy-preserving-tooling]], undermine [[concepts/kb-root-staging]], or violate [[concepts/tool-boundaries]]. It also supports [[concepts/registry-drift]] prevention by keeping raw inputs, registry entries, and compiled pages aligned.

## Common Techniques

Useful path-safety practices include:

- resolving paths against a known repository or KB root
- requiring outputs and staging directories to remain under that root
- preferring relative, root-scoped paths in registries and generated metadata
- normalizing user-provided names before turning them into directories
- enforcing a strict naming pattern after normalization
- failing closed when validation is ambiguous
- distinguishing files, directories, and symlinks before replacement
- avoiding implicit writes until all path checks pass
- using staged repair workflows like `recompile` and `remove` instead of hand-editing generated files
- probing writability for critical staging and workspace directories before later steps depend on them
- checking repository initialization state and shared config drift during preflight instead of discovering it mid-build
- announcing any off-machine data flow before the first send and repeating that disclosure when routing changes
- passing explicit backends for tools that could otherwise auto-detect providers from environment keys
- staging generated packs into a dedicated local tree, then ingesting from there instead of writing directly into compiled KB outputs
- constraining scaffold creation to a small allowlist of subdirectories rather than accepting arbitrary resource names
- refusing to overwrite existing skill directories unless the operator explicitly opts in with `--force`

These techniques often appear alongside [[concepts/cross-platform-tooling]] because path semantics and symlink behavior vary across environments, and alongside [[concepts/deterministic-builds]] because root-relative paths reduce machine-specific drift. In OpenKB workflows they also align with [[concepts/deterministic-validation]] and [[concepts/source-driven-regeneration]], since the KB is expected to be rebuilt from trusted inputs rather than patched in place.

## Relationship to Other Concepts

Path safety overlaps with, but is distinct from, several related ideas:

- [[concepts/filesystem-validation]] focuses on checking the state and suitability of files and directories before acting.
- [[concepts/safe-automation]] is broader and includes protective behavior beyond path handling.
- [[concepts/local-vs-shared-configuration]] matters when tools create local-only files that should stay inside repo-scoped boundaries.
- [[concepts/kb-root-staging]] applies path safety specifically to OpenKB staging and ingestion so generated registries do not capture unsafe absolute paths.
- [[concepts/single-source-of-truth]] is supported when path-safe aliases point to canonical files instead of duplicating content in uncontrolled locations.
- [[concepts/validation-vs-health-reporting]] helps distinguish strict boundary checks from softer status and lint reporting in the KB lifecycle.
- [[concepts/explicit-provider-routing]] and [[concepts/consent-first-tooling]] capture the data-flow side of the same discipline.
- [[concepts/preflight-checks]] describes the broader class of early checks that make boundary failures visible before work proceeds.
- [[concepts/skill-scaffolding]] describes the broader pattern of generating a new skill structure from a starter template.
- [[concepts/kebab-case-normalization]] captures the naming style used when turning human titles into stable directory names.
- [[concepts/directory-bootstrap]] covers creating a predictable initial directory structure from a constrained entry point.

## Practical Takeaway

A path-safe script treats repository and KB boundaries as hard constraints. The source documents demonstrate this in two complementary ways: one allows local alias creation only when the alias stays inside the repository, and the other requires staged knowledge inputs to remain inside the KB root so metadata stays relative, portable, and private. The OpenKB source-pack builder extends that same discipline across repository inventory, manifest generation, bundle staging, and oversized-file splitting, while the lifecycle, privacy, and prerequisite checks add disclosure, explicit routing, workspace writability, and config-consistency requirements. The skill initializer applies the pattern to local skill creation by normalizing names, validating the target scope, and limiting optional subdirectories. Together, they show that path safety is a foundational design rule for reliable developer tooling, privacy-conscious ingestion, and local adaptation workflows.

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__graphify__references__extraction-spec-md]]

See also: [[summaries/agents__skills__openkb__references__commands-md]]

## Related Documents
- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]