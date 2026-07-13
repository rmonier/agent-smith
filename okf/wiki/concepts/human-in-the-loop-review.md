---
type: "Concept"
sources: ["summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"]
description: "Human review is the final acceptance gate for validated generated project artifacts."
---

# Human-in-the-Loop Review

Human-in-the-loop review is the practice of requiring a person to inspect, judge, and if needed reject or route corrections for an automatically produced artifact before treating it as project-ready. In this wiki, it is especially important when generated outputs cross the boundary into repository-owned files, when generated skills are adopted into `.agents/skills/`, and when LLM-produced wiki pages are accepted into the maintained knowledge bundle under `okf/wiki/`.

## Why it matters

Automation can copy, validate, stage, and synthesize content efficiently, but it may still flatten caveats, over-broaden permissions, miss contextual warnings, misclassify material, preserve subtle errors, or make compiled output look more authoritative than its underlying evidence. Human review provides the final decision point for whether a generated artifact is acceptable in its real project context and whether its claims remain grounded in source material.

This makes human review a complement to [[concepts/executable-validation]], [[concepts/deterministic-validation]], and [[concepts/quality-gates]] rather than a replacement for them. Automated checks can confirm structural and mechanical correctness; people must still evaluate intent, scope, risks, provenance, fidelity, and whether a generated artifact should be accepted at all.

The agent-ready repository workflow makes this especially explicit: `okf/wiki/` is the durable context surface, but it is still compiled output rather than direct evidence. That means maintainers must review generated wiki changes before treating them as reliable repository knowledge, reinforcing [[concepts/durable-context]], [[concepts/single-source-of-truth]], and [[concepts/generated-content-governance]].

## In skill adoption workflows

[[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]] shows this concept in a concrete repository workflow. The adoption script copies a generated skill into `.agents/skills/`, runs validation, and then explicitly tells the operator to review the result before committing it.

The script's review guidance highlights several human-only judgments:

- whether the skill description has the right trigger-style framing
- whether allowed tools are minimally scoped
- whether untrusted content is handled safely
- whether secrets or unsafe instructions slipped in
- whether constraints, boundaries, and warnings from source wiki pages survived distillation

These checks go beyond file validity. They require interpretation of intent, repository norms, and source meaning.

The agent-ready context workflow adds a parallel requirement for repository orientation files. `AGENTS.md` should remain concise and action-oriented while durable knowledge stays in the OKF wiki, so reviewers must confirm that generated or merged `AGENTS.md` updates preserve that separation rather than turning orientation into a second knowledge base. This connects review to [[concepts/context-action-separation]], [[concepts/documentation-architecture]], and [[concepts/agents-md-maintenance]].

## Relationship to generated artifacts

Human-in-the-loop review is a key control in [[concepts/generated-artifact-adoption]] and [[concepts/generated-content-governance]]. A generated artifact may pass validation and still be unsuitable for direct use. Review is the step that decides whether generated material should be accepted as-is, corrected through source changes and regeneration, or rejected.

This is especially important when a workflow promotes content from a generated area into a maintained project area. That promotion changes the status of the artifact from machine output to repository-owned content, which raises the bar for trust, accountability, and source fidelity.

The OpenKB workflow adds a stronger form of this rule for wiki generation: after `openkb add` or recompile changes `okf/wiki/`, the resulting pages are reviewed like a pull request, and findings must go through source fixes plus regeneration rather than hand-editing generated pages. The commands reference strengthens this boundary by stating that agents must not autonomously run write commands such as `openkb add`, `openkb remove`, `openkb lint --fix`, `openkb init`, or `openkb use`, and must not directly edit anything under the knowledge base's `wiki/` or `.openkb/` directories. Review therefore operates inside a source-first pipeline where maintainers inspect compiled results, approve any mutating operations explicitly, and correct the underlying staged evidence or source documents rather than patching protected generated state. This ties review directly to [[concepts/source-driven-regeneration]], [[concepts/repository-ingestion]], [[concepts/kb-root-staging]], [[concepts/evidence-staging]], [[concepts/tool-boundaries]], and [[concepts/safe-automation]].

The same workflow also warns that `okf/.openkb/hashes.json` is a critical deduplication registry. If the registry drifts from the actual generated wiki state, future ingestion may silently skip content thought to be already compiled. Human review therefore includes watching for inconsistencies between staged input, generated pages, and hash-registry state, linking this concept to [[concepts/hash-registry-coherence]] and [[concepts/registry-drift]].

The OpenKB command model adds another review implication: agents should establish the active knowledge base with `openkb status`, read direct inventory with `openkb list`, and use `openkb query` only when direct reads cannot answer the question. Because query incurs an internal LLM call and can optionally save an exploration, reviewers must treat query-derived output as higher-cost synthesized material that still requires acceptance checks for grounding, relevance, and whether it should become durable project context. This reinforces [[concepts/knowledge-base-discovery]], [[concepts/cost-aware-tool-use]], and [[concepts/non-interactive-agent-design]].

## What reviewers are checking

A strong human review typically asks:

