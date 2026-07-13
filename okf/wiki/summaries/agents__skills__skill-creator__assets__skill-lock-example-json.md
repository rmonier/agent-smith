---
type: "Summary"
description: "Example skill lock file showing pinned dependency metadata fields."
doc_type: short
full_text: "sources/agents__skills__skill-creator__assets__skill-lock-example-json.md"
---

# Summary

This document is an example JSON lock file for a skill management workflow. It illustrates the expected shape of a lock file rather than defining a production-ready schema.

## Key Points

- The file declares its schema as `example-only`, signaling that it is illustrative rather than authoritative.
- A note warns users not to hand-edit real vendor lock entries unless the relevant tool explicitly supports it.
- The `skills` array contains locked skill dependencies with fields for:
  - `name`
  - `source`
  - `version`
  - `integrity`
- The structure emphasizes reproducibility by pinning a specific version or digest and storing a manager-generated integrity value.

## Main Ideas

- Lock files serve as machine-managed records for dependency state.
- Skill dependencies may come from external registries or tool-specific source identifiers.
- Integrity metadata helps verify that resolved artifacts match expected content.
- The example reinforces the distinction between editable configuration and generated dependency metadata.

## Potential Wiki Links

- [[concepts/lock-file-examples]]
- [[concepts/deterministic-builds]]
- [[concepts/integrity-pinning]]
- generated vs hand-edited files
- [[concepts/skill-based-automation]]

## Takeaway

The document provides a minimal example of how a skill lock file can record pinned source, version, and integrity information for reproducible and verifiable skill dependency management.

## Related Concepts
- [[concepts/dependency-management]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/supply-chain-security]]
- [[concepts/generated-content-governance]]
- [[concepts/tool-boundaries]]
