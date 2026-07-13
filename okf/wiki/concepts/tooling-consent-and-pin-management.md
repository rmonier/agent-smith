---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Governed, pinned, and reviewable tooling adoption for agent workflows."
---

# Tooling Consent and Pin Management

Tooling Consent and Pin Management is the practice of introducing, installing, updating, configuring, vendoring, routing, and operating repository tooling only through explicit user approval, exact version selection, approved sourcing, recorded integrity, explicit runtime routing, managed lock artifacts, and clear scope boundaries so agent workflows stay reviewable, reproducible, privacy-aware, and resistant to supply-chain surprises.

## Core idea

In the source guidance captured by [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]], agents are not allowed to treat tool installation as a routine background action. Instead, they must treat it as a governed step that requires consent, exact version choices, traceable records, and explicit trust boundaries. The template also sharpens where this policy lives: `AGENTS.md` is the orientation index for setup commands, repo rules, and safety notes; durable context belongs in `okf/wiki/`; and reusable actions belong in `.agents/skills/`. That makes tooling governance part of the repository's [[concepts/documentation-architecture]], not just a packaging detail.

The same template adds an explicit context order: agents should consult `AGENTS.md` first, then `okf/wiki/`, then Graphify outputs, then `.agents/skills/`. It also says wiki content should be treated as data rather than instructions, while Graphify outputs are navigation aids rather than final authority. That means tooling policy is tied not just to installation, but to authority boundaries and [[concepts/documentation-source-priority]] across the repository.

The bootstrap guidance in [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]] reinforces the same rule at repository setup time: prerequisite checks come first, missing tools are installed only after user agreement, and version provenance is handled through pinned package references and dependency rules. It also turns the repository layout itself into part of the consent model by establishing `AGENTS.md`, `okf/wiki/`, `graphify-out/`, and `.agents/skills/` as distinct surfaces with different authority. Bootstrap is therefore not just about getting commands to run; it is about setting up a repository whose toolchain, knowledge surfaces, and automation boundaries remain inspectable and reviewable.

The dependency reference in [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] sharpens the model by separating metadata from executable truth. `SKILL.md` must stay spec-compliant and should not invent a non-standard dependency field. Compatibility notes and `allowed-tools` may describe expectations, but they are not install manifests and they do not prove local readiness. Instead, prerequisite scripts are the source of truth for whether local CLIs, writable repository paths, and optional capabilities are actually available. The same document also frames companion skills as useful follow-on capabilities rather than runtime blockers, which keeps the workflow consent-driven even when additional automation is available. This connects the concept directly to [[concepts/spec-authority]], [[concepts/dependency-management]], [[concepts/executable-validation]], and [[concepts/tool-boundaries]].

The README summary in [[summaries/README-md]] broadens the same architecture into the repository's public framing. It presents the stack as a three-surface system: `AGENTS.md` for orientation, `okf/wiki/` for durable context, and `.agents/skills/` for actions, with harness-native files treated as runtime projections rather than sources of truth. That framing matters here because tooling policy is not just about package installation; it is about preserving the boundary between routing, knowledge, execution, and runtime adaptation so that each layer is loaded and trusted only when needed. This ties the concept directly to [[concepts/context-action-separation]], [[concepts/documentation-architecture]], [[concepts/progressive-disclosure]], [[concepts/harness-native-profiles]], and [[concepts/single-source-of-truth]].

The newer skill-creator dependency guidance in [[summaries/agents__skills__skill-creator__references__dependencies-md]] extends that same discipline to skill authoring itself. It explicitly forbids inventing a non-standard `dependencies` field in `SKILL.md`, keeps dependency detail in `references/dependencies.md`, requires local prerequisite logic in `scripts/check_prereqs.py` when needed, treats `allowed-tools` as a narrow permission hint rather than an installer, and standardizes namespaced metadata keys for companion skills, vendor skills, prerequisite checks, and dependency guidance. This makes dependency expression itself part of consent and pin management: the manifest stays portable, while installable or local state is handled through explicit references, checks, and manager-owned artifacts.

The source-attribution note in [[summaries/agents__skills__skill-creator__references__source-attribution-md]] adds important design rationale for why this policy is so strict. It makes clear that the skill-creator workflow is adapted from upstream skill systems rather than invented from scratch, but intentionally hardens them with vendor-neutral repository layout, an OpenKB boundary between action, context, and orientation, consent-first version-pinned installs, integrity recording, registry-agnostic commands, secret hygiene, minimal scoped permissions, artifact gitignoring, vendor-skill immutability, lockfile policy, and `uv`-first execution. This places tooling consent and pin management inside a broader adaptation strategy for repository-safe automation rather than treating it as a standalone install rule.

The skill summary in [[summaries/agents__skills__agent-ready-context__SKILL-md]] expands this into a full repository policy. It says missing tooling may be bootstrapped only with explicit consent, and that the operator must present package name, configured index, upstream source, pinned version, and integrity pin procedure before any install. It also makes tool usage part of a larger responsibility split: durable context belongs in `okf/wiki/`, executable procedures belong in skills, and `AGENTS.md` carries concise orientation and routing guidance. That framing keeps tool adoption tied to repository policy rather than convenience.

That same skill summary adds several operational refinements that matter directly here. It makes [[entities/uv]] the required execution path for bundled scripts, says bare `python` or `python3` should not be used when `uv` is available, and treats fallback to `python3` as an explicit degraded mode only if the user declines `uv`. It also makes OpenKB ownership of `okf/` explicit, forbids writing generated content directly into `okf/raw/` or `okf/wiki/` outside narrow exceptions, and requires deterministic staged input under `okf/.okf-build/input/` before ingestion. In practice, tool consent is not only about what gets installed, but also about which execution path, build surface, and generated-state boundary the repository is approving. This strengthens links to [[concepts/kb-root-staging]], [[concepts/deterministic-builds]], [[concepts/durable-context]], and [[concepts/generated-content-governance]].

The same summary also elevates the OpenKB dedupe registry into part of the governance model. It warns that `okf/.openkb/hashes.json` is a critical registry and that if it claims content is already ingested while generated wiki pages were lost, later `add` runs may skip content silently. That makes tooling governance inseparable from state coherence: approved tools are only trustworthy when their managed registries and generated outputs stay aligned. This directly sharpens the connection to [[concepts/hash-registry-coherence]] and [[concepts/registry-drift]].

The new skill summary in [[summaries/agents__skills__skill-creator__SKILL-md]] broadens the concept from repository bootstrap into skill creation itself. It defines every skill as an action capability rather than a context container, requires authors to keep manifests short and procedural, and says fragile or destructive workflows should be narrowed through exact scripts and explicit instructions. It also bakes security defaults directly into created skills: minimal `allowed-tools`, no silent installs, consent-first version-pinned acquisition, secrets in environment variables, fetched content treated as untrusted data, and generated artifacts explicitly identified and gitignored. In this way, tooling consent and pin management become part of the standard contract for reusable automation, not just a rule for one-time setup.

The prerequisite script summary in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] makes this operational in a more detailed way than before. It defines a preflight step that checks required runtime and tooling such as Python `>=3.11`, Git, and [[entities/uv]], verifies the repository is a Git worktree, tests writability of expected paths, and reports optional tools and companion skills separately from hard blockers. It also distinguishes optional CLIs from their vendored skill counterparts: if a tool such as [[entities/graphify]] or [[entities/openkb]] is installed but its vendored skill is missing, the script emits a note telling the user to vendor the pinned skill before first CLI use. That turns consent into a staged decision tree: first measure actual readiness, then decide what to install, then decide what must be vendored before execution. This sharpens the connection to [[concepts/preflight-checks]], [[concepts/filesystem-validation]], [[concepts/graceful-degradation]], and [[concepts/skill-vendoring]].

The newer CI template documented in [[summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml]] extends the same discipline from local setup into automation: validation tooling may be enabled in CI, but only through an explicit install step in the target repository, with clearly bounded behavior and versioned action references.

The skill lock example in [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]] adds a concrete managed-artifact layer to this concept. It shows that when skills are treated as dependencies, their lock state should capture the skill name, source identifier, pinned version or digest, and manager-generated integrity value. Just as importantly, it states that such vendor lock entries are generated by the chosen skill manager and are not meant for casual hand-editing, which reinforces the distinction between approved human decisions and machine-maintained dependency state.

The privacy and routing guidance in [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]] extends this concept beyond installation into operation. Consent is not complete once a binary is installed: users must also approve when a tool will send repository or document content off-machine, which provider or endpoint it will use, which credentials authorize that call, and whether a fully local path remains available. That makes runtime routing decisions part of the same governance model as version pins, integrity records, and managed lock files.

The workflow reference in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] turns those rules into a strict build order for repository compilation. It requires prerequisite checks before anything else, consent-first bootstrap for optional tools, vendoring of the `graphify` and `openkb` skills before first CLI use, explicit `.gitignore`, `.gitattributes`, and `.graphifyignore` coverage, Git-backed deterministic staging, Graphify refresh before source-pack creation when installed, and post-generation validation plus review after any OpenKB change. This makes tooling governance part of the actual control flow of compilation, not just a setup preface. It also ties consent and pin management directly to [[concepts/deterministic-builds]], [[concepts/incremental-compilation]], [[concepts/okf-validation]], [[concepts/human-in-the-loop-review]], and [[concepts/self-reference-control]].

The same workflow reference also shows that tool governance includes refusing structurally unsafe execution. The pipeline must stop if Git history is absent, must not proceed when an installed CLI lacks its vendored skill, must keep the KB root out of Graphify analysis, and must distinguish deterministic staging from later LLM-backed compilation. This broadens the concept from package hygiene into repository-state hygiene and controlled execution ordering.

The template summary itself adds two important operational nuances. First, it explicitly orders context sources: `AGENTS.md` first, then `okf/wiki/`, then Graphify outputs, then `.agents/skills/`. Second, it says wiki content should be treated as data rather than instructions, while Graphify output is only a structural map and not final authority. Tooling governance therefore helps preserve [[concepts/documentation-source-priority]], [[concepts/knowledge-boundaries]], and [[concepts/tool-boundaries]] as well as installation safety.

The template also contributes direct operational requirements around generated knowledge. It says generated wiki pages should not be edited directly, weak output should be fixed by improving committed source documents and re-ingesting them, and the final wiki should be validated before finishing. Those rules make tool adoption inseparable from the quality and governance of generated outputs, tying this concept closely to [[concepts/source-driven-regeneration]], [[concepts/okf-validation]], and [[concepts/generated-content-governance]].

