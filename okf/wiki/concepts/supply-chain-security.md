---
type: "Concept"
sources: ["summaries/README-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md", "summaries/agents__skills__skill-creator__references__source-attribution-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__skill-creator__assets__skill-lock-example-json.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
description: "Secure acquisition and vendoring of tools, skills, and artifacts with pinned provenance."
---

# Supply-Chain Security

Supply-chain security is the set of practices used to reduce the risk that external tools, packages, mirrors, skills, or artifacts are substituted, republished, installed from the wrong source, or modified outside their governed update path. In this wiki, the concept is grounded by [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]], and [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]], which together describe a consent-first, pinned, provenance-aware workflow for local tooling, vendored skills, and project-owned skill dependencies.

## Why it matters

Any workflow that installs or vendors external software inherits risk from package registries, mirrors, install instructions, upstream release processes, skill managers, copied vendor content, and generated dependency metadata. A secure process must answer four questions before installation or vendoring:

- What exact package or skill is this?
- What upstream project authoritatively defines it?
- Which registry, mirror, repository, or source identifier served the artifact?
- How do we detect if the artifact or copied content changes later?

The newer dependency guidance sharpens this by making a distinction between descriptive metadata and executable checks: documentation may explain the rules, but the real readiness gate is an executable prerequisite check, and install guidance must not pretend that a permission hint or frontmatter field is an authoritative dependency manifest. This makes supply-chain security closely related to [[concepts/provenance-tracking]], [[concepts/dependency-management]], [[concepts/tooling-consent-and-pin-management]], [[concepts/executable-validation]], and [[concepts/consent-first-tooling]].

## Core controls

The source documents describe several concrete controls that work together:

### Exact package identity

Tool names and package names may differ, so installs must verify the real package identity rather than assume it from the CLI name. The clearest example in the source is [[entities/graphify]], whose Python package is [[entities/graphifyy]], not `graphify`. This is a basic defense against lookalike or typosquatted packages.

The same principle applies to skills: the user or agent should verify the exact skill name, publisher, and repository before installation or vendoring rather than trusting a convenient shorthand. If older notes, stale setup instructions, or informal examples disagree with the verified upstream source, the upstream source wins and the mismatch should be reported.

### Authoritative upstream source

Each installable dependency should have one authoritative upstream repository or manager-defined source that anchors its identity. The document names upstream sources for [[entities/uv]], [[entities/graphify]], and [[entities/openkb]], and treats those repositories as the source of truth when older instructions conflict. The skill lock example extends this idea by reserving a `source` field for the manager's source identifier, making origin tracking part of locked dependency state.

The vendoring guidance strengthens this control by requiring source verification before installation, including publisher, repository, and license review, and by recording the source version or commit for vendored copies. This ties acquisition to an explicitly reviewed upstream rather than an ambiguous local copy, and aligns with [[concepts/spec-authority]] and [[concepts/provenance-tracking]].

### Exact version pinning

Commands left behind for reuse should pin exact versions instead of floating versions. This prevents silent upgrades and makes installations reproducible. The dependency guidance is explicit that any reusable install command should leave behind exact pins rather than floating versions, and the skill lock example reinforces this by modeling each skill entry with a `version` field that should hold a pinned version or digest. Pinning supports controlled updates and aligns with [[concepts/deterministic-validation]], [[concepts/version-pinning]], and [[concepts/quality-gates]].

The vendored skill guidance makes this explicit for third-party skills: vendor skill versions should be pinned through the manager and its lock file when one exists, and workflows should avoid tracking floating `latest` releases.

### Integrity recording

Version pins alone are not enough, because the same version could be republished or tampered with. The source therefore adds integrity capture by hashing the exact downloaded artifact and recording the sha256 value alongside the version, index, and date. The skill lock example generalizes the same control with an `integrity` field intended to hold a manager-generated integrity value for each locked skill. Together, these patterns create an audit trail that can detect later substitution and align with [[concepts/integrity-pinning]], [[concepts/hash-registry-coherence]], and [[concepts/trust-on-first-use]].

