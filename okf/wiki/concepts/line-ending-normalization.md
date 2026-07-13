---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__gitattributes-template.md"]
description: "Using consistent newlines so text stays stable across systems and hashing workflows."
---

# Line Ending Normalization

Line ending normalization is the practice of making text files use a consistent newline representation across environments so repository content behaves predictably on different operating systems. In Git-based workflows, this is commonly enforced with `.gitattributes` rules that normalize committed text while preserving the intended checkout behavior. In the OpenKB toolchain, it also appears at processing time: staging scripts normalize text to LF before hashing and packaging so logically identical files produce stable outputs across machines.

## Why It Matters

Different platforms have historically used different line endings, which can create noisy diffs, inconsistent hashes, and avoidable merge churn when the same file is edited on multiple systems. Normalization reduces those differences by ensuring text content is stored and processed in a stable form.

This matters especially in workflows that depend on deterministic file content for staging, packaging, or verification. In the OpenKB build workflow, line ending policy is treated as a build-stability requirement: without stable normalization, staged source bytes and derived hashes can drift across machines even when the logical content is unchanged. That makes line ending normalization a foundational part of [[concepts/deterministic-builds]], [[concepts/document-normalization]], and [[concepts/quality-gates]]. It also supports the repository-ingestion path described by [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]], where normalized text is hashed and emitted as staged Markdown sources.

## How the Source Document Uses It

The source summarized in [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]] defines a repository template that applies:

`* text=auto eol=lf`

This rule tells Git to treat files as text when appropriate and normalize them to LF line endings. The document explicitly connects this choice to deterministic OKF staging hashes, making line ending normalization part of a reproducibility strategy rather than just a formatting preference.

The workflow guidance in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] strengthens that requirement. It says `.gitattributes` should be installed from the template so LF normalization keeps deterministic staging hashes stable, and if a repository already has a `.gitattributes` file, the template must be merged rather than blindly replacing user rules. When an existing rule conflicts with the template's normalization policy, the workflow requires surfacing both versions and asking the user instead of silently overriding repository choices. After introducing or changing normalization rules, it recommends `git add --renormalize .` so tracked files are re-staged under the new policy.

The staging script summarized in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]] adds a second layer of normalization at build time. Its `normalize_text()` function decodes source bytes as UTF-8 with replacement and converts both `\r\n` and bare `\r` to `\n` before hashing or embedding content in staged files. That means line ending normalization is not only a repository policy but also an explicit transformation in the source-pack builder, reinforcing stable `source_hash` values even when local working copies differ in newline style.

The same script applies related normalization to imported reports by stripping run-dependent timestamp lines and removing date suffixes from headings before staging a Graphify report. That broader pattern shows line ending normalization as one component of a larger deterministic-staging discipline alongside document cleanup, stable hashing, and reproducible manifests.

## Relationship to Binary Files

Line ending normalization should only apply to text content. The same source document pairs normalization with explicit binary declarations for formats such as images, archives, fonts, and PDFs so Git does not rewrite non-text files. This makes line ending normalization closely related to [[concepts/binary-file-handling]] and [[concepts/git-attributes]].

The workflow context adds that normalization policy is part of a broader repository hygiene layer alongside `.gitignore` and `.graphifyignore`. Text should be normalized for reproducibility, while binary and generated artifacts should be protected from unintended rewriting or tracking. This keeps normalization aligned with [[concepts/generated-content-governance]] and [[concepts/filesystem-validation]].

The source-pack builder follows the same distinction in practice: it normalizes and hashes text-like content for staged Markdown output, while non-text or unreadable files are effectively excluded from text-based processing paths. This keeps newline normalization scoped to content that can safely participate in deterministic text staging.

## Practical Implications

- Reduces cross-platform diffs caused only by newline changes
- Helps keep staged or generated content stable across developer environments
- Supports deterministic hashing and repeatable repository processing
- Requires careful merge behavior when a repository already defines its own `.gitattributes`
- Works best when binary assets are explicitly excluded from text normalization
- Often needs `git add --renormalize .` after policy changes so the repository actually converges on the declared rules
- Benefits from build-time normalization in addition to Git policy, especially in ingestion pipelines that hash derived text artifacts
- Reinforces stable manifests and staged source documents by ensuring newline differences do not become false content changes

## Related Concepts

- [[concepts/git-attributes]]
- [[concepts/binary-file-handling]]
- [[concepts/deterministic-builds]]
- [[concepts/document-normalization]]
- [[concepts/source-driven-regeneration]]
- [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py]]