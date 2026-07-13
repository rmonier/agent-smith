---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
description: "Rules that keep local tooling context separate from project knowledge."
---

# Local Tooling Boundaries

Local tooling boundaries define how harness, runtime, and adapter context stays separate from project knowledge in the OKF wiki. The goal is to let agents capture environment-specific details without turning them into durable project truth.

## Core idea

Tooling pages are **user-scoped**, not project-scoped. They describe the environment of the agent runner, such as harness behavior, model/provider quirks, and local runtime observations. That means they belong in the tooling overlay, not in normal project concept pages.

This boundary is a form of [[concepts/knowledge-boundaries]] and [[concepts/documentation-layer-separation]]: project knowledge stays compiled and shared, while tooling knowledge stays local and interchangeable.

## What belongs in local tooling

The source policy allows local tooling content in only two cases:

- a required harness build record for each agent-ready pass
- fuller adapter/profile context, but only when a detected or user-selected harness actually needs it

The build record should capture the harness name and version, how it was identified, the pass date, and any quirks that matter for running the pipeline. If the harness cannot be identified reliably, the record is skipped rather than guessed.

## What must stay out

The policy explicitly rejects speculative tooling accumulation. It also forbids treating tooling pages as project source material, and warns against creating extra ad hoc folders for it.

Important exclusions include:

- no broad tooling knowledge dump beyond the two permitted cases
- no project-side dependence on local tooling pages
- no ingestion of tooling pages through normal repository import flows
- no extra non-standard tooling folders under `.agents/`

These rules support [[concepts/tooling-boundaries]], [[concepts/local-by-default-tooling]], and [[concepts/consent-first-tooling]].

## Storage and navigation model

Local tooling lives under `okf/wiki/tooling/`, with a committed `index.md` stub and local pages underneath it. The stub exists so every clone has a stable navigation target, while the detailed pages remain local by default.

The policy requires:

- a committed `tooling/index.md` navigation stub
- a bundle-root index entry for tooling when local tooling pages exist
- no enumeration of local tooling pages in committed indexes
- no project page links back into tooling pages

This is closely related to [[concepts/tooling-navigation-exception]], [[concepts/tooling-stub-resolving]], [[concepts/link-directionality]], and [[concepts/wikilink-integrity]].

## Link discipline

Local tooling pages must still link outward to durable project knowledge so they are not treated as orphans. At the same time, project pages must not link inward to local tooling pages.

That creates a one-way boundary:

- tooling pages may point to project pages
- project pages may not depend on tooling pages

This is part of [[concepts/tooling-link-policy]] and [[concepts/context-action-separation]].

## Validation and governance

The document also defines a validator that checks whether the tooling boundary is being respected. It fails when:

- project concept pages link into tooling
- required tooling references are missing from the root index
- the committed tooling stub is absent
- a local tooling page has no outgoing wikilink

This makes the boundary enforceable, not just advisory, and ties it to [[concepts/deterministic-validation]] and [[concepts/okf-validation-rules]].

## Why it matters

Local tooling boundaries keep the knowledge base coherent across users, clones, and harnesses. They preserve reproducibility for runtime context while preventing contamination of project knowledge with environment-specific details.

In practice, the boundary supports [[concepts/compiled-knowledge-bases]], [[concepts/progressive-disclosure]], and [[concepts/knowledge-layer-separation]].

## Related source

- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]