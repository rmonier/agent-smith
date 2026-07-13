---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md"]
description: "Long-lived wiki knowledge that anchors agent work across sessions."
---

# Durable Context

Durable context is the long-lived, maintained repository knowledge that agents should treat as the reliable source of truth across repeated work. It captures facts, rationale, provenance, constraints, and operating context that remain useful beyond a single run, prompt, generated artifact, or agent profile. In the source materials, durable context is not just stored reference material; it is a maintained layer that helps agents decide what to do, when to do it, and under which constraints.

The README for `agent-smith` reframes this as part of a broader [[concepts/knowledge-compilation-pipeline|knowledge compilation pipeline]]: raw sources are treated as input, an interlinked wiki is the compiled knowledge surface, and the LLM acts as a compiler that ingests new material, updates cross-references, and flags contradictions so knowledge compounds instead of evaporating. That framing aligns durable context with the wiki as a stable memory layer for agents, and with [[concepts/progressive-disclosure]] as the principle that only the highest-signal context should be surfaced at the right time.

## What counts as durable context

Durable context typically includes:

- architecture facts and repository structure
- design decisions and the reasons behind them
- runbook context and workflow purpose
- external documentation captured as evidence
- source provenance and traceability details
- validation rules, quality expectations, and bundle conventions that shape how repository knowledge is maintained
- role definitions and standing operational boundaries that agents should consult repeatedly, such as which context files matter for a given kind of task and what permission limits apply
- navigation and maintenance conventions that keep a knowledge base usable over time, such as reserved index and log structures, citation habits, repository-specific interpretation rules, and reusable descriptions of how specialized subagents should approach recurring repository work
- bootstrap and setup guidance that survives repository conversion, including consent-first tool installation, prerequisite checks, and the expected command sequence for building and validating the knowledge base
- commit and artifact policy, such as which generated files belong in version control and which outputs should stay local
- repository-surface definitions that separate orientation, context, actions, and harness-specific projections into distinct layers

These are the kinds of materials that should accumulate in a maintained knowledge base rather than in transient notes or overly long routing files.

## What durable context is not

Durable context is distinct from several neighboring categories:

- It is not a short routing file such as `AGENTS.md`, which should stay focused on instructions, commands, and pointers.
- It is not a structural exploration output such as `graphify-out/`, which may help inspect a repository but is not final authority.
- It is not the same as executable procedures or repeated command sequences, which are better represented as reusable skills under [[concepts/skill-based-automation]].
- It is not temporary pipeline state, build output, or caches.
- It is not the repository source code itself, even when source code remains the implementation source of truth.
- It is not a vendor-native harness profile file by itself; durable context is the maintained knowledge from which such profiles can be derived or adapted.
- It is not the bootstrap scripts or commands themselves, although those scripts may encode how durable context is discovered, validated, or regenerated.

This separation supports cleaner [[concepts/documentation-architecture]] and helps agents find stable information quickly without confusing operational artifacts with maintained knowledge.

## Role in an agent-ready repository

In the source documents, durable context is placed in `okf/wiki/`, which is described as the knowledge source of truth for agents. The codebase still holds implementation truth, but the wiki carries the curated explanations, evidence, and maintenance conventions that let agents work consistently over time. That recommendation creates a layered model:

- `AGENTS.md` routes the agent
- `okf/wiki/` stores durable knowledge
- `graphify-out/` supports exploration
- skills encode repeatable execution
- subagent profiles describe purpose, activation conditions, context dependencies, and permission boundaries for recurring roles

The `agent-smith` README sharpens this model by explicitly splitting the repository into four surfaces: orientation in `AGENTS.md`, context in `okf/wiki/`, actions in `.agents/skills/`, and harness-specific runtime projections that should never become source of truth. It also emphasizes that knowledge should stay out of files that instruct, and that instructions should stay out of files that preserve context.

The bootstrap guidance makes that layering operational. It recommends confirming prerequisites first, installing missing tools only after user consent, and then following a repeatable sequence: merge the OKF section into `AGENTS.md`, refresh graph data, build a source pack, initialize OpenKB, ingest the source pack, lint the wiki, validate the bundle, and merge the updated `AGENTS.md` section again. That sequence shows durable context as both the end product of repository preparation and the guide for how preparation should be repeated.

The new README also identifies three portable skills as the product surface of the repository: `agent-ready-context`, `skill-creator`, and `subagent-profile-adapter`. Their role is to operationalize durable context by transforming repository knowledge into bootstrap, reusable actions, and harness-aware adapter generation. The skills reinforce the same boundary: context lives in the wiki, procedures live in skills, and runtime projections stay local to the active harness.

The new `AGENTS.md` template strengthens the model by explicitly defining the wiki as the place for durable context and by instructing maintainers to move conventions and rationale out of `AGENTS.md` after refreshes. It also sets a read order for context sources: `AGENTS.md`, then `okf/wiki/` with `index.md` first, then `graphify-out/`, then `.agents/skills/`.

The template further clarifies that durable context should survive OKF refreshes and regeneration. Once a fact, convention, or workflow rule has a stable wiki home, `AGENTS.md` should collapse back to a pointer instead of duplicating it. That keeps the operational index lean while preserving durable knowledge in the compiled wiki. This matches [[concepts/compiled-knowledge-bases]], [[concepts/generated-content-governance]], and [[concepts/source-driven-regeneration]].

