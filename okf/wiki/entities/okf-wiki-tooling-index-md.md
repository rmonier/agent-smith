---
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
type: "Work"
description: "The wiki tooling index that catalogs harness-specific tooling pages."
---

# OKF Wiki Tooling Index

The OKF Wiki Tooling Index is the navigation page for `okf/wiki/tooling/`, the harness-specific section of the OKF wiki. It exists to keep tooling context discoverable while preserving the boundary between project knowledge and runtime-specific adapter documentation.

## Role

This page is treated as a deliberate exception in the wiki structure: when tooling pages exist, the root wiki index should reference `okf/wiki/tooling/` in a clearly labeled harness-specific section. That makes the bundle navigable without letting tooling pages become a source of truth for project concepts.

## Key Properties

- It is part of the OKF wiki's tooling context, not the main project knowledge graph.
- It supports [[concepts/tooling-context-governance]] and [[concepts/tooling-navigation-exception]] by separating harness docs from project docs.
- It reinforces [[concepts/link-directionality]] and [[concepts/tooling-link-policy]] by allowing tooling pages to point outward, while preventing project concept pages from depending on tooling content.
- It is closely related to [[entities/okf-wiki]] and [[entities/okf-wiki-index-md]], since it helps structure the compiled wiki bundle.

## In the Source Document

The summarized skill page says that tooling documentation should live under `okf/wiki/tooling/`, that the bundle-root `okf/wiki/index.md` must list that section when tooling pages exist, and that this navigation stub keeps the wiki coherent on every clone. It also warns that deeper project pages must not link back to tooling pages.

## Related Material

- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[entities/okf-wiki-tooling]]
- [[entities/okf-wiki-index-md]]
- [[concepts/tooling-context-pages]]
- [[concepts/local-by-default-tooling]]
- [[concepts/tooling-navigation-exceptions]]