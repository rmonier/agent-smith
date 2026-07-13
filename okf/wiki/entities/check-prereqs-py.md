---
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
type: "Work"
description: "Prerequisite-check script for the OpenKB build workflow"
---

# check_prereqs.py

`check_prereqs.py` is a repository script used at the start of the [[summaries/agents__skills__agent-ready-context__references__workflow-md|OpenKB build workflow]] to verify that required local prerequisites are available before any deeper build steps run.

## What it does

- Checks for hard requirements such as `git`, `uv`, and Python 3.11+.
- Flags missing or non-vendored toolchain skills when the workflow is about to use `graphify` or `openkb`.
- Acts as an early gate before source-pack staging, ingestion, or validation work begins.

## Why it matters

The workflow treats this script as part of [[concepts/preflight-checks|preflight checks]] and [[concepts/consent-first-workflows|consent-first workflows]]: if a hard requirement is missing, the process stops and asks the user before bootstrapping anything else. That keeps the build path aligned with [[concepts/graceful-degradation|graceful degradation]] and [[concepts/deterministic-builds|deterministic builds]].

## Related workflow roles

- Supports [[concepts/toolchain-pinning|toolchain pinning]] by ensuring the expected runtime is present before execution.
- Enforces [[concepts/skill-vendoring|skill vendoring]] by warning when installed CLIs are not backed by vendored skills.
- Fits into [[concepts/openkb-build-workflow|OpenKB build workflow]] as the first executable prerequisite check.
- Connects to [[entities/openkb]] and [[entities/graphify]] as the tooling it helps gate.

## Source context

In the referenced workflow document, this script is run immediately after reading the root `AGENTS.md` and the wiki index, and before any optional tooling bootstrap or OpenKB initialization.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
