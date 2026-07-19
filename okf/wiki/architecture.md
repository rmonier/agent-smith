---
type: Architecture
title: Agent-smith architecture and component boundaries
description: The separation of skills (actions), OKF wiki (context), AGENTS.md
  (orientation), and harness adapters.
timestamp: 2026-07-19T18:17:36.000Z
sources:
  - README.md
  - AGENTS.md
  - .agents/skills/agent-ready-context/SKILL.md
  - .agents/skills/skill-creator/SKILL.md
  - .agents/skills/harness-profile-adapter/SKILL.md
---

# Agent-Smith Architecture

`agent-smith` transforms any repository into an agent-ready system by splitting responsibility across four complementary surfaces:

## Core surfaces

| Surface | Role | Format | Authority |
|---------|------|--------|-----------|
| **Skills** | Repeatable actions, scripts, validations, procedures | Agent Skills YAML + PEP 723 Python scripts | Portable; vendor skills read-only |
| **OKF Wiki** | Durable context, architecture, decisions, evidence, provenance | Open Knowledge Format v0.1 Markdown with YAML frontmatter | Project truth; maintained through OpenWiki |
| **AGENTS.md** | Routing map, setup/test commands, repo rules, toolchain pins | Agents.md convention | Source of truth for operational basics |
| **Harness adapters** | Runtime projections for active harness only | Native harness formats (profiles, subagents, etc.) | Generated from OKF + skills; never source of truth |

## Responsibility boundaries

Keep knowledge split by purpose to minimize context load and enable progressive disclosure:

### Skills = Actions
- Repeatable procedures, scripts, tool orchestrations, validations, transformations
- Procedural guidance: SKILL.md stays under 500 lines; heavy details go to `references/`
- Deterministic code: PEP 723-marked Python scripts under `scripts/`, run via `uv`
- Templates and resources: static files under `assets/` for copying/adaptation
- Security: consent-first installs, version-pinned, user-scoped, minimal `allowed-tools`, environment variables for credentials
- Location: `.agents/skills/<skill-name>/`
- Project skills are always editable; vendor skills read-only

### OKF Wiki = Context
- Architecture, design decisions, external evidence, citations, operational rationale
- Source of truth: `okf/wiki/index.md` is the canonical front door
- Preserved during updates: manual prose, caveats, formatting survive unrelated changes
- Compactness: avoid redundancy; organize by question/concern, not by file/class/directory
- Grounding: every claim outside bundle root (`index.md`, `log.md`) needs YAML frontmatter `sources` field or `## Citations` section citing repository paths
- Maintenance: deterministic producer (OpenWiki) + preservation contract (`INSTRUCTIONS.md`)
- Location: `okf/wiki/`

### AGENTS.md = Orientation
- Short routing map: links to wiki, skills, and when to consult source/tests
- Operational basics: setup, build, test commands; toolchain versions/pins; prerequisites
- House rules: repo-specific safety notes, consent boundaries, escalation paths
- Not a knowledge base: keep it concise; route deeper context to wiki front door
- Never deep-link to individual wiki pages; point to `okf/wiki/index.md` and let it route

### Harness adapters = Runtime projections
- Two distinct duties: baseline harness-visibility bridging (is `AGENTS.md`/`.agents/skills/` natively discoverable? bridge whichever isn't, via a local alias — not optional, applies whenever context + action skills exist) and optional runtime subagent/profile/persona generation (only when the user requests it, after the above)
- Neither is source of truth: point back to canonical AGENTS.md, wiki, and skills
- Adapters proper are short: purpose, activation, permissions hint, and instructions to consult primary sources
- Local-only by default (`.git/info/exclude`), unless team policy is explicit
- Location: harness-specific; documented under `okf/wiki/tooling/` when recorded

## The production surface

The complete transformable product is three portable skills under `.agents/skills/`:

1. **`agent-ready-context`** — the core pipeline
   - Checks prerequisites and bootstraps missing tooling (consent-first)
   - Manages the OpenWiki lifecycle: staging, validation, promotion
   - Maintains `AGENTS.md` orientation and pin records
   - Provides deterministic zero-LLM fallback (skeleton without provider work)
   - `/scripts/run_openwiki_staged.py` — the isolated staging wrapper

2. **`skill-creator`** — turns repeated actions into portable skills
   - Scaffolds new action skills under `.agents/skills/`
   - Enforces security defaults: consent, pinning, minimal permissions, secret hygiene
   - Validates against testing baseline (pressure-test before and after)
   - Reusable across repositories

3. **`harness-profile-adapter`** — baseline harness-visibility bridging (not optional) plus optional harness adapter generation
   - Detects active runtime (not just installed binaries)
   - Bridges instruction-file and skills-directory discovery when the harness can't find `AGENTS.md`/`.agents/skills/` natively
   - Generates native profiles pointing to canonical AGENTS.md, wiki, skills
   - Records tooling evidence under `okf/wiki/tooling/`
   - Runs only after context + action skills are ready

OpenWiki is an external runtime dependency (not a product skill), pinned as an exact released npm package version and installed with user consent under `okf/.openwiki/` (local producer state, never version-controlled).

## Progressive disclosure model

1. **Entry point**: Read root `AGENTS.md` first
2. **Context routing**: Follow `okf/wiki/index.md` and let it determine which pages to open next
3. **Action discovery**: Check `.agents/skills/` when a repeated procedure emerges
4. **Harness runtime**: Inspect local `okf/wiki/tooling/` and run detection only when needed
5. **Source authority**: Consult repository source, tests, Git history, manifests, CI as final authority

## Zero-LLM baseline

The architecture degrades gracefully when OpenWiki is unavailable or declined:

- Prerequisite check still runs (`scripts/check_prereqs.py`)
- Deterministic skeleton builds without provider work (`scripts/build_okf_skeleton.py`)
- Citations and validation remain operational
- Wiki gains source-verified facts but no semantic compilation
- Report explicitly states why semantic work was skipped

## Citations

- `/README.md` — project overview, skills comparison
- `/AGENTS.md` — operational basics, toolchain pins, boundary rules
- `/.agents/skills/agent-ready-context/SKILL.md` — core skill workflow and authority
- `/.agents/skills/skill-creator/SKILL.md` — action skill design and security defaults
- `/.agents/skills/harness-profile-adapter/SKILL.md` — harness adapter boundaries and runtime detection
