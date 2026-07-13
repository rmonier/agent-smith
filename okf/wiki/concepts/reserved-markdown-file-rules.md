---
type: "Concept"
sources: ["summaries/okf-spec.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
description: "Rules for using reserved markdown filenames in OKF bundles."
---

# Reserved Markdown File Rules

Reserved Markdown file rules define which filenames have special meaning in an OKF bundle and therefore must not be used as ordinary concept documents. The core purpose is to preserve navigation, history, and validation behavior across the wiki structure.

## Reserved filenames

The reserved filenames are:

- `index.md` - directory listing and progressive-disclosure navigation
- `log.md` - chronological update history for that scope

These names are reserved at any level of the hierarchy, not just at the bundle root. A file with either name serves a structural role rather than a content-document role.

## Required behavior

- Reserved files must follow their reserved structure when present.
- They must not be treated as standard concept documents.
- All other `.md` files are concept documents and must have YAML frontmatter.
- Non-reserved pages need a non-empty `type` field in frontmatter under the OKF v0.1 baseline.

## Practical implications

- `index.md` files act as navigational entry points for a directory.
- `log.md` files capture date-grouped change history.
- Producers should avoid using these names for topical documentation, even if the content seems concept-like.
- Consumers should tolerate missing optional fields, but still enforce the reserved-file distinction.

## Related rules

These reserved-file rules connect closely to [[concepts/reserved-navigation-files]], [[concepts/reserved-wiki-files]], and [[concepts/frontmatter-metadata]]. They also support [[concepts/knowledge-base-navigation]] and [[concepts/okf-offline-conformance]] by keeping structural files separate from ordinary content.

The source reference for this concept is [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]], which describes the OKF baseline, reserved filenames, and validation expectations in more detail.


See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/okf-spec]]