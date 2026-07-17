---
type: Concepts
title: Harness-specific runtime adapters and profiles
description: How subagent/profile adapters are generated for active harnesses
  without becoming source of truth.
timestamp: 2026-07-16T07:21:44.902Z
sources:
  - .agents/skills/subagent-profile-adapter/SKILL.md
  - .agents/skills/subagent-profile-adapter/references/runtime-detection.md
  - .agents/skills/subagent-profile-adapter/references/tooling-context-policy.md
  - AGENTS.md
---

# Harness Adapters and Runtime Profiles

After agent-ready context and action skills are created, `subagent-profile-adapter` can generate harness-specific runtime adapters (profiles, subagents, personas) that point back to canonical sources without becoming a source of truth themselves.

## What are harness adapters?

Adapters are native files generated for the active runtime environment:
- Claude subagents (Anthropic harness)
- OpenAI assistant profiles or system prompts
- LangChain agent roles or personas
- Vendor-specific execution contexts

They are **projections**, not sources of truth. They always point back to:
- Root `AGENTS.md` — canonical orientation
- `okf/wiki/index.md` — canonical context front door
- `.agents/skills/` — canonical action skills

## When to generate adapters

**Prerequisites** (in order):

1. `AGENTS.md` exists and has been refreshed by `agent-ready-context`
2. `okf/wiki/index.md` exists and routes to all major concepts
3. Custom action skills have been created or reviewed (via `skill-creator`) when repeated actions were found
4. User explicitly requests harness adapters

Never generate adapters before context and actions are ready. Adapters are the final optional step, not the first.

## Runtime detection (not binary detection)

Detect the **active harness**, not merely installed tools:

**Prefer explicit runtime signals:**
- Harness environment variables or metadata
- Current agent/task identification from conversation context
- Explicit user statement ("I'm using Claude Desktop")

**Secondary hints (low confidence):**
- Parent process analysis (which program launched this agent)
- Environment variable prefixes
- Installed binary versions

**Never use as proof:**
- Bare `<tool> --version` output
- Presence of an installed binary
- Configuration file existence alone

**If detection remains ambiguous:**
- Ask the user which harness they're using
- Provide a procedure to verify (e.g., "Ask me 'What harness are you running?'")
- Document the detection gap in the run report

## Adapter workflow

### 1. Detect active harness

Inspect environment and runtime metadata for explicit signals. Use `scripts/inspect_runtime_context.py` for helpers:

```bash
uv run .agents/skills/subagent-profile-adapter/scripts/inspect_runtime_context.py
```

### 2. Check harness capabilities

**Does this harness support subagents/profiles?**

- Use local docs (in repo or harness)
- Use official web documentation (official harness docs only)
- Check version compatibility (some harnesses added profiles in recent versions)

If the harness doesn't support local profiles, use `AGENTS.md` directly or create a symlink/alias and record the decision.

### 3. Record tooling evidence

When harness capabilities are understood, optionally record under `okf/wiki/tooling/harnesses/`:

```
okf/wiki/tooling/
├── index.md           # tooling routing and harness listing
├── harnesses/
│   ├── anthropic.md   # Claude/Anthropic harness capabilities and config
│   ├── openai.md      # OpenAI harness capabilities and config
│   └── langchain.md   # LangChain agent framework specifics
└── providers/
    ├── anthropic.md   # Anthropic API configuration
    └── openai.md      # OpenAI API configuration
```

Baseline `agent-ready-context` writes only the minimal harness build record (or justifies its absence). Fuller pages stay for `subagent-profile-adapter` work or manual maintenance.

### 4. Design candidate adapters

Derive profiles from actual repository needs and available skills:

**Good candidates** (task-scoped, permission-bounded):
- `okf-curator` — maintains the OKF wiki through retrieval and synthesis
- `skill-architect` — designs and validates reusable Agent Skills
- `repo-cartographer` — maps repository structure and surfaces
- `security-reviewer` — audits skills and configurations for safety issues
- `dependency-scout` — tracks supply-chain health and updates

**Poor candidates:**
- Generic "developer" role (too broad)
- Copy-paste of full `AGENTS.md` into profile (defeats routing)
- Multiple adapters that essentially duplicate each other
- Profiles with embedded long project context (should point, not inline)

Each adapter should have a clear, narrow purpose and delegation to shared sources.

### 5. Handle AGENTS.md alias

If the harness requires a specific instruction file name but you have `AGENTS.md`:

**Option 1: Symlink** (recommended if allowed)
```bash
uv run .agents/skills/subagent-profile-adapter/scripts/ensure_local_alias.py \
  --source AGENTS.md \
  --alias <harness-specific-name> \
  --track local
```

