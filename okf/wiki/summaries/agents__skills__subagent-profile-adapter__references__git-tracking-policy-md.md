---
type: "Summary"
description: "Defines default local-only git tracking for adapters and alias handling."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md"
---

# Git Tracking Policy

This document sets the default git-tracking behavior for harness-specific profile adapters and related tooling files.

## Key Policy

The default stance is **local-only**:

- write adapter files locally;
- add those paths to `.git/info/exclude`;
- do not modify `.gitignore`;
- do not commit the adapter files.

This keeps generated or environment-specific adapter state out of shared repository history unless there is an explicit reason to share it.

## When To Use Other Tracking Modes

Two alternatives are called out:

- Use `.gitignore` when every contributor should ignore generated adapters.
- Commit adapters only when the team has explicitly standardized on the harness and wants shared runtime profiles.

This frames git tracking as a consent-based decision rather than an automatic default.

## Tooling Context Exception

The document notes a special case for `okf/wiki/tooling/` pages:

- they follow the same local-default policy in general;
- but every contributor generates harness build records there;
- so the shared-ignore case applies;
- use `.gitignore` for `okf/wiki/tooling/*` with an exception for `!okf/wiki/tooling/index.md`;
- do not rely on `.git/info/exclude` for this directory;
- `tooling/index.md` remains committed as the navigation stub.

It also points to git scope and related tooling policy material for the full rules.

## Instruction File Aliases

If a harness requires a different instruction filename instead of `AGENTS.md`, the preferred approach is:

- create a local symlink to `AGENTS.md`;
- add the alias path to `.git/info/exclude`;
- only do this after confirming the requirement from current docs or user instructions.

The document includes a helper command using `uv run` to create that alias.

## Core Idea

The main theme is controlled visibility of generated files:

- local preferences stay local by default;
- shared ignore rules are used when the team shares a generated-file convention;
- commits are reserved for explicit team-wide standardization.

## Related Concepts
- [[concepts/git-tracking-policy]]
- [[concepts/local-vs-shared-ignore]]
- [[concepts/instruction-file-aliasing]]
- [[concepts/consent-first-tooling]]
- [[concepts/runtime-adapter-management]]
- [[concepts/tooling-context-isolation]]
- [[concepts/tooling-navigation-exceptions]]
- [[concepts/local-vs-shared-configuration]]
- [[concepts/reserved-markdown-files]]
- [[concepts/agents-md-maintenance]]
- [[concepts/harness-native-profiles]]
- [[concepts/wiki-skill-boundaries]]

## Entities
- [[entities/git-info-exclude]]
- [[entities/gitignore]]
- [[entities/agents-md]]
- [[entities/subagent-profile-adapter]]
- [[entities/uv]]
- [[entities/openkb]]
- [[entities/okf-wiki]]
