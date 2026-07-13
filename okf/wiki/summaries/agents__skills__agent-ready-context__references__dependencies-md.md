---
type: "Summary"
description: "Defines dependency rules, tool requirements, and safe install policies for the agent-ready-context skill."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__references__dependencies-md.md"
---

# Summary

This document defines the dependency model for the `agent-ready-context` skill and explains how to keep the workflow spec-compliant, portable, and safe.

## Key points

- The skill must not invent a custom `dependencies` field in `SKILL.md`; instead, it should rely on standard frontmatter fields such as `compatibility`, `allowed-tools`, and namespaced `metadata.*` hints.
- `scripts/check_prereqs.py` is the source of truth for readiness checks, and bundled scripts should run through `uv run` when possible.
- Required local tools are `git`, `uv`, Python 3.11+, and writable repository paths for `okf/.okf-build/`, `okf/`, and `.agents/skills/`.
- Optional tools include `graphify` for exploration, `openkb` for semantic ingestion, and web access only when external documentation or baseline refresh is needed.
- Companion skills such as `skill-creator` and `subagent-profile-adapter` are treated as follow-up capabilities, not hard runtime dependencies; the workflow must degrade gracefully if they are absent.

## Tooling and pinning

The document emphasizes strict provenance and pinning for installable dependencies:

- Exact versions must be pinned in any command left behind.
- Integrity hashes must be recorded alongside version pins in the target repository's `AGENTS.md`.
- Installs should respect the environment's configured Python index and never hardcode or bypass mirrors.
- Updates must be explicit: detect newer versions, review release notes, and only update after user confirmation.

A notable compatibility warning is included for `openkb`: some releases that pin `openai-agents==0.17.x` can break `openkb lint` when `openai` resolves to `>=2.45.0`, so the install may need an additional `--with 'openai==2.44.0'` constraint until the upstream fix is present.

## Vendoring and bootstrap behavior

The document requires that vendor skill copies land in `.agents/skills/` before the corresponding CLI is used:

- `graphify` should be vendored via its project-scoped installer when possible.
- `openkb` should be vendored manually from the pinned upstream tag.
- Optional deck/critic skills may be vendored separately when relevant.

It also distinguishes between project-scoped adoption and harness-wide installation, making clear that the default workflow should stay repository-local and consent-first.

## Broader concepts

This document ties together [[concepts/dependency-management]], [[concepts/supply-chain-security]], tool readiness, and [[concepts/vendor-skill-adoption]]. It also frames a practical model for [[concepts/graceful-degradation]] when optional companion skills or tools are missing.

## Related Concepts
- [[concepts/provenance-aware-tool-installation]]
- [[concepts/trust-on-first-use]]
- [[concepts/consent-first-tooling]]
- [[concepts/toolchain-pinning]]
- [[concepts/integrity-pinning]]
- [[concepts/version-pinning]]
- [[concepts/skill-vendoring]]
- [[concepts/tooling-consent-and-pin-management]]
- [[concepts/preflight-checks]]
- [[concepts/filesystem-validation]]
- [[concepts/harness-vs-local-tools]]
- [[concepts/local-by-default-tooling]]
- [[concepts/openkb-wiki-health-checks]]
- [[concepts/quality-gates]]

## Entities
- [[entities/check-prereqs-py]]
- [[entities/agent-ready-context-skill]]
- [[entities/skill-creator]]
- [[entities/subagent-profile-adapter]]
- [[entities/uv]]
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/openkb]]
- [[entities/python]]
- [[entities/git]]
- [[entities/astral]]
- [[entities/okf-spec]]
- [[entities/okf-wiki]]
- [[entities/openkb-lifecycle]]
- [[entities/runtime-detection-md]]
- [[entities/agents-md]]
- [[entities/agent-ready-context]]
- [[entities/tooling]]
