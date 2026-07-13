---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/graphify-report.md"]
description: "Using structural signals to find the most useful paths through a repository."
---

# Repo Navigation

Repo navigation is the practice of finding the most important files, workflows, and entry points in a codebase by following structural signals rather than reading everything linearly. In this wiki, it is closely tied to graph-style analysis, where hubs, communities, repeated packaging patterns, and weakly connected areas reveal how a repository is organized and where attention is most useful.

## Why it matters

Large repositories accumulate scripts, policies, references, templates, and documentation layers that are difficult to scan from directory structure alone. The `repo-snapshot` source makes this especially clear: even a compact tracked-file inventory shows several skill packages, repeated internal subdirectories, and a mix of top-level controls and deeper operational references. The `graphify-report` adds a more detailed structural view of the same idea: the corpus spans 54 files and about 51,771 words, with 420 nodes, 473 edges, and 49 communities. That scale makes graph structure useful for navigation, not just for analysis.

Effective navigation helps a reader or agent:
- identify the best starting points
- locate the files that coordinate major workflows
- distinguish central guidance from peripheral detail
- notice places where documentation is fragmented, overloaded, or unevenly linked

This makes repo navigation a practical complement to [[concepts/repository-overview-generation]], [[concepts/documentation-architecture]], [[concepts/index-based-discovery]], and [[concepts/graph-structure-analysis]].

## Structural signals used for navigation

A repository can be navigated through several recurring signals:
- highly connected nodes that act as hubs
- communities of related files or sections
- repeated packaging patterns such as `SKILL.md`, `references/`, `assets/`, and `scripts/`
- script entrypoints such as `main()` functions
- policy and instruction documents that bind multiple workflows together
- isolated nodes that may indicate missing links or under-integrated topics

The `repo-snapshot` document strengthens this structural view by showing that navigation is not only about graph degree but also about recognizing standardized layout conventions across modules. The `graphify-report` reinforces that point by identifying prominent hubs like `main()`, `detect_orphans()`, `names_from_git()`, `OKF quality and offline conformance baseline`, `OpenKB lifecycle for OKF maintenance`, `OpenKB repo build workflow`, `OpenKB Wiki Schema`, and `/graphify`. These signals overlap strongly with [[concepts/knowledge-graph-analysis]], [[concepts/main-structural-patterns]], [[concepts/skill-structure-conventions]], and [[concepts/cross-community-bridges]].

## Repo navigation in the Graphify report

[[summaries/graphify-report]] presents repo navigation as a graph problem. The report describes the `agent-smith` repository as a connected graph with 420 nodes, 473 edges, and 49 communities, including 41 shown and 8 thin communities omitted. Its main navigational contribution is showing which parts of the repository are central enough to serve as entry points.

The report identifies several community hubs that are especially useful for orientation:
- `README.md`
- `build_okf_source_pack.py`
- `validate_okf_bundle.py`
- `AGENTS.md`
- `OpenKB Wiki Schema`
- `What You Must Do When Invoked`
- multiple Graphify reference sections

The `repo-snapshot` summary supports this reading by showing the repository's tracked-file surface: a top-level orientation layer (`README.md`, `AGENTS.md`, ignore and attributes files), a documentation asset area, and a dense `.agents/skills/` tree containing distinct but similarly structured skill packages. Together these sources show that navigation in this repository is not purely code-first. Instead, it depends on moving among implementation scripts, process documentation, agent instructions, schema references, and repeated module conventions.

## Hubs as entry points

The report's "god nodes" highlight the abstractions with the most connections. These include `main()`, `detect_orphans()`, `OKF quality and offline conformance baseline`, `What You Must Do When Invoked`, `names_from_git()`, `OpenKB lifecycle for OKF maintenance`, `OpenKB repo build workflow`, `/graphify`, and `OpenKB Wiki Schema`.

From a navigation perspective, this means a newcomer should often begin with the most connected documents and entrypoints rather than the largest directories. The `repo-snapshot` source sharpens this advice: when a repository is organized into repeated skill packages, high-value hubs are often the files that explain or coordinate those packages, not the package directories alone. High-degree nodes tend to summarize assumptions, coordinate workflows, or dispatch to more specific components. This aligns repo navigation with [[concepts/agent-context-layering]], [[concepts/durable-context]], [[concepts/action-oriented-documentation]], and [[concepts/cross-community-bridges]].