The README also sharpens the practical scope of this concept by naming the stack's concrete runtime surfaces: `AGENTS.md`, `okf/wiki/`, `.agents/skills/`, and harness adapters. It treats harness-native files as runtime projections rather than sources of truth, which means permission, install, and pin decisions should attach first to project-owned guidance and only secondarily to harness-specific adapters. This strengthens the boundary with [[concepts/harness-native-profiles]], [[concepts/runtime-adapter-management]], and [[concepts/single-source-of-truth]].

This concept supports a larger [[concepts/agent-context-layering]] model:

- `AGENTS.md` tells the agent what rules govern tooling use, provider routing, and where durable context lives.
- the knowledge wiki preserves the durable rationale and evidence.
- reusable skills execute the workflow once consent and constraints are clear.
- prerequisite scripts establish actual local readiness before install or execution decisions are made.
- lock files preserve machine-managed dependency selections for vendored or manager-installed skills.
- CI templates operationalize approved checks without turning every tool into an unreviewed default.
- harness adapters project approved repository guidance into the active runtime without becoming the policy source.
- `graphify-out/` remains a navigation and structure aid rather than the authority for repository facts.

It also fits within a broader [[concepts/documentation-architecture]] in which operational rules, generated knowledge, structural aids, procedural automation, and runtime projections are kept distinct.

## What "consent" means

Consent means the agent should not install, upgrade, activate, vendor, rewrite lock state, or assume repository knowledge tooling on its own initiative. The source guidance requires explicit approval before bootstrapping missing tooling, and the bootstrap workflow makes that concrete by requiring prerequisite confirmation before any install step for tools such as [[entities/openkb]], [[entities/graphify]], and [[entities/uv]]. The CI template follows the same pattern by presenting validation as a copy-in workflow template rather than silently assuming it should be active everywhere.

The README summary in [[summaries/README-md]] strengthens that definition by describing the stack as consent-first even when the end goal is to make the repository agent-ready. The repository may be transformed substantially, but not implicitly: installs, provider-backed compilation, generated graph analysis, and generated runtime adapters are all framed as deliberate, user-approved steps. This makes repository shaping itself a consent boundary, not just package acquisition.

The template summary adds further specificity. It says agents should read the relevant skill first, confirm prerequisites, and bootstrap missing tooling only with user consent. It also says adopting [[entities/graphify]] or [[entities/openkb]] includes vendoring their read-only skills under `.agents/skills/` before first CLI use, so consent covers both installing binaries and adopting repository-local automation dependencies.

The template also makes consent extend to expensive or destructive knowledge operations after installation. It says agents must ask before large adds, URL or PDF ingestion, `remove`, `recompile`, `lint`, `lint --fix`, `query --save`, `visualize`, and Skill Factory commands, and it expects dry runs before `remove` and `recompile`. Consent therefore governs not only tool adoption but also high-impact use of approved tools, reinforcing [[concepts/safe-automation]] and [[concepts/quality-gates]].

The bootstrap guidance adds that consent also covers repository layout changes and staged build output. The suggested sequence creates intermediate build material under `okf/.okf-build/`, generates or refreshes `graphify-out/`, initializes `okf/`, and may add external evidence before compilation. Because these actions shape repository state and future automation surfaces, they are part of the same approval boundary as package installation.

The dependency guidance makes the disclosure package more explicit. Before a first-time install, the user should be shown the tool, why the workflow wants it, its verified package name on the configured registry, its upstream source, its pinned version, and the exact command to be run. The user then chooses per tool whether they install it themselves, the agent runs the command, or the capability is skipped. Consent therefore applies not only to whether a dependency exists, but to its package identity, install route, and execution scope.

The same dependency guidance adds an important scope rule for toolchain skill adoption. Installing a CLI is only half the decision: before the pipeline uses `graphify` or `openkb`, the corresponding read-only skill must also be vendored into `.agents/skills/<name>/`, preferably through a project-scoped manager or upstream project installer when one exists. The document treats that vendoring as part of the same user-approved adoption step, not as an unrelated background copy. Consent therefore covers both executable tooling and the repository-local guidance the workflow will defer to afterward. This reinforces [[concepts/skill-vendoring]] and [[concepts/skill-governance]].

The skill summary makes this even stricter by requiring a disclosure package before install: package name, configured index, upstream source, pinned version, and integrity procedure must be presented before the user chooses whether to install the tool themselves or have the agent run the command. It also says agents must never override a configured mirror, never use `sudo`, and never leave floating versions in instructions. Consent therefore applies both to the fact of installation and to the exact method used.

That same summary also broadens consent into execution convention and generated-state boundaries. Users are not only approving a package installation; they are approving that bundled scripts run through `uv run`, that deterministic input is staged under `okf/.okf-build/input/`, and that compiled wiki content is regenerated through OpenKB rather than hand-edited in place. Consent therefore covers approved execution paths, accepted degradation modes, and the repository surfaces a tool is allowed to mutate.

The prerequisite script broadens this by making consent conditional on measured repository state rather than assumptions. It checks Python version, Git availability, worktree membership, and writable paths before any install recommendation is acted on. It also distinguishes required tools from optional ones, optional companion skills from hard failures, and installed CLIs from missing vendored tool skills. In practice, this means consent is informed: the user is shown what is actually missing, what is merely helpful, what can be deferred under [[concepts/graceful-degradation]], and what must still be vendored before an installed tool can be used safely.

The dependency guidance broadens consent beyond package installation to include scope and fallback decisions. Users choose per tool whether they install it themselves, the agent runs the command, or the tool is skipped. They also implicitly choose whether a dependency is project-scoped, such as vendoring a skill into `.agents/skills/`, or whether a machine-wide harness integration is appropriate. Missing optional tools or companion skills should not force the workflow to fail; instead, the workflow degrades and reports what is unavailable.

The same source also distinguishes harness tools from local CLIs. Environment-provided powers such as shell, edit, and web access are not the same thing as local commands like Git, Python, [[entities/uv]], [[entities/graphify]], or [[entities/openkb]]. Consent therefore must cover both kinds of capability separately: permission to use a harness tool does not imply that a local CLI is installed, and a local install decision does not expand harness permissions. This is one of the clearest operational overlaps with [[concepts/harness-vs-local-tools]] and [[concepts/permission-scoped-agents]].

The newer skill-creator dependency reference makes the same point from the authoring side. A skill must not imply that dependencies are automatically satisfied just because frontmatter exists. Instead, it should declare concise compatibility requirements, place detailed dependency instructions in `references/dependencies.md`, use namespaced metadata only when those hints genuinely apply, and add a prerequisite checker when local CLIs, credentials, network access, or companion skills matter. It also says `allowed-tools` is a permission hint, not an installation declaration. Consent therefore includes agreement on how dependency state is checked, how absence is handled, and how much authority the skill manifest is allowed to claim.

The skill-creator skill summary extends that same consent boundary into the body of created skills. New skills must treat installs as user-approved steps rather than hidden setup, keep instructions narrowly scoped to the action at hand, and explain why strict rules exist instead of stacking unsupported absolutes. It also says skill descriptions should be written as triggers, because an agent may act on the description alone before reading the full body; consent therefore includes being precise about what kind of action is actually being authorized.

The source-attribution note adds another consent boundary by making explicit what this adaptation chose to keep and what it deliberately rejected from upstream lineages. Its rules say project skills belong only under `.agents/skills/`, skills stay action-oriented, durable context stays in `okf/wiki/`, `AGENTS.md` remains orientation-only, and runtime-specific metadata or personal agent configuration should not be copied into the repository. Consent therefore also includes agreement about what kind of repository shaping is acceptable when tools and skills are adopted.

The skill lock example adds a parallel consent boundary for dependency records. A lock file may describe approved skill dependencies, but the example explicitly marks itself as illustrative and warns against hand-editing real vendor lock entries unless the manager documents that workflow. That means consent covers not only whether a dependency is adopted, but also whether its lock state is refreshed through the approved manager path rather than improvised edits to generated records.

The privacy and data-flow guidance broadens consent further from installation and activation into network behavior. A user is not merely approving that a tool exists locally; they are approving whether and when it may send staged sources, wiki content, prompts, PDFs, URLs, or fetched document content to an external provider. Before the first provider-backed [[entities/openkb]] command, or before [[entities/graphify]] processes non-code sources through a nonlocal backend, the workflow must disclose the tool, provider, model, endpoint, credential source, and what content will be sent. If any of those change, consent must be renewed through a fresh disclosure. This makes [[concepts/data-flow-disclosure]] an operational part of tooling consent rather than a separate concern.

The workflow reference sharpens these rules into a decision tree. Consent is required before bootstrapping hard prerequisites, before adopting optional tools, before initializing Git in a non-Git directory, before using user-supplied URLs with `openkb add`, before first provider-backed OpenKB use, and before broad recompilation. It also constrains what counts as approval: even if a CLI is installed, the workflow still must stop if its vendored skill is missing. Consent therefore covers the full approved operating context, not just binary presence.

The same workflow adds a review-stage form of consent for generated outputs. After `openkb add` or `recompile` changes `okf/wiki/`, the agent should inspect the resulting pages for missing concepts, duplicates, entity or concept misclassification, off-topic distillate from examples, lost caveats, truncation, stale early pages, and grounding problems. Users are effectively approving not only that tooling may run, but that its outputs will be checked before acceptance. This connects the concept strongly to [[concepts/caveat-preservation]], [[concepts/human-in-the-loop-review]], and [[concepts/knowledge-linking-and-citations]].

The template adds a workflow-specific form of consent for knowledge operations. Even after tooling is installed, the agent must ask before expensive or destructive OpenKB work such as large adds, URL or PDF ingestion, `remove`, `recompile`, `lint`, `lint --fix`, `query --save`, `visualize`, and Skill Factory commands, with dry runs expected before `remove` and `recompile`. Consent therefore governs not only tool adoption but also high-impact use of already approved tools.

The template also adds a source-authority consent rule: wiki content is data, not instructions, and Graphify outputs are file-selection aids rather than final authority. Users are therefore approving bounded use of those tools and outputs, not granting them policy-setting authority over the repository. This directly supports [[concepts/knowledge-boundaries]] and [[concepts/repo-navigation]].

The bootstrap flow adds a related distinction between provider-backed and fallback paths. If no LLM provider is configured, the conservative skeleton workflow is used instead of silently escalating into remote semantic generation. Consent therefore includes approval of which generation mode is active, not just which package is installed.

