---
type: "source-file"
title: ".agents/skills/subagent-profile-adapter/references/tooling-context-policy.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/subagent-profile-adapter/references/tooling-context-policy.md"
source_path: ".agents/skills/subagent-profile-adapter/references/tooling-context-policy.md"
source_kind: "markdown"
source_hash: "sha256:ecab319a681b4a5e40c198275c1e4f216464c94fed807ba72f0f5a1804c3d7ff"
source_commit: "9b3f3ff908957a34a8e9fa6e5d402f659cd02cba"
tags: [source-file, markdown]
---

# .agents/skills/subagent-profile-adapter/references/tooling-context-policy.md

~~~
# Tooling context policy

Harness documentation and runtime adapter knowledge live inside OKF in exactly two cases:

1. **Harness build record (required verdict, best-effort record).** Every agent-ready build or refresh pass records the harness that performed it in `okf/wiki/tooling/harnesses/<harness>.md`: harness name and version, how it was identified (see `references/runtime-detection.md`), the date of the pass, and any harness-specific operational quirks observed while running the pipeline (sandbox constraints, background-task behavior, timeout needs). If the executing agent writes no record, its run report must say why explicitly — a silent skip is indistinguishable from a forgotten step. The record itself is never a gate: when the active harness cannot be determined reliably (the don't-guess rules in `references/runtime-detection.md`), skip the record, state that in the run report, and continue the pipeline. The record is the seed of the fuller harness page below.
2. **Adapter/profile tooling context (opt-in).** Fuller harness documentation, only when this skill is actively used for a detected or user-selected harness.

Do not accumulate speculative tooling pages beyond these two cases.

## Location

When needed, use:

```text
okf/wiki/tooling/
├── index.md            committed navigation stub (see "Git scope" below)
├── harnesses/
│   └── <harness>.md    one page per harness a user runs
└── providers/
    └── <provider>.md   optional: provider/model runtime observations
```

This location is a hand-authored OpenKB wiki exception, not a separate storage system. It remains valid only if every non-reserved `.md` file has OKF frontmatter and `type`.

Declare the custom `tooling/` section in `okf/wiki/AGENTS.md`, OpenKB's on-disk wiki-conventions manual. Edit that file only with user consent and keep the declaration when OpenKB regenerates conventions. Do not ingest tooling pages through `openkb add`; they are not source material for project knowledge.

Do not create additional non-standard folders under `.agents/` for tooling context.

## Git scope: local by default

Tooling context is **user-scoped**: it describes the environment of whoever runs the agent (harness, models, providers), not the project, and it does not version with the repository — the same boundary that keeps it out of ingestion. Default git scope, via `.gitignore` (every contributor generates build records, so this is the shared-ignore case of `references/git-tracking-policy.md`, not `.git/info/exclude`):

```gitignore
okf/wiki/tooling/*
!okf/wiki/tooling/index.md
```

The one committed artifact is the **navigation stub** `okf/wiki/tooling/index.md` — the same pattern as the committed `config.yaml.example` anchoring the local provider config. The stub is deliberately **user-neutral**: it names no harness, model, or user, so committing it requires no consent — per-user uniqueness lives entirely in the local pages, and consent rules apply to committing those. It cannot be local itself: the bundle-root `index.md` is committed and machine-managed, so its tooling entry must resolve on every clone, and the stub is that stable target (a local-only stub would leave every other clone with a dangling reference — the incoherence this design exists to prevent). Create it, together with the labeled bundle-root index entry, the first time any tooling content exists; both are committed, everything else under `tooling/` stays local. Example stub:

```markdown
# Tooling context (user-scoped)

Hand-authored harness/runtime context. Pages here are local by default and
differ per user and clone; list this directory to see what exists locally.
Project pages never link here.

* [Root index](../index.md)
```

Rules that keep every clone coherent:

- **Never enumerate local pages in committed index files** (neither the stub nor the bundle root): the entries would dangle on other clones and dirty the worktree. Local pages are discovered by listing the directory — the stub says so.
- Any harness/provider mix works without committed churn: one `harnesses/<harness>.md` per harness, optional `providers/<provider>.md` pages, all local — nothing committed enumerates the overlay, so nothing goes stale.
- Do not leave a local tooling page with no `[[wikilinks]]`: OpenKB defines that page as an orphan because committed indexes intentionally cannot enumerate it. Give every local page at least one valid outgoing wikilink to durable project knowledge (for example `[[index|Project knowledge index]]`); tooling-to-project is allowed and keeps lint clean without committing local navigation.
- Teams that standardize on a harness may opt into committing specific tooling pages — ask first, same consent rule as `references/git-tracking-policy.md`.
- OKF compliance holds on every clone: the committed tree and the committed-plus-local overlay are each a valid bundle (the spec allows arbitrary subdirectories and index files in any directory), and committed content never links to local pages, so wikilink integrity never breaks for another user.

## Required semantics

Tooling pages describe interchangeable harness behavior, not project truth.

Recommended frontmatter:

```yaml
---
type: tooling-context
scope: tooling
title: <Harness> harness context
resource: <official-doc-url-or-local-doc-reference>
tags: [tooling, harness, subagents]
timestamp: <UTC timestamp>
link_policy: tool-to-project-only
---
```

## Link direction

Allowed:

```text
okf/wiki/tooling/harnesses/<harness>.md -> AGENTS.md
okf/wiki/tooling/harnesses/<harness>.md -> .agents/skills/
okf/wiki/tooling/harnesses/<harness>.md -> okf/wiki/<project-page>.md
okf/wiki/index.md (bundle root) -> okf/wiki/tooling/          # required navigation entry, see below
okf/wiki/log.md (bundle root) -> mentions of tooling updates
```

Forbidden:

```text
okf/wiki/<project-concept-page>.md -> okf/wiki/tooling/harnesses/<harness>.md
okf/wiki/<subdir>/index.md -> okf/wiki/tooling/
AGENTS.md -> long tooling explanations
```

`AGENTS.md` may mention that harness-specific profile adapters can exist, but it should not depend on specific tooling docs.

## Required root index entry

OKF navigation must enumerate the bundle: a `tooling/` subtree that no index references breaks progressive disclosure and effectively hides part of the bundle from spec-driven consumers. So whenever `okf/wiki/tooling/` contains non-reserved pages, the bundle-root `okf/wiki/index.md` **must** list it — as an explicitly labeled outsider, so agents index it without treating it as project truth:

```markdown
## Tooling context (harness-specific — do not treat as project truth)

* [Tooling](tooling/index.md) - User-scoped runtime/harness context, local by default. Project concept pages must not depend on it.
```

The entry points at the committed stub, never at individual pages — local pages do not exist on other clones, so the stub is what keeps this reference resolving everywhere.

This is the only place project-side navigation may point at tooling. Root `index.md` and root `log.md` are reserved navigation/history files, so these references do not create a project-to-tooling dependency; concept pages and subdirectory indexes must still never link into `okf/wiki/tooling/`.

## Validation

Run:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .
```

The validator fails if project OKF concept pages link back to `okf/wiki/tooling/`, if `okf/wiki/tooling/` has pages that the bundle-root `index.md` does not reference, or if tooling pages exist without the committed `tooling/index.md` navigation stub.
It also fails when a non-reserved local tooling page has no outgoing `[[wikilink]]`, because that state is guaranteed to appear as an OpenKB orphan while local pages remain correctly absent from committed indexes.


## Default artifact rule

Baseline agent-ready bootstrap creates under `okf/wiki/tooling/` only the minimal harness build record (case 1 above) plus, on first use, the committed `tooling/index.md` stub and the bundle-root index entry. Runtime hint JSON files and policy output text files remain diagnostic outputs for the POC or explicit subagent-profile-adapter runs: print them to the terminal, write them to a temporary path, or save them only if the user requests an audit artifact.
~~~
