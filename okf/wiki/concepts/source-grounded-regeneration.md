---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Repair weak wiki output by improving sources and rerunning OpenKB, not editing output."
---

# Source-Grounded Regeneration

Source-grounded regeneration is the practice of fixing weak, stale, missing, or inconsistent wiki output by improving the committed source material and rerunning the OpenKB pipeline, rather than editing generated pages directly. The wiki is treated as a projection of repository evidence, so the durable repair is to strengthen the source that fed it and let the compiled pages regenerate from that evidence.

The broader repository model places this idea inside [[concepts/repository-transformation-pipelines]], [[concepts/knowledge-layer-separation]], and [[concepts/knowledge-lifecycle-governance]]: source files provide evidence, `AGENTS.md` provides orientation, `okf/wiki/` holds compiled durable knowledge, and `.agents/skills/` carries repeatable actions. Regeneration is therefore not just a refresh step; it is the mechanism that keeps those layers aligned.

## What It Means

The core idea is simple: if a compiled page is wrong, vague, incomplete, or missing a boundary, the answer is not to patch the generated wiki page by hand. Instead, update the originating repository document, keep the knowledge traceable, and let OpenKB regenerate the derived pages from the revised input. This preserves [[concepts/provenance-tracking]], [[concepts/single-source-of-truth]], and [[concepts/wiki-content-as-untrusted-data]].

The OpenKB lifecycle makes that discipline explicit. Before compiling or changing the KB, the workflow starts with `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then reads `okf/wiki/index.md` and relevant pages, using `openkb query` only as a last resort. It treats wiki content as untrusted input, not instruction, and keeps the KB root staged through `okf/.okf-build/input/` before `openkb add` or `openkb recompile` runs.

The lifecycle also distinguishes source-driven regeneration from output-only curation. If the source itself is wrong, fix the committed source and recompile. If the knowledge is missing entirely from the repository, capture it as a finding and promote it through [[concepts/findings-promotion]]. If the wiki structure needs cleanup without changing the underlying claims, use bounded editorial curation instead of pretending the source changed.

## How the Regeneration Loop Works

1. Identify the weak wiki page, missing concept, or stale claim.
2. Find the committed source file that should have expressed the knowledge.
3. Clarify the source so the idea, constraint, or boundary is explicit.
4. Rebuild staged input deterministically under `okf/.okf-build/input/`.
5. Run `openkb --kb-dir ./okf add` on the staged pack.
6. Recompile the affected document if needed, then validate the result.

This is an incremental regeneration workflow built around [[concepts/incremental-compilation]], [[concepts/source-driven-regeneration]], [[concepts/source-trust-levels]], and [[concepts/deterministic-validation]]. It is intentionally conservative: the wiki should change only when the underlying evidence changes.

The lifecycle adds important guardrails around that loop. Deletions, moves, and deselections are reconciled before ingest so stale pages do not linger. `openkb remove` is the deterministic inverse of ingestion, and the repository-specific orphan-reconciliation script uses it to prune stale docs when source files disappear. That makes regeneration more trustworthy because it keeps the registry, raw copies, and wiki pages coherent instead of letting drift accumulate.

## When a Source Does Not Exist

Sometimes no committed document ever stated the knowledge. In that case, the knowledge is discovered rather than documented. The right path is to capture it as a finding page, then promote it if it remains true and conflicts with or fills gaps in the compiled wiki.

That distinction matters because source-grounded regeneration applies to repository-stated knowledge, while findings are the mechanism for newly observed knowledge that has not yet been authored into the repo. The OpenKB lifecycle reinforces this boundary: findings live in `okf/wiki/explorations/findings/`, are triaged as promote/keep/drop, and become `finding-*` docs only when they are mature enough to ingest.

## Key Properties

- Keeps compiled wiki content aligned with repository truth.
- Avoids drift caused by hand-edited generated pages.
- Preserves traceable evidence chains from source to summary to concept.
- Separates repository facts from newly discovered observations.
- Encourages conservative updates and reproducible regeneration.
- Fits the agent-ready repository model of orientation, context, and action layers.
- Treats `okf/wiki/` as compiled durable knowledge, not the place where source correction happens.
- Uses staged input, recompile, and validation gates so regeneration stays deterministic and reviewable.

## Related Lifecycle Rules

The source document also ties regeneration to several operational safeguards:

- Generated pages should not be hand-edited in compiled namespaces.
- The KB registry and wiki pages must remain coherent.
- `openkb recompile` is the approved way to refresh stale or weak pages.
- If the source itself is misleading, the correct repair is to revise the source and rerun the pipeline.
- `openkb add` should ingest staged, deterministic input rather than ad hoc edits.
- Deletions and source loss should be reconciled before ingestion so the compiled wiki does not preserve orphaned claims.
- Findings should be promoted only when they are still true and add missing knowledge.
- Source packs should remain reproducible, with provenance recorded through staged metadata and hash coherence.

These rules connect source-grounded regeneration to [[concepts/registry-drift]], [[concepts/generated-content-governance]], [[concepts/knowledge-lifecycle-governance]], [[concepts/okf-validation]], and [[concepts/okf-workflow-governance]]. They also reflect the consent-first and data-flow-disclosure posture: any regeneration driven by external or LLM-backed tooling should remain explicit, pinned, and auditable.

## Why It Matters

Without source-grounded regeneration, a knowledge base can become visually polished but semantically stale. With it, the wiki remains a living projection of committed evidence, and any correction starts where the knowledge originally lives. That makes the system more trustworthy, easier to audit, and less vulnerable to silent divergence between docs and compiled output.

The OpenKB lifecycle shows the same maintenance philosophy at the system level: keep registry state and wiki pages coherent, stage input before ingest, reconcile deletions before adding new sources, and preserve a grounded chain from source file to summary page to compiled concept. That separation helps the repository stay coherent as its context surface evolves.

The broader agent-ready repository discipline depends on this pattern: keep skills as actions, compiled wiki pages as context, and `AGENTS.md` as orientation. Source-grounded regeneration is the mechanism that lets those layers stay in sync without collapsing them into a single, hard-to-maintain document.

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/karpathy-llm-wiki-gist]]