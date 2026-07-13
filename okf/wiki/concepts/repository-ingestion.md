---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Selective, provenance-rich conversion of repository files into stable ingestible inputs."
---

# Repository Ingestion

Repository ingestion is the process of turning a source code repository into structured, traceable inputs that a knowledge system can import and reason over. In this wiki, the concept is illustrated most directly by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], while the surrounding build workflow in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] and the governing policy in [[summaries/agents__skills__agent-ready-context__SKILL-md]] show how staged input fits into a larger OpenKB pipeline. The Graphify guidance in [[summaries/agents__skills__graphify__references__github-and-merge-md]] extends the concept from single-repository staging to cloned repositories, merged repository graphs, and multi-folder extraction boundaries.

The repository snapshot for this project reinforces that the repository already contains the kind of material ingestion is meant to organize: agent skills, reference docs, scripts, templates, policy files, and top-level project docs. That makes [[summaries/repo-snapshot]] a useful inventory example for understanding how tracked files, repository structure, and staging rules interact.

## Core idea

A repository is not ingested usefully by copying every file unchanged. Effective repository ingestion extracts the parts most relevant to understanding the system, preserves provenance, and packages them in a form that downstream tooling can process consistently. This makes repository ingestion closely related to [[concepts/evidence-staging]], [[concepts/provenance-tracking]], and [[concepts/document-normalization]].

In practice, repository ingestion usually includes:

- identifying which tracked files matter for understanding the project
- excluding generated, transient, or tool-internal output
- normalizing text so equivalent content hashes the same way
- attaching metadata such as source path, content kind, and commit provenance
- producing machine-readable inventories or manifests
- staging generated analysis and external evidence as explicit inputs rather than mixing them invisibly into repository-native content
- preserving a clear boundary between repository evidence, compiled knowledge outputs, lightweight agent orientation, and graph-analysis artifacts
- deciding whether the ingestion unit is one repository, several repositories, or several local subfolders that must later be combined

The workflow material in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] and [[summaries/agents__skills__agent-ready-context__SKILL-md]] makes an additional point: ingestion is not just file selection. It is a controlled boundary between repository evidence, optional generated analysis, external documentation, later compilation, and the broader repository context stack described by [[concepts/agent-context-layering]] and [[concepts/context-action-separation]]. The Graphify merge guidance adds that this boundary also applies to graph outputs: when several repositories or subfolders are analyzed together, each extraction run still needs a clean origin and an explicit merge step rather than an implicit shared output area.

## Why it matters

Knowledge systems built from repositories need stable and meaningful inputs. If ingestion includes volatile metadata or transient files, the system will repeatedly re-import material that has not substantively changed. If ingestion lacks provenance, it becomes harder to trace claims back to source. If ingestion is too broad, the result is noisy and expensive; if too narrow, key context is lost.

This makes repository ingestion a balancing act between completeness, relevance, and stability. It intersects strongly with [[concepts/deterministic-builds]], [[concepts/incremental-compilation]], and [[concepts/source-driven-regeneration]].

The newer policy guidance adds an operational consequence: ingestion quality affects not just compilation, but the integrity of the repository's durable context. In the agent-ready workflow, the OpenKB wiki is treated as the durable context layer, while `AGENTS.md` remains a concise orientation layer. Poor ingestion therefore pollutes the system's main knowledge surface, undermines review and validation, and weakens the single-source discipline captured by [[concepts/durable-context]], [[concepts/single-source-of-truth]], and [[concepts/documentation-architecture]].

The repository snapshot also shows why ingestion matters operationally: the repository contains multiple skill areas, supporting references, templates, and scripts that need to be understood as a structured inventory rather than as undifferentiated files. That kind of file set is exactly where selective capture, path-aware staging, and stable provenance prevent noise from overwhelming signal.

The workflow also shows that repository ingestion matters operationally: later review, validation, recompilation quality, and graph querying all depend on whether the staged inputs reflect the current repository structure, whether unchanged files remain byte-stable across runs, whether generated outputs can be traced back to committed evidence, and whether multi-repository or multi-folder analysis preserves clear source identity instead of blending origins too early.

## Pattern shown in the source document

