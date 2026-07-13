---
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/graphify-report.md", "summaries/README-md.md"]
type: "Work"
description: "Official OKF specification repository in GoogleCloudPlatform/knowledge-catalog"
---

# Knowledge Catalog

Knowledge Catalog is the source repository that publishes the official Open Knowledge Format (OKF) v0.1 specification, including the `okf/SPEC.md` document referenced by [[summaries/okf-spec]].

## What it is

It is a GitHub-hosted project under the GoogleCloudPlatform organization that serves as the canonical home for the OKF specification. In this context, the repository is the authoritative work defining OKF structure, conformance expectations, and bundle organization.

## Key facts from the specification

- The OKF v0.1 spec is hosted at `https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md`.
- The spec describes OKF as a minimal, human- and agent-friendly knowledge format built from Markdown files with YAML frontmatter.
- The format emphasizes portability, diffability, parseability, and filesystem-based organization.
- The specification is the basis for tools such as `okf/wiki/` and `validate_okf_bundle.py`.

## Related concepts

- [[concepts/okf-specification]]
- [[concepts/bundle-conformance]]
- [[concepts/frontmatter-validation]]
- [[concepts/reserved-markdown-file-rules]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/spec-authority]]

## Related entities

- [[entities/google-cloud-platform]]
- [[entities/okf]]
- [[entities/okf-spec]]
- [[entities/okf-wiki]]
- [[entities/validate_okf_bundle-py]]
