---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"]
description: "Repository artifacts meant for local use and excluded from version control."
---

# Local-Only Repository Artifacts

Local-only repository artifacts are files created to support a specific checkout, machine, or harness without becoming part of the shared repository state. They are useful when a workflow needs extra paths, aliases, caches, or adapter files that should exist locally but remain outside normal source control.

This concept appears in [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]], where the script creates a repository-local alias for an agent instruction file and then records that alias in `.git/info/exclude` so it stays untracked by default.

## Why they matter

- They let tooling adapt to local harness expectations without changing canonical repository content.
- They reduce accidental commits of machine-specific or workflow-specific files.
- They help preserve a [[concepts/single-source-of-truth]] for shared documents while still allowing local compatibility layers.
- They support [[concepts/graceful-degradation]] by providing a fallback when a preferred mechanism, such as a symlink, is unavailable.

## Typical properties

- The artifact is created inside the repository but is not intended for distribution.
- The artifact often points to or wraps a canonical file rather than duplicating content.
- The artifact is excluded using local ignore mechanisms such as `.git/info/exclude`, not repository-wide ignore rules.
- The artifact may be regenerated safely and treated as disposable workspace state.

## Example from the source script

The `ensure_local_alias.py` helper embodies this pattern:

- It accepts a required alias path for a harness-specific instruction filename.
- It prefers a relative symlink to the canonical `AGENTS.md` file.
- If symlinks are unavailable, it writes a small Markdown pointer file instead.
- It appends the alias path to `.git/info/exclude` so the local artifact remains untracked.
- It refuses to overwrite unexpected existing paths unless `--force` is used.

That combination makes the alias a clear example of a local-only artifact that is operationally useful but intentionally not shared.

## Related ideas

- [[concepts/instruction-file-aliasing]]: creating a local alias for a canonical instruction file.
- [[concepts/compatibility-fallback]]: switching to an alternate representation when the preferred one fails.
- [[concepts/local-vs-shared-ignore]]: keeping ignore rules scoped to one checkout when appropriate.
- [[concepts/path-safety]]: ensuring local artifacts stay inside the repository.
- [[concepts/reserved-markdown-file-rules]]: avoiding accidental collisions with special repository files.

## Practical takeaway

Use local-only artifacts when a workflow needs repository-adjacent support files but the shared project should continue to track only the canonical source of truth. This keeps the repo clean, portable, and easier to review while still supporting local automation and harness integration.

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]