## Communities and modular understanding

Communities provide a middle scale between individual files and the whole repository. In the source report, communities cluster around:
- README and onboarding material
- build and validation scripts
- OpenKB and OKF governance
- agent and skill guidance
- Graphify reference material

The `repo-snapshot` inventory adds a second kind of modular evidence: named skill packages such as `agent-ready-context`, `graphify`, `openkb`, `skill-creator`, and `subagent-profile-adapter` each follow a recognizable internal structure. This helps a reader build a modular mental model of the repository even before reading contents in depth. Instead of asking "what does this repo contain?" repo navigation asks "which operational area am I in, and what files define it?" This is especially useful in repositories with layered guidance, generated artifacts, and validation workflows, where [[concepts/tool-boundaries]], [[concepts/quality-gates]], [[concepts/generated-content-governance]], and [[concepts/documentation-cohesion]] all shape how work is organized.

## Low cohesion as a navigation warning

Repo navigation is not only about finding strong entry points; it also involves noticing where navigation is hard. In [[summaries/graphify-report]], the `README.md` community and the `What You Must Do When Invoked` community both have low cohesion. That suggests these documents gather multiple concerns in one place and may be harder to use as precise navigation tools.

The `repo-snapshot` source adds a complementary warning sign: a repository can look orderly at the package level while still hiding overloaded documents inside top-level guidance or large reference clusters. Low cohesion can signal:
- broad onboarding pages that should be split or reorganized
- instruction documents that mix orientation with procedures
- reference pages that cover too many separate workflows
- module layouts whose repeated structure is clear, but whose internal routing is still too broad

This connects repo navigation to [[concepts/documentation-cohesion]], [[concepts/progressive-disclosure]], [[concepts/context-action-separation]], and [[concepts/documentation-gaps]].

## Isolated nodes and coverage gaps

The report also notes 214 isolated node(s), which it treats as a documentation gap signal. For navigation, isolated nodes are important because they can represent:
- headings or sections that are not integrated into the larger documentation structure
- implementation details with no clear path from high-level guidance
- topics that may need better linking, grouping, or explanation

The `repo-snapshot` inventory suggests another useful interpretation: when the tracked-file list shows clear module boundaries and repeated conventions, isolated graph nodes may reflect weak cross-linking rather than truly peripheral importance. This makes isolated-node analysis a way to improve navigability, not just graph quality. It complements [[concepts/wikilink-integrity]], [[concepts/single-source-of-truth]], [[concepts/documentation-source-priority]], and [[concepts/knowledge-graph-feedback-loops]].

## Practical use

A good repo navigation workflow often looks like this:
1. Start at the highest-level orientation pages and top hubs.
2. Identify the community or skill package that matches the current task.
3. Use repeated structure signals such as `SKILL.md`, `references/`, `assets/`, and `scripts/` to predict where relevant material lives.
4. Follow the most connected files within that community.
5. Watch for low-cohesion documents that may need more selective reading.
6. Treat isolated nodes as possible documentation gaps, weakly linked modules, or secondary material.

In graph-heavy repositories, this approach helps a person or agent move efficiently without flattening the repository into one long reading list. It also supports [[concepts/query-expansion]], [[concepts/evidence-grounded-answering]], and [[concepts/repo-scoped-graph-partitioning]] when navigation is used to answer focused questions.

## In this knowledge base

Repo navigation is a cross-cutting concept for understanding repositories that combine code, scripts, policies, reusable skill packages, and generated documentation. In the `agent-smith` materials, it explains how graph structure and repository layout together reveal the most useful paths through the project and where those paths break down. The concept is especially relevant when working with [[entities/graphify]], [[entities/agent-smith]], [[entities/agents-md]], [[entities/openkb]], [[entities/agent-ready-context]], [[entities/skill-creator]], and [[entities/subagent-profile-adapter]].

See also: [[summaries/repo-snapshot]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__graphify__references__github-and-merge-md]]

See also: [[summaries/agents__skills__graphify__references__hooks-md]]