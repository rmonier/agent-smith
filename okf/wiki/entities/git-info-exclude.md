---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md"]
type: "Other"
description: "Git's local per-repo exclude file for ignored paths"
---

# git/info/exclude

`git/info/exclude` is a repository-local ignore file that Git can use to exclude paths from tracking and scans on a single clone.

## What this page is about

In [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]], `git/info/exclude` appears as part of a privacy and leakage warning: files hidden only through this local exclude mechanism may still be picked up by tooling that does not read it.

## Key facts

- It is local to a repository clone and does not live in committed project metadata.
- It can hide files from Git status and some local workflows.
- The referenced document notes that `graphify update` does not consult `git/info/exclude` when deciding what to scan.
- Because of that, a file excluded only through `git/info/exclude` can still be processed, and if it produces graph nodes, its content may end up in committed artifacts.
- This is presented as [[concepts/local-artifact-leakage]], not provider egress.

## Why it matters

This entity matters for [[concepts/privacy-preserving-tooling]] and [[concepts/local-vs-shared-ignore]] because it shows that local ignore mechanisms are not always sufficient for protecting sensitive files from downstream compilation or export pipelines.

## Related

- [[entities/gitignore]]
- [[entities/graphify]]
- [[entities/graphify-out-graph-json]]
- [[entities/graphify-out-graph-report-md]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]