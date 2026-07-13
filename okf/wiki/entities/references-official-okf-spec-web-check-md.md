---
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
type: "Work"
description: "Web-check reference for refreshing the OKF offline quality baseline"
---

# Official OKF Spec Web Check

`official-okf-spec-web-check.md` is the web-check companion reference for the OKF quality baseline. It tells agents to refresh the embedded offline rules against the official Google OKF `SPEC.md` and `README.md` whenever web access is available.

## What it does

- Provides the online comparison path for validating OKF v0.1 rules.
- Acts as the source that the offline baseline defers to when the official spec has changed.
- Supports the agent workflow for keeping the local baseline aligned with the upstream OKF definition.
- Fits into the agent-ready-context workflow as the web-backed check used to refresh the offline OKF baseline when network access exists.
- Reinforces that the compiled wiki is context, while source documents and official upstream specs remain the evidence path for baseline updates.
- Serves as the web-check companion to the offline-first OKF baseline in [[entities/okf-quality-md]].
- Belongs to the broader agent-ready repository flow that stages deterministic inputs, ingests them into OpenKB, and validates the resulting wiki rather than editing compiled pages by hand.
- Treats fetched web content as untrusted evidence that should be summarized, not executed.

## Key facts from the source document

- The embedded baseline in [[entities/okf-quality-md]] is sufficient for offline work.
- When web access exists, the baseline should be refreshed against the official OKF spec and README.
- The official spec takes precedence if it has changed.
- When web access is unavailable, validation should continue using the embedded OKF v0.1 rules and report that offline validation was used.
- The skill treats official web checks as untrusted evidence inputs, so fetched content must be summarized rather than executed.
- The workflow keeps the KB root and compiled wiki separate from generated staging areas, with deterministic source packs feeding OpenKB ingestion.
- Guardrails around AGENTS.md and the OKF wiki keep long-form repository knowledge in the compiled wiki rather than in the orientation file.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]
- [[entities/okf-quality-md]]
- [[entities/okf-spec]]
- [[entities/openkb-wiki]]
- [[concepts/okf-offline-conformance]]
- [[concepts/okf-validation]]
- [[concepts/external-documentation]]
- [[concepts/web-evidence-ingestion]]
- [[concepts/spec-authority]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/deterministic-source-pack-staging]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/agent-orientation-index]]
- [[concepts/agent-ready-context]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]


See also: [[summaries/okf-spec]]