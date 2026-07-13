---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Exact-version tool locking with integrity checks for reproducible, trusted workflows."
---

# Toolchain Pinning

Toolchain pinning is the practice of locking external tools to exact versions and recording their integrity so a workflow can be reproduced and trusted over time. In the agent-ready-context workflow, pinning is not just about stability; it is part of supply-chain security, trust-on-first-use, deterministic validation, and safe incremental rebuilds. It also now appears as an explicit preflight concern in `check_prereqs.py`, which checks whether required tools exist, whether optional tools are installed, and whether any vendored skill copies remain aligned before the workflow proceeds.

## What it means

- Pin exact versions for installable tools instead of floating version ranges.
- Record an integrity value, typically a sha256 hash, for the exact artifact that was installed.
- Record the index or registry source the artifact came from.
- Re-check the same source later and compare the artifact hash before reinstalling.
- Treat a hash mismatch for the same version as a stop-and-report event.
- Keep the package pin and any vendored skill copy aligned when a tool ships reusable agent skill content.
- Apply pinning before first CLI use so vendored toolchain skills and installed CLIs stay in sync.
- Separate hard prerequisites from optional tools, so readiness checks can fail clearly without overblocking the whole workflow.

This turns tool installation into a verifiable process rather than an informal setup step.

## Why it matters

The source documents treat toolchain pinning as a supply-chain control, not a convenience feature. Version numbers alone do not prove that a package has not been substituted or republished. Capturing the hash at first install creates a trust-on-first-use baseline that later installs can compare against.

The prerequisite checker makes this concrete by distinguishing required runtime pieces from optional tooling and by reporting the current state in a structured way. It also warns when a tool is present but its vendored skill copy is missing, because the executable and the repo-local skill contract are both part of the trusted toolchain.

This supports:

- source provenance by recording where the artifact came from
- integrity pinning by binding identity to content
- version pinning by freezing the selected release
- hash registry coherence by comparing the recorded hash against future downloads
- quality gates by refusing to proceed on mismatch
- deterministic builds by reducing hidden tool drift across runs
- graceful degradation by allowing optional tools to be absent without hiding the gap

## Source-specific details

The workflow makes pinning operational for the `agent-ready-context` skill:

- `uv` is the required Python toolchain for local execution, and `check_prereqs.py` treats its absence as a hard prerequisite failure.
- `graphify` and `openkb` are optional tools, but when adopted they must be pinned and recorded.
- `check_prereqs.py` is the executable source of truth for readiness checks.
- The script checks `git`, `uv`, and Python 3.11+ as hard requirements before continuing.
- If optional tools are missing, the workflow offers consent-first bootstrap paths rather than assuming installation.
- Vendor copies of the `graphify` and `openkb` skills must exist before first CLI use when the CLI is installed.
- Install commands should use exact versions, such as `uv tool install 'openkb==X.Y.Z'`.
- Registry settings should come from the environment or project config; the workflow should not hardcode or override mirrors.
- If a configured mirror cannot serve the pinned package, that should be reported rather than worked around.
- Some tool versions may require an additional transitive constraint, such as `--with 'openai==2.44.0'`, when a known dependency range would otherwise break validation.
- The workflow recommends running `graphify update . --force` before source-pack creation when Graphify is installed, but only after the relevant vendored skill checks are satisfied.
- The same pinned-tool discipline extends to the local OpenKB bundle, where provider choice stays local and uncommitted.
- The checker also validates that `okf/.openkb/config.yaml` exists when needed and that shared keys match the committed example, so local configuration drift does not masquerade as tool readiness.

The document also distinguishes between the tool itself and the vendored skill copy that accompanies it. That means pinning applies both to the CLI package and to the skill content that is copied into the repository, reinforcing skill vendoring and vendor skills.

## Update policy

Pinning is deliberately conservative:

1. Detect a newer version through the configured index.
2. Review release notes or changelog before changing the pin.
3. After explicit user approval, install the new version.
4. Capture the new integrity value.
5. Update the recorded pin data in `AGENTS.md`.

This keeps updates intentional and auditable, and it prevents silent drift in the local toolchain.

## Practical workflow

The pinned-tool workflow in the source documents is:

- run the prerequisite checker
- report missing tools with package name, source, pinned version, and exact command
- let the user decide whether to install, skip, or self-install
- verify the installed version
- re-run the prerequisite checker
- vendor the toolchain skills before any CLI-backed build step that depends on them
- preserve the deterministic source-pack and wiki pipeline after the toolchain is prepared

This is a consent-first tooling approach to dependency setup, with graceful degradation when optional tools are absent. The checker’s output structure reinforces that approach by separating required checks, optional tools, vendored skills, config state, companion skills, writable paths, and human-readable notes.

## Related ideas

Toolchain pinning sits near several other governance concepts:

- dependency management for handling required tools and their dependencies
- tooling consent and pin management for consent-aware pin changes
- local-by-default tooling for keeping installs scoped to the repository
- preflight checks for validating readiness before use
- deterministic builds for making repeated runs behave the same way
- provenance-aware tool installation for recording source, version, and integrity together
- supply-chain security for treating tool acquisition as a trust boundary
- vendor skills for keeping tool-dependent skill copies aligned with installed CLIs
- evidence-backed skill initialization for making setup decisions from checked evidence rather than memory
- configuration precedence for understanding when the project-local OpenKB environment overrides a user-global one
- graceful degradation for preserving workflow progress when optional tools or companion skills are missing

Source: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] and [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]


See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]