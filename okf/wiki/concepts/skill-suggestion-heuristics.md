---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Heuristics for spotting actionable wiki pages that may become custom skills."
---

# Skill Suggestion Heuristics

Skill suggestion heuristics are lightweight rules for identifying wiki or repository content that looks like a good candidate for a custom action skill. The goal is not to fully understand the document, but to detect repeated operational language that signals an actionable workflow.

This concept is illustrated by [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]], which scans an OKF bundle and proposes skill names from markdown pages using simple keyword matching, page-title extraction, evidence collection, and a score threshold.

## Core idea

The heuristic approach treats documents as evidence of recurring action patterns. Pages that repeatedly describe operations such as running, validating, generating, refreshing, syncing, or managing related tools are more likely to represent reusable skills than pages that mainly explain architecture or background context.

This supports [[concepts/action-candidate-detection]] and fits within a skill-suggestion workflow where generated candidates are derived from observable signals rather than semantic inference. The goal is to find likely action surfaces without overfitting to a full intent model.

## Signals used

The source script assigns a score based on action-oriented terms in the document body. It looks for several categories of operational verbs and tool references:

- execution verbs like `run`, `execute`, `rerun`, `launch`, and `invoke`
- verification verbs like `validate`, `verify`, `check`, `test`, and `lint`
- creation verbs like `generate`, `scaffold`, `build`, `compile`, `export`, `import`, `convert`, and `transform`
- maintenance verbs like `refresh`, `update`, `sync`, `reconcile`, `rotate`, and `migrate`
- tool and runtime references such as `graphify`, `openkb`, `terraform`, `kubectl`, `helm`, `docker`, `git`, `uv`, and `python`

A page must exceed a minimum score before it becomes a candidate, which keeps the output focused on repeated action language rather than isolated mentions. The script uses a default threshold of `2`, so a single stray verb is not enough to trigger a suggestion.

## Exclusion logic

The script also filters out pages that look more like explanatory context than actionable guidance. It skips documents containing terms such as:

- architecture
- decision
- evidence
- overview
- concept
- external documentation

If a skipped page contains fenced code blocks, it can still be considered. That preserves pages where examples or runnable snippets matter, even if the surrounding prose is descriptive.

The scanner also avoids reserved wiki areas like `index.md`, `log.md`, `AGENTS.md`, and content under `sources/` or `reports/`, so it stays focused on the compiled wiki surface.

## Candidate shaping

Once a page is accepted as a candidate, the script:

- extracts a title from frontmatter or the first markdown heading
- converts that title into a slug
- trims and normalizes the slug to a short, stable name
- prefixes generic names with `manage-` when the title does not already suggest a procedural action
- accumulates multiple evidence paths for the same candidate and ranks suggestions by total score

That shaping step keeps the output usable as a seed for [[concepts/evidence-backed-skill-initialization]] and aligns the result with [[concepts/skill-structure-conventions]]. The generated init command points directly at the skill-creation bootstrap path, making the suggestion actionable instead of merely descriptive.

## Why it matters

These heuristics help turn a broad knowledge base into a smaller set of reusable action skills. That supports:

- [[concepts/skill-based-automation]] by surfacing repeatable tasks
- [[concepts/evidence-backed-skill-initialization]] by attaching source paths as evidence
- [[concepts/heuristic-classification]] by using simple pattern matching instead of a heavy model
- [[concepts/generated-artifact-adoption]] by producing ready-to-run init commands for candidate skills
- [[concepts/knowledge-base-discovery]] by mining the wiki for operational patterns

The approach also encourages progressive disclosure: the system only proposes a skill when there is enough repeated action language to justify it, and otherwise keeps the material in context. In that sense, the output is a ranked shortlist rather than an automated decision.

## Limitations

This is a practical but coarse filter.

- It can miss useful skills that are described with nonstandard verbs.
- It can over-suggest pages that mention tools frequently but do not define a reusable action.
- It depends on page naming and markdown structure, so title extraction affects candidate quality.
- It does not inspect intent deeply, so human review remains important.

For that reason, the output should be treated as a shortlist for [[concepts/human-in-the-loop-review]], not as an automatic decision.

## Relationship to surrounding concepts

Skill suggestion heuristics sit between source content and skill creation. They rely on [[concepts/action-oriented-documentation]] and [[concepts/context-action-separation]] to distinguish operational material from explanatory material, while feeding into skill initialization workflows that preserve [[concepts/source-provenance]] and [[concepts/knowledge-boundaries]].

They are especially useful inside an OKF-backed repository where the wiki itself becomes a discovery surface for [[concepts/skill-governance]] and [[concepts/agent-ready-repositories]]. The implementation in the source script also reflects [[concepts/okf-validation]]-style caution by constraining traversal, skipping reserved content, and requiring a score threshold before emitting candidates.

## Implementation notes

The script is intentionally small and deterministic:

- it uses `argparse` for `--repo`, `--okf`, and `--min-score`
- it resolves the OKF directory relative to the repository root
- it reads markdown with UTF-8 and replacement for decode errors
- it uses regex-based counting rather than semantic parsing
- it prints evidence paths and an `init_skill.py` command for each suggested candidate
- it keeps candidate naming bounded with a 64-character slug limit and falls back to `custom-action` when needed

That design makes the heuristic easy to inspect, easy to rerun, and easy to adapt as the wiki evolves.