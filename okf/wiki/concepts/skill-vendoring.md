---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Vendoring copies tool skills into the repo as durable local guidance."
---

# Skill Vendoring

Skill vendoring is the practice of copying an upstream tool's own agent skill into the repository so the workflow has a local, durable, and harness-neutral source of guidance. It treats the skill as vendor content rather than something to edit in place, and it is one of the ways a repository becomes [[concepts/agent-ready-repositories]]. The agent-ready-context skill frames this as part of the broader separation between executable actions, compiled context, and repository orientation.

## Why it matters

Vendoring closes the gap between installing a CLI and actually making that CLI usable for future maintenance inside the repository. The vendored copy preserves the tool's intended usage rules, lets later agents operate without relying on the original installation context, and supports toolchain pinning and provenance tracking by keeping the repository's tool guidance explicit and auditable.

The readiness workflow makes this boundary concrete: if `graphify` or `openkb` is installed, the repository should already contain `.agents/skills/<tool>/SKILL.md` for that tool. If the CLI is present but the vendored skill is missing, the check reports the gap and tells the user to vendor the pinned copy before first use. That turns vendoring into a preflight requirement rather than an optional cleanup step, and it ties directly to [[concepts/preflight-checks]], [[concepts/consent-first-tooling]], and [[concepts/tooling-consent-and-pin-management]].

The agent-ready-context skill also distinguishes portable repository skills from pinned tool copies that may be installed alongside them. The product skills are reusable actions the repository is meant to carry; the vendored tool skills are upstream copies of `graphify` and `openkb` that belong to the local toolchain state, not to the distributable product. That distinction keeps [[concepts/tooling-vendoring]] and [[concepts/tooling-context-governance]] aligned with the intended ownership boundaries.

## Core rules

- Vendor skills are copied into `.agents/skills/<name>/` before the corresponding CLI is used.
- The vendored copy is treated as read-only vendor content.
- Updates happen by re-vendoring from a newer pinned upstream version, not by editing the local copy.
- The repository should record the source repository and version or commit for each vendored skill.
- Missing companion skills should not break the workflow; the process should degrade gracefully.
- Product skills and vendored toolchain copies serve different roles and should not be confused with each other.

## Source document guidance

The readiness script distinguishes between hard runtime requirements, optional tools, and companion skills:

- `check_prereqs.py` is the authoritative readiness check.
- Python 3.11+, `git`, `uv`, and writable repository paths are required.
- `graphify` and `openkb` are optional tools, but if they are adopted their vendored skills must be present first.
- `skill-creator` and `subagent-profile-adapter` are follow-up capabilities, not hard blockers.

The script also checks the OpenKB configuration surface for consistency. If `okf/.openkb/config.yaml` exists alongside `config.yaml.example`, the shared keys `language`, `pageindex_threshold`, and `entity_types` must match the example. Provider-specific values such as model, litellm, and timeout are intentionally excluded from the drift check because they are user-specific rather than repository-shared. That makes vendoring adjacent to [[concepts/local-vs-shared-configuration]] and [[concepts/configuration-precedence]]: the repository controls the shared surface, while the user controls personal provider choices.

It also checks credential homes by name rather than reading secret contents. If both `okf/.env` and `~/.config/openkb/.env` exist, the project file wins for shared keys and the script warns that two credential homes may confuse contributors. This reinforces [[concepts/consent-first-tooling]], [[concepts/preflight-checks]], and [[concepts/tooling-consent-and-pin-management]]: the user approves a scoped adoption, the tool is installed with a pinned version, and the corresponding skill is copied into the repo before use.

## Practical model

The document treats vendoring as a repository-scoped adoption step:

1. Identify the upstream skill source.
2. Pin the tool version and record integrity.
3. Copy the skill into the repository's `.agents/skills/` tree.
4. Use the vendored skill as the durable reference for later work.

That model supports [[concepts/local-by-default-tooling]], [[concepts/project-scaffolding]], and [[concepts/skill-governance]] by keeping tool knowledge inside the repository instead of scattering it across user-specific harness state. It also reinforces [[concepts/deterministic-validation]] and [[concepts/supply-chain-security]] because the repository can validate and revalidate the exact tool content it has adopted.

The readiness script makes the model operational: it checks whether installed CLIs have matching vendored skills, reports when a CLI is installed without its local copy, and frames the missing copy as something that should be added before the first tool invocation. That is a concrete example of [[concepts/tooling-vendoring]] rather than a generic documentation pattern.

## Related ideas

Skill vendoring connects closely to [[concepts/generated-content-governance]], [[concepts/source-provenance]], [[concepts/integrity-pinning]], and [[concepts/trust-on-first-use]]. It is also a concrete example of [[concepts/tool-boundaries]] and [[concepts/graceful-degradation]] in agent workflows.

Source: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] and [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]