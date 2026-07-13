---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "The review and validation layer that checks wiki output before trust."
---

# Wiki Review Gates

Wiki review gates are the checks and manual review steps that happen after OpenKB generates or updates wiki content, but before the output is trusted as part of the knowledge base. They combine deterministic validation with human judgment so generated pages do not silently drift from the source material.

## What the gates do

- Verify that new or changed pages are structurally valid.
- Inspect generated pages for missing concepts, duplicate pages, and misclassified entities.
- Catch truncation, unclosed fences, and other broken output.
- Check that claims remain grounded in the staged source chain.
- Surface stale content when compilation happened in batches or after interruptions.
- Re-check promoted findings so obsolete discoveries do not remain in the wiki.
- Enforce the boundary between automated checks and human review.

## In the workflow

The workflow document makes review gates part of the normal pipeline after ingestion and regeneration. After `openkb add` or `recompile` changes `okf/wiki/`, the reviewer should:

- list the changed files with `git status --short okf/` and `git diff --stat okf/wiki/`,
- read the affected pages,
- compare them against the staged sources they cite,
- route any problems back through source correction and re-ingestion rather than editing generated pages directly.

The workflow also places review gates in a larger build sequence: it starts from `okf/wiki/index.md` when available, treats `openkb lint` as an LLM-backed health report rather than a finish line, and requires structural validation with `validate_okf_bundle.py` after generation. That means the gate is not just validation; it is also a policy boundary that keeps wiki content derived from sources instead of hand-edited in place.

## What reviewers look for

- **Missing concepts**: important ideas from the source have no page or are too vaguely named.
- **Near-duplicates**: two pages restate the same idea under different names.
- **Entity vs concept errors**: named tools, people, and products belong in entities, not concepts.
- **Lost caveats**: important "only when" or "never do" constraints get softened or dropped.
- **Truncation**: pages end mid-thought or with broken markdown.
- **Stale early pages**: earlier compiled pages may not know about concepts added later.
- **Grounding failures**: claims do not clearly trace back through the source chain.
- **Stale findings**: promoted findings may no longer hold at HEAD and should be retracted.

These checks apply especially after incremental refreshes, orphan pruning, and findings triage, where the wiki may have been rebuilt in batches or resumed after interruption.

## Why it matters

These gates protect [[concepts/provenance-tracking]], [[concepts/caveat-preservation]], and [[concepts/human-in-the-loop-review]] at the same time. They also support [[concepts/deterministic-validation]] by ensuring the compiled wiki is not only machine-checkable but also semantically reviewed.

The workflow specifically distinguishes between:

- deterministic validation with `validate_okf_bundle.py`,
- LLM-backed health reporting with `openkb lint`, and
- manual review of generated pages.

That separation keeps checks honest: structure problems fail fast, while content quality issues are examined as review work rather than treated as automatically solved.

## Related workflow details

The source workflow adds several constraints that shape review gates in practice:

- it requires the wiki to be read through `okf/wiki/index.md` first so later review follows the compiled information architecture,
- it identifies the active harness from runtime metadata or self-knowledge rather than guessing from installed binaries,
- it requires vendored toolchain skills before first CLI use,
- it treats `openkb lint` as advisory rather than a structural gate,
- it requires validation after generation with `validate_okf_bundle.py`,
- it insists that corrections flow through source documents and re-ingestion, not direct wiki edits,
- it includes orphan pruning and findings triage as part of maintaining wiki integrity over time,
- it preserves lint reports for triage even when lint exits cleanly,
- it re-reads `AGENTS.md` after validation to keep operational guidance aligned.

This is part of the broader [[concepts/generated-content-governance]] model used by the wiki pipeline, and it connects directly to [[concepts/okf-workflow-governance]] and [[concepts/wiki-review-gates]]? No, the page itself is this concept.

## Related pages

- [[concepts/quality-gates]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/deterministic-validation]]
- [[concepts/caveat-preservation]]
- [[concepts/provenance-tracking]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]