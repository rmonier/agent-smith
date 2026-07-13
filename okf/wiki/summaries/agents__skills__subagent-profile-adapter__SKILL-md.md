---
type: "Summary"
description: "Guidance for generating harness-specific subagent/profile adapters from repo context."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__SKILL-md.md"
---

# Subagent Profile Adapter

This document describes a skill for creating and maintaining harness-specific subagent or profile adapters from the repository's existing agent-ready context. It is explicitly runtime-specific: the goal is to project current repo knowledge into the native adapter format of the active harness, not to define a portable subagent standard.

## Main Purpose

The skill is meant to help an agent understand the active harness and write the adapter files that harness expects. It assumes the repo already has durable context in okf wiki, orientation in `AGENTS.md`, and reusable procedures in Agent Skills under `.agents/skills/`.

## Boundary Rules

The document draws a strict separation between layers:

- okf wiki is the source of truth for durable project knowledge, evidence, and provenance.
- `AGENTS.md` is the repository orientation and best-practices file.
- Agent Skills are reusable procedures and scripts.
- Subagent/profile adapters are runtime projections for the current harness only.

It also states that no new `.agents/` directories should be created except `.agents/skills/`.

## Workflow

The skill recommends a staged process:

1. Confirm `AGENTS.md` and `okf/wiki/` exist or have been refreshed.
2. Make sure repeated actions have been turned into skills when appropriate.
3. Detect the active runtime using explicit environment or conversation clues, not installed binaries alone.
4. Verify whether the harness supports local subagents or profiles using docs or official web references.
5. Decide how the harness should track generated files: local-only, ignored globally, or committed.
6. Write short native adapter files that point back to `AGENTS.md`, `okf/wiki/`, and relevant skills.
7. Validate that the generated files follow the link and storage policy.

## Runtime Detection and Validation

A major emphasis is on avoiding false assumptions about the harness. The skill says not to infer the runtime from `--version` output or from installed tools alone. If the runtime remains ambiguous, the user should be asked directly.

Validation includes a policy check for tooling links and ensuring that project concept pages do not depend on tooling pages. It also requires the bundle-root index to enumerate `okf/wiki/tooling/` in a clearly labeled harness-specific section when tooling pages exist.

## Tooling Context Policy

The document treats harness documentation as special tooling context that belongs in `okf/wiki/tooling/`, not in extra `.agents/` folders. It also says that the OpenKB wiki conventions file should declare the tooling section, and that tooling pages are hand-authored exceptions rather than ingested source material.

A key rule is directionality:

- tooling context may point to project context
- project concept pages must not point back to tooling context

That rule protects project knowledge from becoming entangled with harness-specific implementation details.

## Good Adapter Candidates

The document suggests that adapter candidates should be task-scoped and permission-bounded, such as:

- `okf-curator`
- `skill-architect`
- `repo-cartographer`
- `security-reviewer`
- `dependency-scout`

These should be derived from real repository needs and the current OKF pages, not invented as generic roles.

## Notable Ideas

- The active harness is treated as an environment to inspect, not an assumption to hardcode.
- Adapter files should be minimal and should delegate heavy context to existing repo documentation.
- Tooling pages are allowed, but only as clearly bounded harness-specific context.
- Navigation needs to remain coherent, so the root wiki index must include tooling when present.

## Overall Takeaway

This skill is a policy-driven bridge between stable repository knowledge and runtime-specific agent adapters. It exists to keep harness details local, short, and auditable while preserving `AGENTS.md`, skills, and the wiki as the main project knowledge system.

## Related Concepts
- [[concepts/harness-native-profiles]]
- [[concepts/runtime-adapter-management]]
- [[concepts/tooling-context-governance]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/agent-ready-context]]
- [[concepts/knowledge-boundaries]]
- [[concepts/tooling-boundaries]]
- [[concepts/local-by-default-tooling]]
- [[concepts/instruction-file-aliasing]]
- [[concepts/link-directionality]]
- [[concepts/managed-document-sections]]
- [[concepts/non-interactive-agent-design]]
- [[concepts/permission-scoped-agents]]
- [[concepts/portable-skill-contract]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-signal-prioritization]]
- [[concepts/tool-boundaries]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-link-policy]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/tooling-stub-resolving]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/agent-orientation-index]]
- [[concepts/agents-md-maintenance]]
- [[concepts/context-action-separation]]
- [[concepts/knowledge-layer-separation]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/self-reference-control]]
- [[concepts/wiki-context-routing]]
- [[concepts/wiki-skill-boundaries]]

## Entities
- [[entities/subagent-profile-adapter]]
- [[entities/okf-wiki-tooling-index-md]]
- [[entities/references-tooling-context-policy-md]]
- [[entities/scripts-inspect_runtime_context-py]]
- [[entities/validate_tooling_link_policy-py]]
- [[entities/scripts-ensure_local_alias-py]]
- [[entities/agent-smith]]
- [[entities/romain-monier]]
- [[entities/okf-wiki]]
- [[entities/okf]]
- [[entities/agents-md]]
- [[entities/okf-wiki-agents-md]]
- [[entities/agent-ready-context]]
- [[entities/agent-ready-context-skill]]
- [[entities/agents-md]]
- [[entities/agents-skills]]
- [[entities/agentskills-io]]
- [[entities/openkb]]
- [[entities/openkb-cli]]
- [[entities/openkb-wiki]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-tooling]]
- [[entities/tooling]]
- [[entities/git-info-exclude]]
- [[entities/gitignore]]
- [[entities/uv]]
- [[entities/agent-ready-repositories]]
- [[entities/runtime-detection-md]]
