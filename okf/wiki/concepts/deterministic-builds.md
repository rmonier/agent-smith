---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/graphify-report.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Builds that emit identical output bytes for unchanged meaningful inputs."
---

# Deterministic Builds

Deterministic builds are build or staging processes that produce the same output bytes whenever the same meaningful inputs are provided. Outputs should change only when source content or intended configuration changes, not because of volatile metadata, timestamps, serialization order, platform-specific line endings, or unrelated repository activity.

In this repository's agent-ready workflow, deterministic builds are part of a larger separation of responsibilities: skills define repeatable actions, the OKF wiki stores durable compiled context, and AGENTS.md stays an orientation layer. The agent-ready-context skill treats deterministic staging as a core requirement for making OpenKB-based repository knowledge stable, reviewable, and safe to regenerate. That connects this concept to [[concepts/agent-ready-context]], [[concepts/compiled-knowledge-bases]], [[concepts/documentation-layer-separation]], and [[concepts/context-action-separation]].

This concept is central to `summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py`, which implements a deterministic staging pipeline for `entities/openkb`. It is also a defining requirement of the repository workflow in `summaries/agents__skills__agent-ready-context__references__workflow-md`, where deterministic staging is what makes incremental ingestion, validation, review, and regeneration trustworthy.

## Why deterministic builds matter

Deterministic output supports several important goals:

- predictable hashing and deduplication
- easier detection of real content changes
- less unnecessary recompilation or re-ingestion
- more reliable provenance and audit trails
- better fit for offline and automation-heavy workflows
- stable review surfaces for human-in-the-loop validation

In the OpenKB context, stable staged bytes matter because content is deduplicated by hash. If a pipeline injects changing timestamps, current-branch state, or repository-wide commit metadata into every file, the system sees those files as new even when their substantive content is unchanged. That creates avoidable churn in ingestion and downstream compilation.

The workflow document makes this stronger: determinism is not only a convenience for hashing, but a precondition for incremental knowledge builds. The graph step, source-pack step, and ingest step are ordered so unchanged repository material stays byte-stable and only genuinely changed content is reconsidered by the knowledge base. This makes deterministic builds a practical foundation for [[concepts/incremental-compilation]], [[concepts/hash-registry-coherence]], [[concepts/repository-ingestion]], [[concepts/source-driven-regeneration]], and [[concepts/deterministic-validation]].

## How the source documents apply the concept

`summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py` provides a concrete implementation of deterministic builds for repository ingestion, and `summaries/agents__skills__agent-ready-context__references__workflow-md` explains why those design choices matter at the workflow level. The skill document itself reinforces the same pattern by insisting on deterministic staging under `okf/.okf-build/input/`, OpenKB ingestion as a separate step, and explicit protection against self-referential loops and registry drift.

### 1. It avoids embedding volatile repository state

The staging pipeline explicitly avoids placing the current Git HEAD commit into the repository snapshot. That choice prevents all staged output from changing after every commit, including commits unrelated to the staged files.

Instead, it records the last commit that touched each file by scanning Git history and mapping each tracked path to its newest modifying commit. This preserves useful provenance while limiting output changes to files whose actual history changed. The workflow document calls out this rule directly: each staged file's `source_commit` should reflect the file's own last change, never a global commit stamp. This connects deterministic builds to [[concepts/provenance-tracking]] rather than treating them as competing goals.

### 2. It normalizes file content before hashing

The script decodes text as UTF-8 with replacement and converts all line endings to `\n`. This means the same logical document produces the same hash even if it was edited on different platforms with different newline conventions. The hash is then computed from the normalized text, so byte identity follows canonicalized content rather than local editor behavior. This is closely related to [[concepts/document-normalization]] and [[concepts/line-ending-normalization]].

The workflow reinforces this with repository-level controls: `.gitattributes` should be installed or merged so LF normalization remains stable, and users are advised to renormalize tracked files when normalization policy changes. Deterministic builds therefore depend not only on script behavior, but also on repository hygiene through [[concepts/git-attributes]] and [[concepts/document-normalization]].

### 3. It strips run-dependent generated metadata

When staging the Graphify report, the script removes timestamp lines and date suffixes from report headings before hashing and writing the staged document. Without that step, a generated report could produce a new hash every day even if the structural analysis itself had not changed.

