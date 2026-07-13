---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"]
description: "Keeping AGENTS.md concise by updating only its managed orientation block."
---

# AGENTS.md Maintenance

AGENTS.md maintenance is the practice of keeping `AGENTS.md` accurate, concise, and safe to update by treating it as a bounded repository orientation file rather than a knowledge store. It should route agents and contributors to the right sources for rules, commands, durable context, structural maps, and harness-specific operating references while preserving repository-specific guidance that humans have already written.

This concept is illustrated by [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]], which describes a script that updates only a managed section inside `AGENTS.md` and avoids rewriting unrelated content. The script uses HTML markers to bound the OpenKB-managed block, replaces that block when both markers exist, appends it when the file already has other content, or creates a minimal file when none exists. That makes orientation bootstrapping predictable instead of ad hoc, and it keeps the file's role narrow: repository rules first, then compiled wiki context, then structural graph outputs, then reusable skills. The same boundary is reinforced by [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]] and [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]], which show that when tool or harness behavior is uncertain, `AGENTS.md` should point to maintained tooling-context pages rather than absorb volatile adapter details itself. The local alias-management script in [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] adds a complementary pattern: local harness compatibility can be handled by creating a local alias to `AGENTS.md` instead of renaming, duplicating, or forking the canonical file. The provider-configuration guidance in [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]] extends the same boundary to LLM setup: provider names, model choices, endpoints, and credential sources belong in OpenKB configuration and disclosure flows, not in general orientation text. The integrated skill summary in [[summaries/agents__skills__agent-ready-context__SKILL-md]] makes the boundary sharper still by defining a three-part split: skills hold repeatable actions, the OpenKB wiki holds durable repository context, and `AGENTS.md` remains the concise orientation and routing layer that tells agents where to look next. The Graphify hook and AGENTS integration guidance in [[summaries/agents__skills__graphify__references__hooks-md]] adds an adjacent maintenance concern: `AGENTS.md` can activate or document graph-aware behavior, but it should do so by routing agents toward Graphify as a structural aid rather than by embedding structural repository knowledge directly into the file. The bootstrap reference in [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]] reinforces the same maintenance model with a consent-first setup sequence, a clear target repository structure, and explicit commit guidance that keeps generated artifacts, caches, and environment-specific files out of the canonical orientation layer. The source script also encodes a simple merge policy with HTML markers, which is the practical mechanism behind bounded maintenance: replace the managed block when both markers exist, append it when the file already has other content, or create a minimal file when none exists. That makes maintenance idempotent and reviewable while preserving any preexisting project-specific instructions.

## Purpose

`AGENTS.md` serves as a routing layer between high-level repository instructions and deeper context systems. Good maintenance keeps it useful without letting it become a second knowledge base or an unstable generated file.

In the source material, the managed section positions `AGENTS.md` as the first place to check for:

- repository rules
- setup and test commands
- security notes
- pointers to durable context and reusable skills
- pointers to harness-specific documentation records when adapter behavior depends on external tooling
- declarations of any custom wiki sections that agents may need to recognize during specialized workflows
- pointers to privacy and provider-disclosure expectations without embedding provider-specific configuration facts
- the ordered handoff to compiled wiki context, structural repository mapping, and executable skills
- maintenance rules for when repository structure, CI/CD, security controls, or repeated agent actions change
- reminders that the durable repository context source of truth is the OpenKB wiki under `okf/wiki/`, not `AGENTS.md`
- warnings that generated wiki problems should be fixed through source improvement and re-ingestion rather than hand-editing compiled pages
- concise instructions that graph artifacts should be consulted as repository-overview aids and refreshed through Graphify workflows rather than manually described in orientation text
- a stable place to record toolchain versions, setup commands, and test invocation while leaving conventions and rationale to the wiki
- consent-first bootstrap instructions that verify prerequisites before installing missing tools
- the target layout for an agent-ready repository, including `okf/`, `graphify-out/`, and `.agents/skills/`
- guidance that `AGENTS.md` should not absorb long architectural explanations or copied external documentation
- a canonical note that bundled maintenance scripts should run through `uv` when available rather than bare `python`
- a reminder that `okf/wiki/index.md` is the front door for durable wiki navigation, so `AGENTS.md` should point there instead of deep-linking individual wiki pages
- a note that `AGENTS.md` may mention a `## graphify` section or similar tool-specific routing, but should not absorb graph contents or graph schema details
- a bounded merge policy for updating only the managed section between HTML comments so project-specific instructions survive unchanged

