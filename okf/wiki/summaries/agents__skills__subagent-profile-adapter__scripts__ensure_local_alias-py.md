---
type: "Summary"
description: "CLI helper creates a local AGENTS.md alias with symlink or pointer fallback."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"
---

# Summary

This script creates a repository-local alias for an agent instruction file, usually `AGENTS.md`, so harnesses or adapters that expect a different local filename can still find the canonical instructions. It is designed to work across platforms by preferring a relative symlink and falling back to a small Markdown pointer file when symlinks are unavailable.

## What it does

- Accepts a repository root, canonical source file, required alias path, and optional `--force` / `--fallback` behavior.
- Verifies that the source instruction file exists before doing any writes.
- Ensures the alias stays inside the repository by resolving and validating the alias path.
- Creates the alias parent directories as needed.
- Tries to create a relative symlink first, which keeps the alias portable within the repo.
- Falls back to writing a pointer Markdown file when symlink creation fails and fallback mode allows it.
- Records the alias path in `.git/info/exclude` so the local harness artifact is not committed accidentally.

## Notable behavior

- If the alias already exists as the correct symlink, the script treats that as success and still updates the git exclude file.
- If the alias exists but is not the expected local alias, the script refuses to overwrite it unless `--force` is used.
- It refuses to replace a real directory at the alias path.
- It warns if the repository does not appear to be a git checkout, because exclude-file updates cannot be applied.

## Key ideas

- [[concepts/harness-native-profiles]]: the script adapts to environments where symlinks are not available.
- [[concepts/local-only-repo-artifacts]]: the alias is intentionally excluded from version control.
- [[concepts/instruction-file-aliasing]]: the helper exists to satisfy harness-specific filename expectations without hardcoding vendor rules.
- [[concepts/symlink-fallback]]: the implementation uses a symlink-first strategy with a Markdown pointer fallback.

## Findings

- The alias target is computed relative to the alias directory, which keeps symlinks stable when the repository moves.
- The fallback pointer file explicitly tells contributors not to edit the alias directly, reducing drift from the canonical source.
- The script uses `.git/info/exclude` rather than `.gitignore`, making the exclusion local to the current checkout rather than shared in the repository.

## Scope

This is a small utility script rather than a policy document. Its main contribution is operational: it standardizes how a repository can expose one canonical agent instruction file under a second local name while minimizing accidental commits and preserving portability.

## Related Concepts
- [[concepts/adaptive-harness-detection]]
- [[concepts/agents-md-maintenance]]
- [[concepts/runtime-adapter-management]]
- [[concepts/tooling-context-governance]]
- [[concepts/tooling-boundaries]]
- [[concepts/git-tracking-policy]]
- [[concepts/portable-skill-contract]]
- [[concepts/local-by-default-tooling]]

## Entities
- [[entities/ensure_local_alias-py]]
- [[entities/git-info-exclude]]
- [[entities/subagent-profile-adapter]]
- [[entities/agents-md]]
- [[entities/git]]
- [[entities/python]]
- [[entities/romain-monier]]
- [[entities/apache-license-2-0]]
- [[entities/tooling]]
- [[entities/okf-wiki-tooling]]
- [[entities/runtime-detection-md]]
- [[entities/scripts-inspect_runtime_context-py]]