Add to `.git/info/exclude` so symlink isn't tracked but isn't gitignored globally.

**Option 2: Copy + track**
```bash
cp AGENTS.md <harness-specific-name>
```

Add to `.gitignore` or commit based on team policy (ask user).

**Option 3: Point in config**
- Harness configuration file points to `AGENTS.md` directly
- No alias needed if harness supports path configuration

Choose based on harness capabilities and team preference.

### 6. Write native adapter files

For each candidate profile/subagent:

**Do:**
- Read current harness documentation (official source only)
- Implement native format directly from docs
- Keep short: purpose, description, instructions to consult AGENTS.md/wiki/skills
- Reference canonical sources by path or URL
- Make activation/description clear and concise

**Don't:**
- Rely on hardcoded vendor renderers or templates
- Assume fields are stable between harness versions
- Embed long project context (link instead)
- Use deprecated harness features

Example structure for Claude subagent:

```yaml
name: okf-curator
description: Maintains agent-smith's OKF wiki through retrieval and synthesis
instructions: |
  You are the OKF (Open Knowledge Format) curator for this repository.
  
  Start with: AGENTS.md (orientation) → okf/wiki/index.md (routing) → okf/wiki/quickstart.md (onboarding)
  
  When asked to create, refresh, or validate the knowledge base, follow:
  - .agents/skills/agent-ready-context/SKILL.md (authoritative workflow)
  - okf/wiki/INSTRUCTIONS.md (preservation contract)
  
  Use skills from .agents/skills/ when repeated actions emerge.
  
  Cite repository paths and external URLs with access dates.
  Never commit secrets or build artifacts.
tools: []  # Harness-specific tool list if supported
```

### 7. Ask about tracking preference

**How should generated harness files be tracked?**

Option 1: **Local-only** (default)
- Add to `.git/info/exclude` per-user
- Each developer can have their own harness adapters
- Team doesn't see them; no merge conflicts

Option 2: **Gitignored globally**
- Add patterns to `.gitignore`
- Harness files never committed
- Useful if different team members use different harnesses

Option 3: **Committed as shared team adapters**
- Include in repository
- Team has consistent adapters
- Requires coordination if harness versions diverge

Default to local-only if team policy is undefined.

### 8. Validate outputs

**Syntax check**: Does the profile file parse in the native harness format?

**Coverage check**: Do instructions clearly point to canonical sources (AGENTS.md, wiki, skills)?

**Activation check**: Does the harness load and recognize the profile correctly?

Test the adapter in a real harness session before finalizing.

## Updating adapters

When harness capabilities change (new version, new fields):

1. Check official harness documentation
2. Update adapter file with new fields/format
3. Validate in harness
4. Re-run `subagent-profile-adapter` to incorporate any policy changes

Never hand-edit adapters; use the skill to regenerate them so changes are traceable.

## Tooling context policy

The `okf/wiki/tooling/` directory holds two optional things:

1. **Minimal harness build record** — written by every `agent-ready-context` run (or explicitly skipped with justification)
   - Which harness was detected (or why detection was ambiguous)
   - Whether local profiles are supported
   - High-level configuration needed

2. **Fuller harness evidence** (optional, from `subagent-profile-adapter` work)
   - Detailed capability matrix
   - Version-specific notes
   - Local configuration guide

Link policy:
- `tooling → project` allowed (tooling pages can reference core AGENTS.md, wiki, skills)
- `project → tooling` forbidden (core pages never depend on local tooling context)
- Root `okf/wiki/index.md` must still route to `tooling/index.md` so bundle stays spec-navigable

This keeps tooling evidence available without making it load-bearing for project knowledge.

## Adapter lifecycle

Adapters change less frequently than code but should track major releases:

- **New harness version** with breaking changes → regenerate profiles
- **New skill created** → update profiles to mention it
- **Major wiki restructure** → review adapter links
- **Harness sunset** → remove adapter, document in AGENTS.md

Profiles are disposable; they can be regenerated anytime without data loss because they point to sources, not embed sources.

## Citations

- `/.agents/skills/subagent-profile-adapter/SKILL.md` — skill overview and workflow
- `/.agents/skills/subagent-profile-adapter/references/runtime-detection.md` — detecting active harness vs. installed binaries
- `/.agents/skills/subagent-profile-adapter/references/tooling-context-policy.md` — what goes under okf/wiki/tooling/ and link policy enforcement
- `/.agents/skills/subagent-profile-adapter/scripts/inspect_runtime_context.py` — runtime context inspection helpers
- `/AGENTS.md` — canonical orientation (where adapters point)