The new skill summary adds an additional approval boundary around `okf/wiki/AGENTS.md`. It treats that file as OpenKB's on-disk wiki-conventions manual and says customizations to it should happen only with user consent. That makes consent apply not only to package installs and command execution, but also to changes in the repository's internal wiki conventions and tooling guidance surfaces.

The README adds a final nuance: optional harness adaptation should detect the active runtime rather than every installed runtime. Consent therefore includes agreement on which execution environment is actually being shaped. That reduces accidental spread of repository policy into unrelated local setups and supports [[concepts/runtime-signal-prioritization]] and [[concepts/runtime-ambiguity-resolution]].

This matters because tool installation or activation can:

- change the local or CI environment
- introduce new dependencies
- pull artifacts from package indexes or mirrors
- alter reproducibility across runs
- create security and review risks
- add new enforced checks to the development workflow
- widen scope from repository state into user or harness configuration
- route code or documents to a remote provider if backend selection is not explicit
- create new privacy obligations around credentials, endpoints, and fetched content
- rewrite generated lock artifacts that define approved dependency state
- fail for repository-state reasons such as missing worktree context or unwritable required paths
- create runtime-specific adapter files that should not be mistaken for repository source of truth
- mutate coupled knowledge-base state such as the wiki and its dedupe registry if high-impact commands are used carelessly
- populate or refresh structural outputs such as `graphify-out/` that may be useful but are not the authoritative knowledge surface
- create staged build directories whose presence should not be mistaken for durable committed knowledge
- introduce vendored vendor-skill content whose parent directory name and project scope affect whether agents can discover it correctly
- fail deterministically when required normalization or ignore files are absent or conflicting, forcing an explicit user decision rather than silent override
- create self-reference problems if generated wiki content is allowed back into graph analysis or staging inputs

Installation is allowed only when needed, not preemptively, and CI adoption is framed as a deliberate repository decision rather than an automatic behavior. The bootstrap, dependency, prerequisite, skill, lock-file, source-attribution, privacy, README, workflow, and skill-creator documents also broaden the point from package installation to repository shaping decisions: adding validation, graph generation, knowledge compilation, vendored skill content, or review gates is something the user consents to as part of making the repository agent-ready, and provider-backed execution requires separate disclosure and approval.

## What "pin management" means

Pin management means choosing and recording exact tool versions rather than using floating or implicit latest versions. The source document recommends pinned installs for repository knowledge tooling and provides a table for recording:

- tool name
- pinned version
- artifact integrity hash
- package index used
- date recorded

The template makes this record part of the durable orientation surface: pins, integrity values, index, and recording date belong in repository guidance rather than private operator memory. It also says updates happen only after the user reviews upstream release notes and confirms the change, so pinning is treated as a maintained trust record rather than a one-time install detail.

The dependency reference makes that stricter by requiring exact versions in any command left behind, treating floating versions as acceptable only for a one-off interactive install the user explicitly approves. It also extends pin management beyond version strings to include package identity, upstream source, integrity hash, and install scope. In this model, a trustworthy pin is not merely `tool==version`; it is a recorded decision about which artifact from which source and which index is allowed.

The same dependency guidance adds a packaging-identity rule that matters especially for lookalike names. The user should verify the exact package name before installation and trust the upstream repository when old docs conflict. That is why the document explicitly distinguishes the `graphify` CLI from the [[entities/graphifyy]] Python package name, and why it records the authoritative upstream sources for [[entities/uv]], [[entities/graphify]], and [[entities/openkb]]. Pin management therefore overlaps directly with [[concepts/provenance-tracking]], [[concepts/version-pinning]], and [[concepts/supply-chain-security]].

The bootstrap document reinforces this with concrete install examples that pin both [[entities/graphify]] and [[entities/openkb]] at explicit versions. It also treats package provenance and pinning rules as a separate durable reference rather than burying them inline, which keeps the bootstrap flow readable while preserving exact dependency authority elsewhere. This connects pin management to [[concepts/documentation-source-priority]] and [[concepts/single-source-of-truth]].

The README summary in [[summaries/README-md]] strengthens this by presenting pinned versions and integrity hashes as part of the repository's durable orientation record rather than scattered setup notes. It also frames harness adapters as projections, which implies that any versioned runtime-specific file should remain secondary to the project-owned pin record. This reinforces [[concepts/single-source-of-truth]] and [[concepts/provenance-tracking]].

The template summary adds an important execution detail: `uv sync` is preferred when `pyproject.toml` or `uv.lock` exists, and Python repository maintenance scripts should run through `uv run` rather than bare `python` when uv is available. Pin management therefore includes preserving the expected execution path, not just the package version, because the same script run through the wrong toolchain can break reproducibility.

The dependency reference also requires that the target repository record not just tool pins but the source and version or commit of vendored toolchain skills. When `graphify` or `openkb` guidance is copied into `.agents/skills/`, those copies are treated as immutable vendor content and refreshed only by re-vendoring from an approved new pin or by the skill manager's own update flow. In this concept, pin management therefore includes repository-local skill copies as well as installed binaries. This sharpens the link to [[concepts/skill-vendoring]] and [[concepts/generated-artifact-adoption]].

The skill-creator dependency guidance reinforces the same point for skill-authored instructions. It says installable third-party tooling must be named exactly, including package, registry, and upstream repository; install commands must stay pinned and must never use `@latest`; first install should capture integrity from the environment's configured index; and moving a pin requires user-confirmed release-note review. It also requires the skill to state how behavior degrades when the tool is absent, so pins define approved capability rather than silent assumptions.

The skill-creator skill summary adds a wider operational expectation around pins. Because new skills are expected to keep deterministic behavior in scripts, heavy details in references, and only the essential trigger and procedure in `SKILL.md`, pinning becomes part of the division between stable executable logic and descriptive guidance. When a workflow is fragile or destructive, the summary says to narrow its degrees of freedom through exact scripts and validation rather than leaving a loosely described sequence that future agents might reinterpret.

The source-attribution note adds that these pinning rules are part of a deliberate hardening path layered on top of upstream skill patterns. Its emphasis on consent-first version-pinned installs, integrity recording, registry-agnostic commands, vendor-skill immutability, and lockfile policy shows that pin management is not only a package-installation tactic but also a design constraint for how repository automation is packaged and maintained.

The skill summary aligns with this by requiring that pinned versions and artifact hashes be recorded in the repository's `AGENTS.md` toolchain pin record. It also treats a mismatch for the same version and index as a stop-and-report supply-chain event. This turns installation into a traceable, auditable decision rather than an ad hoc convenience. It directly supports [[concepts/provenance-tracking]] by preserving where a tool came from, which version was trusted, which index served it, and when that trust decision was made.

That same summary adds two newer pin-governance details. First, vendor skill adoption is part of the same pinned tool decision: before first CLI use, the corresponding read-only skill must be copied into `.agents/skills/` under the same consent and version policy. Second, pin management now includes protected state around generated OpenKB repositories, since the dedupe registry in `okf/.openkb/hashes.json` must stay coherent with the compiled wiki for repeatable incremental behavior. A stable pin without coherent tool-managed state is not enough for reproducibility. This deepens the link to [[concepts/skill-vendoring]], [[concepts/hash-registry-coherence]], and [[concepts/incremental-compilation]].

The skill lock example extends pin management into dependency manifests generated by tooling. Its sample `skills` entries pair each skill name with a source identifier, a pinned version or digest, and a manager-generated integrity value. That makes lock files a concrete form of pin record for reusable automation: not a place for free-form documentation, but a machine-maintained snapshot of approved dependency resolution. The example's `schema: "example-only"` marker further clarifies that the shape is illustrative while real authority belongs to the chosen manager's documented lock format, reinforcing [[concepts/spec-authority]].

The prerequisite script adds an important preparatory layer: pin management only becomes meaningful after the workflow confirms the relevant executable is present and the repository is ready to use it. Its required-versus-optional reporting, worktree check, and writable-path validation prevent teams from treating every declared dependency as equally urgent or every missing capability as install-ready. It also keeps optional capabilities, such as semantic compilation with [[entities/openkb]] or graph generation with [[entities/graphify]], from being silently promoted into unreviewed mandatory tooling.

The CI template adds an adjacent point: even when a workflow uses major-version action tags for readability, repositories may need stricter pinning to full commit SHAs depending on policy. That broadens pin management beyond Python packages or local CLIs to include CI dependencies themselves.

The privacy and routing guidance adds another dimension: operational pins are not only version selections but also provider selections. A pinned tool with floating backend behavior can still violate repository policy if it silently chooses among exported API keys or external endpoints. In practice, pin management therefore includes preserving explicit model and backend configuration, especially for provider-integrated tools such as [[entities/openkb]] and [[entities/graphify]]. This ties the concept directly to [[concepts/provider-integration]].

The workflow reference adds a build-order dimension to pin management. Pinned tools are meaningful only if they are invoked in a stable sequence: Graphify before source-pack creation, deterministic staging before `openkb add`, and validation after generation. It also requires `.gitattributes` installation or merge to preserve LF normalization and stable staging hashes, plus `.graphifyignore` to exclude the KB root. This shows that pin management includes the surrounding execution and normalization assumptions needed for reproducible behavior, connecting the concept directly to [[concepts/git-attributes]], [[concepts/line-ending-normalization]], [[concepts/document-normalization]], and [[concepts/hash-registry-coherence]].

The template summary contributes a further knowledge-governance angle. It says generated wiki pages should not be edited directly; weak output should be fixed by improving committed source documents and re-ingesting them. In that workflow, stable tool pins matter because regeneration is only comparable over time when the compilation and validation toolchain remains explicit and repeatable.

The bootstrap guidance adds a commit-policy angle to pin management. It distinguishes durable tracked state from build-only output: generated wiki content and OpenKB config may be committed, while `okf/.okf-build/`, `okf/output/`, cache files, and cost records usually are not. Pin management therefore sits alongside artifact-scoping rules: exact versions are durable, but not every generated intermediate belongs in the long-term repository record. This overlaps with [[concepts/generated-artifact-adoption]] and [[concepts/generated-content-governance]].

The README reinforces the same broader meaning by listing concrete maintenance commands for incremental compilation, linting, and bundle validation. A pinned toolchain is not only for first install; it is the stable base that makes repeated `status`, `list`, source-pack rebuild, `add`, `lint`, and validation cycles comparable over time. That connects this concept directly to [[concepts/incremental-compilation]] and [[concepts/okf-validation]].

## Integrity and trust-on-first-use

A key detail from the source guidance is the trust-on-first-use model for package artifacts. Once a specific version is recorded from a specific configured index, its integrity hash becomes part of the repository's expected tooling state.

