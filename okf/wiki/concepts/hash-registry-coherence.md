---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "OpenKB state must keep hashes, raw inputs, and wiki output aligned."
---

# Hash Registry Coherence

Hash registry coherence is the requirement that OpenKB's ingestion registry, stored raw material, staged inputs, and generated wiki pages remain synchronized so the knowledge base reflects what the system believes has been ingested and can still regenerate safely.

This concept is central to safe OpenKB maintenance in `summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md` and is reinforced by the repository agent-readiness workflow in [[summaries/agents__skills__agent-ready-context__SKILL-md]] and the agent-ready repository template summarized in [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]. It connects closely to [[concepts/generated-content-governance]], [[concepts/source-driven-regeneration]], [[concepts/evidence-staging]], [[concepts/provenance-tracking]], [[concepts/wikilink-integrity]], [[concepts/quality-gates]], and [[concepts/validation-vs-health-reporting]].

## Why it matters

OpenKB deduplicates ingested material by hash through `okf/.openkb/hashes.json`. That behavior is useful for deterministic ingestion, but it creates a failure mode when registry state drifts away from actual generated content.

If the registry records a document as already ingested, later `add` operations can silently skip that document even when its wiki pages have been lost or damaged. In that state, the knowledge base has a persistent hole: the system believes the content is present, but the usable compiled pages are missing.

The lifecycle guidance makes this operationally explicit by warning that `okf/.openkb/hashes.json` is the dedupe registry and that once it claims content is ingested whose wiki pages were lost, future `add` runs may skip that content silently. It treats this as a routine maintenance concern before merges, reverts, or repairs under `okf/`, not as a rare recovery edge case. That ties the concept directly to [[concepts/agent-ready-repositories]], [[concepts/documentation-architecture]], and [[concepts/agent-context-layering]].

## What must stay coherent

The lifecycle and workflow references describe several linked layers:

- the hash registry under `okf/.openkb/`, which records ingested content
- the stored raw document set under `okf/raw/`
- the compiled wiki under `okf/wiki/`
- the deterministic staged input under `okf/.okf-build/input/`, which feeds ingestion but is not itself the live knowledge base

Coherence means these layers agree about what documents exist, what evidence is still present, what was actually ingested, and what can be regenerated. When they drift apart, deterministic behavior works against recovery because deduplication prevents automatic reingestion of content the registry already knows.

The guidance sharpens this model by naming a practical integrity pair: even when the full system includes raw content, operators should especially watch the relationship between `okf/.openkb/hashes.json` and `okf/wiki/`, because that is where silent skips become visible as missing knowledge output. It also places this check inside a broader context order where `AGENTS.md` defines repo rules and `okf/wiki/` provides durable context, reinforcing [[concepts/documentation-source-priority]] and [[concepts/durable-context]] when deciding how to repair state.

## Main failure mode

The source documents highlight a specific risk:

- a document hash remains registered as ingested
- generated wiki pages are deleted, overwritten, or lost in a bad merge
- future `openkb add` runs skip the content because the hash is unchanged
- the missing pages do not come back on their own

This turns accidental wiki damage into a durable inconsistency. The problem is not only missing files; it is the mismatch between registry belief and actual compiled state.

The lifecycle reference adds an important nuance: this is not limited to obvious file loss. It can also show up as order-dependent staleness, where early-compiled pages never learn about concepts discovered later unless their source documents are recompiled against the current wiki. That is a different symptom from missing pages, but it reflects the same maintenance principle that machine-managed state must be deliberately refreshed when its dependent layers change.

The newer workflow guidance adds another dimension: generated pages that are weak, vague, duplicated, misclassified, or stripped of caveats should not be patched directly in `okf/wiki/`. If the wiki output is wrong, the repair path is to improve the committed source inputs and re-ingest. Coherence therefore includes not just file presence but preservation of reliable compiled meaning, linking the concept to [[concepts/caveat-preservation]] and [[concepts/human-in-the-loop-review]].

## Common causes of drift

