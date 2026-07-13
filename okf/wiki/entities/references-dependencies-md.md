---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md"]
type: "Work"
description: "Reference guide for dependency and tooling guidance in skill workflows"
---

# Dependencies

`references/dependencies.md` is a supporting reference for [[entities/skill-creator]] and related skill-authoring workflows. It is treated as a dependency-focused guide rather than a standalone narrative document.

## Role

The page provides shared guidance for declaring tool requirements, companion-skill relationships, vendor skill notes, and provenance-safe setup rules without inventing non-standard dependency fields in `SKILL.md`.

It also supports the broader agent-ready repository workflow by defining how tooling, pins, and bootstrap requirements should be handled before the agent-ready context pipeline runs.

## What It Covers

- Naming and declaring dependencies in a skill-safe way
- Using namespaced metadata keys instead of ad hoc dependency fields
- Reusing the shared dependency vocabulary across skills
- Guiding when to consult dependency details during skill creation or updates
- Tool adoption rules, including explicit consent before installing optional tooling
- Vendoring read-only vendor skills before first CLI use
- Build and validation prerequisites for agent-ready repository setup

## Why It Matters

The skill-creator document relies on this reference to keep skill metadata consistent and portable. It helps ensure dependency information stays structured, minimal, and compatible with Agent Skills conventions.

The same guidance also reinforces [[concepts/consent-first-installation]], [[concepts/toolchain-pinning]], [[concepts/skill-vendoring]], and [[concepts/deterministic-validation]] in the repository agent-ready workflow.

## Related Usage

The reference is part of the broader skill-authoring toolkit alongside initialization, validation, and vendor-skill management guidance.

In the agent-ready context, it is also one of the key documents consulted before bootstrapping OpenKB, checking prerequisites, or deciding whether `graphify` and `openkb` are available and properly vendored.

## Related Documents
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]