The dependency reference makes this operational: on first install, the exact pinned artifact is downloaded through the configured index and hashed, and the resulting digest is recorded alongside the version, index, and date. Later installs or machine bootstraps must compare the same version from the same index against that recorded value.

If the same version from the same index later produces a different hash, the guidance treats that as a supply-chain red flag. The correct response is to stop and report the mismatch, not to silently accept, overwrite, or re-pin it.

The same document is careful about limits. This model detects artifact substitution after the first recorded trust decision, but it does not prove that the first artifact obtained from the configured index was uncompromised. That honesty matters because it keeps trust-on-first-use grounded as an audit trail and review mechanism rather than overselling it as a full signature system. This makes the overlap with [[concepts/trust-on-first-use]], [[concepts/integrity-pinning]], and [[concepts/supply-chain-security]] especially direct.

The README summary in [[summaries/README-md]] supports the same rule by explicitly describing the stack's supply-chain model as trust-on-first-use with revalidation when a pin moves. It presents integrity recording and mismatch handling as repository policy, not just implementation detail, which strengthens the connection to [[concepts/hash-registry-coherence]] and [[concepts/supply-chain-security]].

The template strengthens this by requiring the repository to record not just version and hash, but also the configured index and recording date in the maintained pin table. That makes integrity part of the durable operational memory of the repository rather than a transient install log.

The skill summary reinforces this by calling the mismatch a supply-chain incident and by requiring that version and integrity records remain part of the repository's maintained orientation. It also links trust to runtime policy: when the same executable may route content to different providers, preserving the expected backend configuration is part of preserving the trusted state.

The newer skill-creator dependency reference sharpens the same rule by requiring the integrity capture to come from the environment's configured index, including corporate mirrors, and explicitly forbidding bypassing that index to fetch a supposedly canonical hash. It treats a mismatch for the same version and index as a supply-chain incident and requires user-confirmed release-note review before any trusted version moves forward. That makes trust-on-first-use both an artifact rule and a process rule.

The skill-creator skill summary supports the same model indirectly through its validation-first stance. It says every created or adopted skill should be validated before completion, and that adopted generated skills must be compared back against their source wiki pages to restore any lost caveat, boundary, or "never do" rule. For tooling trust, that means stable artifacts are necessary but not sufficient: the approved executable form must also preserve the original safety conditions rather than flattening them during packaging. This is where the concept overlaps most closely with [[concepts/caveat-preservation]].

The source-attribution note supports this interpretation by naming integrity recording and version-pinned installs as explicit adaptation features rather than incidental implementation details. Because this repository adapts upstream skill patterns into a stricter governance model, trust-on-first-use becomes part of the expected repository contract for tool adoption and not just a local convenience.

The skill lock example adds a dependency-manager analogue to the same rule. Lock entries are expected to carry manager-generated integrity values, so the lock file is not merely a convenience list of names and versions; it is part of the trusted dependency state for vendored or installed skills. If a supposedly identical skill source and version resolve to a different integrity value, that should be treated as a stop-and-investigate event rather than a normal refresh. This overlap makes the example a concrete expression of [[concepts/integrity-pinning]].

The prerequisite script complements this by ensuring that prerequisite failures are surfaced before any trust decision is taken. If [[entities/uv]] is missing, if Git is unavailable, if the repository is not a worktree, or if required repository paths are not writable, the correct response is diagnostic reporting and explicit user choice, not improvising with alternate install paths or silently mutating the environment. This keeps trust-on-first-use attached to the intended acquisition and execution path rather than to an ad hoc fallback.

The template summary adds a coupled-state trust rule for OpenKB repositories: `okf/.openkb/hashes.json` and `okf/wiki/` are one unit. If the registry says content exists but the wiki pages were lost, future adds may skip that content silently. After merges or reverts touching `okf/`, the workflow should run OpenKB lint and inspect the report. Trust-on-first-use therefore applies not just to downloaded artifacts but also to the internal coherence of generated knowledge state. This directly reinforces [[concepts/hash-registry-coherence]].

The new skill summary strengthens that state-integrity model by calling out the hash registry as a dedupe registry whose drift can silently suppress future ingestion. In other words, trust must cover not only the downloaded artifact and its version, but also the managed state the approved tool uses to decide what work to skip or repeat. This makes integrity a property of tool operation as well as tool acquisition, and deepens the connection to [[concepts/registry-drift]] and [[concepts/repository-ingestion]].

The workflow reference extends this integrity model to deterministic staging. The source pack is intentionally stable across commits because each staged file records the last commit that touched that file rather than current HEAD, and the snapshot itself carries no commit stamp. That means unchanged files remain byte-identical and OpenKB's hash registry can deduplicate correctly. Trust, in this context, includes confidence that the same repository content resolves to the same staged evidence under the same normalized conditions. This ties integrity directly to [[concepts/deterministic-builds]], [[concepts/hash-registry-coherence]], and [[concepts/repository-ingestion]].

The workflow also adds a self-reference integrity rule. The repo graph must exclude `okf/`, and source-pack construction refuses graph reports that reference the KB root. Otherwise the pipeline creates a feedback loop in which generated wiki pages influence future graph reports and then re-enter the wiki as evidence. Trust-on-first-use therefore includes preserving a citation chain that terminates in repository files rather than generated derivatives, reinforcing [[concepts/self-reference-control]] and [[concepts/knowledge-linking-and-citations]].

The bootstrap guidance broadens this to repository commit discipline. Because `okf/wiki/`, `okf/.openkb/config.yaml`, and `okf/.openkb/hashes.json` are usually committed while build directories and caches are not, the trusted repository state is partly defined by which generated files are preserved as durable evidence and which are intentionally excluded. Trust is therefore attached to a curated set of committed outputs, not to every transient file a tool may emit.

The README adds a runtime analogue: provider selection and endpoint disclosure are part of trusted operational state. A binary whose package artifact is unchanged can still represent a materially different trust posture if its configured model, endpoint, or off-machine execution path changes. Trust-on-first-use therefore extends naturally into [[concepts/data-flow-disclosure]] and [[concepts/privacy-preserving-tooling]].

This rule is important because it:

- detects unexpected artifact drift
- discourages silent trust resets
- preserves a review trail for tool adoption
- reduces the chance of unnoticed tampering or republishing
- distinguishes normal upgrades from suspicious substitutions
- keeps generated lock records aligned with the actual resolved dependency set
- makes provider-routing changes visible as trust transitions rather than incidental config churn
- treats broken knowledge-registry coherence as a state-integrity problem rather than a harmless wiki mismatch
- keeps durable committed outputs distinct from disposable intermediate build and cache files
- preserves index-specific integrity decisions rather than pretending one public digest always governs every environment
- preserves deterministic staging assumptions so unchanged inputs remain unchanged evidence across runs
- prevents self-referential graph and wiki cycles from corrupting provenance chains

The same mindset appears in bootstrap, prerequisite, privacy, workflow, CI validation, skill, lock-file, source-attribution, README, and skill-creator dependency guidance: workflow dependencies should be understandable, bounded, and pinned tightly enough for the repository's risk posture. Whether the dependency is a package artifact, a vendored skill copy, a skill-manager lock entry, a GitHub Action reference, a normalization file that stabilizes hashing, or a provider configuration that controls network egress, the principle is to make trust decisions explicit. This is one of the clearest places where this concept overlaps with [[concepts/supply-chain-security]].

## Configured indexes only

The source guidance also says installs must go through the package index configured in the environment, including corporate mirrors when present, and must not bypass that configuration. This makes tool acquisition part of the controlled environment rather than a personal shortcut.

That requirement reinforces:

- organizational policy compliance
- consistent artifact sourcing
- comparable installs across users and agents
- stronger provenance records
- respect for enterprise mirror and proxy setups

The dependency reference is explicit that the public registry is only the default, not the authority for a particular environment. Agents should use whatever Python index the environment already configures and should report missing allow-listing or mirror availability problems instead of overriding index settings.

The skill summary complements this by saying the agent must never override a configured mirror and must report the configured index as part of the install disclosure. It also requires all package guidance to stay pinned, which prevents "use latest from wherever works" behavior from bypassing the environment's sourcing controls.

The dependency guidance adds that registry-agnostic behavior must extend to install instructions left behind in the repository. Commands should work unchanged behind mirrors because they rely on the configured index, not on hardcoded registry URLs. When an environment cannot serve a pinned package, the correct response is to report the issue and ask the user to resolve allow-listing or mirror availability, not to bypass policy. This makes configured-index discipline part of [[concepts/safe-automation]] and [[concepts/provenance-tracking]].

The bootstrap guidance complements this by treating dependency provenance and pinning as part of the repository bootstrap rules rather than a local preference. The prerequisite script supports the same discipline by recommending install guidance only after it determines which hard requirements are actually absent, and by framing bare `python3` as a degraded fallback rather than an excuse to bypass the required [[entities/uv]] path without explicit user agreement.

The newer prerequisite summary adds a concrete packaging example that matters here: it documents install guidance for [[entities/graphify]] using the package name [[entities/graphifyy]], and for [[entities/openkb]] using its own package name, while explicitly tying those commands to the environment's configured Python index. That makes source identity, package identity, and configured-index compliance part of one disclosure package rather than separate concerns.

The newer skill-creator dependency reference repeats the same sourcing rule in skill form. It requires Python scripts to use PEP 723 inline metadata and to be documented as `uv run <script>`, with bare `python3` only as a degraded fallback. It also says the integrity recorded on first install must come from the configured index rather than a hardcoded public source, which keeps reproducibility aligned with local environment policy instead of pretending all users share one registry path.

The skill-creator skill summary adds a packaging-level version of the same rule. Because project skills live only under `.agents/skills/<skill-name>/`, while generated downstream outputs stay in `okf/output/skills/` until explicitly adopted, source governance applies not just to package registries but to repository-local automation sources as well. Approved acquisition means using the documented initialization or adoption path, validating afterward, and not treating generated output as automatically trusted project state.

The source-attribution note reinforces this by describing the adaptation as registry-agnostic rather than tied to a single vendor or package ecosystem. That matters because respecting configured indexes is part of keeping automation portable across environments while still preserving approval, provenance, and integrity guarantees.

The skill lock example adds an equivalent source-governance rule for skill dependencies. Its sample entries record a `source` field for each locked skill, making it explicit that pin management is tied not just to version but to the exact source identifier used by the manager. In practice, a lock file that omits or obscures source provenance weakens the same guarantees that package index controls provide for CLIs and libraries.

