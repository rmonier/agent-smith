---
okf_version: "0.1"
---

# Index

## Architecture
- [Agent-smith architecture and component boundaries](architecture.md) — The separation of skills (actions), OKF wiki (context), AGENTS.md (orientation), and harness adapters.

## Concepts
- [Harness-specific runtime adapters and profiles](harness-adapters.md) — How subagent/profile adapters are generated for active harnesses without becoming source of truth.
- [Skills as portable executable action containers](skills-workflow.md) — How to create, validate, maintain, and discover repeatable Agent Skills for procedures, scripts, and tool orchestrations.

## Instructions
- [OpenWiki repository-memory contract](INSTRUCTIONS.md) — Project-owned constraints for compact, editable, grounded OKF memory.

## Policy
- [Security, consent, and data flow in agent-smith](security-and-consent.md) — Consent-first tooling bootstrap, supply-chain pinning discipline, secret hygiene, and data-flow disclosure boundaries.
- [OKF wiki preservation and maintenance contract](wiki-preservation-contract.md) — Rules that every wiki update must preserve; the binding agreement between automated producers and manual editors.

## quickstart
- [Repository memory quickstart](quickstart.md) — Compact front door to agent-smith's durable agent context.

## Reference
- [Agent-Ready Pipeline](agent-ready-pipeline.md) — The `agent-ready-context` skill walks a repository through a deterministic sequence to gain operational orientation, durable context, and portable action capabilities.

## Tooling context (user-scoped)

- [Tooling context](tooling/index.md) — hand-authored local harness and provider observations; local pages are discovered by listing the directory, never enumerated here.
