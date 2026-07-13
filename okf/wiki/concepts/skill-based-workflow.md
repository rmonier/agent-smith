---
type: "Concept"
sources: ["summaries/README-md.md"]
description: "Using reusable skills as the main unit of agent work and repo transformation."
---

# Skill-Based Workflow

[[concepts/skill-based-workflow]] describes a repository operating model where repeated agent work is packaged into reusable skills instead of being handled ad hoc. In this model, the repository is transformed through a small set of durable procedures that agents can invoke consistently, validate deterministically, and extend over time.

The README for [[summaries/README-md]] presents this as part of the broader agent-smith architecture: keep orientation in `AGENTS.md`, durable knowledge in `okf/wiki/`, and repeatable actions in `.agents/skills/`. The result is a workflow where actions are explicit, scoped, and portable across harnesses.

## Core idea

The workflow treats recurring repository tasks as first-class capabilities. Rather than asking an agent to rediscover how to do the same work each time, the work is captured in skills with clear boundaries, inputs, and validation steps.

This supports:

- [[concepts/action-oriented-documentation|action-oriented documentation]] for operational procedures
- [[concepts/context-action-separation|context-action separation]] between knowledge and executable steps
- [[concepts/portable-skill-contract|portable skill contracts]] that can move between repositories
- [[concepts/skill-authoring|skill authoring]] for turning repeated work into reusable skills

## How the README applies it

The README describes three product skills that embody the workflow:

- `agent-ready-context` for repository transformation and wiki compilation
- `skill-creator` for converting repeated actions into new skills
- `subagent-profile-adapter` for generating harness-specific adapters

These skills are framed as the actual distributable product of the repository, while other `.agents/skills/` directories may be vendored tool copies. That distinction reinforces the workflow’s emphasis on [[concepts/skill-vendoring|skill vendoring]] versus core capabilities.

## Why it matters

A skill-based workflow makes repository operations:

- repeatable instead of improvisational
- easier to validate with [[concepts/skill-validation-workflow|skill validation workflow]]
- safer through [[concepts/consent-first-workflows|consent-first workflows]] and explicit routing
- more maintainable because repeated actions are centralized and reused
- better suited to agents that should operate from compact, high-signal instructions

It also aligns with [[concepts/agent-ready-repositories|agent-ready repositories]] by ensuring the repo carries the procedures an agent needs to act effectively.

## Related patterns

Skill-based workflow sits alongside several other repository governance ideas:

- [[concepts/agent-context-layering|agent context layering]] for separating orientation, context, and actions
- [[concepts/managed-document-sections|managed document sections]] for keeping generated content stable under regeneration
- [[concepts/incremental-compilation|incremental compilation]] for updating knowledge without rebuilding everything
- [[concepts/evidence-backed-skill-initialization|evidence-backed skill initialization]] for grounding new skills in observed work
- [[concepts/generated-artifact-adoption|generated artifact adoption]] for promoting validated output into the repository

In short, the concept says that agents should not just use tools; they should operate through skills that encode the repository's repeated work into stable, reviewable procedures.