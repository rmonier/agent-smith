---
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/README-md.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__exports-md.md"]
type: "Product"
description: "Desktop app used as an MCP host for local Graphify graph access."
---

# Claude Desktop

Claude Desktop is a desktop application referenced here as an MCP-compatible host for Graphify's local graph-query server and as an example endpoint for exploring generated knowledge graphs through a local tool connection.

## Role in this source

In [[summaries/agents__skills__graphify__references__exports-md]], Claude Desktop appears as the example client for connecting to Graphify's MCP server mode. The document explains how to configure Claude Desktop so it can launch the server against a local `graph.json` export.

In [[summaries/agents__skills__graphify__SKILL-md]], Claude Desktop is not named directly in the main procedure, but the skill defines `--mcp` as an optional export/runtime mode and treats agent access to the graph through an MCP server as part of the broader Graphify workflow. That places Claude Desktop in the role of a practical host application for the MCP-facing side of [[entities/graphify]].

## Key facts from this document

- Claude Desktop can be configured to run the Graphify MCP server and expose graph-query tools through an MCP integration.
- Its configuration is done in `claude_desktop_config.json`.
- Claude Desktop cannot execute shell substitution such as `$(...)` in the configured command.
- Because of that limitation, the `command` field must use the absolute Python interpreter path recorded in `graphify-out/.graphify_python`.
- The Graphify graph file should also be passed as an absolute path when configuring the server arguments.
- Graphify's main skill treats `--mcp` as an explicit optional mode rather than part of the default build pipeline.
- The Graphify workflow persists interpreter and graph state in `graphify-out/`, which makes Claude Desktop integration depend on durable local artifacts rather than dynamic shell discovery.
- Claude Desktop fits the post-build exploration phase, where an already-generated graph is queried and explained through a local host rather than rebuilt for every question.

## Integration details

The referenced setup launches Graphify with a command equivalent to Python module execution for `graphify.serve`, pointing at the generated graph JSON. This makes Claude Desktop a practical endpoint for [[concepts/mcp-server-integration]] and local, agent-facing graph exploration.

The newer Graphify skill description reinforces that integration pattern by making the graph itself a persistent local asset and by distinguishing build-time work from query-time exploration. In that model, Claude Desktop serves as a host for accessing a previously built graph through MCP, aligning with [[concepts/agent-guided-graph-exploration]], [[concepts/durable-context]], and [[concepts/offline-first-workflows]].

The configuration advice also reflects broader patterns in [[concepts/tool-boundaries]], [[concepts/cross-platform-tooling]], and [[concepts/tooling-context-isolation]]: the host application has concrete execution constraints, so integration must use explicit interpreter and file paths rather than shell-dependent shortcuts.

## Related pages

- [[entities/graphify]]
- [[summaries/agents__skills__graphify__SKILL-md]]
- [[summaries/agents__skills__graphify__references__exports-md]]
- [[concepts/mcp-server-integration]]
- [[concepts/agent-guided-graph-exploration]]
- [[concepts/durable-context]]
- [[concepts/tool-boundaries]]
- [[concepts/cross-platform-tooling]]
- [[concepts/tooling-context-isolation]]
- [[concepts/offline-first-workflows]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]