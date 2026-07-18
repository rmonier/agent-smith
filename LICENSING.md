# Licensing

`agent-smith` contains material under multiple licences, applied by file
according to its nature and origin — this is scope licensing, not ordinary
dual licensing. A given original Markdown file is under CC-BY-4.0. A given
original Python file is under Apache-2.0. Recipients are not offered a
choice between licences for the same file.

## Original material

Unless otherwise indicated below:

- Original Python and other executable source code — the scripts under each
  of the three product skills' `scripts/` directories and the repository's
  `tests/` — is licensed under the Apache License 2.0 (`Apache-2.0`).
- Original agent-skill instructions, documentation, specifications,
  examples, references, and other original Markdown content — including
  `README.md`, `AGENTS.md`, and the three product skills' `SKILL.md` and
  `references/` — are licensed under Creative Commons Attribution 4.0
  International (`CC-BY-4.0`).
- Repository operational configuration (`CITATION.cff`, `.gitignore`,
  `.gitattributes`) and the skills' functional template assets — files a
  target repository copies as working configuration rather than prose
  (`okf-validate.ci.yml`, `gitattributes.template`,
  `skill-lock.example.json`) — are licensed under Apache-2.0.

Copyright © 2026 [Romain Monier](https://github.com/rmonier).

Project source: [`agent-smith`](https://github.com/rmonier/agent-smith).

## Third-party and adapted material

- `.agents/skills/skill-creator/SKILL.md` — original overall, but
  incorporates a small number of closely adapted passages from
  Apache-2.0-licensed upstream `skill-creator` skills; see
  [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

OpenWiki and markitdown are each a separately installed runtime dependency,
not vendored or patched project source. Agent-smith's integration scripts
(including `prepare_external_evidence.py`, which invokes the pinned
markitdown CLI via subprocess and never bundles its source) remain original
Apache-2.0 project code.

File-level copyright and licence assignments are declared through
`REUSE.toml` (and, for the closely adapted passages above, plain-language
notes). Full third-party origin, revision, and modification information is
documented in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## The `okf/wiki/` knowledge base: unlicensed, not hidden

`okf/wiki/` (the OKF project wiki, maintained through OpenWiki) is internal
project context for contributors — orientation notes, cross-document
synthesis, and provenance — not part of the supported product surface
described in [`README.md`](README.md#the-skills).

These files are **not licensed for reuse**. They remain fully copyrighted
by Romain Monier with no licence granted beyond whatever limited rights
GitHub's own terms of service extend to viewing and forking a public
repository (see `LICENSES/LicenseRef-All-Rights-Reserved.txt`). This is
deliberate, not an oversight: being publicly visible in a cloned repository
and being *licensed for reuse* are different things, and this material —
generated commentary about the repository's own files, not a deliverable in
its own right — is the former without the latter.

Exception: `okf/wiki/INSTRUCTIONS.md` is a byte copy of the CC-BY-4.0
template shipped with `agent-ready-context`, and the copy keeps that open
licence via an explicit `REUSE.toml` override.

Maintenance note: `okf/wiki/` pages that synthesize external evidence must
stay short and paraphrased with a source citation, per the
`external-docs.md` rule bundled with `agent-ready-context` (avoid large
copied passages). This keeps the unlicensed scope accurate over time; if a
future page ever needs to hold a substantial third-party excerpt, add a
per-file entry to `THIRD_PARTY_NOTICES.md` documenting that source's own
licence rather than relying on this blanket note.

## Generated content

Files generated from original material (`AGENTS.md` and the OKF wiki
exception above) carry the licence of the original material they were
generated from, per the same rule applied throughout this document.

## Complete licence texts

Complete licence texts are available under [`LICENSES/`](LICENSES/):
`Apache-2.0.txt`, `CC-BY-4.0.txt`, and
`LicenseRef-All-Rights-Reserved.txt` (the custom, non-SPDX-standard
declaration used for the `okf/wiki/` carve-out above — not to be confused
with the SPDX `Unlicense`, which is a public-domain dedication and means the
opposite).

The root [`LICENSE`](LICENSE) contains the Apache License 2.0 text for
conventional GitHub licence detection. It does not override the explicit
CC-BY-4.0, third-party, or unlicensed assignments described above.