The workflow extends this idea by requiring `GRAPHIFY_NO_BACKUP=1` during routine graph refreshes, preventing dated backup directories from introducing extra churn into the repository context. Together, these choices show that deterministic builds require generated artifacts to be cleaned of run-specific noise before they participate in downstream knowledge workflows. This is a useful example of deterministic handling of generated artifacts and connects to [[concepts/generated-content-governance]] and [[concepts/knowledge-graph-analysis]].

### 4. It orders output predictably

The script sorts tracked files before inventory generation, sorts bundle groups and bundle members, and sorts the final manifest by `source_path` and `staged_path`. This ensures that logically identical collections serialize identically across runs.

Predictable ordering is a small but essential part of deterministic builds because semantically identical collections can otherwise emit different byte sequences. At the workflow level, this predictable ordering supports reliable review and stable diffs, making it easier to see whether a change reflects real repository evolution or only serialization noise.

### 5. It writes normalized staged files

The script writes UTF-8 output with normalized newlines and ensures a trailing newline in generated files. It also rebuilds staged documents from normalized text rather than copying source bytes directly. These low-level formatting rules help keep byte output consistent and reduce false-positive changes.

The workflow's validation and re-ingestion model depends on this stability: unchanged staged files should remain byte-identical across runs so the hash registry can skip them and so review effort stays focused on meaningful changes.

### 6. It makes deterministic scope selection explicit

The script applies fixed selection and skip rules when deciding what to stage. It selects repository-relevant material such as `README`, `docs/`, CI configuration, build manifests, `src/`, and `.agents/skills/`, while skipping transient caches, virtual environments, `graphify-out/`, and the `okf/` tree.

Determinism depends not only on stable serialization but also on stable inclusion rules. Explicit scope selection prevents accidental input drift caused by temporary directories, generated scratch data, or previously compiled knowledge-base output. This aligns with [[concepts/kb-root-staging]] and [[concepts/repository-ingestion]].

The workflow also requires prerequisite checks before any major build step, including validation of Git, `uv`, and Python 3.11+ availability, and it treats missing optional tools as a consent-first bootstrap decision rather than a silent fallback. That makes the deterministic pipeline part of a larger [[concepts/preflight-checks]] and [[concepts/consent-first-tooling]] model.

### 7. It keeps bundle behavior content-based

When `--bundle-depth` is enabled, the script groups selected files by directory prefix, computes a bundle hash from the normalized content of member files, and emits sections that record each member's hash and last-touch commit. Bundling changes staging granularity, but the grouping logic and bundle serialization remain deterministic.

This is important because aggregation can easily introduce nondeterminism if member order, path grouping, or serialization layout is unstable. Here, bundle formation is explicit, sorted, and based on normalized content, which keeps [[concepts/source-bundling]] compatible with deterministic builds.

### 8. It keeps the wiki out of the graph

The workflow requires `.graphifyignore` to exclude the KB root, and the source-pack builder refuses to stage a graph report that references `okf/`. That guard prevents the compiled wiki from feeding back into the repo graph that is used to regenerate it.

This is a determinism rule as much as a provenance rule. If the wiki were included in the graph, every ingest could perturb the graph report, which would then perturb the source pack, which would then perturb the wiki again. Excluding the KB root keeps the build acyclic and stable, supporting [[concepts/self-reference-control]], [[concepts/kb-root-staging]], and [[concepts/compiled-knowledge-bases]].

### 9. It distinguishes staging from ingesting

The workflow treats source-pack creation as deterministic staging only; the knowledge base is not updated until `openkb add` runs. That separation matters because it gives the build a stable intermediate artifact that can be inspected, validated, and reused without implying that the wiki has already changed.

This boundary is one reason deterministic builds are useful in OpenKB: stable staging makes it possible for hash-registry deduplication, validation, and post-generation review to operate on a reproducible snapshot rather than on moving input state. The skill document also makes the separation explicit by warning against writing generated files directly into `okf/raw/` or `okf/wiki/`, requiring staged input under `okf/.okf-build/input/`, and describing the wiki as compiled context rather than the source of truth. That design fits [[concepts/source-pack-staging]], [[concepts/hash-registry-coherence]], [[concepts/repository-transformation-pipelines]], and [[concepts/source-driven-regeneration]].

### 10. It supports the full agent-ready context workflow

