---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__runtime-detection-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__references__action-vs-context-md.md", "summaries/agents__skills__skill-creator__assets__skill-template-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Distinct layers between guidance, runtime, permissions, and local execution"
---

# Tool Boundaries

Tool boundaries are the distinctions between what a skill can describe, what an agent harness can authorize, what a role or profile can intend, which runtime is actually active, and what the local repository environment can execute. In practice, this means not treating metadata, permissions, bundled scripts, profile intents, runtime hints, installed command-line tools, package provenance, vendored skill copies, or repository markers as interchangeable sources of truth.

This concept is central to the dependency model in the agent-ready-context materials, which keeps declarative metadata separate from executable readiness checks, package installation policy, and vendored tool-skill adoption. It also appears in subagent-profile-adapter, which frames skills as reusable action capabilities with explicit limits: they can document workflows, declare minimal expected tools, and ship validation scripts, but they do not control the harness or the machine. The same boundary is reinforced by the profile intents example, which shows that subagent profiles can express purpose, context, and permission expectations without becoming native enforcement or execution policy, and by the runtime-detection guidance, which warns against mistaking installed tooling or repository residue for evidence of the active harness. The runtime-inspection script makes the same distinction operational by collecting explicit environment variables, parent-process evidence, and repo markers while still warning that installed binaries are not proof of the active harness. The OKF offline baseline extends the same idea into wiki validation: repository source remains the source of truth, `okf/wiki/` is the durable knowledge source of truth, and validation must distinguish spec conformance from OpenKB-specific policy and harness behavior.

## Core idea

A skill or profile can express expectations, but it does not control the whole execution environment.

Five layers must stay distinct:
- skill metadata and documentation such as `compatibility`, `description`, `license`, namespaced `metadata.*`, workflow steps, command examples, security notes, and edge-case guidance
- profile intents such as purpose, use conditions, required context, and permission expectations for subagent roles
- harness tools and permissions such as read, write, edit, shell, search, or web access
- active runtime signals such as explicit harness metadata, direct user instruction, parent process evidence, and harness-specific environment variables
- local CLIs and runtimes such as `git`, `uv`, Python, `graphify`, and `openkb`

A sixth operational distinction also matters in practice:
- install and supply-chain state such as package identity, configured indexes, exact version pins, integrity hashes, vendored skill copies, and whether those copies were adopted project-scoped or only installed user-wide

Confusing these layers leads to incorrect assumptions, such as believing that a listed tool is installed locally, that a command example is always safe to run, that a permission hint guarantees enforcement, that a role description automatically becomes harness-native policy, that a binary on `$PATH` proves which harness is currently running, or that an installed CLI automatically implies its repository-local skill guidance is present.

This separation aligns with agent-context-layering, dependency-management, executable-validation, and okf-validation.

## What the source documents establish

The source material makes several boundary-setting rules explicit:

- `SKILL.md` must remain spec-compliant and should not invent custom dependency fields.
- frontmatter fields such as `name`, `description`, `license`, `compatibility`, and `metadata` identify and scope the skill, but they do not serve as an install manifest.
- a skill's `description` should act as a trigger for when to invoke it, not as a substitute for the full workflow.
- profile intents can describe purpose, when to use a role, what context it needs, and what permissions it expects, but they are still portable intent descriptions rather than vendor-specific enforcement files.
- workflow steps describe an intended deterministic procedure, but they do not prove the harness can grant the needed actions or that the machine can execute them.
- command blocks document likely usage, but they are examples of execution, not evidence that the referenced binaries are present.
- `allowed-tools` is only a hint about expected harness capabilities, not proof of enforcement and not a package manifest.
- active runtime detection should prefer explicit harness metadata, direct user instruction, parent process evidence, and harness-specific environment variables over ambient repository clues.
- repository configuration files are only low-confidence hints about runtime targeting and should not outweigh stronger execution-context signals.
- runtime inspection should avoid invoking vendor CLIs just to test their presence, because installed binaries are not proof of the active harness.
- local readiness must be checked through executable validation, such as prereq checks and quick validation scripts.
- package provenance, version pins, configured-index behavior, and integrity checks belong to installation and bootstrap workflows, not to skill metadata or profile text alone.
- permission enforcement is owned by the harness, not by the skill or the profile.
- an installed CLI and a vendored project-local skill are related but separate adoption states; one does not prove the other.
- generated or adopted skills still need project-side review, because distillation can erase important caveats and conditional constraints.
- if runtime evidence is weak or conflicting, the correct action is to ask the user which harness to target or whether to skip profile generation.
- OKF validation rules require every non-reserved Markdown file to carry parseable frontmatter, while `index.md` and `log.md` keep reserved structures.
- in OpenKB mode, broken `wikilinks` are treated as errors, missing machine-managed `sources:` lists become warnings, and `tooling/` is a special hand-authored exception that still must be declared in the wiki’s navigation and policy files.

