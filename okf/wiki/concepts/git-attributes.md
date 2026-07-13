---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__assets__gitattributes-template.md"]
description: "Repository rules that stabilize file handling, normalization, and hashing."
---

# Git Attributes

Git attributes are repository rules that control how Git treats files based on path patterns. They distinguish text files from binary files, enforce consistent line endings, and prevent file transformations that would otherwise vary across environments. In this repository-compilation workflow, `.gitattributes` is not just a formatting aid: it is a build-stability mechanism that keeps staged source files byte-stable so hashing, ingestion, and validation behave predictably.

## Why it matters

Git attributes help maintain predictable repository behavior across operating systems, Git settings, and tooling. In [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]], the main goal is to keep repository staging and hashing stable by normalizing text files to LF while explicitly protecting binary files from text processing. The workflow guidance in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] makes this operational: repositories should install or merge `.gitattributes` before building the OpenKB source pack so deterministic staging does not drift because of platform-specific line-ending changes.

The newer skill guidance strengthens this further by making `.gitattributes` part of the required repository baseline for agent-ready preparation. The repository should install or merge the baseline from the template, and conflicting rules should be surfaced to the user rather than silently replaced. This matters because OpenKB ingestion depends on stable file bytes and stable hashes; if normalization differs across machines, the staged input under `okf/.okf-build/input/` can drift even when the underlying content has not meaningfully changed.

This makes Git attributes especially relevant to [[concepts/line-ending-normalization]], [[concepts/binary-file-handling]], [[concepts/deterministic-builds]], [[concepts/kb-root-staging]], and [[concepts/hash-registry-coherence]].

## Core behavior

A `.gitattributes` file applies rules to matching files:

- `* text=auto eol=lf` tells Git to treat matching text files as text and normalize them to LF line endings.
- Binary file patterns such as `*.png`, `*.jpg`, `*.pdf`, `*.zip`, and common font formats are marked `binary` so Git does not apply text normalization.

This combination creates a clear split:

- Text content is normalized for consistency.
- Binary content is preserved byte-for-byte.

In the workflow, this is not just a formatting preference. Stable normalization keeps staged source bytes and repository-derived hashes from changing unnecessarily across machines, which supports OpenKB ingestion, deterministic source packs, and downstream validation. The skill also places `.gitattributes` alongside `.graphifyignore` and `.gitignore` as part of the repository's compilation-control surface: each file constrains a different source of drift or accidental inclusion.

## Role in repository consistency

Git attributes are a practical mechanism for cross-platform consistency. Without them, text files may acquire different line endings on different systems, and automated pipelines can produce inconsistent results. By standardizing text handling and exempting binary assets, Git attributes support reliable content ingestion, stable hashes, and repeatable repository state.

The workflow adds an important governance rule: `.gitattributes` should be installed from a template, but if a repository already has one, the file must be merged rather than replaced. Missing rules can be appended, but conflicting normalization policies should be surfaced to the user instead of silently overridden. After introducing or changing `.gitattributes`, the workflow recommends `git add --renormalize .` so the repository index reflects the new normalization policy.

The new skill-level guidance gives this a broader operational role. Because the durable knowledge workflow relies on deterministic staging into `okf/.okf-build/input/` before ingestion into [[entities/openkb]], line-ending policy becomes part of [[concepts/generated-content-governance]] rather than a low-level Git detail. Stable normalization helps preserve source-driven regeneration, prevents avoidable hash churn, and reduces the risk that registry state and compiled output drift apart during repeated add/rebuild cycles.

This ties Git attributes directly to [[concepts/document-normalization]], [[concepts/deterministic-builds]], [[concepts/provenance-tracking]], and [[concepts/source-driven-regeneration]].

## In the source document

The source documents present Git attributes both as a template and as a required part of the repository-build workflow:

- [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]] provides the concrete rules: LF normalization for text files and binary protection for common image, archive, document, and font formats.
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]] explains when and how to apply those rules during repository preparation.
- [[summaries/agents__skills__agent-ready-context__SKILL-md]] elevates `.gitattributes` to part of the default agent-ready setup baseline and explicitly says to install or merge the baseline for stable source hashes.
- The workflow frames `.gitattributes` as necessary for deterministic staging hashes, especially before building the OpenKB input bundle.
- The skill also connects stable file treatment to the safety of OpenKB's deduplication flow, where unstable bytes can interfere with predictable ingestion behavior and make drift harder to reason about.
- Both documents treat existing repository choices as authoritative unless the user approves a conflict resolution, which makes `.gitattributes` part of repository policy rather than a disposable generated file.

Together, these sources show Git attributes as a foundational piece of repository setup for [[entities/openkb]] workflows: they keep file treatment explicit, preserve binary integrity, support [[concepts/cross-platform-tooling]], and reduce cross-platform variation that would otherwise undermine stable compilation.

## Related pages

- [[concepts/line-ending-normalization]]
- [[concepts/binary-file-handling]]
- [[concepts/deterministic-builds]]
- [[concepts/document-normalization]]
- [[concepts/provenance-tracking]]
- [[concepts/hash-registry-coherence]]
- [[concepts/kb-root-staging]]
- [[concepts/source-driven-regeneration]]
- [[summaries/agents__skills__agent-ready-context__assets__gitattributes-template]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]