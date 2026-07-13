---
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
type: "Work"
description: "Command for adding content to OpenKB"
---

# openkb add

`openkb add` is an OpenKB CLI command used to ingest source material into the wiki. In this document, it is mentioned as a command that should not be used for tooling context pages because those pages are not source material for project knowledge.

## Role in this policy

The tooling context policy treats `openkb add` as out of scope for `okf/wiki/tooling/` content. Tooling pages are user-scoped runtime notes, so they should stay outside normal ingestion flows and remain separate from project knowledge.

## Key points from the document

- Tooling context belongs in `okf/wiki/tooling/`, not in regular source ingestion.
- The policy explicitly says not to ingest tooling pages through `openkb add`.
- This helps preserve [[concepts/local-tooling-boundaries]] and [[concepts/tooling-context-governance]].
- The command is part of the broader OpenKB workflow, but it is not the right path for harness-specific context records.

## Related pages

- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]
- [[entities/openkb]]
- [[entities/openkb-cli]]
- [[concepts/consent-first-tooling]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/tooling-context-isolation]]
- generated generated content governance

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]