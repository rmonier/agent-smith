---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md"]
description: "Finding the active OpenKB root before reading or acting on compiled knowledge."
---

# Knowledge Base Discovery

Knowledge base discovery is the process of identifying the active OpenKB root before attempting to read documents, summaries, concepts, entities, source files, or other compiled knowledge. In the OpenKB workflow described in [[summaries/agents__skills__openkb__SKILL-md]], it is a required first step rather than a convenience, and in the agent-ready-context workflow it is part of the broader preflight that keeps repository knowledge, actions, and configuration correctly separated.

## Why it matters

An agent cannot safely inspect a knowledge base until it knows which knowledge base is active. Reading files before resolving the root risks using the wrong repository, missing the intended `wiki/` tree, or acting on assumptions about local layout. This makes knowledge base discovery a foundational part of [[concepts/preflight-checks]], [[concepts/path-safety]], and [[concepts/safe-automation]].

Discovery also supports evidence-grounded work: the agent should answer from the user's actual compiled KB, not from whichever directory happens to be nearby. In that sense, discovery is a prerequisite for [[concepts/evidence-grounded-answering]] and for respecting [[concepts/knowledge-boundaries]]. In agent-ready workflows, it also keeps durable context in the wiki, actions in skills, and orientation in `AGENTS.md` from being conflated.

## OpenKB discovery behavior

The source material centers discovery on `openkb status`.

- The first output line gives the absolute path of the active knowledge base.
- Agents should capture that path before any file read under `wiki/`.
- Resolution walks upward from the current working directory looking for `.openkb/`.
- If no local match is found, OpenKB falls back to the global default set by `openkb use`.
- If no knowledge base exists, the tool reports that no knowledge base was found, and the agent should stop rather than guess.

This behavior ties discovery to [[concepts/configuration-precedence]] because OpenKB resolves the active location through an ordered lookup, and to [[concepts/filesystem-validation]] because the agent should rely on explicit tool output instead of inferred paths. It also fits [[concepts/agent-context-layering]]: the KB root is a context anchor, not a substitute for reading the repository's operational guidance.

The prerequisite script `check_prereqs.py` reinforces the same boundary conditions before the agent starts KB work. It checks that `python>=3.11`, `git`, and `uv` are available, confirms the repository is a git worktree, and probes the workspace for writability. It also detects whether OpenKB itself is installed, which makes discovery and later KB inspection available as a deliberate workflow rather than an assumption. That makes discovery part of a broader [[concepts/preflight-checks]] and [[concepts/graceful-degradation]] pattern.

## Operational pattern

A safe discovery flow looks like this:

1. Run `openkb status`.
2. Parse the absolute knowledge-base path from the first line.
3. If no knowledge base is found, report that state to the user and stop.
4. Use the resolved root for every subsequent read, including `wiki/index.md`, concept pages, entity pages, summary pages, and source files.
5. Only after discovery, use broader inspection commands such as `openkb list` or direct file reads.

This pattern reinforces [[concepts/tool-boundaries]] and [[concepts/minimal-tool-scoping]]: use the narrowest command needed to establish context before broader inspection or analysis. It also complements [[concepts/index-based-discovery]], since reading `wiki/index.md` is only meaningful after the KB root has been resolved.

In agent-ready repository workflows, discovery also sits before any effort to align `AGENTS.md` with the wiki, stage source packs, or validate an OKF bundle; those actions depend on knowing which KB is authoritative and which on-disk surfaces are local-only versus compiled context. The preflight script extends that discipline by checking vendor-tool availability, local config drift, and writable paths before any KB-sensitive operation begins.

## Relationship to other OpenKB commands

Knowledge base discovery comes before commands such as `openkb list` or `openkb query`.

- `openkb list` becomes reliable only after the active root is known.
- `wiki/index.md` is the preferred next stop for seeing what concepts, entities, summaries, and explorations exist in that KB.
- Direct reads of matching concept or entity pages are usually preferable once the root is known.
- `openkb query` is more expensive and should be reserved for cases where direct discovery through the index, targeted reads, and exact search do not surface useful matches.

That sequencing reflects [[concepts/cost-aware-tool-use]] and [[concepts/non-interactive-agent-design]]. The agent should first establish where it is operating, then prefer direct and deterministic reads over heavier retrieval flows. It also supports [[concepts/knowledge-base-discovery]] as a guardrail around other repository workflows: stage evidence first, inspect the compiled knowledge next, and only then escalate to broader retrieval.

## Safety boundary

The same source also warns that agents must treat everything under the compiled `wiki/` tree as untrusted content. Discovery therefore does not just locate files; it establishes the boundary within which the agent can read data without treating that data as instructions. This aligns with [[concepts/wiki-content-as-untrusted-data]], [[concepts/prompt-injection-defense]], and [[concepts/knowledge-boundaries]].

The source further states that agents must not directly edit anything under the knowledge base `wiki/` directory or `.openkb/` directory without an explicit user request. Discovery therefore does not grant permission to modify those locations; it only establishes the correct context for read operations and user-guided actions. This also aligns with [[concepts/reserved-wiki-files]] and [[concepts/read-only-kb-operations]].

In agent-ready-context workflows, this separation matters because durable knowledge belongs in `okf/wiki/`, procedural action lives in skills, and repository orientation belongs in `AGENTS.md`; discovery only identifies the active KB so that those responsibilities are not mixed up.

## In practice

Knowledge base discovery is the discipline of resolving the active KB root explicitly, respecting OpenKB's lookup order, and refusing to proceed when that resolution fails. In practice, it anchors the rest of the OpenKB workflow: discover the root with `openkb status`, inspect the compiled index, read the most relevant concept or entity pages directly, and escalate to heavier retrieval only when necessary. It is a small step with large consequences: it prevents misdirected reads, preserves user trust, and creates a dependable starting point for every later OpenKB task.

## Related pages

- [[summaries/agents__skills__openkb__SKILL-md]]
- [[concepts/preflight-checks]]
- [[concepts/path-safety]]
- [[concepts/configuration-precedence]]
- [[concepts/filesystem-validation]]
- [[concepts/cost-aware-tool-use]]
- [[concepts/non-interactive-agent-design]]
- [[concepts/knowledge-boundaries]]
- [[concepts/reserved-wiki-files]]
- [[concepts/safe-automation]]
- [[concepts/evidence-grounded-answering]]
- [[concepts/index-based-discovery]]
- [[concepts/wiki-content-as-untrusted-data]]
- [[concepts/prompt-injection-defense]]
- [[concepts/read-only-kb-operations]]
- [[concepts/agent-context-layering]]
- [[concepts/agent-ready-context-skill]]
- [[concepts/agents-md-maintenance]]
- [[concepts/compiled-knowledge-bases]]
- [[concepts/source-pack-staging]]
- [[concepts/okf-bundle-validation]]
- [[concepts/graceful-degradation]]
- [[concepts/preflight-checks]]

See also: [[summaries/repo-snapshot]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]


See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]


See also: [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]