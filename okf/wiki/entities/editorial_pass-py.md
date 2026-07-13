---
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"]
type: "Work"
description: "OpenKB script for guarded editorial curation passes"
---

# editorial_pass.py

`editorial_pass.py` is an OpenKB repository script that supports the guarded class-3 editorial curation pass for wiki maintenance. It is designed to make manual knowledge-base edits safer by combining vendor-backed checks with repository-specific policy enforcement.

## What it does

The script has two primary modes:

- `--brief` prints a pre-edit briefing for the editing agent before any curation work begins.
- `--check` verifies a completed curation diff deterministically and without using an LLM.

It exists as a last-resort maintenance path for output-only semantic-lint problems when the normal correction loop and findings workflow do not apply.

## Key responsibilities

- Loads the installed OpenKB tool environment and runs its lint machinery directly.
- Produces the current valid wikilink target whitelist for the editing agent.
- Falls back to a mirrored OpenKB compiler template when private internals are unavailable.
- Validates that curation changes stay within allowed scope.
- Enforces provenance continuity through `sources:` union checks.
- Requires vendor structural checks to pass, including broken-link and frontmatter validation.
- Supports a deterministic, guarded hand-edit path for compiled output-only cleanup when no source correction fits.
- Encodes repository policy that `okf/wiki/` is the durable context source of truth, while `AGENTS.md` stays an orientation layer rather than a long-form knowledge store.
- Reflects the broader OKF pipeline where repository evidence is staged under `okf/.okf-build/input/` and ingested instead of editing generated pages directly.
- Reinforces the distinction between skills as repeatable actions, OKF wiki as context, and `AGENTS.md` as navigation and best-practice guidance.

## Validation model

`--check` combines two layers of verification:

- **Vendor checks** via `[[entities/openkb-lint]]` functions such as broken-link detection, orphan detection, index synchronization, invalid frontmatter checks, and missing OKF field checks.
- **Policy checks** implemented in the script itself, including scope restriction, new-page approval, provenance preservation, and non-empty `sources:` requirements.

This makes the script a [[concepts/deterministic-validation]] tool for [[concepts/editorial-curation-passes]]. It also depends on the larger [[concepts/okf-wiki-governance]] model that keeps compiled pages under tight review.

## Curation rules encoded in the script

The script treats curation as a narrow maintenance task, not a place to add new knowledge. It enforces these ideas:

- Only `wiki/concepts/`, `wiki/entities/`, and `wiki/index.md` may change during curation.
- New compiled pages require explicit approval through `--allow-new-pages`.
- The union of source citations across compiled pages must not change.
- Every changed concept or entity page must still have a non-empty `sources:` list.
- The root index must stay in sync with page additions, deletions, and merges.
- Repository-local knowledge should continue to flow through staged source packs and OpenKB ingestion rather than direct edits to compiled output.

These rules align with [[concepts/provenance-union-governance]], [[concepts/quality-gates]], and [[concepts/read-only-kb-operations]].

## Vendor integration and fallback behavior

The script relies on the installed OpenKB environment rather than reimplementing OpenKB behavior. It tries to use OpenKB's private compiler whitelist template for briefing output, but if that fails it degrades gracefully to a mirrored copy captured from OpenKB 0.4.4.

That fallback affects only the wording of the briefing, not the correctness of `--check`.

## Error handling

The script distinguishes between:

- exit code `0` for success
- exit code `1` for content or policy violations
- exit code `2` for environment failures

This is a clear example of [[concepts/graceful-degradation]] combined with strict validation boundaries.

## Relationship to the broader agent-ready workflow

Within the larger agent-ready repository workflow, `editorial_pass.py` is the special-purpose tool for semantic-lint exceptions that are purely about output curation. It sits alongside the standard OKF pipeline of source staging, ingestion, linting, and validation, but it does not replace the normal correction loop or findings capture process.

It supports the broader repository workflow described in [[summaries/agents__skills__agent-ready-context__SKILL-md]], including deterministic source-pack staging, validation of compiled output, and the separation between action skills, context, and orientation.

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[entities/openkb]]
- [[entities/openkb-lint]]
- [[entities/uv]]
- [[concepts/editorial-curation-passes]]
- [[concepts/deterministic-validation]]
- [[concepts/provenance-tracking]]
- [[concepts/wikilink-integrity]]
- [[concepts/okf-wiki-governance]]
- guarded editorial pass

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]]

See also: [[summaries/README-md]]