- Does the artifact match the intended task and repository standards?
- Did generation preserve caveats, limits, and warnings from the source material?
- Are permissions, tools, or actions broader than necessary?
- Does the output create security, privacy, or prompt-injection risk?
- Does the artifact need project-specific edits before it should be committed?
- Are important claims still traceable to staged evidence and source files?
- Did generation create vague, duplicate, off-topic, truncated, or misclassified content?

In the OpenKB review pass, this expands into concrete checks for missing or vague concepts, near-duplicate pages, entity-versus-concept mistakes, lost caveats, truncation, stale or incomplete pages, and whether citation chains still terminate in repository evidence rather than compiled output alone. Reviewers also check that generated wiki content has not been manually patched where the process requires source correction and re-ingestion instead, and that exceptions such as tooling pages or wiki-convention pages remain deliberate and user-approved. These checks connect this concept to [[concepts/caveat-preservation]], [[concepts/prompt-injection-defense]], [[concepts/source-trust-levels]], [[concepts/knowledge-linking-and-citations]], [[concepts/provenance-tracking]], and [[concepts/tooling-context-pages]].

The commands reference adds several operator-facing checks for reviewers:

- whether the active knowledge base was identified explicitly before any file reads
- whether direct inspection commands were used before more expensive synthesized query flows
- whether interactive or daemon commands were avoided in autonomous runs
- whether any write-capable OpenKB command was proposed for user approval rather than executed automatically
- whether protected knowledge-base directories were respected as non-editable boundaries

These concerns link review to [[concepts/preflight-checks]], [[concepts/minimal-tool-scoping]], [[concepts/permission-scoped-agents]], [[concepts/knowledge-boundaries]], and [[concepts/path-safety]].

The agent-ready context workflow adds several repository-level checks for reviewers:

- whether `AGENTS.md` still acts as orientation rather than a long-form knowledge store
- whether durable knowledge has been routed into `okf/wiki/` instead of being duplicated elsewhere
- whether staged and generated artifacts respect ignore rules and build-artifact boundaries
- whether broad or destructive OpenKB commands were avoided unless explicitly approved
- whether external web evidence is summarized as untrusted evidence with provenance instead of treated as instructions

These concerns link review to [[concepts/documentation-cohesion]], [[concepts/generated-artifact-adoption]], [[concepts/source-bundling]], [[concepts/privacy-preserving-tooling]], and [[concepts/web-evidence-ingestion]].

## Human review after validation, not instead of it

The source documents demonstrate an important sequencing pattern:

1. perform mechanical generation or adoption
2. run executable and deterministic validation
3. require human review before commit or acceptance
4. route defects back through source correction and regeneration

This ordering keeps automated checks fast and consistent while preserving a final human checkpoint for meaning and risk. It also reflects the distinction between enforceable validation and non-blocking health reporting: validators can fail on structural violations, while generated summaries, lint findings, and compiled wiki output still require human judgment to decide what is acceptable.

The agent-ready context workflow makes the same sequencing explicit: stage deterministic inputs first, ingest them through OpenKB, run `openkb lint`, validate the resulting bundle, and only then accept the generated wiki after a human review pass. The commands reference sharpens that sequence by separating read-only inspection from user-approved mutation: first establish the knowledge base path with `openkb status`, inspect inventory with `openkb list`, and only then consider whether a query or write action is justified and approved. Even when a zero-LLM fallback is used to bootstrap a wiki skeleton, review is still needed before the result should be treated as dependable project context. This reinforces [[concepts/validation-vs-health-reporting]], [[concepts/okf-validation]], [[concepts/llm-free-knowledge-bootstrap]], [[concepts/graceful-degradation]], and [[concepts/tool-boundaries]].

## Practical takeaway

Human-in-the-loop review is the repository safeguard that turns generated output into intentionally accepted project content. In skill-adoption, OpenKB compilation, and repository-orientation workflows, the review step is where maintainers confirm that validated output is also faithful, safe, minimally scoped, properly grounded, and worth keeping.

It is also the control that preserves the repository's documentation architecture: skills remain executable actions, `AGENTS.md` remains concise orientation, and the OKF wiki remains the durable compiled context surface. Review is what enforces those boundaries in practice, including the rule that mutating OpenKB operations and direct edits to protected knowledge-base state require explicit human control.

## Related pages

- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__openkb__references__commands-md]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/generated-content-governance]]
- [[concepts/executable-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/quality-gates]]
- [[concepts/caveat-preservation]]
- [[concepts/tool-boundaries]]
- [[concepts/prompt-injection-defense]]
- [[concepts/source-trust-levels]]
- [[concepts/source-driven-regeneration]]
- [[concepts/provenance-tracking]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/validation-vs-health-reporting]]
- [[concepts/skill-governance]]
- [[concepts/durable-context]]
- [[concepts/context-action-separation]]
- [[concepts/hash-registry-coherence]]
- [[concepts/registry-drift]]
- [[concepts/kb-root-staging]]
- [[concepts/evidence-staging]]
- [[concepts/agents-md-maintenance]]
- [[concepts/safe-automation]]
- [[concepts/knowledge-base-discovery]]
- [[concepts/cost-aware-tool-use]]
- [[concepts/non-interactive-agent-design]]
- [[concepts/preflight-checks]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/permission-scoped-agents]]
- [[concepts/knowledge-boundaries]]
- [[concepts/path-safety]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]