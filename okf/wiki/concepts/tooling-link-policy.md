---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md"]
description: "Defines one-way links between tooling pages and project wiki content."
---

# Tooling Link Policy

Tooling link policy defines the allowed direction of links between the local tooling area and the rest of the OpenKB wiki. It keeps harness-specific context isolated while preserving a narrow navigation path from the bundle root.

This policy matters in a repository like agent-smith, where the wiki is part of a larger agent-ready architecture that separates orientation, durable context, and actions. In that model, tooling pages belong to the runtime-adapter layer, while project concept pages should stay focused on repository knowledge and not depend on harness details.

It also fits the embedded OKF baseline: the bundle can be validated offline, reserved navigation files have special rules, and the wiki should remain machine-checkable without turning tooling into project truth. In that framing, the root index can enumerate tooling for discoverability, but ordinary project pages still must not depend on tooling pages.

The broader [[concepts/agent-ready-context]] workflow reinforces the same separation:

- skills are for actions, checks, orchestration, and repeatable workflows
- the OKF wiki is for durable context, provenance, architecture, and external evidence
- `AGENTS.md` is for concise orientation, setup, routing, and where-to-look-next guidance

That three-layer split keeps tooling context from leaking into long-lived repository knowledge and keeps knowledge updates flowing through the wiki rather than through ad hoc action docs.

The [[concepts/subagent-role-design]] workflow extends this boundary into runtime-specific generation: it treats harness adapters as projections of existing repository context, not as a source of truth. In that workflow, harness detection must be based on the active runtime, adapter files must stay short, and the wiki should be used for durable evidence while profiles or subagents remain harness-specific outputs.

This lines up with [[concepts/runtime-ambiguity-resolution]] and [[concepts/runtime-signal-prioritization]]: do not infer the harness from installed binaries alone. Prefer explicit environment or conversation signals, treat repo files as low-confidence hints, and ask the user when the runtime remains unclear. That keeps adapter generation grounded in the active execution context instead of in assumptions.

## Core Rule

Pages under `okf/wiki/tooling/` may link outward to project pages, but project wiki content must not link back into `okf/wiki/tooling/`. This preserves local-by-default tooling, tooling-context isolation, and tooling-context governance by preventing harness details from becoming a dependency of normal documentation.

The policy also matches the broader boundary in the subagent profile adapter workflow: tooling documentation may inform runtime-specific adapter work, but project concept pages should not treat tooling pages as source-of-truth context. That separation reflects the repository pattern of keeping `AGENTS.md` for orientation, `okf/wiki/` for durable context, and `.agents/skills/` for actions.

The validation script for this policy, `.agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py`, makes the rule concrete. It scans markdown files under the wiki root, strips fenced code blocks and inline code before searching, detects both standard markdown links and bare path references, and rejects project pages that reference tooling paths.

The script also treats tooling pages differently from project concepts. It warns when local tooling pages do not declare `scope: tooling` or `type: tooling-context`, and it expects any non-reserved tooling page to include at least one outgoing wikilink so structural linting does not treat it as orphaned. That keeps tooling pages visible to the graph while still keeping them local.

## Reserved Exceptions

The policy makes a narrow exception for the bundle-root `index.md` and `log.md` files. These are navigation and history files, so they are exempt from the forbidden direction. In practice, the root index may reference tooling when needed to keep the wiki discoverable and auditable.

This exception aligns with the OKF baseline's emphasis on explicit navigation: the bundle-root `index.md` may declare the target OKF version and must remain a stable entry point, even when most tooling context stays local and harness-specific. The reserved-file rule also means that tooling references in the root index are about bundle navigation, not about project pages depending on tooling.

The validator encodes the same exception. It checks the root `index.md` separately, remembers whether it links to tooling, and only reports an error if tooling pages exist but the root index does not reference them. `log.md` is treated as reserved history and excluded from the forbidden-link scan.

The root index may also serve as the front door for progressive disclosure. If the wiki is used to orient an agent, it should route first through `index.md`, then through the relevant compiled areas, rather than exposing tooling internals directly inside project pages.

## Required Navigation Stub

When `okf/wiki/tooling/` contains any non-reserved pages, two things must be true:

- the bundle-root `index.md` must include a clearly labeled harness-specific section that links to `tooling/`
- `okf/wiki/tooling/index.md` must exist as the committed navigation stub

This stub matters because tooling is local by default and often gitignored except for the navigation placeholder, so the root link needs a stable target on fresh clones. It also supports the agent-ready bootstrap pattern, where a repository should expose a small, durable surface for orientation without inlining harness-specific material everywhere.

The validation script enforces that requirement directly. If tooling pages exist and the root index lacks a tooling reference, it errors. If the committed `tooling/index.md` stub is missing, it errors as well. That makes the navigation contract part of the repository's checked structure rather than a convention that can drift.

The same pattern fits the broader concept of tooling-context pages: local harness notes may exist, but only the committed stub is part of the shared navigation contract.

## Validation Behavior

The validator in `.agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py` enforces the policy by walking the wiki tree and classifying pages by location.

It:

- detects tooling links in project pages and reports them as errors
- skips reserved files like `index.md` and `log.md`
- strips fenced code blocks and inline code before scanning to reduce false positives
- checks tooling pages for expected metadata such as `scope: tooling` or `type: tooling-context`
- verifies that the root index references tooling and that the tooling navigation stub exists when tooling pages are present
- avoids flagging entity pages as forbidden project-to-tooling links when they are describing local tooling structure
- tolerates missing OKF directories by printing a warning and exiting cleanly

This fits the broader commitment to deterministic validation, explicit routing, and progressive disclosure: the wiki should be machine-checkable, but the tooling boundary should also be easy for humans to reason about. It also aligns with the offline OKF baseline's guidance that validators should tolerate incomplete bundles while still reporting real policy violations.

The policy is part of a larger validation stack that favors preflight checks, bundle validation, and path-aware safeguards over ad hoc review. In practice, that means link direction is not just a style preference; it is a validation rule that protects the boundary between shared knowledge and local runtime context.

## Related Ideas

This concept overlaps with [[concepts/link-directionality]], [[concepts/okf-bundle-validation]], [[concepts/reserved-navigation-files]], [[concepts/path-based-validation]], [[concepts/adaptive-harness-detection]], [[concepts/runtime-ambiguity-resolution]], [[concepts/runtime-signal-prioritization]], [[concepts/permission-scoped-agents]], and [[concepts/subagent-role-design]] because the adapter workflow depends on identifying the active harness before writing harness-specific files.

It also supports the repository pattern described in the agent-ready-context skill: keep durable knowledge in the wiki, keep actions in skills, and keep harness-specific projections out of the project's conceptual core.

## Why It Matters

Tooling link policy reduces accidental coupling, supports generated content governance, and keeps the wiki structure predictable for both humans and agents. It is a small rule with outsized impact on repository hygiene, discoverability, and long-term maintainability, especially when runtime-specific adapters are generated from repository knowledge without turning tooling pages into project truth.

It also prevents a subtle failure mode in agent-ready repositories: once tooling pages become linked from normal project content, local harness assumptions can start to masquerade as durable repository knowledge. Keeping the direction one-way avoids that confusion and preserves the intended separation between [[concepts/agent-ready-context]] and local execution context.

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[summaries/README-md]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]