---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/graphify-report.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Explicit, reproducible handling of required, optional, and pinned dependencies."
---

# Dependency Management

Dependency management is the practice of declaring, checking, installing, pinning, locking, vendoring, and updating the tools and skill dependencies a workflow relies on in a way that is explicit, reproducible, and safe. In this wiki, it is closely tied to [[concepts/tool-boundaries]], [[concepts/supply-chain-security]], [[concepts/deterministic-validation]], [[concepts/tooling-consent-and-pin-management]], [[concepts/skill-governance]], [[concepts/consent-first-tooling]], [[concepts/agent-ready-repositories]], and [[concepts/graceful-degradation]].

## What this concept means here

In the context described by summaries/agents__skills__agent-ready-context__references__dependencies-md, reinforced by summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py, extended by summaries/agents__skills__agent-ready-context__SKILL-md, illustrated by summaries/agents__skills__skill-creator__assets__skill-lock-example-json, and sharpened by summaries/agents__skills__skill-creator__references__action-vs-context-md, summaries/agents__skills__skill-creator__references__dependencies-md, summaries/agents__skills__skill-creator__references__vendor-skill-management-md, summaries/agents__skills__skill-creator__SKILL-md, summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md, and summaries/agents__skills__agent-ready-context__references__workflow-md, dependency management is not just a list of packages. It is a full operating model for how an agent-facing workflow:

- distinguishes required tools from optional ones and from companion skills
- separates metadata hints from executable readiness checks
- keeps `SKILL.md` spec-compliant instead of inventing a non-standard dependency field
- verifies package identity against an authoritative upstream source
- pins exact versions and records integrity values captured from the configured index
- uses lock data to preserve resolved dependency state where a manager exists
- respects enterprise package indexes and mirrors rather than bypassing them
- asks for user consent before installing, vendoring, or updating anything
- degrades gracefully when optional tools or companion skills are unavailable
- checks repository-local conditions such as writability, Git worktree state, required skill paths, and KB layout expectations
- treats vendor skills as immutable pinned dependencies and custom skills as project-owned procedures
- vendors required CLI skills into the repository before invoking those CLIs
- keeps dependency procedures in skills while storing durable explanatory background in the wiki
- scopes tool access minimally and treats declared tool access as guidance rather than enforcement
- requires created skills to explain security-sensitive dependency behavior such as installs, secrets handling, fetched content, generated artifacts, and off-machine data flow
- treats `AGENTS.md` as a routing file, not a place for long dependency explanations
- uses the wiki as the durable home for rationale, provenance, and repository-specific context
- stages deterministic source input before ingestion and keeps the KB out of the repo graph
- treats lint, validation, and review as part of dependency readiness rather than optional afterthoughts

The prereq checker makes several of these rules concrete. It validates Python `>=3.11`, `git`, `uv`, Git worktree membership, optional tool presence, vendored skill preconditions for CLI-backed workflows, companion skill availability, and write access to required repository locations. It also emits human-readable output and JSON diagnostics, which makes dependency state useful both to operators and to automation.

The main skill adds a stronger dependency policy around the OpenKB repository surface: `okf/` is the KB root, `okf/wiki/` is the durable context surface, generated material should stage first under `okf/.okf-build/input/`, and CLI adoption includes repository-local vendor skill copies before first use. The bootstrap reference adds that `AGENTS.md` should stay short and operational, while durable context belongs in `okf/wiki/`, and it recommends a consent-first bootstrap flow that checks prerequisites before any install. The workflow reference extends this into a full build model: read the root `AGENTS.md`, then `okf/wiki/index.md` when present, then any routed tooling context; run prerequisite checks before anything else; and only proceed to graphing, source-pack staging, OpenKB initialization, ingestion, lint, and validation when the environment is ready. It also makes the local repository layout part of dependency management by requiring `.gitignore`, `.gitattributes`, `.graphifyignore`, Git history, and predictable KB paths. This places the concept within the broader boundary between repeatable action and durable context described by [[concepts/context-action-separation]] and [[concepts/durable-context]].

## Dependency declaration vs dependency enforcement

A key distinction in the source material is that declarative metadata is not the same as installation truth.

- `SKILL.md` must remain spec-compliant and should not invent a non-standard `dependencies` field.
- `compatibility` can describe environment expectations, but only briefly.
- `allowed-tools` can hint at expected harness capabilities, but it is not an install manifest and not an enforcement mechanism.
- Local namespaced `metadata.*` keys may help local tooling, but they are not portable and should stay string-valued.
- Detailed dependency guidance belongs in `references/dependencies.md`.
- Lock files can record resolved dependency state, but they still do not replace runtime validation.
- The actual source of truth for local readiness is an executable prerequisite checker.

