---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"]
description: "Rules for separating agent tooling, context, and runtime-specific adapters."
---

# Tooling Boundaries

Tooling boundaries define which repository surfaces are used for executable workflows, which are used for durable knowledge, and which are treated as operational entry points. The goal is to keep agent tooling local and scoped, while preventing it from bleeding into the compiled wiki or human-facing documentation.

## What belongs where

- `AGENTS.md` is the repository orientation layer: setup, build, launch, test commands, safety notes, and pointers to durable context.
- `.agents/skills/` holds repeatable agent actions such as scripts, checks, repairs, and transformations.
- `okf/wiki/` holds compiled knowledge, provenance, and durable project facts.
- `okf/wiki/index.md` is the routing surface for wiki discovery and should be read before selecting other wiki pages.
- `graphify-out/` provides structural analysis to help choose files, but it is not the source of truth.
- `okf/.okf-build/` is staging-only space for deterministic source packs and findings; it is not the compiled knowledge base.
- Harness-specific subagent or profile adapters are runtime projections only; they should be generated from the current harness context, keep short, and point back to `AGENTS.md`, `okf/wiki/`, and skills rather than embedding project knowledge.

The README makes this layering explicit by splitting the repository into orientation, context, actions, and harness projections. It also frames the repo as an [[concepts/agent-ready-repositories|agent-ready repository]]: a codebase that carries enough structured orientation, durable memory, and actions for agents to operate without repeatedly re-deriving the same understanding.

The source template in [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]] reinforces the same separation by telling agents to keep operational basics in `AGENTS.md`, push conventions and rationale into the wiki, and treat wiki content as data rather than instructions. The workflow document extends that boundary by requiring the wiki index to drive subsequent reads, making the index the first routed knowledge source after `AGENTS.md` and keeping discovery index-based rather than ad hoc.

The subagent-profile-adapter skill adds a runtime-specific layer to this model: it treats subagent/profile adapters as harness-native projections, not as portable standards or sources of truth. It also says adapter generation should begin only after `AGENTS.md`, `okf/wiki/`, and reusable skills are in place, which reinforces the separation between durable context and runtime-specific execution surfaces.

## Core boundaries

### Operational vs durable

Operational guidance is allowed in the agent-facing layer when it helps a tool or workflow run consistently. Durable knowledge belongs in the wiki so it can be linked, reviewed, and refreshed independently of the execution path. This supports [[concepts/documentation-layer-separation]] and [[concepts/knowledge-layer-separation]].

The README's surface split also shows how the repository avoids mixing compiled memory with procedural steps: `AGENTS.md` carries orientation, `.agents/skills/` carries actions, and `okf/wiki/` carries compiled context. That arrangement depends on [[concepts/context-action-separation]] and [[concepts/context-surface-management]] as much as it does on documentation organization.

The workflow also distinguishes staging from knowledge publication: source files are packed into `okf/.okf-build/input/` first, then ingested into OpenKB later. That keeps [[concepts/source-pack-staging]] separate from compiled output and helps preserve [[concepts/deterministic-builds]] and [[concepts/deterministic-validation]].

### Local vs shared

The README emphasizes that vendor skills installed by a manager are read-only and that custom project skills live only under `.agents/skills/`. That is a local-by-default model for tool behavior, aligned with [[concepts/local-by-default-tooling]], [[concepts/tooling-context-isolation]], and [[concepts/skill-vendoring]].

Its installation guidance also matters for boundary-setting: only the three product skills are meant to be copied into a target repository, while vendored `graphify` and `openkb` copies remain repository-specific toolchain artifacts. That distinction supports [[concepts/tooling-vendoring]] and [[concepts/vendor-skill-adoption]] by keeping reusable product skills separate from pinned upstream tool copies.

The subagent-profile-adapter skill sharpens this further by treating harness-specific adapters as local runtime artifacts. It recommends asking the user how generated files should be tracked, with local-only as the default, and it explicitly warns against assuming a runtime from installed binaries alone. That makes adapter generation a form of [[concepts/runtime-adapter-management]] guided by [[concepts/runtime-ambiguity-resolution]] and [[concepts/runtime-signal-prioritization]].

### Instructions vs context

The wiki is for context, not instructions. Agents should use it to understand the repo, not to execute procedures. This separation reduces confusion between [[concepts/action-oriented-documentation]] and [[concepts/durable-context]].

