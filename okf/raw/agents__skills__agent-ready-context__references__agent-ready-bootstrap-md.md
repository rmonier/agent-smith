---
type: "source-file"
title: ".agents/skills/agent-ready-context/references/agent-ready-bootstrap.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/agent-ready-context/references/agent-ready-bootstrap.md"
source_path: ".agents/skills/agent-ready-context/references/agent-ready-bootstrap.md"
source_kind: "markdown"
source_hash: "sha256:e72e7fe88b9ecd1f25db70a2f59afc8396088954f0dbc8a478d5554863a6a87b"
source_commit: "72dec433d9f5de7b377e5a547714b44e917b1925"
tags: [source-file, markdown]
---

# .agents/skills/agent-ready-context/references/agent-ready-bootstrap.md

~~~
# Agent-ready bootstrap

Use this reference when converting a new or existing repository into an agent-ready repository.

## Target structure

```text
repo/
├── AGENTS.md
├── .gitignore          # covers pipeline build artifacts
├── okf/                # OpenKB KB root
│   └── wiki/           # compiled OKF wiki
├── graphify-out/
└── .agents/
    └── skills/
        ├── agent-ready-context/
        └── skill-creator/
```

## Responsibility split

- `AGENTS.md` is a routing and rules file. It should tell agents where the durable context lives and which commands to run.
- `okf/wiki/` is the durable knowledge source of truth for agents.
- `graphify-out/` is a structural exploration aid, not final authority.
- `.agents/skills/` contains reusable actions.

Do not place large repo documentation, long architectural explanations, or copied external documentation in `AGENTS.md`. Put durable context in `okf/wiki/`.

## Tooling bootstrap (consent-first)

Confirm prerequisites first, and install missing tools only after the user agrees. Package provenance and pinning rules live in `references/dependencies.md`.

```bash
uv run .agents/skills/agent-ready-context/scripts/check_prereqs.py --repo .

# After user consent only:
uv tool install 'graphifyy==<pinned-version>'        # `graphify` CLI — https://github.com/safishamsi/graphify
uv tool install 'openkb==<pinned-version>'           # `openkb` CLI — https://github.com/VectifyAI/OpenKB
```

## Suggested command sequence

```bash
uv run .agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py --repo .

graphify update . --force || true

uv run .agents/skills/agent-ready-context/scripts/build_okf_source_pack.py --repo . --out okf/.okf-build/input

# Add external docs as evidence Markdown under okf/.okf-build/input/external/ before semantic generation.

mkdir -p okf
cd okf
openkb init --model <litellm-model> --language <lang>
cd ..

openkb --kb-dir ./okf add ./okf/.okf-build/input/
openkb --kb-dir ./okf lint
uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki
uv run .agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py --repo .
```

If no LLM provider is configured, use the conservative fallback:

```bash
uv run .agents/skills/agent-ready-context/scripts/build_okf_skeleton.py --repo . --input okf/.okf-build/input --out okf/wiki
uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki
```

## Commit guidance

Ensure `.gitignore` contains at least:

```gitignore
# agent-ready pipeline build artifacts
okf/.okf-build/
okf/output/
okf/wiki/reports/
graphify-out/cost.json
graphify-out/cache/
__pycache__/

# local provider credentials
.env
okf/.env
```

Usually commit:

- `AGENTS.md`
- `.agents/skills/agent-ready-context/`
- `.agents/skills/skill-creator/`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/graph.json`
- `okf/raw/`
- `okf/wiki/`
- `okf/.openkb/config.yaml`
- `okf/.openkb/hashes.json`

Usually do not commit:

- `okf/.okf-build/`
- `okf/output/`
- `okf/wiki/reports/`
- provider secrets
- cost/cache files containing local environment details, such as `graphify-out/cost.json`

## Skill lifecycle after OKF generation

Treat the first OKF generation as context discovery, not only documentation generation. After `okf/` exists, inspect it for repeated actions that are better represented as skills.

Use this split:

- **Keep in OKF wiki**: architecture facts, external documentation evidence, design decisions, runbook context, why a workflow exists, and source provenance.
- **Move to or create a skill**: repeated commands, multi-step procedures, validation workflows, transformations, migrations, scaffolding, or any task the agent/harness should execute in the same way again.
- **Keep in AGENTS.md**: short routing rules, the operational basics the AGENTS.md spec expects in-file (primary language and toolchain versions, setup/build/launch commands, the test invocation), and pointers to `okf/wiki/`, `graphify-out/`, and `.agents/skills/`. Point to `okf/wiki/index.md` as the front door — never deep-link individual wiki pages from here.

Vendor skills are read-only project dependencies. Install/update them with the chosen skill manager, for example `skills.sh` or `npx skill`, and preserve the generated lock file such as `skill-lock.json` when that manager creates one. Do not edit vendor skill contents directly. If behavior must change, create a custom wrapper or companion skill in `.agents/skills/` and document the relationship in `AGENTS.md`.

Custom skills are project-owned action procedures. Create or update them with `.agents/skills/skill-creator/` when OKF or recurring agent work reveals repeated executable behavior.
~~~
