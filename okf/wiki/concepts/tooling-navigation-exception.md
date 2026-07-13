---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
description: "Rules for keeping tooling context local, navigable, and boundary-safe."
---

# Tooling Navigation Exception

The tooling navigation exception is the rule set that makes `tooling/` a special, user-scoped area inside OKF/wiki. It allows local harness and provider context to live outside normal project knowledge while still keeping the wiki coherent, validated, and navigable.

This exception is defined in [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]] and sits at the intersection of [[concepts/tooling-context-isolation]], [[concepts/tooling-link-policy]], [[concepts/local-by-default-tooling]], and [[concepts/tooling-navigation-exceptions]]. It also supports the broader separation between durable project knowledge and runtime-specific projections described in [[concepts/runtime-adapter-management]] and [[concepts/wiki-context-routing]].

## What the exception permits

- A small committed navigation stub at `okf/wiki/tooling/index.md`.
- Local pages under `okf/wiki/tooling/harnesses/` for harness build records.
- Optional local pages under `okf/wiki/tooling/providers/` for runtime observations.
- A root `okf/wiki/index.md` entry pointing to the tooling stub when local tooling pages exist.
- Short, native adapter notes that refer back to `AGENTS.md`, `okf/wiki/`, and reusable skills without turning tooling pages into project source of truth.

These pages are allowed because tooling context is treated as operational metadata, not project truth. The adapter guidance in [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]] reinforces that these runtime projections should stay short, harness-specific, and separate from durable OKF content.

## What makes it an exception

Normally, OKF wiki content follows the same indexing and link expectations as other knowledge pages. Tooling content breaks that pattern in a controlled way:

- local pages are not enumerated in committed indexes
- project concept pages must not link back into `okf/wiki/tooling/`
- the tooling stub must remain user-neutral and non-speculative
- only a limited set of tooling pages is allowed to exist
- runtime detection and harness validation should be based on explicit environment clues and docs, not installed binaries alone

This keeps the wiki compatible with [[concepts/progressive-disclosure]] while avoiding broken references across clones. It also preserves a clean boundary between durable compiled knowledge and harness-specific runtime state, which is central to [[concepts/knowledge-boundaries]] and [[concepts/tooling-context-governance]].

## Why it matters

The exception solves a practical tension between two goals:

- preserve reproducible, inspectable harness/runtime notes
- prevent user-specific runtime details from polluting shared project knowledge

Without this carve-out, tooling context would either be lost or would contaminate the compiled knowledge base. With it, the wiki can support [[concepts/tooling-context-governance]] and [[concepts/knowledge-boundaries]] at the same time. It also lets runtime adapters exist as projections rather than sources of truth, which aligns with [[concepts/adapter-bloat-prevention]] and [[concepts/agent-context-layering]].

## Operational rules

The policy requires that:

- the root index must reference tooling when local tooling pages exist
- local tooling pages must contain at least one valid wikilink to durable project knowledge
- tooling pages remain local by default and do not get ingested as source material
- validation should enforce the boundary rather than relying on manual discipline
- active harness detection should prefer explicit runtime signals and documentation, with user confirmation when ambiguous
- generated adapter files should stay minimal and point back to shared repo guidance instead of embedding large context blocks

This is a boundary-management pattern, not just a folder rule. It connects tooling navigation to [[concepts/runtime-ambiguity-resolution]], [[concepts/non-invasive-detection]], and [[concepts/generated-artifact-validation]].

## Related ideas

- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/local-by-default-tooling]]
- [[concepts/tooling-link-policy]]
- [[concepts/wikilink-integrity]]
- [[concepts/knowledge-boundaries]]
- [[concepts/runtime-adapter-management]]
- [[concepts/runtime-ambiguity-resolution]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]