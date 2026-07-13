---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__graphify__references__transcribe-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__graphify__-graphify_version.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__skill-creator__assets__skill-template-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md"]
description: "Reusable skills encode repeated agent work as governed, executable procedures."
---

# Skill-Based Automation

Skill-based automation is the practice of encoding recurring agent tasks as reusable, project-scoped procedures instead of leaving them scattered across routing files, generated knowledge pages, or ad hoc prompts.

## Core idea

In an agent-ready repository, repeated work should be classified by what it is for. Facts and rationale belong in durable context, routing and operational basics belong in `AGENTS.md`, and repeatable execution belongs in skills. That separation keeps the repository easier to reason about and helps agents operate with less ambiguity.

This concept is grounded in [[concepts/agent-ready-context-skill]] and relates closely to [[concepts/durable-context]], [[concepts/documentation-architecture]], [[concepts/agent-context-layering]], and [[concepts/agent-ready-repositories]]. The bootstrap guidance makes the layering explicit: `AGENTS.md` is for routing and operational basics, `okf/wiki/` is for durable knowledge, `graphify-out/` supports structural exploration, and `.agents/skills/` holds reusable actions. Within that model, skills are where the agent or harness carries out repeated procedures, while the wiki remains a source of context rather than instructions.

The README for agent-smith reinforces that model by describing a repository as having three distinct surfaces: orientation in `AGENTS.md`, durable memory in `okf/wiki/`, and actions in `.agents/skills/`. It also frames harness adapters as runtime-only projections, not source of truth. That makes skill-based automation part of a broader [[concepts/context-action-separation]] pattern rather than a standalone convenience.

The newer profile-intent examples make the layering easier to operationalize by showing how reusable roles can be defined in a portable, harness-agnostic way. In those examples, an `okf-curator` maintains durable context, a `skill-architect` decides when repeated actions should become skills and then creates or updates them, and a `repo-cartographer` performs read-only repository reconnaissance before OKF changes. That division of labor reinforces that skill-based automation is not just about writing procedures; it is also about deciding which recurring work belongs in the execution layer, which belongs in durable context, and which should remain exploratory. It connects this concept directly to [[concepts/subagent-role-design]], [[concepts/permission-scoped-agents]], and [[concepts/tool-boundaries]].

The skill-creator guidance makes that operational boundary more exact. It defines a skill as a reusable action capability rather than a knowledge base or narrative memory, and it explicitly separates skills from durable context in OpenKB and from orientation material in `AGENTS.md`. It also sharpens the distinction between project-owned skills and vendored third-party skills: local skills under `.agents/skills/<skill-name>/` are the place for repository-specific procedure, while vendor skills are dependencies that remain read-only unless wrapped by a companion skill. In practice, skill-based automation depends not only on deciding what should become a skill, but also on preserving the distinction between custom procedures, compiled knowledge, and external dependencies under clear governance rules.

The agent-ready bootstrap reference also adds concrete repository-shaping guidance. It says `AGENTS.md` should stay short and focused on routing, setup, and test commands; that durable facts belong in `okf/wiki/`; that `graphify-out/` is only an exploration aid; and that skills should absorb repeated executable behavior once the repository has enough OKF context to reveal those patterns. That makes skill-based automation part of the repository's maintenance loop, not just a design preference.

The README's installation and usage sections turn that design into an explicit workflow. The repository is made agent-ready by copying the three product skills, then asking the harness to bootstrap or refresh the repo. The result is a repository that can be maintained through a repeatable cycle: orient, compile knowledge, surface repeated actions, and promote them into skills when they recur often enough.

The skill template source and the skill initializer make that operational role more concrete. They show that a reusable skill is not just an idea but a structured artifact with stable metadata, a clear action statement, an ordered workflow, concrete commands, and explicit edge-case handling. The initializer further reinforces this by scaffolding a normalized, repository-scoped skill directory with a starter `SKILL.md`, default metadata, and optional `scripts`, `references`, and `assets` folders. The newer skill-creator document extends that model by arguing that `SKILL.md` should stay short and procedural, while heavy detail lives in `references/`, deterministic logic in `scripts/`, and templates or static resources in `assets/`. The testing guidance extends that definition: a skill is not complete merely because it is documented in the right format, but because it has been exercised against realistic failure conditions that reveal whether it actually changes agent behavior. The vendor skill management guidance adds a second boundary: not every reusable procedure should be authored or edited in the same way. Some skills are external dependencies that must remain pinned and read-only, while others are project-owned automation maintained locally.

