---
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
type: "Work"
description: "CLI script that suggests custom skills from repeated OKF actions"
---

# suggest_skills_from_okf.py

`suggest_skills_from_okf.py` is a Python CLI script in `.agents/skills/skill-creator/scripts/` that scans an OKF wiki bundle and suggests candidate custom action skills from repeated action-oriented language.

## What It Does

- Traverses the `okf/wiki` directory and reads Markdown pages.
- Skips structural pages such as `index.md`, `log.md`, `AGENTS.md`, plus `sources/` and `reports/` content.
- Uses keyword heuristics to detect action-heavy pages with terms like `run`, `validate`, `generate`, `refresh`, `git`, `docker`, `kubectl`, `python`, and `uv`.
- Filters out pages that look like non-action documentation when they mostly contain context terms such as `architecture`, `decision`, `evidence`, or `overview` without code blocks.
- Derives a slugified candidate skill name from the page title or heading, and prepends `manage-` when the name does not already read like an action.
- Prints ranked suggestions with evidence paths and an `init_skill.py` command for bootstrapping a new skill.
- Supports the skill-creator workflow for turning repeated wiki actions into skills under `.agents/skills/`.
- Works with `uv run` as the preferred execution convention for bundled Python scripts.

## Key Facts

- Implemented with `argparse`, `re`, `pathlib.Path`, and `collections.Counter`.
- Accepts `--repo`, `--okf`, and `--min-score` arguments.
- Uses UTF-8 reads with replacement error handling so malformed text does not stop the scan.
- Limits generated slugs to 64 characters and normalizes them to kebab-case.
- Emits a fallback message when no candidates meet the minimum score threshold.
- Fits the skill-creator guidance that repeated actions should become skills, while durable knowledge stays in the wiki.
- Aligns with the rule that skills should be short, procedural, and validated before use.

## Relationship To Wiki Concepts

- This work is an example of [[concepts/heuristic-skill-suggestion]].
- It operationalizes [[concepts/action-candidate-detection]] by looking for repeated action language in documents.
- It depends on [[concepts/action-oriented-documentation]] as the signal source for likely skills.
- It fits within [[concepts/skill-suggestion-heuristics]] and [[concepts/evidence-backed-skill-initialization]].
- It supports knowledge base mining and [[concepts/compiled-knowledge-bases]] by turning wiki content into actionable recommendations.
- It reflects [[concepts/skill-authoring]] and [[concepts/skill-validation-workflow]] in the broader skill-creator process.

## Related Pages

- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]
