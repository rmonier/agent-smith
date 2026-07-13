---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Deterministic repo-to-KB staging that also enables orphan reconciliation."
---

# Source Pack Staging

Source pack staging is the process of turning a Git repository into a deterministic, OpenKB-compatible input pack for ingestion, validation, and later reconciliation. It converts tracked source material into staged documents with stable hashes, provenance metadata, and a manifest that downstream tools can validate and use to detect orphans. In the OpenKB workflow, it is the deterministic bridge between repository state and the compiled knowledge base.

This concept is embodied by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], which builds the staged pack under `okf/.okf-build/input/` and records the result in a manifest. The same staging rules are relied on by [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]], which uses the manifest or a git-derived fallback to decide which KB documents have become orphans and whether they should be removed as deleted, renamed, or merely deselected. The broader workflow also requires the repo root `.graphifyignore` to exclude `okf/`, since the wiki must stay out of the repo graph and avoid self-reference loops.

## Core Goals

- Preserve all selected source content without silent truncation.
- Produce stable output bytes so unchanged inputs do not re-ingest needlessly.
- Attach provenance data to every staged item.
- Keep staging compatible with [[concepts/compiled-knowledge-bases]] and [[concepts/staging-manifests]].
- Avoid feedback loops, self-reference, and other forms of self-referential ingestion.
- Support later reconciliation by keeping staged names, source paths, and registry expectations aligned.
- Keep the repository agent-ready by feeding deterministic input into the OpenKB pipeline rather than hand-editing compiled pages.
- Respect the build workflow’s requirement that prerequisite checks, toolchain vendoring, and ignore-file setup happen before ingestion begins.
- Enable safe orphan retraction by giving cleanup tools a stable source-path and hash trail.

## How It Works

The staging script walks tracked files from Git, filters them with path heuristics, and writes synthetic OpenKB source pages into the build area. It also creates a repository snapshot page listing tracked files and can stage a graph report when it is safe to do so. The workflow assumes Git history is available, because the source pack builder stages `git ls-files` output and uses last-touch commits for provenance.

Key steps include:

- Enumerating tracked paths with `git ls-files`.
- Inferring last-touch commits from `git log` for provenance.
- Skipping internal build, cache, and transient directories.
- Selecting repository files that are likely to carry durable knowledge, such as docs, workflows, manifests, and source code.
- Emitting per-file staged pages or grouped bundles depending on configuration.
- Splitting oversized files into full-content parts rather than cropping them.
- Writing a JSON manifest that maps each staged document back to its source path.
- Staging deterministic input under `okf/.okf-build/input/` instead of writing generated content directly into `okf/raw/` or `okf/wiki/`.
- Respecting the workflow’s rule that `GRAPHIFY_NO_BACKUP=1 graphify update . --force` runs before source pack creation when Graphify is available.

The staging rules are intentionally mirrored by orphan cleanup tooling. [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]] prefers the manifest when present and falls back to re-deriving the expected staged names from the repository when the manifest is absent. That keeps the pack builder and the retraction path in sync about which repository file maps to which KB document.

The cleanup script also distinguishes document states rather than treating every mismatch as a hard delete. A missing staged page may be a true deletion, a rename detected by matching content hashes, or a deselection where the source file still exists but no longer matches the current selection rules. It also protects pseudo-documents like `repo-snapshot` and `graphify-report`, which are regenerated artifacts and must never be treated as orphans.

The workflow also insists that `.gitattributes` normalization be installed from the shared template so staged bytes remain deterministic across environments. If a repository already has a conflicting rule, the workflow requires a human decision rather than silently overriding the existing normalization choice.

## Important Design Ideas

### [[concepts/deterministic-builds]]
Staged output is intended to be reproducible. The script avoids embedding changing values like the current `HEAD` commit in snapshot content, because that would churn hashes and cause unnecessary re-ingestion. Deterministic staging is what makes incremental compilation and hash-registry coherence work.

### [[concepts/provenance-tracking]]
Each staged document includes source metadata such as source path, source kind, source hash, and often the last commit that touched the file. This makes the pack auditable and easier to reconcile later. The workflow also treats external URLs as evidence only, preserving provenance boundaries between repository sources and outside references.

### source selection
Staging is selective rather than exhaustive. The script favors repository paths that usually represent durable knowledge sources, such as `README` files, docs folders, CI workflows, build descriptors, and source directories. This aligns staging with [[concepts/documentation-source-priority]] and keeps incidental files from overwhelming the knowledge base.

### content splitting
When a file exceeds the size budget, it is split into multiple documents instead of being cropped. Markdown splits at heading boundaries, while code splits at layout boundaries so the content remains complete and deterministic. This preserves evidence while preventing truncation-induced knowledge loss.

### [[concepts/source-bundling]]
Optional bundle mode groups non-markdown files into per-directory digest documents. This changes the unit of ingestion from individual files to directory-based bundles, which can be useful for large repositories.

