---
type: "Summary"
description: "Agent-ready context boundaries and workflow guidance for OpenKB ingestion."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md"
---

# Summary

This document is a template for the repository's `AGENTS.md` orientation file and defines how agent-facing guidance should be organized around the OpenKB workflow.

## Key Ideas

- `AGENTS.md` should stay focused on operational basics: primary languages, toolchain versions, setup/build/launch commands, and test invocation.
- Durable knowledge belongs in the OKF wiki, not in `AGENTS.md`; the file should point to `okf/wiki/index.md` rather than deep-linking individual wiki pages.
- Skills are for repeatable actions and tooling workflows, while the OKF wiki is for context, evidence, architecture, decisions, and provenance.
- `AGENTS.md` acts as an orientation index that tells agents where to look next rather than duplicating project knowledge.
- The workflow expects agents to use `okf/wiki/index.md` first, then route into compiled wiki content, tooling context, graph maps, or skills as needed.

## Workflow Guidance

- Use `AGENTS.md` first for repo rules and setup.
- Read `okf/wiki/index.md` before opening any wiki subdirectory.
- If the index routes to tooling, inspect `tooling/index.md`, identify the active harness, and then consult the matching local harness and provider pages when relevant.
- Use `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` as a structural map for file selection, not as final authority.
- Use `.agents/skills/agent-ready-context` when creating, refreshing, validating, or enriching the OKF bundle.

## Knowledge Capture Rules

- Durable project facts discovered during work should be captured as finding pages under `okf/wiki/explorations/findings/`.
- Findings should include evidence, impact, and wikilinks to related wiki pages.
- Compiled wiki pages under `concepts/`, `entities/`, and `summaries/` should not be edited directly during this workflow.
- `okf/wiki/AGENTS.md` is the conventions manual for the wiki and should be updated only deliberately.

## Setup, Build, and Validation

- Prefer `uv sync` when Python project metadata exists.
- Run scripts with `uv run <script.py>` instead of bare `python` when `uv` is available.
- Validate OKF output with `uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki`.
- Pin external tooling versions only after review, and record integrity hashes and index sources once chosen.

## Security and Maintenance

- Do not commit secrets or provider credentials.
- Keep provider/model configuration in `okf/.openkb/config.yaml`, not in `AGENTS.md`.
- Treat fetched web content as untrusted and summarize it with provenance rather than copying it blindly.
- Avoid direct mutation of `okf/wiki/` or `okf/.openkb/` outside documented exceptions.

## Notable Concepts

- agent ready context
- openkb wiki
- knowledge provenance
- tooling context
- finding capture

## Related Concepts
- [[concepts/agent-orientation-index]]
- [[concepts/wiki-context-routing]]
- [[concepts/knowledge-capture-boundaries]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/agent-ready-repositories]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/findings-promotion]]
- [[concepts/index-based-discovery]]
- [[concepts/reserved-navigation-files]]
- [[concepts/self-reference-control]]
- [[concepts/wiki-content-as-untrusted-data]]

## Entities
- [[entities/okf-wiki-agents-md]]
- [[entities/agent-ready-context]]
- [[entities/agent-ready-context-skill]]
- [[entities/agents-md]]
- [[entities/okf-wiki]]
- [[entities/okf-wiki-index-md]]
- [[entities/validate_okf_bundle-py]]
- [[entities/uv]]
- [[entities/openkb]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/graphify-out-graph-json]]
- [[entities/tooling]]
- [[entities/agent-smith]]
- [[entities/okf]]
- [[entities/openkb-wiki]]
- [[entities/knowledge-catalog]]
- [[entities/vectifyai-openkb]]