The newer guidance makes the placement rules sharper. Dependency-shaped information should be distributed deliberately: concise runtime expectations in `compatibility`, non-portable local hints in namespaced metadata, detailed requirements in `references/dependencies.md`, and executable validation in a prereq script. The skill-creation guidance adds that `allowed-tools` should be minimal and narrowly scoped, but that those declarations remain hints rather than safety guarantees; the instructions and scripts must still be safe if tool declarations are imperfect. The prereq script makes this distinction concrete by validating Python version, tool presence, Git repository state, vendored skill presence, and writable paths rather than trusting prose alone. It also demonstrates that enforcement can include repository state, not just package presence: a workflow may have the right tools installed and still be unready if it cannot write to `okf/` or `.agents/skills/`, or if it is not inside a Git worktree. The newer skill summary sharpens this further by defining adoption rules that prose alone cannot guarantee: before first use of `graphify` or `openkb`, the corresponding read-only vendor skill must already exist under `.agents/skills/`, and generated wiki or raw content should not be written directly into OpenKB-owned directories outside the documented exceptions. The lock-file example reinforces a complementary point: generated lock metadata is useful for preserving exact dependency selections, but it is still separate from proving that the current machine and repository are ready. The action-vs-context guidance adds another layer to this distinction: procedural installation or remediation steps belong in skills, while background explanations of why a dependency exists, what architectural role it plays, or how the repository came to depend on it belong in the wiki. The vendor-skill guidance extends the same separation to third-party skills: manager state and lockfiles govern what is installed, but policy about when to vendor, when not to edit, and when to create a companion custom skill belongs in durable documentation. The skill-creator document also reinforces a compact authoring discipline: heavy dependency detail should not bloat `SKILL.md` when it can live in references or scripts. A workflow can appear well documented while still be nonfunctional if its dependencies are not actually checked, and it can be well automated while still being hard to understand if its rationale is not captured as durable context. The concept therefore overlaps with [[concepts/deterministic-validation]], [[concepts/tool-boundaries]], and [[concepts/agent-context-layering]].

## Required, optional, and companion dependencies

Dependency management benefits from classifying dependencies by role.

### Required local tools

Required tools are hard prerequisites for the workflow to operate. In the source material, these include tools such as Git, the UV Python toolchain, compatible Python, valid Git worktree membership, writable repository paths, and repository-local directories that must exist or be creatable before later steps can run.

The prereq checker models these as hard requirements and rolls them into a single failure result when missing. The important idea is that required dependencies should be:

- explicitly listed
- machine-checkable
- verified before work proceeds
- described in terms of both tool availability and environment constraints
- failed fast when absent or unusable

This makes dependency management about operational readiness, not just package presence. The checker also shows that writable-path validation belongs in the same category. If the workflow cannot create and remove a probe file in expected paths such as `okf/.okf-build/input`, `okf`, or `.agents/skills`, then the dependency story is incomplete even if every CLI is installed. The main skill adds that `uv` is the required execution path for bundled scripts and should not be silently substituted away; if `uv` is unavailable, that is a missing prerequisite that should trigger bootstrap guidance rather than an undocumented change in execution model. It also frames the KB root layout itself as a dependency precondition: repository work should assume `okf/` as the OpenKB root and `okf/wiki/` as the compiled wiki location, which turns path conventions into part of runtime readiness. The bootstrap reference supports this by making path layout explicit in the target structure and by directing durable knowledge to the wiki rather than to the bootstrap file. The workflow reference extends this by making `.gitignore`, `.gitattributes`, and `.graphifyignore` part of the readiness contract, because deterministic line endings, ignored build outputs, and graph exclusion are prerequisites for stable pipeline behavior. The skill-creator guidance strengthens this by requiring validation before finishing a skill and by recommending scripts whenever correctness matters or the same dependency logic would otherwise be rewritten repeatedly.

### Optional tools

Optional dependencies provide enhanced functionality but must not block the core workflow. In the source material, examples include [[entities/graphify]] for exploration output, [[entities/openkb]] for semantic wiki ingestion and compilation, and web access when external documentation evidence or baseline refresh work is explicitly requested.

Optional dependencies should:

- be identified clearly as optional
- have their value explained
- support graceful degradation when absent
- never be treated as hidden hard requirements
- produce clear notes about what capabilities are reduced