The OKF suggestion script adds another important operational lens. It treats skill discovery as a repository-observation task: scan compiled wiki pages, look for repeated action-heavy language, filter out mostly conceptual material, and rank likely candidates for promotion into reusable procedures. That reinforces that skill-based automation is not only a top-down design choice but also a bottom-up response to repeated actions already visible in durable knowledge. The script's use of action patterns, title-derived naming, score thresholds, and evidence paths makes the promotion process transparent and reviewable rather than purely intuitive. In that sense, skill-based automation also depends on lightweight [[concepts/heuristic-classification]] to surface procedural repetition inside a knowledge base without collapsing context pages into instructions.

The Graphify add-and-watch reference extends the same idea into graph maintenance. It treats URL ingestion and folder watching as optional, non-default operations that should be invoked as explicit procedures rather than improvised each time. In that workflow, adding a URL means calling the ingestion pipeline with visible error handling, saving the fetched material into the corpus, and then running the graph update pass. Watching a folder means running a background monitor with debounce behavior and distinct branches for code-only changes versus docs, papers, or images. This is a strong example of skill-based automation because the value lies not only in the commands themselves, but in repeating the same guarded decision logic every time: fail loudly on ingest errors, auto-update after successful saves, rebuild immediately for structural code changes, and defer semantic updates when richer sources change. That ties this concept naturally to [[concepts/incremental-graph-maintenance]], [[concepts/web-evidence-ingestion]], and [[entities/graphify]].

The new merge script sharpens the same pattern from a different angle. It creates or updates `AGENTS.md` by managing only the content between `<!-- okf:start -->` and `<!-- okf:end -->`, leaving the rest of the file untouched. That makes the repository orientation layer intentionally conservative: skills may refresh the OpenKB guidance block, but they should not rewrite project-specific setup, style, test, or PR instructions. The script also encodes a clear source-ordering policy inside the managed section by directing agents to consult `AGENTS.md` first, then `okf/wiki/index.md`, then `graphify-out/` outputs, and only then `.agents/skills/`. In other words, the automation around `AGENTS.md` is itself a skill-shaped workflow: bounded, idempotent, and careful about which layer it is allowed to modify.

## What belongs in a skill

The source documents describe skills as the right place for repeatable actions such as:

- repeated commands
- multi-step operating procedures
- validation workflows
- transformations and migrations
- scaffolding tasks
- controlled evidence collection from approved external documentation sources
- environment and repository preflight checks before a workflow runs
- ingestion routines that fetch remote materials and merge them into repository context or graph state
- background monitoring workflows that react to file changes under explicit rules
- any action the agent or harness should perform the same way again

The unifying characteristic is repeatability with operational intent. A skill is for doing, not just for explaining. This matters especially when tasks cross tool boundaries, such as checking whether required tools are installed, confirming a repository is writable and inside a Git worktree, fetching official vendor documentation, staging extracted facts, ingesting them into a repository knowledge base under repeatable rules, or running a watcher that distinguishes between low-cost structural rebuilds and higher-cost semantic refreshes. In those cases, a skill can standardize how the task is carried out while preserving human intent and approval boundaries. This connects skill-based automation to [[concepts/tool-boundaries]], [[concepts/evidence-staging]], [[concepts/external-documentation]], and [[concepts/filesystem-validation]].

The new `AGENTS.md` guidance adds a concrete discovery rule: after OpenKB generation, the agent should inspect `okf/wiki/` for repeated actions and promote them into custom skills when they represent recurring executable workflows. That makes skills not just a design-time choice, but also an outcome of observing repeated operational patterns in compiled repository knowledge.

The profile-intent examples refine the same boundary by showing that a reusable action can be specified not only as a workflow artifact but also as an invocation contract. Each example is defined by purpose, use conditions, required context, and permissions. Read that way, a mature skill belongs in the repository when maintainers can say what it is for, when it should run, what sources it depends on, and what authority it needs. The `skill-architect` example is especially direct: repeated executable actions revealed by the OKF or user workflow should be turned into custom skills, while the `repo-cartographer` shows that some repeated work is intentionally read-only reconnaissance rather than mutation.

The skill template, initializer, and skill-creator guidance also clarify what a mature skill should contain once a repeated action is promoted. A project skill should identify itself clearly through fields such as `name`, `description`, `license`, and versioned `metadata`, then describe the action through a short purpose statement, a deterministic workflow, and a commands section, with supporting resource folders created only when needed. The initializer operationalizes this standard by normalizing skill names to kebab-case, constraining creation to the `.agents` hierarchy, and generating a predictable baseline structure instead of ad hoc procedure files. The skill-creator guidance adds that the `description` field should act as the trigger for when the skill is invoked, not as a compressed copy of the workflow, and that action instructions should be proportionate to task fragility: destructive or brittle tasks get tighter procedures and scripts, while more open-ended work can leave room for judgment. The testing reference adds that mature skills should also be shaped around known breakdown points: forgetting required steps, replacing deterministic scripts with fragile rewrites, mixing context with action, editing vendor skills directly, overloading `AGENTS.md` with large knowledge, or skipping validation and provenance. The vendor management reference further narrows the category: if the repeated action is project-specific, it belongs in a custom skill; if it comes from a third party, it should be treated as a dependency rather than casually absorbed into local procedure files. This reinforces that skill-based automation is not merely command reuse; it is repeatable procedure design informed by observed failure modes, ownership boundaries, naming discipline, metadata discipline, and clear validation expectations.

