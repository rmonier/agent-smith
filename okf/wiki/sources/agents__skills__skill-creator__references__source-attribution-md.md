---
type: "source-file"
title: ".agents/skills/skill-creator/references/source-attribution.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/references/source-attribution.md"
source_path: ".agents/skills/skill-creator/references/source-attribution.md"
source_kind: "markdown"
source_hash: "sha256:251e8287be0737be9a6eeb7a960e0ce5ec4d4089eace4d1645cb1459f9b23f54"
source_commit: "1ee94b6b1cbd3168d6dc0d0293dd251fb1c0070a"
tags: [source-file, markdown]
---

# .agents/skills/skill-creator/references/source-attribution.md

~~~
# Source attribution and adaptation notes

`skill-creator` is an adaptation, not an invention. Lineage, in order of influence (verified against the upstream repositories on 2026-07-05):

1. **Anthropic `skill-creator`** — <https://github.com/anthropics/skills/tree/main/skills/skill-creator> — the primary base: progressive-disclosure layering (metadata → SKILL.md body under 500 lines → bundled resources loaded on demand), the `scripts/`/`references/`/`assets/` split, description-as-trigger guidance, degrees-of-freedom calibration, and the writing rule "explain to the model why things are important in lieu of heavy-handed MUSTs".
2. **`superpowers` `writing-skills`** — <https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/writing-skills> — the testing discipline: baseline-first pressure scenarios (run the task *without* the skill, record the exact failures, write the skill against them, then close remaining loopholes), "description = when to use, not what the skill does" (an agent may follow a workflow summary in the description instead of reading the body), token-budget mindset, and the red flags: narrative examples, generic names, batch skill creation.
3. **OpenAI system `skill-creator`** — <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md> — the lean understand → plan → initialize → edit → validate → iterate workflow shape and the `init_skill.py`/`quick_validate.py` script pattern, "the context window is a public good" (challenge every line), and the no-auxiliary-files rule (no README or CHANGELOG inside a skill).

Related integration, not lineage: **OpenKB Skill Factory** (`openkb skill new/validate/eval`) — <https://github.com/VectifyAI/OpenKB> (verified 2026-07-07) — the optional downstream packaging path this skill points at. Generated skills stay under `okf/output/skills/` until the user adopts one into `.agents/skills/`, where it must pass the same validation and standards as any hand-written skill.

## What this adaptation adds

The reasons this exists as its own skill instead of vendoring one of the above:

- vendor-neutral `.agents/skills/` layout and agentskills.io spec compliance, instead of product-specific folders;
- the OKF boundary: action vs context vs orientation, so skills never absorb knowledge that belongs in `okf/wiki/` or `AGENTS.md`;
- the hardening path: consent-first version-pinned installs, integrity recording, registry-agnostic commands, secret hygiene, minimal scoped `allowed-tools`, artifact gitignoring;
- vendor-skill immutability and lockfile policy;
- uv-first script execution with PEP 723 inline metadata.

## Adaptation rules

- write project skills only under `.agents/skills/`
- keep skills action-oriented
- keep context in `okf/wiki/`
- keep `AGENTS.md` as orientation only
- validate required frontmatter and folder naming before handoff

Do not copy runtime-specific metadata, product-specific folders, or personal agent configuration into the repository.
~~~
