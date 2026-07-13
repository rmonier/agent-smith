---
type: "Concept"
sources: ["summaries/graphify-report.md"]
description: "How tightly a document stays focused on one clear purpose."
---

# Documentation Cohesion

Documentation cohesion is the degree to which a page's sections, headings, examples, and references reinforce one clear purpose instead of collecting loosely related topics. A cohesive page has a recognizable center of gravity: readers can tell what belongs there, what does not, and how the page fits into the larger documentation system.

High cohesion makes documentation easier to navigate, maintain, and trust. Low cohesion makes it harder to see what belongs together, where to look next, and whether a page should be split into smaller modules.

## Why it matters

Cohesive documentation improves:
- reader orientation and faster lookup
- cleaner boundaries between overview, procedure, policy, and reference material
- maintainability when content changes
- better structural signals for tools that analyze repositories, such as graph-based mapping
- more reliable hub-and-spoke navigation through indexes and related pages

In practice, documentation cohesion is closely related to [[concepts/documentation-architecture]], [[concepts/repo-navigation]], and [[concepts/index-based-discovery]]. It also supports [[concepts/progressive-disclosure]] by letting overview pages stay broad without becoming dump sites for unrelated material.

## What low cohesion looks like

A low-cohesion document often:
- mixes multiple purposes in one file
- collects topics that are only weakly related
- becomes a default dumping ground for guidance, rules, edge cases, and examples
- has many headings that connect weakly to each other
- is useful as a broad entry point but weak as a focused module

This does not always mean the content is bad. A broad orientation page can be intentionally wide in scope. The issue is whether that breadth starts to work against clarity, maintainability, or modular reuse.

## Evidence from [[summaries/graphify-report]]

The [[summaries/graphify-report]] for the `agent-smith` corpus uses graph structure to identify cohesion problems in repository documentation. It reports 472 nodes and 550 edges across 54 communities, with 45 communities shown and 9 thin communities omitted, which is large enough that structural analysis adds value. The report also highlights 234 isolated nodes, suggesting uneven integration across the documentation graph.

The report's most relevant cohesion findings are:
- `README.md` is a major community hub but has very low cohesion.
- `Skill Creator` is another large, weakly interconnected cluster.
- `What You Must Do When Invoked` is also flagged as a low-cohesion community.
- Several other clusters around build, validation, and tooling documentation are dense, but many peripheral nodes remain isolated.

The report explicitly suggests asking whether large documents should be split into smaller, more focused modules. That recommendation follows from structural evidence:
- the `README.md` community is large and weakly interconnected
- `Skill Creator` spans many subtopics with limited internal cohesion
- `What You Must Do When Invoked` groups many operational subtopics under one umbrella
- the graph contains many isolated nodes, indicating missing links or undocumented components

This makes documentation cohesion a measurable structural concern rather than only a stylistic judgment. In [[summaries/graphify-report]], low cohesion is inferred from weak internal connectedness within a document-centered community, not just from subjective reading.

## Cohesion in graph terms

In a repository graph, documentation cohesion can be approximated by how strongly the concepts, sections, and references within a document connect to one another.

Signs of stronger cohesion:
- a document forms a compact community
- its headings and subtopics are strongly linked
- the page has a clear central theme with supporting details
- the page acts as a focused module rather than a general catch-all

Signs of weaker cohesion:
- a document is large but internally sparse
- many sections connect only through the file container rather than through shared ideas
- the page acts as a storage surface for unrelated concerns
- the document becomes a bridge between many topics without enough internal structure

This connects documentation analysis to [[concepts/knowledge-graph-analysis]], [[concepts/repository-overview-generation]], and [[concepts/graph-structure-analysis]].

## Practical interpretation

Low cohesion does not automatically require splitting a file. A document may be intentionally broad if it serves as onboarding or a top-level map. The better question is whether readers can still distinguish:
- what the document is for
- what belongs elsewhere
- how to move from overview to task-specific detail

When cohesion is too low, useful responses include:
- split broad pages into purpose-specific modules
- move procedures into dedicated references
- separate policy from walkthrough content
- improve cross-linking between overview and detailed pages
- use indexes or hub pages instead of overloading a single document

These responses align with [[concepts/progressive-disclosure]], [[concepts/action-oriented-documentation]], and [[concepts/tooling-context-pages]]. They also support healthier documentation boundaries and make repository graphs easier to interpret.

## Relationship to other documentation qualities

Documentation cohesion is related to, but distinct from:
- [[concepts/documentation-architecture]]: the overall system of pages and their roles
- [[concepts/link-directionality]]: how pages point readers toward overview or detail
- [[concepts/generated-content-governance]]: rules for how generated or maintained docs are organized
- [[concepts/knowledge-linking-and-citations]]: how supporting pages connect evidence and claims
- [[concepts/documentation-gaps]]: missing links or missing pages that can make cohesion appear weaker than it really is

A documentation system can have strong architecture overall while still containing some low-cohesion pages. Cohesion is a page- or cluster-level quality inside the larger information structure.

## Takeaway

Documentation cohesion is a structural measure of how well a document holds together around a single purpose. In [[summaries/graphify-report]], it is used to identify overloaded documentation hubs whose sections are weakly connected, suggesting opportunities to improve clarity, modularity, and navigation across the repository.