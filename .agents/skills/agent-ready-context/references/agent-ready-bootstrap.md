# Agent-ready bootstrap

Use this reference when converting a new or existing repository into an agent-ready repository.

## Target structure

```text
repo/
├── AGENTS.md
├── .gitignore          # covers pipeline build artifacts
├── okf/
│   ├── external/       # reviewed external-evidence docs (tracked, staged)
│   ├── wiki/           # OKF wiki maintained through OpenWiki
│   └── .openwiki/      # ignored local producer state and credentials
└── .agents/
    └── skills/
        ├── agent-ready-context/
        └── skill-creator/
```

## Responsibility split

- `AGENTS.md` is a routing and rules file. It should tell agents where the durable context lives and which commands to run.
- `okf/wiki/` is the durable knowledge source of truth for agents, entered through `okf/wiki/index.md`.
- `okf/external/` holds reviewed external-evidence documents that the staged runs ingest and cite.
- `.agents/skills/` contains reusable actions.

Do not place large repo documentation, long architectural explanations, or copied external documentation in `AGENTS.md`. Put durable context in `okf/wiki/`.

## Tooling bootstrap (consent-first)

Confirm prerequisites first, and install missing tools only after the user agrees. Package provenance and pinning rules live in `references/dependencies.md`.

```bash
uv run .agents/skills/agent-ready-context/scripts/check_prereqs.py --repo .

# After user consent only:
fnm install <node-version-meeting-upstream-minimum>   # producer runtime — https://github.com/Schniz/fnm
# --allow-build: without a human to answer pnpm's interactive build-script
# approval prompt, a scripted install silently skips compiling native
# dependencies (better-sqlite3, esbuild) instead of erroring - see
# references/dependencies.md.
pnpm add --global --allow-build=better-sqlite3 --allow-build=esbuild openwiki@<exact-pinned-version>  # released OKF-capable pin — https://github.com/langchain-ai/openwiki
uv tool install '<python-helper>==<pinned-version>'   # e.g. a pinned markitdown for okf/external/ evidence prep
```

## Suggested command sequence

```bash
uv run .agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py --repo .

# Preview the exact Git-tracked corpus the producer would receive; add
# --exclude for anything sensitive. Prepare external docs as reviewed
# evidence pages under okf/external/ before semantic generation.
uv run .agents/skills/agent-ready-context/scripts/run_openwiki_staged.py --repo .

# After the provider disclosure and consent (references/openwiki-providers.md):
uv run .agents/skills/agent-ready-context/scripts/run_openwiki_staged.py --repo . --run-id <id> --execute -- openwiki code --init --print "Read openwiki/INSTRUCTIONS.md first and treat it as the user-authored scope contract. Preserve it byte-for-byte. Document only the staged repository; write only under openwiki/."

# Review okf/.okf-build/<id>/review.diff and the candidate pages, then:
uv run .agents/skills/agent-ready-context/scripts/run_openwiki_staged.py --repo . --run-id <id> --promote
uv run .agents/skills/agent-ready-context/scripts/validate_openwiki_bundle.py --repo .
uv run .agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py --repo .
```

If no LLM provider is configured, use the conservative fallback:

```bash
uv run .agents/skills/agent-ready-context/scripts/build_okf_skeleton.py --repo . --dry-run
uv run .agents/skills/agent-ready-context/scripts/build_okf_skeleton.py --repo .
uv run .agents/skills/agent-ready-context/scripts/validate_openwiki_bundle.py --repo .
```

## Commit guidance

Ensure `.gitignore` contains at least:

```gitignore
# agent-ready pipeline build artifacts
okf/.okf-build/

# OpenWiki local producer and OAuth state
okf/.openwiki/

# local provider credentials
.env
__pycache__/
```

Usually commit:

- `AGENTS.md`
- `.agents/skills/agent-ready-context/`
- `.agents/skills/skill-creator/`
- `okf/wiki/` (including `index.md`, `quickstart.md`, and `INSTRUCTIONS.md`)
- `okf/external/`

Usually do not commit:

- `okf/.okf-build/`
- `okf/.openwiki/` contents (credential state, update state)
- provider secrets
- local evaluation artifacts or prompts containing private source

## Skill lifecycle after OKF generation

Treat the first OKF generation as context discovery, not only documentation generation. After `okf/` exists, inspect it for repeated actions that are better represented as skills.

Use this split:

- **Keep in OKF wiki**: architecture facts, external documentation evidence, design decisions, runbook context, why a workflow exists, and source provenance.
- **Move to or create a skill**: repeated commands, multi-step procedures, validation workflows, transformations, migrations, scaffolding, or any task the agent/harness should execute in the same way again.
- **Keep in AGENTS.md**: short routing rules, the operational basics the AGENTS.md spec expects in-file (primary language and toolchain versions, setup/build/launch commands, the test invocation), and pointers to `okf/wiki/` and `.agents/skills/`. Point to `okf/wiki/index.md` as the front door — never deep-link individual wiki pages from here.

Vendor skills are read-only project dependencies. Install/update them with the chosen skill manager, for example `skills.sh` or `npx skill`, and preserve the generated lock file such as `skill-lock.json` when that manager creates one. Do not edit vendor skill contents directly. If behavior must change, create a custom wrapper or companion skill in `.agents/skills/` and document the relationship in `AGENTS.md`.

Custom skills are project-owned action procedures. Create or update them with `.agents/skills/skill-creator/` when OKF or recurring agent work reveals repeated executable behavior.
