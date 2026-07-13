---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md"]
description: "Workflow for promoting verified findings into compiled KB knowledge."
---

# Findings Promotion

Findings Promotion is the workflow for turning a captured discovery in `okf/wiki/explorations/findings/` into compiled wiki knowledge when it is still true and fills a gap, corrects a mismatch, or otherwise needs to become durable KB content.

This concept is described in [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]], where it is treated as part of the OpenKB lifecycle for maintaining the KB without hand-editing generated pages. It also connects to [[concepts/findings]], knowledge gap, [[concepts/source-grounded-regeneration]], [[concepts/provenance-tracking]], and [[concepts/registry-drift]].

## What gets promoted

A finding is eligible for promotion when:
- it is still true at HEAD
- it is supported by evidence such as a file, commit, command output, or test run
- a compiled `concepts/` or `entities/` page misses it or contradicts it

Promotion is for discovered knowledge, not for procedure docs or harness notes. The lifecycle document distinguishes findings from skill material and tooling context by routing procedure into skills and runtime observations into tooling pages instead.

## Promotion flow

The lifecycle is deliberately conservative:
- capture the finding as a markdown page under `okf/wiki/explorations/findings/`
- verify it against the current repository state
- stage it as `okf/.okf-build/findings/finding-<topic>.md`
- ingest it with `openkb --kb-dir ./okf add ./okf/.okf-build/findings/`
- delete the capture page and its index entry in the same change

The staged promoted page becomes durable knowledge in `okf/raw/` and its compiled wiki outputs can then participate in normal citation chains and regeneration. Promotion uses the same ingest path as other staged content, but with a dedicated staging location so promoted findings do not collide with repository-pack staging or get swept up by orphan reconciliation.

## Why the dedicated path matters

The document emphasizes several safeguards:
- findings are writable notes, while compiled namespaces are projection outputs
- `query --save` and chat saves write to the explorations root, so the `findings/` subdirectory avoids collisions
- staging inside the KB root keeps registry paths KB-relative and avoids leaking absolute paths
- promoted findings are outside automatic orphan reconciliation by design

This makes promotion a controlled handoff from observation to compiled truth, while preserving provenance and minimizing accidental overwrites. It also keeps the findings workflow distinct from general [[concepts/evidence-staging]], [[concepts/documentation-layer-separation]], and [[concepts/knowledge-capture-boundaries]].

## Relation to the KB lifecycle

Findings promotion sits inside a larger loop of source-grounded regeneration, incremental compilation, and knowledge lifecycle governance. It complements the correction loop: source defects are fixed in committed source documents, while genuine knowledge gaps are captured and promoted as findings.

The page also ties into provenance tracking, evidence staging, registry drift, and orphan retraction, because promotion depends on clean evidence, staged input, and deterministic OpenKB mutation behavior. The lifecycle guidance also makes clear that promoted findings can coexist with stale repository docs that say otherwise; both remain sources, and the compiled wiki should retain that tension until the source landscape changes.

## Key idea

Promotion is not automatic synthesis. It is a deliberate act of elevating verified discovered knowledge into the KB when existing compiled pages are incomplete or stale.

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]