---
type: "source-file"
title: ".agents/skills/subagent-profile-adapter/references/git-tracking-policy.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/subagent-profile-adapter/references/git-tracking-policy.md"
source_path: ".agents/skills/subagent-profile-adapter/references/git-tracking-policy.md"
source_kind: "markdown"
source_hash: "sha256:62f6be6742bfe229e127a26be3619d750e52929517d6f3dc56aaa8d14de24056"
source_commit: "c039bcb85c5f6dcddf93f8be4716656af4f70f82"
tags: [source-file, markdown]
---

# .agents/skills/subagent-profile-adapter/references/git-tracking-policy.md

~~~
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

## Instruction file aliases

If the active harness does not support `AGENTS.md` but requires another instruction filename, prefer a local symlink to `AGENTS.md` and add the alias to `.git/info/exclude`.

Use:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/ensure_local_alias.py \
  --repo . \
  --source AGENTS.md \
  --alias <harness-required-file>
```

Only use the alias after confirming the harness requirement through current docs or user instruction.
~~~