The prereq script follows this model by checking optional tools, reporting their status, and attaching actionable notes without marking the overall workflow as failed. It gives concrete degraded-mode explanations: without Graphify, source packs rely on git inventory and docs only; without OpenKB, the workflow falls back to a conservative skeleton generator. It also adjusts its probing behavior to reduce false negatives, such as allowing a longer timeout for `openkb --help` because first invocation may be slow due to imports. The main skill adds a stronger operational policy for optional tools: Graphify should run only when available, web-backed enrichment should happen only when the user provides external URLs, and non-code Graphify processing requires explicit backend disclosure before content may leave the machine. It also treats OpenKB commands differently by cost and blast radius, requiring extra consent before adding large directories, URLs, or PDFs, or before running broad and potentially destructive commands. This links to [[concepts/quality-gates]] because optional tools should not silently become mandatory through undocumented expectations. The newer skill guidance also adds that skills should explicitly explain degraded behavior when preferred tooling such as `uv` is unavailable and only then fall back to alternatives such as `python3`.

### Companion skills

The source also distinguishes companion skills from runtime dependencies. These are follow-on capabilities that may improve or extend the workflow, but the workflow should continue without them.

The newer dependency guidance formalizes companion-skill handling as metadata rather than as a standard manifest dependency field. A skill may expose a namespaced metadata key such as `<skill-name>.companion-skills` to note useful sibling skills, but that remains a local convention and does not change the core requirement that the skill must explain how it behaves when the companion is absent.

In the prereq checker, companion skills such as `skill-creator` and `subagent-profile-adapter` are checked via expected repository paths and reported as non-required when absent. Missing companion skills add notes about lost capabilities rather than causing hard failure. Those notes are specific rather than generic: missing `skill-creator` means repeated action skill creation is unavailable, while missing `subagent-profile-adapter` means harness-specific subagent or profile adapters cannot be hydrated automatically. That separation prevents over-coupling and preserves modularity within [[concepts/skill-based-automation]].

The main skill adds a sequencing rule to that distinction: `skill-creator` becomes relevant only after repeated actions are visible in the refreshed knowledge base, and `subagent-profile-adapter` should be used only after context and action skills are already prepared. This means companion dependencies can also be phase-dependent rather than simply optional in the abstract. The vendor-skill guidance sharpens a nearby distinction: a companion skill used to customize behavior is not the same thing as editing a vendor dependency in place. If project-specific behavior is needed around a third-party skill, the dependency should remain read-only and the customization should live in a separate project-owned skill. The skill-creator document reinforces the same rule as a boundary constraint for all created skills: project skills are editable local procedures, while vendored vendor skills remain dependencies. The action-vs-context reference clarifies the broader boundary: companion skills are still action-bearing assets, not repositories of long-lived explanation. If a companion skill encodes a repeated dependency workflow, it belongs in skill form; if analysis discovers lasting facts about why that workflow exists, those facts belong in wiki pages as durable context.

## Executable readiness as the source of truth

The source material emphasizes that dependencies should be validated by running a prereq script rather than trusting documentation alone. This is a strong dependency-management principle:

- documentation explains intent
- executable checks determine current reality

The newer guidance also says a prereq checker is especially appropriate when the workflow depends on local CLIs, credentials, network access, companion skills, or project-scoped vendored skills. The prereq script embodies this by actually invoking commands, resolving executables, checking whether the repository is inside a Git worktree, confirming vendored-skill preconditions for CLI use, and probing filesystem writability with a temporary file. It also emits both JSON diagnostics and human-readable output, which makes the dependency state usable by both automation and operators.

Several implementation choices strengthen the concept. The command runner resolves executable paths before invocation, which avoids command-shim problems on Windows and turns dependency checking into a cross-platform practice rather than a Unix-only assumption. The writable-path probe creates and deletes a temporary file instead of assuming directory existence implies usability, which is a stronger form of [[concepts/filesystem-validation]]. The script groups results into required, optional, vendored tool skills, companion skills, writable paths, and notes, which makes dependency state legible and machine-mergeable.

