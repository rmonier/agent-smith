# Licensing

`agent-smith` contains material under multiple licences, applied by file
according to its nature and origin — this is scope licensing, not ordinary
dual licensing. A given original Markdown file is under CC-BY-4.0. A given
original Python file is under Apache-2.0. Recipients are not offered a
choice between licences for the same file.

## Original material

Unless otherwise indicated below:

- Original Python and other executable source code — the scripts under each
  of the three product skills' `scripts/` directories — is licensed under
  the Apache License 2.0 (`Apache-2.0`).
- Original agent-skill instructions, documentation, specifications,
  examples, references, and other original Markdown content — including
  `README.md`, `AGENTS.md`, and the three product skills' `SKILL.md` and
  `references/` — are licensed under Creative Commons Attribution 4.0
  International (`CC-BY-4.0`).
- Repository operational configuration (`CITATION.cff`, `.gitignore`,
  `.gitattributes`, `.graphifyignore`, `okf/.openkb/hashes.json`,
  `okf/.openkb/config.yaml.example`) is licensed under Apache-2.0.

Copyright © 2026 [Romain Monier](https://github.com/rmonier).

Project source: [`agent-smith`](https://github.com/rmonier/agent-smith).

## Third-party and vendored material

Vendored, copied, generated, or adapted third-party files remain under
their applicable upstream licences:

- `.agents/skills/openkb/` — unmodified upstream `Apache-2.0` material.
- `.agents/skills/graphify/` — unmodified upstream `MIT` material.
- `graphify-out/graph.html` — embeds Graphify's own `MIT`-licensed viewer
  template.
- `.agents/skills/skill-creator/SKILL.md` — original overall, but
  incorporates a small number of closely adapted passages from
  Apache-2.0-licensed upstream `skill-creator` skills.
- `.agents/skills/agent-ready-context/scripts/editorial_pass.py` — original
  overall, but incorporates a small OpenKB-derived fallback (Apache-2.0,
  same licence as the rest of the file) used only when OpenKB's private
  compiler internals can't be imported.

File-level copyright and licence assignments are declared through
`REUSE.toml` (and, for the closely adapted passages above, plain-language
notes). Full third-party origin, revision, and modification information is
documented in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Generated reports about this repository

`graphify-out/graph.json`, `graphify-out/manifest.json`,
`graphify-out/.graphify_labels.json`, and `graphify-out/GRAPH_REPORT.md` are
Graphify-generated data and prose describing this repository's own
structure. They carry no third-party boilerplate, so they are licensed
`CC-BY-4.0` like other generated documentation (see
[Generated content](#generated-content) below).

## The `okf/` knowledge base: unlicensed, not hidden

`okf/wiki/` (the OpenKB-compiled project wiki) and `okf/raw/` (its staged
sources) are internal project context for contributors — orientation notes,
cross-document synthesis, and provenance — not part of the supported
product surface described in [`README.md`](README.md#the-skills).

These files are **not licensed for reuse**. They remain fully copyrighted
by Romain Monier with no licence granted beyond whatever limited rights
GitHub's own terms of service extend to viewing and forking a public
repository (see `LICENSES/LicenseRef-All-Rights-Reserved.txt`). This is
deliberate, not an oversight: being publicly visible in a cloned repository
and being *licensed for reuse* are different things, and this material —
generated commentary about the repository's own files, not a deliverable in
its own right — is the former without the latter.

Exception: `okf/wiki/sources/` and `okf/raw/` also hold full-text staged
copies of *every* ingested repository file — not just newly synthesized
commentary. Three sub-cases carry their own licence rather than the
blanket "unlicensed" rule, each via an explicit `REUSE.toml` override (see
`THIRD_PARTY_NOTICES.md` for the full lists):

1. The vendored `openkb`/`graphify` skill mirrors — a verbatim copy of
   someone else's already Apache-2.0/MIT-licensed content stays under that
   same licence regardless of where it's restaged.
2. Mirrors of this repository's *own* already-licensed files (`README.md`,
   the three product skills' `SKILL.md`/`references/`/`assets/`/scripts,
   etc.) — these inherit the same CC-BY-4.0/Apache-2.0 grant as the
   original file. Declaring a byte-identical copy of your own openly
   licensed file "all rights reserved" doesn't protect anything (the
   original is already open) and only creates confusing, inconsistent
   metadata.
3. External evidence staged verbatim from a URL for provenance (currently
   the OKF spec, the Agent Skills spec, and Andrej Karpathy's "LLM Wiki"
   gist) — these carry whatever licence (or lack of one) the actual
   upstream source states, independently verified, never assumed. Their
   thin YAML frontmatter wrapper (staging metadata) remains Romain
   Monier's own commentary; the body is the third party's.

The blanket "unlicensed" rule above applies only to what's left: the
compiled wiki's own synthesized commentary (`okf/wiki/concepts/`,
`okf/wiki/entities/`, `okf/wiki/summaries/`, `okf/wiki/tooling/`,
`okf/wiki/index.md`, `okf/wiki/log.md`, `okf/wiki/AGENTS.md`) and the small
number of repository-generated files without a more specific rule.

Maintenance note: `okf/wiki/` pages that synthesize external evidence must
stay short and paraphrased with a source citation, per the
`external-docs.md` rule bundled with `agent-ready-context` (avoid large
copied passages). This keeps the unlicensed scope accurate over time; if a
future page ever needs to hold a substantial third-party excerpt, add a
per-file entry to `THIRD_PARTY_NOTICES.md` documenting that source's own
licence rather than relying on this blanket note.

`okf/.openkb/hashes.json` and `okf/.openkb/config.yaml.example` are
operational integrity/config files, not wiki content, and are licensed
Apache-2.0 like other repository configuration (see above).

## Generated content

Files generated from original material (`AGENTS.md`, the OKF wiki
exception above, and Graphify's data/report outputs) carry the licence of
the original material they were generated from, per the same rule applied
throughout this document. Files that reproduce or embed third-party
material (`graphify-out/graph.html`) retain that material's licence
instead.

## Complete licence texts

Complete licence texts are available under [`LICENSES/`](LICENSES/):
`Apache-2.0.txt`, `CC-BY-4.0.txt`, `MIT.txt`, and
`LicenseRef-All-Rights-Reserved.txt` (the custom, non-SPDX-standard
declaration used for the `okf/` carve-out above — not to be confused with
the SPDX `Unlicense`, which is a public-domain dedication and means the
opposite).

The root [`LICENSE`](LICENSE) contains the Apache License 2.0 text for
conventional GitHub licence detection. It does not override the explicit
CC-BY-4.0, third-party, or unlicensed assignments described above.
