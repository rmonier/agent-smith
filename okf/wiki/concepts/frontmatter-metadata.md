---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md"]
description: "Structured header metadata used for validation, provenance, and identity."
---

# Frontmatter Metadata

Frontmatter metadata is a structured header block at the start of a document that carries compact, machine-readable fields such as identity, description, resource references, provenance, and compatibility information. It gives tools a stable place to read document facts before trusting the body text, and it is a core part of the embedded OKF conformance model.

This concept appears directly in skill validation workflows, where validators read frontmatter in `SKILL.md` and use it as the authoritative source for repository checks. The `quick_validate.py` script is a clear example: it parses a simple YAML-like header, extracts `name`, `description`, and optional `compatibility`, and then compares that metadata against the filesystem layout of the skill directory. Frontmatter also underpins the OpenKB wiki model, where non-reserved Markdown files must have parseable YAML frontmatter, concept pages must declare a non-empty `type`, and curated pages often preserve a machine-managed `sources:` list as part of provenance tracking.

Frontmatter also matters in guarded editorial curation. The `editorial_pass.py` script treats machine-readable metadata as part of the edit contract: it checks that changed concepts and entities keep a non-empty `sources:` list, rejects invented provenance, and uses frontmatter parsing to compare provenance across the before and after states. In that workflow, metadata is not just descriptive; it is part of the safety boundary around [[concepts/editorial-curation-passes]], [[concepts/provenance-tracking]], and [[concepts/generated-content-governance]].

The OpenKB bundle validator adds a broader view of the same contract. `summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py` treats frontmatter as the first line of structural validation for an entire bundle: it requires parseable YAML on every non-reserved Markdown file, enforces a non-empty `type` on concept pages, allows `okf_version` only at the root `index.md`, and warns when generated concept or entity pages are missing the machine-managed `sources:` list that preserves provenance. In OpenKB wiki mode, frontmatter-based page identity also helps separate compiled content from operational areas like `AGENTS.md`, `sources/`, and `reports/`.

## What frontmatter metadata does

Frontmatter metadata separates core descriptive fields from the main body text so tooling can:

- identify a document or package by name
- enforce required fields
- apply length and format constraints
- compare declared metadata to filesystem state
- fail fast when structural expectations are not met
- distinguish reserved navigation files from concept pages
- attach provenance, resource, and tag information for ingestion pipelines
- preserve machine-managed links to source documents and bundles
- support bundle-level validation before body text is trusted

In this role, frontmatter acts as a lightweight contract between human-authored documentation and automated validation, making it a practical foundation for [[concepts/executable-validation]], [[concepts/quality-gates]], [[concepts/deterministic-validation]], and [[concepts/filesystem-validation]]. It also supports the broader idea of metadata as a machine-readable interface for knowledge bundles.

## Role in validation scripts

In `summaries/agents__skills__skill-creator__scripts__quick_validate-py`, the script parses a YAML-like frontmatter block from `SKILL.md` and extracts simple key-value pairs. The metadata then drives several checks:

- `name` is required
- `description` is required
- `compatibility` is optional but length-limited
- `name` must satisfy formatting constraints
- the directory name must match the frontmatter `name`
- the skill must live under `.agents/skills`
- `scripts`, `references`, and `assets` must be directories if they exist

This makes frontmatter more than descriptive annotation: it becomes the input to filesystem-oriented validation and path-based consistency checks. The same pattern appears in `summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py`, where reserved files, concept pages, and wiki metadata are distinguished by file location and parseable headers rather than by inference from body text.

That validator broadens the frontmatter contract beyond a single skill file. It requires parseable YAML on non-reserved Markdown files, enforces a non-empty `type` on concept documents, allows `okf_version` at the root `index.md`, and warns when generated concept or entity pages are missing the machine-managed `sources:` list that preserves provenance.

The validator also adds deterministic audit checks that are not part of the formal OKF spec but help catch damaged content. It warns on unclosed code fences at the end of a file, because that is a reliable signal of truncation or a bad merge, and it warns when sibling page names collapse to the same normalized slug, which often indicates near-duplicate concepts. These checks make frontmatter and file structure part of a broader integrity model rather than a narrow metadata parser.

The editorial curation pass adds a complementary check. `summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py` verifies completed diffs by combining vendor lint checks with git-based policy rules, including a requirement that every changed concept or entity page still carries a non-empty `sources:` list. It also parses frontmatter to compare provenance across the before and after states, so a merge can union source lists without losing citations or inventing new ones.

## Key properties

### Early-file placement

The scripts require frontmatter to begin at the top of the file and to include a closing delimiter. This reflects an important property of frontmatter metadata: it must be easy to find so tools can read it deterministically.

The OKF baseline extends this idea across the bundle: every non-reserved Markdown file must have parseable frontmatter, while `index.md` and `log.md` follow special reserved structures. That makes header parsing a prerequisite for dependable bundle traversal and policy enforcement.

### Compact schema

The scripts expect only a small set of fields and validate them with simple rules. This shows how frontmatter metadata often works as a schema-lite interface rather than a full data model. That supports predictable automation without requiring complex parsing infrastructure.

The OKF reference treats this compactness as a feature: unknown frontmatter keys are allowed, and the main requirement is a stable minimum contract that downstream tooling can rely on. In OpenKB, that contract often includes `type`, `sources`, and other machine-managed fields rather than a rigid exhaustive schema.

### Human and machine readability

