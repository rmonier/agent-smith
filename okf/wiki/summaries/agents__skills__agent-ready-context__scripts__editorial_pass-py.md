---
type: "Summary"
description: "Script for safe editorial curation briefings and deterministic diff checks."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"
---

# .agents/skills/agent-ready-context/scripts/editorial_pass.py

This script supports the guarded class-3 editorial curation pass for OpenKB wiki maintenance. It has two main modes: `--brief`, which prints a pre-edit briefing for the editing agent, and `--check`, which validates a completed curation diff without using an LLM.

## Purpose

The script exists to make last-resort hand edits safer by enforcing the same whitelisting and structural expectations used by the installed OpenKB toolchain, while also adding repository-specific policy checks that OpenKB does not cover directly.

## Main responsibilities

- Generates a briefing that includes the current valid wikilinks targets.
- Tries to use OpenKB's private compiler whitelist template, then falls back to a mirrored copy if needed.
- Verifies curation diffs against a git base, defaulting to `HEAD`.
- Enforces scope rules so only compiled knowledge pages and the root index can change.
- Checks provenance continuity by comparing `sources:` values before and after the edit.
- Delegates structural validation to the installed OpenKB `openkb.lint` API.

## Key concepts

### wikilinks whitelist
The briefing uses OpenKB's list of existing wiki targets as the authoritative set of allowed links. If the private compiler template cannot be imported, the script falls back to a mirrored template captured from OpenKB 0.4.4.

### provenance preservation
For changes under `wiki/concepts/` and `wiki/entities/`, the union of all `sources:` entries must remain unchanged across the diff. This reflects the rule that merges may combine source lists, but may not invent or lose sources.

### scope control
The check mode allows only the following locations to change during curation:

- `wiki/concepts/`
- `wiki/entities/`
- `wiki/index.md`

Everything else under the knowledge base root is treated as out of scope.

### vendor integration
The script executes OpenKB's installed Python environment directly through `uv tool dir`, ensuring that checks run against the pinned vendor code rather than a reimplementation.

## `--brief`

The briefing mode:

- loads the installed OpenKB wiki target list
- renders the vendor's whitelist middleware if possible
- falls back to `_MIRRORED_KNOWN_TARGETS_USER` when private internals drift
- prints curation rules for the editing agent before any manual change

This makes the prompt context deterministic and aligned with the current wiki state.

## `--check`

The verification mode performs these checks:

- detects changed files relative to the selected git base
- flags edits outside the allowed curation scope
- blocks new compiled pages unless explicitly approved with `--allow-new-pages`
- compares aggregated `sources:` sets before and after the edit
- rejects changed concept/entity pages that end up without a non-empty `sources:` list
- runs vendor lint checks for broken links, index sync, orphans, invalid frontmatter, and missing OKF fields

It also filters a documented false positive by ignoring orphan findings under `reports/`.

## Error handling and stability

The script distinguishes between two failure classes:

- environment problems, which return exit code `2`
- policy or content violations, which return exit code `1`

The public `openkb.lint` functions used by `--check` are treated as stable. By contrast, the private compiler template used for `--brief` is explicitly fragile, so any import or formatting failure only downgrades the wording of the briefing, not the correctness of validation.

## Notable implementation details

- Uses `git diff`, `git status`, and `git archive` to inspect curation changes efficiently.
- Reads frontmatter with `pyyaml` and extracts `sources:` values from Markdown pages.
- Normalizes command execution to UTF-8 so vendor output is handled consistently on Windows and Unix.
- Treats untracked pages as additions during diff inspection, which matches working-tree curation workflows.

## Related ideas

- [[concepts/provenance-tracking]]
- wiki link policy
- [[concepts/deterministic-validation]]
- [[concepts/editorial-curation-passes]]

## Related Concepts
- [[concepts/vendor-backed-validation]]
- [[concepts/provenance-union-governance]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/wikilink-integrity]]
- [[concepts/frontmatter-metadata]]
- [[concepts/conservative-document-merging]]
- [[concepts/source-provenance]]
- [[concepts/generated-content-governance]]
- [[concepts/okf-wiki-governance]]
- [[concepts/quality-gates]]
- [[concepts/read-only-kb-operations]]

## Entities
- [[entities/editorial_pass-py]]
- [[entities/openkb-lint]]
- [[entities/openkb-agent-compiler]]
- [[entities/pyyaml]]
- [[entities/uv]]
- [[entities/openkb]]
- [[entities/openkb-cli]]
- [[entities/validate_okf_bundle-py]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki]]
- [[entities/git]]
- [[entities/okf-wiki-agents-md]]
- [[entities/okf-wiki-tooling]]
- [[entities/openkb-wiki]]
- [[entities/references-official-okf-spec-web-check-md]]
