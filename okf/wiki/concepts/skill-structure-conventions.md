---
type: "Concept"
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/repo-snapshot.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md"]
description: "Conventions for structuring skills so agents can validate and reuse them."
---

# Skill Structure Conventions

Skill structure conventions define how repository skills are organized so agents can find reusable actions, supporting references, executable scripts, and validation cues without mixing them into durable wiki context or top-level routing files.

## What This Concept Covers

A well-structured skill keeps its purpose clear and its assets easy to reuse. The bootstrap references frame skills as project-owned action procedures that should absorb repeated workflows once they emerge during OKF generation or ongoing agent work. The `init_skill.py` script reinforces that pattern by creating a predictable skill skeleton under `.agents/skills/`, which makes structure important not just for readability, but for maintaining a reliable boundary between [[concepts/skill-based-automation]], tooling context pages, and durable wiki knowledge.

The official Agent Skills specification adds a stricter contract around that structure. A skill is a directory with a required `SKILL.md` file, plus optional `scripts/`, `references/`, and `assets/` directories. `SKILL.md` must begin with YAML frontmatter and then Markdown body content. The metadata fields are intentionally limited: `name` and `description` are required, while `license`, `compatibility`, `metadata`, and `allowed-tools` are optional. That turns structure into something agents can reason about mechanically, not just a style preference.

The companion `quick_validate.py` script shows that structure conventions are not only about layout generation, but also about fast structural verification. It validates that a candidate skill directory has a `SKILL.md` file, that the file starts with frontmatter, and that the frontmatter contains required metadata such as `name` and `description`. That makes structure a contract that can be checked automatically, not just a convention documented in prose.

## Core Structure

The bootstrap and initialization flow describe `.agents/skills/` as the home for reusable actions. Within that area, a skill typically contains:

- a top-level `SKILL.md` describing what the skill does and how to use it
- `references/` for explanatory material, provenance, and policy notes
- `scripts/` for executable procedures the agent can run directly
- `assets/` for templates, examples, and static helper files

The specification treats `SKILL.md` as the only required file, with the rest optional. Its recommended body sections include step-by-step instructions, examples, and edge cases, while longer supporting material should move into separate files to keep the main skill under a manageable size. This fits [[concepts/progressive-disclosure]] and [[concepts/skill-progressive-disclosure]]: metadata is loaded first, the full skill body is loaded when activated, and support files are loaded only as needed.

The initializer also allows optional creation of `scripts`, `references`, and `assets` subdirectories through a constrained `--resources` flag, which helps keep the layout consistent while still supporting only the common support folders. This pattern keeps the skill focused on action rather than broad documentation, and it supports [[concepts/action-oriented-documentation]] and [[concepts/context-action-separation]].

The quick validator complements that layout by checking that these support directories, if present, are directories rather than files. That protects the expected shape of a skill tree and makes it easier for downstream tooling to assume the standard structure.

## Initialization And Naming

The `init_skill.py` bootstrapper makes structure conventions enforceable rather than aspirational:

- it normalizes the requested skill name into kebab-case
- it applies a strict name pattern with length and character limits
- it rejects invalid names after normalization instead of silently creating ambiguous directories
- it refuses to write outside a `.agents/skills`-scoped location unless the parent path still appears to be within `.agents`
- it prints the created target path on success so the result is explicit and scriptable

The Agent Skills specification adds more detail to that naming discipline. The `name` field must be lowercase letters, numbers, and hyphens only; it must not start or end with a hyphen; it must not contain consecutive hyphens; and it must match the parent directory name. The `description` field must be non-empty and concise enough to stay within the spec limit. Optional fields like `compatibility` also have explicit length constraints, which means the validator is enforcing a schema, not just a directory shape.

The quick validator extends that discipline in a read-only direction:

- it verifies the directory exists before treating it as a skill
- it requires the directory name to match the frontmatter `name`
- it rejects names that do not satisfy the same kebab-case-style constraints
- it enforces a `description` length limit and an optional `compatibility` length limit
- it reports all detected problems together instead of stopping at the first failure

This behavior ties structure to naming discipline and path safety, reinforcing [[concepts/kebab-case-normalization]], [[concepts/path-safety]], and [[concepts/filesystem-validation]].

## Separation From Other Repository Areas

The documents are explicit that skills are not the place for all project knowledge. Instead:

