---
type: quickstart
title: Repository memory quickstart
description: Compact front door to agent-smith's durable agent context.
timestamp: 2026-07-16T07:21:44.902Z
sources:
  - AGENTS.md
  - README.md
  - .agents/skills/agent-ready-context/SKILL.md
---

# Repository memory quickstart

Use this page after root `AGENTS.md`. Treat the wiki as context and repository
source/tests as authority.

## Start here

- [Preservation contract](INSTRUCTIONS.md) — rules every update must preserve.
- [Full index](index.md) — the canonical routing catalog.

This is the deterministic zero-LLM baseline of the wiki: agent-smith's three
product skills live under `.agents/skills/` (`agent-ready-context`,
`skill-creator`, `subagent-profile-adapter`), the OpenWiki producer maintains
this bundle through the staged runner
(`.agents/skills/agent-ready-context/scripts/run_openwiki_staged.py`), and the
operational basics (setup, tests, toolchain pins) stay in root `AGENTS.md`.
Semantic coverage by the provider-backed producer is pending; enrich or
replace this page through the documented lifecycle or reviewed direct edits.

## Working rules

- Use `.agents/skills/` for repeatable actions.
- Preserve manual wiki edits during incremental updates.
- Cite repository-relative evidence near important claims.
- Do not turn this page into a source-file catalog.
