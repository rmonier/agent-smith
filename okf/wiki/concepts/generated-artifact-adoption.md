---
type: "Concept"
sources: ["summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md"]
description: "Controlled promotion of generated artifacts into repository-owned assets."
---

# Generated Artifact Adoption

Generated artifact adoption is the controlled process of promoting a machine-produced output into a repository-owned asset only after checks, validation, and human review. It treats generation as a draft-producing step, not as automatic authority, and makes the adopted copy the point where the project explicitly accepts ownership.

In OpenKB-driven workflows, adoption also marks the handoff from disposable build output to durable wiki or repository content. That matters because the KB lifecycle is intentionally split between staged input, compiled pages, and maintained assets: generated material may live in `okf/.okf-build/` or `okf/output/` until it is explicitly accepted, while the committed wiki, skills, and configuration are the project-owned layer.

## Why it matters

Generated outputs can be useful accelerators, but they may flatten constraints, omit caveats, widen permissions, or introduce unsafe defaults. Adoption creates a boundary between "the system generated this" and "the project now owns this." That boundary supports [[concepts/generated-content-governance]], [[concepts/quality-gates]], and [[concepts/human-in-the-loop-review]].

In practice, this means a generated artifact is not accepted merely because it exists. It must be copied into its destination deliberately, checked for structural correctness, validated near its final repository location, and reviewed against project standards and source-derived intent. In agent-ready repositories, this boundary is especially important because generated material may move from exploratory or build-only locations into durable project context such as `okf/wiki/`, `.agents/skills/`, or other tracked repository assets.

The skill workflow adds an important refinement: generated output may satisfy format checks and still fail the real adoption bar if it loses trigger clarity, overreaches on permissions, mishandles untrusted inputs, or drops action-specific caveats during distillation. Adoption therefore marks both ownership transfer and a semantic review boundary.

OpenKB lifecycle rules reinforce the same boundary from the repository side. Before compiling, querying, or changing the KB, the workflow starts with `openkb --kb-dir ./okf status` and `openkb --kb-dir ./okf list`, then reads `okf/wiki/index.md` and relevant wiki pages before trusting any content. That makes adoption part of a broader discipline of [[concepts/wiki-content-as-untrusted-data]] and [[concepts/read-only-kb-operations]] before mutation.

## Core pattern

A typical adoption workflow includes:

1. Identify a specific generated artifact to promote.
2. Verify that it has the expected structure and naming.
3. Prevent accidental overwrite unless replacement is explicitly requested.
4. Copy or move it into the project-owned location.
5. Run validation against the adopted copy.
6. Clean up or warn if validation fails.
7. Require human review before commit.

This makes adoption a form of [[concepts/executable-validation]] plus repository workflow control, rather than a blind file transfer. In OpenKB-oriented workflows, adoption is also the moment when generated output stops being build output and becomes a maintained repository asset. The agent-ready bootstrap guidance sharpens this distinction by treating locations such as `okf/.okf-build/`, `okf/output/`, and reports directories as disposable or non-authoritative, while treating selected wiki, config, and skill outputs as repository-owned once deliberately accepted.

The OpenKB lifecycle also adds a staging discipline: deterministic staged sources are ingested from `./okf/.okf-build/input/`, and external content is only added after explicit consent and data-flow disclosure. Adoption is therefore not just file copying; it is choosing the right source path, the right trust boundary, and the right mutation mechanism. When a source is deleted or moved, the lifecycle recommends reconciliation before ingestion so stale pages do not linger alongside new ones.

For skills specifically, adoption also includes checking that the result belongs in the action layer rather than in durable context or repository guidance. The skill-creation rules make this explicit: facts, architecture, decisions, provenance, and explanations remain in OpenKB, while repeated executable behavior belongs in a project-owned skill. Adoption is therefore partly a placement decision within [[concepts/agent-context-layering]] and [[concepts/context-action-separation]].

## Example in the skill adoption script

[[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]] provides a concrete implementation of this concept for OpenKB-generated skills.

The script adopts a skill from `okf/output/skills/` into `.agents/skills/` and applies several controls:

- It validates the skill name with a strict pattern before touching the filesystem.
- It rejects names containing `--` in addition to the regex check.
- It requires the source to contain `SKILL.md`, confirming the artifact looks like a skill.
- It refuses to replace an existing destination unless `--force` is supplied.
- It copies the generated skill into the destination and then runs a validator script against the adopted copy.
- If validation fails after a fresh copy, it removes the copied directory.
- If validation fails after a forced replacement, it leaves the replaced copy in place and warns the operator to fix or remove it.
- It resolves the validator path relative to the script location, keeping validation tied to the skill-creator tooling layout.

This is a practical combination of [[concepts/filesystem-validation]], [[concepts/deterministic-validation]], and [[concepts/skill-governance]].

The surrounding skill workflow adds additional adoption criteria beyond the script itself: the adopted skill should have a clear trigger-style description, declare minimal allowed tools, treat fetched content as untrusted data, avoid storing secrets in repository files, and remain editable as a project-owned copy after adoption. The adoption command performs copy-and-validate, but the workflow still expects human judgment before the result is considered acceptable.

The OpenKB lifecycle adds parallel safeguards for wiki material. The KB owns `okf/raw/` and generated wiki pages, so generated content should never be hand-edited in place. If a promoted artifact becomes stale or is revealed to be wrong, the supported repair path is to regenerate, recompile, or remove it through OpenKB rather than editing the projection directly. That keeps adoption aligned with [[concepts/source-driven-regeneration]], [[concepts/hash-registry-coherence]], and [[concepts/registry-drift]].

