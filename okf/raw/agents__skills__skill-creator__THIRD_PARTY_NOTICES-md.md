---
type: "source-file"
title: ".agents/skills/skill-creator/THIRD_PARTY_NOTICES.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/THIRD_PARTY_NOTICES.md"
source_path: ".agents/skills/skill-creator/THIRD_PARTY_NOTICES.md"
source_kind: "markdown"
source_hash: "sha256:27cdac5ae5412188b08b30f546d8cc157dafb4a4065ce39fe9b522560a4e1769"
source_commit: "ccc5c46198d5f3cff6552ca621d8ef7171074cf9"
tags: [source-file, markdown]
---

# .agents/skills/skill-creator/THIRD_PARTY_NOTICES.md

~~~
# Third-party notices

## Adapted passages in SKILL.md

`SKILL.md` documents its full conceptual lineage in
[`references/source-attribution.md`](references/source-attribution.md):
concepts and structure drawn from Anthropic's `skill-creator`, `superpowers`'
`writing-skills`, and OpenAI's system `skill-creator`. A textual comparison
against those three upstream sources found the file overwhelmingly
independent expression of borrowed ideas — not itself protected by
copyright — with one exception: three short passages that closely track
specific upstream wording. They are recorded here per Apache-2.0 §4(c).

Upstream sources for the adapted passages:

- Anthropic `skill-creator` — <https://github.com/anthropics/skills/tree/main/skills/skill-creator>
  — Licence: Apache-2.0. Copyright 2026 Anthropic, PBC. (per
  `skills/skill-creator/LICENSE.txt` in that repository)
- OpenAI system `skill-creator` — <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md>
  — Licence: Apache-2.0, per `skills/.system/skill-creator/LICENSE.txt` in
  that repository. That LICENSE.txt ships as the unfilled Apache-2.0
  appendix template (`Copyright [yyyy] [name of copyright owner]`); no
  specific copyright holder is stated by the upstream source itself.

Adapted passages:

1. Local: "The context window is a public good: challenge every line you
   add." — Adapted from OpenAI system `skill-creator`: "The context window
   is a public good. Skills share the context window with everything else
   Codex needs... Challenge each piece of information."
2. Local: "Match the skill's degrees of freedom to task fragility: fragile
   or destructive sequences get exact scripts and narrow instructions;
   open-ended tasks get principles and room to reason." — Adapted from
   OpenAI system `skill-creator`, "Set Appropriate Degrees of Freedom":
   "Match the level of specificity to the task's fragility and
   variability... Low freedom... Use when operations are fragile and
   error-prone, consistency is critical... High freedom... Use when
   multiple approaches are valid."
3. Local: "Catching yourself writing ALWAYS/NEVER everywhere is a yellow
   flag — reframe with the reasoning." — Adapted from Anthropic
   `skill-creator`: "If you find yourself writing ALWAYS or NEVER in all
   caps, or using super rigid structures, that's a yellow flag — if
   possible, reframe and explain the reasoning."

No notice is recorded for `superpowers`' `writing-skills`
(<https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/writing-skills>):
that repository carries no licence file at all (checked at its root and at
the `writing-skills` skill directory), and the comparison found no passage
in `references/testing-skills.md` closely tracking its specific wording —
only the shared, non-original RED-GREEN-REFACTOR/TDD terminology that
`writing-skills` itself attributes to standard test-driven-development
practice, not its own invention.

## Provenance rule

The upstream copyright holders, years, and licence terms above were
retrieved directly from the exact upstream files at the time this document
was written, not inferred or guessed. Re-verify against the current
upstream state before relying on this document for a new adaptation.
~~~