The script summarized in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] provides a concrete repository-ingestion pattern for OpenKB, while [[summaries/agents__skills__agent-ready-context__references__workflow-md]] and [[summaries/agents__skills__agent-ready-context__SKILL-md]] define the order and policy around it. The Graphify reference in [[summaries/agents__skills__graphify__references__github-and-merge-md]] shows the same pattern applied to repository graph extraction and later merge:

- it reads tracked files from Git rather than scanning the working tree loosely
- it requires a real Git repository because the source pack depends on `git ls-files` and file-level history
- it builds a repository snapshot as an inventory of tracked files
- it selects a curated subset of files likely to explain the repository
- it skips transient and generated paths such as caches, KB output, and prior build output
- it stages each selected file as a Markdown document with structured metadata
- it can stage an optional normalized Graphify report as generated analysis
- it emits a manifest describing all staged items
- it can bundle files by directory depth when coarser ingestion units are preferred
- it writes deterministic input under the KB build area instead of directly editing compiled wiki outputs
- it supports repository graph extraction from cloned GitHub repositories, where each repository produces its own graph artifact before any merge occurs
- it treats cross-repository analysis as a second step, combining completed per-repository graph outputs rather than skipping per-repository staging
- it treats local subfolder extraction as separate ingestion runs because shared working-directory outputs would otherwise overwrite one another

The resulting staged pack is designed for OpenKB ingestion, but the conceptual pattern is broader: repository content is transformed into durable knowledge inputs that can be reviewed before import. The skill page makes that boundary explicit by prohibiting direct generation into `okf/raw/` or `okf/wiki/` during normal operation and routing repository evidence through staged input first. The Graphify merge instructions make an analogous point for graph analysis: cloned repositories and local service folders should each emit their own reviewable graph outputs before those outputs are merged into a larger combined artifact. This makes repository ingestion part of [[concepts/kb-root-staging]] and [[concepts/generated-content-governance]], not just data collection.

## Selection and curation

A key repository-ingestion decision is what to include. The source script favors files that typically carry architectural, operational, or implementation meaning, including:

- README and documentation files
- CI and workflow configuration
- container, deployment, and infrastructure files
- language and package metadata files
- source directories such as `src/`
- agent skill materials under `.agents/skills/`

The repository snapshot shows that this repository is built around those same categories, with tracked files spanning skill definitions, reference docs, scripts, templates, and repo-level policy files. That makes it a good illustration of curation around meaningful structure rather than raw volume.

It excludes directories like `okf/`, `.okf-build/`, `graphify-out/`, and common caches. The workflow and skill documents strengthen that rule by treating some exclusions as structural requirements, not just conveniences: the KB root must stay out of repository graph analysis, build/output/cache artifacts must stay out of version control and the staged evidence set, and compiled knowledge products should not flow back into their own evidence base.

This demonstrates that repository ingestion is not just capture; it is selective interpretation. The goal is to preserve explanatory evidence while filtering noise, which aligns with [[concepts/repository-overview-generation]], [[concepts/generated-content-governance]], and [[concepts/self-reference-control]].

The newer skill guidance adds another curation rule: external documentation and generated analyses may be staged, but only as explicitly labeled inputs with distinct trust and provenance handling. They are supplements to repository evidence, not invisible additions to it. The Graphify merge guidance adds a parallel curation rule for scope: if several local subfolders are being analyzed, each folder should be extracted in place so its `graphify-out/` stays local to that source boundary. If several GitHub repositories are analyzed, each repository should be cloned into its own persistent location and processed separately before merging. That sharpens the relationship between repository ingestion, [[concepts/external-documentation]], [[concepts/source-trust-levels]], [[concepts/web-evidence-ingestion]], and [[concepts/repo-scoped-graph-partitioning]].

## Provenance as a first-class concern

Repository ingestion should preserve where each staged artifact came from. In the source script, each staged document records metadata such as:

- original repository path
- inferred source kind
- content hash
- commit information for the last change touching that file

The script makes a specific provenance choice that matters for stability: it records the last-touch commit for each file instead of embedding the repository HEAD in every staged artifact. This keeps provenance attached to the evidence that actually changed, while avoiding repository-wide churn when unrelated commits land.

The workflow around that script adds an important grounding model: staged files become the evidence base for later summaries and concept pages, so each load-bearing claim in the wiki should be traceable through the citation chain back to the staged copy and then to the repository file and commit. The skill page reinforces this by warning that compiled wiki pages are not themselves evidence and should not be promoted into agent instructions without tracing the claim back through the source chain.

