---
type: Policy
title: OKF wiki preservation and maintenance contract
description: Rules that every wiki update must preserve; the binding agreement
  between automated producers and manual editors.
timestamp: 2026-07-19T11:42:15.000Z
sources:
  - /openwiki/INSTRUCTIONS.md
  - .agents/skills/agent-ready-context/scripts/run_openwiki_staged.py
  - .agents/skills/agent-ready-context/references/openwiki-lifecycle.md
  - .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py
  - tests/test_openwiki_adapter.py
---

# Wiki Preservation Contract

This is the binding agreement between automated memory producers (OpenWiki) and manual editors. Every update to `okf/wiki/` must preserve this contract byte-for-byte.

## What this contract protects

1. **Manual prose and caveats** — reviewed explanations, disclaimers, uncertainty markers survive across unrelated updates
2. **Formatting and structure** — intentional layout, lists, tables, emphasis remain unchanged
3. **Unknown metadata** — frontmatter keys beyond the standard schema are preserved
4. **Timestamp discipline** — an existing timestamp advances when body content changes and never changes independently; no-op updates are byte-identical
5. **Architecture integrity** — no subdirectory index.md; single root index.md routes to every page

## The producer's preservation obligations

When OpenWiki runs on updated repository source:

1. **Classify all Git changes** — added, modified, deleted, renamed, moved files
2. **Surgical regeneration** — touch only affected concept pages
3. **Don't rewrite the root** — never regenerate `index.md` or `quickstart.md` unless routing materially changed
4. **No analysis artifacts** — never use previously generated memory or analysis-tool reports as evidence; cite underlying sources instead
5. **No deleting for cleanliness** — preserve manual content that remains supported, even if it makes the bundle look less uniform

## The editor's update obligations

When you manually edit `okf/wiki/`:

1. **Edit one owning page per fact** — use cross-references instead of copying the same explanation
2. **Prefer enriching over creating** — add to an existing page rather than create overlapping new pages
3. **Organize by question/concern, not structure** — one page per domain or durable question, not per file/class/directory/function
4. **Ground every important claim** — cite evidence in frontmatter `sources` or `## Citations` section with repository-relative paths
5. **Mark uncertainty** — say when evidence is incomplete or contradictory; never invent a resolution
6. **Update surgically** — change only the pages affected by new evidence; review other pages for forward references

## Frontmatter requirements

Every non-reserved page must have valid YAML frontmatter:

```yaml
---
type: <required: Architecture|Workflow|Concepts|Policy|quickstart|etc.>
title: <required: concise page title>
description: <required: one-sentence summary>
sources: ["<staged-relative-path>", ...]
<any-other-keys>: <preserve unknown keys unchanged>
---
```

**Formatting requirement**: every value above must itself be valid YAML. Quote any string value — `title`, `description`, or any other field — that contains a colon, so it can never be misread as a nested mapping (an unquoted colon followed by a space fails the parse with `ScannerError: mapping values are not allowed here`, which then fails deterministic validation). Quoting the whole value in double quotes is always safe, even when only part of it needs it.

**Reserved files** (exempt from frontmatter/citations):
- `index.md` — bundle root, automatically managed
- `log.md` — OpenWiki run history, never hand-edited; the adapter may add deterministic frontmatter only in the isolated stage for producer compatibility, then strips it before candidate validation and promotion

**All other files** are knowledge pages and need frontmatter + citations.

## Citations requirements

Every non-reserved page must cite its evidence in one (or both) of these forms:

### Form 1: Frontmatter sources

```yaml
sources: ["README.md", "AGENTS.md", ".agents/skills/agent-ready-context/SKILL.md@line-range"]
```

### Form 2: Citations section

```markdown
## Citations

- `README.md` — project vision
- `AGENTS.md` — operational basics
- `.agents/skills/agent-ready-context/SKILL.md` — core pipeline
- `@commit` — add when provenance materially matters
```

### External evidence

Cite URLs with access date inline or under `## References`:

```markdown
- [Anthropic effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), accessed 2026-01-15
```

