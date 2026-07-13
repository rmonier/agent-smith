---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md"]
description: "Consent-based rules for tracking generated and tooling files in git."
---

# Git Tracking Policy

Git Tracking Policy is the consent-based rule set for deciding how generated files, harness-specific adapters, and tooling-context pages should be tracked in a repository. It favors keeping local runtime artifacts out of shared version control unless there is an explicit reason to share them.

## Core Principle

The default behavior is **local-only**:

- write adapter or generated files locally;
- add the paths to `.git/info/exclude`;
- do not modify `.gitignore`;
- do not commit the files.

This default treats harness-specific adapters as environment-bound state rather than repository content. It aligns with [[concepts/local-vs-shared-ignore]] and [[concepts/consent-first-workflows]].

## When Shared Tracking Makes Sense

The policy allows two exceptions:

- use `.gitignore` when every contributor should ignore the generated adapters;
- commit the adapters only when the team has explicitly standardized on the harness and wants shared runtime profiles.

This makes git tracking a deliberate governance decision rather than an automatic outcome, connecting the concept to [[concepts/generated-artifact-adoption]], [[concepts/local-vs-shared-configuration]], and [[concepts/runtime-adapter-management]].

## Tooling Context Exception

The document calls out `okf/wiki/tooling/` as a special case.

That directory follows the same local-default philosophy, but because every contributor generates harness build records there, the shared-ignore model applies instead:

- use `.gitignore` for `okf/wiki/tooling/*`;
- keep `!okf/wiki/tooling/index.md` committed as the navigation stub;
- do not use `.git/info/exclude` for this directory;
- treat further tooling pages as an opt-in consent decision, just like adapter commits.

This exception reflects [[concepts/tooling-context-pages]], [[concepts/tooling-navigation-exceptions]], and [[concepts/documentation-architecture]]. It also matches the broader tooling-context policy: harness build records are required when the harness can be identified reliably, while fuller tooling documentation is optional and only belongs there when a detected or user-selected harness is actively in use. The tooling area is user-scoped, not project truth, so committed navigation must stay stable while local pages remain unenumerated. That boundary supports [[concepts/tooling-context-governance]], [[concepts/tooling-context-isolation]], and [[concepts/minimal-tool-scoping]].

## Instruction File Aliasing

If a harness does not support `AGENTS.md` but requires another instruction filename, the preferred strategy is to create a local symlink to `AGENTS.md` and exclude the alias locally.

The policy recommends:

- create the alias only after confirming the requirement from current docs or user instruction;
- prefer a local symlink over committing an alternate instruction file;
- add the alias to `.git/info/exclude`.

This fits with [[concepts/instruction-file-aliasing]] and [[concepts/harness-native-profiles]].

## Why It Matters

This policy reduces accidental repository pollution from generated harness state, preserves contributor autonomy, and keeps shared tracking limited to cases with clear team agreement. It is a practical example of [[concepts/privacy-preserving-tooling]] and [[concepts/source-trust-levels]]. It also supports [[concepts/tooling-consent-and-pin-management]] by separating user-scoped tooling records from project-scoped content.

## Related Source

- [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]