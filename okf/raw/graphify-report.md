---
type: "graph-report"
title: "Graphify Report"
description: "Graphify structural report used as an exploration map."
resource: "graphify-out/GRAPH_REPORT.md"
source_path: "graphify-out/GRAPH_REPORT.md"
source_kind: "markdown"
source_hash: "sha256:ecd83769b073995108e2c17bb99c8b5d6946ef432df1738c66db158fc3acc029"
source_commit: "98fd2cf48c75182df1733e7082c80a9f67d726e6"
tags: [graphify, repo-analysis]
---

# Graph Report - agent-smith

## Corpus Check
- 63 files · ~79,281 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 472 nodes · 550 edges · 54 communities (45 shown, 9 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1bd19302`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- README.md
- build_okf_source_pack.py
- validate_okf_bundle.py
- OKF quality and offline conformance baseline
- AGENTS.md
- Dependencies and tool boundaries
- AGENTS.md
- OpenKB lifecycle for OKF maintenance
- OpenKB repo build workflow
- Skill Creator
- Agent-ready bootstrap
- Tooling context policy
- check
- Skill dependency rules
- Subagent Profile Adapter
- External documentation evidence
- OpenKB provider configuration by harness
- build_okf_skeleton.py
- Action vs context boundaries
- Runtime detection
- Example Action Skill
- Vendor and custom skill management
- Example profile intents
- Git tracking policy
- Profile adapter authoring
- main
- inspect_runtime_context.py
- Optional official OKF spec web refresh
- Source attribution and adaptation notes
- Harness documentation handling
- validate_tooling_link_policy.py
- merge_agents_md_okf_section.py
- Testing skills with pressure scenarios
- init_skill.py
- quick_validate.py
- suggest_skills_from_okf.py
- editorial_pass.py
- Licensing
- Third-party notices
- What You Must Do When Invoked
- LICENSING.md
- LICENSING.md
- OpenKB Wiki Schema
- graphify reference: extra exports and benchmark
- OpenKB knowledge base
- OpenKB CLI reference
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native AGENTS.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- extraction-spec.md

## God Nodes (most connected - your core abstractions)
1. `main()` - 17 edges
2. `detect_orphans()` - 13 edges
3. `OKF quality and offline conformance baseline` - 12 edges
4. `What You Must Do When Invoked` - 12 edges
5. `names_from_git()` - 11 edges
6. `OpenKB lifecycle for OKF maintenance` - 11 edges
7. `OpenKB repo build workflow` - 11 edges
8. `/graphify` - 10 edges
9. `OpenKB Wiki Schema` - 10 edges
10. `main()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `bundle_key()`  [INFERRED]
  .agents/skills/agent-ready-context/scripts/build_okf_source_pack.py → .agents/skills/agent-ready-context/scripts/prune_okf_orphans.py

## Import Cycles
- None detected.

## Communities (54 total, 9 thin omitted)

### Community 0 - "README.md"
Cohesion: 0.04
Nodes (41): Backend connection modes, Choosing a provider for the active harness, Credential resolution order, Dependency-schema failures are not provider verdicts, Example config, OpenKB provider configuration by harness, Verification, Air-gapped recipe (+33 more)

### Community 1 - "build_okf_source_pack.py"
Cohesion: 0.16
Nodes (21): frontmatter(), json_string(), last_touch_commits(), main(), normalize_text(), Path, Deterministic split of an oversized source into full-content parts.      Croppin, Drop run-dependent lines so unchanged reports stage to identical hashes.      Gr (+13 more)

### Community 2 - "validate_okf_bundle.py"
Cohesion: 0.23
Nodes (16): has_unclosed_fence(), load_yaml(), main(), normalized_slug(), Any, Path, All valid wikilink targets, mirroring openkb lint._all_wiki_pages keys.      Eve, Collapse a file stem for near-duplicate comparison (case, `_` vs `-`). (+8 more)

### Community 3 - "OKF quality and offline conformance baseline"
Cohesion: 0.15
Nodes (12): Bundle structure, Concept documents, Core model, Hard conformance rules, Index files, Links and citations, Local validation command, Log files (+4 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.18
Nodes (9): Agent context map, Agent-ready knowledge workflow, Build and test commands, Code style, Knowledge-base workflow, Project overview, Security considerations, Setup commands (+1 more)

### Community 5 - "Dependencies and tool boundaries"
Cohesion: 0.18
Nodes (10): Bootstrap procedure (consent-first), Companion skills, Dependencies and tool boundaries, Harness tools vs local CLIs, Integrity pinning and update policy (supply-chain), Permissions and security, Provenance and pinning, Registry-agnostic installs (+2 more)

### Community 6 - "AGENTS.md"
Cohesion: 0.20
Nodes (9): Agent context map, AGENTS.md, Build and test commands, Code style, Knowledge-base workflow, Project overview, Security considerations, Setup commands (+1 more)

### Community 7 - "OpenKB lifecycle for OKF maintenance"
Cohesion: 0.17
Nodes (11): Citations and provenance chain, Command selection by goal, Correction loop: improve the input signal, never the output, Dedupe before ingest, Findings: the memory-brain loop (capture in-wiki, consolidate by ingestion), No-hand-edit rule, `okf/wiki/AGENTS.md` conventions management, OpenKB lifecycle for OKF maintenance (+3 more)

### Community 8 - "OpenKB repo build workflow"
Cohesion: 0.17
Nodes (11): AGENTS.md re-pass (after validation), Continuous validation (optional, zero-LLM), Decision tree, Incremental update, Inputs, Local-artifact leakage risk: graphify has no local-ignore tier, OpenKB repo build workflow, Post-generation review pass (+3 more)

### Community 9 - "Skill Creator"
Cohesion: 0.14
Nodes (29): bundle_key(), detect_orphans(), _git_blob_bytes(), git_blob_content_hash(), git_tracked(), is_pipeline_owned(), load_registry(), main() (+21 more)

### Community 10 - "Agent-ready bootstrap"
Cohesion: 0.25
Nodes (7): Agent-ready bootstrap, Commit guidance, Responsibility split, Skill lifecycle after OKF generation, Suggested command sequence, Target structure, Tooling bootstrap (consent-first)

### Community 11 - "Tooling context policy"
Cohesion: 0.22
Nodes (8): Default artifact rule, Git scope: local by default, Link direction, Location, Required root index entry, Required semantics, Tooling context policy, Validation

### Community 12 - "check"
Cohesion: 0.38
Nodes (10): check(), check_openkb_config(), ensure_writable(), main(), Any, Path, Top-level ``key: value`` scalars without a YAML dependency.      Good enough for, Config-surface and credential-home checks (existence and non-secret     config o (+2 more)

### Community 13 - "Skill dependency rules"
Cohesion: 0.29
Nodes (6): Skill dependency rules, Skill-to-skill relationships, Standard metadata key vocabulary, Third-party tool requirements, Vendor skills, When creating a skill

### Community 14 - "Subagent Profile Adapter"
Cohesion: 0.20
Nodes (9): Agent-Ready Context, Build artifact hygiene, Commands, OKF conformance authority, References, Script execution convention, Security baseline, Tooling bootstrap (+1 more)

### Community 15 - "External documentation evidence"
Cohesion: 0.33
Nodes (5): Evidence file template, Example use, External documentation evidence, Rules, Security rules for fetched content

### Community 16 - "OpenKB provider configuration by harness"
Cohesion: 0.29
Nodes (6): Boundary rules, Core workflow, Non-goals, Runtime detection rule, Subagent Profile Adapter, Tooling context in OKF

### Community 17 - "build_okf_skeleton.py"
Cohesion: 0.53
Nodes (4): frontmatter(), main(), Path, run_git()

### Community 18 - "Action vs context boundaries"
Cohesion: 0.33
Nodes (5): Action vs context boundaries, Put it in a skill when it is an action, Put it in AGENTS.md when it is orientation, Put it in OKF wiki when it is context, Vendor skill rule

### Community 19 - "Runtime detection"
Cohesion: 0.33
Nodes (5): Ambiguity handling, Inspection helper, Non-signals, Reliable signals, Runtime detection

### Community 20 - "Example Action Skill"
Cohesion: 0.40
Nodes (4): Commands, Edge cases, Example Action Skill, Workflow

### Community 21 - "Vendor and custom skill management"
Cohesion: 0.40
Nodes (4): Custom skills, Vendor and custom skill management, Vendor skills, Vendor skills vs adopted generated skills

### Community 22 - "Example profile intents"
Cohesion: 0.40
Nodes (4): Example profile intents, okf-curator, repo-cartographer, skill-architect

### Community 23 - "Git tracking policy"
Cohesion: 0.33
Nodes (5): Alternatives, Default policy, Git tracking policy, Instruction file aliases, Tooling context pages

### Community 24 - "Profile adapter authoring"
Cohesion: 0.40
Nodes (4): Anti-bloat rules, Minimal profile intent, Profile adapter authoring, Recommended candidate profiles

### Community 25 - "main"
Cohesion: 0.80
Nodes (4): append_exclude(), main(), Path, write_pointer()

### Community 26 - "inspect_runtime_context.py"
Cohesion: 0.70
Nodes (4): main(), parent_chain(), read_proc(), score_candidates()

### Community 27 - "Optional official OKF spec web refresh"
Cohesion: 0.50
Nodes (3): Embedded baseline remains authoritative offline, Optional official OKF spec web refresh, Refresh procedure

### Community 28 - "Source attribution and adaptation notes"
Cohesion: 0.22
Nodes (7): Licensing, Adaptation rules, Source attribution and adaptation notes, What this adaptation adds, Adapted passages in SKILL.md, Provenance rule, Third-party notices

### Community 29 - "Harness documentation handling"
Cohesion: 0.50
Nodes (3): Harness documentation handling, OKF record, Source priority

### Community 30 - "validate_tooling_link_policy.py"
Cohesion: 0.36
Nodes (8): is_tooling_link(), main(), parse_frontmatter(), Path, Remove code spans/blocks while preserving line numbers for diagnostics., Return True for project concept pages and navigation indexes only.      Entity p, should_scan_for_project_to_tooling_links(), strip_code_preserve_lines()

### Community 37 - "editorial_pass.py"
Cohesion: 0.21
Nodes (20): base_kb_page_texts(), cmd_brief(), cmd_check(), diff_entries(), fail_env(), _format_targets_mirrored(), main(), openkb_python() (+12 more)

### Community 38 - "Licensing"
Cohesion: 0.29
Nodes (7): Complete licence texts, Generated content, Generated reports about this repository, Licensing, Original material, The `okf/` knowledge base: unlicensed, not hidden, Third-party and vendored material

### Community 39 - "Third-party notices"
Cohesion: 0.29
Nodes (7): agent-ready-context: OpenKB-derived compatibility fallback, Graphify-generated output (graphify-out/), Graphify vendored skill, Important provenance rule, OpenKB vendored skill, skill-creator: adapted passages, Third-party notices

### Community 40 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native AGENTS.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 41 - "LICENSING.md"
Cohesion: 0.40
Nodes (3): Licensing, OpenKB-derived compatibility fallback, Third-party notices

### Community 103 - "OpenKB Wiki Schema"
Cohesion: 0.18
Nodes (10): Directory layout, OpenKB Wiki Schema, Short vs long classification, `wiki/concepts/<slug>.md`, `wiki/entities/<slug>.md`, `wiki/index.md`, `wiki/sources/<doc>.json` (long PDFs), `wiki/sources/<doc>.md` (short docs) (+2 more)

### Community 140 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 141 - "OpenKB knowledge base"
Cohesion: 0.22
Nodes (8): First: find where the KB lives, Frontmatter, MUST NOT modify the KB or environment autonomously, OpenKB knowledge base, Read content, See what's available, Trust boundary, When the KB doesn't have the answer

### Community 200 - "OpenKB CLI reference"
Cohesion: 0.29
Nodes (6): OpenKB CLI reference, `openkb list`, `openkb query "<question>"`, `openkb status`, Read-only commands the skill should NOT call, Write commands — MUST NOT run autonomously

### Community 224 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 281 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 282 - "graphify reference: commit hook and native AGENTS.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native AGENTS.md integration, graphify reference: commit hook and native AGENTS.md integration

### Community 283 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **234 isolated node(s):** `Licensing`, `Script execution convention`, `Workflow`, `Tooling bootstrap`, `Build artifact hygiene` (+229 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `build_okf_source_pack.py` to `Skill Creator`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `bundle_key()` connect `Skill Creator` to `build_okf_source_pack.py`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **What connects `Map each path to the newest commit that touched it.      Staged frontmatter must`, `Deterministic split of an oversized source into full-content parts.      Croppin`, `Drop run-dependent lines so unchanged reports stage to identical hashes.      Gr` to the rest of the system?**
  _260 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `README.md` be split into smaller, more focused modules?**
  _Cohesion score 0.043478260869565216 - nodes in this community are weakly interconnected._
- **Should `Skill Creator` be split into smaller, more focused modules?**
  _Cohesion score 0.1425287356321839 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
