---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/graphify-report.md", "summaries/agents__skills__graphify__SKILL-md.md"]
description: "Read-only checks that reveal graph and wiki structural trust issues."
---

# Graph Integrity Diagnostics

Graph integrity diagnostics are read-only checks that detect structural problems in a built or extracted knowledge graph and surface those problems to the user without silently blocking use of the graph. In [[summaries/agents__skills__graphify__SKILL-md]], this concept appears as a dedicated health-check stage between graph construction and community labeling, and the broader graphify report reinforces that role by treating health checks as a visibility layer for extraction and merge defects rather than as a hard stop.

The same pattern shows up in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]: the validator separates hard conformance failures from warnings, keeps non-destructive checks visible, and uses structural signals such as fence balance, slug collisions, and broken links to reveal damage without pretending the bundle is healthy. That makes graph integrity diagnostics a broader pattern of trustworthy inspection, not just a graphify-specific stage.

The graphify report adds a fuller picture of why this matters. It describes a corpus of 55 files and about 56,244 words, with 442 nodes, 520 edges, and 50 communities. It also highlights 215 isolated nodes and several weakly connected communities. Those numbers are not themselves integrity failures, but they show why structural diagnostics matter: the graph can be large enough to be useful while still containing gaps, bridges, and sparse areas that deserve caution.

## What the concept does

The purpose of graph integrity diagnostics is to answer a narrow but important question: is the graph structurally trustworthy enough to interpret? The checks do not decide whether the content is semantically correct; instead, they look for signs that the graph assembly pipeline may have introduced breakage, loss, mismatch, or coverage gaps.

This makes the concept distinct from full validation. It is closer to health reporting: expose integrity risks, preserve usability, and ensure the user knows when analysis may be incomplete. That aligns closely with [[concepts/validation-vs-health-reporting]], [[concepts/quality-gates]], and [[concepts/evidence-grounded-answering]].

The OKF bundle validator extends that same idea into wiki maintenance. It validates reserved files, frontmatter shape, and optional OpenKB-specific link integrity while still preserving the distinction between errors and warnings. In that mode, diagnostics cover the structural trustworthiness of the knowledge base itself: malformed YAML, missing required fields, unclosed fences, duplicate normalized slugs, and broken wikilinks.

## How it works in graphify

In [[summaries/agents__skills__graphify__SKILL-md]], the graph pipeline includes a dedicated graph health check after extraction has been merged and the graph has been built. The diagnostic is explicitly:

- read-only
- non-destructive
- visible to the user
- non-aborting

The step runs before labeling, so integrity warnings are surfaced before the graph is turned into human-facing categories and explanations. This sequencing matters: it prevents polished labels and reports from hiding extraction or merge defects.

The graphify report gives that sequencing a broader context. It frames the corpus as large enough that graph structure adds value, then uses community analysis, hub rankings, freshness checks, and knowledge-gap reporting to turn the graph into an exploration map. That makes integrity diagnostics part of the interpretive contract: if the structural layer is suspect, the higher-level navigation cues become less trustworthy too.

The bundle validator follows the same sequencing logic. It checks reserved navigation files, then ordinary pages, then runs cross-file diagnostics such as near-duplicate slug detection and link resolution. When used in OpenKB wiki mode, it also skips operational areas like `AGENTS.md`, `sources/`, and `reports/`, because those are maintenance or evidence areas rather than compiled content.

## Problems it is designed to catch

The source document names several silent-corruption modes that the diagnostics should surface:

- dangling endpoint edges
- missing endpoint edges
- self-loop edges
- collapsed edges caused by endpoint duplication
- directed or undirected edge collapse caused by AST and semantic ID mismatches

These checks target the places where [[concepts/graph-merging]] and [[concepts/incremental-graph-maintenance]] can go wrong. For example, if structural extraction and semantic extraction assign inconsistent node identifiers, edges may point at nodes that do not exist or may collapse into malformed graph structure.

The OKF validator adds a parallel class of structural checks for wiki bundles. It detects malformed frontmatter, missing required `type` values, reserved-file violations, unclosed code fences, and sibling page names that collapse to the same normalized slug. In OpenKB mode, broken wikilinks are treated as errors because unresolved links indicate a broken knowledge graph edge rather than a harmless typo.

The graphify report makes the same concern visible at scale: it highlights a surprising cross-community bridge between `build_okf_source_pack.py` and `prune_okf_orphans.py`, and it identifies 215 isolated nodes. Those are not integrity failures by themselves, but they are exactly the kind of structural signals that diagnostics should help interpret. They also point toward [[concepts/cross-community-bridges]] and [[concepts/documentation-gaps]] as separate but related concerns.

## Why this matters

Knowledge graphs are often consumed through higher-level analysis such as community detection, shortest paths, explanation, or graph-guided question answering. If the underlying graph has integrity defects, those downstream outputs can become misleading while still looking plausible.

Graph integrity diagnostics act as a safeguard against that failure mode. They preserve the usability of the graph while making the uncertainty explicit. This supports [[concepts/confidence-calibration]], [[concepts/caveat-preservation]], and [[concepts/knowledge-boundaries]].

The bundle validator shows the same practical value in a wiki setting. A repository can still be browsable even if some pages have damaged frontmatter or broken links, but the diagnostics make those problems visible before users trust the bundle as a stable source of truth. That is especially important when a page is meant to function as compiled knowledge rather than raw notes.

In the graphify report, this matters especially because the report itself is framed as an exploration map: a graph with 442 nodes, 520 edges, and 50 communities. The more the user relies on hubs, bridge nodes, or suggested questions, the more important it becomes to know whether the graph is structurally sound enough to trust those interpretations.

## Relationship to the rest of the pipeline

Within the graphify workflow, integrity diagnostics sit at the intersection of several other concepts:

- [[concepts/knowledge-graph-analysis]]: analysis depends on structurally sound nodes and edges
- [[concepts/idempotent-graph-import]]: repeated imports or rebuilds should not quietly degrade graph structure
- [[concepts/link-directionality]]: directed versus undirected edge handling can change what counts as a collapsed edge
- [[concepts/incremental-compilation]]: update flows are especially vulnerable to mismatch between prior state and new extraction
- [[concepts/provenance-tracking]]: integrity issues are easier to interpret when nodes and edges retain source roots and extraction origins
- [[concepts/graph-structure-analysis]]: community hubs, isolated nodes, and bridge nodes all depend on reliable structure
- [[concepts/cross-community-bridges]]: bridge nodes are useful only when edge integrity is trustworthy

The OKF validator extends that same relationship into bundle and wiki validation. It connects integrity diagnostics to [[concepts/frontmatter-metadata]], [[concepts/reserved-markdown-files]], [[concepts/wikilink-resolution]], [[concepts/line-ending-normalization]], and [[concepts/naming-normalization]]. In OpenKB mode, it also reflects [[concepts/openkb-wikilink-resolution]] and [[concepts/openkb-wiki-health-checks]] by treating unresolved internal links and missing `sources:` metadata as signs that a generated page lost its traceability.

The graph report also shows how integrity and structure diagnostics complement one another: it surfaces freshness information, a community breakdown, omitted thin communities, knowledge gaps, and suggested questions. Those outputs are valuable, but they depend on the graph being structurally honest first.

The source also pairs these diagnostics with stronger destructive safeguards elsewhere in the pipeline. For example, graphify refuses to overwrite an existing larger `graph.json` with a smaller one unless the shrink is intentional. The bundle validator uses a similar layered approach by separating errors, warnings, and optional `--strict-warnings` escalation. Together, these mechanisms form a layered approach to [[concepts/safe-automation]].

## Design principles illustrated by the source

### Health reporting over silent failure

The graph health check prints a warning instead of failing the whole run. This reflects a practical stance: a graph can still be useful even if some edges are suspect, but the user must be told.

The bundle validator follows the same rule by reserving errors for structural failures and using warnings for conditions that reduce confidence without making the bundle unusable. Examples include missing recommended frontmatter fields, unclosed code fences, and duplicate normalized slugs.

### Visibility before interpretation

By running diagnostics before community labeling and final report generation, the pipeline ensures that integrity concerns are surfaced before interpretive outputs are consumed.

The validator applies the same principle to wiki content: it checks conformance before downstream use, and in OpenKB mode it resolves links only after excluding code spans so that structural defects are visible without being confused with literal text.

### Structural honesty

The source document repeatedly emphasizes not inventing edges and not hiding warning conditions. Graph integrity diagnostics are the mechanical expression of that honesty requirement, complementing [[concepts/telemetry-auditing]] and [[concepts/source-provenance]].

The OKF validator adds another form of structural honesty: reserved files must stay reserved, frontmatter must remain parseable, and page relationships must resolve to actual wiki targets. That makes it a guard against both malformed input and silent drift in compiled knowledge pages.

## Practical interpretation

A graph integrity warning does not necessarily mean the graph is unusable. It means the user should treat outputs such as clusters, bridge nodes, suggested questions, and omitted-community summaries with additional caution. In practice, these warnings are especially important when the graph was assembled from multiple extraction modes, updated incrementally, or merged across repositories.

The OKF validator uses the same practical logic for wiki bundles. A file can still be present and readable even when it has a bad fence, missing `type`, or broken link, but those signals indicate that the bundle should not be treated as fully trustworthy without review. In OpenKB mode, missing `sources:` metadata is especially important because it breaks the page's citation chain and weakens provenance.

The graphify report adds another practical clue: the report is built from a specific commit and explicitly asks the user to compare it against the current repository state. That freshness check belongs to the same family of structural trust signals, because stale graphs can be structurally consistent yet still misleading.

For graph-based exploration workflows, this concept supports trustworthy navigation: the graph remains available, but its limitations are made explicit. That directly supports [[concepts/agent-guided-graph-exploration]] and [[concepts/repo-navigation]].

## In the source document

[[summaries/agents__skills__graphify__SKILL-md]] uses graph integrity diagnostics as a formal stage in the graph build pipeline. The document treats them as a mandatory visibility layer for extraction and merge defects, especially those introduced by AST/semantic mismatches, directional edge collapse, and incremental update drift. The checks are deliberately non-destructive, but any warning must be surfaced in the final user-facing summary.

[[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] generalizes that same pattern into bundle validation. It distinguishes reserved files from concept pages, checks YAML frontmatter, warns on code-fence truncation and slug collisions, and optionally enforces OpenKB wiki link integrity. Its design makes structural damage visible while keeping the validator local, deterministic, and OS-agnostic.

The graphify report extends that idea from pipeline mechanics to graph-wide analysis: it presents corpus size, graph size, hub structure, omitted thin communities, isolated nodes, freshness guidance, and cross-community bridges as part of the same trust story. In that sense, graph integrity diagnostics are not just a validation step; they are part of the graph's interpretive contract.

## Related pages

- [[summaries/agents__skills__graphify__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/graph-merging]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/idempotent-graph-import]]
- [[concepts/link-directionality]]
- [[concepts/provenance-tracking]]
- [[concepts/confidence-calibration]]
- [[concepts/safe-automation]]
- [[concepts/documentation-gaps]]
- [[concepts/graph-structure-analysis]]
- [[concepts/frontmatter-metadata]]
- [[concepts/reserved-markdown-files]]
- [[concepts/openkb-wikilink-resolution]]
- [[concepts/openkb-wiki-health-checks]]
- [[summaries/graphify-report]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]