The skill-creator document also adds explicit security defaults for what belongs in a skill. Reusable skills should request the minimal tool scope they actually need, avoid silent software installation, keep secrets in environment variables instead of repository files, treat fetched web content as untrusted data rather than instructions to follow, and identify generated artifacts that should be gitignored. That means a mature skill is not just operationally repeatable; it also encodes safe execution boundaries. In that sense, skill-based automation aligns closely with [[concepts/minimal-tool-scoping]], [[concepts/prompt-injection-defense]], and [[concepts/tooling-consent-and-pin-management]].

The OKF suggestion script sharpens the same boundary from another angle. It scores wiki pages using action verbs and tool markers such as run, validate, build, migrate, git, docker, and python, then proposes normalized skill names from page titles or headings. If a page appears action-heavy but the derived name lacks an obvious action verb, the script prefixes it with `manage-`, making the procedural intent explicit. This captures an important practical rule: when a repeated pattern is promoted, the resulting artifact should read like an action, not like a topic. The script therefore aligns skill creation with [[concepts/naming-normalization]] and with the broader distinction between action-heavy documentation and descriptive context in [[concepts/action-oriented-documentation]].

The Graphify reference contributes two concrete examples of the same boundary. A URL-add workflow belongs in a skill because it is a sequence with parameters, typed resource handling, failure branches, and a required follow-up update. A watch workflow belongs in a skill because it is a long-running operational mode with debounce control, background execution guidance, and explicit branching based on changed file classes. Both illustrate that workflows with conditional automation logic, especially around ingestion and graph freshness, are better captured as executable procedure than as loose prose.

The merge script adds another clear example: a procedure that updates a managed section of `AGENTS.md` should remain narrowly scoped and preserve the rest of the file. That is exactly the kind of behavior that belongs in a skill, because it is deterministic, repeatable, and constrained by explicit boundaries rather than by broad document rewriting.

## What should stay outside skills

The same sources distinguish skills from durable knowledge stored elsewhere:

- `okf/wiki/` should retain architecture facts, external evidence, design decisions, workflow rationale, and provenance
- `AGENTS.md` should stay short and focus on routing rules, setup or test commands, and pointers to major context locations
- fetched documentation content should be preserved as staged evidence rather than embedded directly into procedural instructions
- diagnostics produced by a skill can guide action, but the lasting policy and rationale belong in durable documentation rather than being buried in executable logic alone
- Graphify outputs should support file discovery and structural understanding, not become the final authority for behavior or policy
- vendor skills should remain immutable dependencies rather than serving as the place where repository-specific policy is edited into third-party content
- ingested remote artifacts such as tweets, PDFs, webpages, images, and transcriptions should remain corpus material, not be collapsed into the skill that fetched them
- watch-mode status markers such as `graphify-out/needs_update` should signal follow-up work, not replace the durable record of why semantic refresh is needed
- the managed `AGENTS.md` section should not absorb the project's custom setup, style, test, or PR instructions outside the OKF block

This split helps prevent procedural clutter from overwhelming durable context and supports a more maintainable repository knowledge structure. It also keeps source material and execution logic separate: skills define how to perform a workflow, while the wiki and staged evidence preserve what was learned and where it came from. Related ideas include [[concepts/durable-context]], [[concepts/provenance-tracking]], and [[concepts/source-driven-regeneration]].

The template source reinforces this boundary by keeping skills concise and action-centered, and the initializer does the same by generating a short procedural `SKILL.md` with workflow and command placeholders rather than long-form explanatory sections. Metadata identifies and governs the skill, while the body focuses on procedure.

The skill-creator guidance sharpens this boundary further by explicitly saying that a skill is not a knowledge base and not a narrative memory. It warns against duplicating context already present in OpenKB and instead favors linking to repository context only when the action genuinely depends on it. It also rejects auxiliary files such as `README` or `CHANGELOG` inside a skill, which keeps the skill contract narrow and prevents local procedure directories from turning into parallel documentation silos.

The profile-intent examples support the same split by separating maintenance of durable context from maintenance of reusable procedures. The `okf-curator` exists to keep `okf/wiki/` current and evidence-backed, while the `skill-architect` exists to extract repeated executable behavior into `.agents/skills/`. That distinction is useful because it keeps the durable context layer authoritative without turning every recurring maintenance pattern into embedded prose. It also reinforces that repository exploration, context curation, and procedure authoring can be distinct responsibilities with different permissions.

