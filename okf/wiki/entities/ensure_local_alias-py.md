---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"]
type: "Work"
description: "Utility script that creates a local AGENTS.md alias for harnesses"
---

# ensure_local_alias.py

`ensure_local_alias.py` is a Python utility script in `.agents/skills/subagent-profile-adapter/scripts/` that creates a repository-local alias for the canonical agent instruction file, usually `AGENTS.md`.

It is documented in [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] and supports harness-specific filename expectations without changing the canonical source file.

## Key facts

- Prefers creating a relative symlink from the alias path to the canonical instruction file.
- Falls back to writing a small Markdown pointer file when symlinks are unavailable, unless `--fallback fail` is selected.
- Verifies that the source instruction file exists before making changes.
- Rejects alias paths that escape the repository root.
- Can replace an existing alias only when `--force` is provided.
- Refuses to replace a real directory at the alias path.
- Appends the alias path to `.git/info/exclude` so the local artifact stays out of version control.

## Design traits

- [[concepts/instruction-file-aliasing]]: its main purpose is to map one canonical instruction file to a second local name.
- [[concepts/symlink-fallback]]: it uses symlinks first and degrades to a pointer file when needed.
- [[concepts/local-only-repo-artifacts]]: the alias is treated as a checkout-local helper, not a committed repository file.
- [[concepts/local-vs-shared-ignore]]: it updates `.git/info/exclude`, which keeps the exclusion local to the current clone.
- [[concepts/path-safety]]: it checks that the alias remains inside the repository before writing.
- [[concepts/graceful-degradation]]: it continues to work when symlink creation is unavailable.

## Relationship to the subagent adapter

The script belongs to the `subagent-profile-adapter` skill tooling and helps bridge differences between repository conventions and external harness expectations. It is a small adapter utility rather than a policy source, and its behavior is intentionally narrow: preserve the canonical instruction file while providing a local compatibility alias.

## Related pages

- [[entities/subagent-profile-adapter]]
- [[entities/git-info-exclude]]
- [[entities/agents-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]