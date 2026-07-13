---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Explicit rules classify content from observable signals for triage and staging."
---

# Heuristic Classification

Heuristic classification is the use of simple, explicit rules to sort, identify, or prioritize items based on observable signals rather than deep semantic understanding. In this wiki, it describes tooling that detects likely procedural, operational, or knowledge-relevant material by scanning for patterns such as action verbs, file paths, tool names, structural markers, and exclusion cues.

## Core idea

A heuristic classifier does not try to fully understand a document. Instead, it applies practical rules that are cheap to run, easy to inspect, and easy to adjust. This makes the approach useful in repository tooling, especially when the goal is triage, suggestion, selection, or ranking rather than final authoritative judgment.

In [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]], the classifier works by:

- scanning Markdown pages in an OKF bundle
- skipping administrative or raw-source areas
- matching predefined action-oriented regex patterns
- excluding likely conceptual pages through skip-context keywords
- assigning scores to pages based on match counts
- converting high-scoring pages into suggested skill candidates

In [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], heuristic classification appears in a different but related form: repository files are selected for staging based on path prefixes, filenames, and extensions rather than content understanding. The script uses explicit inclusion and exclusion rules to decide which tracked files are likely to be valuable for knowledge ingestion and how to label them as `markdown`, `text`, `code`, or `other`.

Together, these examples show heuristic classification supporting both [[concepts/skill-based-automation]] and [[concepts/repository-ingestion]]: one workflow identifies documents that look operational enough to become reusable actions, while the other identifies files that look important enough to stage into the knowledge pipeline.

## Signals used in practice

The source documents show several common heuristic signal types.

### Positive signals

Positive signals increase confidence that an item belongs in a target category. In the skill suggestion script, these include:

- action verbs such as run, validate, generate, build, sync, and migrate
- tool references such as git, docker, kubectl, helm, uv, and python
- repeated operational language that raises the page score
- code fences, which can indicate implementation-oriented content

In the source pack builder, positive signals are more repository-oriented:

- filenames such as `README`, `Dockerfile`, `Makefile`, `package.json`, `pyproject.toml`, `go.mod`, and `Cargo.toml`
- path prefixes such as `docs/`, `src/`, `.github/workflows/`, and `.agents/skills/`
- infrastructure and deployment markers such as compose files, Helm files, and Terraform files
- file extensions that indicate likely `markdown`, `text`, or `code` content

These signals push the classifier toward treating a file or page as useful operational material rather than noise.

### Negative signals

Negative signals reduce confidence or exclude content from consideration. The skill suggestion script uses terms like architecture, decision, evidence, overview, concept, and external documentation as skip-context markers when no code blocks are present. This helps preserve [[concepts/context-action-separation]] by avoiding the conversion of explanatory context into action skills too early.

The source pack builder uses exclusion heuristics at the path level. It skips areas such as `okf/`, `graphify-out/`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, and `.venv`. These rules reflect a judgment that generated artifacts, transient caches, and local runtime directories are poor staging candidates.

A more specialized negative heuristic appears in the Graphify report handling: if the report contains repeated references to generated KB paths under `okf/`, the script refuses to stage it to avoid self-referential ingestion. This connects heuristic classification to [[concepts/self-reference-control]] and [[concepts/generated-content-governance]].

### Structural signals

The classifier also relies on document and repository structure:

- file location inside or outside reserved areas
- heading and metadata extraction for candidate names
- repository path filtering for `sources/`, `reports/`, `index.md`, `log.md`, and `AGENTS.md`
- extension-based source kind detection
- directory depth grouping when source files are bundled

This connects heuristic classification with [[concepts/reserved-wiki-files]], [[concepts/frontmatter-metadata]], [[concepts/source-bundling]], and [[concepts/repository-ingestion]].

## Why this approach is useful

Heuristic classification is valuable when:

- the corpus is large enough that manual review is expensive
- the categories are approximate and operational
- the system needs to provide suggestions or selection, not enforce truth
- maintainers need transparent logic they can tune quickly

In the skill suggestion workflow, heuristics help bridge curated knowledge and automation opportunities. Rather than requiring an LLM or a full parser, the script produces candidate skills from visible patterns in repository knowledge. This fits well with [[concepts/llm-free-knowledge-bootstrap]], [[concepts/offline-first-workflows]], and [[concepts/privacy-preserving-tooling]].

In the source pack workflow, heuristics help stage the most knowledge-relevant repository material without needing semantic analysis of the whole codebase. The result is a deterministic, inspectable selection layer that supports [[concepts/evidence-staging]], [[concepts/kb-root-staging]], and [[concepts/deterministic-builds]].

## Tradeoffs and limits

Heuristic classification is intentionally shallow. Its strengths come with known limitations:

- false positives when conceptual documents contain many action words or files match broad naming conventions
- false negatives when useful procedural content uses uncommon vocabulary or nonstandard paths
- sensitivity to wording changes in titles, body text, filenames, or directory layout
- dependence on manually curated pattern lists, extensions, and skip terms
- brittleness when repository conventions differ from the classifier's assumptions

Because of these limits, heuristic classification is best treated as a discovery or staging aid rather than a final decision-maker. The skill suggestion script reflects this by printing suggestions and evidence rather than directly generating or adopting skills. The source pack builder reflects it by using explicit path-based inclusion rules that are easy to audit and revise. These designs support [[concepts/human-in-the-loop-review]] and [[concepts/skill-governance]].

## Relationship to naming and scoring

The source documents also show how classification often extends beyond detection into normalization, labeling, and ranking:

- scores aggregate repeated matches across pages
- titles or headings become candidate labels
- slugification converts labels into stable action-style identifiers
- a `manage-` prefix is added when no action verb is present
- file paths are converted into safe staged names using separator replacement
- file extensions and well-known filenames determine source-kind labels

This links heuristic classification to [[concepts/naming-normalization]], [[concepts/project-scaffolding]], and [[concepts/document-normalization]] because the classifier not only finds candidates but prepares them for downstream tooling.

## Design pattern in this wiki

Within this knowledge base, heuristic classification appears as a practical pattern for extracting operational value from documentation and repositories without collapsing all context into automation or trying to fully interpret every source. It works best when paired with:

- [[concepts/context-action-separation]] to keep conceptual material distinct from executable tasks
- [[concepts/action-oriented-documentation]] to improve discoverability of actionable pages
- [[concepts/quality-gates]] to validate outputs before adoption
- [[concepts/skill-governance]] to ensure suggested skills are reviewed and managed deliberately
- [[concepts/deterministic-builds]] to keep heuristic staging outputs stable across runs
- [[concepts/provenance-tracking]] to preserve traceability when heuristics decide what enters the KB

## See also

- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
- [[concepts/action-oriented-documentation]]
- [[concepts/context-action-separation]]
- [[concepts/skill-based-automation]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/naming-normalization]]
- [[concepts/project-scaffolding]]
- [[concepts/quality-gates]]
- [[concepts/repository-ingestion]]
- [[concepts/reserved-wiki-files]]