The testing guidance sharpens the same boundary in another way: when a failure stems from missing discipline during execution, the answer is often a focused procedural skill, but when the material is explanatory or archival, it belongs in durable repository context instead. The vendor-management guidance adds that repository-specific changes should not be hidden inside third-party skill files; they should be expressed as companion custom skills that preserve upgradeability and provenance. Skill-based automation therefore depends on keeping context and action separate, and also on keeping project ownership separate from vendored dependencies, so that a skill can consume repository knowledge without swallowing it and can extend external capability without mutating it in place.

The OKF suggestion script makes this boundary explicit in code. It skips `sources/`, generated `reports/`, and reserved files such as `index.md` and `log.md`, because those areas are not the right substrate for discovering reusable actions. It also filters out pages dominated by terms like architecture, decision, overview, concept, or external documentation unless they include fenced code blocks. This reflects a useful principle: explanatory pages can inform skills, but not every informative page should become one. Skill-based automation works best when procedural extraction is selective and when durable context remains durable context.

The Graphify add-and-watch guidance reinforces this split in practical terms. The skill should explain how to invoke ingestion or watch behavior, but the downloaded PDF, saved tweet Markdown, fetched webpage, extracted image, or resulting graph artifacts are outputs and evidence, not part of the skill definition itself. Likewise, the distinction between code-only changes and semantic sources belongs in the procedure logic, while the repository's broader rationale for graph maintenance frequency or corpus policy belongs in durable documentation.

The merge script adds a similar reminder for repository orientation: it updates only the OpenKB-managed block and leaves repository-specific guidance intact. That is a concrete instance of a broader rule that procedural automation should be bounded and conservative rather than rewriting the whole document surface.

## Role in an agent-ready repository

Skill-based automation is part of a broader repository operating model:

- `AGENTS.md` routes the agent
- `okf/wiki/` preserves stable knowledge
- structural or generated outputs support understanding and validation
- skills capture repeated execution patterns
- evidence staging captures facts gathered from external sources in a reviewable form
- preflight procedures confirm that repository and tool prerequisites are satisfied before heavier workflows begin
- vendor skills provide pinned external procedures without becoming editable local policy
- custom skills hold repository-owned behavior and wrappers around external capabilities
- graph maintenance skills coordinate ingestion, update passes, and watcher behavior without turning graph state into policy

This layering reduces ambiguity. Agents can use concise routing guidance to find durable context, while relying on skills for actions that should be standardized. It is especially useful for tasks that mix retrieval, filtering, provenance capture, environment checks, ingestion, and conditional graph refresh, because those tasks benefit from a consistent sequence and clear stopping rules. In practice, a preflight skill can distinguish hard blockers from optional enhancements, report machine-readable and human-readable diagnostics, and fail early when the repository is not ready. A graph maintenance skill can likewise distinguish between changes that justify immediate structural rebuilds and changes that should raise a deferred semantic-update flag. This improves consistency and complements [[concepts/deterministic-validation]], [[concepts/quality-gates]], [[concepts/graceful-degradation]], and [[concepts/cross-platform-tooling]].

The newer guidance sharpens the role of skills in this layered model. It explicitly instructs agents to consult `AGENTS.md` first, then `okf/wiki/`, then Graphify outputs, and only then `.agents/skills/` for reusable procedures. That ordering does not diminish skills; instead, it clarifies that skills should execute repeatable workflows using repository rules and durable context as inputs, rather than replacing those sources.

The profile-intent document adds a complementary execution pattern: repositories may also benefit from role-specialized subagents that occupy different positions in the same layered model. A `repo-cartographer` can map files and flows read-only before any write-heavy work begins, an `okf-curator` can maintain durable context and evidence pages, and a `skill-architect` can formalize repeated actions into durable automation. In other words, skill-based automation can apply both to standalone repository procedures and to role-scoped execution profiles that decide when and how those procedures are used. This strengthens the connection between reusable skills and [[concepts/subagent-role-design]].

The template and initializer support this role by modeling a predictable internal layout for each skill and a predictable directory structure for creating one. Workflow steps and commands are separated explicitly, while optional support directories can be created in a standard way. The initializer's path guardrails and name normalization further signal that skills are repository infrastructure, not arbitrary scratch files. The skill-creator guidance adds that every skill should be validated before completion and that the validation loop should include not just format correctness but operational soundness. The testing document completes that operational picture by requiring at least one pressure scenario before considering a skill complete. The vendor management document adds repository-scope discipline: skills may live in the same directory tree, but vendored external skills and locally maintained custom skills play different roles in the execution layer and should be handled differently. In this model, a skill is part of the repository's execution layer only when it can withstand realistic prompts that previously led the agent off course and when its ownership model is clear enough to support safe updates. That ties skill-based automation directly to [[concepts/baseline-first-testing]] and [[concepts/failure-driven-development]].

