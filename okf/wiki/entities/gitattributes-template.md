---
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/README-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md"]
type: "Other"
description: "Repository asset template for deterministic .gitattributes setup"
---

# gitattributes Template

`gitattributes-template` is the repository asset used as the source template for installing or updating `.gitattributes` during the OpenKB build workflow and the agent-ready-context pipeline.

## What it does

- Provides the normalization rules the workflow uses to keep line endings and staging hashes deterministic.
- Supports [[concepts/line-ending-normalization]], [[concepts/git-attributes]], [[concepts/deterministic-builds]], [[concepts/staging-manifests]], and [[concepts/toolchain-pinning]].
- Is installed from `assets/gitattributes.template` as part of the workflow's pre-ingestion setup, alongside `.gitignore` and `.graphifyignore` handling.
- If a `.gitattributes` file already exists, the workflow merges in only missing rules rather than replacing the file.
- When an existing rule conflicts with the template, the workflow requires both versions to be shown to the user before any override.
- After adding or changing `.gitattributes`, the workflow recommends `git add --renormalize .`.
- The template exists to keep LF normalization stable so deterministic staging hashes do not drift across builds.
- It is part of the build-artifact hygiene and repository bootstrap surface that keeps generated state out of version control.

## Key facts from the workflow document

- The workflow requires `.gitattributes` to be installed from `assets/gitattributes.template`.
- The merge step is conservative: append missing rules, do not silently overwrite existing normalization choices.
- Conflict handling is consent-first and explicit when pattern policy differs.
- Renormalization is recommended after any `.gitattributes` change to keep Git's index aligned with the template.
- Stable line-ending normalization is treated as part of the repository's deterministic build surface.
- The template is tied to repository agent readiness, where local-only build artifacts, staged inputs, and reproducible outputs are governed together.

## Related pages

- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[concepts/document-normalization]]
- [[concepts/git-attributes]]
- [[concepts/line-ending-normalization]]
- [[concepts/deterministic-builds]]
- [[concepts/staging-manifests]]
- repository bootstrap
- [[concepts/local-only-repo-artifacts]]
- [[entities/git]]

See also: [[summaries/repo-snapshot]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]