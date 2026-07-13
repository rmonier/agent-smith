---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md"]
description: "Configuration should stay local unless it is shared team policy."
---

# Local vs Shared Configuration

Local vs shared configuration is the distinction between settings, files, and runtime choices that should remain specific to one contributor's environment and those that should be adopted across a whole repository or team.

This concept matters when a tool, harness, or workflow needs configuration artifacts that may reflect personal runtime preferences rather than project-wide standards. The key question is whether a configuration file expresses an individual setup choice or a deliberate team policy.

## Core idea

A local configuration should stay outside normal repository tracking when it is:

- specific to one user's environment;
- tied to a personal tool or harness choice;
- not required for other contributors to work effectively;
- likely to create noise or accidental policy changes if committed.

A shared configuration belongs in repository-visible mechanisms when it is:

- useful for all contributors;
- part of a documented team standard;
- required for consistent behavior across environments;
- intentionally governed as project configuration.

This decision boundary overlaps with [[concepts/runtime-adapter-management]], [[concepts/generated-content-governance]], and [[concepts/tooling-context-isolation]].

## Guidance from the source documents

[[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]] presents a conservative default for harness-specific profile adapters: treat them as local-only unless the team explicitly decides otherwise. It recommends writing adapter files locally, adding them to `.git/info/exclude`, avoiding `.gitignore` changes by default, and committing them only when the team explicitly standardizes on the harness and wants shared runtime profiles.

[[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] reinforces the same policy in executable form for instruction-file aliases. Its default behavior is to create a local alias to `AGENTS.md`, prefer a relative symlink, optionally fall back to a small pointer file when symlinks are unavailable, and then record the alias in `.git/info/exclude`.

[[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] extends the same local/shared split into repository preflight checks. It treats `okf/.openkb/config.yaml` as a per-user file that should be copied from `config.yaml.example` when needed, compares only shared keys such as `language`, `pageindex_threshold`, and `entity_types`, and ignores provider-specific values like `model`, `litellm`, and `timeout` because those are user choices rather than shared policy. It also checks for both `okf/.env` and `~/.config/openkb/.env`, warns when both exist, and makes clear that the project file wins for shared keys while provider routing remains a local decision.

Across these sources, the default local-only policy is to:

- write adapter or alias files locally;
- exclude them through `.git/info/exclude` when they are only relevant to one clone;
- avoid modifying `.gitignore` by default unless the team wants a repo-wide ignore rule;
- avoid committing the files unless the team explicitly adopts that policy;
- keep provider-specific OpenKB configuration in the user's local `config.yaml` or environment rather than treating it as shared repository state.

The same pattern appears in the separate tooling-context exception described by [[concepts/tooling-context-pages]] and [[concepts/tooling-navigation-exceptions]]: `okf/wiki/tooling/` pages use `.gitignore` rather than `.git/info/exclude` because every contributor generates harness build records there, but the committed `tooling/index.md` stub remains the shared navigation anchor.

This approach keeps personal runtime adapters and provider settings from being mistaken for shared repository policy. It also limits unnecessary churn in version control, preserves contributor choice, and reduces the chance that one contributor's harness choice becomes an implicit requirement for others.

## Local-only mechanisms vs shared mechanisms

The source material distinguishes between repository-level visibility choices by matching the mechanism to the intended scope of authority.

Using `.git/info/exclude` signals a local decision. It hides files only in one clone, making it appropriate for personal tooling preferences, machine-specific adapter files, and local instruction-file aliases created only to satisfy one harness.

Using `.gitignore` signals a broader project decision. It is appropriate when every contributor should ignore the same generated or runtime-specific files.

Committing the files is the strongest form of sharing. That should happen only when the team has explicitly standardized on the harness, adapter, alias, or configuration shape and wants those artifacts shared as part of normal collaboration.

This reflects a broader pattern of matching the storage and tracking mechanism to the intended scope of authority, connecting to [[concepts/configuration-precedence]], [[concepts/spec-authority]], and [[concepts/skill-governance]].

## Why the distinction matters

Keeping local configuration local helps preserve repository clarity and contributor autonomy. It supports:

- cleaner Git history;
- fewer accidental workflow mandates;
- safer experimentation with tools;
- clearer separation between personal setup and team policy;
- cross-platform compatibility without forcing one workaround on everyone;
- consistent OpenKB compilation without hard-coding each contributor's provider choice into shared files.

The alias-creation script and the prereq checker add an important practical lesson: even when a compatibility artifact or config file is useful, it should still remain local if it exists only to satisfy one runtime environment or one contributor's provider setup. Promoting configuration to shared status should be an explicit act of team agreement, not a side effect of one user's tooling.

## Example from instruction file aliases

The source material applies this principle directly to alternate instruction filenames. If a harness requires a filename other than `AGENTS.md`, the preferred solution is a local alias to the canonical file rather than duplicating instructions.

[[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] operationalizes that rule by:

- validating that the canonical source exists;
- requiring the alias path to stay inside the repository;
- reusing an already-correct alias instead of rewriting it;
- refusing unsafe replacements such as directories;
- preferring a relative symlink;
- falling back to a pointer file when symlinks are unavailable;
- excluding the alias locally through `.git/info/exclude`.

This keeps compatibility workarounds scoped to the users who need them while preserving [[entities/agents-md]] as the single shared instruction source. That pattern relates to [[concepts/agents-md-maintenance]], [[concepts/single-source-of-truth]], [[concepts/cross-platform-tooling]], [[concepts/graceful-degradation]], [[concepts/path-safety]], and [[concepts/safe-automation]].

## Example from OpenKB config

The prereq checker applies the same local/shared distinction to OpenKB repository setup.

It checks whether `okf/.openkb/config.yaml` exists, and if `config.yaml.example` is present but the local file is missing, it reports that the user should copy the example into a local config and choose a provider mode. When both files exist, it compares only the shared keys that should match across contributors, not the provider-specific keys that belong to the local environment.

It also distinguishes between the project-local `okf/.env` and the user-global `~/.config/openkb/.env`:

- if both exist, it notes that the project file wins for shared keys and warns about ambiguity;
- if only the global file exists, it treats that as a valid personal setup;
- if only the project file exists, it uses that as the active credential home;
- if neither exists, it treats that as acceptable for OAuth-based setups but notes that key-based providers need `LLM_API_KEY`.

That behavior aligns with local vs shared configuration at the file, environment, and credential level: shared project values should be stable, while provider routing and secret-bearing files remain local whenever possible.

## Practical heuristic

A useful rule is:

- keep it local if it serves one contributor's runtime preference;
- use local exclusion mechanisms when the artifact exists only for one clone or one machine;
- share it through ignore rules if everyone benefits from suppressing it;
- commit it only if the team has consciously adopted it as standard behavior;
- keep OpenKB provider-specific settings local, but compare and preserve shared schema keys across contributors.

When a local compatibility file is unavoidable, prefer the least invasive form that preserves a single canonical source and avoids turning private setup into accidental repository policy.

## Related pages

- [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[concepts/runtime-adapter-management]]
- [[concepts/configuration-precedence]]
- [[concepts/generated-content-governance]]
- [[concepts/tooling-context-isolation]]
- [[concepts/skill-governance]]
- [[concepts/spec-authority]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]