---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/README-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Product"
description: "Version control prerequisite used throughout the OpenKB workflow"
---

# Git

Git is the version control system used as a hard prerequisite in the OpenKB build workflow, the fallback OKF skeleton generator, the editorial curation pass validator, the orphan retraction script, and the local agent alias helper. In the README, it is also part of the repository's consent-first bootstrap model: the agent checks for Git before proceeding, explains what it needs when Git is missing, and stops with a manual fallback if the repository cannot be safely prepared another way.

## Role In The Workflow

- The workflow requires a Git repository before the source pack can be built.
- `build_okf_source_pack.py` stages `git ls-files` output, so the repository must have Git history.
- `build_okf_source_pack.py` also uses `git log --name-only` to derive last-touch commits for staged provenance metadata.
- `build_okf_skeleton.py` uses `git rev-parse HEAD` to capture the current commit for generated wiki pages.
- `check_prereqs.py` verifies that `git` is installed and that the target path is inside a Git worktree before agent-ready-context proceeds.
- `editorial_pass.py` uses `git diff`, `git status`, and `git archive` to validate curation diffs against a chosen base.
- `prune_okf_orphans.py` uses Git to compare the current repository against the KB registry, detect deleted or renamed source files, and distinguish true deletion from a path move.
- `prune_okf_orphans.py` falls back to git-derived staged names only when a fresh source-pack manifest is unavailable, so Git remains the backup source of truth for reconciliation.
- `ensure_local_alias.py` uses Git to detect `.git/info/exclude`, record the local alias path, and keep repository-local harness artifacts out of commits.
- If the repo has no Git history, the process stops and asks for user consent before initializing Git.
- The README also treats `git` as one of the hard bootstrap requirements alongside `uv`, with the expectation that missing prerequisites are disclosed and handled explicitly rather than installed silently.

## Why It Matters

- Git provides the tracked-file inventory used for deterministic source staging.
- The workflow relies on commit history to assign stable `source_commit` values to staged files.
- The source-pack builder intentionally avoids stamping the current HEAD into staged bytes, because that would churn hashes and defeat OpenKB deduplication.
- Git also supports the repository safety model by enabling rollback when build steps update curated files.
- The source-pack builder uses `git -c core.quotepath=false` to preserve readable path names in inventory and provenance extraction.
- Prerequisite checks treat a missing or non-working Git setup as a hard failure, since later stages depend on repository-aware operations.
- The editorial curation pass uses Git as the source of truth for diff scope, rename detection, and base-vs-working-tree comparison.
- The orphan retraction script uses Git file tracking, content-hash comparison, and commit ancestry to tell whether an orphaned document was deleted, renamed, or merely deselected by current selection rules.
- `ensure_local_alias.py` uses Git's local exclude file rather than shared ignore rules, which keeps the alias a local-only repository artifact.
- Git-backed detection helps protect OpenKB from accidental retraction when a file still exists but the staging policy changed.
- The README's installation guidance reinforces Git's role as part of the repository's controlled bootstrap path: the repository is only made agent-ready once the prerequisite checks and consent-first setup succeed.

## Related Concepts

- [[concepts/deterministic-builds]]
- [[concepts/source-pack-staging]]
- [[concepts/provenance-tracking]]
- [[concepts/git-tracking-policy]]
- [[concepts/toolchain-pinning]]
- [[concepts/repository-inventory]]
- [[concepts/llm-free-knowledge-bootstrap]]
- [[concepts/preflight-checks]]
- [[concepts/deterministic-validation]]
- [[concepts/editorial-curation-passes]]
- [[concepts/safe-automation]]
- [[concepts/orphan-retraction]]
- [[concepts/rename-vs-delete-detection]]
- [[concepts/manifest-authoritative-reconciliation]]
- [[concepts/instruction-file-aliasing]]
- [[concepts/compatibility-fallback]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/local-vs-shared-ignore]]
- [[concepts/consent-first-installation]]
- [[concepts/data-flow-disclosure]]
- [[concepts/graceful-degradation]]

## Related Pages

- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

## Related Documents
- [[summaries/README-md]]
