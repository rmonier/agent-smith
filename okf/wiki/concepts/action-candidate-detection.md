---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Detecting repeated operational language to suggest reusable skills."
---

# Action Candidate Detection

Action candidate detection is the practice of scanning wiki content for repeated operational language that suggests a page should become a custom skill or other executable workflow artifact. It is a lightweight form of [[concepts/heuristic-classification]] focused on finding documents whose content is more about doing than describing.

## Core idea

The goal is to identify documents that repeatedly describe actions such as running, validating, generating, syncing, refreshing, or managing tools. When those patterns appear often enough, the document becomes evidence that a reusable skill may be warranted.

This bridges [[concepts/action-oriented-documentation]] and [[concepts/skill-suggestion-heuristics]]: instead of manually reading every page for procedural value, the system uses simple signals to surface likely candidates for [[concepts/evidence-backed-skill-initialization]].

## How the detection works

The referenced script, [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]], implements a rule-based pass over an OKF wiki bundle:

- It walks Markdown pages under `okf/wiki`.
- It skips housekeeping pages such as `index.md`, `log.md`, and `AGENTS.md`.
- It ignores material under `sources/` and `reports/`.
- It reads each remaining page as text and scores it using action-oriented keyword patterns.
- It filters out pages that look like abstract context unless they contain code fences.
- It derives a candidate skill name from the page title or first heading, normalizes it into a slug, and reports matching evidence paths.
- It boosts names that already contain an obvious action verb, and prefixes `manage-` when they do not.
- It prints an `init_skill.py` command so the suggestion can be turned into a new skill quickly.

## Heuristic signals

The detector treats these word groups as action signals:

- run, execute, rerun, launch, invoke
- validate, verify, check, test, lint
- generate, scaffold, build, compile, export, import, convert, transform
- refresh, update, sync, reconcile, rotate, migrate
- tool-heavy references such as `graphify`, `openkb`, `terraform`, `kubectl`, `helm`, `docker`, `git`, `uv`, and `python`

A document only becomes a candidate when the total score reaches the configured minimum threshold. This makes the detector a simple form of [[concepts/heuristic-classification]] rather than semantic understanding.

## Naming behavior

When the script identifies a candidate, it derives a skill name from the page title or heading, then normalizes it into a slug. The slug is lowercased, punctuation is collapsed into hyphens, and the result is truncated to keep names compact.

If the resulting name does not already suggest an action, the script prefixes `manage-` to keep the generated skill name operational. That keeps the output aligned with [[concepts/naming-normalization]] while preserving the source page's intent.

## Skip logic

The detector avoids pages that appear to be explanatory rather than operational by looking for terms like:

- architecture
- decision
- evidence
- overview
- concept
- external documentation

If these terms appear and the page does not include code fences, the page is skipped. This reduces false positives from background or meta-documentation and keeps the output closer to [[concepts/agent-ready-context-skill]] material.

The script also skips `index.md`, `log.md`, `AGENTS.md`, and pages under `sources/` and `reports/`, which helps maintain [[concepts/documentation-layer-separation]] and avoids confusing compiled knowledge with generated or diagnostic output.

## Why it matters

Action candidate detection is useful because it supports:

- [[concepts/evidence-backed-skill-initialization]] by grounding skill creation in observed repository content
- [[concepts/agent-trigger-design]] by surfacing natural cues for when a skill should exist
- [[concepts/safe-automation]] by making suggestions from local evidence instead of guessing
- [[concepts/generated-content-governance]] by keeping skill creation tied to visible source material
- [[concepts/knowledge-base-discovery]] by turning repeated operational phrasing into a navigation aid for reuse

The result is a practical bridge from documentation to executable support: pages that repeatedly describe work can be organized as skills instead of remaining scattered procedural notes.

## Limitations

The approach is intentionally simple. It does not understand intent deeply, so it can miss nuanced procedural docs or overcount pages that happen to use action verbs in descriptive ways. Its value comes from being transparent, cheap to run, and easy to audit.

That makes it a good fit for [[concepts/consent-first-workflows]] and [[concepts/deterministic-validation]], where users want predictable behavior and clear evidence trails rather than opaque ranking.

## Related ideas

- [[concepts/action-oriented-documentation]]
- [[concepts/skill-suggestion-heuristics]]
- [[concepts/heuristic-classification]]
- [[concepts/evidence-backed-skill-initialization]]
- [[concepts/safe-automation]]