For vendored skills, the comparable control is to preserve source and version metadata and update only through a fresh vendoring step or manager-driven lock update rather than through ad hoc file edits that break the chain of custody.

### Registry-aware verification

Installs should use the Python index or mirror already configured by the environment. The workflow explicitly forbids bypassing an enterprise mirror to reach the public registry. If a mirror cannot serve the pinned package, the correct action is to report the problem rather than switch indexes. This keeps the chain of custody explicit and preserves organizational controls.

The same mindset applies to skill managers and repository vendoring: use the approved source and acquisition path, and report source-resolution problems rather than silently switching to an unreviewed alternative. This combines supply-chain review with [[concepts/configuration-precedence]] and [[concepts/offline-first-workflows]].

### Consent-first installation

The user should be shown what will be installed, why it is needed, where it comes from, what version is pinned, and the exact command to run. The user can then choose whether to install it personally, have the agent run the command, or skip it. This reduces hidden changes and ties secure installation to explicit approval.

The newer dependency guidance is especially clear that approval is per tool and includes the repository consequences of adopting that tool, such as vendoring its associated skill into `.agents/skills/` before use. Vendor skill guidance adds a review step before approval: because a skill is executable guidance, its `SKILL.md` and scripts should be inspected for surprising instructions before installation. This makes supply-chain security part of [[concepts/human-in-the-loop-review]] and [[concepts/safe-automation]].

### Machine-managed lock data

The skill lock example adds an important governance rule: lock files are manager-generated records, not casual configuration files. Its note explicitly warns against hand-editing real vendor lock entries unless the manager documents that workflow. This matters because supply-chain controls depend on the lock file remaining a faithful record of resolved dependency state rather than an unverified manual claim. That pattern connects supply-chain security to [[concepts/generated-content-governance]] and [[concepts/lock-file-examples]].

The vendor skill document reinforces the same point by requiring lock files to be committed when the manager creates them and by treating them as the canonical pinned record for third-party skill resolution.

## Trust-on-first-use model

The source document uses a [[concepts/trust-on-first-use]] approach for package and artifact integrity:

1. On first install, download the pinned artifact from the configured index or source.
2. Compute or record its integrity value.
3. On later installs, compare the same version from the same source against the recorded integrity.
4. If the integrity differs, stop and report instead of installing.

The newer dependency guidance adds two important qualifiers. First, the integrity record should preserve not only the version and hash but also the index or mirror it came from and the date it was captured. Second, a mismatch for the same version from the same index is a stop-and-report event, not a reason to silently refresh the recorded value. If the organization genuinely changed mirrors, re-baselining requires explicit user acknowledgement.

This model has an honest limitation: it can detect later artifact substitution, but it cannot prove that the first captured artifact was trustworthy if the index or source was already compromised. The source treats this as a limitation to state clearly rather than hide.

A similar limitation applies to vendored skill content: recording source, version, and lock data improves later detection and reviewability, but cannot retroactively prove that an initially vendored copy was safe if the upstream or acquisition path was already compromised.

## Mirrors, proxies, and enterprise environments

A key idea in the source is that secure behavior must still work in mirrored or proxied environments. Public registries are not treated as inherently more trustworthy than an organization's configured index; instead, the configured index defines the environment's approved acquisition path. Supply-chain security here is not just about cryptographic checks, but also about respecting deployment boundaries, administrative controls, and existing index configuration.

This reinforces the connection between supply-chain security and [[concepts/tool-boundaries]], [[concepts/configuration-precedence]], and [[concepts/privacy-preserving-tooling]].

## Update discipline

The concept also includes controlled updates:

- detect that a newer version exists
- show upstream release notes or changelog differences
- wait for explicit user confirmation
- install or re-resolve the new version
- capture and record the new integrity value in the relevant lock or tracking record

For vendored skills, the same discipline means re-vendoring a newer pinned version or regenerating manager lock state rather than editing vendor files in place. This keeps updates reviewable and preserves a clean distinction between upstream dependency state and local project behavior.

