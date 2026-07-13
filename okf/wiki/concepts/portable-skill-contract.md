---
type: "Concept"
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/repo-snapshot.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md"]
description: "A portable interface for defining reusable skills without host-specific assumptions."
---

# Portable Skill Contract

The portable skill contract is the narrow, reusable interface that a skill can expose without relying on repository-specific installation state or hidden environment assumptions. It centers on `SKILL.md` frontmatter and a small set of optional support directories, while pushing dependency handling into explicit scripts and reference docs. It also keeps runtime-specific adapter concerns out of the skill definition itself, so a skill can stay portable even when the active harness needs separate subagent or profile projections.

## Core Shape

The contract keeps the skill definition portable by limiting the official surface to:

- `SKILL.md` frontmatter
- optional `scripts/`
- optional `references/`
- optional `assets/`

This keeps the skill aligned with [[concepts/skill-structure-conventions]] and avoids turning a skill file into a full installation manifest.

The initialization script in `summaries/agents__skills__skill-creator__scripts__init_skill-py` reinforces this shape by bootstrapping a new skill directory, writing a starter `SKILL.md`, and optionally creating only the supported resource folders. That makes the contract concrete: a skill starts as a small, portable directory with a predictable layout rather than a bespoke project scaffold.

The same portability boundary applies when a repository needs harness-specific runtime adapters. The subagent-profile-adapter skill treats adapters as runtime projections, not as a portable skill concern, which keeps the contract focused on reusable action logic rather than host-specific execution layers.

## What Belongs Outside The Contract

The document makes a clear boundary: dependency resolution, vendor lockfiles, installation state, and runtime adapter generation belong to the skill manager, harness tooling, or explicit project scripts, not to `SKILL.md` itself. That boundary supports [[concepts/skill-dependency-declaration]] and reduces confusion between skill metadata and environment provisioning.

In practice, the skill should not add a non-standard `dependencies` field. Instead, it should describe requirements in portable, human-readable ways that preserve [[concepts/tooling-boundaries]] and [[concepts/local-tooling-boundaries]].

The initializer follows that same principle by generating a generic procedural template instead of embedding environment-specific assumptions. It creates a starting `SKILL.md`, but leaves the real workflow, commands, and validation steps to be filled in by the skill author.

## Recommended Placement Of Requirements

The source document distributes dependency information across several places:

- `compatibility` for runtime and environment requirements, with a strict size limit
- namespaced `metadata.*` keys for local, non-portable hints
- `references/dependencies.md` for detailed requirements and instructions
- `scripts/check_prereqs.py` when the action depends on CLIs, credentials, network access, or companion skills

This pattern supports [[concepts/consent-first-tooling]] and [[concepts/preflight-checks]] by making prerequisites explicit before execution.

The initializer complements this by accepting a `--resources` flag that can create `scripts`, `references`, and `assets` on demand. That keeps support material organized without expanding the contract into arbitrary project structure.

## Metadata Conventions

The document defines a shared vocabulary for dependency-related namespaced metadata. These keys are optional and only used when relevant:

- `<skill-name>.companion-skills` for helpful sibling skills
- `<skill-name>.companion-skill-roles` for role descriptions
- `<skill-name>.provides` for reusable capabilities exposed to others
- `<skill-name>.vendor-skills` for third-party skills the skill defers to
- `<skill-name>.prereq-check` for the prerequisite checker path
- `<skill-name>.prereq-guidance` for the dependency reference path
- `<skill-name>.subagent-profile-adapter` for runtime-specific adapter guidance when a harness needs a local projection

This keeps local hints structured without inventing a separate dependency system, and it aligns with [[concepts/frontmatter-metadata]] and [[concepts/skill-governance]].

## Third-Party Tooling Rules

When a skill depends on installable tooling, the document requires:

- exact package, registry, and upstream source repository naming
- pinned versions in documented install commands
- consent-first installation, with user confirmation before installing
- user-scoped installers such as `uv tool install`
- integrity tracking on first install
- a stated fallback or degraded mode when the tool is absent

These rules connect directly to [[concepts/consent-first-installation]], [[concepts/integrity-pinning]], and [[concepts/provenance-aware-tool-installation]].

The initializer does not manage these dependencies itself; instead, it sets up a skill shell where such requirements can be documented or checked explicitly. That separation helps keep portable skill definitions distinct from install-time orchestration.

## Skill Relationships

The document prefers the term companion skill for useful but non-required pairings between skills. It also distinguishes vendor skills from repository-owned skills, treating installed vendor skills as immutable and requiring adaptation through custom companion skills when needed.

That distinction supports [[concepts/skill-vendoring]] and [[concepts/vendor-skill-adoption]] while preserving a clean [[concepts/skill-action-boundary]].

The initialization script fits this model by creating a normalized skill name and a standard directory target, making new skills easier to recognize, reference, and connect to related capabilities later.

## Why It Matters

The portable contract keeps skills predictable across environments, easier to validate, and safer to share. It avoids hidden dependency behavior, makes prerequisite checks discoverable, and keeps the skill definition focused on what the skill does rather than how a particular machine happens to satisfy it.

The `init_skill.py` script shows how that contract is operationalized: it normalizes names, validates the target path, initializes a reusable directory structure, and emits a consistent `SKILL.md` template. Together, those behaviors support [[concepts/skill-scaffolding]], [[concepts/project-scaffolding]], [[concepts/path-safety]], and [[concepts/kebab-case-normalization]].

The subagent-profile-adapter skill extends this same philosophy into the runtime layer: use the skill contract for portable action logic, and generate harness-specific adapters only as separate projections when the active environment requires them.

See also [[summaries/agents__skills__skill-creator__references__dependencies-md]].

See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/repo-snapshot]]

See also: [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]

## Related Documents
- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]


See also: [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agent-skills-spec]]