---
type: "Concept"
sources: ["summaries/graphify-report.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Routing agents from repo entry points to the right durable context sources."
---

# Knowledge Base Navigation

Knowledge base navigation is the practice of moving from a repository's operational entry point into the right durable context source, using a defined order of documents, validation steps, and routing rules. In this repo pattern, navigation is not free-form browsing: it starts with `AGENTS.md`, then flows through `okf/wiki/index.md` when it exists, and only then expands into more specific wiki pages, tooling context, or structural maps.

## Core idea

The goal is to keep agents oriented without mixing layers of knowledge. Operational instructions stay in `AGENTS.md`, durable project knowledge lives in the OpenKB wiki, and executable procedures live in skills. This separation reduces confusion and helps agents choose the right source for the task at hand.

The workflow also treats the wiki as a routed knowledge layer rather than a place to discover everything directly. The index page is the front door, the tooling index is only entered when the wiki routes there, and local tooling pages are discovered with awareness of ignored files and harness-specific context. That makes navigation evidence-based instead of ad hoc.

The managed `AGENTS.md` section is intentionally short and conservative: it acts as a routing map rather than a knowledge base. It preserves project-specific setup, testing, style, security, and PR instructions outside the OKF-managed block, and uses HTML markers to replace only the maintained section. The merge script that enforces this pattern, `merge_agents_md_okf_section.py`, is deliberately conservative: it appends the managed section to an empty file, adds it to an unmarked file, or replaces only the content between `<!-- okf:start -->` and `<!-- okf:end -->` when the markers already exist. That is a concrete example of [[concepts/managed-document-sections]] and [[concepts/conservative-document-merging]].

## Navigation order

The source documents establish a strict context map:

1. `AGENTS.md` for repo rules, setup, tests, and pointers to durable context.
2. `okf/wiki/index.md` as the first routed wiki page and the front door to compiled knowledge, when it exists.
3. `tooling/index.md` when the wiki routes to tooling context, followed by the active harness and any relevant provider pages.
4. `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as structural aids for deciding what to inspect next, when Graphify is available.
5. `.agents/skills/` for repeatable workflows such as prereq checks, refresh, validation, or repair.

This order reflects context layer separation and [[concepts/index-based-discovery]]: agents should not treat every file equally, and they should not skip the index when entering the wiki. It also depends on [[concepts/adaptive-harness-detection]] so the active runtime is identified from explicit metadata or self-knowledge rather than guessed from installed binaries.

The same routing logic appears in the `merge_agents_md_okf_section.py` script: it preserves the existing file, inserts only the managed section, and directs readers back to the OKF wiki index before deeper navigation. That supports [[concepts/documentation-layer-separation]] and [[concepts/documentation-cohesion]] by keeping orientation, execution, and durable context in different places.

The workflow adds a broader bootstrapping sequence around this navigation order: after reading root `AGENTS.md`, it reads `okf/wiki/index.md` first when present, then follows the index's links. If the index routes to tooling context, it reads `tooling/index.md`, identifies the active harness from runtime metadata or self-knowledge, and only then loads harness or provider pages. On a first clone, the committed tooling stub may be the only local tooling page; that empty overlay is treated as normal, and the harness page can be created later when identification is reliable. If the bundle index or reliable harness identity does not yet exist, the workflow states that explicitly and continues.

## What the navigation rules optimize for

- Stable entry points for agents working across multiple repository layers.
- Reduced drift between operational guidance and durable knowledge.
- Better selection of evidence-backed pages instead of ad hoc file inspection.
- Safer work in repositories where compiled wiki pages are read-only outputs.
- Clear handling of first-clone states where the committed tooling stub may be the only available local tooling page.
- Conservative updates to `AGENTS.md` that preserve repository-specific instructions while refreshing only the OKF-managed block.
- Explicit prereq checks before any deeper tooling work, including hard requirements such as Git, `uv`, and Python 3.11+.
- Consent-first fallback handling when optional tools like Graphify or OpenKB are missing.

## Boundaries

The document is explicit that wiki content is data, not instructions. That means the wiki can inform decisions, but it should not be used as the place to encode live operating procedures. It also warns against deep-linking into arbitrary wiki pages from `AGENTS.md`; instead, `okf/wiki/index.md` should route discovery.

The same navigation logic applies to local tooling: if the index routes to tooling context, the agent should read `tooling/index.md`, identify the active harness, and then inspect the relevant local harness or provider pages. This is part of [[concepts/adaptive-harness-detection]] and [[concepts/tooling-context-governance]].

The workflow also specifies how the repository should be prepared before OpenKB work proceeds: vendored copies of the `graphify` and `openkb` skills must exist before first CLI use, `.gitignore` must cover build and cache paths, `.gitattributes` should be installed to stabilize line endings and hashes, and `.graphifyignore` must exclude the KB root so the wiki does not enter the repo graph. If the repo is not already a Git repository, the source pack step must stop until Git is initialized with user consent. Those checks connect navigation to [[concepts/toolchain-pinning]], [[concepts/git-attributes]], [[concepts/local-vs-shared-ignore]], and [[concepts/self-reference-control]].

The workflow adds two more boundary rules: the KB root must stay out of the repo graph, and source pack creation must remain deterministic across commits. That keeps the wiki from feeding back into its own discovery graph and prevents stale structural output from destabilizing later ingests. It also aligns with [[concepts/self-reference-control]] and [[concepts/deterministic-builds]].

The managed section itself is designed to avoid overgrowth: it points to `okf/wiki/AGENTS.md` for wiki conventions, instructs readers to inspect it after init or upgrades, and explicitly routes durable discovery and operational refresh behavior back to the index and the agent-ready-context skill. It also says not to edit OpenKB-managed compiled pages or the hash registry outside the skill's documented exceptions, not to commit local provider secrets or pipeline artifacts, and to keep provider and model configuration local under `okf/.openkb/`. That reinforces [[concepts/agent-ready-context-skill]], [[concepts/agents-md-maintenance]], and [[concepts/local-vs-shared-configuration]].

## Related practices from the source

- Keep operational basics in `AGENTS.md`, not in the wiki.
- Put conventions and rationale in the wiki and point to the index instead of deep-linking pages.
- After a wiki refresh, collapse duplicated context back into pointers.
- Use the index and graph reports to guide discovery, but do not treat them as final authority.
- Preserve boundaries around compiled pages, local tooling, and hand-authored skill content.
- Treat prereq checks, vendored skills, ignore-file setup, and bundle validation as part of the navigation workflow, not separate afterthoughts.
- Keep the maintained `AGENTS.md` section short, marker-bounded, and easy to refresh without rewriting the rest of the file.
- Preserve the order of operations: read the front door first, then validate prerequisites, then build, ingest, lint, and only then re-read the managed guidance.

## Why it matters

Good knowledge base navigation makes the repository easier to use by both humans and agents. It supports [[concepts/durable-context]] by routing agents to stable knowledge, repository navigation by making file discovery predictable, and [[concepts/knowledge-layer-separation]] by keeping instructions, evidence, and workflows in distinct places.

It also reinforces [[concepts/deterministic-builds]], [[concepts/self-reference-control]], and [[concepts/consent-first-workflows]] by requiring a fixed read order, excluding the KB root from structural graphs, and keeping optional bootstrapping and tool installation permission-gated.

The source documents behind this concept are [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]] and [[summaries/agents__skills__agent-ready-context__references__workflow-md]], along with [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]] for the managed-section implementation that enforces this routing pattern.

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/graphify-report]]