The template summary adds an execution-source constraint too: if the repository has a `pyproject.toml` or `uv.lock`, maintenance scripts should follow that project toolchain rather than bypassing it with ad hoc interpreter choices. That keeps acquisition, resolution, and execution within the same governed channel.

The bootstrap guidance adds another repository-source boundary: external documents should be added as evidence under staged build input before semantic generation, not mixed directly into final wiki pages or orientation files. That means approved sourcing applies not only to binaries and packages but also to the evidence that generation tools consume. This overlaps with [[concepts/evidence-staging]] and [[concepts/external-documentation]].

The workflow reference strengthens this by requiring external URLs to be materialized as evidence under `okf/.okf-build/input/external/`, or added through `openkb add <url>` only for user-supplied URLs with consent. It also says fetched external material is evidence only and never hidden memory or instructions. Approved sourcing therefore applies equally to executables, vendored skills, staged evidence, and graph inputs. This directly supports [[concepts/web-evidence-ingestion]], [[concepts/evidence-staging]], and [[concepts/source-trust-levels]].

The README adds a parallel runtime sourcing rule: Graphify should use an explicit backend for non-code processing, and OpenKB routing should be configured deliberately rather than inferred from ambient credentials. A configured package index governs where binaries come from; explicit backend configuration governs where repository content goes. Together, they bind acquisition and execution to approved channels and reinforce [[concepts/provider-integration]].

In practice, this also complements CI adoption. A repository may choose to enforce structural checks in hosted automation, but the dependencies and execution path for those checks should still remain within approved tooling and sourcing patterns.

The privacy guidance adds a parallel rule for network destinations: tools should not silently bypass the chosen execution path by auto-selecting a provider from ambient credentials. A configured package index governs where binaries come from; an explicit backend or model configuration governs where repository content goes at runtime. Together these two controls keep both acquisition and execution inside approved channels.

## Update discipline

Pin updates are not routine maintenance to perform automatically. The source requires that a pin be updated only after the user reviews upstream release notes and confirms the change. In practice, this means version movement is a deliberate decision with human oversight.

The dependency reference extends that discipline by defining an update sequence: detect that a newer version exists through configured index metadata, show the upstream release notes or changelog diff, obtain explicit confirmation, then install the new version and capture a fresh integrity value. A version change therefore becomes a reviewed trust transition rather than a convenience upgrade.

The same dependency guidance also treats vendored toolchain skills as part of the update story. After an approved pin bump, `graphify` should refresh through its project-scoped installer or the manager's own update command, while `openkb` should be re-vendored from the newly approved upstream tag. Those copies remain immutable in the repository between approved updates. Update discipline therefore covers repository-local vendor content as well as installed executables.

The skill summary matches this by saying a pin must never be updated without user confirmation of the new version's release notes. It also adds that runtime route changes matter too: switching model, backend, or provider is a material operational change even if the binary version remains fixed.

The README summary in [[summaries/README-md]] reinforces this by treating telemetry claims, package pins, and provider behavior as things that must be re-verified when a pin moves. It also frames maintenance as incremental refresh rather than regeneration from scratch, which makes disciplined updates especially important: repeated small changes are only trustworthy if each version and routing transition is explicit. This connects update discipline to [[concepts/incremental-compilation]] and [[concepts/telemetry-auditing]].

The bootstrap document extends that discipline to the broader toolchain used for agent-ready repository setup. The first installation of a tool, the later update of that tool, and the decision to adopt or refresh a skill dependency are all separate trust decisions. Vendor skills are treated as read-only project dependencies, and any generated lock file is meant to be preserved rather than casually rewritten.

The bootstrap guidance also adds an important post-generation maintenance rule: first OKF generation should be treated as context discovery, and repeated executable behavior found in the resulting repository knowledge should be moved into or created as skills. That means updates are not only about bumping versions; they are also about reclassifying stable repeated procedures into governed automation while keeping architecture facts and rationale in the wiki. Update discipline therefore overlaps with [[concepts/skill-based-automation]] and [[concepts/context-action-separation]].

The newer skill-creator dependency guidance gives a stricter authoring pattern for those updates. Third-party tool requirements must stay pinned in written instructions, `@latest` must never be left behind for future agents, release notes must be reviewed before changing any pin, and the skill must tell the user how behavior degrades when the tool is absent. It also says vendor skills installed by a package manager should remain immutable in the repository, and if adaptation is needed, a custom companion skill should be created under `.agents/skills/` instead of patching the vendor skill directly. That makes update discipline apply both to binaries and to reusable automation packages.

The skill-creator skill summary adds two important refinements. First, skill creation itself should follow [[concepts/baseline-first-testing]]: run a pressure scenario without the skill, record actual failures, then write the skill against those failures and retest with the skill in place. Second, adoption of generated skills ends with a caveat-preservation review because distillation can flatten conditions into unconditional steps. Together these rules make updates a form of controlled revalidation rather than simple content replacement, and closely align this concept with [[concepts/failure-driven-development]].

The source-attribution note reinforces that immutability policy by naming vendor-skill immutability and lockfile policy among the main additions of this adaptation. It also ties update discipline to repository boundaries: project-owned customizations belong under `.agents/skills/`, while adopted vendor skills remain managed dependencies rather than quietly edited local forks.

The skill lock example sharpens that preservation rule. Because real lock entries are generated by the manager and carry source, version, and integrity details, an update to a locked skill should come from an approved refresh operation rather than hand-edited JSON. That keeps the lock file aligned with the manager's documented semantics and avoids accidental drift between declared and resolved dependency state. This is where the concept most directly overlaps with [[concepts/lock-file-examples]].

The prerequisite script contributes a related discipline around readiness changes. Required-tool availability, Python compatibility, worktree state, vendored tool-skill presence, and repository writability are all preconditions that may change independently of version changes. Re-running preflight before installs, upgrades, or validation execution helps distinguish a real pin update from an environment problem, and prevents users from misattributing readiness failures to version drift.

The privacy guidance adds that version updates are not the only trust transitions that matter. A change in provider, endpoint, model, credential source, or local-versus-remote execution mode is also a material operational change that should be surfaced and approved. Telemetry claims must be re-verified when a pin changes, and the date of that verification should be recorded alongside the trusted version. This makes [[concepts/telemetry-auditing]] part of update discipline rather than an optional afterthought.

The workflow reference adds process-specific update discipline for compiled knowledge. Refresh order matters: rerun Graphify first when installed, rebuild the deterministic source pack, ingest staged input, preview recompilation with `--dry-run`, then review and validate. It explicitly warns against recompiling against a stale graph and against broad `recompile --all` without consent. This means pin discipline alone is insufficient; updates must also preserve the approved execution order and regeneration boundaries of the repository pipeline. This strongly reinforces [[concepts/incremental-compilation]], [[concepts/source-driven-regeneration]], and [[concepts/quality-gates]].

The workflow also adds a post-generation review rule that functions as update discipline for generated outputs. After `openkb add` or `recompile`, changed pages should be inspected for missing or vague concepts, near duplicates, entity or concept misclassification, off-topic distillate from examples, lost caveats, truncation, stale early compilation, and grounding. Tooling updates are therefore not complete when commands succeed, but when regenerated outputs still preserve repository meaning and provenance. This tightly connects the concept to [[concepts/human-in-the-loop-review]], [[concepts/caveat-preservation]], and [[concepts/knowledge-linking-and-citations]].

The template summary adds a repository-state update rule around generated knowledge. After merges or reverts touching `okf/`, lint should be run and the report reviewed because version discipline alone cannot protect a repository whose dedupe registry and compiled wiki have drifted apart. Update discipline therefore includes revalidating stateful generated outputs after source-control transitions.

The new skill summary strengthens that point by making the dedupe registry warning part of the main workflow rather than a peripheral implementation detail. Pin updates, merges, reverts, or repairs under `okf/` are all repository-state transitions that can alter whether approved tools behave incrementally or skip work silently. Update discipline therefore includes checking state coherence, not merely bumping versions and re-running commands.

The template also says the final wiki should be validated before finishing work. That makes completion itself part of update discipline: changes are not complete when the install succeeds, but when the resulting generated and validated repository state remains coherent.

This is a useful quality control pattern because it separates:

- installing an already approved tool version
- deciding to trust a newer upstream release
- enabling a new CI dependency
- tightening or relaxing pinning policy for automation references
- re-baselining after an environment index change
- updating vendored skill dependencies versus editing project-owned custom skills
- refreshing manager-generated lock state versus editing explanatory examples
- changing a provider route, model, or credential source for an existing tool
- re-verifying telemetry and off-machine data-flow claims after a version change
- fixing repository readiness problems before treating them as upgrade work
- adopting new runtime adapters versus reusing existing approved projections
- restoring knowledge-base coherence after merges or reverts that affect compiled outputs
- promoting repeated discovered procedures into custom skills while leaving durable rationale in the wiki
- re-running graph extraction before recompilation so generated pages see the current repository structure
- correcting source materials and regenerating outputs instead of hand-editing compiled pages

That separation aligns with [[concepts/quality-gates]] by making version and routing changes review checkpoints instead of implicit side effects.

## Why this matters in agent-ready repositories

Agent-oriented workflows often depend on external tools to build maps, ingest evidence, compile knowledge, validate outputs, and maintain reusable procedures. Without consent and pin management, these workflows can become:

- non-reproducible
- hard to audit
- vulnerable to unnoticed environment drift
- difficult to review after the fact
- prone to hidden CI behavior changes
- blurred in ownership between durable context and executable automation
- exposed to package-identity confusion or index substitution risks
- prone to silent provider selection based on exported keys
- unclear about when repository or document content leaves the machine
- brittle when repository prerequisites are assumed instead of verified
- inconsistent when manager-generated lock state is hand-edited or allowed to drift from actual dependency resolution
- polluted by runtime-specific adapter files being mistaken for canonical project guidance
- vulnerable to silent knowledge-compilation skips when registry state and compiled outputs lose coherence
- harder to govern when structural aids, staged inputs, build artifacts, and durable outputs are mixed together
- weakened when installed CLIs and vendored skill copies drift apart or when a portable skill is replaced by a harness-specific projection
- destabilized when generated wiki content is allowed to feed back into graph analysis or future evidence staging
- misleading when example files or fixtures are semantically compiled without review into repo-level concepts

