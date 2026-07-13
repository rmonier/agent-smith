---
type: "Concept"
sources: ["summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__LICENSING-md.md", "summaries/agents__skills__skill-creator__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__NOTICE.md"]
description: "How repositories encode rights, attribution, and reuse terms."
---

# Licensing and Attribution

Licensing and attribution covers the legal and provenance metadata that tells readers who created a work, what rights apply, and how the material should be credited when reused. In this wiki, it is closely related to [[concepts/license-compliance-requirements]], [[concepts/open-source-attribution]], [[concepts/provenance-tracking]], and [[concepts/attribution-based-reuse]]. The repo snapshot shows that this concern is not isolated to a single notice file: it is repeated across the repository's core governance files, license texts, skill packages, and third-party notice artifacts.

## What it captures

A licensing-and-attribution record usually answers four basic questions:

- Who owns the work or holds the copyright
- What license or reuse terms apply
- Where the material originally came from
- How the original author or upstream project should be credited

That makes it a foundation for safe reuse, traceability, and downstream documentation integrity.

In the repository snapshot, this pattern appears at multiple levels:

- Repository-wide governance files such as `LICENSE`, `NOTICE`, `LICENSING.md`, `REUSE.toml`, `THIRD_PARTY_NOTICES.md`, and `CITATION.cff`
- Shared license texts under `LICENSES/`
- Skill-local licensing bundles under `.agents/skills/*/LICENSES/` and `.agents/skills/*/THIRD_PARTY_NOTICES.md`
- Documentation and asset packs that separate original content from executable code and mirrored material

## Source examples

The document [[summaries/agents__skills__agent-ready-context__NOTICE]] is a compact example of this pattern. It functions as a legal notice rather than instructional content and preserves:

- Copyright attribution to Romain Monier
- The project name `agent-smith — agent-ready-context`
- The upstream source URL `https://github.com/rmonier/agent-smith`
- The author name and GitHub profile reference

The document [[summaries/agents__skills__subagent-profile-adapter__NOTICE]] shows the same pattern for another packaged component. It records:

- Copyright attribution to Romain Monier
- The component name `agent-smith — subagent-profile-adapter`
- The upstream source project `agent-smith`
- The original source URL `https://github.com/rmonier/agent-smith`
- The author name and GitHub profile reference

The document [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]] shows the same pattern for imported or mirrored code. It records:

- The local fallback location in `scripts/editorial_pass.py`
- The upstream repository `VectifyAI/OpenKB` and source file `openkb/agent/compiler.py`
- The verified upstream release tag `v0.4.4` and commit `bd9fe3989e71fc8012b19eb305662fa307f0a799`
- Apache-2.0 licensing and copyright attribution to Vectify AI
- The distinction between verbatim reuse and clean-room reimplementation

The licensing note in [[summaries/agents__skills__skill-creator__LICENSING-md]] extends this pattern to a multi-license skill package. It separates original documentation from executable code and records:

- `SKILL.md`, original files under `references/` and `assets/`, and other original documentation under [[concepts/creative-commons-attribution-4-0]]
- Original executable files under `scripts/` under [[concepts/apache-license-2-0]]
- `LICENSES/` as the location of the complete license texts
- Attribution to Romain Monier and the original source project `agent-smith`
- The absence of `THIRD_PARTY_NOTICES.md` because the skill contains no third-party-derived material

The companion note in [[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]] shows the same split-license structure in another skill package. It records:

- `SKILL.md`, original files under `references/` and `assets/`, and other original documentation under [[concepts/creative-commons-attribution-4-0]]
- Original executable files under `scripts/` under [[concepts/apache-license-2-0]]
- Copyright attribution to Romain Monier
- The original source project `agent-smith`
- Complete license texts under `LICENSES/`
- The explicit statement that no `THIRD_PARTY_NOTICES.md` is needed because no third-party-derived material is present

The repository snapshot also shows that licensing and attribution are normalized across the broader file surface:

- Top-level compliance files define repository-wide policy and notice behavior
- Bundled license files are tracked alongside the source pack and summary pages
- Package-local notices reinforce the split between original authored content and reused upstream material
- The documentation tree includes an illustration asset, showing that even non-text content is part of the same provenance and reuse surface

This kind of notice does not explain how the software works; it records the rights and provenance attached to the material.

## Why it matters

Licensing and attribution support several wiki goals:

- They preserve [[concepts/provenance-tracking]] across imported or derived material
- They help distinguish original authorship from compiled or summarized knowledge
- They reduce ambiguity when source material is redistributed or transformed
- They create a reliable basis for source-provenance and reuse governance
- They document when fallback code depends on upstream behavior but not on the original implementation itself
- They make mixed-license projects easier to audit by separating documentation, source references, and executable code
- They help repository inventories identify which files carry legal metadata versus ordinary project content

## Relationship to other concepts

- [[concepts/open-source-attribution]] focuses on giving proper credit to upstream open-source authors.
- [[concepts/license-compliance-requirements]] focuses on meeting the obligations imposed by a license.
- [[concepts/provenance-tracking]] focuses on recording where content came from and how it entered the knowledge base.
- [[concepts/attribution-based-reuse]] focuses on reuse patterns that depend on preserving credit and source metadata.
- [[concepts/clean-room-reimplementation]] is relevant when behavior is reproduced without copying the original implementation.
- [[concepts/compatibility-fallback]] is relevant when mirrored behavior exists only to preserve compatibility in constrained environments.
- [[concepts/creative-commons-attribution-4-0]] and [[concepts/apache-license-2-0]] are common license families that appear in mixed-source skill packages.
- [[concepts/split-licensing]] captures the broader pattern of assigning different license terms to different file classes within one package.
- [[concepts/repository-inventory]] helps explain why a file surface needs to enumerate legal artifacts alongside source and documentation.

## Practical pattern

A strong licensing-and-attribution page or notice usually includes:

- The work title or package name
- The copyright holder
- The source repository or origin
- The license name or license family
- Any author or upstream reference needed for proper credit
- A clear note distinguishing copied material from independently reimplemented behavior
- Any document that explains how lineage, notices, and full license texts are partitioned across the package

When these details are preserved, the wiki can safely compile, summarize, and cross-link source material without losing legal or historical context.

See also: [[summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt]]

See also: [[summaries/agents__skills__skill-creator__LICENSES__CC-BY-4-0-txt]]

See also: [[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]]

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt]]

See also: [[summaries/repo-snapshot]]