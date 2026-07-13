---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"]
description: "Using a fallback when symlinks are unavailable or blocked."
---

# Symlink Fallback

Symlink fallback is the practice of trying to create a symbolic link first, then switching to a safer alternative when the filesystem, platform, or permissions do not allow symlinks. In repository tooling, this pattern preserves the main workflow on systems with full symlink support while still offering a usable result in constrained environments.

## Why it matters

Symlink-based aliases are convenient because they stay lightweight, track the canonical file, and avoid duplicating content. But they are not always portable: some operating systems restrict symlink creation, some environments lack the required privileges, and some checkout or automation contexts treat symlinks inconsistently. A fallback path reduces failure rates and supports [[concepts/graceful-degradation]] in local tooling.

## Pattern

A typical symlink fallback flow is:

1. Validate the canonical source exists.
2. Try to create a relative symlink to the source.
3. If symlink creation fails, use an alternate representation such as a pointer file.
4. Record the generated alias as a local-only artifact so it is not committed.

The source script in [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] follows this pattern for a harness-specific instruction-file alias.

## Key details from the source

- The script prefers a relative symlink, which keeps the alias stable if the repository is moved.
- If symlink creation raises `OSError`, the script can fall back to writing a small Markdown pointer file.
- The fallback behavior is configurable with `--fallback pointer` or `--fallback fail`.
- The alias is added to `.git/info/exclude`, reinforcing [[concepts/local-only-repo-artifacts]] and avoiding accidental commits.
- If the alias already exists as the correct symlink, the script treats that as success instead of rewriting it.
- The script refuses to replace an existing directory at the alias path, which protects local state and aligns with [[concepts/path-safety]].

## Related ideas

- [[concepts/compatibility-fallback]]: broader use of alternate execution paths when the preferred path is unavailable.
- [[concepts/graceful-degradation]]: keep the workflow usable even when the ideal mechanism fails.
- [[concepts/local-only-repo-artifacts]]: keep generated local helper files out of shared version control.
- [[concepts/instruction-file-aliasing]]: exposing one canonical instruction file under another name for harness compatibility.
- [[concepts/harness-native-profiles]]: adapting repository behavior to harness-specific expectations without changing the canonical source.

## Practical takeaway

Symlink fallback lets tooling remain portable without giving up the advantages of symlinks where they are supported. For local repository adapters, it is a small implementation detail that carries a large usability benefit.