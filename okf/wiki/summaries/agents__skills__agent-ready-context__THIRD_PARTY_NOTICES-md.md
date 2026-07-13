---
type: "Summary"
description: "Provenance note for an OpenKB compatibility fallback and mirrored symbols."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md"
---

# Summary

This document records third-party provenance for a [[concepts/compatibility-fallback|compatibility fallback]] in `scripts/editorial_pass.py`. It identifies an OpenKB-derived implementation detail that mirrors upstream `openkb/agent/compiler.py`, including the verbatim `_MIRRORED_KNOWN_TARGETS_USER` string and the reimplemented `_format_targets_mirrored` behavior.

## Key points

- The fallback is tied to `scripts/editorial_pass.py`, specifically the `_MIRRORED_KNOWN_TARGETS_USER` constant and `_format_targets_mirrored` function.
- The upstream source is [[entities/openkb|OpenKB]] at `openkb/agent/compiler.py`, release tag `v0.4.4`, commit `bd9fe3989e71fc8012b19eb305662fa307f0a799`.
- The copied material is covered by the Apache-2.0 license, with copyright attributed to Vectify AI.
- `_MIRRORED_KNOWN_TARGETS_USER` is a verbatim copy, while `_format_targets_mirrored` is a clean-room reimplementation that matches upstream behavior.

## Purpose

The fallback exists only when the private `openkb.agent.compiler` API cannot be imported from the installed tool environment. It is a best-effort degradation path that changes only the wording of `--brief` output, not the correctness of `editorial_pass.py --check`.

## Licensing and scope

- The document distinguishes copied code from separately implemented behavior.
- It notes that the rest of the script depends on OpenKB's stable public API (`openkb.lint`) rather than duplicated source.
- It serves as the formal provenance record for the fallback implementation and its licensing context.

## Related concepts

- [[entities/openkb|OpenKB]]
- [[concepts/compatibility-fallback|compatibility fallback]]
- [[concepts/provenance-tracking|provenance tracking]]
- [[concepts/license-compliance-requirements|license compliance]]
- [[concepts/clean-room-reimplementation|clean-room reimplementation]]

## Related Concepts
- [[concepts/compatibility-fallback]]
- [[concepts/clean-room-reimplementation]]
- [[concepts/license-compliance-requirements]]
- [[concepts/provenance-tracking]]
- [[concepts/licensing-and-attribution]]
- [[concepts/graceful-degradation]]
- [[concepts/apache-license-2-0]]
- [[concepts/vendor-backed-validation]]

## Entities
- [[entities/openkb-agent-compiler]]
- [[entities/vectify-ai]]
- [[entities/romain-monier]]
- [[entities/openkb]]
- [[entities/apache-license-2-0]]
- [[entities/editorial_pass-py]]
- [[entities/openkb-cli]]
- [[entities/openkb-lint]]