This creates a clean division of responsibility:
- metadata describes
- profile intents express role boundaries and expected context
- runtime detection infers the active harness from current execution evidence
- workflow sections instruct
- the harness authorizes
- the local environment provides binaries and runtimes
- installation policy governs package names, indexes, version pins, integrity, and vendored skill copies
- validation scripts verify whether those binaries and runtimes are actually usable
- wiki validation verifies bundle structure, reserved files, and OpenKB-specific conventions
- human review restores caveats that packaging or generation may flatten

That structure supports quality-gates, tooling-consent-and-pin-management, supply-chain-security, and reserved-wiki-files.

## Metadata is not execution

A recurring mistake in skill systems is to read metadata as if it were operational truth. The source material rejects that pattern, and the profile-intents example extends the same warning to role descriptions.

Examples:
- Declaring `allowed-tools` does not mean the harness exposes those tools.
- Declaring a compatibility expectation does not mean the machine satisfies it.
- Including namespaced metadata hints does not create a portable standard.
- Naming a tool in documentation does not confirm the package name, source, install path, or configured index.
- Listing a command in a workflow does not mean the command is available or permitted.
- Writing a deterministic procedure does not guarantee that every step can run in the current environment.
- Describing a subagent as read-only by default does not prove the harness enforces read-only behavior.
- Stating that a role may write only under user policy does not itself implement that policy.
- Finding a vendor CLI in `$PATH`, seeing a config folder in a home directory, or reading a repo marker file does not prove that harness is the active runtime.
- The runtime-inspection script intentionally uses those clues only as signals, scoring parent-process text, explicit environment variables, and repo markers without elevating any one of them to proof.
- Old generated profile folders in the repo do not prove they match the harness currently executing the agent.
- A public package name shown in old docs does not outweigh verified upstream identity when names conflict.
- Installing a CLI does not prove the repository contains the corresponding vendored skill needed for durable local guidance.
- Packaging knowledge into a generated skill does not preserve every boundary or exception unless the adopted copy is reviewed.

Because of this, metadata and profile definitions should remain descriptive and lightweight, while actual execution requirements are enforced through checks, explicit bootstrap steps, harness-level controls, vendoring rules, and runtime-specific evidence. Structured sections such as workflow, commands, permissions, and context improve clarity, but they remain documentation until validated or enforced by the correct layer. This is closely related to documentation-architecture and source-driven-regeneration.

## Harness tools versus local CLIs

The source material draws a direct line between harness capabilities and local commands.

Harness tools are agent-environment capabilities, for example:
- reading files
- editing files
- shell execution
- web fetch or search

Local CLIs are repository-environment commands, for example:
- `git`
- `uv`
- Python
- `graphify`
- `openkb`

Profile intents sit adjacent to these layers but remain distinct from both. A profile may say that a role has read-only default permissions, limited shell use, or write access that depends on user policy, but those are still expectations to be translated into the native harness model.

