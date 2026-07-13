# Third-party notices

This document records third-party and adapted material distributed within
`agent-smith`. Runtime dependencies that users install separately (the
`openkb` and `graphifyy` PyPI packages themselves) are not bundled here
unless explicitly stated below — only what is actually committed to this
repository is in scope.

## OpenKB vendored skill

- Local path: `.agents/skills/openkb/`
- Upstream project: <https://github.com/VectifyAI/OpenKB>
- Upstream file or directory: `skills/openkb/`
- Upstream release: tag `v0.4.4`, commit `bd9fe3989e71fc8012b19eb305662fa307f0a799`
  — this repository's pinned OpenKB version per `AGENTS.md`. The
  `skills/openkb/` directory content is unchanged from tag `v0.4.3`
  (commit `3889e97`); both revisions were fetched and diffed directly
  against the vendored copy to confirm this rather than assumed.
- Licence: Apache-2.0
- Copyright: 2026 Vectify AI (per the upstream repository's `LICENSE` file)
- Local modifications: none — verified byte-for-byte identical to the
  upstream `skills/openkb/` directory (`SKILL.md` and `references/`) at
  the pinned revision

The vendored files remain under their upstream Apache-2.0 licence. No
upstream `NOTICE` file exists in this OpenKB revision to preserve.

**Also mirrored into the OKF wiki:** the `agent-ready-context` pipeline
stages a full-text copy of every repository file it ingests, including the
vendor skill files themselves. `okf/wiki/sources/agents__skills__openkb__*.md`
and the matching `okf/raw/agents__skills__openkb__*.md` files are verbatim
copies of `.agents/skills/openkb/SKILL.md` and its `references/`, not
original commentary. They remain Apache-2.0/Vectify AI, declared via an
explicit `REUSE.toml` override — the broader "`okf/` is unlicensed"
treatment described in `LICENSING.md` does not apply to these specific
files, since a verbatim copy of someone else's already-licensed material
cannot be relicensed just by restaging it.

## Graphify vendored skill

- Local path: `.agents/skills/graphify/`
- Upstream project: <https://github.com/safishamsi/graphify>
- Upstream package: PyPI `graphifyy`, version `0.9.10`
- Upstream file: the `agents`-harness variant shipped in the wheel —
  `graphify/skill-agents.md` plus `graphify/skills/agents/references/`
- Licence: MIT
- Copyright: (c) 2026 Safi Shamsi (per the `graphifyy` wheel's
  `licenses/LICENSE` file)
- Local modifications: none — verified byte-for-byte identical to the
  `skill-agents.md` variant and its `references/` bundled in `graphifyy`
  0.9.10 (this repository targets the AGENTS.md-convention harness variant,
  not the Claude-specific default `skill.md`)

**Also mirrored into the OKF wiki:** the same staging applies here —
`okf/wiki/sources/agents__skills__graphify__*.md` and the matching
`okf/raw/agents__skills__graphify__*.md` files are verbatim copies of
`.agents/skills/graphify/SKILL.md`, its `references/`, and
`.graphify_version`. They remain MIT/Safi Shamsi via the same `REUSE.toml`
override, for the same reason.

The vendored files remain under their upstream MIT licence.

## Graphify-generated output (graphify-out/)

- Local path: `graphify-out/graph.html`
- Nature: this file is not repository content passed through Graphify —
  it is Graphify's own generated interactive-viewer template (inline
  CSS/JS scaffold, plus a `vis-network` CDN include), populated with data
  about this repository. The template itself is Graphify's work product.
- Upstream project: <https://github.com/safishamsi/graphify>, PyPI package
  `graphifyy` version `0.9.10`, generated via the `/graphify` pipeline
  documented in `.agents/skills/graphify/SKILL.md`
- Licence: MIT
- Copyright: (c) 2026 Safi Shamsi

`graphify-out/graph.json`, `graphify-out/manifest.json`,
`graphify-out/.graphify_labels.json`, and `graphify-out/GRAPH_REPORT.md`
sit alongside `graph.html` but contain no Graphify template code — they are
generated data/report describing this repository's own structure, and are
licensed `CC-BY-4.0` as generated documentation (see `LICENSING.md`), not
listed here as third-party material.

## agent-ready-context: OpenKB-derived compatibility fallback

- Local file: `.agents/skills/agent-ready-context/scripts/editorial_pass.py`,
  the `_MIRRORED_KNOWN_TARGETS_USER` string constant and the
  `_format_targets_mirrored` function (approximately lines 131-154)
- Upstream repository: <https://github.com/VectifyAI/OpenKB>
- Upstream source file: `openkb/agent/compiler.py`
- Upstream symbols: `_KNOWN_TARGETS_USER` (copied verbatim) and
  `_format_known_targets` (logic mirrored, reimplemented from scratch)
- Upstream release: tag `v0.4.4`, commit
  `bd9fe3989e71fc8012b19eb305662fa307f0a799` — the upstream source was
  fetched and diffed directly against the mirrored copy to confirm the
  match, not assumed from the in-file comment that already documented it
