---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md"]
description: "Assigning different licenses to different file types within one project."
---

# License Segmentation by File Type

License segmentation by file type is the practice of applying different licenses to different classes of files within the same project, usually to separate documentation, assets, and executable code. It is a practical form of [[concepts/split-licensing]] that makes reuse conditions clearer and helps preserve [[concepts/license-compliance-requirements]] across mixed-content repositories.

## Core idea

Instead of giving an entire skill or repository a single blanket license, the project divides its contents into categories and assigns each category a license that matches how the material is used and distributed. This reduces ambiguity when a package includes both prose and runnable code.

## Example from the source document

The document [[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]] describes a two-part licensing structure for the `subagent-profile-adapter` skill:

- `SKILL.md`, original files under `references/` and `assets/`, and other original documentation are licensed under [[concepts/creative-commons-attribution-4-0]].
- Original executable files under `scripts/` are licensed under [[concepts/apache-license-2-0]].
- The skill points to complete license texts in `LICENSES/`.
- It also states that there is no third-party-derived material, so no separate `THIRD_PARTY_NOTICES.md` is needed.

## Why it matters

- It clarifies reuse expectations for different artifact types.
- It supports [[concepts/licensing-and-attribution]] by pairing file-category rules with source attribution.
- It aligns with [[concepts/open-source-attribution]] and [[concepts/attribution-based-reuse]] by making provenance and permissions explicit.
- It can reduce compliance mistakes in repositories that mix prose, assets, and code.

## Related patterns

- [[concepts/split-licensing]]: broader pattern of using more than one license in a single project.
- [[concepts/license-compliance-requirements]]: the policy and notice obligations that segmentation helps satisfy.
- [[concepts/permissive-open-source-licensing]]: relevant when one segment uses Apache-2.0 or similar terms.
- [[concepts/creative-commons-attribution-4-0]]: commonly used for documentation and other authored content.
- [[concepts/apache-license-2-0]]: commonly used for source code and executable scripts.