The active runtime is another separate layer. Runtime identification should be based on current execution evidence such as explicit harness metadata, direct user instruction, parent process chain, or harness-specific environment variables. Repository configuration files can help as weak hints, but they should not override stronger signals from the actual running context.

The distinction matters because a harness may allow shell access while the required local binary is still missing. Conversely, a binary may exist locally while the harness forbids using it. Similarly, a profile may request narrow permissions while the actual harness configuration is broader, narrower, or differently named. A valid workflow must account for all of these conditions. It must also avoid assuming that because several harnesses are installed, any one of them is the current execution target.

The dependency reference adds a further boundary inside the local-tool layer: an installed CLI, its package identity, its pinned version, its artifact integrity, and its vendored project skill are not the same fact. For example, a repository may have shell access and `uv`, but still lack a verified install of `openkb` or `graphify`; it may have the CLI installed from the configured index, but not have the required `.agents/skills/<name>/` vendor copy; or it may have an old vendored copy that no longer matches the approved pin. The documented command and the local binary are only part of the picture.

The source material reinforces this boundary by requiring minimal tool scoping and by recommending `uv run` for bundled Python scripts when available. That convention improves isolation and repeatability, but it still does not guarantee that `uv` exists, that shell access is granted, that the correct package was installed from the configured index, or that the intended harness is the one currently executing the agent. A commands block can show what should be run, and a profile can describe the intended permission envelope, but only the harness, local machine, and install state determine whether running it is possible. This boundary is one reason the source material requires deterministic prereq checks rather than relying on declarations alone, connecting to executable-validation and skill-based-automation.

## Why executable checks are the source of truth

The source material treats prerequisite and quick validation scripts as the executable source of truth for readiness. That reflects an important principle: environment claims should be verified in a repeatable way.

Executable checks are better than assumptions because they can confirm:
- whether required tools are installed
- whether versions are acceptable
- whether writable paths exist
- whether optional tools are available for enhanced workflows
- whether the environment is degraded and needs to be reported as such
- whether the documented workflow can realistically be attempted under current conditions
- whether a generated or adopted skill actually meets the repository's validation standard
- whether required vendored skill directories are present before CLI-dependent steps run
- whether the bundle satisfies OKF frontmatter and reserved-file rules
- whether OpenKB-specific `wikilinks` and wiki navigation remain intact

Runtime inspection follows the same pattern. Context-gathering helpers can collect evidence without invoking vendor CLIs, but their output is still evidence rather than authority. Detection should remain evidence-based and should escalate to the user when signals conflict.

This is a boundary between documentation and validation. Documentation explains what should be present; validation determines what is present now. Profiles contribute another form of documentation: they help route work to the right role and scope expected permissions, but they still do not verify that the environment matches the description. Runtime heuristics help identify the active harness, but they do not replace explicit confirmation when confidence is low. The skill creation workflow makes validation an explicit final step, and its baseline-first testing model strengthens the same idea: first observe where unaided execution fails, then add the skill, then verify the remaining gaps are closed. That pattern reinforces quality-gates, baseline-first-testing, failure-driven-development, and deterministic-validation.

## Tool boundaries and consent

The concept also has a governance side: a skill or profile should not silently cross boundaries from guidance into machine changes.

In the source material, installs are consent-first and user-scoped. The workflow requires the user to be shown:
- what tool is wanted
- why it is needed
- where it comes from
- which package name maps to the tool
- which version is pinned
- which index or mirror will supply it
- what exact command would be run
- whether a repository-local vendored skill copy will also be added

Only then can the user choose whether to install, skip, or perform the install themselves. This keeps tool discovery, authorization, installation, vendoring, and execution separate, supporting tooling-consent-and-pin-management and privacy-preserving-tooling.

The same boundary appears in profile intents. A role may say that writes to `okf/wiki/` or `AGENTS.md` should ask or allow according to user policy, or that shell access should be limited to validation scripts, but that still preserves consent by describing constraints rather than bypassing them. A profile can narrow expectations; it cannot self-authorize actions.