The OKF suggestion script fits this operating model as a bridge between context and action. It inspects compiled wiki pages, tallies action-oriented evidence, and prints candidate skill names together with supporting source paths and a ready-to-run initializer command. That means the repository can treat its compiled knowledge not only as reference material but also as an input to the next automation pass. In layered terms, `okf/wiki/` remains the context layer, while the suggestion workflow helps identify where the execution layer is still missing structure.

The Graphify reference adds a further operational example of this layer separation. The corpus and graph outputs remain context-supporting artifacts, but the procedures for adding new remote material or keeping the graph fresh under file change are execution-layer concerns. Encoding those steps as skills keeps graph maintenance repeatable without promoting transient watcher state or downloaded source files into the repository's policy layer.

The merge script extends this model into document maintenance: it encodes a bounded update mechanism for `AGENTS.md`, preserving the repository's own instructions while refreshing the managed OKF block. That is the same execution-vs-context split applied to orientation text instead of to graph or ingestion workflows.

## Skill discovery after OKF generation

A key point from the source is that the first OpenKB generation pass is not only documentation work. It is also a discovery phase for identifying repeated operational behavior.

After `okf/` exists, the repository team or agent should inspect the generated knowledge base for workflows that appear often enough to warrant formalization as skills. This includes not only internal maintenance patterns, but also recurring evidence-gathering tasks such as consulting official vendor documentation for topics already present in the repository, repeatedly checking that the local environment has the required tooling and writable paths for repository operations, repeatedly ingesting remote resources into a corpus, or repeatedly deciding whether changed files need immediate rebuilds or deferred semantic updates.

The newer `AGENTS.md` guidance makes this explicit by directing maintainers to review generated wiki pages for repeated actions after OKF generation and then create or update custom skills accordingly. The recommendation is to keep context in the wiki while moving recurring executable patterns into `.agents/skills/`.

The profile-intent examples make the same discovery loop more legible at the role level. The `skill-architect` is explicitly triggered when the OKF or user workflow reveals repeated executable actions, while the `repo-cartographer` gathers the repository understanding that often precedes confident extraction. This implies that post-OKF skill discovery is not just textual pattern matching; it can also be a deliberate handoff from exploration, to durable context maintenance, to procedural formalization under separate permissions and scopes.

The skill-creator guidance turns that recommendation into a specific workflow: scan for true actions, check whether an existing skill already covers them, initialize a new project-local skill when needed, test it baseline-first, and run quick validation before considering it done. It also explicitly allows OpenKB content to drive skill discovery through a dedicated suggestion script while insisting that facts, design decisions, architecture, and external documentation remain in the wiki rather than being converted into procedures.

The merge script contributes a related maintenance rule: when source files, architecture, CI/CD, security controls, external documentation assumptions, or repeated agent actions change, the managed orientation section should be refreshed rather than expanded into a duplicate knowledge base. That keeps the repository's routing layer current without turning it into a substitute for the wiki or the skills directory.

In this sense, documentation and automation reinforce each other:

- the wiki reveals recurring patterns
- recurring patterns can be promoted into reusable procedures
- external research workflows can be turned into repeatable evidence-staging routines
- environment readiness checks can be turned into repeatable preflight routines
- graph ingestion and watch workflows can be turned into explicit maintenance procedures instead of ad hoc operator memory
- managed `AGENTS.md` sections can be refreshed without rewriting project-specific guidance
- generated maintenance workflows can reveal where standardized execution is missing
- the resulting skills reduce future repetition and drift

This makes skill-based automation a natural extension of [[concepts/source-driven-regeneration]] and a practical outcome of well-structured [[concepts/documentation-architecture]].

The template and initializer add a useful implication: once a recurring pattern is promoted, it should be normalized into a standard skill shape rather than captured as a one-off note. Consistent metadata, sectioning, kebab-case naming, and a predictable directory layout make discovered workflows easier to compare, revise, and validate across a repository.

The testing source adds a second implication: discovery should be followed by targeted validation, not immediate rule accumulation. A newly promoted workflow should first be run without the skill to establish a baseline failure, then updated minimally to address that concrete behavior, and then rerun to close loopholes. This keeps discovered skills narrow, evidence-based, and easier to maintain.

The vendor-management guidance adds a third implication: discovery does not automatically mean invention from scratch. Some repeated capabilities may already exist as external skills, in which case the repository can vendor a pinned read-only copy and surround it with project-owned companion skills for local rules, validation, or caveat handling instead of duplicating or patching the dependency.