## Adoption is not trust

A key idea in this concept is that generation does not grant correctness. The generated skill still needs review for:

- trigger-style description quality
- minimal allowed tools
- handling of untrusted content
- absence of secrets
- preservation of source-derived limits, caveats, and warnings
- continued fit with the intended action rather than drift into durable context or repository guidance

That review step connects generated artifact adoption to [[concepts/caveat-preservation]], [[concepts/tool-boundaries]], and [[concepts/context-action-separation]]. A generated result may be structurally valid while still being semantically wrong, over-permissive, incomplete, or misplaced.

The same principle applies to agent-ready repository bootstrap outputs. A generated or compiled wiki, a synthesized skills directory, or structural output from repository analysis can be helpful without being authoritative by default. The bootstrap guidance explicitly distinguishes durable context from routing instructions and structural exploration aids, reinforcing that generated artifacts must be reviewed for where they belong, what role they serve, and whether they preserve source intent.

The skill workflow makes this especially concrete by warning that distillation tends to flatten conditional guidance into unconditional steps. Adoption is the checkpoint where the operator compares the generated result back to the source wiki pages and restores any missing boundary, warning, or "never do" instruction before treating the artifact as repository-owned.

The OpenKB lifecycle reaches the same conclusion from another angle: wiki content is treated as untrusted data, and `openkb query` is reserved as a last resort because it consumes an LLM call and should not replace direct inspection of index, summaries, or sources. That makes adoption part of a larger [[concepts/evidence-grounded-answering]] discipline rather than a convenience shortcut.

## Safety properties

A strong adoption workflow usually preserves these properties:

- explicit operator intent for destructive replacement
- validation close to the destination state
- failure handling that limits damage
- visible separation between generated outputs and maintained assets
- review guidance tied to project standards
- minimal tool and permission scope in the adopted result
- protection against silently accepting distilled content as authoritative

These properties align with [[concepts/source-driven-regeneration]] and [[concepts/okf-validation]] when generated content originates from structured source material and must remain faithful to it. They also align with the agent-ready bootstrap recommendation to keep build artifacts and caches out of the committed knowledge base while selectively adopting validated outputs such as `okf/wiki/`, tracked configuration, and project-owned skills.

The skill-creation guidance adds a few concrete safety expectations for adopted skills: use the smallest practical tool scope, never treat package installation as implicit, keep credentials in environment variables, and treat web-fetched material as untrusted data rather than instructions. Adoption is stronger when these expectations are reviewed at the same time as structural validity.

The OpenKB lifecycle adds another safety layer: staged material should come from known paths, registry entries and wiki pages should be treated as one unit, and reconciliation should happen before adding new content so deleted or moved sources do not leave behind stale compiled pages. That makes adoption part of a broader maintenance posture that includes [[concepts/registry-drift]] and [[concepts/provenance-tracking]].

## In the OpenKB skill workflow

In the referenced skill workflow, adoption is the point where generated skill drafts become project-owned skills. Generated skills remain in `okf/output/skills/` as optional downstream output until a user explicitly chooses to adopt one into `.agents/skills/<skill-name>/`, which is the project-local location for maintained skills.

The adoption step is followed by validation and a caveat-preservation review. The project-owned copy is expected to be edited if needed, especially when the generation process has flattened conditions into unconditional steps or dropped important boundaries. The operator is instructed to compare the adopted skill against the `okf/wiki/` pages it distilled from and restore any missing constraint, boundary, or warning.

The broader agent-ready bootstrap process provides the same repository-level framing: first generate or compile context, then decide what becomes durable and committed. `AGENTS.md` stays short and routing-oriented, `okf/wiki/` serves as durable knowledge, `graphify-out/` remains an exploration aid rather than final authority, and reusable procedures belong in `.agents/skills/`. Adoption therefore includes not only accepting a file, but placing it into the correct layer of repository knowledge and automation.

In this workflow, adoption also distinguishes generated project-owned skills from vendored skills. Vendored vendor skills remain unchanged, while adopted generated skills become editable local assets that must meet project standards. That distinction reinforces adoption as a governance event, not just a copy operation.

The OpenKB lifecycle also explains why adoption must respect ownership boundaries. Generated wiki pages, raw source copies, and registry state are maintained by OpenKB, and the no-hand-edit rule exists because compiled pages are projections of source material. Adoption has to honor that projection model: if a generated artifact is adopted into the wiki or another maintained layer, it must be accepted through the lifecycle rather than patched into place by hand.

That reinforces that adoption is not only about syntax or file presence; it is also about preserving meaning, constraints, and intent from source material while ensuring the result remains a safe, action-oriented repository asset.

## Related concepts

- [[concepts/generated-content-governance]]
- [[concepts/quality-gates]]
- [[concepts/executable-validation]]
- [[concepts/filesystem-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/human-in-the-loop-review]]
- [[concepts/skill-governance]]
- [[concepts/caveat-preservation]]
- [[concepts/tool-boundaries]]
- [[concepts/okf-validation]]
- [[concepts/source-driven-regeneration]]
- [[concepts/context-action-separation]]
- [[concepts/agent-context-layering]]
- [[concepts/documentation-architecture]]
- [[concepts/durable-context]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/safe-automation]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/skill-vendoring]]
- [[concepts/read-only-kb-operations]]
- [[concepts/registry-drift]]
- [[concepts/provenance-tracking]]
- [[concepts/hash-registry-coherence]]

## Source

- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]
- [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]