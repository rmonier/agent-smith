---
type: "source-file"
title: ".agents/skills/skill-creator/references/action-vs-context.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/references/action-vs-context.md"
source_path: ".agents/skills/skill-creator/references/action-vs-context.md"
source_kind: "markdown"
source_hash: "sha256:ee6bb244bb0554721091a13d9cddd17e958278c9147c05e919eb6f6076d04ed8"
source_commit: "3e2b0704b5fefafe51867cb71a9a484563563cc5"
tags: [source-file, markdown]
---

# .agents/skills/skill-creator/references/action-vs-context.md

~~~
# Action vs context boundaries

Use this reference when deciding where a piece of information belongs.

## Put it in a skill when it is an action

Create or update a skill when the agent/harness should repeat a procedure:

- run a multi-step command sequence
- generate or transform files in a predictable way
- validate an artifact
- call a tool/API with non-obvious flags
- scaffold a repeated project structure
- perform a migration or incident workflow
- wrap a vendor skill with project-specific guardrails

## Put it in OKF wiki when it is context

Keep durable knowledge in OKF:

- architecture and component explanations
- source provenance and external documentation evidence
- design decisions and tradeoffs
- runbook background and why a workflow exists
- repository-specific facts discovered during analysis
- historical memory that helps agents understand the project

## Put it in AGENTS.md when it is orientation

Keep `AGENTS.md` concise:

- setup and test commands
- repo-specific rules
- where to find `okf/wiki/`, `graphify-out/`, and `.agents/skills/`
- security and contribution best practices
- maintenance reminders

## Vendor skill rule

Vendor skills are dependencies. Install and update them through the chosen skill manager, keep the generated lock file such as `skill-lock.json` when present, and do not patch vendor files directly. Put project changes in a custom skill under `.agents/skills/`.
~~~
