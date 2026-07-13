---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Finding recurring action signals in docs to propose reusable skills."
---

# Action Pattern Mining

Action pattern mining is the practice of scanning documentation for repeated operational language, then turning those repeats into reusable automation candidates. It sits between [[concepts/action-oriented-documentation]] and [[concepts/heuristic-classification]], using lightweight signals to identify where a new skill may be useful.

## Core Idea

The goal is not to fully understand a document semantically. Instead, it looks for patterns that often indicate a repeatable task:

- verbs such as `run`, `execute`, `validate`, `generate`, and `refresh`
- tool names and workflow markers such as `git`, `docker`, `kubectl`, `python`, and `uv`
- multiple occurrences across a knowledge base, suggesting the task is common enough to automate

This makes action pattern mining a practical discovery method for [[concepts/skill-suggestion-heuristics]] and [[concepts/skill-based-automation]].

## How It Works in the Source Script

The source document [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]] implements a small heuristic pipeline:

- it walks Markdown pages in an OKF wiki bundle
- it skips structural pages like `index.md`, `log.md`, and `AGENTS.md`
- it ignores source and report directories to reduce noise
- it filters out pages that appear to be conceptual rather than operational, especially when they mention words like `architecture`, `decision`, or `overview` without code blocks
- it scores pages by counting matches against a set of action-oriented regex patterns
- it extracts a title or heading, converts it into a slug, and normalizes it into a candidate skill name
- it accumulates evidence paths and prints an initialization command for each suggestion

## Practical Output

The script does more than detect action language. It also packages the result for downstream use:

- a candidate skill name
- an aggregate score showing how strongly the page matches action patterns
- a short evidence trail of source pages
- a ready-to-run `init_skill.py` command for skill bootstrapping

This makes the mining process directly useful for [[concepts/evidence-backed-skill-initialization]] and [[concepts/skill-authoring]].

## Design Characteristics

- Heuristic-first: relies on regex and simple filters rather than model inference
- Bundle-aware: works over an OKF wiki tree rather than arbitrary documents
- Noise-resistant: excludes low-signal and structural content
- Action-biased: prefers names that look operational, and prefixes generic slugs with `manage-` when needed
- Evidence-oriented: keeps source paths attached to every suggestion

## Related Concepts

- [[concepts/action-candidate-detection]] for identifying likely automation opportunities
- [[concepts/knowledge-base-discovery]] for finding useful material across a corpus
- [[concepts/skill-suggestion-heuristics]] for the broader strategy of recommending skills from text
- [[concepts/compiled-knowledge-bases]] for the environment this kind of mining operates on
- [[concepts/document-normalization]] for the cleaning and filtering that makes the scan workable

## Why It Matters

Action pattern mining helps convert recurring documentation into executable capability. In practice, it reduces the gap between what a repository knows and what an agent can do, while keeping the process simple, inspectable, and grounded in source evidence.