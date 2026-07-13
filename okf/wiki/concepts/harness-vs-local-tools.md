---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Separates harness permissions from repository tool readiness and runtime detection."
---

# Harness vs Local Tools

[[summaries/agents__skills__agent-ready-context__references__dependencies-md]] draws a strict boundary between capabilities exposed by the current agent environment and commands that must exist in the repository's execution environment. This distinction prevents permission hints from being mistaken for installed software, and prevents local dependency checks from being replaced with assumptions about the harness.

## Definition

Harness tools are capabilities the active agent runtime exposes directly, such as reading files, editing files, running shell commands, searching the workspace, or fetching web content. Local tools are repository-environment executables such as `git`, `uv`, `python`, `graphify`, and `openkb` that must actually be present, callable, and appropriate for the target workflow.

The core rule is simple: harness capabilities determine what the agent is allowed or able to do in the current session, while local tools determine what the repository workflow can execute. One does not imply the other.

## Why the distinction matters

Confusing these layers causes avoidable failures:

- A skill may declare `allowed-tools`, but that is only a permission hint, not proof that a local CLI is installed.
- A harness may provide shell access, but shell access does not guarantee that `uv` or `openkb` exists in `PATH`.
- A repository may depend on a CLI even when the harness already provides roughly similar native abilities.
- A local CLI may be installed, but the harness may still forbid the actions needed to invoke it safely.
- Runtime inspection should rely on explicit signals, parent-process clues, and repository markers as evidence, not as proof of active harness identity.

This makes the concept central to [[concepts/tool-boundaries]], [[concepts/executable-validation]], [[concepts/permission-scoped-agents]], and [[concepts/adaptive-harness-detection]].

## Two separate responsibility layers

### Harness layer

The harness owns runtime permissions and interaction surfaces:

- file read/write/edit abilities
- shell execution
- search and web-fetch capabilities
- approval and escalation flow
- enforcement of destructive-command restrictions, if supported

This is a permissions and environment-exposure problem, not a package-installation problem. The source document explicitly says permission enforcement belongs to the harness, even if a skill declares `allowed-tools`.

Runtime detection should therefore prefer strong, explicit signals when they exist and fall back to weaker hints only for orientation. The inspected script models this by reading explicit environment variables, checking parent processes, and gathering repo markers without invoking vendor CLIs.

### Local tool layer

The repository environment owns executable readiness:

- whether required binaries such as `git` and `uv` are installed
- whether the correct Python version is available
- whether repository paths are writable
- whether optional tools such as `graphify` and `openkb` are present
- whether vendored skill copies exist where the workflow expects them

This is why readiness is checked through executable validation rather than metadata alone, connecting the idea to [[concepts/filesystem-validation]], [[concepts/path-based-validation]], and [[concepts/single-source-of-truth]].

## Source-specific guidance

In [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], the authoritative source for local readiness is `check_prereqs.py`. That design encodes several important ideas:

- `SKILL.md` stays spec-compliant and does not become a dependency manifest.
- `allowed-tools` may describe expected harness-side capabilities but cannot guarantee enforcement or installation.
- local CLI readiness must be tested directly through a script that checks commands, versions, writable paths, and vendored skill state.
- the workflow should degrade gracefully when optional local tools are missing.

The runtime-inspection script extends that pattern for subagent adaptation. It collects explicit environment variables, softer environment hints, repository markers, and the parent-process chain, then scores candidate harnesses while warning that installed binaries are not proof of the active harness. That makes runtime identification a case of [[concepts/adaptive-harness-detection]] and [[concepts/runtime-signal-prioritization]] rather than a single-source lookup.

## Common failure modes this concept prevents

### Mistaking permissions for installation

An agent may be allowed to use the shell, but `uv` can still be missing. A workflow that assumes shell access implies tool readiness will fail late and unclearly.

### Mistaking installation for permission

A machine may have `openkb` installed, but the harness may deny writes, web access, or even shell execution. Installed software cannot override harness policy.

### Treating metadata as enforcement

A skill's declared `allowed-tools` might describe intended usage, but the source document warns that this field is only advisory. Using it as if it were an enforced contract confuses policy declaration with runtime truth.

### Treating weak runtime signals as proof

Environment hints, process names, and repo markers can improve confidence, but they should not be confused with a guaranteed harness identity. The script's guidance explicitly warns against that overreach.

### Blurring optional and required tooling

When optional CLIs are absent, the workflow should continue in a reduced mode rather than collapsing. Distinguishing the harness layer from the local tool layer helps preserve this [[concepts/graceful-degradation]] behavior.

## Relationship to consent and safety

The distinction also supports safer automation:

- harness permissions should follow least privilege and ask before risky actions
- local installs should be explicit, pinned, and consent-first
- untrusted fetched content should not be treated as commands to run
- repository workflows should verify actual prerequisites before executing transformations
- runtime detection should stay non-invasive and avoid probing vendor CLIs just to guess the active environment

This links the concept to [[concepts/safe-automation]], [[concepts/tooling-consent-and-pin-management]], [[concepts/supply-chain-security]], and [[concepts/prompt-injection-defense]].

## Practical application

When working in an agent-ready repository, evaluate both layers separately:

1. What can the current harness actually do right now?
2. What local CLIs and files does the repository workflow require?
3. Which of those requirements are mandatory versus optional?
4. Which checks are documented, and which are executable?
5. Which runtime clues are explicit, and which are only hints?

The source document's answer is that harness capabilities may enable actions, but only direct local checks can establish workflow readiness. For runtime context, the stronger signals should drive decisions, while hints and markers remain advisory. That separation is a durable pattern in [[concepts/agent-ready-repositories]], [[concepts/skill-based-automation]], and [[concepts/durable-context]].

## See also

- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[concepts/executable-validation]]
- [[concepts/permission-scoped-agents]]
- [[concepts/graceful-degradation]]
- [[concepts/single-source-of-truth]]
- [[concepts/safe-automation]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/supply-chain-security]]
- [[concepts/agent-ready-repositories]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/runtime-signal-prioritization]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]
