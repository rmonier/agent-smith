---
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
type: "Work"
description: "Policy document governing tooling context handling"
---

# References Tooling Context Policy

`References Tooling Context Policy` is a repository policy document used by the [[entities/subagent-profile-adapter]] skill to govern how tooling context is recorded, linked, and isolated from project knowledge.

## What it covers

- Defines what belongs in `okf/wiki/tooling/` versus the main compiled knowledge base.
- Sets the link direction rule that tooling context may reference project context, but project concept pages must not link back to tooling pages.
- Establishes how harness-specific evidence should be persisted when the subagent/profile adapter skill runs.
- Supports the broader separation between runtime-specific adapters and durable project knowledge.

## Role in the skill workflow

The subagent-profile-adapter skill explicitly requires reading this policy before writing tooling pages. It uses the policy to decide:

- whether a harness-specific page should be retained or left transient,
- how to treat local-only versus shared tooling artifacts,
- where to place navigation entries in `okf/wiki/index.md`, and
- how to validate that tooling links do not leak into project concept pages.

## Why it matters

This policy helps preserve [[concepts/tooling-context-isolation]] and [[concepts/tooling-link-policy]] while still allowing harness-specific documentation to exist as a controlled exception. It also reinforces [[concepts/knowledge-layer-separation]] and [[concepts/link-directionality]] in the compiled wiki.

## Related material

- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[entities/subagent-profile-adapter]]
- [[entities/okf-wiki-tooling]]
- [[entities/okf-wiki-index-md]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/scripts-ensure_local_alias-py]]