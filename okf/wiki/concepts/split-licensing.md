---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md"]
description: "Using different licenses for different file types within one skill."
---

# Split Licensing

Split licensing is the practice of assigning different licenses to different parts of the same project based on file type or role. In the `subagent-profile-adapter` skill, the licensing file separates documentation and asset content from executable scripts, giving each group its own license terms.

## Core Idea

This approach makes the legal status of a repository component more precise. Instead of applying one blanket license to everything, the project declares which files are governed by which license and keeps that mapping explicit in the licensing document.

## How It Appears In The Skill

The source document `[[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]]` states that:

- `SKILL.md`, original files under `references/` and `assets/`, and other original documentation are licensed under [[concepts/creative-commons-attribution-4-0]].
- Original executable files under `scripts/` are licensed under [[concepts/apache-license-2-0]].
- The skill includes complete license texts in `LICENSES/`.
- The skill says it contains no third-party-derived material, so it does not require its own `THIRD_PARTY_NOTICES.md`.

## Why It Matters

- It supports [[concepts/license-segmentation-by-file-type]] by matching the license to the content category.
- It improves [[concepts/license-compliance-requirements]] by making reuse and distribution terms easier to interpret.
- It reinforces [[concepts/licensing-and-attribution]] by preserving copyright and source provenance.
- It reduces ambiguity for downstream users who may reuse documentation differently from executable code.

## Related Patterns

- [[concepts/permissive-open-source-licensing]] for the broader use of permissive licenses.
- [[concepts/open-source-attribution]] for preserving author and source credit.
- [[concepts/source-provenance]] for documenting where the material came from.
- [[concepts/single-source-of-truth]] for keeping the license terms centralized in one authoritative document.

## Practical Implication

Split licensing works best when the repository clearly separates content categories and when the license statement is easy to find. In this skill, that separation is already reflected in the file layout and the explicit notice in the licensing document.