The README also describes a progressive-disclosure model: deeper knowledge stays out of orientation and action files, while each surface is loaded only when useful. That reinforces [[concepts/progressive-disclosure]], [[concepts/documentation-architecture]], and [[concepts/knowledge-boundaries]].

The workflow makes the distinction operational by requiring external documentation URLs to be treated as evidence, not hidden memory or instructions, and by separating evidence staging from wiki compilation. It also requires disclosure before the first LLM-backed command, which reinforces [[concepts/data-flow-disclosure]] and [[concepts/wiki-content-as-untrusted-data]].

The subagent-profile-adapter skill adds another distinction: harness docs are evidence for writing native adapter files, but project concept pages must not depend on tooling pages. That strict directionality keeps tooling context available for adapter work without letting it become project truth.

## Source-driven expectations

From the README, the template document, the workflow, and the subagent-profile-adapter skill, the main boundary rules are:

- Keep `AGENTS.md` focused on runtime basics and repo-specific orientation.
- Put conventions, rationale, and long-lived knowledge in the wiki.
- Never deep-link individual wiki pages from `AGENTS.md`; point to `okf/wiki/index.md` instead.
- Treat `okf/wiki/index.md` as the first routed knowledge source after `AGENTS.md`.
- Use `.agents/skills/agent-ready-context/` when refreshing or validating the OKF bundle.
- Avoid direct edits to OpenKB-managed compiled pages except where the workflow explicitly allows it.
- Keep `okf/` out of the repo graph so the wiki does not feed back into its own structural analysis.
- Stage source material first, then ingest it, then validate the compiled bundle.
- Reconcile deleted or moved sources before ingest so stale pages do not survive as orphans.
- Generate harness-specific subagent/profile adapters only from current docs and local runtime evidence, and keep them short and non-authoritative.
- Prefer local-only tracking for generated harness adapters unless the user chooses a shared policy.
- Validate tooling-link policy so project pages do not link back into `okf/wiki/tooling/`.

These rules reinforce [[concepts/agent-context-layering]], [[concepts/index-based-discovery]], [[concepts/knowledge-base-navigation]], and [[concepts/self-reference-control]]. They also connect to [[concepts/orphan-retraction]] and [[concepts/source-driven-regeneration]], because the workflow explicitly prefers source fixes and re-ingestion over hand-editing generated pages.

The README adds a broader repository-transformation view: the repo is not just documented, it is compiled into an agent-ready structure with orientation, memory, and actions. That broader framing ties tooling boundaries to [[concepts/knowledge-compilation-pipeline]], [[concepts/compiled-knowledge-bases]], and [[concepts/repository-transformation-pipelines]].

The subagent-profile-adapter skill also ties into [[concepts/permission-scoped-agents]], [[concepts/subagent-role-design]], and [[concepts/harness-native-profiles]] by framing adapters as task-scoped, permission-bounded projections of the current harness. That makes generated profiles useful without turning them into a portable standard.

## Why this matters

Clear tooling boundaries prevent a repo from turning into a mixed-purpose dump of instructions, knowledge, and automation. They help agents:

- find the right starting point quickly,
- avoid treating generated knowledge as source code authority,
- preserve repository-specific conventions in a stable place,
- keep harness-specific adapters local and short,
- and keep knowledge refreshes reproducible and reviewable.

The README strengthens this by showing that the same boundary model is part of the project's core product, not just a maintenance convenience. It frames the repo as a deliberate split between portable skills, compiled knowledge, and orientation files, which supports [[concepts/generated-content-governance]], [[concepts/compiled-knowledge-bases]], and [[concepts/read-only-kb-operations]]. The workflow adds a final guardrail: validation should be structural and deterministic, while semantic health reporting stays separate and non-blocking. That keeps the wiki maintainable without turning every refresh into an ad hoc manual review.

## Related concepts

- [[concepts/tooling-context-governance]]
- [[concepts/tooling-context-pages]]
- [[concepts/tooling-navigation-exception]]
- [[concepts/agents-md-maintenance]]
- [[concepts/consent-first-tooling]]
- [[concepts/skill-governance]]
- [[concepts/agent-orientation-index]]
- [[concepts/okf-workflow-governance]]
- [[concepts/repo-ingestion-pipelines]]
- [[concepts/runtime-adapter-management]]
- [[concepts/harness-native-profiles]]
- [[concepts/subagent-role-design]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]