# Git tracking policy

Harness-specific profile adapters may be local preferences or team-shared runtime adapters. Ask before changing tracking behavior.

## Default policy

Default to **local-only**:

- write the adapter files;
- add those paths to `.git/info/exclude`;
- do not modify `.gitignore`;
- do not commit them.

## Alternatives

Use `.gitignore` when every contributor should ignore generated adapters.

Commit adapters only when the team explicitly standardizes on the harness and wants shared runtime profiles.

## Tooling context pages

`okf/wiki/tooling/` pages follow the same local-default, with one difference: every contributor generates harness build records there, so the shared-ignore case applies — use `.gitignore` (`okf/wiki/tooling/*` with `!okf/wiki/tooling/index.md`), not `.git/info/exclude`. The committed exception is the `tooling/index.md` navigation stub. Committing further tooling pages is the same opt-in consent decision as committing adapters. Full rules in `references/tooling-context-policy.md` ("Git scope").

## Instruction-file and skills-directory aliases

Both bridges follow this same local-default tracking policy — see `SKILL.md` step 3 for when and how to create them (`scripts/ensure_local_alias.py` handles a harness-required instruction-file name and a harness-required skills directory the same way, with a directory-specific fallback on Windows). This section is about tracking the *alias itself* once created: local by default, via `.git/info/exclude`, same as any other adapter output above; only commit it under the same explicit team-policy decision.