That role connects AGENTS.md maintenance to [[concepts/agent-context-layering]], [[concepts/documentation-architecture]], [[concepts/durable-context]], [[concepts/tooling-context-pages]], [[concepts/context-action-separation]], [[concepts/documentation-source-priority]], and [[concepts/knowledge-boundaries]].

## Core maintenance pattern

A strong maintenance pattern is to update only a clearly delimited section rather than rewrite the whole file. In the source script, the managed block is bounded by HTML comments and is either:

- replaced in place when both markers exist
- appended when the file already contains other content
- inserted into a new file with a default heading when the file does not yet exist

This preserves project-specific instructions outside the managed region, reduces accidental loss of local guidance, and makes generated updates reviewable because maintainers can focus on a known bounded block. That makes AGENTS.md maintenance a form of [[concepts/generated-content-governance]] with respect to human-authored content.

The summarized script also adds content-level discipline to that bounded update model. The inserted section does not just mention OpenKB in general terms; it codifies a specific repository knowledge split: skills for actions, the wiki for durable context, and `AGENTS.md` for orientation and best practices. It also explicitly warns that `okf/wiki/AGENTS.md` is a conventions manual to inspect after initialization or upgrades and to customize only with user consent, especially for custom sections. This turns AGENTS.md maintenance into a practical enforcement point for [[concepts/context-action-separation]], [[concepts/documentation-source-priority]], and [[concepts/knowledge-boundaries]].

The tooling-context policy strengthens this pattern by adding another bounded responsibility: `AGENTS.md` may declare and preserve a custom wiki section such as `okf/wiki/tooling/`, but only as a conventions-level navigation aid. It must not become the place where fast-changing harness requirements are fully restated. Maintenance therefore includes keeping navigation structure current while leaving detailed operational facts in downstream tooling-context pages and preserving the distinction between project knowledge and harness-specific behavior. This makes AGENTS.md maintenance closely related to [[concepts/tooling-context-isolation]] and [[concepts/knowledge-boundaries]].

The provider reference adds a parallel boundary for LLM-backed workflows. `AGENTS.md` can remind maintainers to configure OpenKB explicitly and disclose where staged content will be sent, but it should not duplicate the current `model`, provider name, endpoint, or credential-source details that live in `okf/.openkb/config.yaml` and runtime environment resolution. Duplicating those facts in orientation text would create drift the moment configuration changes, so maintenance includes keeping `AGENTS.md` vendor-agnostic while routing provider-specific checks to the right configuration and disclosure records. This aligns with [[concepts/single-source-of-truth]], [[concepts/provider-integration]], and [[concepts/data-flow-disclosure]].

The bootstrap reference extends that same discipline to repository setup. It treats tooling installation as consent-first, recommends checking prerequisites before installing missing tools, and separates the durable repository layout from the commands used to generate it. `AGENTS.md` should therefore name the target structure and the sequence of setup commands without trying to become a full procedural manual. This fits [[concepts/preflight-checks]], [[concepts/consent-first-tooling]], and [[concepts/project-scaffolding]].

The local-alias script adds a second bounded-update idea at the filesystem level. When a harness expects a different instruction filename, the repository can keep `AGENTS.md` as the canonical source and satisfy the harness with a local alias or pointer file created in the working tree. This avoids editing `AGENTS.md` to chase vendor naming requirements and reinforces [[concepts/single-source-of-truth]], [[concepts/cross-platform-tooling]], [[concepts/graceful-degradation]], and [[concepts/local-vs-shared-configuration]].

The Graphify integration guidance adds a similar boundary for structural repository analysis. `graphify agents install` can write a `## graphify` section into local `AGENTS.md` so agent sessions consistently check graph outputs before answering codebase questions and rebuild them after code changes, but that does not change the file's role. Good maintenance keeps such guidance narrow and operational: `AGENTS.md` may tell agents when to consult graph outputs and when to refresh them, yet the graph itself remains a generated structural aid rather than a source of orientation truth. This makes AGENTS.md maintenance closely related to [[concepts/repository-overview-generation]], [[concepts/generated-artifact-adoption]], and [[concepts/incremental-graph-maintenance]].