- `AGENTS.md` should remain short and routing-oriented
- the wiki should hold durable context and repository truth
- `graphify-out/` should remain an exploration aid, not a final source of authority
- `.agents/skills/` should hold reusable behavior that agents may execute again later

The specification sharpens that separation by describing `SKILL.md` as the skill's entrypoint and by recommending that details, examples, and supporting references be split into adjacent files when needed. That keeps the skill focused on action rather than turning it into a general knowledge dump.

The initializer supports that boundary by generating a procedural `SKILL.md` template that stays lightweight and workflow-focused, rather than embedding broad project explanation. The validator reinforces the same boundary by treating `SKILL.md` as a required, structured entrypoint rather than a free-form document.

That separation helps preserve [[concepts/documentation-architecture]], [[concepts/durable-context]], and [[concepts/single-source-of-truth]].

## Lifecycle Guidance

The source recommends treating the first OKF generation as context discovery. After the wiki exists, repeated procedures should be reviewed for skill extraction. Good candidates include:

- repeated command sequences
- validation workflows
- transformations and migrations
- scaffolding steps
- other multi-step actions that should be executed consistently

The initializer fits that lifecycle by providing a fast way to create a new skill directory when a repeated workflow has been identified. The validator fits it too by enabling quick preflight checks before a skill is adopted or distributed. Together, they reflect [[concepts/generated-content-governance]] and [[concepts/source-driven-regeneration]]: the wiki captures knowledge, while the skill system captures repeatable execution.

The spec's progressive-disclosure model also supports this lifecycle. A new skill can begin as a small `SKILL.md` with metadata and core instructions, then grow through separate `references/` files or scripts only when repeated use reveals the need for deeper guidance. That helps skill authors avoid premature expansion while still allowing stable refinement over time.

## Read-Only Vendor Skills vs Custom Skills

The document also distinguishes between vendor skills and custom skills:

- vendor skills are read-only dependencies
- they should be installed or updated via the chosen skill manager
- custom wrappers or companion skills should be created when behavior must change
- generated lock files should be preserved when the manager creates them

That distinction matters for structure because the repository-created skill skeleton is meant for local ownership, while external skills may arrive with their own managed layout and lock files. This aligns with [[concepts/skill-vendoring]], [[concepts/skill-governance]], and [[concepts/version-pinning]].

The spec also recommends validating skills with `skills-ref validate ./my-skill`, which checks frontmatter validity and naming conventions. That gives skill structure a portable verification path independent of repository-specific helpers, making the layout useful across implementations as long as they honor the same contract.

The quick validator supports this ecosystem by checking only the minimum structural contract needed for a skill to be considered valid, which keeps validation lightweight enough for local use while still defending the expected shape of repository-owned skills.

## Practical Implications

Following these conventions makes skills easier to maintain and safer for agent use:

- agents can discover the right action quickly
- behavior stays modular and reusable
- documentation does not sprawl into the wrong layer
- repeated operational steps become standardized rather than ad hoc
- skill creation is repeatable because the initializer enforces a stable directory shape
- skill validity can be checked quickly before broader workflows depend on it
- skill metadata remains compact enough for startup-time loading and routing

The referenced bootstrap document reinforces these conventions as part of converting a repository into an [[concepts/agent-ready-repositories]] setup, with the wiki front door anchored at summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.

## Related Concepts

- [[concepts/agent-ready-repositories]]
- [[concepts/skill-based-automation]]
- [[concepts/skill-governance]]
- [[concepts/skill-vendoring]]
- [[concepts/action-oriented-documentation]]
- [[concepts/context-action-separation]]
- [[concepts/durable-context]]
- [[concepts/single-source-of-truth]]
- [[concepts/kebab-case-normalization]]
- [[concepts/path-safety]]
- [[concepts/filesystem-validation]]
- [[concepts/lightweight-frontmatter-validation]]
- [[concepts/preflight-checks]]
- [[concepts/quality-gates]]
- [[concepts/progressive-disclosure]]
- [[concepts/skill-progressive-disclosure]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/portable-skill-contract]]

See also: summaries/agents__skills__skill-creator__SKILL-md

See also: summaries/repo-snapshot

## Related Documents
- [[summaries/agent-skills-spec]]
- summaries/agents__skills__skill-creator__scripts__init_skill-py
- summaries/agents__skills__skill-creator__scripts__quick_validate-py
- summaries/agent-skills-spec