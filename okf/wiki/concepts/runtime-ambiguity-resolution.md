---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md"]
description: "Resolves active harness identity from conflicting runtime signals."
---

# Runtime Ambiguity Resolution

Runtime ambiguity resolution is the practice of determining which agent harness or execution environment is actually active when multiple signals are available but none is perfectly authoritative. It favors explicit proof over inference, preserves uncertainty, and treats weaker hints as guidance rather than certainty.

This concept is central to [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]], which collects environment, process, and repository signals to infer the current runtime without invoking vendor CLIs. It also underpins [[concepts/adaptive-harness-detection]] and the runtime-specific workflow described in [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]].

## Core idea

A runtime can present several plausible identities at once: environment variables may mention one harness, parent processes may suggest another, and repository markers may indicate compatibility with yet a third. Runtime ambiguity resolution handles this by ranking evidence, separating active execution from passive compatibility hints, and keeping uncertainty visible instead of forcing a brittle yes/no answer.

This makes it especially useful in mixed or layered environments where a repo supports more than one harness, where a shell session is nested, or where installed tools do not prove what is currently running.

## Signal hierarchy

The source script distinguishes between several classes of evidence:

- Explicit runtime-related environment variables are treated as the strongest signals.
- Parent process command lines and process names provide moderate evidence.
- Repository markers such as `.claude`, `.opencode`, or `AGENTS.md` are treated as low-confidence hints.
- Installed binaries are deliberately excluded as proof, because they do not establish which harness is currently active.

This reflects [[concepts/confidence-calibration]] and [[concepts/runtime-signal-prioritization]]: strong signals should outweigh weak ones, but weaker signals still help explain the environment.

The broader skill also reinforces the distinction between observing the harness and acting on it. It recommends checking docs or official references when harness semantics are unknown, and asking the user when runtime identity remains ambiguous.

## Behavior in the source document

The script in [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]:

- reads explicit runtime-related environment variables
- collects additional environment hints from editor and harness-related variables
- walks the `/proc` parent chain to inspect process names and command lines
- scans the repository for harness markers
- scores candidate harnesses by signal type
- emits decision guidance that warns against confusing presence with active execution

The output is a JSON report that keeps the ambiguity visible by listing candidate harnesses, their confidence, and the signals behind each candidate.

The parent skill extends this same idea into adapter generation: runtime detection is only the first step, because the active harness must then be checked for support of local subagents or profiles before any native adapter files are written.

## Why it matters

This concept supports reliable agent behavior in mixed or layered environments. It helps avoid incorrect assumptions when a repo is compatible with multiple harnesses, when tooling is installed but not in use, or when the current session has enough hints to be plausible but not conclusive.

It also reinforces [[concepts/non-invasive-detection]] and [[concepts/adaptive-harness-detection]] by basing conclusions on passive observation rather than command execution. In the subagent-profile-adapter workflow, it is a guardrail against confusing compatibility markers with actual runtime identity.

## Related ideas

- [[concepts/harness-vs-local-tools]]: distinguishes active runtime context from merely available tools
- [[concepts/harness-native-profiles]]: uses runtime-specific profile adaptation
- [[concepts/context-action-separation]]: separates observation of context from acting on it
- [[concepts/confidence-calibration]]: assigns confidence based on evidence strength
- [[concepts/runtime-signal-prioritization]]: orders competing runtime hints by reliability
- [[concepts/non-invasive-detection]]: infers context without probing vendor CLIs
- [[concepts/permission-scoped-agents]]: keeps harness-specific behavior bounded to the needed runtime capabilities
- [[concepts/tooling-context-governance]]: keeps harness evidence separate from durable project knowledge

## Practical outcome

A good ambiguity-resolution strategy produces a cautious answer such as "likely Claude Code" or "possible Codex runtime" rather than a false absolute claim. When evidence remains weak or conflicting, it should either surface multiple candidates or ask the user for confirmation.

In the adapter workflow, that caution prevents premature file generation and helps ensure that any generated subagent or profile files match the actual harness rather than a guessed one.