The main skill broadens executable readiness from tool presence into workflow readiness. It expects prerequisite checks before making changes when repository state is unknown, treats `openkb lint` plus bundle validation as downstream health gates, and insists that generated output be reviewed before acceptance. It also introduces a subtle but important readiness rule around deduplication state: `okf/.openkb/hashes.json` is a dependency of correct incremental ingestion behavior, so registry drift can leave the environment apparently ready while silently preventing expected rebuilds. That makes dependency management part of [[concepts/hash-registry-coherence]] and [[concepts/registry-drift]], not just package installation. The bootstrap reference reinforces this with an explicit caution that `.gitignore` should cover pipeline build artifacts and that the suggested command sequence should stage, build, ingest, lint, and validate in order. The workflow reference makes the same idea more concrete by showing that staged sources, graph updates, source-pack creation, OpenKB init, ingestion, lint, and validation form one ordered readiness chain. It also adds that lint findings must be preserved and triaged even when `openkb lint` exits successfully, which means health reporting itself is part of dependency governance. This approach improves repeatability and reduces ambiguity. It also helps align dependency handling with [[concepts/source-driven-regeneration]] and [[concepts/deterministic-validation]], because the system can re-check the environment consistently instead of relying on memory or informal setup notes. The vendor-skill guidance adds that manager-produced lock state is also not self-proving: a pinned vendor skill recorded in a lock file still benefits from explicit source review and repository-local policy checks. The skill-creator document adds a broader workflow expectation around this point: validation is not optional polish but part of the definition of a finished skill, and testing should happen baseline-first rather than by assuming the dependency story is already correct. At the same time, the action-vs-context guidance prevents this emphasis on executability from swallowing the documentation model entirely: the skill or checker performs the action, but the wiki preserves the durable explanation of architecture, design tradeoffs, provenance, and repository-specific discoveries that inform dependency policy.

## Provenance and package identity

Dependency management is not only about version numbers. It also includes knowing what a package actually is and where it comes from.

The source material treats each installable dependency as having a single authoritative upstream source that anchors its identity. This is especially important when:

- a CLI name differs from the package name
- older docs contain conflicting install instructions
- lookalike packages may exist
- the install comes through a mirror instead of a public registry
- a vendored skill is copied into the repository and might otherwise lose its upstream identity

The newer dependency reference makes this explicit by requiring detailed dependency docs to name the exact package, its registry, and its upstream source repository. It also gives a concrete identity table for tools such as [[entities/uv]], [[entities/graphify]], and [[entities/openkb]], including the important distinction that the Python package for Graphify is [[entities/graphifyy]] rather than `graphify`. The prereq script operationalizes this guidance in its notes by naming package identities and upstream sources for missing tools, and by distinguishing between a missing CLI and a missing repository-local vendored skill for that CLI. The main skill reinforces the same identity discipline by requiring install disclosures to include package name, configured index, upstream source, pinned version, and integrity-pin procedure before any bootstrap step. It also treats vendoring the corresponding read-only tool skill as part of adopting the tool, not an optional extra, which preserves provenance for future maintainers by keeping the repository-local usage contract tied to a known upstream artifact. The lock-file example supports the same discipline by giving each locked skill a `source` field alongside version and integrity data. The vendor-skill guidance applies the same rule to third-party skills more broadly: before installing or vendoring one, verify publisher, repository, and license, then review its `SKILL.md` and scripts for surprising instructions. The skill-creator document generalizes this into a default security expectation for created skills: any install guidance should identify the package registry and upstream source repository rather than leaving package identity implicit. This is where dependency management meets [[concepts/provenance-tracking]] and [[concepts/supply-chain-security]]. A package or skill should not be accepted merely because its name is familiar; it should be matched against its known upstream project and expected distribution channel.

The action-vs-context guidance also reinforces that provenance explanation is durable context. Evidence about why a dependency is trusted, which upstream is authoritative, or what historical decision led to a vendoring choice belongs in the wiki, while the commands that fetch, validate, or lock the dependency belong in a skill or tool.

## Version pinning and integrity recording

A major idea from summaries/agents__skills__agent-ready-context__references__dependencies-md and summaries/agents__skills__skill-creator__references__dependencies-md is that version pinning alone is insufficient. Safe dependency management adds integrity recording on top of exact version pins.

The model described is:

- install exact versions rather than floating ones for persistent setup instructions
- never leave `@latest` or equivalent floating instructions in guidance handed to future agents
- capture the integrity hash of the exact artifact retrieved from the configured index
- record version, integrity, index, and date together
- compare later installs against that recorded value
- stop and report if the same version from the same index no longer matches the recorded hash
- require user-confirmed release-note review before moving a pin

The newer guidance also narrows how integrity evidence is gathered: for Python tooling, the artifact sha256 should be captured from the environment's configured index, which may be an enterprise mirror and must not be bypassed or hardcoded. A hash mismatch for the same version from the same index is treated as a supply-chain incident, not a normal drift condition.

The lock-file example makes this concrete in a machine-readable form by showing a generated entry with `name`, `source`, `version`, and `integrity`. It also explicitly labels itself as an example and warns against hand-editing real vendor lock entries unless the tool supports it. That warning matters: integrity data is only trustworthy when it is generated and maintained by the responsible tool, not casually edited by hand. The vendor-skill guidance reinforces the same rule for third-party skills more broadly: vendor skill versions should be pinned through the skill manager and its lockfile, not tracked as floating latest, and updates should happen by re-vendoring or manager-driven refresh rather than by ad hoc editing. The skill-creator document complements this by requiring any created skill that installs or updates tooling to be explicit, version-pinned, and consent-first, which makes pinning a baseline creation rule rather than an optional hardening step.

