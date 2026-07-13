---
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__NOTICE.md", "summaries/agents__skills__skill-creator__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__NOTICE.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/repo-snapshot.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/docs__assets__agent-smith-svg.md"]
type: "Work"
description: "Graphify structural report for the agent-smith repository context"
---

# agent-smith

`agent-smith` is the repository and project context for the agent-ready workflow described in [[summaries/agents__skills__agent-ready-context__SKILL-md]]. It provides the source skill, supporting references, and operational conventions for making a repository agent-ready, and the graphify report shows it as a major structural hub in the OpenKB knowledge graph.

## What It Contains

- The `.agents/skills/agent-ready-context/SKILL.md` skill that defines the agent-ready workflow
- Supporting references for dependencies, workflow, OpenKB lifecycle, providers, privacy, external docs, and quality checks
- Scripts for prerequisite checks, KB source-pack staging, validation, pruning, and editorial review
- Shared conventions for keeping repository knowledge in the OpenKB wiki rather than in long-form instruction files
- A graph-structured view of the repository, including community clusters, hub nodes, and weakly connected areas used for navigation and maintenance

## Key Ideas

- Separates [[concepts/context-action-separation]] into skills for actions, the OKF wiki for context, and `AGENTS.md` for orientation
- Treats the OpenKB wiki as the durable source of truth for repository knowledge
- Uses [[concepts/deterministic-okf-staging]] and validation to keep KB compilation reproducible
- Emphasizes [[concepts/consent-first-tooling]] and [[concepts/provenance-aware-tool-installation]] when adopting external tools
- Protects the repository from [[concepts/self-referential-ingestion-loops]] and other invalid KB inputs
- Functions as a graph-analysis anchor for [[concepts/graph-structure-analysis]] and [[concepts/cross-community-bridges]]
- Surfaces repository maintenance patterns that relate to [[concepts/documentation-gaps]] and [[concepts/documentation-cohesion]]

## Related Entities

- [[entities/agent-ready-context-skill]]
- [[entities/openkb]]
- [[entities/graphifyy]]
- [[entities/agent-skills]]
- [[entities/graphify-report-agent-smith]]
- [[entities/graphify-out-graph-report-md]]

## Notes

This entity is central because the document identifies `agent-smith` as the upstream project that supplies the skill, references, and workflow policy for agent-ready repository compilation.

The graphify report adds that `agent-smith` is also a high-value structural node in the corpus: it sits near hubs such as `main()`, `bundle_key()`, `detect_orphans()`, and the OpenKB workflow documents, and it spans communities covering build workflow, skill creation, tooling policy, and validation. It also highlights a large set of isolated nodes and thin communities, making the repository useful as a map for future documentation work.

See also: [[summaries/karpathy-llm-wiki-gist]]

## Related Documents
- [[summaries/graphify-report]]