In the source guidance, this concern appears as part of a larger disciplined workflow around generated knowledge, validation, and repository safety. The bootstrap document sharpens the point by defining a responsibility split: durable repository knowledge belongs in the wiki, routing belongs in `AGENTS.md`, structural exploration is secondary, and repeated executable behavior belongs in skills. The dependency reference adds another boundary: harness permissions, skill metadata, local CLIs, vendored skill content, and lock artifacts are related but distinct layers and should not be conflated.

The bootstrap guidance also clarifies why this separation matters after initial setup. First-generation OKF output is treated as context discovery rather than final documentation alone, and the repository should then inspect that output for repeated procedures worth extracting into skills. Tooling governance matters because the same toolchain that compiles knowledge is also helping decide what becomes durable context and what becomes executable automation. Without consent and pin discipline, that classification step can turn into unreviewed repository shaping.

The source-attribution note makes that architectural split more explicit by tracing the adaptation back to upstream skill systems while explaining why this repository keeps action, context, and orientation separate. Skills stay action-oriented, durable knowledge stays in `okf/wiki/`, and `AGENTS.md` stays brief and directive. Tooling governance matters because once tools can install dependencies, route traffic, or vendor automation into a repository, weak boundaries quickly become repository-shaping errors rather than mere convenience shortcuts. This overlap is especially close to [[concepts/context-action-separation]].

The README summary in [[summaries/README-md]] strengthens this argument by making the same split central to the project's public explanation. It presents the repository as becoming agent-ready through orientation, memory, and actions, not through a monolithic setup file. That means tooling governance directly affects whether those three surfaces remain cleanly separated and progressively loadable, which ties the concept to [[concepts/agent-ready-repositories]], [[concepts/durable-context]], and [[concepts/skill-based-automation]].

The newer skill-creator dependency guidance adds a further architectural boundary. It says the portable contract is `SKILL.md` plus optional `scripts/`, `references/`, and `assets/` directories, while dependency resolution, installation state, and vendor lockfiles belong to the skill manager or explicit project scripts. It also standardizes a small namespaced metadata vocabulary for companion skills, vendor skills, prerequisite checks, and prerequisite guidance. This makes repository automation more reviewable because the skill manifest stays descriptive, prerequisite scripts stay executable, and lock artifacts stay manager-owned.

The skill-creator skill summary adds the same argument in more operational terms. It says `SKILL.md` should stay short and procedural, detailed context should move into references, deterministic code should live in scripts, and generated outputs should be validated before completion. It also insists that skills are actions, not narrative memory or knowledge bases. Tooling governance matters here because reusable automation becomes safer when context, action, and generated artifacts are kept in separate, inspectable layers. That connects directly to [[concepts/skill-structure-conventions]] and [[concepts/skill-governance]].

The skill summary strengthens this by making `okf/wiki/` the durable context source of truth, treating `AGENTS.md` as orientation rather than long-form memory, and requiring generated inputs to be staged deterministically before ingest. Tool governance matters because these tools participate directly in how repository knowledge is built, validated, and refreshed. If the tooling path is unstable or unreviewed, the resulting context layer is unstable too.

The same summary also adds a repository-shape discipline around OpenKB ownership. Because OpenKB owns `okf/raw/`, `okf/wiki/`, `okf/.openkb/`, and `okf/output/`, and because generated pages should be corrected through source improvement and re-ingestion instead of direct editing, tooling governance becomes part of protecting the repository's single durable context surface. This further reinforces [[concepts/single-source-of-truth]], [[concepts/source-driven-regeneration]], and [[concepts/durable-context]].

The prerequisite script strengthens the same argument by showing that even a simple tool adoption path has multiple boundaries: hard prerequisites, optional enhancements, companion skills, vendored tool-skill dependencies, and writable repository state are all reported separately. That reporting model preserves scope clarity and keeps a missing optional capability from being mistaken for a repository failure while still stopping execution when installed CLIs lack their required vendored guidance.

The dependency reference adds an especially repository-specific reason this matters: toolchain skills adopted for [[entities/graphify]] and [[entities/openkb]] should be project-scoped, harness-neutral, and discoverable under exact top-level directories in `.agents/skills/`. If they are installed only machine-wide, nested inside another skill, or replaced by harness-specific projections, future agents may not find the governing usage guidance even though the CLI exists. Tooling governance therefore protects not only binaries, but the discoverability and portability of the automation layer itself.

The skill lock example adds another practical boundary: examples can teach a lock structure, but actual dependency locks remain generated state tied to a specific manager. That distinction helps repositories avoid turning illustrative files into unofficial specifications or editing generated records as if they were ordinary configuration.

The privacy guidance strengthens the same argument by making clear that installation governance is incomplete without runtime routing governance. A tool may be correctly pinned and locally installed yet still violate repository expectations if it silently sends non-code sources, staged wiki content, or fetched URLs to an unintended provider. That is why explicit disclosures, backend selection, and local fallback paths are part of the same concept rather than separate hygiene concerns.

The workflow reference adds two further reasons this matters. First, it says the graph must exclude the KB root so the repository's knowledge system does not become its own source material. Second, it says generated wiki changes must be reviewed for duplicates, weak names, entity-concept misfiling, off-topic distillation from examples, caveat loss, truncation, stale early compilation, and citation grounding. In agent-ready repositories, tool outputs are useful only when their authority remains bounded and their results are reviewed by humans. That keeps this concept tightly linked to [[concepts/human-in-the-loop-review]], [[concepts/knowledge-linking-and-citations]], [[concepts/caveat-preservation]], and [[concepts/self-reference-control]].

That separation only works reliably when the tools and skill dependencies used to create it are installed intentionally, pinned clearly, routed explicitly, and locked in managed records when the workflow uses dependency managers. The CI template reinforces the same point by showing that even a simple validation gate should be explicit about what it runs, what it does not run, and how it is installed. The prerequisite script adds that the gate should begin by confirming the repository can actually support the workflow. The result is that tooling is treated as part of the evidence chain, not just background machinery.

## Relationship to deterministic validation

This concept is closely related to [[concepts/deterministic-validation]]. The CI template distinguishes between a structural validator that exits nonzero on violations and an LLM-backed health report that is intentionally not used as a merge gate. That distinction matters for consent and pin management because repositories should be especially careful about which tools are granted enforcement authority in automation.

The dependency guidance supports the same distinction by separating permission hints from actual readiness and by requiring explicit tool verification through prerequisite checks. A consented and pinned tool is not automatically appropriate as a mandatory gate; the repository still needs to decide whether the tool's behavior is deterministic, reviewable, and suitable for failing builds.

The newer skill-creator dependency guidance reinforces this by treating `allowed-tools` as a permission hint rather than an installer or dependency declaration. Skill authors may document prerequisites and dependency behavior, but that does not automatically promote a tool into an enforced build requirement. Deterministic validation still requires a separate decision about whether the repository wants that tool in a blocking role.

The skill-creator skill summary adds a complementary discipline: validation is mandatory before finishing, but the skill itself should be tested first against observed failure modes rather than assumed ideal behavior. That makes enforcement authority something earned through demonstrated usefulness and repeatability, not merely declared in metadata. It also means a validation tool should be narrow enough to reproduce known failures and close them, which aligns with [[concepts/executable-validation]].

The source-attribution note adds a lineage explanation for this restraint. One of the inherited upstream ideas is that the context window is a public good and every line should justify its cost; another is progressive disclosure that loads deeper material only when needed. Applied here, that encourages narrow, explicit validation authority rather than sprawling always-on automation.

The prerequisite script adds a concrete enforcement boundary: it can fail fast on missing hard requirements and unwritable required paths, but it only reports optional tools and companion skills. It also treats installed CLIs without vendored skills as a stop condition for later use rather than as permission to proceed. That separation models how deterministic validation should behave more broadly: enforce the minimum necessary conditions, disclose optional enrichments, and avoid turning every auxiliary capability into a hard gate.

The bootstrap flow shows the same layering by pairing generation steps with lint and validation steps, and by offering a conservative fallback when richer provider-backed generation is unavailable. The skill summary adds that validation belongs after staged ingestion and review, and that broad or destructive OpenKB operations should not be run casually. The skill lock example contributes a reproducibility detail: deterministic validation is easier to trust when skill dependencies are locked to explicit source, version, and integrity values rather than left as floating automation inputs. The privacy guidance adds that provider-backed commands may involve off-machine processing even when they are invoked for validation or linting, so approval for deterministic enforcement and approval for external processing must be considered separately. Consent and pinning help stabilize the toolchain, but deterministic enforcement remains a separate decision.

The workflow reference sharpens this relationship by naming the zero-LLM validator as the right automation point and by explicitly excluding `openkb lint` from CI or Git hooks because it is LLM-backed and never exits nonzero on findings. It also recommends consent-first installation of validation hooks or CI files rather than silently adding them. This links the concept especially tightly to [[concepts/validation-vs-health-reporting]], [[concepts/executable-validation]], and [[concepts/quality-gates]].

The template summary adds a maintenance angle: final wiki validation is expected before finishing, but wiki content itself is still treated as data rather than executable authority. Deterministic validation therefore stabilizes outputs without collapsing the boundary between validation tooling and knowledge content.

The README adds concrete support for this distinction by describing bundle validation as a standard maintenance step while also preserving zero-LLM and local-first modes. That suggests a validation hierarchy: structural, deterministic checks may become routine gates, while provider-backed compilation remains a separately governed capability. This strengthens the relationship with [[concepts/okf-validation]] and [[concepts/offline-first-workflows]].

## Relationship to privacy-preserving tooling

This concept also intersects with [[concepts/privacy-preserving-tooling]]. The CI validator is described as zero-LLM by design, requiring no API key and sending nothing externally. That bounded behavior makes approval easier to reason about: users are not only consenting to a tool version, but also to its operational characteristics.

The dependency reference strengthens this point with explicit security rules: credentials belong only in environment variables or gitignored `.env` files, fetched web content is untrusted input, and generated artifacts should stay out of version control. A pinned tool with unclear network behavior is still risky, while a privacy-preserving tool with unreviewed version drift is still hard to trust.

The prerequisite script adds a practical privacy boundary by supporting a dependency-free, local preflight path that can run in a fresh repository before any richer tooling is installed. Its ability to separate optional semantic or graph tooling from required local checks helps preserve local-first workflows when remote-capable tools are absent or not yet approved. Its notes about bare `python3` as a degraded fallback also keep local execution policy explicit instead of silently changing how scripts run.

The dependency guidance adds a further privacy-preserving boundary by insisting on project-scoped installs and by rejecting machine-wide or harness-wide installs unless the user explicitly requests that alternative. A project-scoped vendor skill limits the spread of repository-specific automation assumptions, while a harness-level install changes the user's broader environment. Consent and privacy both improve when the default adoption scope stays inside the repository. This connects closely to [[concepts/local-vs-shared-configuration]] and [[concepts/minimal-tool-scoping]].