The skill frames deterministic builds as part of a broader operational surface that includes prerequisite checks, graph generation, source-pack staging, OpenKB initialization, ingestion, linting, validation, and optional harness/tooling context management. That larger workflow depends on stable intermediate artifacts so each stage can be reviewed independently and repeated without incidental drift.

The same document also ties determinism to consent-first tooling and explicit provider routing: `uv` is required for script execution, optional tools are adopted only with user approval, and web refreshes are treated as untrusted evidence rather than executable instructions. This widens deterministic builds from a purely technical property into a governance practice for repeatable agent operations, connecting to [[concepts/tooling-consent-and-pin-management]], [[concepts/provenance-aware-tool-installation]], [[concepts/vendor-skill-adoption]], and [[concepts/web-evidence-ingestion]].

## Design patterns within deterministic builds

Deterministic builds often rely on a set of recurring patterns, all visible in the source documents:

- normalize inputs before hashing or packaging
- exclude transient caches and generated scratch directories
- avoid embedding current time or global mutable state
- preserve provenance using content-relevant metadata rather than run metadata
- serialize outputs in a stable order
- make selection rules explicit and repeatable
- keep generated analysis from recursively consuming its own output
- keep output naming and formatting stable across runs

The workflow's self-reference rule adds an important pattern: deterministic systems must avoid feedback loops. The source-pack script includes a loud guard that refuses to stage a Graphify report if it repeatedly references paths under `okf/`, because that indicates the graph was built from compiled KB output rather than from source material. Excluding `okf/` from graph analysis is not just a cleanliness preference; it protects the build from infinite churn where generated wiki changes would alter the graph, which would alter the report, which would alter the wiki again. This makes deterministic builds closely related to [[concepts/self-reference-control]] and [[concepts/kb-root-staging]].

These patterns also support [[concepts/repository-ingestion]], because ingestion pipelines are especially sensitive to noisy changes.

## Relationship to adjacent concepts

Deterministic builds overlap with, but are not identical to, several related ideas:

- [[concepts/document-normalization]] focuses on canonicalizing content so semantically identical inputs are treated consistently.
- [[concepts/provenance-tracking]] focuses on retaining trustworthy origin information without introducing unnecessary churn.
- [[concepts/incremental-compilation]] benefits from deterministic outputs because stable hashes make it easier to skip unchanged work.
- [[concepts/source-driven-regeneration]] relies on outputs being regenerated from source in a repeatable way.
- [[concepts/repository-ingestion]] uses deterministic staging to avoid reprocessing unchanged repository material.
- [[concepts/deterministic-validation]] complements this concept by checking results with stable, non-LLM gates after generation.
- [[concepts/validation-vs-health-reporting]] clarifies that deterministic build guarantees and deterministic validation are stronger operational controls than advisory health reports.
- [[concepts/consent-first-tooling]] and [[concepts/preflight-checks]] describe the operational envelope that keeps deterministic automation safe to run.

## Practical implications

For repository-to-knowledge pipelines, deterministic builds improve both efficiency and trustworthiness. They reduce needless updates, make hash-based deduplication more effective, and help operators understand when a change reflects real source evolution rather than tool noise.

The source-pack implementation shows that this requires attention to details that are easy to dismiss as minor: line ending normalization, stable manifest ordering, run-independent report cleanup, file-level provenance, explicit scope rules, and suppression of volatile generated fields. These details are what turn reproducibility from an aspiration into an operational property.

The workflow document also shows a broader implication: deterministic staging is what makes the correction loop and review process tractable. When generated wiki output changes only in response to meaningful source or graph changes, reviewers can investigate diffs as evidence of actual repository evolution instead of sorting through incidental rebuild churn. That makes deterministic builds an enabling condition for [[concepts/human-in-the-loop-review]], [[concepts/okf-validation]], and [[concepts/executable-validation]].

In the OpenKB workflow described by `summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py` and `summaries/agents__skills__agent-ready-context__references__workflow-md`, deterministic builds are not just a build-quality preference; they are a core operational requirement for stable ingestion behavior.

## Takeaway

Deterministic builds ensure that repeated runs over the same meaningful inputs produce the same staged artifacts. In this codebase, that principle is implemented through content normalization, stable ordering, selective provenance metadata, explicit scope rules, suppression of volatile generated fields, deterministic bundling, and active protection against self-referential churn, making the repository staging process more efficient, predictable, and compatible with `entities/openkb`.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]