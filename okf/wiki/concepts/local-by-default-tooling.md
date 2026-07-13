---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md"]
description: "Tooling stays local while the shared wiki keeps a minimal navigation stub."
---

# Local-By-Default Tooling

Local-by-default tooling is a wiki governance pattern where harness-specific context lives in a user-scoped, ignored, or otherwise local area, while the shared repository keeps only a minimal committed stub and navigation entry. The goal is to keep runtime-specific or sensitive tooling private and flexible without breaking discoverability, validation, or wiki navigation.

## Core idea

Under this model, tooling pages are not treated like ordinary shared documentation. They can exist locally, be excluded from normal repository tracking, and still participate in the wiki through a stable public entry point. That is why the committed `tooling/index.md` stub matters: it gives the root index something durable to point at, even when a clone has no local tooling pages.

This concept connects to [[concepts/tooling-context-isolation]], [[concepts/local-tooling-boundaries]], and [[concepts/local-only-repo-artifacts]]. It also depends on [[concepts/knowledge-boundaries]] and [[concepts/reserved-navigation-files]] so that local tooling does not leak into the shared knowledge graph in unintended ways.

The subagent profile adapter skill makes this pattern concrete by requiring harness-specific adapter files to stay short, local, and runtime-specific. It treats `AGENTS.md` as the orientation file, `okf/wiki/` as durable knowledge, and `.agents/skills/` as reusable actions, while adapter outputs remain projections for the active harness rather than a source of truth.

## What the policy enforces

The source script [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]] encodes the policy in executable form:

- pages under `okf/wiki/tooling/` may link outward to project pages;
- project concept pages and most indexes must not link back into tooling;
- the bundle-root `index.md` and `log.md` are exempt because they serve navigation and history roles;
- if tooling contains non-reserved pages, the root `index.md` must reference `tooling/` in a clearly labeled harness-specific section;
- if tooling contains non-reserved pages, a committed `tooling/index.md` stub must exist so the root link resolves cleanly on clones without local tooling pages.

The subagent profile adapter adds two further constraints that reinforce the same boundary: do not create extra `.agents/` directories outside `.agents/skills/`, and do not commit harness-specific outputs unless the user or repository policy explicitly allows it. When an alias is needed for a harness that does not support `AGENTS.md`, the skill prefers a symlink or local alias rather than duplicating content.

That combination keeps local tooling discoverable without letting it become an accidental dependency of the shared wiki graph.

## Why it matters

Local-by-default tooling supports a few broader goals:

- [[concepts/consent-first-tooling]]: users can keep tooling under local control instead of publishing it by default;
- [[concepts/privacy-preserving-tooling]]: sensitive or environment-specific tooling details do not need to be shared broadly;
- [[concepts/tooling-context-governance]]: the boundary between tooling and project knowledge is explicit and enforceable;
- [[concepts/link-directionality]]: knowledge links follow a controlled direction instead of forming cycles;
- [[concepts/wikilink-integrity]]: the wiki remains navigable without broken or misleading references.

It also fits the adapter skill's emphasis on runtime ambiguity resolution: harness detection should come from explicit environment or documentation signals, not from installed binaries alone. That keeps tooling behavior grounded in the actual active harness instead of a guessed environment.

## Structural implications

This pattern treats the root wiki index as a navigation contract, not just a page list. If local tooling exists, the shared repository must still advertise it, but only through a minimal stub and a labeled section. That makes the repository easier to clone, lint, and reason about in mixed local/shared setups.

It also means that tooling pages should be authored with awareness of their limited scope: they can describe local harness behavior, but they should not become hidden sources of truth for project concepts. In practice, this supports [[concepts/documentation-layer-separation]] and [[concepts/local-vs-shared-configuration]].

The adapter skill extends this idea into file layout and workflow: harness-specific profiles belong to the active runtime only, companion skills handle repeated actions, and generated adapters should remain short enough to point back to the repo's durable sources instead of embedding them.

## Related behavior

The validation script also warns when local tooling pages do not declare tooling scope or tooling-context type. That is not a hard failure, but it encourages clearer metadata and better graph hygiene. In the broader wiki, this aligns with [[concepts/lightweight-frontmatter-validation]] and [[concepts/generated-content-governance]].

The same validation mindset shows up in the adapter skill's required checks: verify file placement, ensure no profile embeds large project content, and confirm that project pages do not link back into tooling. These checks keep local projections and durable knowledge separate while still allowing the wiki to remain navigable.

## Summary

Local-by-default tooling is a compromise between privacy, portability, and navigability: tooling can stay local, but the shared wiki still exposes a controlled entry point so users and validators can find it reliably.

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
