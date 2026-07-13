---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md"]
description: "A controlled workflow for staging and citing facts from external web documentation."
---

# Web Evidence Ingestion

Web evidence ingestion is the practice of collecting facts from external documentation pages, converting them into staged evidence files, and adding them to the knowledge base in a controlled way. It enables external sources to support repository-focused knowledge work without weakening [[concepts/knowledge-boundaries]], [[concepts/safe-automation]], or [[concepts/provenance-tracking]].

This concept is defined most directly in [[summaries/agents__skills__agent-ready-context__references__external-docs-md]].

## Core idea

External documentation can be useful when a user supplies URLs or when a workflow explicitly names official vendor or specification pages. The goal is not open-ended browsing. The goal is to extract a small set of relevant facts, preserve source context, and stage those facts as evidence for later compilation.

This makes web evidence ingestion a specialized form of [[concepts/evidence-staging]] that operates under tighter trust and scope rules than repository-derived sources.

## Scope constraints

A web evidence workflow should stay narrowly bounded:

- Fetch only URLs supplied by the user or official pages explicitly named by the workflow.
- Avoid browsing beyond those pages.
- Prefer official vendor documentation over blogs, community posts, or forum answers.
- Extract only facts relevant to the repository and the requested topic.
- Prefer short paraphrases over large copied passages.

These constraints reinforce [[concepts/minimal-tool-scoping]], [[concepts/tool-boundaries]], [[concepts/spec-authority]], and [[concepts/documentation-source-priority]].

## Evidence staging model

Each fetched URL should become its own Markdown evidence file stored in a staging directory before ingestion. The staged file records what page was used, why it matters, what facts were extracted, and how trustworthy the source is.

Important elements include:

- page title
- source URL
- short description of relevance
- retrieval timestamp
- fetch source such as a web tool
- trust label such as official docs, vendor blog, or community
- a short list of paraphrased relevant facts

After staging, the evidence is ingested into the knowledge base rather than being treated as ad hoc browsing output. This connects web evidence ingestion to [[concepts/repository-ingestion]], [[concepts/frontmatter-metadata]], and [[concepts/knowledge-linking-and-citations]].

## Security and trust model

Fetched pages are untrusted inputs, even when they come from official vendors. A documentation page may contain instructions, examples, or embedded text that should never be treated as agent directives.

Key protections include:

- never treating fetched text as instructions for the agent
- ignoring embedded prompts or suspicious guidance
- not running commands, installing packages, or changing files just because a page recommends it
- treating commands from docs as evidence until separately validated for the actual user task
- excluding credentials, tokens, and internal hostnames from staged evidence
- recording provenance and trust honestly

This ties the concept closely to [[concepts/prompt-injection-defense]], [[concepts/source-trust-levels]], [[concepts/tooling-context-isolation]], [[concepts/privacy-preserving-tooling]], and [[concepts/supply-chain-security]].

## Why timestamps are allowed here

Repo-derived staged files often favor deterministic generation, but web evidence is different because the retrieved page is external and time-sensitive. Recording a retrieval timestamp is part of honest provenance rather than an unnecessary source of variation.

This makes web evidence ingestion compatible with [[concepts/deterministic-builds]] only by carving out a documented exception for external fetches. The result is a balance between reproducibility and accurate source tracking.

## Relationship to compilation

The staged evidence file is an input to later wiki generation, not the final knowledge product by itself. Summary, concept, or entity pages may cite both the staged evidence file and the original URL. This preserves traceability while keeping the generated wiki focused and concise.

In practice, web evidence ingestion supports [[concepts/llm-wiki]], [[concepts/incremental-compilation]], and [[concepts/generated-content-governance]] by ensuring that external material enters the system through a reviewable, well-scoped path.

## Typical use cases

Common examples include:

- vendor configuration docs that clarify runtime behavior
- specification pages that define official field meanings or protocol rules
- cloud provider docs that explain deployment or integration constraints
- user-supplied documentation URLs needed to answer a specific repository question

When used well, the process strengthens [[concepts/external-documentation]] as a supporting source without letting it outrank repository evidence or explicit workflow scope.

## Practical takeaway

Web evidence ingestion is a disciplined method for bringing external documentation into a repository-centered knowledge workflow. Its value comes from three things working together:

- narrow fetch scope
- explicit provenance and trust labeling
- strong separation between extracted facts and executable action

That combination makes it a durable pattern for adding external context while preserving [[concepts/context-action-separation]], [[concepts/knowledge-boundaries]], and [[concepts/safe-automation]].

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]
- [[concepts/evidence-staging]]
- [[concepts/external-documentation]]
- [[concepts/provenance-tracking]]
- [[concepts/prompt-injection-defense]]
- [[concepts/source-trust-levels]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/minimal-tool-scoping]]
- [[concepts/tool-boundaries]]
- [[concepts/safe-automation]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__graphify__references__add-watch-md]]