Never use external URLs as the only evidence in `## Citations` (which is for repository paths).

## What NOT to include

Never commit to `okf/wiki/`:

- Absolute machine paths or usernames
- Secrets, API keys, OAuth tokens, credentials
- Provider configuration settings
- Ignored producer state (`okf/.openwiki/` contents)
- Build caches or generated artifacts
- Old previously-generated memory or analysis reports

## Index and routing rules

**Single root index.md**
- Must route to every page (directly or transitively)
- Never create subdirectory index.md files
- When the mapped page set is unchanged, the adapter restores the accepted root index byte-for-byte instead of accepting producer regeneration churn

**Quickstart**
- Keeps compact onboarding route
- Links to full index and preservation contract
- Routes to deeper pages

**Tooling context**
- Optional, user-scoped local pages
- Listed only in tooling/index.md, not in root index
- Discovered by directory listing, never enumerated in parent index

## Update workflow

When updating the wiki in response to source changes:

1. **Start from the accepted wiki** — the version in `okf/wiki/` before your run
2. **Classify the Git changeset** — what was added, modified, deleted, renamed
3. **Identify impacted concepts** — which wiki pages explain those changes
4. **Edit only impacted pages** — review and update only affected concepts
5. **Update cross-references** — fix broken links, update callers/consumers
6. **Never regenerate unrelated pages** — leave pages whose source didn't change alone
7. **On source deletion** — remove only unsupported claims and dead routes; preserve manual prose that remains valid

## Timestamp discipline

- **Change body content** → advance an existing frontmatter timestamp to current time; never remove it
- **Unchanged body** → timestamp must remain unchanged, even when other metadata is reviewed
- **No-op edits** (format fix, link check, unknown key preservation) → output is byte-identical to input
- **Deterministic gate** — candidate mapping normalizes generated Markdown to LF, rejects a changed body with a missing, stale, or non-advancing existing timestamp, and rejects timestamp churn when the body is unchanged

## Contradiction resolution

When evidence contradicts prior claims:

1. State the contradiction explicitly
2. Cite both conflicting sources
3. Mark uncertainty with "✗ Unclear: evidence suggests X but previous notes claim Y"
4. Escalate to human review if resolution is ambiguous

Never silently replace manual prose with contradictory generated content.

## Reserved frontmatter keys

Standard OKF keys (preserve all):
- `okf_version` — OKF specification version
- `type` — content type/role
- `title` — page title
- `description` — one-line summary
- `sources` — YAML array of repository-relative citation paths

Custom namespaced keys are allowed (preserve unchanged):
- `x-manual: true` — marks manually maintained pages
- `sources-<language>: [...]` — language-specific citations
- Any `<key>: <string-value>` pair survives regeneration

## Quality gates

Before promoting any update:

1. **Validation**: `scripts/validate_openwiki_bundle.py --strict`
   - Frontmatter valid on all pages
   - Citations resolve to pre-run stage paths
   - No secrets, usernames, absolute paths
   - Generated Markdown uses LF and page timestamps follow body changes
   
2. **Semantic review**: Read all changed pages
   - Check claims against source evidence
   - Ensure caveats survived
   - Confirm no duplicates or vague names
   - Verify cross-references point to correct destinations

3. **Contract compliance**: Verify this contract is preserved byte-for-byte

Never weaken a quality gate to make a run pass.

## Citations

- `/openwiki/INSTRUCTIONS.md` — full scope contract (byte-for-byte source)
- `/.agents/skills/agent-ready-context/references/workflow.md` — automation lifecycle and review gates
- `/.agents/skills/agent-ready-context/references/openwiki-lifecycle.md` — reserved-file and index-preservation adapter behavior
- `/.agents/skills/agent-ready-context/scripts/run_openwiki_staged.py` — LF normalization and timestamp enforcement
- `/tests/test_openwiki_adapter.py` — regression coverage for preservation gates
- `/.agents/skills/agent-ready-context/scripts/validate_openwiki_bundle.py` — citation validation implementation
