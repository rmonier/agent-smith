---
type: "source-file"
title: ".agents/skills/subagent-profile-adapter/references/runtime-detection.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/subagent-profile-adapter/references/runtime-detection.md"
source_path: ".agents/skills/subagent-profile-adapter/references/runtime-detection.md"
source_kind: "markdown"
source_hash: "sha256:6b99017bc2c27423d4d88b69e5526ff010d8fb6b42f0979ad7f4c3ecf1cb9d42"
source_commit: "ee31be43bdae04171c7b76d789f4d2cfbcc9b2db"
tags: [source-file, markdown]
---

# .agents/skills/subagent-profile-adapter/references/runtime-detection.md

~~~
# Runtime detection

The goal is to identify the **active harness** that is executing the agent, not every tool installed on the machine.

## Reliable signals

Prefer, in order:

1. Explicit harness/runtime metadata supplied by the current agent environment.
2. Explicit user instruction such as "target OpenCode" or "I am running Claude Code".
3. Parent process chain showing the active CLI or harness process.
4. Harness-specific environment variables that are known to be set by the running harness.
5. Repository configuration files, only as low-confidence hints.

## Non-signals

Do not infer the active runtime from:

- `<tool> --version` succeeding;
- a binary existing in `$PATH`;
- global config folders in the user's home directory;
- old generated profile folders in the repo.

A user can have several harnesses installed but run only one of them.

## Ambiguity handling

If signals conflict or are weak, ask the user which harness to target and whether profile generation should be skipped.

Suggested prompt:

```text
I could not confidently identify the active harness. Which harness should I target for local subagent/profile adapters, or should I skip this step?
```

## Inspection helper

The helper script gathers hints without invoking vendor CLIs:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/inspect_runtime_context.py --repo .
```

Treat the output as evidence, not authority.
~~~