The main skill adds an important repository-level recording rule: toolchain pins and their artifact hashes should be recorded in the target repository's `AGENTS.md`, and a mismatch for the same version and index is a stop-and-report event. That turns version pinning from a local convenience into a maintained repository contract. The prereq checker complements this model by surfacing the current installed tool version or a clear missing-state detail. In other words, pinning defines what should be present, while executable checks show what is actually present now. It also treats missing `uv` as a hard prerequisite and points users to the installer documentation rather than silently substituting an unpinned flow. Together, exact pins, source identifiers, and integrity values move the workflow closer to reproducible and auditable dependency state. This is effectively a [[concepts/trust-on-first-use]] pattern for tooling. It does not solve every supply-chain problem, but it detects changes after the first accepted baseline. That makes it an operational extension of [[concepts/supply-chain-security]], [[concepts/integrity-pinning]], and [[concepts/tooling-consent-and-pin-management]].

The action-vs-context guidance adds a placement rule here as well: lock maintenance, pin updates, and integrity verification procedures are workflow actions and should be encoded in skills or managers, while the rationale for choosing a specific pinning policy belongs in durable documentation.

## Registry-agnostic dependency handling

Another important part of this concept is avoiding assumptions about where dependencies come from. Enterprise environments often use mirrors, proxies, or internal indexes.

Good dependency management therefore:

- uses the package index already configured in the environment
- does not bypass a configured mirror to reach a public registry
- does not hardcode public registry URLs into persistent instructions
- reports missing packages instead of silently switching sources

The prereq script's remediation notes are consistent with this approach: they describe installation through the environment's configured Python index rather than assuming direct access to a public service. Its notes also pair package identity with upstream source, which helps preserve provenance even when the actual artifact is resolved through a mirror. The newer dependency guidance reinforces this by requiring integrity capture from the active configured index rather than from a bypassed upstream. The main skill matches this exactly: never override the configured mirror, never use `sudo`, and never leave floating versions in instructions. It also requires disclosure of package source and index before bootstrap, which makes registry choice explicit instead of implicit. This preserves policy compliance and environment predictability. The skill-creator document fits the same model by requiring install instructions to identify registry and source explicitly while still keeping the workflow compatible with local repository policy and configured tooling. It also keeps the dependency model compatible with private infrastructure while maintaining traceability through [[concepts/provenance-tracking]].

## Consent-first installation and updates

The source frames installation as a user choice, not an automatic side effect. Dependency management here includes a social and operational contract:

- show what tool is needed and why
- identify the package name and source
- show the exact pinned command
- let the user decide whether to install, delegate, or skip
- prefer user-scoped installers rather than privileged system-wide changes
- verify the result and re-run checks afterward

The newer guidance makes the installer policy explicit: installation should be consent-first and user-scoped, such as using [[entities/uv]] tool installation flows, never `sudo`. The same standard applies to updates. A newer version should be surfaced, release notes reviewed, and the pin moved only after explicit confirmation. The newer dependency reference also extends this consent model to vendoring required toolchain skills into the repository before first CLI use: project-scoped vendoring is part of the same adoption decision as installing the pinned CLI. The bootstrap reference mirrors this by making prerequisite checks the first action and by separating proposed installation commands from the user-consent step. The workflow reference adds that the build pipeline should not assume a provider is available; if the bundle lacks one, the process should generate a skeleton bundle and avoid claiming semantic completeness. The main skill strengthens that link by requiring bootstrap conversations to present package name, configured index, upstream source, pinned version, and integrity-pin procedure together, then letting the user choose between self-installation and agent-run installation. It applies similar consent rules to costly or broad OpenKB operations, large ingests, external web evidence collection, and wiki-convention customization. The prereq checker supports this model by stopping at diagnosis and recommendation; it does not install tools on the user's behalf. Instead, it reports missing hard requirements, explains degraded paths for optional tools, and notes when a CLI is installed but its vendored repository skill is still missing. The lock-file example sharpens this boundary by implying that lock entries are manager-generated artifacts, so changing dependency state should happen through the appropriate skill manager rather than by ad hoc manual edits. The vendor-skill guidance applies the same policy to third-party skills: installation through a skill manager is acceptable, but harness-level installation is only a user-requested alternative, and vendor updates still require pinned versions and deliberate review. The skill-creator document broadens this into a standard for every created skill: no silent installs, no privileged installation flow, and no secret material written into repository files. This aligns directly with [[concepts/tooling-consent-and-pin-management]] and supports privacy- and safety-oriented workflow design such as [[concepts/privacy-preserving-tooling]].

