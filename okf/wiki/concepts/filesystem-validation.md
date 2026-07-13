---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md"]
description: "Checking filesystem paths for write access and expected repo state"
---

# Filesystem Validation

Filesystem validation is the practice of probing repository paths to confirm they exist, are writable, and behave as expected before an agent depends on them. In the `agent-ready-context` workflow, it acts as a lightweight safety check that catches setup problems early without requiring any third-party tooling.

## What it covers

- Existence checks for required directories and files.
- Write probes for paths the workflow needs to modify.
- Detection of path-specific setup drift, such as missing local config files.
- Basic confirmation that the current repository can support later build or ingestion steps.

## In `check_prereqs.py`

The script in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] validates three writable locations:

- `okf/.okf-build/input`
- `okf`
- `.agents/skills`

It attempts to create a temporary marker file in each path and remove it immediately afterward. This confirms that the directory is not just present, but actually usable for subsequent workflows.

The same script also checks for filesystem-backed configuration and credential placement:

- `okf/.openkb/config.yaml`
- `okf/.openkb/config.yaml.example`
- `okf/.env`
- `~/.config/openkb/.env`

These checks help determine whether the repository is prepared for [[concepts/local-vs-shared-configuration]] and whether the local environment matches the expectations of [[concepts/agent-ready-context]].

## Why it matters

Filesystem validation prevents agents from discovering too late that a repository is read-only, missing expected directories, or configured in a way that will break later stages. That makes it a practical foundation for [[concepts/preflight-checks]], [[concepts/executable-validation]], and [[concepts/safe-automation]].

## Design traits

- Uses direct path probes instead of assuming a repository layout.
- Treats write access as a hard readiness signal for workflow-critical directories.
- Keeps the check simple enough to run in a fresh clone.
- Avoids reading secrets while still confirming credential-file presence.

## Related ideas

- [[concepts/path-safety]] for avoiding unsafe path assumptions.
- [[concepts/configuration-precedence]] for deciding which config location wins.
- [[concepts/graceful-degradation]] for continuing when optional paths or tools are absent.
- [[concepts/preflight-checks]] for the broader readiness-check pattern.

See also: [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]