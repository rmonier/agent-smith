---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
description: "Workflows that require explicit approval before risky or scope-expanding actions."
---

# Consent-First Workflows

Consent-first workflows require explicit user approval before actions that are risky, irreversible, optional, or otherwise change the user's environment, repository state, or data flow. In the OpenKB workflow model, consent is not a one-time prompt; it is a recurring control that gates bootstrapping, dependency installation, validation setup, regeneration, and any step that could expand scope beyond what the user intended.

## Core idea

The workflow treats the user as the authority for actions that cross a trust, scope, or safety boundary. Instead of assuming permission, the process pauses, explains the tradeoff, and offers a degraded path when possible. This is closely related to [[concepts/safe-automation]], [[concepts/permission-scoped-agents]], and [[concepts/data-flow-disclosure]].

Consent-first behavior also fits with [[concepts/graceful-degradation]] and [[concepts/progressive-disclosure]]: when a preferred tool, provider, or capability is missing, the agent should describe the fallback path rather than force an unsupported setup or silently shift the execution model.

The workflow model also separates orientation, durable context, and actions into distinct surfaces so the agent can ask for permission only when a step changes the repository or the environment, while still keeping the rest of the workflow deterministic and composable. That design aligns consent with [[concepts/context-action-separation]] and [[concepts/documentation-layer-separation]].

In skill initialization, the same principle appears as a guarded bootstrap path: a skill creator script normalizes the requested skill name, validates the target location, and refuses to write outside the expected `.agents/skills` area without an explicit override. It also treats existing targets as immutable unless `--force` is supplied, and it restricts resource directory creation to a small approved set. That makes skill scaffolding predictable while still requiring the user to opt into updates and structure changes. This is closely related to [[concepts/skill-scaffolding]], [[concepts/path-safety]], [[concepts/kebab-case-normalization]], and [[concepts/project-scaffolding]].

## How it appears in the source workflow

The OpenKB build workflow makes consent a gate at several points:

- Hard prerequisites are checked first, and missing requirements such as `git`, `uv`, or Python 3.11+ stop the process until the user approves bootstrapping.
- Optional tools such as Graphify and OpenKB are not forced; the user may skip them and accept reduced functionality.
- If Graphify or OpenKB are needed, vendored skill copies must exist first, and the pipeline must not proceed past a missing-vendoring flag.
- Git history, Graphify updates, and OpenKB initialization are treated as prerequisites that may require consent if absent or if they change the environment.
- `.gitignore`, `.gitattributes`, and `.graphifyignore` are part of the repository setup, but normalization or policy conflicts must be surfaced instead of silently overwritten.
- Deletion and move reconciliation is reported first, and `--apply` requires consent before any retraction happens.
- CI files and local hooks are offered as optional validation aids, but the document explicitly says not to install them without approval.
- Broad `recompile --all` operations are disallowed without consent.
- External URLs may be materialized as evidence files, or added through `openkb add <url>` only for user-supplied URLs and only with consent.
- The workflow requires disclosure of data flow before the first LLM-backed command.
- The system stops and explains what it needs, including source, pin, integrity plan, and exact command, before any install or bootstrap action.
- Air-gapped operation is explicitly supported, so users can ask for the repository to become agent-ready without sending repository content off the machine.
- Skill creation follows the same pattern: the initializer script will not write into a skill directory that already exists unless `--force` is given, and it rejects invalid resource names before creating any optional subdirectories.

These patterns are described in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] and reinforced by the broader agent-ready context guidance.

## Practical implications

Consent-first design shapes the entire pipeline:

- It prevents silent bootstrap of dependencies the user may not want.
- It protects local repositories from unexpected mutation.
- It keeps optional quality gates optional while still making them easy to enable.
- It supports graceful degradation when tools, providers, or network access are unavailable.
- It makes the agent explain data flow before the first LLM-backed action, reinforcing transparency.
- It avoids hidden reuse of external material by treating fetched content as evidence, not instruction.
- It preserves the distinction between orientation, context, and action surfaces so approval happens at the right layer.
- It makes skill scaffolding safer by requiring explicit confirmation for reuse, overwrite, and non-default resource layout.

## Related constraints

Consent-first workflows usually depend on other KB policies:

- [[concepts/preflight-checks]] for detecting missing requirements before doing work.
- [[concepts/tool-boundaries]] for respecting the division between local, shared, and external systems.
- [[concepts/human-in-the-loop-review]] for review before acceptance of generated or mutated output.
- [[concepts/tooling-consent-and-pin-management]] for combining approval with version pinning and vendoring discipline.
- [[concepts/deterministic-validation]] for keeping the non-LLM gates predictable once the user has approved them.
- [[concepts/agent-context-layering]] for separating orientation, context, and action surfaces so consent can be applied at the right layer.
- [[concepts/agent-ready-repositories]] for the broader goal of making a repository safe and usable for agent-driven work.
- [[concepts/directory-bootstrap]] for the controlled creation of new repository structure.
- [[concepts/filesystem-validation]] for rejecting unsafe or invalid paths before mutation.

## Why it matters

This concept is central to making repository automation trustworthy. It ensures that the agent can be helpful without overreaching, and that expensive, destructive, policy-sensitive, or externally visible actions happen only after the user has been informed and has agreed.

In the OpenKB model, consent is part of the architecture rather than a wrapper around it: the repository becomes agent-ready only when the workflow can explain what it will do, where data will flow, what it will change, and what fallback exists if the user declines.

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

## Related Documents
- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]