The lifecycle policy, agent-readiness guidance, and orphan-retraction script together call out several ways coherence can be broken:

- hand-editing generated wiki files
- hand-editing the hash registry
- restoring or reverting `okf/wiki/` without the matching registry state
- merge or conflict-resolution mistakes touching `okf/`
- interrupted ingest or regeneration workflows
- writing generated material directly into `okf/raw/` or `okf/wiki/` instead of staging deterministic inputs first
- accepting generated changes without reviewing whether pages were lost, duplicated, misfiled, or weakened
- separating the registry from raw content or wiki state during cleanup or selective restoration
- changing ingestion structure or source-pack strategy in ways that alter hash behavior without understanding the downstream effect
- deleting repository sources while leaving the KB registry and compiled pages behind
- re-running ingestion without reconciling orphaned pipeline-owned documents

These are all examples of violating [[concepts/generated-content-governance]] and [[concepts/tool-boundaries]]. The guidance also adds a privacy and portability angle: registry entries can record absolute host paths when staged inputs live outside `okf/`, so keeping staging inside the KB root reduces both disclosure risk and machine-specific drift in committed registry state. That links coherence to [[concepts/privacy-preserving-tooling]] as well as ordinary maintenance discipline.

## Operational rule

The practical rule is to treat `okf/.openkb/hashes.json`, `okf/raw/`, and `okf/wiki/` as one machine-managed system, with `okf/.openkb/hashes.json` and `okf/wiki/` as the most visible integrity pair.

The source materials explicitly say not to hand-edit these layers and not to merge, revert, or restore one without the others. They also add a stronger workflow boundary: generated files should not be written directly into `okf/raw/` or `okf/wiki/`; deterministic source material belongs in `okf/.okf-build/input/` and enters the KB only through OpenKB ingestion, except for narrow user-approved conventions and tooling exceptions.

The maintenance expectation is concrete: after merges or reverts touching `okf/`, run `openkb --kb-dir ./okf lint` and read the report. More broadly, generated wiki changes should be reviewed before acceptance, and weak pages should be fixed by improving source evidence and re-ingesting rather than patching compiled output by hand.

This reflects a broader maintenance pattern: generated knowledge systems are safe only when their machine-managed layers are preserved together. It also aligns with [[concepts/safe-automation]], [[concepts/human-in-the-loop-review]], and [[concepts/single-source-of-truth]], because coherence depends on deliberate review gates around machine-managed state and repair through authoritative inputs.

## Detection and validation

The documents recommend checking coherence after any merge, revert, or conflict resolution involving `okf/`.

Several mechanisms support this:

- `openkb --kb-dir ./okf lint` reports structural coherence issues across registry, raw content, and wiki state
- the guidance specifically says to read the lint report, not merely run the command
- the repository validator acts as a stricter pass/fail gate for structural quality checks
- generated wiki changes should be reviewed for duplicates, vague names, entity/concept misfiles, lost caveats, and citation grounding
- final wiki validation is required before concluding the workflow
- a concept or entity page missing its machine-managed `sources:` metadata is itself a coherence warning because the citation chain has been damaged
- `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list` help confirm what the KB currently believes before further ingest or repair
- the orphan-retraction script can identify pipeline-owned documents whose repository source has been deleted, renamed, or merely deselected, helping separate real deletions from policy changes
- its `--preview` mode shows OpenKB's own removal plan via `remove --dry-run`, and its manifest-first reconciliation path keeps orphan detection aligned with the builder when the pack manifest is present

The lifecycle reference also clarifies the difference between health reporting and gating: `openkb lint` always completes and writes findings into `okf/wiki/reports/`, while the repository validator is the non-LLM pass/fail enforcement layer. That places hash registry coherence within the broader framework of [[concepts/deterministic-validation]], [[concepts/okf-validation]], [[concepts/quality-gates]], [[concepts/executable-validation]], and [[concepts/validation-vs-health-reporting]].

## Repair paths

The source materials give a two-branch recovery model:

