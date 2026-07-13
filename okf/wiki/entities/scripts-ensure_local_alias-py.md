---
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
type: "Work"
description: "Helper script for creating local instruction aliases"
---

# Ensure Local Alias Script

`Ensure Local Alias Script` is a helper script referenced by the [[summaries/agents__skills__subagent-profile-adapter__SKILL-md|subagent-profile-adapter]] skill for managing local instruction-file aliases when a harness needs a different agent-instruction path.

## What it does

- Helps create a local alias, preferably as a symlink, to `AGENTS.md` when the active harness does not use `AGENTS.md` directly.
- Supports the skill's instruction-file compatibility workflow by keeping the repository's canonical orientation file intact.
- Can add the alias path to `.git/info/exclude` so the adapter stays local by default.

## Key facts

- The skill treats `AGENTS.md` as the canonical orientation file.
- Alias creation is only appropriate after confirming the target path from documentation or the user.
- The script is mentioned as a generic local symlink and exclude helper.
- The surrounding workflow emphasizes [[concepts/instruction-file-aliasing]], [[concepts/local-only-repo-artifacts]], and [[concepts/symlink-fallback]].

## Related context

- The script belongs to the skill's broader runtime-adapter workflow, which also covers runtime detection and harness-specific file generation.
- It supports the skill's boundary between repository truth and harness-specific runtime projections.
- It is part of the local tooling surface rather than a project knowledge source of truth.

## See also

- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[concepts/runtime-adapter-management]]
- [[concepts/tooling-context-governance]]
- [[concepts/instruction-file-aliasing]]