The OKF suggestion script makes this discovery process more concrete. It recursively scans Markdown pages in the wiki, ignores administrative and generated areas, scores pages against action regexes, and aggregates candidate names with evidence from up to several source pages. Its threshold-based ranking turns "this page feels procedural" into a reproducible suggestion process, while still leaving the final decision to a human or maintainer. That matters because not every repeated phrase should become a skill, but repeated action signals across multiple pages are strong evidence that a workflow may deserve standardization. In this way, post-OKF skill discovery becomes a form of [[concepts/repository-ingestion]] feedback: the repository ingests and compiles knowledge, then mines the resulting structure for automation opportunities.

The Graphify add-and-watch reference provides a clear example of what this discovery can surface. A repository that repeatedly adds URLs to a corpus, then manually remembers to update the graph, or repeatedly restarts a watcher and interprets change types, is showing the exact kind of repeatable operational pattern that should be promoted into a skill. The existence of typed URL support, explicit post-save update rules, debounce settings, and different reactions to code versus document changes makes the workflow especially suitable for formalization.

The merge script is similarly discoverable as a repeated maintenance pattern: update only the managed section, preserve the surrounding instructions, and keep the orientation file concise. That pattern is a good candidate for reuse because it is both recurring and rule-bound.

## Vendor skills and custom skills

The source documents distinguish two kinds of skills:

- vendor skills are read-only dependencies managed through a skill manager and preserved with their lock file when applicable
- custom skills are project-owned procedures kept in `.agents/skills/` and updated as recurring needs emerge

Vendor skills should not be edited directly. If project behavior must differ, the recommended approach is to create a wrapper or companion skill instead. This preserves upgradeability while allowing repository-specific behavior.

The updated `AGENTS.md` guidance reinforces the same rule: vendor skills are dependencies, not local policy files, so repository teams should install or update them through the chosen manager and keep any generated lock file. Repeated actions discovered during OKF maintenance should become custom skills rather than modifications to vendored ones.

The vendor management reference makes this distinction more exact. Vendored third-party skills and adopted generated skills can both appear under `.agents/skills/`, but they follow different rules. Vendored third-party skills remain read-only and should be updated only by re-vendoring a reviewed, pinned version. Adopted generated skills become project-owned at adoption, must pass validation, and can then be edited like any other custom skill. The skill-creator guidance reinforces this split by treating adoption as an explicit copy-and-validate step from build output into the spec-compliant project skill location, not as an automatic overwrite of existing repository procedure. This means skill-based automation includes not just procedure design but ownership transitions: some procedures stay external, some are local from the start, and some are generated elsewhere and only later become repository-maintained.

That source also introduces a caveat-preservation review for adopted generated skills. Because LLM distillation can flatten conditional guidance into unconditional instructions, a repository should compare an adopted skill against the originating wiki pages and underlying sources, then restore any lost boundaries such as "only when" conditions, explicit prohibitions, or scope limits. This links skill-based automation directly to [[concepts/caveat-preservation]] and makes adoption a governance step, not just a file copy.

The profile-intent examples add a useful ownership lens here too. Their permission sections treat access limits as part of the role contract, not an afterthought. The `okf-curator` may read freely but only write to OKF or `AGENTS.md` under user policy, the `skill-architect` may write `.agents/skills/` according to policy, and the `repo-cartographer` is read-only by default. This mirrors the vendor/custom split: repository automation is safer when maintainers define not only what a skill does, but also what kinds of roles or procedures are allowed to mutate which layers.

The preflight-check pattern adds an important nuance: project-owned skills often encode local assumptions about required tools, optional tools, writable directories, and companion skills. That kind of repository-specific readiness logic belongs naturally in custom skills rather than in generic vendor dependencies. The initializer supports that local ownership model by bootstrapping project skills with versioned metadata and by allowing optional support folders without assuming every skill needs the same resource footprint.

The Graphify add-and-watch workflow shows the same point. A repository-specific skill may wrap `graphify` with local paths such as `./raw`, local authoring rules, or local expectations about when to run `--update` and when to leave a `needs_update` flag for later. Those repository rules belong in a custom skill even if the underlying graph tooling is external.

The merge script is also a repository-owned procedure rather than a vendored dependency. It manages a local orientation section and is meant to be run through the repository's own maintenance workflow, which makes it a good example of custom automation that preserves project-specific content while updating a shared OpenKB block.

The testing guidance makes this distinction operational as well. One of the explicit pressure-scenario failure modes is editing vendor skills directly, which means custom skills should absorb repository-specific counters, wrappers, and discipline rules instead of patching dependencies in place. This distinction supports reliable automation and aligns with controlled tooling practices such as [[concepts/tooling-consent-and-pin-management]], [[concepts/dependency-management]], [[concepts/version-pinning]], [[concepts/integrity-pinning]], and [[concepts/supply-chain-security]].

