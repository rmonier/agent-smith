---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md"]
description: "Deterministic transformation of names into stable, policy-safe canonical forms."
---

# Naming Normalization

Naming normalization is the practice of transforming user-provided or source-provided names into a predictable canonical format before those names are used in files, directories, identifiers, graph nodes, or generated content. It reduces ambiguity, prevents invalid outputs, and helps automation produce consistent results across repeated runs.

## Why it matters

Normalized naming supports reliable scaffolding, extraction, and validation workflows. When tools accept free-form titles, labels, paths, or symbol names, they need a stable way to derive filesystem-safe and policy-compliant outputs. This improves repeatability, lowers the chance of malformed paths or duplicate records, and makes generated artifacts easier to discover and manage.

This is especially relevant to [[concepts/project-scaffolding]], where a tool may create directories and template files directly from user input. It also complements [[concepts/filesystem-validation]] by ensuring names are cleaned before they become part of the filesystem. In graph-building workflows, normalization also protects against unstable identifiers by making the same source entity resolve to the same canonical name every time, which supports [[concepts/idempotent-graph-import]] and [[concepts/incremental-graph-maintenance]].

## Example from the source

[[summaries/agents__skills__skill-creator__scripts__init_skill-py]] shows naming normalization in a skill initialization script. The script accepts a skill name or title from the command line, then converts it into a kebab-case directory name before creating the new skill.

The normalization flow in that source includes:

- trimming surrounding whitespace
- converting all characters to lowercase
- replacing non-alphanumeric runs with hyphens
- collapsing repeated hyphens into a single hyphen
- stripping leading and trailing hyphens
- truncating the result to 64 characters

After normalization, the script validates the result with a strict pattern so the final name:

- starts with a lowercase letter or digit
- ends with a lowercase letter or digit
- contains only lowercase letters, digits, and hyphens internally
- does not contain double hyphens

If the normalized value is empty or invalid, the script exits instead of creating files. This ties naming normalization directly to [[concepts/deterministic-validation]] and [[concepts/quality-gates]].

The same script also uses the normalized name as the basis for multiple outputs: the skill directory path, the generated `SKILL.md` metadata `name` field, and the rendered title in the initial Markdown file. That reuse makes normalization part of the scaffold's internal consistency rather than just an input-cleaning step. The script also constrains its parent path to `.agents/skills`-scoped locations and supports a limited set of resource subdirectories (`scripts`, `references`, and `assets`), showing how normalized names often sit alongside path safety and controlled scaffolding rules.

A second example appears in [[summaries/agents__skills__graphify__references__extraction-spec-md]], where graph extraction node IDs must be normalized into lowercase identifiers containing only `[a-z0-9_]`. In that specification, the ID is built from the full repo-relative path with the extension removed, plus a normalized entity name, with non-alphanumeric characters replaced and every directory segment preserved. The spec explicitly forbids chunk-number suffixes or other unstable additions, because such variations create duplicate or orphaned nodes during rebuilds. Here, naming normalization is not just about path safety; it is a control for stable graph identity and source provenance.

## What this enables

A normalized name becomes a dependable input for downstream automation. In the skill scaffold source, the canonicalized name is reused for:

- the skill directory path
- the generated `SKILL.md` metadata `name` field
- the human-readable title derived from the normalized slug

In the graph extraction specification, the canonicalized form is reused for:

- deterministic node IDs
- alignment between semantic extraction and AST extraction
- replacement matching during incremental re-extraction
- prevention of ghost duplicates caused by inconsistent ID formats

Because the same canonical name is used throughout, the scaffold remains internally consistent and the graph remains mergeable across runs. That consistency supports [[concepts/source-driven-regeneration]], [[concepts/incremental-compilation]], and [[concepts/provenance-tracking]].

## Design characteristics

Good naming normalization usually balances flexibility at input time with strictness at output time.

Key characteristics include:

- accepting messy human input but producing one stable result
- constraining characters to a known-safe subset
- applying deterministic transformations in a fixed order
- preserving enough source structure to keep same-named items distinct
- validating the final form after transformation, not just before
- enforcing length or format limits when names are used in paths or identifiers
- refusing unstable suffixes or ad hoc variations that break identity across runs

The graph extraction spec adds an important design lesson: normalization must fit the identity model of the system, not just its syntax rules. Using only a filename or only the immediate parent directory may produce a valid-looking ID, but still be semantically wrong if different files collapse into the same normalized name. In practice, normalization is often paired with refusal behavior: if the canonical output still fails policy checks, the tool should stop rather than guess. That pattern keeps tool behavior explicit and predictable, aligning with [[concepts/tool-boundaries]].

## Relationship to other concepts

- [[concepts/project-scaffolding]]: scaffolding tools often derive directories and template content from normalized names.
- [[concepts/filesystem-validation]]: normalized names help ensure generated paths are safe and acceptable.
- [[concepts/deterministic-validation]]: the same input should normalize and validate the same way every time.
- [[concepts/quality-gates]]: invalid names are blocked before file creation or extraction proceeds.
- [[concepts/document-normalization]]: both concepts emphasize canonical forms, though naming normalization focuses on identifiers and path-safe labels rather than whole documents.
- [[concepts/idempotent-graph-import]]: stable normalized IDs help repeated imports update existing graph elements rather than creating duplicates.
- [[concepts/incremental-graph-maintenance]]: deterministic naming is necessary for correct replace-on-re-extract behavior.
- [[concepts/source-provenance]]: normalized identifiers work best when they preserve meaningful source structure such as full paths.
- [[concepts/skill-scaffolding]]: skill bootstrap flows depend on normalized names to create consistent directory and file layouts.
- [[concepts/path-safety]]: normalization reduces the risk that user input turns into invalid or unsafe filesystem paths.

## Practical takeaway

Naming normalization is a small but foundational control in automation systems. The skill initialization script in [[summaries/agents__skills__skill-creator__scripts__init_skill-py]] demonstrates the classic pattern: normalize first, validate the normalized result, and only then use the name to create durable project structure. The graph extraction prompt in [[summaries/agents__skills__graphify__references__extraction-spec-md]] extends the same principle to graph identity: normalize names in a deterministic, structure-preserving way so the same entity resolves to the same identifier regardless of when or where it is processed.

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]