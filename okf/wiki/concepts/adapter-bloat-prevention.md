---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md"]
description: "Keeping profile adapters narrow, source-linked, and non-redundant."
---

# Adapter Bloat Prevention

Adapter bloat prevention is the practice of keeping harness-specific profile or subagent adapters small, focused, and operationally specific instead of turning them into catch-all documentation bundles. The subagent-profile-adapter skill treats this as a core design constraint: adapters are runtime-specific projections, not a place to store durable project knowledge or broad reference material.

## Why it matters

Profile adapters are meant to describe how a specialized context should behave: what task it handles, when it should be invoked, what skills it may use, what repository context it should consult, how permissions should be narrowed, and what it must not do. When adapters expand beyond that role, they blur boundaries between execution instructions, repository knowledge, and reference material. Preventing bloat supports [[concepts/harness-native-profiles]], [[concepts/context-action-separation]], and [[concepts/minimal-tool-scoping]].

Keeping adapters lean also improves maintainability. A concise adapter can point to the current source of truth instead of copying material that will drift over time. That aligns with [[concepts/documentation-source-priority]], [[concepts/durable-context]], and the adapter skill's emphasis on using current local or official documentation rather than hardcoded vendor renderers.

## What bloat looks like

The source guidance explicitly says profile adapters must not embed:

- long project architecture descriptions;
- copies of OKF pages;
- full external documentation;
- long troubleshooting narratives;
- vendor documentation beyond the minimum fields needed to make the file valid.

The skill also pushes against other forms of overgrowth: it says adapters should be short, task-scoped, permission-bounded, and derived from actual repository needs, OKF pages, and reusable skills rather than from copied context. In other words, bloat is any material that belongs in `AGENTS.md`, `okf/wiki/`, or `.agents/skills/` instead of the adapter itself.

## Preferred alternative: reference, do not copy

Instead of carrying large bodies of context, adapters should point to stable repository resources:

- `AGENTS.md` for orientation;
- `okf/wiki/` for source-of-truth context;
- `.agents/skills/` for available actions.

The skill's boundary model makes this explicit: OKF wiki content is the durable knowledge base, `AGENTS.md` is the orientation/index, Agent Skills are reusable procedures, and adapters are only the runtime-specific projection for the active harness. That layered model connects directly to [[concepts/agent-context-layering]], [[concepts/documentation-architecture]], [[concepts/skill-based-automation]], and [[concepts/tooling-context-governance]].

The document also stresses a policy of strict link direction: tooling context may inform project context, but project concept pages must not link back into tooling pages. That reinforces [[concepts/link-directionality]] and [[concepts/tooling-link-policy]] while keeping adapters from becoming a backdoor for tooling knowledge to leak into the project graph.

## Design implications

A well-scoped adapter should act like a narrow dispatch layer rather than a knowledge archive. It should help the harness choose and constrain behavior, not reproduce every relevant background document. In practice, adapter bloat prevention encourages:

- short intent-focused definitions;
- explicit links to authoritative context;
- narrow permission and task boundaries;
- reuse of existing skills instead of embedded procedures;
- lower risk of stale or conflicting duplicated guidance.

The adapter skill adds a few operational constraints that support this design:

- detect the active runtime from real harness signals, not installed binaries;
- confirm whether the harness actually supports local subagents or profiles;
- ask how generated files should be tracked before writing them;
- keep generated files short and harness-native;
- validate that profiles do not embed large project context.

Those practices reinforce [[concepts/permission-scoped-agents]], [[concepts/tool-boundaries]], [[concepts/runtime-ambiguity-resolution]], and [[concepts/deterministic-validation]].

## Source grounding

The clearest source for this concept is [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]], which frames profile adapters as harness-specific files that must remain minimal, repository-driven, and carefully separated from durable project knowledge. The skill also introduces a validation step for tooling link policy, showing that keeping adapters small is tied to preserving graph hygiene as well as readability.

## Takeaway

Adapter bloat prevention keeps profile adapters useful by limiting them to the information needed to route and constrain behavior, while delegating orientation, repository knowledge, runtime detection, and action details to the right supporting documents.

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]