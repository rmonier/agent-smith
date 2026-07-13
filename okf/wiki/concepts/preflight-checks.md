---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md"]
description: "Checks that verify a repo is ready before agent workflows run."
---

# Preflight Checks

Preflight checks are early validation steps that confirm a repository, runtime, and local setup are ready before an agent workflow continues. They act as a fast gate that separates hard failures from optional capabilities, reducing ambiguous runtime errors later in the process.

## What they cover

Preflight checks typically confirm:

- Required runtime support, such as Python version constraints and command availability
- Repository state, such as whether the current path is inside a Git worktree
- Optional tooling, where missing tools are reported but do not always block progress
- Configuration readiness, especially shared settings versus user-specific overrides
- Filesystem writability for paths the workflow needs to create or update

## In the checked script

The script in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] implements a structured preflight pass for the `agent-ready-context` skill. It performs these checks:

- Confirms Python 3.11+ at runtime
- Verifies `git` and `uv` are installed
- Confirms the repo is inside a Git worktree
- Probes optional CLIs like `graphify` and `openkb`
- Checks that vendored tool skills exist when those CLIs are installed
- Validates OpenKB config presence and compares shared config keys against the committed example
- Detects whether `.env` files exist in the project or user-global OpenKB location
- Tests writability of key paths such as `okf/.okf-build/input`, `okf`, and `.agents/skills`

## Design goals

This kind of check is built around a few recurring goals:

- [[concepts/graceful-degradation]]: optional tools can be missing without stopping the whole workflow
- [[concepts/configuration-precedence]]: project-local config and user-global config are distinguished clearly
- [[concepts/local-vs-shared-configuration]]: shared settings are kept aligned while provider-specific values stay user-controlled
- [[concepts/path-based-validation]]: filesystem paths are tested directly instead of assumed
- [[concepts/executable-validation]]: installed commands are executed or probed to confirm real availability
- [[concepts/consent-first-tooling]]: optional tools are reported as installable, not silently added

## Key behaviors

- Hard requirements and optional dependencies are reported separately.
- The script uses simple YAML scalar parsing to compare only the small set of shared config keys.
- It avoids reading secrets from `.env` files and checks only for their presence.
- It explicitly warns when both project and user-global credential homes exist, because that can create confusion over which one is authoritative.
- It treats vendored tool skills as part of the toolchain contract, not as an optional convenience.

## Why it matters

Preflight checks improve [[concepts/quality-gates]] by catching setup drift before the main workflow starts. In an agent-driven repository, they also support [[concepts/agent-ready-context]] by ensuring the environment is stable enough for deterministic execution, repeatable compilation, and predictable tool routing.

They are especially useful for workflows that depend on [[concepts/toolchain-pinning]], [[concepts/vendor-skill-adoption]], and [[concepts/filesystem-validation]], because those workflows need both software availability and repository write access to succeed reliably.

## Related ideas

- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/quality-gates]]
- [[concepts/graceful-degradation]]
- [[concepts/configuration-precedence]]
- [[concepts/toolchain-pinning]]
- [[concepts/vendor-skill-adoption]]
- [[concepts/filesystem-validation]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]