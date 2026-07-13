---
sources: ["summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md"]
type: "Work"
description: "Upstream OpenKB compiler module mirrored by a local fallback"
---

# OpenKB Agent Compiler

OpenKB Agent Compiler is the upstream `openkb/agent/compiler.py` module referenced as the source of a compatibility fallback in `scripts/editorial_pass.py`.

## What it is

- A specific upstream code module from [[entities/openkb]] used as the provenance source for mirrored behavior.
- Identified in the third-party notices for [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]].
- Associated with release tag `v0.4.4` and commit `bd9fe3989e71fc8012b19eb305662fa307f0a799`.

## Why it matters

- It defines the private symbols that the local script mirrors when the installed OpenKB environment cannot import the private API.
- The notices distinguish between verbatim reuse and clean-room style reimplementation, which connects this module to [[concepts/compatibility-fallback]], [[concepts/clean-room-reimplementation]], and [[concepts/provenance-tracking]].
- Its Apache-2.0 licensing and Vectify AI copyright attribution are part of the reuse record, connecting it to [[concepts/apache-license-2-0]] and [[concepts/licensing-and-attribution]].

## Documented symbols

- `_KNOWN_TARGETS_USER`: copied verbatim into the local fallback.
- `_format_known_targets`: logic mirrored by the local `_format_targets_mirrored` function.

## Scope of reuse

- The fallback is only used when the private compiler API is unavailable in the installed tool environment.
- The notices state that this affects only the wording of `--brief` output, not the correctness gates of `editorial_pass.py --check`.
- The module is treated as an external upstream reference rather than a bundled dependency.

## Related pages

- [[entities/editorial_pass-py]]
- [[entities/openkb]]
- [[entities/vectify-ai]]
- [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]]