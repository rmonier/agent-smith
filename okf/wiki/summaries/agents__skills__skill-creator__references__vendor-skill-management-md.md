---
type: "Summary"
description: "Guidance for handling vendor and custom skills in OpenKB projects."
doc_type: short
full_text: "sources/agents__skills__skill-creator__references__vendor-skill-management-md.md"
---

# Vendor and custom skill management

This document defines how to manage third-party and project-owned skills under `.agents/skills/`, with an emphasis on treating vendor skills like pinned dependencies and custom skills like maintained project procedures.

## Core guidance

Vendor skills are treated as external dependencies. They should be installed through a skill manager when applicable, pinned through the manager's lock file, and preferably vendored into the repository at project scope rather than installed at the harness level. The document emphasizes that vendored copies should remain immutable and carry recorded source and version metadata.

Custom skills are project-owned procedural assets. They live under `.agents/skills/<skill-name>/`, follow skill directory and frontmatter conventions, and are intended to capture repeatable actions while leaving broader context in `okf/wiki/`.

## Vendor skills

Vendor skills should be:

- safety-reviewed before installation
- pinned to a specific version
- tracked with a lock file when available
- kept read-only after vendoring
- updated only by re-vendoring or using the relevant manager

The document names official OpenKB read-only skills from VectifyAI/OpenKB as examples of typical vendor skills, including optional deck helper skills. It recommends creating project-specific companion skills when behavior must differ instead of modifying the vendored copy directly.

This reflects a broader [[concepts/dependency-management]] and [[concepts/version-pinning]] approach: skills are executable guidance and should be handled with the same care as software dependencies.

## Vendor skills vs adopted generated skills

A key distinction is made between vendored third-party skills and adopted generated skills:

- Vendored vendor skills remain third-party, read-only content.
- Adopted generated skills become project-owned once brought in through `adopt_generated_skill.py`.

Adopted generated skills must pass validation and then be maintained like any other custom skill. Unlike vendor skills, they are expected to be edited when needed.

The document highlights an important risk in adoption workflows: LLM distillation may flatten conditional guidance into unconditional instructions. Because of this, adopted skills require a caveat-preservation review against the originating `okf/wiki/` pages and their underlying sources. Constraints such as boundaries, exceptions, and explicit prohibitions must be restored if they were lost during distillation.

This introduces a recurring concern around [[concepts/caveat-preservation]] and [[concepts/provenance-tracking]].

## Rules for vendor skills

The document gives explicit rules:

1. Do not edit vendor skill files directly.
2. Update vendor skills only through the package or skill manager.
3. Commit the lock file created by the manager.
4. Create a custom companion skill for project-specific behavior.
5. Verify source, publisher, repository, license, and review `SKILL.md` and scripts before installing.
6. Pin versions and avoid floating `latest`.

Together these rules frame vendor skills as a form of [[concepts/supply-chain-security]].

## When to create custom skills

Custom skills should be created when repeated actions are identified across project materials such as:

- OKF wiki pages
- `AGENTS.md` maintenance notes
- incident and runbook history
- repeated user prompts
- repeated agent command sequences

The intended pattern is to keep the skill procedural while preserving broader explanatory context in `okf/wiki/`. This suggests a separation between [[concepts/context-action-separation]] and durable knowledge-base context.

## Practical takeaway

The main operational model is:

- vendor external skills as pinned, reviewed, immutable dependencies
- keep project-specific behavior in separate custom skills
- treat adopted generated skills as editable project assets
- verify that distilled skills preserve the caveats and limits found in source materials

This document is primarily about safe [[concepts/skill-governance]] for agent workflows, especially around provenance, immutability, validation, and preserving meaning from source knowledge.

## Related Concepts
- [[concepts/skill-based-automation]]
- [[concepts/quality-gates]]
- [[concepts/deterministic-validation]]
- [[concepts/tool-boundaries]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-linking-and-citations]]

## Entities
- [[entities/vectifyai-openkb]]
- [[entities/openkb]]
- [[entities/agents-md]]