The OKF baseline also clarifies that durable context lives in a structured Markdown bundle with reserved navigation files such as `index.md` and `log.md`, concept pages with required metadata, and directory layouts that may include concepts, summaries, entities, explorations, reports, and repository-specific areas like tooling. That structure makes durable context easier to validate, browse, and preserve.

The profile-intent examples add an important operational detail: durable context is not only something agents read after they are assigned work, but also something used to shape role selection itself. A curator role may rely on the wiki to detect missing or stale knowledge, a skill-architecture role may use the wiki to detect repeated actions worth formalizing, and a repository-mapping role may gather read-only understanding before the wiki is updated. In that sense, durable context acts both as a memory layer and as an input to agent orchestration under [[concepts/permission-scoped-agents]] and [[concepts/subagent-role-design]].

## Why it matters

Durable context makes agent behavior more consistent over time because it gives future work a stable base of facts and explanations. Instead of relying on ad hoc prompts or one-off repository scans, agents can use curated knowledge that persists across sessions.

Benefits include:

- less repetition when rediscovering architecture or workflow intent
- clearer boundaries between facts, guidance, and automation
- better retention of evidence from [[concepts/external-documentation]]
- stronger traceability through [[concepts/provenance-tracking]]
- easier validation and maintenance through [[concepts/deterministic-validation]] and [[concepts/quality-gates]]
- better offline reliability when agents must work without live access to external specifications or services
- more portable role definitions because agent profiles can point to stable repository knowledge instead of embedding all context directly into harness-specific configuration
- more reliable bootstrap and recovery workflows because the repository retains the commands, boundaries, and policy decisions needed to rebuild its own context layer
- less confusion between orientation, durable memory, and reusable actions because each surface has a clear job

The offline OKF baseline especially shows that durable context is not just stored knowledge but also a fallback contract: when network access is unavailable, agents can still validate and maintain the repository against embedded rules while clearly reporting the authority level they used. This connects durable context to [[concepts/offline-first-workflows]] and [[concepts/spec-authority]].

## Durable context and regeneration

A key implication of the source documents is that durable context should survive regeneration workflows. Generated or compiled knowledge can be refreshed, but the repository should preserve the authoritative content and supporting evidence needed to rebuild it consistently. This connects durable context to [[concepts/source-driven-regeneration]].

The same materials also show that durable context must preserve the rules needed to regenerate and validate the knowledge base itself: metadata expectations, navigation conventions, citation practices, local policy overlays such as stricter wikilink checks, and the bootstrap steps that define how the wiki is built from source material. Maintaining those rules inside the repository helps regeneration stay repeatable and auditable.

The bootstrap guidance also notes that initial knowledge-base generation is a discovery process: once durable context exists, repeated procedures found during that process should be moved into skills rather than left embedded in documentation.

The profile-intent examples sharpen this distinction. Reusable role descriptions may persist as durable context because they explain how work should be delegated and constrained, while the executable steps those roles perform belong in skills or validation scripts. This reinforces the separation between maintained context and actions, and fits with the broader pattern of keeping role intent, repository knowledge, and executable automation in distinct but connected layers.

The updated `AGENTS.md` template adds an explicit maintenance loop around this idea: after each OKF refresh, context that now has a wiki home should be collapsed in `AGENTS.md` to a pointer; repo-specific facts and conventions should continue to live in the wiki, and any durable discovery that emerges during work should be captured as a finding page for later promotion. That practice keeps the knowledge base from drifting back into duplicate operational notes.

## Practical guidance

When deciding whether something belongs in durable context, ask:

- Will this still matter in future sessions or after personnel changes?
- Is it a fact, rationale, evidence, or standing validation rule rather than a one-time instruction?
- Should an agent consult this before acting again?
- Does it explain why a workflow, structure, or policy exists?
- Would losing this make future regeneration, validation, or auditability weaker?
- Would a future subagent need this information to know its purpose, relevant context, or permission limits?

If the answer is yes, it likely belongs in durable context rather than only in a prompt, temporary note, or command transcript.

Durable context is especially valuable when it records not only project facts but also the repository's operating contract: what files are authoritative, how evidence is cited, which link forms are expected, what quality checks are enforced, which local policy exceptions apply, how recurring agent roles should interpret and use that information, and what tooling bootstrap sequence the repository expects. Those details turn a knowledge base from passive documentation into an actively maintainable system.

## See also

- `AGENTS.md`
- [[concepts/agent-context-layering]]
- [[concepts/documentation-architecture]]
- [[concepts/skill-based-automation]]
- [[concepts/external-documentation]]
- [[concepts/provenance-tracking]]
- [[concepts/source-driven-regeneration]]
- [[concepts/offline-first-workflows]]
- [[concepts/spec-authority]]
- [[concepts/permission-scoped-agents]]
- [[concepts/subagent-role-design]]
- [[concepts/agents-md-maintenance]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/generated-content-governance]]
- [[concepts/source-provenance]]
- [[concepts/consent-first-tooling]]
- [[concepts/preflight-checks]]
- [[concepts/project-scaffolding]]
- [[concepts/quality-gates]]
- [[concepts/context-surface-management]]
- [[concepts/progressive-disclosure]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/documentation-architecture]]
- [[concepts/skill-based-workflow]]

## Related Documents

- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/README-md]]