- If `okf/raw/` still contains the document, use `recompile <doc>` to regenerate the missing wiki pages.
- If raw content is also missing, remove the registered document entry, using a dry run first, and then re-add the original source.

The lifecycle reference adds more precise operating policy around those repairs:

- use `recompile <doc> --dry-run` before the real run
- use `remove <doc> --dry-run` before clearing a registry entry
- reserve broader rebuild actions such as `--all` for explicit consent
- use recompilation not only for missing pages but also for order-dependent staleness when a page was compiled before later concepts existed

The orphan-retraction script extends that repair model for repository deletions. It treats the OpenKB registry as the inverse of source removal: when a repo file disappears, pipeline-owned KB documents that no longer correspond to current staged names become candidates for retraction. It prefers a freshly built source-pack manifest when present, falls back to git-derived expectations when necessary, and classifies removals as deleted, deselected, or renamed. That makes deletion reconciliation deterministic while still protecting intentionally kept external documents and pseudo-documents that are always regenerated.

The script also adds two important safety properties to the repair workflow:

- it is report-only by default, so coherence checks can be run without mutation
- it refuses large-scale automatic retraction unless the user overrides the guard with `--force`, reducing the risk that a stale manifest or wrong bundle depth deletes too much

The workflow guidance complements this by recommending dry-run previews before destructive or broad changes and by explicitly placing `remove` and `recompile` behind ask-first review gates. That framing matters because registry/output drift can look simple while actually requiring a state-changing repair with irreversible side effects if handled carelessly.

Recovery should happen through `openkb` commands, not through manual file reconstruction.

## Relationship to staging and regeneration

Hash registry coherence also explains why staging alone is not enough. Rebuilding `.okf-build/input/` does not update `okf/raw/` or `okf/wiki/` by itself. The staged source must still pass through the ingestion and regeneration workflow governed by OpenKB.

That ties this concept to [[concepts/evidence-staging]] and [[concepts/source-driven-regeneration]]: authoritative repair comes from reprocessing approved source material, not from editing compiled output.

The guidance adds several refinements:

- staged inputs should be rebuilt deterministically and checked with `status` and `list` before ingestion
- generated source packs and manifests prepare evidence but do not alter the live KB until `openkb add` runs
- for large repositories, source-pack bundling can change hash behavior across the whole corpus, so teams should choose bundling strategy early and keep it stable
- external files or URLs should be added only with consent and disclosure because they alter both provenance and registry state
- staging inside `okf/` helps keep registry paths portable and reduces host-path leakage
- manifest-based orphan detection and git-based fallback checks help keep source-pack expectations aligned with the registry during deletion cleanup

The workflow also emphasizes that external documentation should be materialized into evidence with provenance before ingestion, linking coherence to [[concepts/data-flow-disclosure]], [[concepts/external-documentation]], [[concepts/provenance-tracking]], and [[concepts/web-evidence-ingestion]].

## Broader implication

This concept captures a core lesson of OpenKB maintenance: deterministic systems preserve integrity only when their state layers remain aligned. Hash-based deduplication improves reproducibility, but it also means corrupted, incomplete, or stale state can persist unless operators deliberately restore coherence through supported workflows.

The newer maintenance guidance shows that hash registry coherence is not only a storage concern but also a governance concern. Repository teams need routine review, validation, source-driven repair discipline, clear boundaries between generated knowledge and editable source artifacts, explicit consent around potentially destructive maintenance actions, stable staging practices, and careful handling of citation metadata to keep deterministic behavior trustworthy.

## See also

- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]
- [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[concepts/generated-content-governance]]
- [[concepts/source-driven-regeneration]]
- [[concepts/evidence-staging]]
- [[concepts/provenance-tracking]]
- [[concepts/deterministic-validation]]
- [[concepts/okf-validation]]
- [[concepts/quality-gates]]
- [[concepts/tool-boundaries]]
- [[concepts/safe-automation]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/validation-vs-health-reporting]]
- [[entities/openkb]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]