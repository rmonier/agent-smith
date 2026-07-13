---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__transcribe-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__exports-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/graphify-report.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md"]
description: "Documentation organized around concrete steps, commands, and operational outcomes."
---

# Action-Oriented Documentation

Action-oriented documentation is documentation written to help someone do something concrete: run a command, validate a system, generate an artifact, update a workflow, ingest new material, export data, start a service, or carry out another operational task. It emphasizes executable steps, tool usage, branching behavior, and outcome-focused instructions over abstract explanation alone.

This concept appears clearly in [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]], which treats action-heavy pages as stronger candidates for reusable skills. It also appears in [[summaries/agents__skills__graphify__references__add-watch-md]], where the document is structured around operational triggers for adding a source and starting a watcher, and in [[summaries/agents__skills__graphify__references__exports-md]], where each procedure is gated by a specific export flag and tied to a concrete artifact or runtime behavior.

## Core idea

Action-oriented documentation makes procedural intent explicit. Common signals include:

- imperative verbs such as run, validate, build, export, import, sync, update, ingest, push, serve, or watch
- references to concrete tools such as git, docker, python, uv, or [[entities/graphify]]
- command examples, code fences, and stepwise instructions
- descriptions tied to outputs, checks, flags, endpoints, or operational results
- error paths or branching behavior that tell the operator what to do when execution fails or prerequisites are missing
- ordering constraints such as which step must run before cleanup or which action should be skipped unless a threshold is met

This style of documentation is especially useful when a repository is being mined for automation opportunities, because it exposes repeatable tasks that can be converted into scripts, checks, or skills. That makes it closely related to [[concepts/skill-based-automation]] and [[concepts/executable-validation]].

## Contrast with descriptive documentation

Action-oriented documentation differs from conceptual or explanatory material. A page about architecture, decisions, or an overview may be useful context, but it does not necessarily tell an agent or operator what to execute next. The source script reflects this distinction by skipping pages with terms like architecture, decision, evidence, overview, or concept unless they also contain code fences. This creates a practical boundary between explanation and action, aligning with [[concepts/context-action-separation]] and [[concepts/progressive-disclosure]].

The graphify references sharpen this contrast. They do not mainly explain what a graph is or why ingestion and export exist. Instead, they specify when to load a reference, which command to run, which flags activate which steps, which defaults apply, how to react to errors or missing credentials, and what follow-on behavior is required. That is a strong example of documentation whose value lies in execution rather than background description.

## How the source document operationalizes the concept

In [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]], action-oriented documentation is not just described; it is used as a heuristic input for automation discovery.

### Signals used

The script scans Markdown pages in an OKF bundle and scores them using regex patterns that match:

- execution verbs like run, execute, launch, invoke, and watch
- validation verbs like validate, verify, check, test, and lint
- generation verbs like generate, scaffold, build, compile, export, import, convert, and transform
- maintenance verbs like refresh, update, sync, reconcile, rotate, migrate, and ingest
- tool names like terraform, kubectl, helm, docker, git, uv, python, and graphify

These signals operationalize [[concepts/heuristic-classification]]: the script assumes that when documentation repeatedly uses action verbs and tool references, it is more likely to encode reusable operational knowledge.

The graphify add/watch and export references are strong fits for these signals. They include explicit command invocations, parameter substitution rules, expected output behavior, conditional branches for different flags, and differentiated system responses depending on whether the user is adding a remote source, monitoring a folder for changes, generating an artifact, pushing to a graph database, or starting an MCP server.

### Filtering behavior

The script avoids raw source pages, reports, and reserved files, and it also downranks purely descriptive materials by skipping certain contextual pages unless they contain fenced code blocks. This shows that action-oriented documentation is not merely about wording; it is strengthened by executable examples and concrete evidence. That behavior connects to [[concepts/reserved-wiki-files]], [[concepts/repository-ingestion]], and [[concepts/documentation-architecture]].

The graphify references reinforce this point because their procedural value comes from executable examples plus operational constraints. The add/watch page distinguishes error cases that must be surfaced to the user and explains when automatic graph rebuilding is sufficient versus when a manual semantic update is still needed. The exports page adds another pattern: step-gated execution based on flags, explicit defaults for systems like [[entities/neo4j]] and [[entities/falkordb]], ordering requirements for wiki export, and threshold-based execution for benchmarking. Together, they show that action-oriented documentation often includes not just commands, but decisions about when a command should or should not run.

### Output effect

When a page looks sufficiently action-oriented, the script proposes a skill name, keeps evidence paths, and prints a bootstrap command for creating the skill. In practice, this means action-oriented documentation serves as a bridge between curated knowledge and automation-ready assets. The concept therefore also supports [[concepts/project-scaffolding]] and [[concepts/generated-content-governance]].

The graphify references show why this matters. Compact operational pages can encode reusable workflows for web evidence ingestion, graph refresh, export to external systems, visualization generation, and live graph serving through [[concepts/mcp-server-integration]]. That makes them the kind of pages an automation system can turn into repeatable command surfaces rather than leaving them as passive documentation.

## Why it matters

Action-oriented documentation is valuable because it:

- makes operational knowledge easier to execute consistently
- reveals repeated tasks that are good candidates for automation
- helps separate procedural instructions from background context
- improves discoverability for validation, build, ingestion, export, and maintenance workflows
- supports turning repository knowledge into reusable agent skills
- captures branching execution logic such as success paths, failure handling, credential prompting, thresholds, and follow-up actions

In knowledge systems like [[entities/openkb]], this kind of documentation is especially useful because it can be reused by both humans and tools. It helps preserve not just what a system is, but how to operate it safely and repeatably.

## Practical indicators

A document is more likely to be action-oriented when it includes:

- commands or code blocks
- explicit prerequisites, defaults, and expected outputs
- steps tied to validation, ingestion, monitoring, export, benchmarking, or state changes
- references to tools or scripts by name
- language that can be mapped directly to an operational workflow
- branching instructions such as what to do on error, when to ask for credentials, what happens after success, or when a step should be skipped
- execution guards based on flags, file availability, or measured thresholds

A document is less action-oriented when it stays at the level of rationale, overview, or conceptual framing without giving a concrete next action.

## Related concepts

- [[concepts/context-action-separation]]
- [[concepts/executable-validation]]
- [[concepts/heuristic-classification]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/mcp-server-integration]]
- [[concepts/project-scaffolding]]
- [[concepts/progressive-disclosure]]
- [[concepts/repository-ingestion]]
- [[concepts/skill-based-automation]]
- [[concepts/web-evidence-ingestion]]

## Source connection

The main source for this concept here is [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]], which demonstrates how action-oriented documentation can be detected heuristically and used to suggest new reusable skills.

Additional strong sources are [[summaries/agents__skills__graphify__references__add-watch-md]], which shows the concept in operational form through URL ingestion and folder watching workflows, and [[summaries/agents__skills__graphify__references__exports-md]], which shows the same concept through flag-scoped export procedures, graph database push flows, MCP server startup, and threshold-triggered benchmarking.

See also: [[summaries/agents__skills__skill-creator__SKILL-md]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__graphify__references__github-and-merge-md]]

See also: [[summaries/agents__skills__graphify__references__hooks-md]]

See also: [[summaries/agents__skills__graphify__references__query-md]]

See also: [[summaries/agents__skills__graphify__references__transcribe-md]]

See also: [[summaries/agents__skills__graphify__references__update-md]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]

See also: [[summaries/agents__skills__openkb__references__commands-md]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/README-md]]

See also: [[summaries/karpathy-llm-wiki-gist]]