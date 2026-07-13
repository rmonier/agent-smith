---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
description: "Separates harness-specific tooling context from durable project knowledge."
---

# Tooling Context Isolation

Tooling context isolation is the practice of keeping harness-specific documentation, adapter guidance, and runtime evidence separate from the project knowledge base that agents use for durable compilation and navigation. In the subagent profile adapter skill, this separation is treated as a hard boundary: project knowledge lives in the OKF wiki, repo orientation lives in `AGENTS.md`, reusable procedures live in skills, and harness adapters remain runtime-specific projections.

## Why It Matters

This concept exists to prevent harness details from becoming mistaken for project truth. When tooling notes, runtime semantics, or adapter files are mixed into compiled project pages, agents can start depending on transient environment behavior as if it were stable domain knowledge. The skill therefore frames tooling pages as support material for the active harness, not as a source of truth for the repository itself.

It also matters because adapter generation is intentionally local to the active runtime. The skill does not define a portable subagent standard; instead, it helps the current agent detect the harness, verify whether local subagents or profiles are supported, and emit only the native files expected by that environment. That keeps runtime-specific projections disposable unless the user explicitly wants them shared.

## Core Boundaries

- OKF wiki content is the durable project knowledge source.
- `AGENTS.md` is the repository orientation and best-practices file.
- `.agents/skills/` contains reusable actions and procedures.
- Harness adapters are generated for the active runtime only.
- Tooling documentation belongs in `okf/wiki/tooling/`, not in extra `.agents/` folders.
- The bundle-root wiki index must enumerate tooling in a clearly labeled harness-specific section when tooling pages exist.
- The committed `tooling/index.md` navigation stub keeps tooling coherent on every clone.

This produces a clear layer split between [[concepts/compiled-knowledge-bases]], [[concepts/documentation-layer-separation]], and [[concepts/tooling-context-governance]].

## Source-Driven Rules

The subagent profile adapter skill makes several practical demands that reinforce isolation:

- detect the active harness from runtime signals, not from installed binaries alone;
- inspect parent process or environment hints before relying on repo files;
- consult local or official docs before generating native adapter files;
- keep adapter files short and pointed back to `AGENTS.md`, `okf/wiki/`, and skills;
- avoid embedding large amounts of project context inside profile files;
- validate that project concept pages do not link back to tooling pages;
- preserve tooling evidence only when persistence is useful, and otherwise keep it transient.

These rules support [[concepts/runtime-ambiguity-resolution]], [[concepts/adaptive-harness-detection]], and [[concepts/link-directionality]].

## Link Direction Policy

The document establishes a one-way knowledge flow:

- tooling context can reference project context;
- project concept pages must not depend on tooling context.

That policy protects the wiki from self-referential tooling loops and preserves clean navigation across compiled knowledge. It also aligns with [[concepts/tooling-link-policy]] and [[concepts/self-reference-control]]. In practice, this means tooling pages may mention project pages such as `AGENTS.md` or the OKF wiki, but concept pages should never treat tooling pages as durable source material.

## Practical Outcome

When tooling context is isolated correctly, the repo can support multiple harnesses without collapsing them into the same knowledge layer. The wiki stays reusable across environments, the agent orientation file stays concise, and runtime adapters remain disposable or locally scoped unless the user explicitly chooses to share them.

The result is a cleaner workflow for harness-aware agenting: durable knowledge stays in the wiki, repeated procedures become skills, and generated adapters remain projections of the current runtime rather than new sources of truth.

## Related Source

- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]