The broader skill policy adds another important maintenance rule: `AGENTS.md` should describe the stable process surface, not the mutable compiled outputs or tool internals. It can tell contributors to inspect `okf/wiki/`, Graphify outputs, and project skills in a defined order, but it should not absorb the wiki's long-form context, Graphify's structural details, or reusable workflow logic that belongs in skills. In that sense, maintenance is partly about preventing layer collapse across [[concepts/documentation-cohesion]], [[concepts/durable-context]], and [[concepts/skill-based-automation]].

## What belongs in AGENTS.md

The source material presents `AGENTS.md` as an orientation and policy surface, not the canonical home for detailed repository knowledge. It should contain:

- concise instructions for how to navigate repository context
- repository-specific operating rules
- setup, validation, and testing entry points
- warnings about sensitive or destructive workflows
- links to the systems that hold longer-lived or more specialized information
- references to maintained tooling-context pages when external harness semantics affect how agents should behave
- concise notice that harness-specific profile adapters or tooling-context records can exist without embedding the full operational detail there
- canonical guidance that local aliases should defer to rather than duplicate when a harness needs a different instruction-file path
- disclosure expectations for LLM-backed operations, stated at the policy level rather than as pinned provider selections
- reminders that bundled maintenance scripts should run through `uv` when available rather than bare `python`
- maintenance triggers that tell contributors when broader repo changes should cause orientation and knowledge-routing updates
- reminders that OpenKB owns `okf/` as the KB root and that wiki regeneration flows should start from staged inputs rather than direct edits to compiled pages
- concise statements about which artifacts are navigation aids versus sources of truth
- brief instructions for when Graphify-generated graph outputs should be checked or rebuilt, without copying graph contents into the file
- the primary language and toolchain versions needed to work in the repository
- the setup, build, launch, and test commands contributors should run first
- the target directory structure for agent-ready repositories
- the consent-first rule for installing missing tools
- a short pointer to `okf/wiki/index.md` as the front door to durable wiki context
- a clear note that `AGENTS.md` can mention a `## graphify` section or other tool-specific routing, but should not absorb graph contents or graph schema details
- a reminder that local compatibility aliases should point back to the canonical file rather than become the authoritative copy
- a bounded merge policy that updates only the managed block and preserves the surrounding project guidance

In the managed guidance described by the summaries, `AGENTS.md` points agents to:

- `okf/wiki/` for compiled durable context
- Graphify outputs for structural repository overview
- `.agents/skills/` for reusable executable procedures
- harness tooling-context records when profile paths, frontmatter requirements, permissions, tool model, instruction-file behavior, or generation policy must be checked before adapter work
- OpenKB configuration and privacy/data-flow references when provider selection, model configuration, or content-disclosure obligations matter before LLM-backed commands
- validation scripts and maintenance utilities that verify generated wiki integrity after updates
- `okf/wiki/AGENTS.md` when wiki conventions or custom wiki sections need inspection after initialization or upgrades
- Graphify maintenance commands or installed integrations when code changes require graph refreshes as part of normal repository navigation
- the repository wiki index rather than individual deep-linked pages when orientation needs a stable front door

This aligns the document with [[concepts/context-action-separation]], [[concepts/skill-based-automation]], [[concepts/repository-overview-generation]], [[concepts/documentation-source-priority]], and [[concepts/orientation-routing]].

## What should not happen

AGENTS.md maintenance should avoid turning the file into a dumping ground for every detail discovered during repository analysis. The source script is designed to prevent that drift by keeping the managed section narrow and replaceable.

The document set also implies several anti-patterns:

- rewriting the full file when only a shared section needs refresh
- duplicating durable repository knowledge that belongs in the wiki
- copying long harness documentation into `AGENTS.md` instead of summarizing it in a tooling page
- storing executable workflow detail that should become a reusable skill
- manually patching generated wiki knowledge instead of improving source inputs
- relying on community examples in `AGENTS.md` when official local or official web documentation should be consulted first
- allowing `AGENTS.md` to depend on detailed harness writeups instead of merely acknowledging that such pages may exist
- treating tooling-context pages as ordinary project truth rather than bounded operational context
- creating committed harness-specific copies of `AGENTS.md` when a local alias or pointer file is sufficient
- renaming the canonical instruction file to satisfy one adapter when a local compatibility layer can preserve repository-wide stability
- copying current OpenKB provider names, model strings, endpoint details, or credential-resolution specifics into `AGENTS.md` when those belong in config and disclosure flows
- embedding billing or vendor assumptions in orientation guidance instead of requiring explicit provider choice at runtime
- treating structural graph outputs or compiled wiki pages as the final authority instead of navigation and context aids
- embedding `graph.json` or `GRAPH_REPORT.md` detail into `AGENTS.md` instead of directing agents to inspect the generated artifacts themselves
- assuming Graphify automation covers every change type when hook-driven rebuilds intentionally ignore document and image updates
- bypassing the recommended `uv` execution path for bundled maintenance scripts when that execution contract is part of the repository workflow
- writing generated content directly into OpenKB-owned wiki locations when staged input and ingestion are the intended regeneration path
- using `AGENTS.md` to hide or blur the distinction between repeatable actions, compiled context, and orientation
- letting bootstrap instructions become sprawling installation prose instead of a compact consent-first checklist
- turning local alias files into a second canonical instruction surface
- deep-linking `AGENTS.md` guidance to individual wiki pages when the wiki index should remain the navigational front door
- allowing the managed block to overwrite local additions outside the HTML markers

These constraints support [[concepts/source-driven-regeneration]], [[concepts/tool-boundaries]], [[concepts/documentation-source-priority]], and [[concepts/source-trust-levels]].

## Relationship to OpenKB and repository workflows

In the source summaries, the managed AGENTS.md section defines a workflow order: check `AGENTS.md` first, then the OpenKB wiki, then structural outputs such as Graphify, then reusable skills. This makes AGENTS.md the front door for repository operation while keeping it lightweight.

The integrated script summary makes that ordering more concrete by pairing each layer with a distinct responsibility: `AGENTS.md` for repository rules and orientation, the wiki for durable context treated as data rather than instructions, Graphify for structural guidance rather than source authority, and skills for reusable executable actions. That layered ordering is a maintenance concern because drift in `AGENTS.md` can collapse those boundaries and confuse whether a contributor should read, execute, or regenerate a given artifact.

The harness-documentation guidance adds a more specific branch to that workflow: when a harness profile or subagent contract is unclear or may have changed, the next step is to consult a maintained tooling-context page derived from current official documentation. That page captures only the adapter-critical details, such as supported profile paths, required frontmatter, permissions or tool model, instruction-file behavior, and the user-selected generation policy.

The tooling-context policy further clarifies that these pages are conditional artifacts, not baseline repository outputs. They belong under `okf/wiki/tooling/harnesses/` only when a detected or user-selected harness makes them necessary, and they are not source material to be ingested through normal repository knowledge flows. `AGENTS.md` maintenance therefore includes keeping the distinction visible: project knowledge lives in the standard wiki structure, while harness-specific runtime context remains isolated, optional, and one-way in its dependencies on project material.

The provider guidance adds another operational branch: before the first OpenKB command that sends staged content to an LLM, maintainers should verify configuration through lightweight status and list checks, ensure the chosen provider and model are configured in `okf/.openkb/config.yaml`, and disclose tool, provider, model, endpoint, credential source, and what content will be sent. `AGENTS.md` should route users to that process, but should not restate the active provider configuration or preserve stale vendor facts. This ties AGENTS.md maintenance directly to [[concepts/provider-integration]], [[concepts/data-flow-disclosure]], [[concepts/local-vs-shared-configuration]], and [[concepts/privacy-preserving-tooling]].

The alias script extends that workflow with an operational compatibility step: if a harness requires a different instruction-file name, maintainers can generate a local alias that points back to `AGENTS.md` and exclude it through local Git metadata. This lets repository workflows adapt to harness expectations without altering the project’s canonical orientation file or changing shared tracking policy, which fits [[concepts/local-vs-shared-configuration]], [[concepts/path-safety]], and [[concepts/safe-automation]].

The Graphify hook guidance adds another branch for repositories that rely on structural graph outputs during agent work. A post-commit hook can automatically rebuild graph artifacts after each `git commit` by checking changed code files, re-running AST extraction on them, and regenerating `graph.json` and `GRAPH_REPORT.md`. AGENTS.md maintenance should reflect that behavior as workflow guidance when the project has enabled it, while also preserving the caveat that documentation and image changes are not covered by the hook and still need manual graph updates. This ties AGENTS.md maintenance to [[concepts/incremental-graph-maintenance]], [[concepts/safe-automation]], and [[concepts/action-oriented-documentation]].

