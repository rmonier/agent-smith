---
sources: ["summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md"]
type: "Organization"
description: "Organization upstream source for `uv` and provenance-sensitive tooling."
---

# Astral

Astral is the organization identified in [[summaries/agents__skills__agent-ready-context__SKILL-md]], [[summaries/agents__skills__agent-ready-context__references__dependencies-md]], [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]], and [[summaries/agents__skills__skill-creator__references__dependencies-md]] as the authoritative upstream source for [[entities/uv]]. In this wiki, Astral matters because the workflow treats tool identity, installation guidance, version pinning, and integrity verification as provenance-sensitive decisions rather than trusting package names, command availability, or installer shortcuts alone. The prereq checker makes that role operational by treating `uv` as a hard prerequisite, directing installation back to Astral's official documentation when `uv` is missing, and framing bare `python3` as a degraded fallback only if the user explicitly declines `uv`. [[summaries/agents__skills__agent-ready-context__SKILL-md]] strengthens this further by making `uv` the required execution path for bundled scripts, requiring user consent before bootstrap installs, and positioning upstream ownership as part of the repository's durable tooling policy rather than a one-off setup detail. The [[summaries/graphify-report]] reinforces that this role is structurally central to the repository's documentation and policy graph, where dependency, provenance, and tooling-governance topics appear as prominent communities rather than incidental notes.

## Role in the dependency policy

The documents use Astral as the provenance anchor for `uv`:
- `uv` is treated as a hard requirement for the `agent-ready-context` skill and as the required Python toolchain through which bundled scripts are expected to run.
- Its upstream source is Astral, with installation and verification guidance pointing back to Astral-owned source and documentation rather than informal third-party instructions.
- Install and verification guidance depends on confirming the exact tool identity against that upstream source before adoption.
- The prereq checker treats missing `uv` as a hard requirement failure and directs the user to Astral's installation documentation rather than suggesting ad hoc substitutes.
- The prereq checker also distinguishes between required and degraded operation: `uv` is the expected path for isolated execution, while bare `python3` is only a user-approved fallback when the preferred Astral-backed tool is unavailable.
- [[summaries/agents__skills__agent-ready-context__SKILL-md]] adds that every bundled script should run through `uv run`, because PEP 723 metadata allows isolated dependency resolution without touching the target repository environment.
- The skill's tooling bootstrap rules require explicit user consent before installation and require the exact package name, configured index, upstream source, pinned version, and integrity plan to be disclosed first, making Astral part of the approval chain for adopting `uv`.
- Skill dependency guidance requires exact package, registry, and upstream source documentation for installable tools, making Astral the concrete upstream reference for `uv` in that policy.
- Versioned install commands should be pinned and integrity-aware, so Astral is part of the chain of evidence used for reproducible, consent-first tooling decisions.
- Older or conflicting installation instructions should be checked against the upstream source rather than accepted at face value.
- The dependencies reference adds a registry-agnostic rule: even when a private mirror or enterprise index is used, package identity should still be anchored to the verified upstream source, which keeps Astral relevant even when the artifact is not fetched directly from the public default index.
- The same reference makes `uv tool install` and `uv run` part of a broader policy of exact version pinning, first-install integrity capture, later hash comparison, and stop-and-report behavior on mismatches for the same version and index.
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] adds that the checker probes `uv` with a longer timeout because its first invocation may spend significant time importing dependencies, which treats installation latency as a practical part of the trusted workflow rather than evidence that the tool is missing.
- The checker also uses `uv` as a signal for vendor-skill readiness: if the CLI is installed but the matching skill is not vendored under `.agents/skills/`, it emits a note telling the user to vendor the pinned copy before first use.
- [[summaries/agents__skills__agent-ready-context__SKILL-md]] also ties Astral indirectly to repository-wide bootstrap policy by stating that `uv` is the required Python toolchain for this skill, and that declining it moves the workflow into an explicitly reported degraded mode.
- In the repository graph summarized by [[summaries/graphify-report]], Astral appears as a named entity within a broader documentation architecture shaped by dependency policy, provider/tool boundaries, and validation workflows, which supports treating upstream ownership as part of the repository's durable context rather than a one-off setup detail.

This places Astral within the workflow's broader emphasis on [[concepts/provenance-tracking]], [[concepts/supply-chain-security]], [[concepts/dependency-management]], [[concepts/trust-on-first-use]], and [[concepts/version-pinning]].

## Why Astral is significant here

Astral is not discussed as a general company profile in these sources; instead, it is referenced as a trust anchor in a consent-first tooling workflow. The important idea is that the repository's setup process should:
- verify the exact upstream owner for critical tools
- avoid lookalike or misleading package identities
- use pinned, auditable installations
- record and check integrity details when documenting or moving tool pins
- respect configured package indexes or mirrors without bypassing them, while still validating tool identity against the upstream source
- keep local tool readiness separate from harness permissions
- preserve isolated execution for bootstrap scripts by preferring `uv run` over assuming the target repository environment is safe or appropriate
- treat upstream tool provenance as part of repository-wide structural governance, consistent with the graph report's picture of tooling and policy documents as core navigation hubs
- make prerequisite validation actionable by routing remediation for missing `uv` back to the authoritative installation source rather than relying on generic environment debugging
- support [[concepts/graceful-degradation]] without weakening provenance rules, by allowing fallback execution only as an explicit exception to the preferred Astral-backed path
- keep bootstrap behavior aligned with [[concepts/tooling-context-isolation]] by using `uv` to isolate script execution from the repository's own runtime state
- connect installation approval, integrity capture, and later verification into a single policy flow consistent with [[concepts/tooling-consent-and-pin-management]] and [[concepts/integrity-pinning]]
- treat startup latency as part of operational reality, since the prereq checker gives `uv` a longer probe timeout to avoid misclassifying a healthy installation as missing
- enforce vendored skill readiness, so a present CLI still requires the repository-local skill copy before the tool is used in this repo

Those practices connect Astral to [[concepts/tooling-consent-and-pin-management]], [[concepts/tool-boundaries]], [[concepts/deterministic-validation]], [[concepts/tooling-context-isolation]], [[concepts/harness-vs-local-tools]], and [[concepts/cross-platform-tooling]].

## Related pages

- [[entities/uv]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__skill-creator__references__dependencies-md]]
- [[summaries/graphify-report]]
- [[concepts/provenance-tracking]]
- [[concepts/supply-chain-security]]
- [[concepts/dependency-management]]

See also: [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]