The template and initializer are especially relevant for custom skills because they provide a baseline shape for project-owned procedures. The workflow and command sections help custom skills evolve without losing clarity, while the initializer's overwrite guard reflects that local skills are maintained artifacts rather than disposable generated output.

The OKF suggestion script reinforces the same split by ending in a custom-skill bootstrap step rather than editing existing skills in place. For each ranked candidate, it prints an `init_skill.py` command with a normalized name and standard resource folders, nudging maintainers toward repository-owned implementation rather than ad hoc patching. In practice, this means the discovery pipeline can suggest what to automate, but ownership and dependency discipline still determine where the resulting procedure belongs.

## Benefits

Skill-based automation provides several repository-level advantages:

- improves consistency for repeated tasks
- reduces prompt duplication and undocumented operator judgment
- keeps durable knowledge separate from executable procedures
- makes recurring workflows easier to validate and evolve
- helps agents act with less ambiguity and less context sprawl
- standardizes safe handling of external sources, provenance, and trust decisions
- enables early preflight detection of missing prerequisites, unwritable paths, and absent companion tooling
- supports clear separation between hard requirements and optional enhancements
- turns repeated OKF maintenance behavior into reviewable, reusable repository procedures
- preserves upgradeability by separating pinned vendor dependencies from local procedural extensions
- makes graph ingestion and watch behavior predictable by encoding post-save updates, debounce rules, and semantic-versus-structural change handling
- keeps `AGENTS.md` concise by moving repeating procedures into skills instead of expanding orientation text indefinitely
- enables conservative document mutation by limiting managed sections to explicit markers

When used for external-documentation workflows, skills can also help ensure that only approved URLs are fetched, official sources are preferred, provenance is recorded, and extracted facts are staged instead of acted on directly. When used for repository readiness, skills can similarly ensure that required tooling such as `git` and `uv` is checked consistently, optional tools are surfaced with actionable notes, and degraded modes are treated explicitly rather than silently assumed. When used for Graphify maintenance, skills can ensure that ingest failures are surfaced immediately, supported remote resource types are handled through one repeatable entry point, code-only edits trigger low-cost structural refreshes, and richer document changes set an explicit follow-up marker instead of silently drifting out of sync. When used for `AGENTS.md` maintenance, skills can ensure that the repository's orientation block stays current without rewriting the rest of the file. That makes skills a practical mechanism for reinforcing [[concepts/prompt-injection-defense]], [[concepts/source-trust-levels]], [[concepts/privacy-preserving-tooling]], [[concepts/tooling-context-isolation]], and [[concepts/tooling-consent-and-pin-management]].

The newer guidance also ties skills to safer generated-content workflows. Because OpenKB maintenance involves staged evidence, dry-run previews, approval gates, and final validation, encoding that sequence as reusable skills helps preserve review discipline across repeated runs. This links skill-based automation to [[concepts/generated-content-governance]], [[concepts/data-flow-disclosure]], and [[concepts/incremental-compilation]].

The profile-intent examples add another benefit: they show that reusable automation can be described in a portable way before being translated into harness-native files. That portability makes it easier to preserve intent across tools while keeping purpose, invocation conditions, context dependencies, and permissions explicit. In practice, this reduces the chance that an execution profile drifts into an underspecified prompt blob and supports clearer [[concepts/permission-scoped-agents]] and [[concepts/subagent-role-design]].

The vendor-management guidance adds a supply-chain benefit: third-party skills are treated as executable dependencies that deserve source verification, license review, script inspection, and pinned installation rather than casual trust. Handling skills this way reduces drift, improves auditability, and keeps repository-specific logic in custom layers that can evolve without obscuring the provenance of upstream behavior.

The template and initializer add a maintenance benefit as well: consistent skill formatting and scaffolding make procedures easier to review, transfer, and update. A standard body shape with deterministic steps, explicit commands, named resource folders, constrained write paths, and normalized names reduces ambiguity for both humans and agents, which strengthens repeatability and complements [[concepts/deterministic-validation]] and [[concepts/naming-normalization]].

The skill-creator guidance adds another benefit: safe defaults become portable. Minimal tool scopes, explicit handling for untrusted fetched content, secret hygiene through environment variables, and explicit artifact handling can all be baked into the procedure itself instead of being rediscovered in each run. That makes reusable skills a practical way to standardize execution safety, not just execution order.

The testing document adds another benefit: skills become more robust when they are built around actual failure pressure rather than idealized instructions. Pressure scenarios expose skipped validation, brittle manual rewrites, context-action confusion, and provenance gaps before those problems are repeated in production workflows. Baseline-first testing also helps keep skill content minimal, because new rules are added only to address observed failures.

