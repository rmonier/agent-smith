---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
description: "Rules that keep harness tooling context separate from project knowledge."
---

# Tooling Context Governance

Tooling context governance is the set of rules that keeps harness-specific documentation, adapter files, and runtime evidence separate from durable project knowledge. It defines where tooling details belong, how they may link, and how they should be validated so they do not become mistaken for project source of truth.

## Core idea

The main goal is [[concepts/documentation-layer-separation]]: project knowledge stays in the compiled wiki, while harness-specific context lives in `okf/wiki/tooling/`. This keeps runtime adapters useful without letting them reshape the repository's durable knowledge graph.

## Source-driven rules

The [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]] document frames tooling governance through a few strict boundaries:

- `AGENTS.md` is the repo orientation file, not a place for runtime projections.
- Agent Skills are reusable procedures and scripts.
- Subagent/profile adapters are runtime-specific outputs for the active harness only.
- `okf/wiki/` remains the source of truth for durable project knowledge and provenance.

The document also says not to create extra `.agents/` directories beyond `.agents/skills/`, which helps prevent adapter sprawl and keeps generated harness files bounded.

## Link and dependency policy

A central part of this concept is [[concepts/link-directionality]]. Tooling pages may reference project pages, but project concept pages must not point back to tooling pages. That asymmetry preserves [[concepts/tooling-context-isolation]] and prevents harness details from leaking into the compiled knowledge base.

The source document also requires the bundle-root `okf/wiki/index.md` to list `okf/wiki/tooling/` in a clearly labeled harness-specific section when tooling pages exist. That makes tooling discoverable without elevating it into normal project navigation.

## Validation expectations

Tooling governance is not just about where content lives; it is also about verifying that it stays within bounds. The skill requires validation that:

- generated adapters are in the correct harness location;
- profile files do not embed large chunks of OKF or project content;
- project concept pages do not link back to `okf/wiki/tooling/`;
- the root index includes the tooling section when applicable.

This aligns with [[concepts/generated-artifact-validation]] and [[concepts/tooling-link-policy]].

## Runtime awareness

The document emphasizes [[concepts/adaptive-harness-detection]] and [[concepts/runtime-signal-prioritization]]: the active harness should be identified from explicit runtime evidence, not from installed binaries or assumptions. If the runtime is ambiguous, the user should be asked.

That approach supports [[concepts/runtime-ambiguity-resolution]] and reduces the risk of generating adapters for the wrong environment.

## Why it matters

Tooling context governance protects the wiki from becoming a mixed archive of project facts and harness-specific mechanics. It keeps generated adapters short, local, and auditable, while preserving the wiki as a stable knowledge base and making it easier to maintain [[concepts/knowledge-layer-separation]] and [[concepts/single-source-of-truth]].

See also: [[summaries/README-md]]