---
type: "Concept"
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md"]
description: "Canonical spec rules outrank local baselines, validators, and compiled context."
---

# Specification Authority

Specification authority is the rule that the canonical external specification is the final decision-maker when local guidance, embedded baselines, validators, installation policy, or compiled knowledge outputs disagree.

## Core idea

In this workflow, local reference material, validation scripts, dependency guidance, and repository orientation files are designed to support an [[concepts/offline-first-workflows]] process, but they do not outrank the official specification. Embedded rules are useful for speed, resilience, repeatable checks, and safe repository setup, yet they remain secondary when fresher authoritative guidance is available.

The OKF quality baseline in `summaries/agents__skills__agent-ready-context__references__okf-quality-md` makes this explicit: it is intentionally sufficient for offline creation, refresh, and validation of a practical bundle, but it must be refreshed against the official Google OKF `SPEC.md` and `README.md` when web access is available. The official spec wins if it has changed. The local validator extends that baseline into executable checks, including hard OKF conformance rules and stricter repository-oriented warnings, but those checks still inherit their legitimacy from the upstream specification rather than replacing it. The dependency guidance in `summaries/agents__skills__agent-ready-context__references__dependencies-md` applies the same principle to tools: local metadata, permission hints, vendoring requirements, and prereq checks organize execution, but package identity and install instructions are still anchored to authoritative upstream sources. The repository workflow in `summaries/agents__skills__agent-ready-context__SKILL-md` adds the same rule at the process level: the durable context in `okf/wiki/`, the local `AGENTS.md` orientation, and project skills all have different roles, but none of those local structures is allowed to overrule the official specification they depend on. This makes specification authority a concrete operational rule rather than a vague preference.

## How it works in practice

The source document `summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md` describes a web refresh procedure for checking the latest official OKF guidance. The process starts from the official specification and uses local materials as a baseline for comparison.

The embedded OKF quality reference complements that process by defining an offline baseline for bundle structure, reserved filenames, concept document requirements, index and log conventions, and hard conformance rules. Its model is explicit: an OKF bundle is a directory tree of UTF-8 Markdown files; `index.md` and `log.md` are reserved names; non-reserved Markdown files need YAML frontmatter; and every concept document needs a non-empty `type` field. It also defines the local layout conventions for `okf/wiki/`, treats root `index.md` and `log.md` as reserved navigation files, and describes when `index.md` may carry version metadata. The validator summarized in `summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py` operationalizes those expectations by checking Markdown bundles for required frontmatter, reserved-file handling, root index behavior, and OpenKB-specific checks such as broken wikilinks and missing machine-managed `sources:` metadata. That baseline is meant to keep work moving offline, not to replace upstream authority.

The same pattern appears in the dependency reference. `summaries/agents__skills__agent-ready-context__references__dependencies-md` states that `SKILL.md` should remain spec-compliant, that `allowed-tools` is only a permission hint, and that readiness is determined by an executable prereq check rather than by invented schema fields. It also says that installable tool identity must be verified against authoritative upstream repositories, not inferred from stale local notes or ambiguous package names. In practice, that means the workflow uses local documentation to explain what to do, but it resolves package-name conflicts, source conflicts, and vendoring rules by checking the real upstream project.

The repository workflow adds another practical layer. `summaries/agents__skills__agent-ready-context__SKILL-md` says the durable context source of truth inside the repository is `okf/wiki/`, but that local source of truth is still subordinate to the official OKF materials when there is a conflict. The same document requires the agent to refresh the offline baseline with the official `SPEC.md` and `README.md` when web access is available, to follow the official spec if there is a mismatch, and to report that mismatch rather than silently enforcing stale local behavior. It also distinguishes between compiled wiki output, repository policy, and evidence: the wiki is useful context, but claims promoted into instructions must still be traced through their citation chain back to authoritative sources. This prevents compiled knowledge or repository conventions from being mistaken for standards authority.

When web access is available, the workflow checks the current official rules for items such as:

- OKF version
- bundle structure
- reserved filenames
- concept document rules
- version declaration requirements
- conformance expectations
- canonical tool package names and upstream repositories
- project-scoped vendoring behavior when a tool's own documentation defines it
- privacy- and provider-related requirements when the official docs define them

Local validation and bootstrap guidance still matter, but they serve as supporting [[concepts/quality-gates]] and [[concepts/dependency-management]] mechanisms rather than the ultimate source of truth.

## Relationship to local validation

This concept does not reduce the value of local checks. Instead, it clarifies their role. Local validators help enforce consistency, catch mistakes early, and support [[concepts/deterministic-validation]]. However, if a validator conflicts with the official specification, the validator is treated as stale, overly strict, or otherwise in need of maintenance.

The OKF validation script makes this distinction unusually clear because it mixes strict conformance checks with additional repository-protective heuristics and project policy. Alongside spec-facing checks, it warns about unclosed code fences, flags near-duplicate sibling filenames by normalized slug, and in OpenKB wiki mode treats broken wikilink integrity as errors while warning on missing machine-managed `sources:` metadata in generated pages. These checks are valuable for [[concepts/filesystem-validation]], [[concepts/generated-content-governance]], and repository health, but they are not automatically part of the upstream standard.

