---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md"]
description: "Converting names into stable kebab-case identifiers for skills and paths."
---

# Kebab-Case Normalization

Kebab-case normalization is the process of converting a human-facing name into a stable, lowercase, hyphen-separated identifier. In the skill initializer, it turns the user-provided skill name into the directory name used for the generated skill, helping keep names consistent, portable, and easy to validate.

## Why it matters

This kind of normalization reduces ambiguity between free-form titles and filesystem-safe identifiers. It supports [[concepts/naming-normalization]], [[concepts/path-safety]], and [[concepts/portable-skill-contract]] by ensuring that generated skill directories follow a predictable naming convention.

## How it works in the source script

The initializer in [[summaries/agents__skills__skill-creator__scripts__init_skill-py]] applies a small normalization pipeline:

1. Trim surrounding whitespace.
2. Convert the value to lowercase.
3. Replace runs of non-alphanumeric characters with `-`.
4. Collapse repeated hyphens into a single `-`.
5. Strip leading and trailing hyphens.
6. Truncate to 64 characters if needed, then strip trailing hyphens again.

The resulting name must also satisfy a regular expression constraint that allows only lowercase letters, digits, and hyphens, with length and boundary restrictions.

## Validation and constraints

Normalization is not treated as sufficient on its own. The script validates the final result before using it:

- The normalized name must not be empty.
- It must match the allowed pattern for skill names.
- It must not contain problematic repeated separators such as `--`.

This pattern reflects [[concepts/deterministic-validation]] and [[concepts/generated-artifact-validation]]: the output should be predictable enough to use as a directory name and as a skill identifier.

## Relationship to skill scaffolding

In the skill creator workflow, kebab-case normalization is part of the bootstrap step that transforms a user intention into a concrete directory structure. That makes it a core piece of [[concepts/skill-scaffolding]] and [[concepts/directory-bootstrap]]. The normalized name becomes the anchor for the generated `SKILL.md` file and any optional resource folders.

## Practical effects

- Title-like inputs such as `My New Skill` become `my-new-skill`.
- Irregular punctuation and spacing are removed instead of preserved.
- The resulting identifier is safer to use across tooling and filesystems.
- Consistent names make downstream discovery and registry maintenance easier.

## Related concepts

- [[concepts/naming-normalization]]
- [[concepts/document-normalization]]
- [[concepts/deterministic-validation]]
- [[concepts/skill-scaffolding]]
- [[concepts/path-safety]]
- [[concepts/generated-artifact-validation]]

See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]