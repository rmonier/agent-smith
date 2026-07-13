---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "How vendored skills are adopted, pinned, and kept optional in workflows."
---

# Vendor Skill Adoption

Vendor skill adoption is the practice of bringing external skill packages into a repository as immutable, project-scoped guidance so the workflow can use them without relying on a user-wide installation or a harness-specific setup. It sits at the intersection of [[concepts/tooling-vendoring]], [[concepts/toolchain-pinning]], [[concepts/consent-first-tooling]], and [[concepts/graceful-degradation]].

## What it means

A vendor skill is not treated as a normal code dependency or an implicit runtime requirement. Instead, it is copied into the repository's skill space, usually under `.agents/skills/`, before the corresponding CLI is used. The vendored copy becomes the durable, repository-local source of usage knowledge for that tool.

This approach keeps the workflow aligned with [[concepts/local-by-default-tooling]] and [[concepts/tooling-context-isolation]]: the repo carries the guidance it needs, while the host machine stays out of scope unless the user explicitly asks for a broader install.

## Core rules

- Vendoring is part of the adoption decision, not an afterthought.
- The vendored skill should be treated as immutable vendor content.
- Updates happen by re-vendoring from a newer pinned upstream version, not by editing the copied files in place.
- The skill copy should exist before the CLI is invoked, so the repository always has a committed, inspectable explanation of how that tool is expected to behave.
- Adoption must remain consent-first and project-scoped, with clear fallback behavior when a skill is unavailable.

## How the source document applies this concept

The source document [[summaries/agents__skills__agent-ready-context__references__dependencies-md]] defines a concrete vendor-skill policy for the `agent-ready-context` skill. It distinguishes between:

- hard local requirements such as `git`, `uv`, and Python 3.11+
- optional tools such as `graphify` and `openkb`
- companion skills that are useful but not mandatory

That separation is an example of [[concepts/skill-governance]] and [[concepts/minimal-tool-scoping]]: the workflow should not fail just because a companion skill is missing.

## Relationship to other concepts

Vendor skill adoption depends on [[concepts/provenance-tracking]] and [[concepts/integrity-pinning]] because each installed skill version should be tied to a known upstream source and a recorded integrity value. It also supports [[concepts/supply-chain-security]] by making the adoption path explicit and auditable.

It is closely related to [[concepts/evidence-backed-skill-initialization]], because the vendored copy acts as the evidence-backed local reference for how a skill should be initialized and used. The same pattern reinforces [[concepts/graceful-degradation]] when a skill or CLI is absent: the workflow should continue in a reduced mode rather than stopping.

## Practical implications

- The repo should carry the pinned skill copy, not just a note that the tool exists.
- The main CLI and its vendored skill should be kept in sync.
- Optional companion skills can be advertised as follow-up capabilities without becoming blockers.
- If a package or mirror mismatch appears, the workflow should stop and report rather than silently substituting another source.

## Why it matters

This concept turns third-party skills into stable, reviewable inputs to the knowledge pipeline. That makes the repository easier to bootstrap, safer to audit, and less dependent on hidden environment state. It also keeps compiled knowledge grounded in a local, versioned skill source instead of in ad hoc operator memory or harness behavior.


See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]