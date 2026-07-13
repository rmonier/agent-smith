---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/repo-snapshot.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__transcribe-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__runtime-detection-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__references__testing-skills-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
type: "Product"
description: "Python toolchain used for local, pinned script execution in OKF workflows"
---

# uv

`uv` is a Python toolchain used by the [[summaries/agents__skills__agent-ready-context__SKILL-md|agent-ready-context]] skill as the required way to run bundled scripts and manage Python-based workflow commands.

## What It Does

The skill treats `uv` as the default execution layer for repository automation. It is used to run the skill's packaged scripts in isolated environments, resolve their dependencies, and avoid touching the repository's own project environment.

## Key Facts From The Documents

- `uv` is required for the skill's script execution convention.
- The skill says to run bundled scripts with `uv run`.
- It explicitly forbids bare `python` or `python3` when `uv` is available.
- If `uv` is missing, the skill treats that as a prerequisite problem and routes through tooling bootstrap.
- The document names `uv` as one of the core tools in the agent-ready pipeline alongside OpenKB and Graphify.
- `uv` is also referenced in install and validation commands for prereq checks, OKF staging, and bundle validation.
- `uv` is documented as having no telemetry, which supports the pipeline's [[concepts/privacy-preserving-tooling]] posture.

## Role In The Workflow

`uv` supports the broader [[concepts/toolchain-pinning]] and [[concepts/provenance-aware-tool-installation]] approach in the skill by making script execution reproducible and isolated. It is part of the operational setup for [[concepts/agent-ready-context]] and the repository's [[concepts/deterministic-validation]] workflow.

In the privacy and data-flow guidance, `uv` belongs to the local-only tier of the toolchain: prereq checks, source packing, skeleton generation, and validation steps remain on the machine, and `uv` itself is not a source of telemetry or network egress.

## Related Pages

- [[concepts/agent-ready-context]]
- [[concepts/toolchain-pinning]]
- [[concepts/provenance-aware-tool-installation]]
- [[concepts/deterministic-validation]]
- [[concepts/privacy-preserving-tooling]]
- [[entities/openkb]]
- [[entities/graphifyy]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]