---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md"]
description: "Design of narrow, runtime-bound subagent roles for specific harnesses"
---

# Subagent Role Design

Subagent role design is the practice of defining narrow, permission-bounded task roles for local subagents or profile-based agents in a specific harness. It focuses on what a subagent should do at runtime, how that runtime is recognized, and how to keep the role separate from durable project knowledge.

## What it is for

- Turn existing agent-ready repository context into harness-native subagent or profile adapters.
- Keep each role focused on a bounded job such as repository inspection, skill creation, runtime detection, or OKF curation.
- Separate runtime execution roles from durable project knowledge stored in [[concepts/compiled-knowledge-bases]] and expressed through [[concepts/agent-ready-context-skill]].
- Support [[concepts/adaptive-harness-detection]] so role design starts from evidence about the active runtime rather than assumptions.

## Core design principles

- Roles should be derived from real repository needs, not invented as generic personas.
- Each role should stay small and task-scoped, with only the permissions and tools required for the job.
- Profiles should point back to shared guidance like `AGENTS.md`, `okf/wiki/`, and skills, rather than duplicating long context.
- Adapter files are runtime projections, so they should not become a source of truth for the project.
- Role definitions should work with runtime-signal prioritization: explicit environment values are stronger than process clues, which are stronger than repo markers.

## Runtime constraints

- First identify the active harness using runtime signals, not just installed binaries, aligning with [[concepts/adaptive-harness-detection]] and [[concepts/runtime-ambiguity-resolution]].
- Use explicit environment variables when available, then parent-process inspection and environment hints, and treat repository markers as weaker evidence.
- Do not treat the presence of local tools, repo files, or marker directories as proof of the active runtime.
- Check whether the active environment actually supports local subagents or profiles before designing one.
- Prefer harness-native files and conventions, which connects this concept to [[concepts/harness-native-profiles]] and [[concepts/runtime-adapter-management]].
- If the harness is ambiguous, ask the user which target runtime to support.

## Boundary rules

- `AGENTS.md` remains the canonical orientation and best-practices file.
- Agent Skills define reusable actions, while subagent/profile adapters are runtime-specific outputs.
- OKF wiki pages hold durable project knowledge and provenance, while adapters remain disposable or harness-local.
- Tooling context should inform project work, but project concept pages must not depend on tooling pages, consistent with [[concepts/tooling-context-governance]] and [[concepts/tooling-link-policy]].
- Runtime detection scripts should be passive and non-invasive, avoiding CLI probing that confuses installed binaries with active harness identity.

## Workflow implications

- Use the existing repository context to decide which roles are actually useful.
- Prefer a few clear roles over many overlapping ones to reduce adapter bloat.
- Ask how generated harness files should be tracked: local-only, ignored, or committed.
- Validate that generated profiles are short, correctly placed, and free of embedded project dumps.
- When a role depends on runtime detection, capture the confidence level and signals that led to the choice.

## Why it matters

Good subagent role design reduces confusion between durable knowledge and runtime behavior. It helps a repository support multiple harnesses without turning one harness's profile format into a project dependency. By grounding role selection in explicit signals, parent-process evidence, and repo markers only as hints, it keeps the system easier to maintain, easier to validate, and less likely to drift from the compiled knowledge base.

## Related source

- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]