The OKF suggestion script adds a discovery and governance benefit. Because it emits ranked candidates with source evidence and a reproducible initializer command, it reduces the chance that reusable procedures are invented arbitrarily or named inconsistently. Teams can inspect the evidence, decide whether a candidate is truly procedural, and then scaffold a repository-owned skill in a standard form. This improves auditability and helps keep the boundary between context mining and action authoring explicit.

The merge script adds a maintenance benefit too: it lets the repository refresh the OpenKB-managed portion of `AGENTS.md` without disturbing project instructions outside the managed block. That lowers the cost of keeping orientation current and reduces the risk of accidental overwrites.

## Practical interpretation

A useful rule is:

- if the content explains why something exists or records facts about the repository, keep it in durable documentation
- if the content tells an agent how to repeatedly perform a task, consider making it a skill
- if the task involves external documentation, use the skill to constrain fetching, extraction, trust recording, and staging rather than treating fetched pages as instructions
- if the task must verify environment or repository readiness before proceeding, encode those checks as a repeatable preflight skill instead of relying on informal operator memory
- if generated wiki output repeatedly exposes the same action pattern, promote that pattern into a custom skill instead of leaving it scattered across context pages
- if action-heavy wiki pages repeatedly match operational verbs and tool patterns, use that evidence as a signal for skill discovery rather than relying only on intuition
- if the candidate page is mostly conceptual, architectural, or descriptive, keep it in the wiki even if it discusses workflows
- if a reusable capability comes from a third party, treat it as a pinned dependency, review it like executable guidance, and avoid editing it directly
- if project-specific behavior is needed on top of an external skill, create a companion custom skill rather than patching the vendored copy
- if a generated skill is adopted into the repository, validate it and compare it against its source material to restore any flattened caveats or lost boundaries
- if a skill is created, scaffold it in a stable location with a normalized name, clear metadata, an ordered workflow, concrete commands, and only the supporting resource folders it actually needs
- if the skill uses Python scripts, prefer running them with `uv run` when available so execution stays isolated from the target repository environment
- if the derived skill name is descriptive rather than action-oriented, rename it or normalize it so the procedure reads like an action
- if the skill seems complete, test it with at least one realistic pressure scenario that reproduces a known failure mode
- if the first draft still leaves loopholes, add explicit counters that explain the reasoning behind the constraint, not just the prohibition
- if the skill requests tools or installation steps, scope them minimally and require explicit, pinned, user-scoped installation guidance
- if the skill fetches web content, treat that content as untrusted data rather than instructions to follow
- if the skill generates artifacts, list them and ensure the repository ignores them appropriately
- if validation is available, run the repository's quick validation step before treating the skill as done
- if a repeated workflow is better expressed first as a reusable role contract, define its purpose, use conditions, context inputs, and permission limits before translating it into harness-native files
- if repository exploration is needed before automation, keep that reconnaissance read-only and separate from write-capable maintenance or skill-authoring steps
- if a workflow repeatedly adds remote sources into a graph corpus, encode the ingest command, parameter handling, supported resource expectations, error reporting, and required post-ingest update as one reusable procedure
- if a workflow repeatedly watches a folder for graph-affecting changes, encode debounce timing, background execution expectations, and the distinction between immediate structural rebuilds and deferred semantic refreshes as explicit procedure logic
- if a watcher produces a follow-up marker such as `needs_update`, treat that marker as a trigger for another governed step rather than an implicit guarantee that the graph is current
- if a repository orientation file has a managed OpenKB section, update only that section and leave project-specific guidance intact

Used this way, skill-based automation strengthens the relationship between routing guidance, durable knowledge, repeatable execution, readiness validation, safe evidence handling, dependency discipline, heuristic discovery, permission-scoped role design, and caveat-preserving skill maintenance in an agent-ready repository.

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]]

See also: [[summaries/agents__skills__skill-creator__assets__skill-template-md]]

See also: [[summaries/agents__skills__skill-creator__references__action-vs-context-md]]

See also: [[summaries/agents__skills__skill-creator__references__dependencies-md]]

See also: [[summaries/agents__skills__skill-creator__references__source-attribution-md]]

See also: [[summaries/agents__skills__skill-creator__references__testing-skills-md]]

See also: [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md]]

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__graphify__-graphify_version]]

See also: [[summaries/agents__skills__graphify__references__add-watch-md]]

See also: [[summaries/agents__skills__graphify__references__github-and-merge-md]]

See also: [[summaries/agents__skills__graphify__references__hooks-md]]

See also: [[summaries/agents__skills__graphify__references__query-md]]

See also: [[summaries/agents__skills__graphify__references__transcribe-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/repo-snapshot]]