Runtime targeting has the same consent and ambiguity boundary. If the active harness cannot be confidently identified, the system should ask the user which harness to target or whether profile generation should be skipped, rather than silently generating artifacts for the wrong environment. This keeps runtime inference subordinate to explicit user direction when evidence is weak, matching runtime-ambiguity-resolution and runtime-signal-prioritization.

The same boundary applies to generated skills adopted from wiki-derived output: adoption is explicit, project-local, and reviewed rather than automatic. A generated artifact can suggest an action pattern, but it should not cross into trusted executable policy without human acceptance and validation. That directly connects tool boundaries to generated-artifact-adoption and human-in-the-loop-review.

## Tool boundaries and security

Boundary clarity also improves security.

When permissions, install state, runtime identity, fetched content, provenance, package identity, configured index, vendored skill copies, and role descriptions are separated, the workflow can apply focused controls:
- harness permissions follow least privilege
- local installs are pinned, provenance-checked, and integrity-checked
- runtime targeting uses current execution evidence rather than ambient machine state
- fetched web content is treated as untrusted input
- secrets remain outside repo-tracked files
- generated artifacts stay out of version control until adopted intentionally
- command examples remain reviewable instructions rather than hidden execution triggers
- role or profile text remains auditable intent rather than implicit executable policy
- vendored tool skills are treated as immutable vendor content rather than casually edited local code
- wiki pages remain validated source-backed knowledge rather than arbitrary freeform content

Without tool boundaries, these concerns blur together and make it easier to over-trust metadata, bypass package controls, mistake profile guidance for enforced restrictions, infer the wrong runtime from installed tools, silently move version pins, accept lookalike package names, assume unsafe commands are allowed, or treat bundle navigation as optional. This directly supports supply-chain-security, provenance-tracking, prompt-injection-defense, and wikilink-integrity.

## Practical implications

When applying this concept in an agent-ready repository:
- keep skill metadata descriptive rather than overloading it as a package manifest
- write the skill description as an invocation trigger, not as a compressed workflow
- use profile intents to describe role purpose, context, and expected permissions without treating them as enforcement
- use workflow sections to describe repeatable actions, but do not confuse them with guaranteed execution rights
- treat command blocks as documentation that still depends on harness permissions and local binaries
- detect the active runtime from execution-context signals rather than from installed tools or stale repository artifacts
- treat repository config, repo markers, and generated profile folders as hints, not proof
- ask the user when runtime evidence is ambiguous or conflicting
- declare only the minimal expected tool scope
- verify local CLI availability with deterministic checks
- use bundled validation scripts instead of assuming metadata is enough
- document degraded modes and edge cases instead of pretending all environments are identical
- separate package identity, pinned version, integrity record, and vendored project copy when reasoning about tool readiness
- respect configured package indexes and mirrors rather than bypassing them
- keep vendored tool skills separate from project-owned skills and treat them as immutable vendor content
- keep generated skills separate from project-owned skills until explicit adoption and review
- compare adopted generated skills against their source context so lost caveats are restored
- record install provenance and pins outside lightweight skill declarations or profile text
- validate OKF bundle structure and OpenKB wiki conventions instead of relying on directory shape alone
- preserve reserved `index.md` and `log.md` roles and treat broken `wikilinks` as build-time damage in OpenKB-managed content

These practices help preserve predictable automation behavior across repositories and harnesses.

## See also

- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__skill-creator__references__dependencies-md]]
- [[summaries/agents__skills__skill-creator__references__testing-skills-md]]
- [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]
- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]
- [[summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__runtime-detection-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
- [[concepts/dependency-management]]
- [[concepts/executable-validation]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/supply-chain-security]]
- [[concepts/provenance-tracking]]
- [[concepts/agent-context-layering]]
- [[concepts/quality-gates]]
- [[concepts/caveat-preservation]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/okf-validation]]
- [[concepts/reserved-wiki-files]]
- [[concepts/wikilink-integrity]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__openkb__references__commands-md]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]