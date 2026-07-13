# Graph Report - agent-smith  (2026-07-13)

## Corpus Check
- 66 files · ~81,521 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 508 nodes · 593 edges · 65 communities (57 shown, 8 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

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
- adopt_generated_skill.py
- editorial_pass.py
- Licensing
- Third-party notices
- What You Must Do When Invoked
- LICENSING.md
- LICENSING.md
- OpenKB provider configuration by harness
- Privacy, data flows, and air-gapped operation
- Code of Conduct
- Contributing
- openkb_python
- Security Policy
- Usage
- Contribute
- About The Project
- Getting Started
- preserve_lint_reports.py
- graphify reference: transcribe video and audio
- Testing skills with pressure scenarios
- init_skill.py
- quick_validate.py
- suggest_skills_from_okf.py
- Contribute
- About The Project
- extraction-spec.md
- LICENSING.md

## God Nodes (most connected - your core abstractions)
1. `main()` - 17 edges
2. `detect_orphans()` - 13 edges
3. `OKF quality and offline conformance baseline` - 12 edges
4. `OpenKB repo build workflow` - 12 edges
5. `What You Must Do When Invoked` - 12 edges
6. `names_from_git()` - 11 edges
7. `OpenKB lifecycle for OKF maintenance` - 11 edges
8. `/graphify` - 10 edges
9. `OpenKB Wiki Schema` - 10 edges
10. `main()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `bundle_key()`  [INFERRED]
  .agents/skills/agent-ready-context/scripts/build_okf_source_pack.py → .agents/skills/agent-ready-context/scripts/prune_okf_orphans.py

## Import Cycles
- None detected.

## Communities (65 total, 8 thin omitted)

### Community 0 - "README.md"
Cohesion: 0.14
Nodes (29): bundle_key(), detect_orphans(), _git_blob_bytes(), git_blob_content_hash(), git_tracked(), is_pipeline_owned(), load_registry(), main() (+21 more)

### Community 1 - "build_okf_source_pack.py"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native AGENTS.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 2 - "validate_okf_bundle.py"
Cohesion: 0.16
Nodes (21): frontmatter(), json_string(), last_touch_commits(), main(), normalize_text(), Path, Deterministic split of an oversized source into full-content parts.      Croppin, Drop run-dependent lines so unchanged reports stage to identical hashes.      Gr (+13 more)

### Community 3 - "OKF quality and offline conformance baseline"
Cohesion: 0.21
Nodes (20): base_kb_page_texts(), cmd_brief(), cmd_check(), diff_entries(), fail_env(), _format_targets_mirrored(), main(), openkb_python() (+12 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.10
Nodes (18): Complete licence texts, Generated content, Generated reports about this repository, Licensing, Original material, The `okf/` knowledge base: unlicensed, not hidden, Third-party and vendored material, agent-ready-context: OpenKB-derived compatibility fallback (+10 more)

### Community 5 - "Dependencies and tool boundaries"
Cohesion: 0.23
Nodes (16): has_unclosed_fence(), load_yaml(), main(), normalized_slug(), Any, Path, All valid wikilink targets, mirroring openkb lint._all_wiki_pages keys.      Eve, Collapse a file stem for near-duplicate comparison (case, `_` vs `-`). (+8 more)

### Community 6 - "AGENTS.md"
Cohesion: 0.15
Nodes (12): Bundle structure, Concept documents, Core model, Hard conformance rules, Index files, Links and citations, Local validation command, Log files (+4 more)

### Community 7 - "OpenKB lifecycle for OKF maintenance"
Cohesion: 0.15
Nodes (12): AGENTS.md re-pass (after validation), Continuous validation (optional, zero-LLM), Decision tree, Incremental update, Inputs, Local-artifact leakage risk: graphify has no local-ignore tier, Non-interactive `openkb init`, OpenKB repo build workflow (+4 more)

### Community 8 - "OpenKB repo build workflow"
Cohesion: 0.21
Nodes (7): About the Name, Contact, Credits, Licensing, References, Security and Privacy, Tree Structure

### Community 9 - "Skill Creator"
Cohesion: 0.17
Nodes (11): Citations and provenance chain, Command selection by goal, Correction loop: improve the input signal, never the output, Dedupe before ingest, Findings: the memory-brain loop (capture in-wiki, consolidate by ingestion), No-hand-edit rule, `okf/wiki/AGENTS.md` conventions management, OpenKB lifecycle for OKF maintenance (+3 more)

### Community 10 - "Agent-ready bootstrap"
Cohesion: 0.18
Nodes (9): Agent context map, Agent-ready knowledge workflow, Build and test commands, Code style, Knowledge-base workflow, Project overview, Security considerations, Setup commands (+1 more)

### Community 11 - "Tooling context policy"
Cohesion: 0.18
Nodes (10): Bootstrap procedure (consent-first), Companion skills, Dependencies and tool boundaries, Harness tools vs local CLIs, Integrity pinning and update policy (supply-chain), Permissions and security, Provenance and pinning, Registry-agnostic installs (+2 more)

### Community 12 - "check"
Cohesion: 0.38
Nodes (10): check(), check_openkb_config(), ensure_writable(), main(), Any, Path, Top-level ``key: value`` scalars without a YAML dependency.      Good enough for, Config-surface and credential-home checks (existence and non-secret     config o (+2 more)

### Community 13 - "Skill dependency rules"
Cohesion: 0.18
Nodes (10): Directory layout, OpenKB Wiki Schema, Short vs long classification, `wiki/concepts/<slug>.md`, `wiki/entities/<slug>.md`, `wiki/index.md`, `wiki/sources/<doc>.json` (long PDFs), `wiki/sources/<doc>.md` (short docs) (+2 more)

### Community 14 - "Subagent Profile Adapter"
Cohesion: 0.20
Nodes (9): Agent context map, AGENTS.md, Build and test commands, Code style, Knowledge-base workflow, Project overview, Security considerations, Setup commands (+1 more)

### Community 15 - "External documentation evidence"
Cohesion: 0.20
Nodes (9): Agent-Ready Context, Build artifact hygiene, Commands, OKF conformance authority, References, Script execution convention, Security baseline, Tooling bootstrap (+1 more)

### Community 16 - "OpenKB provider configuration by harness"
Cohesion: 0.22
Nodes (7): Licensing, Adaptation rules, Source attribution and adaptation notes, What this adaptation adds, Adapted passages in SKILL.md, Provenance rule, Third-party notices

### Community 17 - "build_okf_skeleton.py"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 18 - "Action vs context boundaries"
Cohesion: 0.22
Nodes (8): First: find where the KB lives, Frontmatter, MUST NOT modify the KB or environment autonomously, OpenKB knowledge base, Read content, See what's available, Trust boundary, When the KB doesn't have the answer

### Community 19 - "Runtime detection"
Cohesion: 0.22
Nodes (8): Boundary rules, Core principles, Creation workflow, Naming, Script execution convention, Security defaults for created skills, Skill Creator, Updating skills from OKF

### Community 20 - "Example Action Skill"
Cohesion: 0.22
Nodes (8): Default artifact rule, Git scope: local by default, Link direction, Location, Required root index entry, Required semantics, Tooling context policy, Validation

### Community 21 - "Vendor and custom skill management"
Cohesion: 0.36
Nodes (8): is_tooling_link(), main(), parse_frontmatter(), Path, Remove code spans/blocks while preserving line numbers for diagnostics., Return True for project concept pages and navigation indexes only.      Entity p, should_scan_for_project_to_tooling_links(), strip_code_preserve_lines()

### Community 22 - "Example profile intents"
Cohesion: 0.25
Nodes (7): Agent-ready bootstrap, Commit guidance, Responsibility split, Skill lifecycle after OKF generation, Suggested command sequence, Target structure, Tooling bootstrap (consent-first)

### Community 23 - "Git tracking policy"
Cohesion: 0.25
Nodes (7): Backend connection modes, Choosing a provider for the active harness, Credential resolution order, Dependency-schema failures are not provider verdicts, Example config, OpenKB provider configuration by harness, Verification

### Community 24 - "Profile adapter authoring"
Cohesion: 0.29
Nodes (6): Air-gapped recipe, Disclosure before first compile, Explicit backend rule for graphify, Privacy, data flows, and air-gapped operation, Telemetry status of the toolchain, What leaves the machine, stage by stage

### Community 25 - "main"
Cohesion: 0.29
Nodes (6): OpenKB CLI reference, `openkb list`, `openkb query "<question>"`, `openkb status`, Read-only commands the skill should NOT call, Write commands — MUST NOT run autonomously

### Community 26 - "inspect_runtime_context.py"
Cohesion: 0.29
Nodes (6): Skill dependency rules, Skill-to-skill relationships, Standard metadata key vocabulary, Third-party tool requirements, Vendor skills, When creating a skill

### Community 27 - "Optional official OKF spec web refresh"
Cohesion: 0.29
Nodes (6): Boundary rules, Core workflow, Non-goals, Runtime detection rule, Subagent Profile Adapter, Tooling context in OKF

### Community 28 - "Source attribution and adaptation notes"
Cohesion: 0.33
Nodes (5): Evidence file template, Example use, External documentation evidence, Rules, Security rules for fetched content

### Community 29 - "Harness documentation handling"
Cohesion: 0.53
Nodes (4): frontmatter(), main(), Path, run_git()

### Community 30 - "validate_tooling_link_policy.py"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 31 - "merge_agents_md_okf_section.py"
Cohesion: 0.33
Nodes (5): Action vs context boundaries, Put it in a skill when it is an action, Put it in AGENTS.md when it is orientation, Put it in OKF wiki when it is context, Vendor skill rule

### Community 32 - "Testing skills with pressure scenarios"
Cohesion: 0.33
Nodes (5): Alternatives, Default policy, Git tracking policy, Instruction file aliases, Tooling context pages

### Community 33 - "init_skill.py"
Cohesion: 0.33
Nodes (5): Ambiguity handling, Inspection helper, Non-signals, Reliable signals, Runtime detection

### Community 34 - "quick_validate.py"
Cohesion: 0.33
Nodes (6): Code of Conduct, Enforcement, Expected behavior, Our pledge, Scope, Unacceptable behavior

### Community 35 - "suggest_skills_from_okf.py"
Cohesion: 0.33
Nodes (6): Before you start, Contributing, Licensing hygiene, Making a change, Pull requests, Validating before you open a PR

### Community 36 - "adopt_generated_skill.py"
Cohesion: 0.40
Nodes (3): Licensing, OpenKB-derived compatibility fallback, Third-party notices

### Community 37 - "editorial_pass.py"
Cohesion: 0.60
Nodes (4): main(), openkb_python(), Path, Interpreter of the installed openkb uv tool venv, if any.

### Community 38 - "Licensing"
Cohesion: 0.60
Nodes (4): _is_clean_marker_state(), main(), merge(), True when markers are absent, or present exactly once each in order.

### Community 39 - "Third-party notices"
Cohesion: 0.40
Nodes (4): Commands, Edge cases, Example Action Skill, Workflow

### Community 40 - "What You Must Do When Invoked"
Cohesion: 0.40
Nodes (4): Custom skills, Vendor and custom skill management, Vendor skills, Vendor skills vs adopted generated skills

### Community 41 - "LICENSING.md"
Cohesion: 0.40
Nodes (4): Example profile intents, okf-curator, repo-cartographer, skill-architect

### Community 42 - "LICENSING.md"
Cohesion: 0.40
Nodes (4): Anti-bloat rules, Minimal profile intent, Profile adapter authoring, Recommended candidate profiles

### Community 43 - "OpenKB provider configuration by harness"
Cohesion: 0.80
Nodes (4): append_exclude(), main(), Path, write_pointer()

### Community 44 - "Privacy, data flows, and air-gapped operation"
Cohesion: 0.70
Nodes (4): main(), parent_chain(), read_proc(), score_candidates()

### Community 45 - "Code of Conduct"
Cohesion: 0.40
Nodes (5): Getting Started, Installation, Manual (no skill manager), npx skills (third-party manager), Prerequisites

### Community 46 - "Contributing"
Cohesion: 0.40
Nodes (5): Design background, Reporting a vulnerability, Response, Security Policy, What's in scope

### Community 47 - "openkb_python"
Cohesion: 0.50
Nodes (3): Embedded baseline remains authoritative offline, Optional official OKF spec web refresh, Refresh procedure

### Community 48 - "Security Policy"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 49 - "Usage"
Cohesion: 0.50
Nodes (3): For git commit hook, For native AGENTS.md integration, graphify reference: commit hook and native AGENTS.md integration

### Community 50 - "Contribute"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 51 - "About The Project"
Cohesion: 0.50
Nodes (3): Harness documentation handling, OKF record, Source priority

### Community 52 - "Getting Started"
Cohesion: 0.50
Nodes (4): Agent-ready bootstrap, Air-gapped operation, Maintenance, Usage

### Community 59 - "Contribute"
Cohesion: 0.67
Nodes (3): A. Extend an existing skill, B. Create a new skill, Contribute

### Community 60 - "About The Project"
Cohesion: 0.67
Nodes (3): About The Project, Built With, The Skills

## Knowledge Gaps
- **253 isolated node(s):** `Licensing`, `Script execution convention`, `Workflow`, `Tooling bootstrap`, `Build artifact hygiene` (+248 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Third-party notices` connect `AGENTS.md` to `OpenKB repo build workflow`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `Map each path to the newest commit that touched it.      Staged frontmatter must`, `Deterministic split of an oversized source into full-content parts.      Croppin`, `Drop run-dependent lines so unchanged reports stage to identical hashes.      Gr` to the rest of the system?**
  _281 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `README.md` be split into smaller, more focused modules?**
  _Cohesion score 0.1425287356321839 - nodes in this community are weakly interconnected._
- **Should `build_okf_source_pack.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `AGENTS.md` be split into smaller, more focused modules?**
  _Cohesion score 0.10457516339869281 - nodes in this community are weakly interconnected._