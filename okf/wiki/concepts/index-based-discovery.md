---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
description: "Navigation through explicit indexes to keep content discoverable and bounded."
---

# Index-Based Discovery

Index-based discovery is the practice of making wiki content visible through explicit index navigation so users and agents can find it reliably without inferring hidden structure. It is especially important for exceptional or constrained content areas that should remain discoverable while still being clearly separated from core project knowledge.

This concept is illustrated by the tooling-context policy, which requires the bundle-root `okf/wiki/index.md` to list the `tooling/` subtree whenever that subtree contains non-reserved pages. The goal is not to elevate tooling pages into project truth, but to prevent them from becoming invisible to index-driven or spec-driven consumers.

The graphify structural report reinforces this pattern at the repository level. It shows `OpenKB Wiki Schema` as a strong structural hub, alongside high-centrality workflow and validation nodes such as `main()`, `detect_orphans()`, `OpenKB lifecycle for OKF maintenance`, and `OpenKB repo build workflow`. That suggests index design is not only a documentation concern, but also part of the repo's maintenance topology and navigation strategy. The same report also highlights many weakly connected or isolated nodes, which makes explicit indexing even more important for discoverability and [[concepts/documentation-gaps]] management.

## Why it matters

A wiki can contain valid content that is intentionally isolated, such as harness-specific tooling notes or other local-by-default knowledge. If that content is stored on disk but omitted from root navigation, agents that rely on indexes for traversal may never discover it. In practice, this breaks progressive disclosure: the content exists, but only readers with path knowledge can find it.

Index-based discovery solves that problem by requiring a sanctioned navigation entry at the appropriate root. This creates a controlled balance between:
- discoverability
- structural clarity
- authority boundaries

That balance connects this concept to [[concepts/progressive-disclosure]], [[concepts/documentation-architecture]], and [[concepts/knowledge-boundaries]]. It also aligns with the OKF baseline rule that bundles are Markdown directory trees with explicit reserved navigation files, and that valid content should remain navigable without depending on hidden structure.

The graph report's community structure supports this interpretation. Large hubs like `README.md`, `AGENTS.md`, `OpenKB quality and offline conformance baseline`, and `OpenKB repo build workflow` show that navigation and validation are already organized around a few core anchors. By contrast, the 234 isolated nodes and omitted thin communities point to areas where index-based discovery could reduce drift and improve reachability.

## Role in the tooling context policy

The tooling-context policy makes index-based discovery a concrete requirement. Harness and runtime adapter knowledge may live inside OKF only in two cases: a required harness build record for each agent-ready pass, and optional adapter/profile tooling context when a detected or user-selected harness is actively in use. That policy keeps tooling pages from accumulating speculatively while still allowing the right content to be recorded when needed.

In that policy, the root index has a special responsibility. If `okf/wiki/tooling/` contains pages beyond the reserved stub, `okf/wiki/index.md` must include a clearly labeled harness-specific section that references `tooling/`. The label must make clear that tooling content is user-scoped, harness-specific, and should not be treated as project truth. The committed `okf/wiki/tooling/index.md` stub is the stable discovery target; local harness and provider pages remain undisclosed in committed indexes.

The validator for this policy reinforces the same structure in code. It scans Markdown pages outside tooling, ignores code blocks and inline code while searching, and reports an error if a project page links to tooling. It also checks that the root index references tooling when non-reserved tooling pages exist, and that the committed `tooling/index.md` stub is present. Tooling pages that are present but omit expected metadata such as `scope: tooling` or `type: tooling-context` produce warnings rather than hard failures.

This requirement preserves two properties at once:
- tooling context remains discoverable from the bundle root
- project knowledge does not depend on tooling pages

The policy therefore allows root-level navigation while still forbidding project pages and subdirectory indexes from linking into tooling content. It is a concrete example of combining discovery with [[concepts/tooling-context-isolation]], [[concepts/reserved-wiki-files]], and [[concepts/tool-boundaries]].

