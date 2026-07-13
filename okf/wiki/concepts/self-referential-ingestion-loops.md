---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md"]
description: "Ingestion loops that re-ingest generated KB output and amplify themselves."
---

# Self-Referential Ingestion Loops

A self-referential ingestion loop happens when a repository ingestion pipeline stages or re-ingests artifacts that were produced by the knowledge base itself. Instead of reflecting the source repository, the pipeline begins to consume its own outputs, creating a feedback cycle where generated documents feed back into generation again.

This concept is central to `build_okf_source_pack.py`, which explicitly guards against staging a graph report that appears to reference KB output paths. The script treats that situation as a failure mode because it can create a loop like source -> graph -> report -> ingest -> wiki -> graph, which never converges.

## Why It Matters

Self-reference breaks the boundary between source material and generated knowledge. Once that boundary collapses, several problems appear:

- duplicated or unstable content across ingestion runs
- unnecessary re-compilation from unchanged generated artifacts
- noisy diffs and churn in staged hashes
- recursive dependence on the KB's own output rather than repository truth
- reduced trust in staged provenance and source selection

This is closely related to [[concepts/source-pack-staging]], [[concepts/generated-artifact-adoption]], [[concepts/source-provenance]], and [[concepts/self-reference-control]].

## How the Script Avoids the Loop

The script stages a graph report only after applying a safety check. It normalizes the report text, strips run-dependent timestamps, and then scans for references to KB-root paths such as `okf/wiki`, `okf/raw`, `okf/.openkb`, or `okf/output`. If the report references those paths enough times, the script refuses to stage it and prints a warning telling the user to exclude `okf/` from graphification output.

This is a practical example of [[concepts/knowledge-graph-feedback-loops]] and [[concepts/self-reference-control]] in a repository ingestion pipeline.

## Key Design Ideas

- Generated artifacts are not automatically safe just because they are structured or useful.
- A pipeline should distinguish between external source content and content produced by earlier stages of the same pipeline.
- Detection should be loud and actionable, not a silent omission.
- Preventing the loop earlier is better than trying to clean up after it has already entered the KB.

## Relation to the Source Pack Builder

In `build_okf_source_pack.py`, the guard exists specifically for `graphify-out/GRAPH_REPORT.md`. The script treats that file as useful only if it does not look like it was compiled from the KB itself. This keeps the staged pack aligned with repository reality and supports [[concepts/deterministic-builds]], [[concepts/repository-ingestion]], and [[concepts/evidence-staging]].

The script's warning also points to a maintenance path: adjust graphification filters, rebuild the graph report, then stage again. That workflow reflects the broader idea that ingestion pipelines should preserve documentation boundaries and avoid consuming their own downstream outputs as upstream evidence.

## Related Concerns

- [[concepts/graph-integrity-diagnostics]] for detecting structural problems in graph-derived artifacts
- [[concepts/idempotent-graph-import]] for keeping repeated imports stable
- [[concepts/knowledge-graph-feedback-loops]] for the broader class of recursive knowledge contamination
- [[concepts/generated-content-governance]] for deciding which generated artifacts should be admitted into the KB
- [[concepts/validation-vs-health-reporting]] for separating useful diagnostics from ingestible source material

## Source Link

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]