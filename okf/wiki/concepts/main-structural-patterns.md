---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/graphify-report.md"]
description: "Recurring whole-repository organization patterns revealed by graph and inventory analysis."
---

# Main Structural Patterns

## Definition
Main structural patterns are the recurring organization tendencies that shape how a repository is connected, navigated, and maintained at the whole-repository level. In this wiki, the concept refers to patterns visible in structural analysis and repository inventories rather than just local code style or isolated document conventions.

## What the source documents show
[[summaries/graphify-report]] and [[summaries/repo-snapshot]] together show the `agent-smith` repository as a modular, documentation-heavy, skill-centered system. The graph report provides the relational picture: 472 nodes, 550 edges, and 54 communities, with a structure dominated by documentation, workflow, validation, governance, and tooling artifacts. The repository snapshot provides the file-system picture: a tracked-file inventory centered on `.agents/skills/` packages, repeated internal conventions, top-level orientation files, and a compact docs surface.

Taken together, these sources show that:

- central hubs are documentation, workflow, validation, and governance artifacts
- the repository is organized around a repeated skill package pattern under `.agents/skills/`
- script entrypoints and validation tools are structural anchors alongside narrative docs
- top-level navigation files such as `README.md` and `AGENTS.md` frame the repository for human and agent use
- weakly connected or isolated nodes reveal places where structure is thin, fragmented, or under-linked
- a large set of isolated nodes and thin communities suggests many local support artifacts that do not yet participate in the broader knowledge graph
- graph bridges tend to connect maintenance and build orchestration rather than domain runtime behavior

This makes the repository look less like a conventional application organized around runtime modules and more like an [[concepts/agent-ready-repositories]] knowledge-and-tooling system.

## Core patterns visible in the graph and file layout

### Documentation-centered hubs
The graph report highlights `README.md`, `AGENTS.md`, OpenKB Wiki Schema, What You Must Do When Invoked, and multiple Graphify reference sections as major hubs. The snapshot reinforces this by showing that each major skill includes `SKILL.md` and a `references/` subtree, while the repository root keeps a small set of orientation and control files. Together, these signals suggest that repository use is anchored in explicit documentation, not left implicit in code layout alone. That pattern aligns with [[concepts/documentation-architecture]], [[concepts/action-oriented-documentation]], and [[concepts/agents-md-maintenance]].

### Repeated skill-package structure
The snapshot adds a strong file-level pattern that the graph alone only implies: the repository is composed of named skill directories such as `agent-ready-context`, `graphify`, `openkb`, `skill-creator`, and `subagent-profile-adapter`, each following similar internal conventions. This repeated packaging structure shows that the repository's main shape is not only topical but also templated and modular. That pattern aligns with [[concepts/skill-structure-conventions]], [[concepts/skill-based-automation]], and [[concepts/project-scaffolding]].

### Workflow and governance as first-class structure
Highly connected communities include OKF quality baselines, OpenKB lifecycle guidance, repo build workflow, dependency boundaries, provenance-sensitive packaging, and validation scripts. The snapshot confirms that these are backed by concrete script and reference surfaces such as validators, bootstrap tools, and policy-oriented references. These are not peripheral concerns; they are part of the repository's main shape. This reflects strong [[concepts/generated-content-governance]], [[concepts/provenance-tracking]], [[concepts/quality-gates]], and [[concepts/deterministic-validation]].

### Layered agent context
The graph shows distinct but related clusters for `AGENTS.md`, OpenKB wiki material, skill references, Graphify operational instructions, and runtime/profile tooling. The snapshot makes the same layering visible in directory form through the separation of top-level guidance, skill-local references, reusable assets, and executable scripts. That supports a layered model in which orientation, durable knowledge, and executable actions live in different places. This is closely related to [[concepts/agent-context-layering]], [[concepts/context-action-separation]], and [[concepts/durable-context]].

### Script entrypoints as operational anchors
Named scripts such as `build_okf_source_pack.py`, `validate_okf_bundle.py`, `build_okf_skeleton.py`, `inspect_runtime_context.py`, and repeated `main()` nodes act as concentrated connection points in the graph. The snapshot confirms that script directories recur across several skills rather than appearing as isolated utilities. This suggests a repository where automation is funneled through a small set of explicit operational tools embedded inside modular skill packages. That pattern relates to [[concepts/skill-based-automation]], [[concepts/minimal-tool-scoping]], and [[concepts/safe-automation]].

### Local coherence over broad cross-file linkage
The graph report explicitly says no import cycles were detected and notes that the surprising inferred connection runs between build and prune operations rather than through a tangled dependency loop. It also shows that many connections stay inside the same source files or tight maintenance clusters. The snapshot helps explain why: much of the repository is organized as self-contained skill packages with their own local references, assets, and scripts. This implies strong internal cohesion inside individual files and modules, but weaker graph-visible linkage across the repository. That is a meaningful structural pattern: the repo is well-clustered locally, but many relationships remain document-bounded or package-bounded.

