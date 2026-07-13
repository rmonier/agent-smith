---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md"]
description: "Installation that requires explicit approval before changing the system."
---

# Consent-First Installation

Consent-first installation is the practice of requiring explicit user approval before installing tools, dependencies, or other system-changing components. It treats installation as a deliberate action rather than an automatic side effect of using a skill or workflow.

## What It Means

In the skill-creator dependency guidance, installation is not something a skill may assume or perform silently. Instead, the skill should:

- ask the user before installing anything
- prefer user-scoped installers such as `uv tool install`
- avoid privileged installation paths like `sudo`
- explain what will be installed, why it is needed, and what happens if the tool is absent

This keeps dependency handling aligned with permission-scoped agents, minimal tool scoping, and provenance-aware tool installation.

The prerequisite checker for `agent-ready-context` extends this same pattern from dependency management into repository readiness checks: it detects whether `uv`, `git`, optional CLIs like `graphify` and `openkb`, and writable paths are available, but it only turns missing optional tooling into guidance rather than automatic installation. When a tool is absent, the script reports the gap, explains the degraded path, and leaves installation to an informed user.

## Why It Matters

Consent-first installation reduces surprise, avoids unnecessary system changes, and makes agent behavior safer in shared or managed environments. It also supports supply chain security by keeping installs explicit and reviewable.

For portable skills, this approach helps preserve the portable skill contract: the skill definition stays focused on metadata and guidance, while installation remains the responsibility of the skill manager or an informed user.

The `check_prereqs.py` script shows why this matters operationally. It distinguishes hard failures such as missing `git`, `uv`, or write access from optional capabilities like `graphify` and `openkb`, and it records notes that explain what to install, which tool path is preferred, and how the repo behaves when the tool is missing. That keeps setup transparent without forcing changes.

## Source Guidance

The related summary page for `.agents/skills/skill-creator/references/dependencies.md` says that:

- dependency resolution and installation state belong outside `SKILL.md`
- detailed requirements should live in `references/dependencies.md`
- third-party tooling must be documented with exact package and registry information
- installation must be consent-first and user-scoped
- the skill should describe degraded behavior when the tool is missing

That guidance makes consent-first installation a core rule of skill dependency declaration and consent-first tooling.

`check_prereqs.py` reinforces the same boundary by treating installation as a follow-up action, not an implicit step in validation. It can confirm whether a CLI is present, but it does not install anything itself. Instead, it surfaces whether the repo is ready, whether a skill has been vendored, and whether the current environment has enough tooling for the next step.

## Practical Pattern

A skill using this model usually follows a sequence like:

1. detect whether the needed tool is available
2. explain the missing requirement
3. ask the user whether they want it installed
4. install only after approval
5. document the fallback path if installation is declined

This pattern works best with a prerequisite checker such as `scripts/check_prereqs.py` and with concise metadata that records only portable hints.

The checker also shows a useful refinement of the pattern: separate hard prerequisites from optional enhancements. For example, `git` and `uv` are required for the workflow, while `graphify` and `openkb` are optional and can be introduced later with consent. That division makes installation decisions more legible and keeps the skill usable in degraded mode.

## Related Ideas

- [[concepts/dependency-management]]
- [[concepts/toolchain-pinning]]
- [[concepts/integrity-pinning]]
- [[concepts/graceful-degradation]]
- [[concepts/skill-governance]]
- [[summaries/agents__skills__skill-creator__references__dependencies-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]


See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]