The newer dependency guidance also makes it explicit that package pins and vendored skill copies move together: when a tool version changes, the corresponding vendored skill should be refreshed from that approved version through the proper project-scoped mechanism or manager update path. This prevents silent pin movement and keeps dependency changes reviewable. In practice, this turns updates into a documented decision rather than an automatic side effect.

## Vendored skill content

The source extends supply-chain thinking beyond Python packages to vendored OpenKB skills. When skills are copied into a repository, the workflow prefers project-scoped vendoring, records source version or commit, and treats copied skill directories as immutable vendor content. The lock file example complements this by showing how a skill manager can preserve `name`, `source`, `version`, and `integrity` as structured dependency metadata. Updates happen by re-vendoring from a newer pinned source or regenerated lock state rather than editing the vendored copy or lock entries in place.

The updated dependency guidance adds an important operational requirement: for CLI-backed workflows, a tool is not fully adopted until its associated skill is vendored into the repository before the CLI is used. This matters because the vendored skill is the durable, repository-local carrier of usage knowledge. Running the CLI first and vendoring later leaves generated state without committed guidance that explains how that state should be maintained. In that sense, supply-chain security is not only about getting the right bits, but also about ensuring the reviewed operational instructions that accompany those bits are present when the tool first changes the repository.

The vendor skill guidance sharpens the distinction between vendored vendor skills and adopted generated skills. Vendored vendor skills remain third-party content and should never be edited directly, even to make them conform better to local conventions. If project-specific behavior is needed, it belongs in a separate custom companion skill. By contrast, adopted generated skills become project-owned after adoption and validation, so later edits are expected and are not a supply-chain violation in the same way.

The same document also introduces a review concern that matters for secure adoption workflows: generated or distilled skill content can flatten conditional guidance into unconditional instructions. Preserving caveats, boundaries, and explicit prohibitions during adoption is therefore part of keeping project-owned skill behavior faithful to its reviewed sources, connecting this concept to [[concepts/caveat-preservation]].

That approach strengthens traceability and aligns with [[concepts/source-driven-regeneration]], [[concepts/documentation-architecture]], and [[concepts/skill-vendoring]].

## Practical signals of a secure workflow

A workflow is following this concept when it does most of the following:

- verifies package or skill names against upstream repositories or documented sources
- reviews publisher, repository, license, and executable guidance before adopting a new vendor skill
- records exact versions instead of relying on floating installs
- records integrity values for downloaded artifacts or locked dependencies
- preserves which index, mirror, repository, or source identifier supplied the artifact
- refuses to bypass configured mirrors
- treats lock files as manager-generated state rather than hand-maintained metadata
- treats mismatched hashes or integrity values as stop-and-report events
- requires explicit approval before install or update
- vendors tool-provided skills before first CLI use when the workflow depends on them
- records vendored content provenance and avoids in-place mutation
- keeps third-party vendor skills read-only and moves project-specific behavior into custom companion skills
- separates permission hints and frontmatter metadata from actual dependency enforcement or readiness checks

## In this wiki

The primary sources for this concept are [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]], and [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]. Together they provide a practical, operations-focused model of supply-chain security centered on package identity, provenance, index-aware acquisition, integrity pinning, lock discipline, explicit review, immutable vendoring, and reproducible installation behavior.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__skill-creator__assets__skill-lock-example-json]]
- [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]
- [[concepts/dependency-management]]
- [[concepts/provenance-tracking]]
- [[concepts/tool-boundaries]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/deterministic-validation]]
- [[concepts/quality-gates]]
- [[concepts/integrity-pinning]]
- [[concepts/generated-content-governance]]
- [[concepts/lock-file-examples]]
- [[concepts/caveat-preservation]]
- [[concepts/executable-validation]]
- [[concepts/version-pinning]]
- [[concepts/hash-registry-coherence]]
- [[concepts/skill-vendoring]]
- [[concepts/configuration-precedence]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/safe-automation]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__references__dependencies-md]]

See also: [[summaries/agents__skills__skill-creator__references__source-attribution-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/README-md]]