### [[concepts/self-reference-control]]
The script checks graph reports for signs that they reference the KB output tree. If the report appears to describe generated wiki content, it is skipped to avoid self-referential ingestion loops. The same self-reference policy applies at the repo level: the wiki must not be pulled into the graph as a source of itself.

### [[concepts/manifest-authoritative-reconciliation]]
When a fresh manifest exists, it is treated as the authoritative description of staged names. Orphan cleanup uses that manifest directly and only falls back to git-based derivation when the manifest is missing. If the manifest and repository disagree, the cleanup tool emits an advisory instead of silently guessing, because the mismatch may indicate stale staging or helper drift.

### [[concepts/orphan-retraction]]
Source pack staging does not remove stale KB pages itself, but it establishes the names and provenance needed for later cleanup. The orphan retraction tool uses the staged source metadata to distinguish true deletions from renamed files, and it refuses to treat pseudo-documents like `repo-snapshot` and `graphify-report` as orphans because they are regenerated artifacts rather than repository-backed sources.

### rename detection
The retraction script tries to tell a rename from a deletion by comparing the old content hash against newly staged input. This lets the workflow retract the obsolete KB page while preserving empty shared pages when a replacement document will repopulate them. That distinction is critical when a `git mv` turns into delete-plus-add at the repository level.

### safety guardrails
The staging pipeline is designed to support safe automation. Downstream reconciliation applies a mass-orphan guard, treats deselected files conservatively, and uses `openkb remove` as a deterministic inverse rather than a free-form mutation path. Those guardrails depend on staging being consistent, because the orphan detector must be able to trust the staged pack’s naming and source-path conventions.

### workflow ordering
The broader build workflow places staging after prerequisite checks, ignore-file setup, and optional Graphify refresh, but before OpenKB ingestion. That ordering ensures the staged pack reflects the current repository structure and that later validation runs against the same structure the wiki was compiled from.

## Outputs

The staging process produces several outputs:

- a repository snapshot document containing a tracked-file inventory
- optional graphify report staging when it is safe to do so
- staged source documents or bundles in `okf/.okf-build/input/repo-files`
- a manifest JSON file under `okf/.okf-build/manifests`

These outputs support ingestion into OpenKB and later reconciliation with the source repository. They also provide the basis for deterministic orphan detection when source files are deleted, moved, or deliberately deselected. The workflow treats the source pack as build input only; generated wiki content lives in `okf/wiki/` and must not be staged back into the graph.

## Operational Tradeoffs

Source pack staging balances completeness, determinism, and safety:

- It preserves content by splitting rather than truncating important oversized sources.
- It reduces churn by using stable hashing and avoiding volatile metadata.
- It can regroup files into bundles for scalability, but that changes staging granularity and should be chosen deliberately.
- It warns when staged bundles may be too large for downstream compilation.
- It provides the naming and provenance needed for orphan cleanup, but retraction is handled by a separate reconciliation step.
- It fits into the larger agent-ready repository workflow, where skills drive actions, the wiki stores durable context, and `AGENTS.md` stays a concise orientation layer.
- It depends on local-only build artifacts staying out of version control, including `okf/.okf-build/`, `okf/output/`, and `okf/wiki/reports/`.

## Related Concepts

- [[concepts/repository-ingestion]] for the broader pipeline that consumes repository content.
- [[concepts/staging-manifests]] for the machine-readable inventory of staged items.
- [[concepts/source-provenance]] for how staged outputs retain source identity.
- [[concepts/document-normalization]] for the text normalization used before hashing.
- [[concepts/path-based-validation]] for the path heuristics that control selection and skipping.
- [[concepts/knowledge-base-discovery]] for using repository structure as a knowledge source.
- [[concepts/safe-automation]] for the script’s cautious handling of risky inputs and loops.
- [[concepts/orphan-retraction]] for the inverse operation that removes KB pages after source deletion.
- [[concepts/hash-registry-coherence]] for keeping registry state aligned with repository state.
- [[concepts/rename-vs-delete-detection]] for distinguishing true deletions from file moves.
- [[concepts/agent-context-layering]] for the separation between skills, wiki context, and `AGENTS.md` orientation.
- [[concepts/agent-ready-context-skill]] for the governing workflow that makes this staging step part of an agent-ready repository.
- [[concepts/knowledge-lifecycle-governance]] for the ordering, validation, and curation rules that keep staged knowledge reliable.

## Why It Matters

Source pack staging is the handoff point between a repository and the knowledge base. If this step is unstable, incomplete, or self-referential, the rest of the OpenKB pipeline becomes noisy and expensive. Done well, it provides a clean, deterministic, provenance-rich foundation for ingestion, validation, incremental regeneration, orphan reconciliation, and the broader agent-ready context workflow.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/repo-snapshot]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