The action-vs-context reference fits this model by implying that install and update procedures are repeatable actions suited to skills, while policy explanations such as why consent is required or why a given dependency is optional should be captured as durable context.

## Graceful degradation

A mature dependency-management model does not fail unnecessarily. The source material repeatedly treats missing optional tools as a reason to degrade capability, not to abort the workflow.

Examples of graceful degradation include:

- continuing without optional exploration tooling
- continuing without semantic wiki tooling by using a more conservative output path
- continuing without companion skills while documenting what automation is unavailable
- using direct Python execution in a degraded mode when the preferred toolchain is explicitly declined
- generating a skeleton bundle when no provider is available

The newer dependency guidance adds a general rule: every documented installable requirement should state how the skill degrades when the tool is absent. The prereq script encodes this distinction directly: required failures flip the overall result to failed, while optional tool and companion-skill gaps generate notes only. It also gives concrete degraded-path messaging rather than generic warnings, which makes the fallback behavior actionable. For example, bare `python3` is framed as a degraded fallback only when the user explicitly declines `uv`, while missing OpenKB falls back to the conservative skeleton path and missing Graphify reduces source-pack richness rather than blocking the workflow. The main skill reinforces this by naming a zero-LLM fallback path with `build_okf_skeleton.py` and separate validation, and by treating offline staging and validation as still useful when richer tooling or provider connectivity is unavailable. The workflow reference further sharpens this: if Graphify fails, the pipeline continues without it and reports the failure; if no provider is available, the bundle is still generated but semantic completeness is not claimed. It also treats web access as enrichment rather than a prerequisite, which keeps external evidence gathering optional instead of structurally mandatory. The vendor-skill guidance supports the same pattern structurally: if project-specific behavior is needed, it should live in a separate custom skill rather than forcing modification of a vendor dependency, which keeps the base dependency stable while allowing optional extensions. The skill-creator document reinforces the same principle in both script execution and skill design: prefer `uv run`, but allow `python3` as a fallback when `uv` is unavailable, and keep the workflow usable even when optional companions are absent. This keeps the core workflow available while still reporting what has been lost. Good dependency management therefore balances rigor with practicality and is closely aligned with [[concepts/graceful-degradation]].

## Vendored dependencies and immutability

The source also covers vendored OpenKB skills as a dependency form. In that model, selected upstream skill directories are copied into the repository and treated as immutable vendor content.

The important dependency-management ideas are:

- prefer project-scoped vendoring over machine-wide changes
- record the source repository and version or commit used
- avoid editing vendored content in place
- update by re-vendoring from a newer reviewed version

The newer vendor-skill guidance generalizes this model. Vendored vendor skills are third-party content copied in read-only and should be safety-reviewed before vendoring, pinned by manager state and lockfiles when available, and left unmodified even when they do not perfectly match local conventions. They should be updated only through the skill manager or by re-vendoring a newer pinned version. If a lockfile exists, it should be committed as the reproducibility record.

The new dependency reference adds a sharper precondition: for certain CLIs, the vendored skill copy must land in `.agents/skills/<name>/` before the pipeline invokes that CLI. This is because the vendored skill is the repository-local, harness-neutral carrier of usage knowledge for later maintenance. The prereq script enforces this as a soft but explicit check: if a CLI such as Graphify or OpenKB is installed but the matching vendored skill is missing, it marks the vendored-tool-skill entry as not OK and adds a note telling the user to vendor the pinned copy before first use. If the CLI is not installed, missing vendored skill state is reported as not yet required. This conditional behavior is an important refinement because dependency management here is not just presence-based; it is dependency-by-intended-use. The main skill strengthens the policy further by treating vendoring as part of adopting the tool under the same user consent that approved installation, and by explicitly distinguishing required vendored tool skills from optional add-on skills that are never preconditions. The guidance also distinguishes project-scoped vendoring from harness-level installation, and prefers repository-local copies over user- or system-wide changes. It further notes discovery and directory-structure constraints for optional sibling skills, which makes vendoring not just a copying task but part of dependency correctness.

The same guidance also draws an important contrast with adopted generated skills. Both may live under `.agents/skills/`, but adopted generated skills become project-owned when brought in through an adoption workflow. They are expected to pass validation and then be edited and maintained like other custom skills. Vendor skills, by contrast, remain dependencies and should not be patched directly. That ownership distinction is central to safe dependency handling because it prevents the repository from blurring upstream dependency state with local custom logic. The skill-creator document makes this distinction explicit and adds that adopted generated skills must be reviewed for lost caveats or flattened constraints before being trusted as local skill assets.

