---
type: "Concept"
sources: ["summaries/agents__skills__graphify__-graphify_version.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md"]
description: "Exact dependency version selection to keep tooling behavior stable and reviewable."
---

# Version Pinning

Version pinning is the practice of selecting and recording an exact dependency version rather than following a floating or implicit latest release. In this wiki, the concept is especially important for vendor skills and local toolchains, where the dependency is not just code but executable guidance or automation that can directly affect agent behavior, repository state, and validation outcomes.

## Why it matters

Pinning reduces unexpected change. When a repository depends on an external skill or CLI, a floating version can silently alter instructions, workflows, file layouts, or safety assumptions. Exact version selection makes behavior more repeatable across runs, contributors, and environments.

This supports:

- predictable repository behavior
- safer updates with explicit review points
- easier rollback and comparison
- clearer provenance for installed guidance and tools

Version pinning therefore sits at the intersection of [[concepts/dependency-management]], [[concepts/integrity-pinning]], [[concepts/provenance-tracking]], and [[concepts/skill-governance]].

## In vendor skill management

[[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]] treats vendor skills as dependencies that should be pinned by a manager-generated lock file when available. The document states that vendor skill versions should be fixed through the manager or lockfile, and should not track floating latest releases.

The source also recommends committing the lock file created by the skill manager. This matters because the lock file is the shared record of the chosen version, making installs reproducible for the whole project rather than relying on local state or memory.

[[summaries/agents__skills__agent-ready-context__references__dependencies-md]] extends this pattern from vendored skills to the surrounding local toolchain. It treats commands left behind for tools such as `openkb` and `graphifyy` as requiring exact version pins, with the chosen version recorded in `AGENTS.md` together with source and verification details. In that model, pinning is not only a package-manager concern; it is part of the repository's durable operational contract.

In practice, pinning in this context means:

- install vendor skills through the intended manager when applicable
- record the exact selected version
- commit the generated lock file when one exists
- record toolchain pins in repository guidance when the workflow depends on local CLIs
- update only through a deliberate re-vendoring or manager-driven upgrade

These practices reinforce [[concepts/deterministic-builds]], [[concepts/deterministic-validation]], and [[concepts/quality-gates]].

## Pinning and vendoring

The source documents pair version pinning with read-only vendoring. A pinned vendor skill is copied into the repository under `.agents/skills/<name>/`, kept immutable, and tracked with its source version. If behavior must change, the correct response is not to edit the vendored dependency in place, but to create a project-owned companion skill or repository-local procedure.

[[summaries/agents__skills__agent-ready-context__references__dependencies-md]] makes this especially explicit for the `graphify` and `openkb` toolchain skills: the CLI is not considered fully adopted until its corresponding pinned skill copy is vendored into the repository before use. The vendored copy is treated as immutable vendor content and refreshed only by re-vendoring from a newly approved pinned release.

This separation helps preserve a clean distinction between third-party content and project-authored procedure. Pinning defines what was imported; immutability preserves it; companion skills capture local customization. Together, these patterns support [[concepts/source-trust-levels]], [[concepts/skill-vendoring]], and [[concepts/tooling-consent-and-pin-management]].

## What pinning prevents

Without pinning, teams risk:

- silent behavior drift when upstream releases change
- inconsistent installs across machines or time
- harder audits of which instructions and tool versions were active
- confusion between upstream changes and local edits
- accidental divergence between a vendored skill and the CLI version it is meant to describe

For agent skill workflows, these failures are especially significant because a changed dependency can alter procedural guidance, validation expectations, or safety boundaries. For local CLIs, they can also change generated output, prerequisite checks, or repository bootstrap steps.

## Relationship to review and trust

Pinning is not a substitute for review. The source documents say vendor skills and installable tools should also be checked for publisher, repository, package identity, license, and surprising instructions before installation. Pinning preserves a reviewed state; it does not make an unreviewed dependency safe.

The newer dependency guidance adds a stronger supply-chain framing: exact version selection should be paired with upstream-source verification, consent-first installation, and recorded integrity data for the exact artifact obtained from the configured index. In this sense, pinning works together with [[concepts/trust-on-first-use]], [[concepts/integrity-pinning]], and [[concepts/supply-chain-security]] rather than replacing them.

That makes version pinning complementary to [[concepts/supply-chain-security]] and to the broader handling of trusted external materials under [[concepts/dependency-management]].

## Practical interpretation

Use version pinning when bringing vendor skills or required local tools into a project so the repository depends on a known, reviewable, reproducible version. Treat the pinned version, any related lock file, and any recorded repository pin record as part of the project's operational contract. Make upgrades explicit events: detect the candidate version, review upstream changes, obtain user approval, then update the pin and refresh any vendored copy.

In this wiki's tooling context, pinning also implies respecting configured package indexes rather than bypassing them, leaving behind exact install commands instead of floating ones, and keeping the repository's vendored guidance aligned with the pinned runtime tools it depends on.

## Related pages

- [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[concepts/dependency-management]]
- [[concepts/integrity-pinning]]
- [[concepts/deterministic-builds]]
- [[concepts/deterministic-validation]]
- [[concepts/provenance-tracking]]
- [[concepts/skill-governance]]
- [[concepts/skill-vendoring]]
- [[concepts/supply-chain-security]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/quality-gates]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__graphify__-graphify_version]]