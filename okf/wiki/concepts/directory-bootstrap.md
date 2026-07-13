---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__init_skill-py.md"]
description: "Automated creation of a ready-to-use directory scaffold."
---

# Directory Bootstrap

Directory bootstrap is the automated creation of a new project or skill directory with a predictable starting structure, so a user can begin working immediately without assembling folders and starter files by hand. In this wiki, it is closely tied to [[concepts/project-scaffolding]], [[concepts/skill-scaffolding]], and [[concepts/generated-artifact-validation]].

## Core idea

A bootstrap script takes a small input, usually a name and a few options, and turns it into a usable directory tree. The output is not just an empty folder: it usually includes a starter document, optional subdirectories, and basic guardrails that keep the new directory aligned with the expected format.

## Source-backed behavior

The script in [[summaries/agents__skills__skill-creator__scripts__init_skill-py]] shows directory bootstrap as a skill-authoring workflow:

- It normalizes the requested skill name into kebab-case using [[concepts/kebab-case-normalization]].
- It validates the resulting name with a restricted pattern, reinforcing [[concepts/naming-normalization]] and [[concepts/filesystem-validation]].
- It checks that the destination stays within `.agents/skills`, which reflects [[concepts/path-safety]] and [[concepts/skill-governance]].
- It creates the target skill directory, optionally reusing it with `--force`.
- It writes a starter `SKILL.md` file that includes metadata and a procedural outline.
- It can also create optional support directories such as `scripts`, `references`, and `assets`, which connects to [[concepts/skill-resource-organization]].

## Why it matters

Directory bootstrap reduces setup friction and helps enforce a consistent on-disk shape from the start. That consistency supports:

- [[concepts/deterministic-validation]] because generated layouts are easier to inspect.
- [[concepts/skill-structure-conventions]] because new skills start from the same baseline.
- [[concepts/portable-skill-contract]] because the bootstrap output follows an expected contract.
- [[concepts/agent-ready-context-skill]] because the result is immediately usable by downstream agent workflows.

## Design characteristics

This pattern is intentionally narrow:

- It creates structure, but does not attempt to author the full skill content.
- It prefers safe defaults and a constrained option set.
- It makes generated files explicit and easy to recognize.
- It keeps the bootstrap step separate from later refinement, which aligns with [[concepts/documentation-layer-separation]] and [[concepts/context-action-separation]].

## Common risks

Bootstrap utilities can drift into unsafe or overly permissive behavior if path checks are weak or if they allow arbitrary folder creation. The source document shows mitigation through:

- explicit name normalization,
- a simple allowlist for extra resources,
- refusal to write outside the intended skills area,
- and a fixed starter template rather than unconstrained file generation.

## Related concepts

- [[concepts/skill-authoring]]
- [[concepts/skill-adoption]]
- [[concepts/skill-validation-workflow]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/preflight-checks]]