---
type: "Summary"
description: "Preflight checker for agent-ready-context repo prerequisites and config drift."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__check_prereqs-py.md"
---

# `.agents/skills/agent-ready-context/scripts/check_prereqs.py`

This script performs preflight checks for the `agent-ready-context` skill before the workflow proceeds. It is designed to run without third-party dependencies so it can work in a fresh repository, with `uv` preferred and bare `python3` as a degraded fallback.

## What it checks

- Required runtime and tools: [[concepts/preflight-checks|Python 3.11+]], `git`, and `uv`.
- Git repository state: confirms the path is inside a worktree.
- Optional CLI tools: `graphify` and `openkb`, with generous timeouts because first startup may be slow.
- Vendored tool skills: verifies that CLI tools expected in the repo have matching `.agents/skills/<tool>/SKILL.md` copies when the CLI is installed.
- OpenKB configuration: checks for `okf/.openkb/config.yaml`, compares shared keys against the example file, and warns about drift in project-shared settings.
- Credential homes: detects whether `.env` exists in the project or in `~/.config/openkb/.env`, and explains which one will be used.
- Writable paths: probes `okf/.okf-build/input`, `okf`, and `.agents/skills` for basic write access.

## Core ideas

- The script separates hard requirements from optional capabilities, so missing tools do not all fail the same way.
- Shared config keys are treated as contributor-wide contract values, while provider-specific settings are left to each user.
- It avoids parsing secrets directly; `.env` files are checked by presence only.
- It prefers the project-local credential file when both project and user-global homes exist, which can create ambiguity that is explicitly reported.
- Toolchain skills are treated as vendored dependencies: if a CLI is installed, its pinned skill copy should also be present in the repo.

## Output structure

- `required`: hard checks such as Python, `git`, `uv`, and worktree status.
- `optional`: installed state for `graphify` and `openkb`.
- `vendored_tool_skills`: whether corresponding tool skills are present in the repo.
- `openkb_config`: config and credential-home checks.
- `companion_skills`: presence of supporting skills like `skill-creator` and `subagent-profile-adapter`.
- `writable_paths`: filesystem write probes.
- `notes`: human-readable guidance for missing or conflicting prerequisites.

## Notable behavior

- Uses `shutil.which` plus a resolved executable path so Windows command shims work reliably.
- Reads YAML only as simple top-level scalars, which is enough to detect drift in a small set of shared keys.
- Reports a failure if any hard requirement or writable-path probe fails.
- Produces either a concise text report or a full JSON diagnostic payload.

## Why it matters

This script acts as a repository health gate for agent-driven work. It reduces setup ambiguity, catches config drift early, and makes it clear when the repo is ready for the `agent-ready-context` workflow versus when the user needs to install tools or align configuration.

## Related Concepts
- [[concepts/preflight-checks]]
- [[concepts/filesystem-validation]]
- [[concepts/configuration-precedence]]
- [[concepts/consent-first-installation]]
- [[concepts/dependency-management]]
- [[concepts/graceful-degradation]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/toolchain-pinning]]
- [[concepts/vendor-skills]]
- [[concepts/skill-vendoring]]
- [[concepts/cross-platform-tooling]]
- [[concepts/path-based-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/openkb-build-workflow]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/vendor-backed-validation]]

## Entities
- [[entities/check_prereqs-py]]
- [[entities/uv]]
- [[entities/git]]
- [[entities/openkb]]
- [[entities/graphify]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/agent-ready-context-skill]]
- [[entities/agent-ready-context]]
- [[entities/agents-skills]]
- [[entities/openkb-cli]]
- [[entities/graphifyy]]
- [[entities/python]]
- [[entities/git]]
- [[entities/uv]]
- [[entities/okf-openkb-config-yaml-example]]
- [[entities/okf-openkb-config-yaml]]
- [[entities/skill-creator]]
- [[entities/subagent-profile-adapter]]
- [[entities/agents-skills]]
- [[entities/okf]]
- [[entities/openkb-wiki]]
- [[entities/openkb-cli]]
- [[entities/graphify]]
- [[entities/uv]]
- [[entities/git]]
- [[entities/python]]
- [[entities/agent-ready-context]]
- [[entities/agent-ready-context-skill]]
