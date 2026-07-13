---
type: "Summary"
description: "Guidance for identifying the active agent harness from reliable runtime signals."
doc_type: short
full_text: "sources/agents__skills__subagent-profile-adapter__references__runtime-detection-md.md"
---

# Summary

This reference explains how to detect the **active agent runtime/harness** for profile adaptation, emphasizing that the goal is to identify the environment currently executing the agent rather than any tools merely installed on the machine.

## Key points

- Runtime detection should prioritize **high-confidence signals** tied to the current execution context.
- The preferred evidence order is:
  1. Explicit harness/runtime metadata from the current agent environment.
  2. Explicit user instruction naming the target harness.
  3. Parent process chain showing the active CLI or harness.
  4. Harness-specific environment variables known to be set by the running runtime.
  5. Repository configuration files, treated only as low-confidence hints.
- Several common indicators are explicitly rejected as unreliable for determining the active runtime:
  - a `<tool> --version` command succeeding;
  - a binary being present in `$PATH`;
  - global config folders in the user home directory;
  - stale generated profile folders in the repository.

## Ambiguity handling

When runtime evidence is weak or conflicting, the document recommends asking the user directly which harness should be targeted, or whether profile generation should be skipped. This reinforces a cautious approach to [[concepts/runtime-signal-prioritization]] and [[concepts/runtime-ambiguity-resolution]].

Suggested fallback prompt:

> I could not confidently identify the active harness. Which harness should I target for local subagent/profile adapters, or should I skip this step?

## Inspection helper

The document points to an inspection helper:

`uv run .agents/skills/subagent-profile-adapter/scripts/inspect_runtime_context.py --repo .`

This helper collects contextual hints without invoking vendor CLIs. Its output should be treated as supporting evidence rather than definitive authority, aligning with [[concepts/evidence-staging]].

## Related concepts

- [[concepts/runtime-signal-prioritization]]
- [[concepts/runtime-ambiguity-resolution]]
- [[concepts/runtime-adapter-management]]
- [[concepts/tool-boundaries]]
- [[concepts/evidence-staging]]

## Related Concepts
- [[concepts/graceful-degradation]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/source-trust-levels]]
- [[concepts/documentation-source-priority]]
- [[concepts/subagent-role-design]]

## Entities
- [[entities/uv]]