The Graphify reference adds a graph-specific provenance pattern. When several repositories are merged, each node in the combined graph carries a `repo` attribute so the merged artifact still exposes origin by repository. This matters because cross-repository ingestion is useful only if later querying can still separate sources, filter by origin, and trace structural claims back to the repository that produced them.

This enables downstream users and tools to connect imported knowledge back to repository evidence. Provenance is especially important when repository ingestion feeds summaries, concepts, or automated analyses. It supports trust, auditability, selective refresh, and cross-repository filtering, making it a direct expression of [[concepts/provenance-tracking]] and [[concepts/knowledge-linking-and-citations]].

## Determinism and stable refresh behavior

The source document emphasizes that repository ingestion should avoid unnecessary churn. It does this by normalizing line endings, hashing normalized text, avoiding HEAD-dependent metadata in staged outputs, and stripping volatile timestamps from generated reports.

The source script also normalizes imported Graphify report headings by removing date suffixes and drops timestamp lines entirely so daily report regeneration does not force meaningless re-ingestion. More broadly, it treats deterministic staged bytes as a requirement, not just a convenience.

The workflow and skill documents make this principle explicit at pipeline scale: the source pack is meant to be deterministic across commits, with each staged file carrying the last commit that touched that file rather than a changing repository-wide commit stamp. Unchanged files therefore produce byte-identical staged outputs, and downstream hash registries can skip re-ingesting them.

The merge guidance contributes another stability rule: each repository or subfolder should produce its own graph output in a predictable location before merge. For GitHub repositories, persistent clone locations under Graphify's managed repo cache reduce repeated setup work. For local subfolders, extraction must happen inside each scanned path because using a shared working-directory output would cause output collisions and non-deterministic overwrite behavior. Stable ingestion therefore depends not just on normalized bytes, but also on stable output boundaries and repeatable merge inputs.

The skill also highlights the operational importance of the hash registry in `okf/.openkb/hashes.json`: if the registry claims content has already been ingested while the corresponding wiki pages were lost, later add runs may silently skip rebuilding them. That makes stable inputs necessary but not sufficient; repository ingestion also has to coexist with careful registry maintenance and drift awareness.

These choices matter because ingestion often feeds a pipeline that recompiles knowledge artifacts only when source bytes change. Stable staging therefore supports [[concepts/deterministic-builds]], [[concepts/line-ending-normalization]], [[concepts/hash-registry-coherence]], [[concepts/deterministic-validation]], and [[concepts/registry-drift]].

In this sense, repository ingestion is not only about collecting material; it is about collecting it in a way that makes repeated runs predictable and efficient.

## Staged outputs as ingestion units

The script shows several useful ingestion units:

- a repository snapshot listing tracked files
- normalized copies of selected source files wrapped as Markdown
- an optional normalized Graphify report
- per-directory source bundles when `--bundle-depth` is used
- a manifest mapping source paths to staged paths and hashes
- separately materialized external evidence files when URLs are intentionally brought into the build
- per-repository graph artifacts produced from cloned repositories before cross-repository merge
- per-subfolder graph artifacts produced locally before project-level merge
- a merged graph artifact used as a later query surface once the separate extraction runs are complete

These units separate repository evidence from the downstream wiki or graph representation. That separation is important for [[concepts/tool-boundaries]] and for source-first workflows where staged inputs can be reviewed before import. The workflow and skill documents also reinforce the boundary between deterministic staging and later processing, which helps keep ingestion inspectable even when later compilation is less strictly deterministic.

The bundle mode also highlights a practical tradeoff: repository ingestion can preserve the same evidence while changing the granularity of import units. Per-file staging favors fine-grained refresh and traceability, while directory bundles reduce item count at the cost of coarser change boundaries. The Graphify merge workflow shows a similar tradeoff at a structural level: separate repository or subfolder graphs preserve origin and avoid collisions, while the merged graph provides a convenient combined surface for later query.

The skill page further clarifies that staged outputs are the sanctioned write surface for generated repository evidence. This prevents direct writes into OpenKB-owned compiled areas and preserves a clean handoff from source preparation to knowledge compilation, which is central to repository ingestion as practiced in an OpenKB pipeline.

## Relationship to repository analysis

