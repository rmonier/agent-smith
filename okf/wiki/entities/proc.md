---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md"]
type: "Other"
description: "Linux /proc process information filesystem used for runtime inspection"
---

# proc

`proc` is the Linux process information filesystem mounted at `/proc`. In this document, it is used as a read-only runtime signal source for inspecting the current process and its parent chain without invoking external commands.

## What it provides here

- `read_proc(pid)` reads `/proc/<pid>/comm`, `/proc/<pid>/cmdline`, and `/proc/<pid>/stat`.
- The script uses those fields to capture process names, command lines, and parent process IDs.
- `parent_chain()` walks upward from the current process through ancestors until it reaches PID 1 or a limit.
- The collected data becomes part of the runtime-harness detection report in [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]].

## Why it matters

- `proc` enables [[concepts/non-invasive-detection]] by exposing runtime context directly from the operating system.
- It supports [[concepts/runtime-signal-prioritization]] by providing stronger evidence than repository markers alone.
- It helps with [[concepts/adaptive-harness-detection]] because parent-process names and command lines can hint at the active harness.

## Notes

- The script treats `proc` data as evidence, not proof.
- If `/proc` is unavailable, `read_proc()` returns `None` and the inspection degrades gracefully.
- This makes the utility more robust for environments where process introspection is restricted or absent.

## Related

- [[entities/python]]
- [[entities/scripts-inspect_runtime_context-py]]
- [[concepts/runtime-ambiguity-resolution]]