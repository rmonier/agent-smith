---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Skill suggestions grounded in repeated action evidence from repository content."
---

# Evidence-Backed Skill Initialization

Evidence-backed skill initialization is the practice of creating or suggesting new custom skills only when repository or knowledge-base content shows repeated, action-oriented evidence that a skill would be useful. Instead of inventing skills from abstract needs, the workflow grounds each suggestion in concrete document traces and uses those traces to justify the initial skill scaffold.

## Core idea

The concept combines [[concepts/skill-suggestion-heuristics]] with [[concepts/source-provenance]] and [[concepts/agent-ready-context-skill]]. A document set is scanned for repeated operational language, and only pages that cross a minimum signal threshold are treated as candidate evidence for a new skill. This keeps skill creation tied to actual work patterns rather than broad topic labels.

The source script in `summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py` shows the pattern in a compact form: it traverses an OKF wiki bundle, skips reserved navigation and maintenance pages, ignores source and report directories, and scores markdown pages using regex patterns that look for verbs and tool names associated with action. Pages that read like high-level context are filtered out unless they contain fenced code, which helps separate descriptive material from procedural material. When a page clears the threshold, the script derives a slug from the title or heading, nudges generic names toward action-oriented prefixes, and emits both evidence paths and an initialization command.

This is a practical example of [[concepts/heuristic-classification]] used for [[concepts/action-candidate-detection]] and [[concepts/action-pattern-mining]].

## How the source script applies it

The script in `summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py` implements a lightweight version of this approach:

- It walks an OKF wiki bundle and inspects Markdown pages.
- It skips catalog and operational files such as `index.md`, `log.md`, and `AGENTS.md`.
- It ignores pages under `sources/` and `reports/` to avoid self-referential noise and generated artifacts.
- It filters out pages that look like high-level architecture, decision, evidence, overview, concept, or external documentation material unless they include code fences.
- It scores pages with regex patterns that capture verbs such as run, validate, generate, refresh, and action-heavy tool references like git, docker, kubectl, python, and uv.
- It requires a minimum score before considering a page as evidence for a candidate skill.
- It derives a skill name from the page title or first Markdown heading, normalizes it into a short slug, and prefixes generic names with `manage-` when needed.
- It aggregates repeated hits across pages, records up to three evidence paths per candidate, and prints an `init_skill.py` command for starting the skill scaffold.

The script is intentionally conservative: it favors repeated signals over isolated mentions, and it avoids treating descriptive material as evidence unless the page contains code. That makes it a simple [[concepts/heuristic-classification]] pipeline for [[concepts/action-pattern-mining]] in a wiki bundle.

## Why the evidence matters

The evidence list is not just a convenience. It serves several governance goals:

- It shows why a skill was suggested.
- It preserves traceability back to source pages.
- It supports later review and refinement.
- It reduces the risk of creating skills that do not map to recurring workflow needs.

That makes the workflow consistent with [[concepts/evidence-grounded-answering]] and [[concepts/provenance-tracking]]. The evidence also helps distinguish a real skill opportunity from a one-off mention, which is important when using broad action keywords that may appear in descriptive prose.

## Related safeguards

Evidence-backed skill initialization works best when paired with:

- [[concepts/human-in-the-loop-review]] for confirming whether a suggested skill is worth creating.
- [[concepts/quality-gates]] to keep thresholds and heuristics meaningful.
- [[concepts/wiki-review-gates]] to ensure wiki content is fit for reuse.
- [[concepts/generated-content-governance]] so that generated skill scaffolds remain accountable.
- [[concepts/skill-governance]] to manage skill lifecycle decisions after initialization.
- [[concepts/skill-action-boundary]] so that action skills stay focused on operational work rather than absorbing general context.

## Practical outcome

The output of this process is a ranked list of candidate skills, each backed by observed repository evidence and a ready-to-run initialization command. In effect, the repository itself becomes a discovery surface for skill creation, and the initialization step becomes a controlled response to recurring operational signals.

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

## Related Documents
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/karpathy-llm-wiki-gist]]