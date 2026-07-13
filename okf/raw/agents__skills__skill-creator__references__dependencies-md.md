---
type: "source-file"
title: ".agents/skills/skill-creator/references/dependencies.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/references/dependencies.md"
source_path: ".agents/skills/skill-creator/references/dependencies.md"
source_kind: "markdown"
source_hash: "sha256:493c69622453c667e2931098b7944e65978671a87b13c8652be83a2bb49d2813"
source_commit: "fe332d86064854bf7b4e943365857eeffbd5ae89"
tags: [source-file, markdown]
---

# .agents/skills/skill-creator/references/dependencies.md

~~~
# Skill dependency rules

Do not add a non-standard `dependencies` field to `SKILL.md`.

The current portable Agent Skills contract is the `SKILL.md` frontmatter plus the optional `scripts/`, `references/`, and `assets/` directories. Dependency resolution, vendor lockfiles, and installation state belong to the skill manager or to explicit project scripts.

## When creating a skill

Use this pattern:

- Put runtime/environment requirements in `compatibility` (max 500 characters).
- Put non-portable local hints under namespaced `metadata.*` keys (string values only, prefixed with the skill name, for example `my-skill.companion-skills`).
- Document detailed requirements in `references/dependencies.md`.
- Add a `scripts/check_prereqs.py` script when the action depends on local CLIs, credentials, network access, or companion skills.
- Treat `allowed-tools` as a permission hint, not as an installer or dependency declaration, and keep it minimal and scoped (`Bash(git:*)`, not `Bash`).
- Give Python scripts PEP 723 inline metadata and document them as `uv run <script>`, with bare `python3` only as a degraded fallback.

## Standard metadata key vocabulary

Namespaced `metadata.*` keys are free-form, but dependency-flavored keys reuse this shared vocabulary so any skill's frontmatter reads the same way (`<skill-name>` is the skill's own `name`):

- `<skill-name>.companion-skills` — comma-separated sibling project skills that pair with this one (useful, not required).
- `<skill-name>.companion-skill-roles` — semicolon-separated `skill=role` descriptions that clarify direction and lifecycle without turning companions into hard dependencies.
- `<skill-name>.provides` — comma-separated reusable capabilities exposed to companion skills inside a coordinated bundle.
- `<skill-name>.vendor-skills` — third-party skills this skill defers to when installed, each as `name (source, role)`.
- `<skill-name>.prereq-check` — skill-relative path to the prerequisite checker, usually `scripts/check_prereqs.py`.
- `<skill-name>.prereq-guidance` — skill-relative path to the dependency reference, usually `references/dependencies.md`.

Add a key only when it applies to the skill; never write an empty placeholder. Other local hints (policy pointers, optional integrations) keep the same skill-name prefix but need no fixed suffix.

## Third-party tool requirements

When a skill depends on installable tooling:

1. Name the exact package, its registry, and its upstream source repository in the skill's `references/dependencies.md`.
2. Pin versions in documented install commands; never leave `@latest` in instructions the skill hands to future agents.
3. Make installation consent-first: the skill instructs the agent to ask the user before installing, and to use user-scoped installers such as `uv tool install` — never `sudo`.
4. Record integrity on first install next to the pin (for Python, artifact sha256 captured from the environment's configured index, which may be a corporate mirror and must never be bypassed or hardcoded), treat a mismatch for the same version and index as a supply-chain incident, and require user-confirmed release-note review before moving any pin.
5. State how the skill degrades when the tool is absent.

## Skill-to-skill relationships

Prefer the term **companion skill** when another skill is useful but not strictly required.

A companion skill may be listed in namespaced metadata, for example:

```yaml
metadata:
  my-skill.companion-skills: other-skill
```

This is a local convention, not a standard dependency field. The skill must still explain how to behave when the companion skill is absent.

## Vendor skills

Vendor skills installed by a package manager should stay immutable in the repository. Do not patch them directly. A skill that defers to an installed vendor skill declares it with `<skill-name>.vendor-skills` from the vocabulary above.

If a vendor skill must be adapted, create a custom companion skill under `.agents/skills/` and document the relationship.

If the skill manager provides a lockfile, keep it as the reproducibility source for vendor skills. Do not hand-author fake lock entries.
~~~