- Licence: Apache-2.0
- Copyright: 2026 Vectify AI (per the upstream repository's `LICENSE` file)
- Modifications: `_format_targets_mirrored` is a from-scratch
  reimplementation matching the upstream function's behaviour (renamed, no
  docstring); `_MIRRORED_KNOWN_TARGETS_USER` is an unmodified verbatim copy

This is a best-effort fallback used only when OpenKB's private
(underscore-prefixed, no-stability-guarantee) compiler internals cannot be
imported from the installed tool environment — it degrades briefing
wording only, never the script's `--check` correctness gates, which use
OpenKB's stable public API as an external dependency (not copied code).
See `.agents/skills/agent-ready-context/THIRD_PARTY_NOTICES.md` for the
per-skill copy of this same record.

**Also mirrored into the OKF wiki:** `okf/wiki/sources/agents__skills__agent-ready-context__scripts__editorial_pass-py.md`
and `okf/raw/agents__skills__agent-ready-context__scripts__editorial_pass-py.md`
are staged copies of this file. Since the original file's own copyright is
split between Romain Monier (the bulk of the file) and Vectify AI (the
mirrored fragment described above), the mirror's `REUSE.toml` entry credits
both holders too — both under Apache-2.0, so the licence identifier itself
doesn't change, only the copyright attribution.

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

## External evidence staged verbatim in okf/raw/ and okf/wiki/sources/

The `agent-ready-context` pipeline stages some external documentation as
byte-identical evidence copies (not paraphrased — provenance requires the
staged copy to match what was actually fetched). Unlike the vendored
openkb/graphify skill mirrors above, these are not this repository's own
tooling; they are third-party reference material fetched from a URL. Each
entry below was independently verified against the live upstream source on
2026-07-13, not inferred from the staged copy's own text.

Each of these files also carries a thin YAML frontmatter wrapper (`type`,
`title`, `resource`, `description`, `tags`, `timestamp`, `source`, `trust`)
documenting how and when the source was staged. That wrapper is original
commentary by Romain Monier; the Markdown body below it is the third
party's own text. `REUSE.toml` records both copyright holders on the file
per this split.

### OKF v0.1 specification

- Local paths: `okf/raw/okf-spec.md`, `okf/wiki/sources/okf-spec.md`
- Upstream: <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>
- Licence: Apache-2.0, confirmed by fetching that repository's `LICENSE.md`
  directly. The file is the unfilled Apache-2.0 appendix template
  ("Copyright [yyyy] [name of copyright owner]") — no specific copyright
  holder name or year is committed to the licence file itself.
- Copyright: attributed here as "GoogleCloudPlatform/knowledge-catalog
  contributors" since no more specific holder is stated by the source.
  Re-verify if that repository ever adds an explicit NOTICE/AUTHORS file.
- Modifications: none to the body — staged verbatim as evidence.

### Agent Skills specification

- Local paths: `okf/raw/agent-skills-spec.md`, `okf/wiki/sources/agent-skills-spec.md`
- Upstream: <https://agentskills.io/specification> (published from
  <https://github.com/agentskills/agentskills>)
- Licence: that repository states a split — Apache-2.0 for code, CC-BY-4.0
  for documentation — confirmed by fetching its `LICENSE` file (Apache-2.0,
  copyright line "Copyright 2025 Anthropic, PBC"). The staged spec text is
  documentation, so CC-BY-4.0 applies to it. The documentation-specific
  licence file was not independently fetched (only the code `LICENSE`
  was), so the "2025 Anthropic, PBC" copyright attribution here is a
  same-repository inference, not independently confirmed for the docs
  licence specifically. Re-verify if that repository's ownership or
  licensing structure changes.
- Modifications: none to the body — staged verbatim as evidence.

### Karpathy "LLM Wiki" gist

- Local paths: `okf/raw/karpathy-llm-wiki-gist.md`, `okf/wiki/sources/karpathy-llm-wiki-gist.md`
- Upstream: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- Licence: none stated anywhere on the gist page — confirmed by direct
  inspection, not assumed. Under default copyright, this means no formal
  redistribution licence is granted. The gist's own body text states: "This
  is an idea file, it is designed to be copy pasted to your own LLM Agent
  (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.)" — an explicit
  authorial invitation to copy for exactly this kind of use, though not a
  formal licence grant (no modification/sublicensing/further-redistribution
  rights are stated). See
  `LICENSES/LicenseRef-Karpathy-Gist-No-License-Stated.txt` for the full
  reasoning behind the custom `LicenseRef` used in `REUSE.toml`.
- Copyright: Andrej Karpathy.
- Modifications: none to the body — staged verbatim as evidence.

If a future external-evidence file is staged this way (a byte-identical
fetch, not a paraphrase), apply the same process: verify the actual
upstream licence directly (never infer it from the staged copy or guess),
add a per-file `REUSE.toml` override splitting frontmatter/body copyright
the same way, and record it here.

## Important provenance rule

None of the above upstream copyright holders, years, revisions, or source
paths are inferred or guessed — each was retrieved directly from the exact
vendored/generated version (pinned commit, installed wheel, or fetched
upstream file) at the time this document was written. If any of these
upstream projects move to a new pinned revision, re-verify this section
against the new revision rather than assuming these facts still hold.
