---
sources: ["summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/graphify-report.md", "summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
type: "Product"
description: "Python package behind the graphify CLI for repo graph analysis"
---

# graphifyy

`graphifyy` is the Python package that provides the `graphify` CLI, used for repository-scoped graph generation and exploration in the agent-smith workflow.

## Key facts

- It is one of the optional tool-adoption targets in the repository readiness workflow, alongside `openkb`.
- The package name is `graphifyy`; the CLI is `graphify`, so package install records and CLI usage must be kept distinct.
- Tool adoption is consent-first and supply-chain aware: the workflow records version pins, integrity hashes, and index provenance before use.
- The workflow expects `graphifyy` to be installed through the environment's configured Python index, with pinned versioning and integrity tracking.
- Before the first `graphify` invocation, the repository should vendor the read-only skill copy under `.agents/skills/graphify/`.
- The prerequisite check is `uv run .agents/skills/agent-ready-context/scripts/check_prereqs.py --repo .`.
- The prerequisite checker treats `graphify` as an optional CLI, allowing the repository to degrade gracefully if it is absent.
- If the CLI is installed but the vendored skill is missing, the checker records a note urging the repo to vendor `.agents/skills/graphify/SKILL.md` before first use.
- When the toolchain is refreshed, the upstream installer can regenerate the project-scoped skill copy and its `.graphify_version` marker.
- The workflow treats `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as supporting structural inputs for graph exploration, not as final authority.
- `README.md` frames `graphifyy` as a pinned vendor copy that appears in the repo's `.agents/skills/` directory alongside other toolchain skills, but remains outside the three distributable product skills.
- The skill also ties `graphifyy` to the broader agent-ready repository workflow, where `okf/wiki/` is the durable context layer and `AGENTS.md` stays focused on orientation rather than long-form knowledge.
- The `graphify` graph report shows the package as part of a larger structural analysis ecosystem, with strong links to build and validation tooling and a role in repo navigation and maintenance.
- In the report's community map, `graphifyy` sits near the graph-analysis and skill-adoption clusters, reinforcing its function as a tool for structural exploration rather than a primary content source.
- The privacy and data-flow policy adds that `graphify` must never silently auto-select a backend when non-code sources are processed; an explicit `--backend` is required, with `--backend ollama` as the local path.
- For docs, PDFs, images, and video, `graphify` may send document content to the selected LLM backend unless the local backend is chosen.
- For code-only repositories, the preferred path is code-only extraction, which stays local and needs no key.
- When `graphify` does need a key for semantic extraction of non-code sources, it reads process environment only and does not load `.env` itself.
- The documented sourcing pattern keeps secrets in gitignored files while preventing them from crossing the agent's context.
- The toolchain's telemetry posture is explicitly local-first: upstream claims no telemetry, usage tracking, or analytics for `graphifyy`, with local transcription and local-only cost files.
- A separate integrity concern is local-file leakage into committed graph artifacts: `graphify update` does not honor `.git/info/exclude` or global excludes, so locally excluded files can still be scanned and baked into committed outputs.
- The KB staging rule requires `openkb` input to live inside `okf/.okf-build/input/`; when content is staged outside the KB root, OpenKB can record absolute machine paths in its hash registry.

## Operational role

Within the dependencies workflow described in [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] and the repository transformation narrative in [[summaries/README-md]], `graphifyy` supports optional graph generation and discovery-aid tasks. It fits into the broader toolchain pinning and integrity model described by [[concepts/toolchain-pinning]], [[concepts/integrity-pinning]], [[concepts/trust-on-first-use]], and [[concepts/tooling-vendoring]].

The prerequisite checker adds a second layer of operational guidance by distinguishing installed CLI availability from vendored-skill presence. That keeps `graphifyy` aligned with [[concepts/consent-first-tooling]], [[concepts/tooling-context-governance]], [[concepts/tooling-context-isolation]], and [[concepts/graceful-degradation]].

It also sits inside a broader agent-tooling boundary where skills are actions, the OKF wiki is durable context, and tool-specific context is kept separate from project truth. That makes it relevant to [[concepts/agent-tooling-ecosystem]], [[concepts/local-by-default-tooling]], [[concepts/tooling-consent-and-pin-management]], [[concepts/tooling-context-governance]], and [[concepts/tooling-context-isolation]].

The graph report adds that `graphifyy` is part of the repo's graph-structure analysis workflow: the corpus is large enough that graph structure adds value, and the report highlights graph freshness checks, community hubs, and knowledge gaps as key navigation aids. This makes `graphifyy` especially relevant to [[concepts/graph-structure-analysis]], [[concepts/knowledge-graph-analysis]], [[concepts/agent-guided-graph-exploration]], and [[concepts/documentation-gaps]].

## Related ideas

- [[concepts/air-gapped-operation]]
- [[concepts/cross-platform-tooling]]
- [[concepts/data-flow-disclosure]]
- [[concepts/dependency-management]]
- [[concepts/explicit-provider-routing]]
- [[concepts/local-artifact-leakage]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/skill-vendoring]]
- [[concepts/supply-chain-security]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-context-isolation]]
- [[entities/graphify]]
- [[entities/uv]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/graphify-report]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]