The policy also emphasizes that tooling context is not source material for project knowledge: it should not be ingested through `openkb add`, and it must not create additional non-standard folders under `.agents/` for tooling context. That makes the discovery rule narrow: the root can expose the tooling subtree, but only as a user-scoped overlay with constrained semantics.

## Root index as a controlled exception

The root `index.md` and `log.md` act as reserved bundle-wide navigation and history files. Because they are infrastructural rather than conceptual pages, they can mention tooling content without creating the kind of semantic dependency that the policy forbids elsewhere.

This means index-based discovery is not just "add a link somewhere." It is a governed pattern:
- only the bundle root may expose the tooling subtree
- the exposure must be explicit and labeled
- the exposure must not collapse the distinction between project pages and tooling context
- committed navigation should point at the stable stub, not at local pages that may not exist on other clones

This governance-oriented use of indexing relates to [[concepts/okf-validation]], [[concepts/wikilink-integrity]], and [[concepts/generated-content-governance]]. It also depends on the broader OKF rule that consumers should tolerate local tooling pages as an overlay, while OpenKB-managed wikis may enforce stricter checks as a producer-side quality bar.

The graphify report adds a second reason for controlled indexing: it identifies many weakly connected content areas and a set of omitted thin communities. In that setting, explicit index surfaces become a practical tool for reducing orphaning, surfacing cluster boundaries, and making the wiki's structure legible to both humans and graph-based agents.

## Validation and enforcement

The source documents do not leave this principle informal. A validator checks whether tooling pages exist without a corresponding root index reference, whether project pages improperly link back into tooling, and whether the committed tooling stub is missing. If those conditions fail, validation fails.

That turns index-based discovery into an enforceable quality rule rather than a documentation preference. It links the concept to [[concepts/executable-validation]], [[concepts/deterministic-validation]], [[concepts/quality-gates]], and [[concepts/validation-vs-health-reporting]]. It also fits the OKF baseline's broader approach: validation should distinguish conformance failures from softer warnings, while still reporting genuine structural problems.

The tooling policy also adds an operational requirement: when the active harness cannot be determined reliably, the record should be skipped and the run report should say why explicitly. That keeps discovery and provenance aligned with [[concepts/adaptive-harness-detection]] and [[concepts/runtime-ambiguity-resolution]] rather than relying on guesses.

The graph report is consistent with this validation-first view. It emphasizes that graph freshness must be checked against the current commit, and that graph updates should be rerun after code changes. In other words, discovery structure itself is a maintained artifact, not a static diagram.

## Practical takeaway

Index-based discovery ensures that exceptional wiki content is visible through official navigation, but only in a way that preserves scope and authority. In this policy, the root index is the single approved discovery surface for tooling pages: enough to make them findable, but not enough to let them become implicit project dependencies.

It is best understood as part of a larger bundle-conformance model that includes explicit reserved files, frontmatter discipline, local-by-default tooling overlays, and validation-aware navigation. The same pattern supports discoverability for harness records and optional tooling context while keeping the main knowledge base organized, trustworthy, and easy to traverse.

The graphify report suggests that this same pattern scales beyond tooling. Strong hubs like `OpenKB Wiki Schema` and `OpenKB repo build workflow` can anchor navigation, while weakly connected nodes benefit from explicit indexing and better cross-links. In that sense, index-based discovery is a structural aid for [[concepts/graph-structure-analysis]], [[concepts/repository-orientation-indexing]], and [[concepts/knowledge-base-navigation]].

See also [[concepts/progressive-disclosure]], [[concepts/tooling-context-pages]], and [[concepts/knowledge-boundaries]].

See also [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]].

See also [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]].

See also [[summaries/graphify-report]].

See also [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]].

See also [[summaries/agents__skills__openkb__references__wiki-schema-md]].

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
