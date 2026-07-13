---
type: "source-file"
title: ".agents/skills/subagent-profile-adapter/assets/profile-intents.example.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/subagent-profile-adapter/assets/profile-intents.example.md"
source_path: ".agents/skills/subagent-profile-adapter/assets/profile-intents.example.md"
source_kind: "markdown"
source_hash: "sha256:095c3dc6338c67a8265fc962c3c491b31b7eb28d878d6fc71138adc5bb156c51"
source_commit: "3e2b0704b5fefafe51867cb71a9a484563563cc5"
tags: [source-file, markdown]
---

# .agents/skills/subagent-profile-adapter/assets/profile-intents.example.md

~~~
# Example profile intents

These are not vendor-specific files. They are short intent descriptions the agent can translate into native harness files after reading current harness documentation.

## okf-curator

Purpose: Maintain `okf/wiki/` as the durable context source of truth.
Use when: OKF is missing, stale, invalid, or external docs need evidence pages.
Context: `AGENTS.md`, relevant `okf/wiki/` pages, `agent-ready-context` skill.
Permissions: Read allowed; write OKF/AGENTS.md ask or allow according to user policy; shell limited to validation scripts.

## skill-architect

Purpose: Decide whether repeated actions should become skills and create/update custom skills.
Use when: OKF or user workflow reveals repeated executable actions.
Context: `AGENTS.md`, `okf/wiki/`, existing `.agents/skills/`, `skill-creator` skill.
Permissions: Read/write `.agents/skills/` according to user policy; shell limited to validation scripts.

## repo-cartographer

Purpose: Explore repository structure read-only and summarize important files and flows.
Use when: initial repo understanding is needed before OKF updates.
Context: `AGENTS.md`, `graphify-out/`, file tree, relevant source files.
Permissions: Read-only by default.
~~~
