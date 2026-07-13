---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md"]
description: "Bootstrap OKF knowledge without LLM synthesis while preserving provenance."
---

# LLM-Free Knowledge Bootstrap

LLM-free knowledge bootstrap is the practice of creating a minimally usable, traceable knowledge base from staged source material without relying on model-driven semantic synthesis. It favors structure, provenance, and navigability over completeness, so a repository can be oriented and validated even in environments where provider credentials are unavailable.

## Core Idea

This approach produces a conservative starting point instead of a polished compilation. The output is intentionally labeled as a skeleton, reminding users that later enrichment is required before the pages should be treated as authoritative. That makes it a practical fallback for [[concepts/air-gapped-operation]], [[concepts/offline-first-workflows]], and other constrained environments where LLM access is missing or inappropriate.

A related downstream use is action discovery: once a bundle exists, heuristic scripts can scan the OKF wiki for repeated operational language and suggest candidate skills without any semantic model. The script in `summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py` does exactly that by mining Markdown pages for action patterns, filtering low-signal context, and emitting ranked custom action skill suggestions with evidence paths.

## How The Bootstrap Works

The script in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]] builds a small OKF wiki bundle directly from repository metadata and staged inputs:

- it reads the repository root, staged input directory, and output directory from CLI flags
- it captures the current git commit for provenance
- it copies any staged external markdown files into a references area
- it emits a repository overview page from the git state and Graphify report excerpt
- it writes a root index and a log entry so the generated bundle is navigable

This is a form of [[concepts/source-grounded-regeneration]] because the generated pages come from existing artifacts rather than inferred meaning. It also reflects [[concepts/evidence-staging]] by separating evidence files from compiled pages.

The same bootstrap mindset supports later heuristic compilation steps. In particular, the skill-suggestion script shows how a bootstrapped wiki can be mined for operational intent: it walks the wiki, ignores reserved and low-signal pages, scores action-oriented keywords such as `run`, `validate`, `generate`, `refresh`, `git`, `docker`, `kubectl`, `python`, and `uv`, and proposes skill names with supporting evidence and an init command. That keeps skill creation grounded in the repository rather than in free-form synthesis.

## Why It Matters

LLM-free bootstrap is useful when the goal is to get from zero to a valid wiki scaffold quickly, safely, and deterministically. It supports:

- [[concepts/graceful-degradation]] when semantic tooling is unavailable
- [[concepts/deterministic-builds]] by producing predictable output from staged inputs
- [[concepts/provenance-tracking]] through git commit capture and evidence copying
- [[concepts/knowledge-base-navigation]] by ensuring a root index exists immediately
- [[concepts/generated-content-governance]] by clearly marking the output as non-authoritative
- [[concepts/heuristic-skill-suggestion]] by enabling post-bootstrap discovery of action candidates without LLM inference

## Source-Specific Characteristics

The referenced script is deliberately conservative in several ways:

- it avoids claiming semantic completeness
- it uses a plain overview page rather than inferred topical pages
- it limits itself to the first portion of `graphify-report.md` if present
- it treats external documentation as evidence, not as compiled truth
- it preserves a boundary between project knowledge and harness-specific tooling context
- it relies on simple pattern matching and `slugify` normalization to suggest skills from repeated operational language

Those choices align with [[concepts/knowledge-boundaries]] and [[concepts/tooling-boundaries]], keeping the bootstrap layer separate from the final knowledge model.

## Relationship To Other Concepts

LLM-free bootstrap is closely related to [[concepts/repository-overview-generation]], [[concepts/project-scaffolding]], and [[concepts/kb-root-staging]]. It can also feed later stages of [[concepts/repo-ingestion-pipelines]] and [[concepts/source-bundling]], where the scaffold becomes input for richer compilation.

It also complements [[concepts/action-pattern-mining]] and [[concepts/heuristic-classification]]: once the minimal wiki exists, repeated action verbs and tool references can be mined from it to identify likely skill boundaries. In that sense, the bootstrap phase creates the readable substrate, and the suggestion phase turns that substrate into candidate automation.

The concept depends on a broader governance pattern: first establish a safe, inspectable base, then apply [[concepts/editorial-curation-passes]] or other enrichment workflows once stronger sources or model access are available.

## Practical Outcome

The result is not a finished wiki, but a reliable floor:

- a repository overview exists
- evidence files are preserved
- the bundle is indexed
- the generation step is logged
- the knowledge base can be expanded later without losing provenance
- recurring action pages can be surfaced later as candidate skills from the bootstrapped corpus

In short, LLM-free knowledge bootstrap makes it possible to start an OKF bundle with [[concepts/source-trust-levels]] intact, even when the semantic compiler is absent.

## Related Documents
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]


See also: [[summaries/README-md]]