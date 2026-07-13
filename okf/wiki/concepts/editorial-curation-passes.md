---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"]
description: "Guarded manual wiki edits that preserve scope, provenance, and validation."
---

# Editorial Curation Passes

An editorial curation pass is a controlled, last-resort manual edit workflow for a compiled wiki. It is used when normal automation does not cover a needed change, such as a merge, split, or consolidation that must be applied directly to the knowledge base while still preserving validation, provenance, and index consistency.

This concept is implemented by [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]], which provides a briefing mode for pre-edit context and a check mode for post-edit verification.

## Core purpose

Editorial curation passes exist to make hand edits safer and more deterministic. They are not a general-purpose editing path; they are a guarded maintenance path for structural knowledge-base changes.

The workflow emphasizes:

- deterministic validation of the completed diff
- provenance tracking through source-list preservation
- wiki review gates before changes are accepted
- read only kb operations for the standard linting path, with curation as a special exception

## What the pass allows

The curation pass is intended for:

- merging pages
- splitting pages when a new compiled page is pre-approved
- reorganizing or tightening existing compiled content
- rewiring links after a merge or delete
- updating the root index to match the new page graph

The script explicitly treats this as curation only: no new knowledge should be introduced through the pass. New knowledge belongs in [[concepts/findings]] and the findings-promotion workflow instead.

## Scope boundaries

The check phase enforces a narrow edit scope. Under the KB root, only these paths may change:

- `wiki/concepts/`
- `wiki/entities/`
- `wiki/index.md`

Everything else is out of bounds for curation, including source material, summaries, logs, tooling, and other repo-maintained channels. This reflects knowledge boundaries and tooling boundaries between compiled wiki maintenance and other repository functions.

## Provenance rules

A central rule of editorial curation is that source provenance must be preserved, not invented.

For changed concept and entity pages, the union of all `sources:` values before the edit must match the union after the edit. In practice, this means:

- merges may combine source lists
- no source citation may be lost
- no new provenance may be fabricated
- every changed concept/entity page must retain a non-empty `sources:` list

This is a concrete application of provenance union governance and source provenance.

## Validation behavior

The script combines vendor checks with local policy checks.

Vendor checks, executed by the installed OpenKB environment, include:

- broken link detection
- index synchronization checks
- orphan detection
- invalid frontmatter detection
- missing OKF field detection

Local checks add repository policy constraints such as:

- scope validation
- provenance-union comparison
- new-page approval via `--allow-new-pages`

This makes the pass part of deterministic validation and vendor backed validation, while still keeping the policy specific to the wiki's curation rules.

## Briefing mode

Before editing, the script prints a briefing that:

- lists all currently valid wikilink targets
- uses the vendor's own whitelist middleware when available
- falls back to a mirrored template if private vendor internals drift
- reminds the operator of the curation rules

That briefing supports wikilink integrity, confidence calibration, and progressive disclosure by surfacing only the allowed targets and the rules for using them.

## Check mode

After editing, the script verifies the diff against a git base, defaulting to `HEAD`.

It checks for:

- out-of-scope file changes
- unauthorized new compiled pages
- lost or invented provenance
- empty `sources:` lists on changed compiled pages
- structural wiki errors reported by the vendor lint API

The pass returns clear exit codes:

- `0` for success
- `1` for policy or content violations
- `2` for environment failures

## Why this matters

Editorial curation passes protect compiled knowledge from accidental drift. They create a controlled lane for manual restructuring while preserving the wiki's structural rules, source accountability, and link integrity. In that sense, they sit at the intersection of graph merging, rename vs delete detection, and knowledge graph feedback loops.

They are especially important in workflows where automated compilation is strong but not complete, and where a human must still intervene without breaking the compiled knowledge base.