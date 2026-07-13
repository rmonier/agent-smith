---
type: "Summary"
description: "Script merges managed OKF guidance into AGENTS.md without overwriting local content."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"
---

# .agents/skills/agent-ready-context/scripts/merge_agents_md_okf_section.py

This script updates an `AGENTS.md` file by inserting or replacing a managed OKF guidance block wrapped in `<!-- okf:start -->` and `<!-- okf:end -->` comments. It is intentionally conservative: it preserves existing repository-specific guidance and only manages the designated section.

## Purpose

The script standardizes the orientation content that points agents toward the right sources of truth:

- `AGENTS.md` for repository rules, setup, tests, and local best practices
- `okf/wiki/index.md` as the front door to the compiled OKF wiki
- `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as a structural repo map
- `.agents/skills/` as the home for reusable skills

It also explains how to treat wiki content as data, not instructions, and how to handle tooling context, especially when local tooling overlays may be empty on a fresh clone.

## Key Ideas

- [[concepts/agent-ready-context]]: the workflow for keeping repository orientation and OKF context aligned
- knowledge routing: using indexes and structured pointers to reach the right source of truth
- tooling context: separating local harness knowledge from compiled project knowledge
- openkb wiki: the compiled wiki as durable context, not executable instructions
- repository maintenance: refreshing guidance when repository facts or workflows change

## Behavior

The merge logic has three modes:

- If both markers exist, it replaces only the content between them
- If the file already has content, it appends the managed section to the end
- If the file is missing or empty, it creates a new `AGENTS.md` with a title and the managed section

The script uses `pathlib.Path` for file handling, reads and writes UTF-8 text, and prints the resulting path after updating the file.

## Operational Guidance Encoded in the Section

The managed section includes several workflow rules that are important for agents:

- Prefer `uv run <script.py>` over bare `python` when `uv` is available
- Read `okf/wiki/index.md` first for wiki discovery and follow its routing
- Inspect `tooling/index.md` and local harness metadata when the index routes to tooling
- Avoid editing OpenKB-managed compiled pages directly
- Capture durable project facts as findings under `okf/wiki/explorations/findings/`
- Rerun the `agent-ready-context` skill when source files, CI/CD, security, architecture, or repeated actions change

## Notable Constraints

The file explicitly preserves a boundary between:

- repository orientation in `AGENTS.md`
- executable workflow in `.agents/skills/agent-ready-context/SKILL.md`
- compiled OKF wiki pages in `okf/wiki/`
- local provider and harness configuration in `okf/.openkb/`

It also warns against destructive changes, hidden provenance, and broad regeneration without consent.

## Implementation Notes

- `START` and `END` mark the managed block boundaries
- `SECTION` contains the full OKF guidance text to insert
- `merge()` handles replacement, append, or initialization
- `main()` exposes a small CLI with `--repo` and `--file` arguments

## Why It Matters

This script is the mechanical entry point for keeping agent orientation consistent across repository refreshes. It helps ensure that the human-maintained `AGENTS.md` stays concise while still directing agents toward the right context, the right skills, and the right maintenance workflow.

## Related Concepts
- [[concepts/managed-document-sections]]
- [[concepts/conservative-document-merging]]
- [[concepts/agents-md-maintenance]]
- [[concepts/knowledge-base-navigation]]
- [[concepts/documentation-layer-separation]]
- [[concepts/documentation-architecture]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-boundaries]]
- [[concepts/okf-workflow-governance]]
- [[concepts/skill-based-automation]]
- [[concepts/agent-orientation-index]]
- [[concepts/context-action-separation]]
- [[concepts/index-based-discovery]]
- [[concepts/local-tooling-boundaries]]
- [[concepts/tooling-context-governance]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/wiki-context-routing]]

## Entities
- [[entities/merge_agents_md_okf_section-py]]
- [[entities/okf-wiki-index-md]]
- [[entities/okf-wiki-agents-md]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/graphify-out-graph-json]]
- [[entities/agent-ready-context-skill]]
- [[entities/skill-creator]]
- [[entities/uv]]
- [[entities/agents-md]]
- [[entities/okf-wiki]]
- [[entities/openkb-wiki]]
- [[entities/openkb]]
- [[entities/okf]]
- [[entities/tooling]]
- [[entities/agent-ready-context]]
- [[entities/agents-skills]]
- [[entities/openkb-cli]]
- [[entities/python]]
- [[entities/graphify]]
- [[entities/openkb-wiki]]
