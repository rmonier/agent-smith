---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
description: "Using only the narrowest tools and permissions a workflow truly needs."
---

# Minimal Tool Scoping

Minimal tool scoping is the practice of declaring and using only the smallest set of tools and tool permissions needed to complete an action safely and reliably. In skill design, this reduces accidental capability expansion, makes the intended operating boundary explicit, and helps separate harness capabilities from repository-local command dependencies.

This concept is emphasized in [[summaries/agents__skills__skill-creator__SKILL-md]], which treats narrow tool access as a default safety property for created skills. It is reinforced by [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], which distinguishes permission hints from actual local tool readiness and requires explicit prereq checking for repository workflows. It is also sharpened by [[summaries/agents__skills__openkb__references__commands-md]], which shows the same principle at the CLI level by separating safe inspection commands from commands that mutate the knowledge base.

## Core idea

A skill should ask for as little execution authority as possible:

- Prefer a short, specific `allowed-tools` list over broad access.
- Scope shell permissions to the concrete need, such as `Bash(git:*)` rather than unrestricted `Bash`.
- Treat tool declarations as guidance rather than enforcement; the instructions themselves must still remain safe if the environment grants more access than expected.
- Distinguish harness tools from local CLIs: a skill may expect read, write, search, or shell capabilities from the harness while separately requiring local commands such as `git`, `uv`, or `python` in the repository.
- Use executable prereq checks for local command availability instead of implying that a permission hint also guarantees installation or readiness.
- Prefer narrowly read-oriented commands over expensive or stateful alternatives when a direct inspection path exists.
- Reserve mutating commands for explicit user direction rather than folding them into autonomous default behavior.

This makes minimal scoping both a design rule and a documentation rule. It tells future agents what the action genuinely depends on, helps reviewers notice when a skill is requesting more power than its task justifies, and prevents metadata from blurring the line between permission scope and environment setup. This fits closely with [[concepts/tool-boundaries]], [[concepts/harness-vs-local-tools]], and [[concepts/executable-validation]].

## Why it matters

Minimal tool scoping supports several goals:

- It lowers the chance that a reusable skill performs unrelated or overly destructive actions.
- It makes the action easier to audit because the expected tool surface is small and visible.
- It reinforces user consent by making required capabilities explicit.
- It helps separate deterministic execution needs from convenience-driven overreach.
- It reduces confusion between what the agent is allowed to do and what the repository environment is actually prepared to support.
- It encourages workflows to prefer direct reads and bounded inspection before escalating to broader, more expensive, or mutating operations.

Within a skill ecosystem, broad tool grants can blur boundaries between narrowly procedural skills and general-purpose operator access. The same is true when a skill treats an `allowed-tools` declaration as if it were an install manifest or a guarantee that local CLIs already exist. A similar failure appears when an automation path treats every available CLI command as fair game instead of respecting distinctions between status, query, interactive, daemon, and write operations. Minimal scoping keeps a skill aligned with its specific action contract, which fits the broader patterns of [[concepts/tool-boundaries]], [[concepts/skill-governance]], and [[concepts/single-source-of-truth]].

## In the skill-creator source

The skill-creator source states that every created skill should:

- Declare the minimal `allowed-tools` set the action actually needs.
- Use scoped shell hints like `Bash(git:*)`, not a generic unrestricted shell declaration.
- Remain safe even though `allowed-tools` is only a hint and not a hard enforcement mechanism.

That last point is important: minimal scoping is not solved by metadata alone. The procedural instructions, scripts, and validation approach must also assume that safety comes from careful design, not only from platform controls. This aligns the concept with [[concepts/executable-validation]] and [[concepts/deterministic-validation]].

The agent-ready-context dependency guidance sharpens the same principle from the environment side:

- `allowed-tools` is a permission hint only.
- compatibility metadata can summarize environment expectations, but should not replace real readiness checks.
- local CLI requirements should be validated by scripts rather than inferred from the skill declaration.
- optional companion capabilities should not be promoted into hard dependencies unless the workflow truly requires them.

The OpenKB command guidance applies the same logic to command selection inside a tool:

- establish the active knowledge base with `openkb status` before attempting reads.
- prefer direct listing and deterministic inspection before using `openkb query`, which carries additional model cost.
- avoid interactive or daemon-style commands in autonomous flows.
- do not autonomously invoke commands that mutate the knowledge base.
- treat curated wiki content and internal state directories as protected areas rather than normal write targets.

Together, these sources show that minimal scoping applies both to agent permissions and to dependency claims. A narrowly scoped skill should request only the powers it needs, choose only the least powerful commands that answer the question, and describe only the local tools it can actually justify and verify.

## Relationship to safety defaults

Minimal tool scoping is one part of a larger safety posture for reusable skills. In the surrounding source guidance, it appears alongside other defaults such as:

- no silent software installation
- consent-first and version-pinned setup
- keeping secrets in environment variables rather than repo files
- treating fetched web content as untrusted data
- disclosing generated artifacts and ensuring they are gitignored when appropriate
- degrading gracefully when optional tools are unavailable rather than expanding scope to compensate informally
- respecting protected state areas and declining autonomous writes even when a tool technically exposes them

Together, these form a coherent model of constrained, reviewable automation. Minimal scoping is the entry point: first limit what the skill can or expects to do, then constrain how it handles dependencies, data, commands, and outputs. This connects naturally to [[concepts/tooling-consent-and-pin-management]], [[concepts/prompt-injection-defense]], [[concepts/supply-chain-security]], [[concepts/graceful-degradation]], and [[concepts/provenance-tracking]].

## Practical implications for skill authors

When authoring or reviewing a skill, minimal tool scoping usually means asking:

- Does this skill really need shell access at all?
- If shell access is needed, can it be narrowed to a specific command family?
- Are file writes limited to the action's intended area?
- Is network access implied, and if so, is that need clearly justified and safely handled?
- Do the scripts and instructions rely on any capability not declared in the skill metadata?
- Are local CLI requirements checked explicitly rather than assumed from the presence of shell access?
- Are optional tools presented as optional, with a clear degraded path if they are absent?
- If a CLI offers both inspection and mutation commands, does the workflow explicitly prefer the inspection path first?
- Are interactive, daemon, or persistent-state commands excluded from autonomous execution unless the user clearly asks for them?
- Are protected directories or internal state locations named as out of bounds even when write access exists in principle?

These questions help keep a skill action-focused rather than vaguely powerful. They also help preserve a clean boundary between permissions, prerequisites, workflow stages, and command classes, which supports [[concepts/context-action-separation]], [[concepts/skill-structure-conventions]], and [[concepts/dependency-management]].

## Signals of poor scoping

Common signs that tool scope is too broad include:

- unrestricted shell access for a task that only needs one command family
- adding tools "just in case"
- instructions that assume install, network, or write access without saying so
- metadata that understates or overstates what the scripts actually do
- combining unrelated actions into one skill so that the tool list keeps expanding
- treating permission hints as if they also guarantee local package installation or environment readiness
- turning optional helper tools into apparent hard requirements without an explicit workflow reason
- defaulting to high-cost query flows when direct reads or listings would suffice
- invoking interactive, watch, or write commands in unattended workflows without explicit user approval
- treating internal state or curated knowledge directories as ordinary write targets

These are usually governance and maintenance issues as much as technical ones, because oversized tool scope often reflects an unclear skill boundary. They can also indicate a breakdown in documentation authority, where executable checks, source references, and declared permissions no longer agree. That ties the concept to [[concepts/action-oriented-documentation]], [[concepts/documentation-architecture]], and [[concepts/spec-authority]].

## Summary

Minimal tool scoping means keeping a skill's operational authority as narrow as its action allows. In the skill-creator, agent-ready-context, and OpenKB command guidance, it is a default for safe reusable skills: declare the least capability needed, scope shell access precisely, separate harness permissions from local CLI prerequisites, prefer bounded inspection over broader command paths, and make sure the workflow remains safe even when permission metadata is not strictly enforced.

## Related pages

- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__openkb__references__commands-md]]
- [[concepts/tool-boundaries]]
- [[concepts/harness-vs-local-tools]]
- [[concepts/skill-governance]]
- [[concepts/context-action-separation]]
- [[concepts/executable-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/prompt-injection-defense]]
- [[concepts/skill-structure-conventions]]

See also: [[summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]