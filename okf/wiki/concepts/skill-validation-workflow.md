---
type: "Concept"
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
description: "How skills are structured and validated before adoption."
---

# Skill Validation Workflow

Skill Validation Workflow is the process used to confirm that a skill is safe, focused, structurally valid, and reliable before it is adopted for routine use. In the `skill-creator` materials and the Agent Skills specification, validation is treated as a required finish step, not an optional cleanup, because skills are meant to be executable capabilities that future agents can trust.

This concept is closely tied to [[concepts/baseline-first-testing]], [[concepts/deterministic-validation]], [[concepts/executable-validation]], and [[concepts/quality-gates]]: the workflow is not just about checking that files exist, but about proving the skill behaves correctly under realistic pressure and that its layout matches the repository's contract.

It also depends on the official Agent Skills format itself, including the required `SKILL.md` structure, progressive disclosure, and the expectation that skills can be validated with a dedicated checker. That makes validation part of [[concepts/portable-skill-contract]] and [[concepts/progressive-disclosure]], not just a final lint pass.

## Core purpose

The validation workflow exists to catch problems that are easy to miss during drafting:

- missing or incorrect instructions
- unsafe or overly broad tool permissions
- accidental duplication of context that belongs elsewhere
- broken scripts, paths, or naming conventions
- hidden assumptions that make the skill fragile
- frontmatter or directory-structure issues that would block adoption
- lost caveats or boundary rules in generated drafts
- mismatches between a skill's directory name and its declared `name`

The goal is to make the skill robust enough that another agent can follow it without extra coaching and that the repository can trust it as a portable skill artifact.

## Validation sequence

The `skill-creator` document describes a baseline-first approach:

1. Identify the repeated action and confirm it really belongs in a skill.
2. Check for existing skills so the new one does not duplicate coverage.
3. Build the skill with the right resource split between scripts, references, and assets.
4. Test the skill against a pressure scenario before trusting it.
5. Rewrite the skill to close the observed gaps.
6. Run the final quick validation step.

That sequence reflects a [[concepts/failure-driven-development]] mindset: first observe how the action fails in practice, then encode the fix. The quick validator is the last gate in that sequence, turning the draft into a checked artifact rather than a provisional one.

The process also matches the Agent Skills spec's progressive disclosure model:

- metadata is loaded first through the `name` and `description` fields
- the full `SKILL.md` body is loaded when the skill is activated
- supporting resources are loaded only when needed

Because of that, validation has to cover both the visible metadata and the supporting file layout, not just the prose in the skill body.

The document also distinguishes between two creation paths:

- hand-scaffolded skills, used when OpenKB is unavailable, the repository is in air-gapped mode, or the action is small or fragile
- generated skills, which may be adopted from an OpenKB draft and then reviewed for caveat preservation

Both paths converge on the same validation requirement: the skill is not ready until it has passed the validator and any pressure-test issues have been resolved.

## What gets validated

The workflow validates both content and behavior:

- the `SKILL.md` file stays short, procedural, and action-focused
- `name` stays lowercase, hyphenated, and aligned with the parent directory name
- `description` clearly explains what the skill does and when to use it
- optional fields such as `license`, `compatibility`, `metadata`, and `allowed-tools` stay within their spec limits
- `allowed-tools` is minimal and scoped to the real task
- security defaults are present, including consent-first installs and secret handling
- generated or adopted skills preserve caveats instead of flattening them away
- naming rules, resource layout, and repository paths are consistent
- supporting directories such as `scripts`, `references`, and `assets` exist only as directories when present
- the skill can be validated with the bundled script before use

This makes the workflow part of [[concepts/safe-automation]] rather than a simple formatting check. The validation step also reinforces [[concepts/path-based-skill-validation]] and [[concepts/lightweight-frontmatter-validation]] by checking the skill's location and metadata directly.

## Spec alignment

The Agent Skills specification adds several concrete constraints that validation should enforce or at least surface clearly:

- a skill is a directory that must contain `SKILL.md`
- `SKILL.md` must begin with YAML frontmatter followed by Markdown content
- `name` must be 1-64 characters, use lowercase letters, numbers, and hyphens only, avoid leading/trailing hyphens, avoid consecutive hyphens, and match the directory name
- `description` must be non-empty and can be up to 1024 characters
- `compatibility` is optional but limited to 500 characters
- `metadata` is an arbitrary string-to-string map
- `allowed-tools` is an experimental space-separated string of approved tools
- the body should include instructions, examples, and edge cases when useful
- the main file should stay under 500 lines, with heavier detail split into referenced resources
- file references should stay relative and close to `SKILL.md`

These rules make skill validation a combined structure, metadata, and maintainability check, not just a content review.

## Source-specific details

In `skill-creator`, validation is explicitly mandatory. The document recommends using the bundled validator after the skill is created or adopted, and it also warns that generated skills should be reviewed for lost constraints, especially boundary rules and "never do" clauses.

The bundled script, `quick_validate.py`, enforces a fast structural pass over a candidate skill directory. It checks that `SKILL.md` exists, that frontmatter starts and closes correctly, and that required fields are present. It also validates the `name` against a lowercase kebab-case pattern, ensures the directory name matches the frontmatter name, and caps the lengths of `name`, `description`, and `compatibility` fields.

The script is intentionally narrow: it uses simple frontmatter extraction instead of full YAML parsing, reports all errors before exiting, and treats filesystem layout as part of the skill contract. It also rejects misplaced skills that are not under `.agents/skills` and flags any non-directory `scripts`, `references`, or `assets` entries.

The document's creation guidance is aligned with this validation model:

- use `uv run` for bundled Python scripts when uv is available
- initialize skills with the provided scaffold script and the expected resource directories
- prefer scripts for deterministic or reusable operations
- keep `SKILL.md` short and move heavier detail into resource files
- validate before finishing, not after deployment

## Related ideas

- [[concepts/evidence-backed-skill-initialization]] connects validation to the decision to create a skill in the first place.
- [[concepts/generated-artifact-adoption]] matters when a generated draft is brought into the repository and must be checked for drift.
- [[concepts/caveat-preservation]] is essential because validation must restore constraints that LLM-generated drafts may lose.
- [[concepts/skill-authoring]] and [[concepts/skill-governance]] frame the broader lifecycle around skill creation and maintenance.
- [[concepts/portable-skill-contract]] helps explain why a validated skill should work cleanly across compatible harnesses.
- [[concepts/deterministic-validation]] and [[concepts/filesystem-validation]] explain why a compact validator can produce predictable, repeatable outcomes.
- [[concepts/skill-frontmatter-schema]] and [[concepts/skill-resource-organization]] capture the spec-level structure that validation needs to protect.

## Practical takeaway

A skill validation workflow should not merely confirm that the skill exists; it should prove that the skill is narrowly scoped, safely executable, structurally valid, and resilient under the conditions it was written for.

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]

## Related Documents
- [[summaries/agent-skills-spec]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]