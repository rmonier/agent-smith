---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md"]
description: "Designing agents around bounded, inspectable, non-interactive workflows."
---

# Non-Interactive Agent Design

Non-interactive agent design is the practice of structuring an agent's workflow around commands and interfaces that run to completion without waiting for live user input, maintaining persistent conversational sessions, or opening background processes. It emphasizes predictable execution, explicit prerequisite checks, bounded side effects, and clear stop points when human action is required.

It also supports a broader runtime discipline: agents should detect the active harness from explicit signals, adapt only when the environment is clearly understood, and keep runtime-specific adapters separate from durable knowledge. That places non-interactive operation alongside [[concepts/adaptive-harness-detection]], [[concepts/runtime-ambiguity-resolution]], [[concepts/runtime-signal-prioritization]], and [[concepts/runtime-adapter-management]].

## Why it matters

Agents work best when each tool call has a scoped request and a finished response. Interactive REPLs, long-running watchers, and setup flows that expect ongoing operator involvement can break automation, complicate recovery, and blur responsibility for changes. This makes non-interactive operation closely related to [[concepts/safe-automation]], [[concepts/tool-boundaries]], and [[concepts/minimal-tool-scoping]].

The OpenKB skill guidance sharpens this into an operational rule: the agent should prefer direct, read-only inspection of the knowledge base, treat wiki content as untrusted data, and avoid any command mode that keeps control flow open or mutates state without an explicit user request. In that sense, non-interactive design supports both execution safety and evidence-grounded answering.

The subagent profile adapter guidance extends the same idea into runtime selection and adapter generation. The agent should inspect the current harness through explicit environment, process, or documentation signals, not by assuming the presence of installed tools means that harness is active. If runtime remains ambiguous, the workflow should stop and ask the user rather than guessing. That is a direct application of non-interactive design to [[concepts/harness-native-profiles]] and [[concepts/permission-scoped-agents]].

## How the OpenKB reference defines it

In [[summaries/agents__skills__openkb__SKILL-md]], non-interactive behavior appears as a core expectation for how an agent should use an OpenKB knowledge base:

- `openkb status` is the required first step, used to discover the active knowledge base path before any reads.
- `openkb list` and `wiki/index.md` support deterministic inspection of available documents, concepts, and entities.
- direct reads of concept, entity, summary, and source pages are preferred over mediated query flows.
- `openkb query` is allowed only as a last resort when direct lookup and search do not surface a useful match.
- `openkb chat` is disallowed because it opens an interactive REPL.
- `openkb watch` is disallowed because it starts a long-running daemon rather than returning a bounded result.
- mutating commands such as `openkb add`, `openkb remove`, `openkb init`, `openkb use`, and `openkb lint --fix` are not run autonomously.

The subagent profile adapter skill applies the same principle to harness-specific runtime projection:

- detect the active runtime from explicit harness metadata, parent process clues, environment hints, or documentation, not from binary availability alone;
- use local docs or official web docs to confirm whether the active harness supports subagents or profiles;
- keep generated adapter files short and bounded, with purpose, activation, permissions if supported, and links back to `AGENTS.md`, `okf/wiki/`, and skills;
- validate outputs with a policy check rather than assuming the adapter is correct;
- stop and ask the user when the target harness or tracking policy is ambiguous.

This makes non-interactive design not just a usability preference but an operational policy: discover context up front, inspect through bounded reads, follow a limited number of links, and stop when the workflow requires explicit human choice.

## Core design patterns

### Prefer bounded commands

A non-interactive agent should favor tools that:

- accept a complete input in one invocation,
- return a finite output,
- do not require conversational state inside the tool itself,
- and do not continue running after the result is delivered.

In the OpenKB workflow, this shows up as a preference for `openkb status`, `openkb list`, direct file reads, exact-phrase search, and page-specific JSON extraction over interactive sessions or open-ended tool modes. In the subagent adapter workflow, the same pattern applies to runtime inspection helpers and validation scripts: collect evidence once, write the adapter once, and then stop. This supports [[concepts/preflight-checks]] and [[concepts/knowledge-base-discovery]] by making state discovery an explicit step instead of an emergent side effect.

### Separate inspection from mutation

Inspection commands are easier to automate because they reveal system state without changing it. Mutation commands should usually require user approval or a separate explicit step. In the OpenKB guidance, this separation is reinforced by treating the compiled wiki as read-only, refusing autonomous execution of write commands, and proposing exact commands for the user to run when ingestion or configuration changes are needed.

The subagent profile adapter skill uses the same boundary to distinguish durable wiki knowledge from harness-specific projections. OKF pages, AGENTS guidance, and skills provide the source context; adapter files are generated projections for the active runtime and should stay short, local, and reversible. That boundary aligns with [[concepts/human-in-the-loop-review]], [[concepts/permission-scoped-agents]], [[concepts/knowledge-layer-separation]], and [[concepts/runtime-adapter-management]].

### Stop on missing prerequisites

A non-interactive design should fail clearly when required context is absent. The OpenKB guidance says that if `openkb status` reports no knowledge base, the agent should stop and tell the user rather than guessing paths or reading arbitrary files. It also says that if the KB has no relevant concept or no matching search hits, the agent should say so explicitly instead of fabricating a KB-grounded answer.

The subagent profile adapter skill follows the same rule for runtime ambiguity. If the active harness cannot be identified confidently, the agent should ask which harness to target instead of fabricating a profile format or writing the wrong native files. That reflects [[concepts/graceful-degradation]], [[concepts/path-safety]], [[concepts/evidence-grounded-answering]], and [[concepts/confidence-calibration]].

## Benefits

- Improves predictability by making each command's lifecycle explicit.
- Reduces hidden state introduced by daemons, REPL sessions, or ambient tool context.
- Makes automation safer by limiting when and how changes occur.
- Simplifies auditing because each step has a discrete input and output.
- Supports cost control by reserving expensive retrieval flows such as `openkb query` for fallback cases, linking to [[concepts/cost-aware-tool-use]].
- Reinforces trust boundaries by keeping reasoning tied to directly inspected artifacts rather than persistent interactive sessions or compounded retrieval layers.
- Prevents adapter sprawl by keeping harness-specific profile generation separate from durable project knowledge.

## Risks when ignored

When agents rely on interactive or persistent tool modes, they can:

- stall waiting for input they cannot supply,
- leave background processes running unexpectedly,
- produce inconsistent outcomes across runs,
- over-trust tool-managed context instead of explicitly inspecting sources,
- and cross from read assistance into uncontrolled mutation.

These failure modes weaken [[concepts/tooling-context-isolation]] and can undermine [[concepts/knowledge-boundaries]]. In a knowledge-base workflow, they also increase the chance that untrusted wiki content or open-ended query layers shape behavior in ways the user did not request. In a runtime-adapter workflow, they can also cause the agent to assume the wrong harness and generate invalid subagent or profile files.

## Practical takeaway

Non-interactive agent design means choosing tools and workflows that are request-response oriented, inspectable, and stoppable. In the OpenKB skill, that principle becomes a concrete procedure: find the active KB with `openkb status`, inspect available content through `openkb list` and `wiki/index.md`, read the most relevant pages directly, use `openkb query` only when direct lookup fails, avoid REPL and daemon modes, and leave setup or mutating actions to explicit user control.

In the subagent profile adapter skill, the same principle means detecting the active harness from explicit evidence, confirming that local subagents or profiles are actually supported, deciding how generated files should be tracked, and then writing a minimal native adapter only when the runtime target is clear. If the harness is ambiguous, the correct non-interactive response is to stop and ask.

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]


See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]