The newer skill-creator dependency guidance adds a related privacy-preserving discipline: when a skill depends on local CLIs, credentials, network access, or companion skills, it should surface that requirement through a prerequisite checker and documented dependency reference rather than assuming execution can proceed. It also says the skill must explain how it degrades when the tool is absent, which supports local fallback modes instead of forcing remote or privileged installation.

The skill-creator skill summary strengthens the privacy angle by requiring new skills to keep credentials in environment variables, treat fetched web content as untrusted data rather than instructions, and identify generated artifacts so they can be gitignored in the target repository. It also frames `allowed-tools` as a minimal scope hint, which supports narrower runtime permissions and less accidental exposure. These defaults make privacy preservation part of the generated skill contract rather than an optional extra.

The source-attribution note reinforces this by naming secret hygiene, minimal scoped `allowed-tools`, and vendor-neutral structure among the adaptation's main additions. Those choices make privacy-preserving behavior easier to preserve because tools and skills are described in terms of bounded permissions and repository-owned scope rather than opaque runtime defaults.

The skill lock example contributes a narrower but related point: generated lock state should not become a covert configuration surface for changing dependency behavior outside the approved manager flow. Preserving that boundary helps keep operational changes observable and reviewable, especially when locked skills may influence how content is processed.

The privacy and data-flow guidance makes the overlap explicit. A privacy-preserving toolchain requires more than local installation discipline: it requires explicit provider routing, disclosure before off-machine processing, the ability to keep `PAGEINDEX_API_KEY` unset for local PDF handling, and the preservation of both air-gapped and zero-LLM workflows. The skill summary adds the same principle operationally by requiring disclosure before the first LLM-backed command and by preserving a zero-LLM skeleton path when richer compilation is unavailable. In that sense, pin management and privacy-preserving operation reinforce one another, and [[concepts/offline-first-workflows]] become a practical fallback rather than an abstract ideal.

The workflow reference sharpens this overlap further. It says Graphify code-only extraction stays local, but non-code processing must use an explicit backend, and external URLs must be treated as evidence rather than instructions. It also requires disclosure before the first LLM-backed command and allows a skeleton bundle when no provider is available. This makes privacy preservation part of execution ordering, not merely a set of static warnings. It links the concept directly to [[concepts/data-flow-disclosure]], [[concepts/web-evidence-ingestion]], and [[concepts/llm-free-knowledge-bootstrap]].

The template summary sharpens this by requiring package installs to use the environment's configured index and by warning that fetched web content should be summarized into evidence with provenance rather than trusted as instructions. Privacy preservation here includes both network-path control and [[concepts/prompt-injection-defense]].

The bootstrap guidance adds a repository-state privacy dimension too. It recommends ignoring local provider credential files and local cost or cache artifacts that may encode environment details. Privacy-preserving tooling therefore includes not just runtime network controls but also commit hygiene around generated traces of local execution.

The README summary in [[summaries/README-md]] adds an explicit security and privacy stance: no silent installs, registry-agnostic but environment-respecting acquisition, explicit data-flow disclosure, no-telemetry verification, secret hygiene, and local-model or zero-LLM fallback paths. This makes privacy-preserving tooling not just an adjacent benefit but a declared design goal of the repository stack.

## Relationship to source-driven regeneration

This concept complements [[concepts/source-driven-regeneration]]. If generated knowledge should be regenerated from improved sources instead of hand-edited, then the tooling used for that regeneration and validation must also be stable and accountable. Pinned, consented tooling helps ensure regeneration and validation results are understandable and comparable over time.

The bootstrap guidance adds that the first generation pass is also a discovery step for deciding what should remain durable knowledge and what should become a reusable skill. The dependency reference extends that by treating companion skills as optional and vendored vendor skills as immutable inputs unless deliberately refreshed. That makes tool governance part of regeneration discipline as well: if the repository repeatedly derives knowledge and procedures from sources, then the pipeline that performs that derivation must be both stable and reviewable.

The newer skill-creator dependency guidance strengthens this by keeping detailed dependency behavior in `references/dependencies.md`, by using prerequisite scripts as the executable check layer, and by leaving lockfiles to the skill manager when vendor skills are involved. That arrangement helps regeneration stay source-driven rather than drifting into hand-maintained dependency folklore embedded in manifests.

The skill-creator skill summary adds a practical adoption path for generated automation. It says skills surfaced from `okf/wiki/` should only be created when they represent true actions, and that generated downstream skills remain build output until the user explicitly adopts them into `.agents/skills/` and validates them. That makes regeneration-compatible automation subject to the same adoption gate as regenerated knowledge: output is not self-authorizing just because it was produced by a tool. This is closely related to [[concepts/generated-artifact-adoption]] and [[concepts/generated-content-governance]].

The source-attribution note adds a complementary architectural reason: the adaptation deliberately preserves a boundary where skills handle action, the wiki holds durable context, and orientation stays in `AGENTS.md`. That keeps regeneration pipelines from collapsing into repository-local tool lore or personal agent configuration, and helps ensure that repeated runs continue to derive from committed sources and explicit procedures.

The skill summary adds a crucial compiled-output rule: when generated wiki pages are weak or wrong, the fix should be made in committed source documents and re-ingested rather than patched in place. It also warns that the OpenKB hash registry must remain coherent or future adds may silently skip content. Tooling consent and pin management therefore support not only repeatable regeneration but also reliable incremental compilation and repair.

The same summary also reinforces regeneration discipline through staging. It says deterministic input belongs under `okf/.okf-build/input/`, that generated files should not be written directly into `okf/raw/` or `okf/wiki/`, and that only narrow exceptions should bypass that path. Regeneration therefore depends on keeping input staging and compiled outputs separate, which strengthens the connection to [[concepts/kb-root-staging]], [[concepts/source-bundling]], and [[concepts/staging-manifests]].

The template summary further operationalizes this workflow. It says external URLs should be materialized into evidence Markdown with URL, timestamp, and provenance; deterministic input should be built under `okf/.okf-build/input/`; and the user should inspect KB state with `status` and `list` before adding new sources. Regeneration is therefore staged, inspected, and replayable rather than improvised.

The bootstrap flow sharpens the same point by defining a concrete build sequence: merge routing context, refresh structural analysis, build staged source-pack input, add external evidence before semantic generation, initialize the knowledge base, ingest, lint, validate, and then re-merge `AGENTS.md` context. It also preserves a non-LLM skeleton path when provider-backed generation is unavailable. This makes regeneration not just source-driven but mode-aware and reproducible across richer and more conservative toolchains.

The workflow reference makes this relationship especially explicit. It says deterministic staging happens before OpenKB updates, that unchanged files should yield byte-identical staged artifacts across commits, that Graphify refresh precedes any recompilation, and that broad recompilation should be avoided without consent. It also forbids hand-editing generated pages and routes all fixes through the correction loop: improve committed sources, re-ingest, recompile, then validate. This ties the concept directly to [[concepts/deterministic-builds]], [[concepts/repository-ingestion]], and [[concepts/incremental-compilation]].

The same workflow also adds a structural anti-drift rule: never recompile against a stale graph, and spot-check early-compiled pages after multi-batch or interrupted ingestion for plain-text mentions of concepts that gained pages later. That means regeneration quality depends on execution order, not just on having pinned binaries. Stable tooling and stable process are both needed for source-driven regeneration to remain trustworthy.

The skill lock example fits this model because lock files preserve dependency state as generated evidence rather than narrative documentation. Keeping those files manager-maintained makes regeneration of dependency state comparable over time in much the same way that keeping summaries source-driven makes knowledge regeneration comparable.

The prerequisite script contributes an earlier layer to the same story: regeneration pipelines should begin from a known-ready repository state. Verifying required executables, Git context, vendored tool-skill readiness, and writable target paths before generation reduces ambiguity when outputs differ, because changes are less likely to be caused by missing local prerequisites or partial setup.

The privacy guidance adds a further requirement for regenerable workflows: the route by which sources are processed must remain stable and documented as well. A repository cannot easily compare successive regenerations if one pass stayed local and another silently used a remote provider under different credentials or endpoints. Source-driven regeneration therefore benefits from the same explicit routing and disclosure discipline as version pinning.

The README reinforces this relationship by recommending incremental maintenance commands rather than whole-cloth rebuilds and by presenting the wiki as durable compiled knowledge. Stable, consented tooling is what makes those repeated adds, lints, and validations comparable over time rather than opaque snapshots.

## Practical indicators of good practice

A repository is following this concept well when:

- tool installation happens only when necessary
- the user has explicitly approved bootstrap actions
- exact versions are recorded for key tooling
- integrity hashes and package indexes are documented
- package identity is checked against the intended upstream source
- prerequisite checks happen before install attempts
- configured mirrors or indexes are respected rather than bypassed
- hard requirements are reported separately from optional tools and companion skills
- worktree state and writable repository paths are verified before setup proceeds
- installed CLIs and vendored tool skills are checked separately rather than conflated
- optional tools can be skipped cleanly without pretending the repository is broken
- missing vendored skills block first tool use even when the matching CLI is already installed
- CI workflows are added intentionally rather than assumed by default
- enforced automation uses deterministic checks where appropriate
- action and package references are pinned to the level required by policy
- vendored skill dependencies are treated as managed, read-only inputs
- manager-generated lock files preserve source, version, and integrity details
- lock entries are refreshed through the documented manager flow rather than casual hand edits
- skill manifests avoid non-standard dependency fields and rely on references plus prerequisite checks
- namespaced metadata is used only for applicable local hints such as companion skills or prerequisite guidance
- repository-owned customizations live under `.agents/skills/` rather than patching vendor-managed skills
- skills stay action-oriented while durable context stays in `okf/wiki/`
- the repository uses `AGENTS.md` for setup and safety orientation rather than burying policy inside generated knowledge
- context is loaded in a documented order, with wiki content treated as data and structural maps treated as navigation aids
- `graphify-out/` is used as an exploration aid rather than final authority
- external evidence is staged before generation instead of being copied directly into durable outputs
- build directories, output directories, reports, caches, and secrets are scoped correctly in `.gitignore`
- `.gitattributes` preserves stable line-ending normalization and is merged rather than blindly replaced
- `.graphifyignore` excludes the KB root so generated wiki content stays out of the repository graph
- toolchain CLI adoption includes project-scoped vendoring of the corresponding portable skill before first use
- vendored skill directories use the exact top-level names expected by discovery rules instead of nested or repurposed layouts
- source-pack generation depends on real Git history rather than an ad hoc non-Git snapshot
- Graphify, when present, runs before source-pack creation so structural inputs are current
- staged source input remains deterministic across commits for unchanged files
- broad or destructive knowledge-base operations require separate approval instead of riding on initial tool consent
- `openkb lint` is treated as a health report, not a blocking validation gate
- zero-LLM validation is preferred for CI and hooks when enforcement is required
- provider-backed runs disclose tool, provider, model, endpoint, credential source, and payload before execution
- non-code processing in [[entities/graphify]] uses an explicit backend rather than ambient key auto-detection
- local-only and zero-LLM fallbacks remain available when repository policy requires them
- telemetry and network-egress claims are re-checked when pinned versions change
- routing expectations are recorded in `AGENTS.md` so later agents follow the same policy
- generated repository evidence is staged before ingest rather than written directly into compiled knowledge locations
- `okf/.openkb/hashes.json` and `okf/wiki/` are treated as one coherent state unit and linted after disruptive merges or reverts
- generated wiki changes are reviewed for duplicates, weak names, misclassification, lost caveats, stale compilation, and citation grounding
- harness-specific adapters are generated for the active runtime only and remain secondary to repository-owned policy
- the repository treats orientation, context, actions, structural aids, staged evidence, and runtime projections as distinct controlled surfaces
- repeated procedures discovered during initial OKF generation are promoted into custom skills only through explicit review and adoption
- self-referential graph or citation loops are prevented by keeping generated wiki content out of structural analysis inputs
- final wiki validation happens before work is considered complete
- fallback to bare `python3` is treated as a disclosed degraded mode rather than a silent substitute for the [[entities/uv]] path
- bundled scripts are run through `uv run` when available rather than ad hoc interpreter choices
- generated content is corrected through source improvement and re-ingestion rather than direct wiki patching
- changes to `okf/wiki/AGENTS.md` conventions happen only with explicit user approval
- harness adapters are treated as runtime projections rather than the repository's policy source
- only the three distributable product skills are copied into downstream repositories, while vendored toolchain copies are re-vendored fresh under approved pins
- maintenance follows explicit incremental commands rather than opaque full rebuilds whenever possible

## Source grounding

This concept is grounded primarily in [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]], which defines consent requirements, pinned installation guidance, integrity recording, configured-index usage, ordered context loading, explicit `AGENTS.md` and wiki boundaries, review expectations for generated knowledge, direct validation expectations for the final wiki, and approval requirements for costly or destructive operations involving [[entities/openkb]] and [[entities/graphify]].

It is further informed by [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]], which shows how those same governance principles apply during repository bootstrap: prerequisite checks before install, consent-first setup, pinned CLI installation, explicit separation of `AGENTS.md`, `okf/wiki/`, `graphify-out/`, and `.agents/skills/`, staged source-pack construction before generation, fallback skeleton generation when no provider is configured, commit-versus-ignore discipline for generated artifacts, vendor-skill immutability, preservation of manager-generated lock artifacts, and the expectation that first OKF generation should drive later skill extraction.

It is also informed by [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], which formalizes the dependency model for the workflow: metadata is not an install manifest, prerequisite scripts are the executable source of truth, configured indexes must be respected, package identity must be verified against upstream provenance, integrity hashes are part of the pin record, optional companion skills must not block the workflow, [[entities/uv]] is the required Python toolchain, degraded bare-`python3` execution must be disclosed, installed CLIs and vendored portable skills are both preconditions for use, `graphify` should be vendored project-scoped through its upstream installer when possible, `openkb` should be manually vendored from the pinned upstream tag, optional deck and critic skills remain separate top-level siblings when adopted, and vendored copies are immutable dependencies updated only through re-vendoring or the manager's own refresh flow.

It is also informed by [[summaries/README-md]], which frames the repository as an agent-ready stack built from orientation, durable compiled context, actions, and optional runtime adapters; documents consent-first bootstrap and maintenance; names trust-on-first-use, explicit provider routing, air-gapped and zero-LLM fallback modes, and telemetry review as first-class policy; treats harness adapters as runtime projections rather than sources of truth; distinguishes the three distributable product skills from vendored toolchain copies; and makes pinned, disclosed, reviewable tooling part of the public architecture rather than an internal implementation note.

It is also informed by [[summaries/agents__skills__skill-creator__references__dependencies-md]], which extends the same policy to skill creation: no non-standard `dependencies` field in `SKILL.md`, dependency details belong in `references/dependencies.md`, local readiness belongs in `scripts/check_prereqs.py`, `allowed-tools` stays a minimal permission hint, namespaced metadata keys may describe companion skills or vendor skills without pretending to be an install manifest, installable third-party tooling must be pinned and consent-first, first-install integrity must be captured from the configured index, vendor skills remain immutable, and lockfiles belong to the manager rather than manual editing.

It is also informed by [[summaries/agents__skills__skill-creator__references__source-attribution-md]], which explains the lineage of the adapted skill-creator workflow and identifies the repository-specific additions that matter most here: vendor-neutral `.agents/skills/` layout, the action/context/orientation boundary, consent-first version-pinned installs, integrity recording, registry-agnostic commands, secret hygiene, minimal scoped permissions, vendor-skill immutability, lockfile policy, and `uv`-first execution.

It is also informed by [[summaries/agents__skills__agent-ready-context__SKILL-md]], which consolidates the governing workflow: explicit consent before any install, exact disclosure of package name/index/source/version/integrity process, required use of [[entities/uv]] for bundled scripts, recording toolchain pins in `AGENTS.md`, treating runtime provider selection as part of tool governance, using staged inputs for repository ingestion, protecting OpenKB-owned paths from direct generated writes, warning about dedupe-registry drift in `okf/.openkb/hashes.json`, and requiring separate approval for costly or destructive OpenKB operations.

It is also informed by [[summaries/agents__skills__skill-creator__SKILL-md]], which defines the action-oriented structure of reusable skills, requires short procedural manifests with details moved into scripts and references, establishes security defaults such as minimal `allowed-tools`, no silent installs, environment-variable secrets, untrusted-content handling, and artifact gitignoring, mandates validation before finishing, promotes baseline-first skill testing, and requires caveat-preservation review when generated skills are adopted into project-owned `.agents/skills/` locations.

It is also informed by [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]], which operationalizes the preflight model through explicit checks for Python version, Git, [[entities/uv]], worktree membership, optional tooling, installed-versus-vendored tool-skill readiness, companion skills, and writable repository paths, while reporting hard blockers separately from degradable capabilities and warning when installed CLIs still lack their required vendored guidance.

It is also informed by [[summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml]], which shows how the same governance principles apply to CI validation: explicit installation, bounded zero-LLM behavior, selective use of deterministic checks, and awareness that action references may need stricter pinning.

It is also informed by [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], which extends the concept from install-time governance into runtime governance: disclosure before off-machine processing, explicit provider routing, mandatory local and zero-LLM fallback paths, re-verification of telemetry claims when versions change, and explicit backend selection for [[entities/graphify]] when processing non-code inputs.

It is also informed by [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]], which provides a minimal example of a skill lock file recording dependency name, source, pinned version or digest, and integrity value, while explicitly warning that real vendor lock entries should remain manager-generated rather than hand-edited.

It is also informed by [[summaries/agents__skills__agent-ready-context__references__workflow-md]], which defines the operational decision tree for OKF compilation: prerequisite checks first, consent-first optional bootstrap, required vendoring of toolchain skills before CLI use, deterministic source-pack construction backed by Git history, normalization and ignore file requirements, Graphify-before-staging update order, explicit evidence handling for external URLs, consent-aware recompilation, human review of generated wiki changes, zero-LLM validation as the enforceable gate, and strict exclusion of `okf/` from graph analysis to avoid self-referential provenance loops.

## Related pages

- [[summaries/README-md]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__skill-creator__references__dependencies-md]]
- [[summaries/agents__skills__skill-creator__references__source-attribution-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__assets__okf-validate-ci-yml]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[concepts/agent-context-layering]]
- [[concepts/agent-ready-repositories]]
- [[concepts/baseline-first-testing]]
- [[concepts/caveat-preservation]]
- [[concepts/context-action-separation]]
- [[concepts/data-flow-disclosure]]
- [[concepts/dependency-management]]
- [[concepts/deterministic-builds]]
- [[concepts/deterministic-validation]]
- [[concepts/document-normalization]]
- [[concepts/documentation-architecture]]
- [[concepts/documentation-source-priority]]
- [[concepts/durable-context]]
- [[concepts/evidence-staging]]
- [[concepts/executable-validation]]
- [[concepts/external-documentation]]
- [[concepts/failure-driven-development]]
- [[concepts/filesystem-validation]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/generated-content-governance]]
- [[concepts/git-attributes]]
- [[concepts/graceful-degradation]]
- [[concepts/harness-native-profiles]]
- [[concepts/harness-vs-local-tools]]
- [[concepts/hash-registry-coherence]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/incremental-compilation]]
- [[concepts/integrity-pinning]]
- [[concepts/kb-root-staging]]
- [[concepts/knowledge-boundaries]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/line-ending-normalization]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/lock-file-examples]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/offline-first-workflows]]
- [[concepts/okf-validation]]
- [[concepts/permission-scoped-agents]]
- [[concepts/preflight-checks]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/progressive-disclosure]]
- [[concepts/prompt-injection-defense]]
- [[concepts/provenance-tracking]]
- [[concepts/provider-integration]]
- [[concepts/quality-gates]]
- [[concepts/registry-drift]]
- [[concepts/repo-navigation]]
- [[concepts/repository-ingestion]]
- [[concepts/runtime-adapter-management]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/safe-automation]]
- [[concepts/self-reference-control]]
- [[concepts/single-source-of-truth]]
- [[concepts/skill-based-automation]]
- [[concepts/skill-governance]]
- [[concepts/skill-structure-conventions]]
- [[concepts/skill-vendoring]]
- [[concepts/source-bundling]]
- [[concepts/source-driven-regeneration]]
- [[concepts/source-trust-levels]]
- [[concepts/spec-authority]]
- [[concepts/staging-manifests]]
- [[concepts/supply-chain-security]]
- [[concepts/telemetry-auditing]]
- [[concepts/tool-boundaries]]
- [[concepts/trust-on-first-use]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/version-pinning]]
- [[concepts/web-evidence-ingestion]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__openkb__references__commands-md]]


See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]