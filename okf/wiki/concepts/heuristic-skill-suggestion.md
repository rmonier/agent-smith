---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Heuristic detection of reusable skills from action-heavy wiki content."
---

# Heuristic Skill Suggestion

Heuristic skill suggestion is the practice of scanning wiki content for repeated action-oriented language and turning those patterns into candidate custom skills. It is a lightweight way to discover automation opportunities without requiring semantic analysis or manual curation up front.

## Core Idea

The approach treats operational verbs, tool names, and repeatable workflow language as signals that a page may represent a reusable action. Instead of trying to fully understand the document, it looks for patterns that often correlate with things a skill could do: run, validate, generate, refresh, build, export, import, sync, and similar terms.

This makes heuristic suggestion useful for early-stage [[concepts/skill-suggestion-heuristics]] and [[concepts/action-candidate-detection]], especially when the goal is to mine an existing knowledge base for workflow-shaped opportunities.

## How It Works

The source script [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]] implements a simple pipeline:

- Walk the OKF wiki tree and inspect Markdown pages.
- Skip structural pages like `index.md`, `log.md`, and `AGENTS.md`.
- Ignore source and report directories so the scan focuses on compiled knowledge pages.
- Filter out pages that look like non-action context, especially those dominated by architecture or overview language.
- Count matches for a small set of action-oriented regex patterns.
- Derive a candidate skill name from the page title or filename.
- Normalize the name into kebab-case and prefix generic names with `manage-` when needed.
- Rank candidates by accumulated score and print evidence paths plus an initialization command.

## Important Details

- The script uses simple keyword matching rather than embeddings or LLM-based classification, which keeps it fast and deterministic.
- Evidence is preserved as file paths so a human can quickly inspect why a candidate was suggested.
- A minimum score threshold prevents weak signals from producing noisy recommendations.
- Pages that mention high-level documentation terms without code blocks are often treated as context, not skill material.
- The output is designed to feed directly into skill scaffolding workflows, connecting discovery to creation.

## Why It Matters

Heuristic skill suggestion helps bridge [[concepts/action-oriented-documentation]] and [[concepts/skill-scaffolding]]. It lets a repository surface likely action boundaries from accumulated knowledge, which is especially useful in large or evolving OKF bundles where reusable procedures may be spread across many documents.

This also supports [[concepts/agent-ready-context]] by turning discovered workflows into explicit candidate skills that can later be validated, packaged, and adopted.

## Tradeoffs

Heuristic approaches are intentionally approximate.

- They are easy to run and explain.
- They can produce false positives when action words appear in narrative or conceptual prose.
- They can miss valid skills if the wording is indirect or domain-specific.
- They work best when paired with human review and downstream validation.

That makes them a good fit for [[concepts/human-in-the-loop-review]] and [[concepts/skill-validation-workflow]] rather than a fully automated decision system.

## Related Concepts

- [[concepts/action-pattern-mining]]: Finds repeated operational patterns across documents.
- [[concepts/action-oriented-documentation]]: Documentation style that naturally exposes action boundaries.
- [[concepts/heuristic-classification]]: Broad pattern-based classification strategy.
- [[concepts/skill-suggestion-heuristics]]: The specific heuristics used to propose new skills.
- [[concepts/evidence-backed-skill-initialization]]: Uses evidence to justify starting a skill scaffold.
- [[concepts/knowledge-base-discovery]]: Discovering useful structure from compiled knowledge.
- [[concepts/agent-ready-context-skill]]: A downstream target for turning context into reusable skill packaging.