The lock-file example fits this same model of controlled dependency state: a lock file records the selected vendor skill identity, source, version, and integrity as generated metadata, while the vendored payload remains separate from local customization. This preserves traceability and keeps local modifications from blurring the boundary between upstream dependency and local customization. It also fits the broader repository discipline described by [[concepts/documentation-architecture]].

The action-vs-context reference makes the customization rule more explicit: vendor skills are dependencies, should be installed and updated through the chosen skill manager, and should not be patched directly. Project-specific behavior should instead live in custom skills under `.agents/skills/`. That is both a dependency-management rule and a boundary rule between upstream dependency state and local action logic.

## Workflow-level dependency governance

The workflow reference adds a higher-level view: dependency management is not isolated from the build pipeline; it defines the pipeline's ordering and safety conditions.

Key governance rules include:

- read the KB index first when it exists, and let it determine subsequent wiki reads
- resolve tooling context before loading provider-specific guidance
- run prerequisite checks before graphing, staging, or ingestion
- vendor required tool skills before first CLI use
- keep `.gitignore`, `.gitattributes`, and `.graphifyignore` aligned with the build model
- stage source-pack input deterministically before OpenKB ingest
- preserve `openkb lint` reports even when the command exits successfully
- triage lint findings into the required classes before validation
- never recompile against a stale graph
- preserve consent boundaries for URL ingestion, broad recompile, and CI automation

This makes dependency management a control-plane concern. The workflow does not merely consume dependencies; it uses dependency state to decide what steps are allowed to happen at all. In that sense, dependency management is also [[concepts/knowledge-lifecycle-governance]], [[concepts/quality-gates]], and [[concepts/source-pack-staging]] in practice.

The workflow document also extends the self-reference rule: the wiki must stay out of the graph, because graphing the wiki into itself breaks fixed-point determinism, creates circular grounding, and pollutes discovery with generated pages. That is why `.graphifyignore` must exclude `okf/`. This directly supports [[concepts/self-reference-control]] and [[concepts/repo-scoped-graph-partitioning]].

## Action/context placement for dependency knowledge

The action-vs-context reference contributes a general rule that helps keep dependency management maintainable over time.

When dependency information describes a repeatable procedure, it belongs in an action-bearing asset such as a skill. This includes:

- multi-step install or update sequences
- lock regeneration workflows
- integrity verification procedures
- migration steps for changing dependency managers
- scripted remediation for failed prerequisite checks
- wrappers around vendor skills with repository-specific guardrails
- bootstrap flows that merge routing rules into `AGENTS.md` and stage generated input into the KB pipeline

When dependency information describes durable understanding, it belongs in the wiki. This includes:

- why a dependency exists
- how it relates to repository architecture
- the tradeoffs behind pinning or vendoring choices
- provenance evidence for package identity
- historical decisions about mirrors, indexes, or optional tooling
- background for why a runbook or dependency workflow exists
- why `AGENTS.md` stays short while `okf/wiki/` carries the durable explanation

Concise operator orientation, such as where dependency-related skills live, what commands to run first, and which repo rules apply, belongs in entities/agents-md. The newer dependency guidance adds a further placement rule within skills themselves: portable manifest fields stay minimal, namespaced metadata carries local hints, `references/dependencies.md` holds the detailed requirement narrative, and the prereq script proves current readiness. The prereq script also shows why this split matters operationally: a single executable checker can centralize version checks, worktree checks, vendored-skill conditions, writable-path probes, and optional-tool status instead of scattering those requirements across prose. The main skill expands the durable-context side of this split by explicitly defining `okf/wiki/` as the source of truth for long-lived repository context and warning against putting long-form knowledge into `AGENTS.md` or converting context into a skill unless it represents a repeatable action. It also establishes that when generated knowledge output is weak or wrong, the repair should happen in source documents and re-ingestion rather than by hand-editing compiled wiki pages. The bootstrap reference adds that `AGENTS.md` should remain a short routing and rules file and points agents to `okf/wiki/index.md` as the front door. The vendor-skill guidance extends this model with an ownership rule: third-party skills remain dependency assets governed by manager state and source provenance, while project-specific adaptations belong in custom companion skills. The skill-creator document sharpens the same placement model structurally: `SKILL.md` stays short and procedural, `scripts/` holds deterministic code, `references/` holds heavy detail, and `assets/` holds templates or static resources. It also insists that skills are not knowledge bases and should not absorb durable explanatory material that belongs in wiki pages. This separation keeps executable dependency logic in the right place, preserves durable context, and prevents orientation docs from becoming overloaded. It aligns dependency management with [[concepts/context-action-separation]], [[concepts/durable-context]], and [[concepts/agents-md-maintenance]].

