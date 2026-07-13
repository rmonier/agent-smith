---
sources: ["summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Work"
description: "Preflight validation script for agent-ready repository setup"
---

# check_prereqs.py

`check_prereqs.py` is a preflight validation script used by the [[entities/agent-ready-context-skill|agent-ready-context skill]] to confirm that a repository is ready for agent-driven work and to surface gaps before the larger OpenKB workflow runs.

## What it does

- Checks hard prerequisites such as [[entities/python|Python]] 3.11+, [[entities/git|git]], and [[entities/uv|uv]].
- Verifies the current path is inside a git worktree.
- Detects optional CLI tools, especially [[entities/graphify|graphify]] and [[entities/openkb|openkb]].
- Confirms vendored tool skills exist when the matching CLI is installed.
- Validates local OpenKB configuration presence and shared-key drift against `config.yaml.example`.
- Checks whether `.env` files exist in the project or user-global OpenKB config location.
- Probes important repository paths for writability.
- Reports whether the repository can proceed with the agent-ready-context workflow without blocking gaps.

## Key behavior

- The script is designed to run without third-party dependencies in a fresh repository.
- It prefers `uv run` but falls back to bare `python3` in degraded mode.
- It treats shared OpenKB config keys like `language`, `pageindex_threshold`, and `entity_types` as contributor-wide settings.
- It does not read secret `.env` contents; it only checks for file presence.
- It uses a short diagnostic report or a full JSON result depending on the `--json` flag.
- It reports notes for missing optional tools, missing companion skills, and config inconsistencies.
- It serves as a prerequisite gate before the broader OpenKB and tooling bootstrap steps in the agent-ready workflow.
- In the broader skill, it sits inside a progressive-disclosure workflow that starts from `AGENTS.md` and then routes through `okf/wiki/index.md` when available.
- The skill also frames it as part of the repository's boundary management between skills, compiled [[concepts/compiled-knowledge-bases|compiled knowledge bases]], and `AGENTS.md` orientation.
- Its guidance ties it to deterministic staging, repository linting, and the wider OpenKB validation loop rather than treating it as an isolated script.

## Repository role

This script acts as a health gate for [[concepts/preflight-checks|preflight checks]] and supports [[concepts/graceful-degradation|graceful degradation]] by distinguishing required failures from optional gaps. It also reflects [[concepts/configuration-precedence|configuration precedence]], [[concepts/skill-vendoring|skill vendoring]], and [[concepts/path-safety|path safety]] concerns in the agent-ready-context workflow. It is part of the larger [[concepts/agent-ready-context|agent-ready context]] pipeline that organizes repository setup, deterministic staging, and validation around OpenKB.

The parent skill also places it within a broader policy stack that includes [[concepts/deterministic-okf-staging|deterministic OKF staging]], [[concepts/openkb-wiki-validation-modes|OpenKB wiki validation modes]], and [[concepts/context-surface-separation|context surface separation]] between action skills, compiled wiki context, and repository guidance.

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[entities/agent-ready-context]]
- [[entities/graphify]]
- [[entities/openkb]]
- [[entities/skill-creator]]
- [[entities/subagent-profile-adapter]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/preflight-checks]]
- [[concepts/graceful-degradation]]
- [[concepts/configuration-precedence]]
- [[concepts/skill-vendoring]]
- [[concepts/path-safety]]
- [[concepts/deterministic-okf-staging]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/context-surface-separation]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/README-md]]