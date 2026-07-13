---
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Other"
description: "Repository Graphify ignore template for excluding KB paths from graph builds."
---

# graphifyignore Template

The `graphifyignore` template is the repository-provided rule file for excluding paths from Graphify's repo graph. In the OpenKB workflow, it is installed from `assets/graphifyignore.template` and merged carefully if a repo already has its own `.graphifyignore`.

## Role in the workflow

- It enforces [[concepts/self-reference-control]] by keeping the KB root out of the graph.
- It supports [[concepts/repo-scoped-graph-partitioning]] and [[concepts/graph-integrity-diagnostics]] by keeping the graph focused on source material rather than generated wiki output.
- It is part of the workflow's [[concepts/deterministic-builds]] and [[concepts/source-bundling]] rules, since the graph inputs must remain stable across runs.
- It protects against [[concepts/knowledge-graph-feedback-loops]] and [[concepts/self-referential-ingestion-loops]] by preventing the wiki from feeding its own generated output back into the graph.
- It also supports [[concepts/kb-root-staging]] and [[concepts/graph-integrity-diagnostics]] by preventing KB artifacts from being reintroduced into graph output.
- It belongs to the broader set of repository hygiene files that keep generated artifacts local and prevent the knowledge base from becoming self-referential.

## Key facts from the workflow document

- The workflow requires `.graphifyignore` to exclude the KB root, specifically `okf/`.
- The template is installed from `assets/graphifyignore.template`.
- If a repo already has a `.graphifyignore`, the workflow says to merge it rather than replace it.
- When an existing rule conflicts with the template, the workflow says to surface both versions and ask the user instead of silently overriding their normalization choices.
- The KB root must stay out of the graph because a wiki that references itself creates a circular feedback loop and undermines deterministic rebuilds.
- The workflow also recommends `git add --renormalize .` after introducing or changing `.gitattributes`, since stable line endings help preserve deterministic staging hashes alongside the ignore rules.
- The ignore policy is a guardrail for both [[concepts/self-reference-control]] and [[concepts/repo-scoped-graph-partitioning]] when Graphify is used.
- The template is part of a larger agent-ready repository bootstrap that also keeps `okf/.okf-build/`, `okf/output/`, and other generated artifacts out of version control.
- Its role is complementary to vendored tooling guidance, prerequisite checks, and source-pack staging, all of which aim to keep graph generation deterministic and safe.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[entities/graphify]]
- [[entities/okf-wiki]]
- [[entities/graphifyignore-template]]
- [[concepts/knowledge-graph-feedback-loops]]
- [[concepts/source-driven-regeneration]]
- [[concepts/knowledge-boundaries]]
- [[concepts/line-ending-normalization]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/tooling-boundaries]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/repo-snapshot]]