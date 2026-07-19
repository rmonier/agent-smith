# Third-party notices

This document records third-party and adapted material distributed within
`agent-smith`. Runtime dependencies that users install separately (such as
OpenWiki or markitdown) are not bundled here unless explicitly stated below —
only what is actually committed to this repository is in scope.

## skill-creator: adapted passages

`.agents/skills/skill-creator/SKILL.md` is original work overall — see
`.agents/skills/skill-creator/references/source-attribution.md` for the
full documented lineage of concepts and structure it draws on. A textual
comparison against the three upstream sources it credits found the
overwhelming majority of the file to be independently written expression
of borrowed ideas (not copyrightable in themselves), with one exception:
three short passages that closely track specific upstream wording closely
enough to treat as adapted rather than independently expressed. They are
recorded here per Apache-2.0 §4(c)'s attribution-notice requirement.

Upstream sources:

- Anthropic `skill-creator` — <https://github.com/anthropics/skills/tree/main/skills/skill-creator>
  — Licence: Apache-2.0. Copyright 2026 Anthropic, PBC. (per
  `skills/skill-creator/LICENSE.txt` in that repository)
- OpenAI system `skill-creator` — <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md>
  — Licence: Apache-2.0, per `skills/.system/skill-creator/LICENSE.txt` in
  that repository. That LICENSE.txt ships as the unfilled Apache-2.0
  appendix template (`Copyright [yyyy] [name of copyright owner]`); no
  specific copyright holder is stated by the upstream source itself.

Adapted passages (local file: `.agents/skills/skill-creator/SKILL.md`):

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

No corresponding notice is recorded for `superpowers`' `writing-skills`
(<https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/writing-skills>):
that repository carries no licence file at all (checked at its root and at
the `writing-skills` skill directory), and the comparison found no passage
in this repository closely tracking its specific wording — only the
shared, non-original RED-GREEN-REFACTOR/TDD terminology that `writing-skills`
itself attributes to standard test-driven-development practice.

## Important provenance rule

None of the above upstream copyright holders, years, revisions, or source
paths are inferred or guessed — each was retrieved directly from the exact
upstream version at the time this document was written. If any of these
upstream projects move to a new revision, re-verify this section against
the new revision rather than assuming these facts still hold.

If a future external-evidence file is ever staged verbatim (a
byte-identical fetch, not a paraphrase), verify the actual upstream licence
directly, add a per-file `REUSE.toml` override splitting frontmatter/body
copyright, and record it here.
