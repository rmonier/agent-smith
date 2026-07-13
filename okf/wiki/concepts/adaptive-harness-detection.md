---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
description: "Detecting the active harness to safely adapt runtime behavior and tooling."
---

# Adaptive Harness Detection

Adaptive harness detection is the practice of identifying which agent harness is actually running so the system can adapt runtime behavior, logging, tooling scope, and adapter generation without guessing. It supports resilient handling of harness-specific quirks while keeping the knowledge base grounded in observed execution rather than assumptions.

The `inspect_runtime_context.py` script adds a concrete detection model for this idea: it collects explicit environment values, softer environment hints, parent-process evidence from `/proc`, and repository marker hits, then scores candidate harnesses without invoking vendor CLIs. Its output is a JSON report that separates strong signals from weak ones and includes decision guidance to avoid mistaking installed binaries or repo artifacts for proof of the active runtime.

This concept also underpins the broader workflow for generating runtime-specific projections. The `subagent-profile-adapter` skill treats harness-specific subagents or profiles as native adapter files for the active harness only, not as a portable standard. That means adaptive harness detection is a prerequisite for writing those adapters safely, because the agent must know whether the current runtime even supports local subagents or profile semantics before creating anything.

## Why it matters

Different harnesses can change sandbox constraints, background-task behavior, timeout needs, instruction-file expectations, and other operational details that affect how agent workflows should run. Detecting the harness reliably helps the system decide when to record a build note, when to skip a record because identification is uncertain, how to preserve accurate runtime context for later use, and whether local subagent or profile adapters are even meaningful for the current environment.

This matters most in tooling-context governance and tooling-context isolation, where runtime knowledge must remain user-scoped and should not be treated as project truth. It also interacts with harness-native profiles because a detected harness determines whether native profile or subagent projections should be written at all. The `subagent-profile-adapter` skill treats harness-specific adapters as runtime projections, not as a portable standard, and it only writes them after confirming the active runtime and its local profile semantics.

The runtime inspector reinforces that boundary by preferring explicit environment values such as `AGENT_HARNESS`, `HARNESS`, and `AGENT_RUNTIME`, while treating repo markers like `.claude`, `.opencode`, `.agents/skills`, and `AGENTS.md` as hints only. That distinction is important because the script is designed to support runtime ambiguity resolution rather than collapse uncertainty into an arbitrary guess.

## Core behavior

- Identify the active harness using explicit runtime signals rather than heuristics that require guessing.
- Treat installed tools, repo hints, and file presence as low-confidence evidence unless they are backed by runtime signals.
- Use runtime detection as a gate before generating harness-specific subagent or profile adapters.
- Ask the user which harness to target if the active runtime remains ambiguous.
- Record a harness build note only when the harness can be determined reliably.
- Include the harness name and version, the detection method, the date of the pass, and any observed operational quirks when a record is written.
- If the harness cannot be determined, say so in the run report and continue without creating a speculative record.
- Keep tooling context limited to the approved cases instead of accumulating broad harness documentation.
- Keep adapter files short and native to the harness, with only the purpose, activation details, supported permissions or tools, and pointers back to `AGENTS.md`, `okf/wiki/`, and skills.
- Avoid using `--version` output or installed binaries alone as proof of the active harness.
- Prefer explicit harness metadata, parent-process clues, and environment hints before resorting to repo files as weak evidence.
- When the harness is ambiguous, stop and ask rather than inferring a target from local artifacts.
- Score multiple weak signals together so the system can surface likely candidates without pretending to have certainty.

## Policy implications

Adaptive harness detection constrains how tooling pages are created and maintained. Under the tooling context policy, harness-specific records belong in `okf/wiki/tooling/harnesses/<harness>.md`, while fuller adapter documentation is only appropriate when a specific harness is actively in use. That makes detection a prerequisite for documenting runtime-specific projections, not an invitation to infer them.

The same principle also supports runtime ambiguity handling and runtime signal prioritization: the agent should favor runtime evidence it can verify, then narrow its behavior to the detected environment. The inspector’s guidance makes this explicit by warning that repo markers and installed binaries are not active runtime proof. It also aligns with consent-first tooling and local-by-default tooling by keeping generated harness outputs local unless the user or repository policy says otherwise.

The `subagent-profile-adapter` skill extends this policy into execution: it first checks that the repository has the expected agent-ready context, then detects the active runtime, then verifies whether local subagents or profiles are supported, and only after that designs and writes adapter files. It also requires validation of the adapter location and link policy so project concept pages do not depend on tooling context pages.

## Related ideas

- [[concepts/runtime-signal-prioritization]] for deciding which runtime clues matter most
- [[concepts/runtime-ambiguity-resolution]] for deciding when uncertainty is too high to proceed
- [[concepts/explicit-provider-routing]] for separating harness detection from provider selection
- [[concepts/tooling-context-pages]] for the local pages that may be created once a harness is known
- [[concepts/local-tooling-boundaries]] for keeping user-scoped tooling separate from project knowledge
- [[concepts/subagent-role-design]] for shaping task-scoped adapter roles after the harness is known
- [[concepts/permission-scoped-agents]] for keeping generated adapters narrow in scope
- [[concepts/agent-ready-context-skill]] for the precondition that prepares repository and wiki context before runtime-specific work
- [[concepts/harness-native-profiles]] for the cases where a harness supports local profile or subagent projections
- [[concepts/tooling-context-governance]] for the policy layer that keeps runtime context scoped correctly
- [[concepts/tooling-context-isolation]] for keeping harness details separate from project knowledge
- [[concepts/local-by-default-tooling]] for preferring local tracking of generated harness files
- [[concepts/consent-first-tooling]] for requiring user or policy approval before broader tracking

## Practical outcome

When adaptive harness detection works well, the agent can produce accurate harness records, avoid silent omissions, and keep the wiki coherent across different clones and users. When it fails safely, the system preserves correctness by refusing to guess and by treating the missing record as an explicit, reported condition rather than a hidden error. It also prevents unnecessary adapter work in environments that do not support local subagents or profile files, and it keeps harness-specific files from growing into accidental project documentation.

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]