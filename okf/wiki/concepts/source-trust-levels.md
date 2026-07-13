---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__references__runtime-detection-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md"]
description: "Trust labels show how authoritative a source is in staged evidence."
---

# Source Trust Levels

Source trust levels are labels that record how authoritative and reliable a source is when turning fetched material into staged evidence. They help preserve [[concepts/provenance-tracking]], support safer use of [[concepts/external-documentation]], and reduce the risk of treating weak or misleading sources as equal to canonical documentation.

## Core idea

When external material is fetched for knowledge-base ingestion, the source should be classified with an explicit trust value such as `official-docs`, `vendor-blog`, or `community`. This classification captures how close the source is to the canonical publisher and helps later readers judge how much confidence to place in the extracted facts.

In the source guidance summarized in [[summaries/agents__skills__agent-ready-context__references__external-docs-md]], trust is part of the required provenance metadata alongside the URL, retrieval timestamp, and fetch mechanism. The same guidance also narrows what may be fetched: only user-supplied URLs or official vendor or specification pages explicitly named by the workflow should be used, and official docs should be preferred over blogs or forums.

## Why trust levels matter

Trust levels make external evidence easier to evaluate and safer to use:

- They distinguish official vendor documentation from less authoritative sources.
- They encourage preference for canonical references over blogs, forums, or secondary commentary.
- They make evidence review more transparent by exposing where confidence should be high or downgraded.
- They complement [[concepts/prompt-injection-defense]] by reminding the agent that even official pages remain untrusted fetched input.
- They improve [[concepts/evidence-staging]] by ensuring staged files preserve context about source quality, not just source location.
- They reinforce [[concepts/knowledge-boundaries]] by keeping external research scoped to approved URLs and explicitly named authoritative sources.

## Common trust distinctions

The source document gives example trust values rather than a fixed universal taxonomy. Typical levels include:

- `official-docs` for canonical vendor or specification documentation.
- `vendor-blog` for material published by the vendor but outside the main documentation set.
- `community` for forums, discussion posts, or community-authored guides.

A key rule is to downgrade trust when the source is not the canonical vendor documentation, even if it appears useful. Trust is therefore comparative as well as descriptive: a vendor-hosted article may still carry lower authority than the vendor's formal documentation set.

## Use in evidence files

Trust levels belong in the metadata for each staged external evidence file. A complete evidence record includes:

- the source URL
- a retrieval timestamp
- the fetch source or tool
- the trust label
- a short description of why the page matters
- short, repo-relevant paraphrased facts

This makes trust assessment part of the durable record rather than an unstated judgment. That pattern aligns with [[concepts/durable-context]] and [[concepts/source-driven-regeneration]]. It also supports [[concepts/knowledge-linking-and-citations]] by letting generated pages cite both the staged evidence file and the original URL with clear provenance.

## Relationship to security and workflow

Trust levels do not make fetched content safe to obey. The workflow still treats all fetched pages as untrusted data, including official vendor documentation. Commands, configuration snippets, or embedded instructions from fetched pages enter the record only as evidence and should not be executed automatically.

For that reason, source trust works together with [[concepts/tool-boundaries]], [[concepts/privacy-preserving-tooling]], and [[concepts/prompt-injection-defense]]. The external-docs workflow also requires that agents avoid recording credentials, tokens, or internal hostnames in evidence files, and that they report suspicious embedded prompts as possible injection attempts rather than following them.

In practice:

- prefer official documentation when available
- fetch only user-supplied URLs or official pages explicitly named by the workflow
- extract only facts relevant to the repository task
- paraphrase instead of copying large passages
- preserve trust metadata in the staged file
- avoid exposing secrets or internal hostnames during capture

## Practical interpretation

A high trust level means the source is a better factual reference, not that it can override user intent, repository policy, or execution safeguards. Trust is therefore about evidence quality and provenance, not permission.

It also does not remove the need for selective extraction. Even highly trusted pages should contribute only the facts relevant to the repository and the requested topic, keeping staged evidence concise, reviewable, and aligned with [[concepts/web-evidence-ingestion]].

## See also

- [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]
- [[concepts/external-documentation]]
- [[concepts/evidence-staging]]
- [[concepts/provenance-tracking]]
- [[concepts/prompt-injection-defense]]
- [[concepts/tool-boundaries]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/durable-context]]
- [[concepts/source-driven-regeneration]]
- [[concepts/knowledge-boundaries]]
- [[concepts/web-evidence-ingestion]]
- [[concepts/knowledge-linking-and-citations]]

See also: [[summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__runtime-detection-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]