Repository ingestion often benefits from generated structural analysis, but generated material must be handled carefully. The source script optionally includes a Graphify report and normalizes away run-dependent timestamps before staging it. It also adds a stronger safeguard: if the report appears to reference generated KB paths under `okf/` repeatedly, staging is refused to avoid a self-referential ingestion loop.

The workflow and skill documents add two more constraints: graph analysis should run before source-pack creation so staged inputs reflect the current repository structure, and the compiled wiki itself must stay out of that graph to avoid recursive churn and circular grounding. The skill also requires `.graphifyignore` coverage so the KB root never enters repository graph analysis.

The newer Graphify reference extends repository analysis beyond one repository. It describes cloning one or more GitHub repositories into managed local paths, running the full extraction pipeline on each repository independently, and then merging the resulting graph files. It also distinguishes this from multiple local subfolders inside one project, where the direct CLI must be used on each subfolder so graph outputs land inside the scanned path rather than a shared root output directory. Once a merged `graphify-out/graph.json` exists, later codebase questions can query that merged graph directly without re-extraction.

This reflects a useful rule: generated analysis can enrich ingestion, but only if it is governed so that it does not undermine stability, boundaries, or provenance. It also shows that combined analysis should be built from explicit, origin-preserving intermediate artifacts rather than from a loosely shared workspace.

That makes repository ingestion adjacent to [[concepts/generated-content-governance]], [[concepts/knowledge-graph-analysis]], [[concepts/self-reference-control]], [[concepts/graph-merging]], and [[concepts/idempotent-graph-import]].

## Design principles

From these sources, repository ingestion can be understood through several design principles:

- source-driven capture over ad hoc copying
- selective inclusion over full-tree dumping
- stable normalization over raw byte preservation
- provenance-rich metadata over anonymous text blobs
- manifest-based traceability over implicit staging
- reviewable staged artifacts over opaque ingestion steps
- explicit separation between repository evidence, external evidence, generated analysis, compiled knowledge outputs, agent orientation, and merged graph products
- ordering refresh steps so ingestion reflects the current repository before recompilation or graph merge
- self-reference safeguards so generated knowledge products do not flow back into their own evidence base
- origin-preserving multi-repository analysis over premature blending of sources
- output-directory isolation so parallel extraction targets do not clobber one another
- consent-aware handling of broad or costly downstream import operations

These principles help knowledge systems remain understandable, auditable, and efficient. They also show that repository ingestion is part of a larger documentation and compilation architecture, not an isolated preprocessing step.

## Practical takeaway

Repository ingestion is the disciplined conversion of repository evidence into stable, reviewable inputs for a knowledge system. In [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], and in the surrounding workflow defined by [[summaries/agents__skills__agent-ready-context__references__workflow-md]] and [[summaries/agents__skills__agent-ready-context__SKILL-md]], that means using Git-tracked files, curated selection rules, normalized content, per-file provenance, explicit staging for generated analysis and external evidence, self-reference controls, hash-aware refresh behavior, and deterministic ordering to create OpenKB-ready staged documents. In [[summaries/agents__skills__graphify__references__github-and-merge-md]], the same discipline is applied to repository graph analysis by cloning repositories into managed local paths, extracting graphs per repository or per local subfolder, preserving source identity in merged outputs, and treating merge as an explicit post-extraction ingestion step rather than a shortcut around source boundaries.

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__graphify__references__github-and-merge-md]]
- [[concepts/evidence-staging]]
- [[concepts/provenance-tracking]]
- [[concepts/document-normalization]]
- [[concepts/deterministic-builds]]
- [[concepts/line-ending-normalization]]
- [[concepts/hash-registry-coherence]]
- [[concepts/incremental-compilation]]
- [[concepts/repository-overview-generation]]
- [[concepts/source-driven-regeneration]]
- [[concepts/generated-content-governance]]
- [[concepts/tool-boundaries]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/self-reference-control]]
- [[concepts/source-bundling]]
- [[concepts/kb-root-staging]]
- [[concepts/context-action-separation]]
- [[concepts/durable-context]]
- [[concepts/single-source-of-truth]]
- [[concepts/registry-drift]]
- [[concepts/graph-merging]]
- [[concepts/repo-scoped-graph-partitioning]]
- [[entities/graphify]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__graphifyignore-template]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

See also: [[summaries/agents__skills__graphify__references__add-watch-md]]

See also: [[summaries/repo-snapshot]]