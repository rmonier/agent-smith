---
type: "source-file"
title: ".agents/skills/graphify/references/hooks.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/graphify/references/hooks.md"
source_path: ".agents/skills/graphify/references/hooks.md"
source_kind: "markdown"
source_hash: "sha256:7910939007ada7966681da02467302f6f1f7c392f42edecd35994aa639e4dee0"
source_commit: "1639ea0c0455e563feea17997ed9f2f18c6b8568"
tags: [source-file, markdown]
---

# .agents/skills/graphify/references/hooks.md

~~~
# graphify reference: commit hook and native AGENTS.md integration

Load this when the user asked to install the post-commit hook or wire graphify into a project's AGENTS.md.

## For git commit hook

Install a post-commit hook that auto-rebuilds the graph after every commit. No background process needed - triggers once per commit, works with any editor.

```bash
graphify hook install    # install
graphify hook uninstall  # remove
graphify hook status     # check
```

After every `git commit`, the hook detects which code files changed (via `git diff HEAD~1`), re-runs AST extraction on those files, and rebuilds `graph.json` and `GRAPH_REPORT.md`. Doc/image changes are ignored by the hook - run `/graphify --update` manually for those.

If a post-commit hook already exists, graphify appends to it rather than replacing it.

---

## For native AGENTS.md integration

Run once per project to make graphify always-on in your agent sessions:

```bash
graphify agents install
```

This writes a `## graphify` section to the local `AGENTS.md` that instructs your agent to check the graph before answering codebase questions and rebuild it after code changes. No manual `/graphify` needed in future sessions.

```bash
graphify agents uninstall  # remove the section
```
~~~