## Practical signals of good dependency management

A workflow has strong dependency management when it:

- defines which tools are required, optional, or companion-only
- keeps `SKILL.md` spec-compliant and avoids inventing a `dependencies` field
- uses `compatibility` for concise environment expectations and namespaced metadata only for local hints
- documents detailed requirements in `references/dependencies.md`
- checks readiness with code, not just prose
- validates repository state such as Git worktree membership, writable paths, required vendored skill locations, and KB root expectations
- ties each dependency to an upstream source and registry
- uses exact pins for reproducible setup
- records integrity values for later comparison
- preserves resolved state in manager-generated lock data where applicable
- respects the environment's configured package indexes
- gets user consent before installation, vendoring, pin changes, broad recompilation, or costly ingestion steps
- prefers user-scoped or project-scoped installers and avoids privileged installation flows
- scopes declared tool access minimally and does not confuse those declarations with enforcement
- explains how the workflow degrades when optional tools are unavailable
- keeps vendored dependencies traceable and immutable
- distinguishes immutable vendor skills from editable adopted or custom skills
- reviews third-party skill source, license, instructions, and scripts before installation
- preserves caveats when adopting generated skills into project-owned form
- stores repeated dependency procedures in skills rather than in long-form prose
- stores design rationale, provenance, and historical background as durable wiki context
- stages deterministic generated input outside tool-owned compiled directories before ingestion
- treats hash-registry state as part of dependency correctness for incremental compilation
- exposes diagnostics in both machine-readable and human-readable forms
- validates before considering a dependency-bearing skill complete
- handles cross-platform command discovery carefully instead of assuming Unix-style execution semantics
- treats writable repository paths as real prerequisites rather than incidental setup details
- uses post-generation review and validation gates before accepting compiled outputs
- keeps `AGENTS.md` focused on routing, commands, and pointers to the wiki rather than detailed dependency analysis
- excludes the wiki from repo-graph inputs so dependency knowledge does not recurse back into its own source

## Relevance to this wiki

This concept is most directly grounded in summaries/agents__skills__agent-ready-context__references__dependencies-md, summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py, summaries/agents__skills__agent-ready-context__SKILL-md, summaries/agents__skills__skill-creator__assets__skill-lock-example-json, summaries/agents__skills__skill-creator__references__action-vs-context-md, summaries/agents__skills__skill-creator__references__dependencies-md, summaries/agents__skills__skill-creator__references__vendor-skill-management-md, summaries/agents__skills__skill-creator__SKILL-md, summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md, and summaries/agents__skills__agent-ready-context__references__workflow-md. It also supports understanding adjacent topics such as [[concepts/tool-boundaries]], [[concepts/provenance-tracking]], [[concepts/supply-chain-security]], [[concepts/deterministic-validation]], [[concepts/skill-based-automation]], [[concepts/tooling-consent-and-pin-management]], [[concepts/skill-governance]], [[concepts/context-action-separation]], [[concepts/durable-context]], [[concepts/agent-ready-repositories]], [[concepts/consent-first-tooling]], [[concepts/self-reference-control]], and [[concepts/source-pack-staging]].

## See also

- summaries/agents__skills__agent-ready-context__SKILL-md
- summaries/agents__skills__agent-ready-context__references__dependencies-md
- summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py
- summaries/agents__skills__skill-creator__SKILL-md
- summaries/agents__skills__skill-creator__assets__skill-lock-example-json
- summaries/agents__skills__skill-creator__references__action-vs-context-md
- summaries/agents__skills__skill-creator__references__dependencies-md
- summaries/agents__skills__skill-creator__references__vendor-skill-management-md
- summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md
- summaries/agents__skills__agent-ready-context__references__workflow-md
- [[concepts/tool-boundaries]]
- [[concepts/supply-chain-security]]
- [[concepts/provenance-tracking]]
- [[concepts/deterministic-validation]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/skill-based-automation]]
- [[concepts/skill-governance]]
- [[concepts/graceful-degradation]]
- [[concepts/integrity-pinning]]
- [[concepts/context-action-separation]]
- [[concepts/durable-context]]
- [[concepts/agent-ready-repositories]]
- [[concepts/consent-first-tooling]]
- [[concepts/self-reference-control]]
- [[concepts/source-pack-staging]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/README-md]]