### High volume of isolated or thinly connected nodes
The graph report identifies 234 isolated nodes and notes 9 thin communities omitted from the report. The snapshot suggests that some of this thinness comes from inventory breadth: many template files, helper assets, and narrowly scoped references exist to support workflows, but may not attract many graph connections on their own. This pattern matters because it points to limits in [[concepts/knowledge-linking-and-citations]], [[concepts/index-based-discovery]], and [[concepts/progressive-disclosure]].

### Graph bridges across maintenance workflows
The report's strongest cross-community bridge is the connection between `main()` in `build_okf_source_pack.py` and `bundle_key()` in `prune_okf_orphans.py`, which ties source-pack building to orphan pruning. That kind of bridge suggests the repository's structural spine runs through maintenance orchestration, not application runtime logic. In practice, the most important linkages are often between generation, validation, pruning, and policy enforcement rather than between business-domain modules.

## Why this concept matters
Understanding main structural patterns helps explain how to work effectively in the repository:

- where to start navigating
- which artifacts define project behavior
- whether operational trust depends more on code, policy, or generated knowledge
- whether the repository is organized around packages, workflows, or runtime modules
- where maintenance risk is likely to concentrate

In these sources, those answers point strongly toward a repository organized around explicit knowledge layers, repeated skill packaging, validation workflows, and operational documentation rather than only source-code architecture.

## Practical interpretation
From [[summaries/graphify-report]] and [[summaries/repo-snapshot]], the main structural pattern of this repository can be described as:

- documentation-heavy
- skill-packaged and modular
- workflow-centric
- validation-oriented
- provenance-aware
- agent-ready and context-layered
- locally cohesive but globally sparse in some areas
- bridge-heavy around maintenance orchestration rather than runtime behavior

This means repository improvement is not just about adding code links or refactoring modules. It may also involve improving summaries, navigation pages, explicit cross-links, package conventions, and the structure of generated knowledge artifacts.

## Signals to look for
You are likely seeing this concept when a repository has several of these traits:

- README, AGENTS, or wiki pages function as major graph hubs
- repeated directory templates define the main package shape
- validation and generation scripts are more central than domain classes
- operational policies appear as recurring communities
- logs, summaries, or indexes are structural navigation artifacts
- broad documents have low cohesion and may need splitting
- many isolated nodes suggest missing structural connections or intentionally narrow support artifacts
- cross-community bridges connect build, validation, pruning, or policy workflows

## Relationship to nearby concepts
- [[concepts/documentation-architecture]] focuses on how documentation is arranged; main structural patterns looks at whole-repository recurring shape.
- [[concepts/agent-context-layering]] explains one important pattern visible in both sources: separation between orientation, knowledge, and action layers.
- [[concepts/repository-overview-generation]] is a use of this concept, since graph analysis and file inventories help produce a high-level map of repository organization.
- [[concepts/generated-content-governance]] and [[concepts/quality-gates]] describe specific structural forces that become visible as graph communities and repeated operational files.
- [[concepts/progressive-disclosure]] helps explain why hubs, summaries, package boundaries, and layered navigation matter in a large repository.
- [[concepts/skill-structure-conventions]] captures one especially important subtype of this concept: repeated internal structure across skill directories.
- [[concepts/cross-community-bridges]] is a useful lens for the inferred connections that tie together build and prune workflows.

## Evidence from the sources
[[summaries/graphify-report]] and [[summaries/repo-snapshot]] support this concept with several concrete signals:

- 53 tracked files in the snapshot, giving a compact but structured repository surface
- 472 nodes and 550 edges in the graph report, indicating a much richer relational view than the file inventory alone
- 54 communities in the graph report, showing meaningful topic segmentation
- a `.agents/skills/` hierarchy containing multiple named skill packages
- repeated package elements such as `SKILL.md`, `references/`, `assets/`, and `scripts/`
- top hubs dominated by `README.md`, `AGENTS.md`, OpenKB guidance, Graphify references, and validation-oriented pages
- major communities centered on README, packaging and bundle validation, OpenKB lifecycle, skill creation, tooling policy, and Graphify usage references
- no import cycles, suggesting the structure is not dominated by tangled code dependencies
- 234 isolated nodes and several thin communities, indicating incomplete linkage, local-only cohesion, or intentionally narrow support artifacts
- an inferred bridge from build packaging to orphan pruning, suggesting maintenance workflow interdependence

## Takeaway
Main structural patterns are the recurring large-scale organization signals that show what kind of repository this is. In [[summaries/graphify-report]] and [[summaries/repo-snapshot]], those patterns reveal an agent-ready repository whose primary structure is built from documentation, repeated skill packaging, workflow control, validation, provenance, and layered context rather than from runtime code relationships alone.

## Related pages
- [[summaries/graphify-report]]
- [[summaries/repo-snapshot]]
- [[concepts/agent-context-layering]]
- [[concepts/documentation-architecture]]
- [[concepts/context-action-separation]]
- [[concepts/generated-content-governance]]
- [[concepts/provenance-tracking]]
- [[concepts/quality-gates]]
- [[concepts/repository-overview-generation]]
- [[concepts/progressive-disclosure]]
- [[concepts/skill-based-automation]]
- [[concepts/skill-structure-conventions]]