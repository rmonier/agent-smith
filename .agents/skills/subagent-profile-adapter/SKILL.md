---
name: subagent-profile-adapter
description: Creates and maintains harness-specific subagent/profile adapters after agent-ready context and custom action skills exist. Use when the active harness supports local subagents, personas, agent profiles, or task-scoped execution contexts and the user wants those runtime adapters generated without making them a source of truth.
license: See LICENSING.md
compatibility: Requires an Agent Skills compatible harness, repository file read/write access, and Python 3.11+ for optional validation helpers (run them with uv when available). Requires web access or local harness documentation when current subagent/profile semantics are unknown.
metadata:
  version: "0.1.0"
  spec: agentskills.io
  author: Romain Monier
  author-url: https://github.com/rmonier
  source: https://github.com/rmonier/agent-smith
  subagent-profile-adapter.companion-skills: agent-ready-context, skill-creator
  subagent-profile-adapter.companion-skill-roles: agent-ready-context=preferred upstream context workflow; skill-creator=preferred upstream action-skill workflow
  subagent-profile-adapter.provides: runtime-context-inspection, tooling-context-policy, harness-adapter-generation
  subagent-profile-adapter.runtime-detection: references/runtime-detection.md
  subagent-profile-adapter.tooling-context-policy: references/tooling-context-policy.md
allowed-tools: Read Write Edit Bash(uv:*) Bash(python:*) Bash(git:*) Bash(readlink:*) Bash(test:*) Bash(mkdir:*) WebFetch WebSearch
---

# Subagent Profile Adapter

Use this skill to create or maintain **harness-specific subagent/profile adapters** from the repository's existing agent-ready context.

This skill does **not** define a new portable subagent standard. It helps the current agent understand the active harness and write the native files expected by that harness, using current local or official documentation.

## Boundary rules

- **OKF wiki (OpenKB-compiled) = context source of truth**: durable project knowledge, external evidence, tooling context, and provenance.
- **AGENTS.md = orientation/index/best practices**: short repo guide for agents.
- **Agent Skills = actions**: reusable procedures and scripts under `.agents/skills/`.
- **Subagent/profile adapters = runtime-specific projections**: generated or maintained for the active harness only.

Do not create new directories under `.agents/` except Agent Skills under `.agents/skills/`. `okf/wiki/tooling/` holds two things only: the minimal harness build record that every agent-ready pass writes (or explicitly declines — see `references/tooling-context-policy.md`), and fuller harness evidence persisted when this skill is explicitly run for a harness. Use the link policy in `references/tooling-context-policy.md`.

## Core workflow

Run this skill only after:

1. `AGENTS.md` exists or has been refreshed by `agent-ready-context`.
2. `okf/wiki/` exists or has been refreshed.
3. Custom action skills have been created or reviewed by `skill-creator` when repeated actions were found.

Then:

1. **Detect the active runtime, not merely installed tools.**
   - Prefer explicit harness metadata exposed by the current environment or conversation.
   - Inspect parent process and environment hints if available.
   - Inspect repo files only as low-confidence hints.
   - Do **not** use `<tool> --version` or the presence of an installed binary as proof of the active harness.
   - If runtime remains ambiguous, ask the user which harness to target.

2. **Check whether the active harness supports local subagents/profiles.**
   - Use local docs/help if already available in the repo or harness.
   - Otherwise use official web documentation.
   - If persistence is useful, record the evidence and summary under `okf/wiki/tooling/harnesses/<harness>.md`; otherwise keep it as transient reasoning/output. Baseline OKF bootstrap writes only the minimal harness build record defined in `references/tooling-context-policy.md` (or justifies its absence in the run report); fuller tooling pages stay adapter work.

3. **Handle agent instruction compatibility.**
   - `AGENTS.md` remains the canonical orientation file.
   - If the harness does not support `AGENTS.md` but requires another file, create a local alias only after confirming the correct target from docs or the user.
   - Prefer a symlink to `AGENTS.md` and add the alias path to `.git/info/exclude` unless the user explicitly wants a tracked adapter.
   - Use `scripts/ensure_local_alias.py` for a generic local symlink/exclude helper.

4. **Design candidate subagent/profile adapters.**
   - Derive them from actual repository needs, OKF pages, and available skills.
   - Good candidates are task-scoped and permission-bounded, for example `okf-curator`, `skill-architect`, `repo-cartographer`, `security-reviewer`, or `dependency-scout`.
   - Do not embed long project context inside profile files. Point to `AGENTS.md`, `okf/wiki/`, and relevant skills.

5. **Ask the user how to track generated harness-specific files.**
   - Local-only via `.git/info/exclude`.
   - Ignored for all via `.gitignore`.
   - Committed as shared team adapters.
   - Default to local-only if the user has not chosen a team policy.

6. **Write native adapter files by reasoning from current docs.**
   - Do not rely on hardcoded vendor renderers.
   - Do not assume fields are stable between harness versions.
   - Read the current docs and implement the native format directly.
   - Keep adapter files short: purpose, activation/description, permissions/tools if supported, and instructions to consult `AGENTS.md`, `okf/wiki/`, and skills.

7. **Validate outputs.**
   - Verify the files are in the correct harness location.
   - Verify no profile embeds large OKF/project content.
   - Verify project OKF concept pages do not link back to `okf/wiki/tooling/`.
   - Verify the bundle-root `okf/wiki/index.md` lists `okf/wiki/tooling/` in a clearly labeled harness-specific section when tooling pages exist, and that the committed `tooling/index.md` navigation stub exists (tooling pages are local by default; the stub keeps navigation coherent on every clone).
   - Run:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .
```

## Tooling context in OKF

Harness documentation belongs in `okf/wiki/tooling/`, not in extra `.agents/` folders.

Because the wiki is OpenKB-compiled, declare the custom `tooling/` section in `okf/wiki/AGENTS.md`, OpenKB's on-disk wiki-conventions manual. Edit that file only with user consent, and preserve the declaration after OpenKB regenerates conventions. Tooling pages are hand-authored exceptions to the no-hand-edit rule and are never ingested through `openkb add`; ingestion would let the compiler scatter harness details across project pages.

The link direction stays strict for concept pages:

```text
tooling context -> project context is allowed
project concept pages -> tooling context is forbidden
```

This means `okf/wiki/tooling/harnesses/<harness>.md` may mention `AGENTS.md`, `.agents/skills/`, or project OKF pages. Normal project concept pages must not depend on or link back to tooling pages.

The bundle-root `okf/wiki/index.md` is the deliberate exception: OKF navigation must enumerate the bundle, so when `okf/wiki/tooling/` contains pages, the root index **must** reference it — in its own clearly labeled section marking it as harness-specific context that project pages never depend on. Root `okf/wiki/log.md` may likewise record tooling changes. Without that index entry the bundle stops being spec-navigable; with more than that (deep links from concept pages), agents start treating interchangeable harness details as project truth. Keep exactly the index entry, nothing more.

Read `references/tooling-context-policy.md` before writing tooling pages.

## Runtime detection rule

Never conclude “the active harness is X” only because `x` is installed. A user can have multiple agents installed while running another harness.

Use `scripts/inspect_runtime_context.py` only to collect hints; it does not replace user confirmation when signals are ambiguous.

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/inspect_runtime_context.py --repo .
```

## Non-goals

Do not:

- create a portable subagent standard;
- create `.agents/profiles/` or other non-standard `.agents/` folders;
- hardcode vendor profile renderers;
- copy `okf/wiki/` content into profiles;
- make harness docs a project source of truth;
- patch vendor skills;
- commit harness-specific outputs without an explicit user or repo policy.
