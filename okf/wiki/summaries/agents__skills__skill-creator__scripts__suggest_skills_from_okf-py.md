---
type: "Summary"
description: "Heuristically suggests custom action skills from an OKF wiki bundle."
doc_type: short
full_text: "sources/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"
---

# .agents/skills/skill-creator/scripts/suggest_skills_from_okf.py

This script scans an OKF wiki bundle and suggests candidate custom action skills based on repeated action-oriented language in Markdown pages. It is a lightweight heuristic tool for surfacing automation opportunities from existing knowledge-base content.

## What It Does

- Walks the `okf/wiki` tree and inspects Markdown files.
- Skips structural or low-signal pages such as `index.md`, `log.md`, `AGENTS.md`, `sources/`, and `reports/`.
- Filters out pages that look like non-action context, especially when they mention terms like `architecture`, `decision`, `evidence`, or `overview` without code blocks.
- Counts action-oriented keywords with regex patterns for verbs like `run`, `validate`, `generate`, `refresh`, and tooling terms like `git`, `docker`, `kubectl`, `python`, and `uv`.
- Derives a candidate skill name from the page title or filename using `slugify`.
- Normalizes generic names by prefixing `manage-` when the slug does not already suggest a strong action.
- Aggregates evidence paths and prints suggested skill names with an initialization command.

## Key Ideas

- [[concepts/heuristic-classification]]: The script uses simple keyword matching rather than semantic analysis to infer likely skill boundaries.
- [[concepts/action-oriented-documentation]]: It treats imperative and operational verbs as signals that a page could map to a reusable action skill.
- [[concepts/knowledge-base-discovery]]: The OKF corpus is mined for recurring operational intent rather than manually curated skill candidates.
- [[concepts/skill-suggestion-heuristics]]: Output is a ranked list of candidate skill names with supporting evidence and a bootstrap command.

## Implementation Notes

- Uses `argparse` for `--repo`, `--okf`, and `--min-score` configuration.
- Relies on `pathlib.Path` for repository traversal and file handling.
- Uses `collections.Counter` to accumulate repeated candidate names and rank them by score.
- Reads files with UTF-8 and replacement error handling so malformed text does not stop the scan.
- Extracts titles from either `title:` metadata lines or top-level Markdown headings.
- Produces a fallback suggestion note when no candidates meet the threshold.

## Notable Behavior

- A page can be skipped entirely if it reads like conceptual documentation and lacks code blocks.
- Candidate names are intentionally constrained to 64 characters and cleaned into lowercase hyphenated slugs.
- If the slug does not already contain an obvious action verb, the script prepends `manage-` to keep the generated skill name action-like.
- The script prints up to three evidence file paths per suggested skill to help validate the recommendation quickly.

## Output Shape

For each candidate, the script prints:

- the suggested skill name
- the aggregated score
- up to three evidence paths
- a ready-to-run `init_skill.py` command

## Relevance

This file is a small but useful bridge between [[concepts/knowledge-base-discovery]] and skill authoring workflows. It helps turn recurring operational knowledge in OKF into concrete starting points for custom actions.

## Related Concepts
- [[concepts/heuristic-skill-suggestion]]
- [[concepts/action-pattern-mining]]
- [[concepts/action-candidate-detection]]
- [[concepts/evidence-backed-skill-initialization]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/kebab-case-normalization]]
- [[concepts/path-based-skill-validation]]
- [[concepts/skill-scaffolding]]
- [[concepts/skill-authoring]]
- [[concepts/skill-based-automation]]
- [[concepts/skill-validation-workflow]]

## Entities
- [[entities/suggest_skills_from_okf-py]]
- [[entities/skill-creator]]
- [[entities/agents-skills]]
- [[entities/agent-skills]]
- [[entities/openkb]]
- [[entities/okf-wiki]]
- [[entities/okf]]
- [[entities/uv]]
- [[entities/python]]
- [[entities/romain-monier]]
- [[entities/build_okf_source_pack-py]]
- [[entities/init_skill-py]]
- [[entities/openkb-skill-factory]]
- [[entities/validate_okf_bundle-py]]
