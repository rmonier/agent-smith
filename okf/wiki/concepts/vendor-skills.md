---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Vendored skill copies that make tool adoption repo-scoped and resilient."
---

# Vendor Skills

Vendor skills are packaged copies of external agent skills that live inside a repository so local tooling can rely on them without reaching back to the upstream source during normal use.

## What They Are

A vendor skill is the repository-scoped copy of a skill that provides the usage guidance for a CLI or workflow component. In this model, the copied skill is treated as durable documentation and operational context, not as editable project code.

Vendor skills also act as a readiness boundary: the installed CLI and the vendored skill are checked separately, so a tool is not considered fully adopted until its pinned skill copy exists in the repository.

## Why They Matter

The source document makes vendor skills a core part of safe tool adoption:

- The repository should not depend on a live upstream skill being present at runtime.
- The vendored copy is the durable carrier of the CLI's usage knowledge inside the repo.
- A later maintainer can keep working even if the original skill package or harness integration is unavailable.
- Installed CLIs and their vendored skills are checked separately, so a tool is not considered fully ready until its skill has been copied into the repository.
- Prereq checks can degrade gracefully when a CLI is absent, but report a warning when the CLI is installed and its vendor skill is still missing.

This connects vendor skills to [[concepts/skill-vendoring]], [[concepts/tooling-consent-and-pin-management]], and [[concepts/harness-vs-local-tools]].

## Source-Defined Rules

The document describes several important rules for vendor skills:

- Vendoring should happen before the pipeline invokes the corresponding CLI for the first time.
- The vendored copy should be treated as immutable vendor content.
- Updates should happen by re-vendoring from a newer pinned release, not by editing the copy in place.
- The source repository and version or commit for the copied skill should be recorded alongside the pin information in `AGENTS.md`.
- The vendored skill is a prerequisite for a complete, repository-scoped adoption of the tool.
- The prereq script checks vendor-skills presence independently from CLI availability so the repo can distinguish "tool installed" from "tool fully adopted."

## Tool-Specific Cases

The document distinguishes between the main CLI skills and optional companion skills:

- `graphify` supports project-scoped skill installation through its own installer, which can write the skill into the repository.
- `openkb` must be vendored manually from the pinned upstream tag when a project-scoped installer is not available.
- Optional deck and critic skills for openkb are separate vendor copies and should be installed as their own top-level skill directories, not nested under the main openkb skill.
- If a CLI is installed but its matching vendor skill directory is missing, the prereq check reports that the skill should be vendored before first use.

This aligns vendor skills with [[concepts/toolchain-pinning]], [[concepts/integrity-pinning]], and [[concepts/source-provenance]].

## Relationship To Readiness Checks

The prereq workflow treats vendored skills as part of local readiness, but not as a substitute for executable verification. The system still relies on `scripts/check_prereqs.py` to confirm tool availability, and it degrades gracefully when an optional vendor skill is missing rather than failing the whole workflow.

`check_prereqs.py` reinforces this by:

- checking `git`, `uv`, and Python 3.11+ as hard prerequisites;
- checking `graphify` and `openkb` as optional CLIs;
- checking `.agents/skills/<tool>/SKILL.md` separately from CLI presence;
- warning when the CLI exists but the vendored skill is absent;
- allowing the workflow to continue when the CLI is not installed yet.

See [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] for the source discussion of dependency handling, tool boundaries, and vendoring requirements.

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
