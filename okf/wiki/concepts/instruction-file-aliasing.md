---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"]
description: "Using a local alias to expose canonical agent instructions to a harness."
---

# Instruction File Aliasing

Instruction file aliasing is the practice of exposing one canonical agent instruction file under a second, repository-local name so a harness, adapter, or runtime can find the instructions it expects without duplicating content. It preserves a single source of truth while accommodating different local conventions and fits the broader pattern of runtime-specific adapter generation.

This concept is demonstrated by [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]], which creates a local alias for `AGENTS.md` and keeps that alias out of version control by default. It also aligns with the subagent/profile adapter workflow in [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]], where local instruction aliases are treated as harness-specific projections rather than shared source material.

## Why it exists

Different tools and harnesses may look for different instruction filenames. Rather than copying the same instructions into multiple files, aliasing lets a repository keep one canonical document and provide a local pointer to it. That reduces drift, supports [[concepts/single-source-of-truth]], and fits [[concepts/agent-ready-context]] workflows where the active instructions must be discoverable in the current environment.

It also supports [[concepts/runtime-adapter-management]] and [[concepts/harness-native-profiles]] by letting the repo adapt to native harness expectations without turning those local names into durable project truth.

## Core behavior

- Prefer a symlink from the alias path to the canonical source file.
- Fall back to a small Markdown pointer file when symlinks are unavailable.
- Keep the alias path inside the repository to avoid unsafe redirection.
- Record the alias in `.git/info/exclude` so it remains a local artifact.
- Refuse to overwrite an unexpected existing path unless explicitly forced.
- Treat a correctly resolving existing alias as success, not as a special failure case.

## Implementation details from the source

The helper script accepts:

- `--repo` for the repository root
- `--source` for the canonical instruction file, defaulting to `AGENTS.md`
- `--alias` for the harness-required path
- `--force` to replace an existing alias
- `--fallback pointer|fail` to control behavior when symlink creation fails

The script validates that the source exists, resolves the alias relative to the repository, and rejects alias paths outside the repo. If the alias already exists and correctly resolves to the source, it is treated as success. If a non-matching file exists, the script stops unless `--force` is supplied.

When symlink creation succeeds, the alias points to the source using a relative target, which helps portability across checkouts. When symlink creation fails and fallback is allowed, the script writes a Markdown pointer file that tells users not to edit the alias directly. The alias is also excluded locally, reflecting the expectation that it is a harness-specific artifact rather than a shared tracked file.

## Related ideas

Instruction file aliasing connects to [[concepts/adaptive-harness-detection]], because the alias is only needed when the active harness expects a specific local filename. It also relates to [[concepts/compatibility-fallback]] and [[concepts/symlink-fallback]], since the implementation is designed to degrade gracefully when filesystem capabilities are limited.

The exclusion step reflects [[concepts/local-only-repo-artifacts]] and [[concepts/local-vs-shared-ignore]]: the alias is intentionally local, not something the repository should publish as shared configuration. It also supports [[concepts/tooling-navigation-exception]] by keeping harness-specific instruction paths outside the normal project knowledge flow.

## Practical value

- Keeps the canonical instructions in one place.
- Avoids duplicated or conflicting agent guidance.
- Works across environments with different symlink support.
- Makes local harness adaptation safer and more reproducible.
- Lets adapter generation reuse existing repository orientation instead of inventing parallel instruction sets.

## Risks and constraints

- The alias must be managed carefully so it does not drift from the canonical file.
- The fallback pointer is readable by humans, but it is not the same as a real symlink.
- If the repository is not a git checkout, the exclude-file safeguard cannot be applied.
- The mechanism is useful only when a runtime or harness truly requires an alternate local filename.
- The alias should stay a local projection, not a new source of truth for project guidance.

## See also

- [[concepts/agent-ready-context]]
- [[concepts/adaptive-harness-detection]]
- [[concepts/compatibility-fallback]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/single-source-of-truth]]
- [[concepts/symlink-fallback]]
- [[concepts/runtime-adapter-management]]
- [[concepts/harness-native-profiles]]