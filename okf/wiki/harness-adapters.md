---
type: Concepts
title: Harness-specific runtime adapters and profiles
description: How subagent/profile adapters are generated for active harnesses
  without becoming source of truth, and how baseline harness-visibility
  bridging keeps AGENTS.md and .agents/skills/ discoverable.
timestamp: 2026-07-19T18:17:36.000Z
sources:
  - .agents/skills/harness-profile-adapter/SKILL.md
  - .agents/skills/harness-profile-adapter/references/runtime-detection.md
  - .agents/skills/harness-profile-adapter/references/tooling-context-policy.md
  - .agents/skills/harness-profile-adapter/references/harness-docs.md
  - .agents/skills/harness-profile-adapter/scripts/ensure_local_alias.py
  - tests/test_harness_profile_adapter.py
  - AGENTS.md
---

# Harness Adapters and Runtime Profiles

After agent-ready context and action skills are created, `harness-profile-adapter` does two things. First, not optionally: it checks whether the active harness can natively discover root `AGENTS.md` and `.agents/skills/`, and bridges whichever it can't with a local alias — without this, the harness cannot see any of what was just built. Second, only when the user separately wants it: it can generate harness-specific runtime adapters (profiles, subagents, personas) that point back to canonical sources without becoming a source of truth themselves.

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

## When to bridge vs. when to generate adapters

**Prerequisites** (in order), for both of the below:

1. `AGENTS.md` exists and has been refreshed by `agent-ready-context`
2. `okf/wiki/index.md` exists and routes to all major concepts
3. Custom action skills have been created or reviewed (via `skill-creator`) when repeated actions were found

Past that point, this skill covers two things, and only the second is optional:

- **Baseline harness-visibility bridging** — check whether the active harness can natively discover root `AGENTS.md` and `.agents/skills/` at all; bridge whichever it can't with a local alias. Do this whenever `harness-profile-adapter` runs after the prerequisites above, whether or not the user separately wants runtime adapters — without it, the harness cannot see anything `agent-ready-context`/`skill-creator` just built, and no adapter below would help either.
- **Runtime subagent/profile adapters** — generated only when the user explicitly requests them, after the above. Never generate these before context and actions are ready; they are the final optional step, not the first.

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
uv run .agents/skills/harness-profile-adapter/scripts/inspect_runtime_context.py
```

### 2. Check harness capabilities

**Baseline (not optional): does this harness natively discover `AGENTS.md` and `.agents/skills/`?**

- Does it read `AGENTS.md` directly, or require a differently named instruction file?
- Does it scan `.agents/skills/` directly, or only its own dedicated skills directory?
- Does a newly created directory in either location need a session/process restart before the harness picks it up? Many harnesses only scan for skills at startup — say so up front.
- Use local docs (in repo or harness) first, then official web documentation.

If either answer is "no," bridge it — see step 5.

**Optional: does this harness support subagents/profiles?**

- Use local docs (in repo or harness)
- Use official web documentation (official harness docs only)
- Check version compatibility (some harnesses added profiles in recent versions)

If the harness doesn't support local profiles, stop here for this part — the baseline bridging above still applies regardless.

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

Baseline `agent-ready-context` writes only the minimal harness build record (or justifies its absence). Fuller pages stay for `harness-profile-adapter` work or manual maintenance.

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

### 5. Bridge instruction-file and skills-directory discovery

`scripts/ensure_local_alias.py` handles both gaps step 2 may have found, the same way: a local, git-excluded alias pointing back at the canonical source, never a copy — one place to edit either way. It detects file vs. directory from `--source` automatically.

**Instruction file**, if the harness requires a specific name instead of `AGENTS.md`:
```bash
uv run .agents/skills/harness-profile-adapter/scripts/ensure_local_alias.py \
  --repo . --source AGENTS.md --alias <harness-required-name>
```
Tries a relative symlink first; falls back to a small Markdown pointer file if symlinks are unavailable (`--fallback fail` to disable that fallback instead).

**Skills directory**, if the harness only scans its own dedicated directory instead of `.agents/skills/`:
```bash
uv run .agents/skills/harness-profile-adapter/scripts/ensure_local_alias.py \
  --repo . --source .agents/skills --alias <harness-required-skills-dir>
```
Tries a relative symlink first too. On Windows, a directory symlink needs Developer Mode or an elevated process even when a file symlink does not; when it fails, the script falls back to an NTFS junction (`mklink /J`), which needs no elevated privilege. A directory alias has no text-pointer fallback — a harness scanning a directory for skills needs a real directory there — so if neither mechanism works, the script fails loudly with next steps rather than silently producing nothing useful.

Either way: the alias is recorded in `.git/info/exclude` automatically (ask the user first if a team-tracked adapter is wanted instead — see step 7), and re-running is idempotent once the alias exists. If step 2 found that the harness needs a restart to pick up a new directory, say so now rather than after the bridge appears not to have worked.

An alternative when the harness supports it: point the harness's own configuration directly at `AGENTS.md`/`.agents/skills/` — no alias needed. Prefer that over an alias when available.

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
4. Re-run `harness-profile-adapter` to incorporate any policy changes

Never hand-edit adapters; use the skill to regenerate them so changes are traceable.

## Tooling context policy

The `okf/wiki/tooling/` directory holds two optional things:

1. **Minimal harness build record** — written by every `agent-ready-context` run (or explicitly skipped with justification)
   - Which harness was detected (or why detection was ambiguous)
   - Whether local profiles are supported
   - High-level configuration needed

2. **Fuller harness evidence** (optional, from `harness-profile-adapter` work)
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

- `/.agents/skills/harness-profile-adapter/SKILL.md` — skill overview and workflow
- `/.agents/skills/harness-profile-adapter/references/runtime-detection.md` — detecting active harness vs. installed binaries
- `/.agents/skills/harness-profile-adapter/references/tooling-context-policy.md` — what goes under okf/wiki/tooling/ and link policy enforcement
- `/.agents/skills/harness-profile-adapter/scripts/inspect_runtime_context.py` — runtime context inspection helpers
- `/.agents/skills/harness-profile-adapter/references/harness-docs.md` — harness-documentation checklist, including instruction-file and skills-directory discovery
- `/.agents/skills/harness-profile-adapter/scripts/ensure_local_alias.py` — file and directory alias creation, symlink/junction fallback mechanism
- `/tests/test_harness_profile_adapter.py` — regression coverage for the alias helper, including the junction fallback and its safe removal
- `/AGENTS.md` — canonical orientation (where adapters point)