The dependency workflow adds a parallel example. `check_prereqs.py` is the executable source of truth for local readiness, but not for standards authority. It can declare that `uv`, Python 3.11+, writable paths, or vendored skills are required for this repository workflow; it can also enforce project-scoped expectations before `graphify` or `openkb` are used. Those are legitimate local operational checks, especially for [[concepts/skill-vendoring]], [[concepts/tool-boundaries]], and [[concepts/safe-automation]], but they still sit beneath upstream specification and upstream package provenance.

The broader workflow adds an important compiled-output example. `summaries/agents__skills__agent-ready-context__SKILL-md` instructs agents not to hand-edit generated wiki pages when they are weak or wrong, but to improve committed sources and re-ingest instead. That means local wiki output, even when treated as the repository's durable context, is still governed by upstream rules, source evidence, and regeneration policy rather than by ad hoc patching. In the same way, `AGENTS.md` is an orientation document and not the place to redefine canonical standards. The result is a layered model in which local validation, local context, and local operating rules are enforceable, but none becomes the spec merely by existing in the repository.

That separation matters operationally. The validator states that the agent should web-check the official OKF specification before relying on the local validator, and the dependency reference states that if older local docs conflict with the verified upstream repository, the upstream source wins. Its package table is explicit that package identity must be checked carefully, such as `graphify` being installed from the `graphifyy` package rather than a similarly named alternative. In other words, a validator or bootstrap guide can legitimately enforce local policy while still remaining subordinate to the canonical spec and canonical upstream source. That makes specification authority a practical companion to [[concepts/source-trust-levels]] and [[concepts/provenance-tracking]]: different sources are not equally authoritative, and the workflow must distinguish between convenient local guidance, executable local policy, repository-specific rules, compiled context, and canonical upstream standards.

## Why it matters

Without a clear authority rule, teams can become trapped between embedded documentation, local validators, compiled wiki pages, mirrored package indexes, and evolving external standards. Specification authority prevents that ambiguity by establishing a simple resolution rule:

- use embedded guidance when offline
- prefer the official specification when it is available and more current
- treat local quality gates as policy rather than spec by default
- treat validator-added heuristics and repository conventions as layered governance unless confirmed upstream
- treat generated wiki content and `AGENTS.md` guidance as operational aids, not canonical standards
- verify tool identity and install provenance against authoritative upstream sources
- report mismatches so local references, validators, compiled context, and bootstrap instructions can be updated

This keeps the workflow aligned with [[concepts/external-documentation]] while preserving the operational benefits of [[concepts/offline-first-workflows]]. It also helps separate package provenance questions from installation convenience: a configured mirror may be the delivery path, but the upstream repository still anchors what the tool actually is.

## In the OKF refresh workflow

In the referenced documents, the official OKF materials are the authoritative source, while the embedded OKF baseline and local validator are operational aids. The dependency reference extends the same model to tool adoption: local prereq checks, pin records, and vendoring rules are repository controls, while upstream specifications and repositories define the canonical identity of the things being installed. The main workflow summary in `summaries/agents__skills__agent-ready-context__SKILL-md` extends the same model to repository context: `okf/wiki/` is the durable local context source of truth, but it is still regenerated from staged evidence, checked against official OKF guidance, and reviewed as compiled output rather than treated as self-justifying authority. The concept therefore supports a disciplined update loop:

- consult official upstream documentation
- compare it against local baseline material
- run local validation
- verify tool names, provenance, and expected install behavior against upstream sources
- distinguish spec violations from local policy failures
- distinguish compiled-context issues from standards issues
- resolve conflicts in favor of the official spec or authoritative upstream source
- treat disagreements as maintenance signals for local tooling, references, and generated context

This matters especially when a local validator adds repository-specific rules, such as OpenKB wiki checks, broken-link enforcement, traceability warnings for generated pages, or project-scoped vendoring requirements for tool-provided skills. Those rules can be valuable and enforceable within the project, but they should be understood as local governance layered on top of the spec rather than as replacements for it.

## Related concepts

- [[concepts/offline-first-workflows]]
- [[concepts/deterministic-validation]]
- [[concepts/quality-gates]]
- [[concepts/source-trust-levels]]
- [[concepts/external-documentation]]
- [[concepts/dependency-management]]
- [[concepts/provenance-tracking]]
- [[concepts/skill-vendoring]]
- [[concepts/tool-boundaries]]
- [[concepts/trust-on-first-use]]
- [[concepts/version-pinning]]
- [[concepts/supply-chain-security]]

See also: `summaries/agents__skills__agent-ready-context__SKILL-md`

See also: `summaries/agents__skills__agent-ready-context__references__dependencies-md`

See also: `summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md`

See also: `summaries/agents__skills__agent-ready-context__references__okf-quality-md`

See also: `summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py`

See also: `summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py`

See also: `summaries/agents__skills__subagent-profile-adapter__SKILL-md`

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]


See also: [[summaries/agent-skills-spec]]