The chosen format is easy for maintainers to edit and easy for tools to inspect. This balance is useful in repositories that emphasize lightweight authoring and fast checks, especially in [[concepts/skill-governance]] and [[concepts/project-scaffolding]].

In OpenKB-style wiki bundles, the same balance shows up in the split between summary pages, concept pages, and navigation pages. Frontmatter provides enough structure for validators and generators while keeping the body readable as normal Markdown.

## Validation behaviors tied to metadata

The source documents illustrate several common frontmatter-driven validation patterns:

- presence validation for required fields
- string-length limits for descriptive fields
- format validation for identifiers
- cross-checking metadata against directory naming
- rejecting malformed or unclosed header blocks
- requiring provenance fields on generated knowledge pages
- preserving source unions across merges and splits
- flagging missing bundle-level metadata when it is expected

The OKF baseline adds a related set of rules:

- parseable frontmatter is required on non-reserved Markdown files
- `type` must be present and non-empty on concept documents
- `index.md` and `log.md` are reserved filenames with special roles
- root and subdirectory index files have different structure expectations
- local validation may warn on missing optional metadata rather than failing immediately

The OpenKB wiki mode in the validator adds two especially important checks. First, broken wikilink targets are treated as structural errors, with link resolution matching page paths without extensions or bare stems. Second, missing `sources:` on generated concept and entity pages is treated as a warning because it signals a damaged or incomplete provenance chain. Together, these checks make metadata part of [[concepts/wikilink-integrity]] and [[concepts/provenance-tracking]], not just page description.

The validator also adjusts its behavior for OpenKB's operational layout. `AGENTS.md`, `sources/`, and `reports/` are skipped because they are infrastructure and evidence areas rather than compiled wiki content. That boundary preserves frontmatter validation for pages that are meant to behave like knowledge artifacts while avoiding false failures in operational files. The script also degrades gracefully when PyYAML is unavailable, reporting that YAML parseability cannot be fully checked instead of silently pretending validation succeeded.

The editorial pass sharpens that idea further by treating scope and provenance as diff-level invariants. Its `--check` mode only permits changes to concepts, entities, and the root index; it rejects edits elsewhere in the KB root; and it compares the union of source citations before and after the edit. That makes frontmatter part of a broader curation workflow rather than a standalone file format rule.

These patterns support deterministic validation by making checks depend on explicit, inspectable inputs rather than inference from free-form content.

## Why it matters

Frontmatter metadata gives repositories a stable place to declare operational facts about a document or package. When validation tools trust these fields, they can provide quick feedback and catch common problems before deeper automation runs.

In the skill validation case, frontmatter metadata helps ensure that a skill is:

- named consistently
- described clearly
- constrained to accepted formats
- positioned for downstream tooling

In the OKF case, frontmatter metadata also helps ensure that wiki pages are classifiable, indexable, and safely processable in offline workflows. That strengthens [[concepts/skill-based-automation]] and [[concepts/agent-ready-repositories]] by making each page or skill directory self-describing in a way that both humans and scripts can use.

It also supports [[concepts/okf-validation]], [[concepts/okf-workflow-governance]], and [[concepts/generated-content-governance]] by preserving the distinction between authored text and machine-managed page identity. A page with valid frontmatter can be validated, linked, and traced more reliably than a page whose metadata is missing or inconsistent.

The editorial curation pass shows why this matters operationally. Its workflow depends on metadata staying stable through merges and consolidations: source lists must be unioned, deleted pages must be rewired in the index, and changed pages must remain parseable. Frontmatter is therefore part of both content governance and change safety.

The bundle validator reinforces the same point at repository scale. By combining reserved-file handling, root-index exceptions, provenance warnings, and link-resolution checks, it treats frontmatter as part of the graph structure of the wiki rather than as decorative document metadata. That makes the page graph more trustworthy for later ingestion, regeneration, and review.

## Limits and tradeoffs

The source script uses a minimal parser rather than full YAML support. That reveals a recurring tradeoff in frontmatter metadata systems:

- simpler parsers are easier to maintain and run
- stricter assumptions improve predictability
- reduced parser complexity may reject or ignore richer YAML constructs

The OKF baseline leans into the same tradeoff. It tolerates unknown frontmatter keys, but it still requires parseable headers for conformance. In practice, that keeps the contract narrow enough for offline validation while still allowing enough metadata to support provenance, resources, tags, and bundle-specific workflow checks.

The OpenKB mode also shows a pragmatic boundary: frontmatter is central for compiled concept and entity pages, but operational areas like `AGENTS.md`, `sources/`, and `reports/` are excluded from wiki validation. That preserves a clear separation between content governance and tooling artifacts.

The editorial pass reflects a related asymmetry. It relies on the installed OpenKB package for vendor checks, but it treats some private compiler internals as best-effort only. If a private whitelist template moves, the script falls back to a mirrored copy rather than failing the curation check. That keeps the validation path strict while allowing briefing text to degrade gracefully.

## Related pages

- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[concepts/executable-validation]]
- [[concepts/filesystem-validation]]
- [[concepts/path-based-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/quality-gates]]
- [[concepts/skill-governance]]
- [[concepts/skill-based-automation]]
- [[concepts/okf-validation]]
- [[concepts/reserved-wiki-files]]
- [[concepts/document-normalization]]
- [[concepts/generated-content-governance]]
- [[concepts/wikilink-integrity]]
- [[concepts/provenance-tracking]]
- [[concepts/editorial-curation-passes]]
- [[concepts/provenance-union-governance]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__openkb__references__wiki-schema-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]