The Graphify AGENTS integration guidance adds a related always-on pattern: local installation can add a `## graphify` section instructing the agent to check the graph before answering codebase questions and rebuild it after code changes. Maintained correctly, that section strengthens repository navigation without turning `AGENTS.md` into a graph export or code index. It keeps the file in its proper role as an instruction surface that routes agents toward generated structural aids. This reinforces [[concepts/repo-navigation]], [[concepts/generated-artifact-adoption]], and [[concepts/agent-ready-repositories]].

The agent-ready context skill adds repository-wide workflow responsibilities around OpenKB itself. `AGENTS.md` should steer maintainers toward prerequisite checks, staged evidence builds, explicit consent before installs or broad regeneration, post-generation review of wiki output, and validation of the final bundle. It should also preserve the idea that `okf/wiki/` is the durable context source of truth while reminding contributors that generated wiki content remains compiled output that must be traceable back through source material and staging. This links AGENTS.md maintenance to [[concepts/preflight-checks]], [[concepts/evidence-staging]], [[concepts/repository-ingestion]], [[concepts/okf-validation]], and [[concepts/knowledge-linking-and-citations]].

The same guidance also includes maintenance rules for when source files, architecture, CI/CD, security controls, external documentation assumptions, or repeated agent actions change. In those cases, AGENTS.md maintenance is not isolated; it participates in a broader repository update cycle involving:

- refreshed repository mapping
- rebuilt evidence inputs
- OpenKB ingestion or recompilation
- regeneration or verification of harness tooling-context records when a harness-specific run requires them
- local alias verification when harness-specific instruction-file conventions are in play
- provider/configuration verification and disclosure review before the first LLM-backed OpenKB operation
- graph hook or AGENTS integration checks when structural graph maintenance is part of the repository workflow
- validation of generated wiki content and tooling link direction
- possible extraction of repeated workflows into custom skills
- review of OpenKB hash-registry consistency when changes under `okf/` could create registry drift

That broader role connects this concept to [[concepts/repository-ingestion]], [[concepts/evidence-staging]], [[concepts/incremental-compilation]], [[concepts/quality-gates]], and [[concepts/okf-validation]].

## Safety and change control

The source documents embed a cautious operational stance that is relevant to AGENTS.md maintenance even though the file itself is simple Markdown. The managed instructions emphasize:

- explicit consent before bootstrapping or broad tool actions
- pinned tooling where possible
- protection of secrets and local artifacts in `.gitignore`
- review of generated changes before acceptance
- use of current official documentation when external harness behavior is uncertain
- recording navigation and wiki-structure changes so validators and future maintainers can trace them
- editing wiki-convention declarations for custom sections only with user consent
- keeping harness-required aliases inside the repository boundary and untracked by default through local exclusion rules
- preferring reversible local symlinks and falling back to pointer files when symlinks are unavailable
- keeping API keys and other credentials out of committed orientation files while disclosing the provider path that will receive staged content
- treating the OpenKB hash registry and compiled wiki as a coupled unit whose consistency should be checked after merges or reverts affecting `okf/`
- validating the final wiki bundle after generation rather than assuming the managed section alone is sufficient process control
- respecting configured package indexes and integrity pinning when AGENTS.md records toolchain expectations
- keeping web-fetched evidence treated as untrusted and summarized rather than executed
- reviewing Graphify-managed hook or AGENTS section changes as bounded automation rather than assuming all repository context has been refreshed
- using local aliases or pointer files only as compatibility layers, not as substitutes for the canonical file
- checking the wiki index before assuming a specific page path, because the index is the stable entry point for durable context navigation

These expectations tie AGENTS.md maintenance to [[concepts/tooling-consent-and-pin-management]], [[concepts/privacy-preserving-tooling]], [[concepts/supply-chain-security]], [[concepts/provenance-tracking]], and [[concepts/okf-validation]].

## Why bounded updates matter

Bounded updates make AGENTS.md easier to trust. A maintainer can inspect a known managed region without worrying that automation has reformatted or deleted the rest of the file. In practice, this improves:

- edit safety
- reviewability
- compatibility with repository-specific customization
- long-term maintainability of shared guidance
- stability of links to downstream wiki sections such as harness tooling pages
- preservation of the boundary between project-facing instructions and tool-specific runtime context
- flexibility to satisfy harness filename expectations through local aliases instead of canonical-file churn
- resistance to provider drift by keeping runtime model and endpoint facts out of static orientation text
- predictability of file creation and replacement behavior when repositories adopt AGENTS.md later in their lifecycle
- confidence that automation is acting conservatively rather than rewriting the entire orientation surface
- protection against accidentally turning compiled outputs or tool-local state into orientation truth
- clearer review of Graphify-specific automation because hook instructions and AGENTS-managed graph sections can be inspected as narrow deltas
- a stable place for the repository's basic commands and operating assumptions even as deeper knowledge moves into the wiki
- a clear bootstrapping path when a repository is first converted into an agent-ready layout
- a stable navigation path through `okf/wiki/index.md` instead of scattered deep links
- less churn when local compatibility aliases or pointer files are needed for a specific harness
- straightforward preservation of any preexisting non-OpenKB instructions outside the managed block

This is especially important when multiple tools or contributors may touch nearby documentation. It also supports [[concepts/wikilink-integrity]] indirectly by keeping navigation guidance stable and predictable, including the requirement that any custom wiki section named in `AGENTS.md` is reflected in the maintained index structure and does not create forbidden project-to-tooling dependencies.

## Practical takeaway

AGENTS.md maintenance is not just about keeping a file current. It is about preserving a stable orientation layer that points to the right sources of truth, updates shared agent guidance conservatively, routes volatile tool-specific details into maintained tooling-context pages, and keeps generated process instructions from overwriting local repository knowledge. Good maintenance also preserves strict boundaries: `AGENTS.md` may declare the existence of specialized tooling-context areas, but it should not become the repository's storage layer for harness-specific behavior. The same applies to OpenKB provider setup: the file may require explicit disclosure and config verification, but provider, model, endpoint, and credential details stay in config and runtime context rather than in `AGENTS.md`. When a harness needs a different instruction-file path, the preferred response is usually to create a local alias back to `AGENTS.md` rather than split, rename, or duplicate the canonical document. When Graphify is integrated, `AGENTS.md` may also tell agents to consult structural graph outputs and explain whether graph refresh is handled by a post-commit hook or by an installed graphify section, but it should still avoid copying graph content or pretending hook automation covers every repository change. The merge script, Graphify integration behavior, and broader agent-ready workflow all point to the same lesson: even the maintenance mechanism itself should embody conservative replacement, explicit boundaries, predictable bootstrap behavior, and a clear separation between repository orientation, durable context, structural analysis, and executable skills. The broader repository workflow extends that lesson across the project: `AGENTS.md` should remain the concise front door to a system whose durable context lives in OpenKB, whose repeatable actions live in skills, whose graph outputs support structural navigation, and whose generated knowledge must be reviewed, validated, and regenerated from source when it drifts.

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- [[summaries/agents__skills__graphify__references__hooks-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]
- [[concepts/agent-context-layering]]
- [[concepts/context-action-separation]]
- [[concepts/cross-platform-tooling]]
- [[concepts/data-flow-disclosure]]
- [[concepts/documentation-architecture]]
- [[concepts/documentation-cohesion]]
- [[concepts/documentation-source-priority]]
- [[concepts/durable-context]]
- [[concepts/evidence-staging]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/generated-content-governance]]
- [[concepts/graceful-degradation]]
- [[concepts/hash-registry-coherence]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/knowledge-boundaries]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/okf-validation]]
- [[concepts/orientation-routing]]
- [[concepts/path-safety]]
- [[concepts/preflight-checks]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/provider-integration]]
- [[concepts/project-scaffolding]]
- [[concepts/quality-gates]]
- [[concepts/registry-drift]]
- [[concepts/repo-navigation]]
- [[concepts/repository-ingestion]]
- [[concepts/repository-overview-generation]]
- [[concepts/safe-automation]]
- [[concepts/single-source-of-truth]]
- [[concepts/skill-based-automation]]
- [[concepts/source-driven-regeneration]]
- [[concepts/source-trust-levels]]
- [[concepts/tool-boundaries]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-context-pages]]
- [[entities/agents-md]]
- [[entities/graphify]]
- [[entities/openkb]]

See also: [[summaries/agents__skills__skill-creator__references__action-vs-context-md]]

See also: [[summaries/agents__skills__skill-creator__references__testing-skills-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/README-md]]