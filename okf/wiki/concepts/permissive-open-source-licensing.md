---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt.md"]
description: "Licensing model with broad reuse rights and light obligations."
---

# Permissive Open-Source Licensing

Permissive open-source licensing grants broad rights to use, modify, sublicense, and redistribute software or documentation while imposing relatively few obligations. It is designed to support reuse across open and proprietary projects while preserving core requirements such as attribution, notice retention, and license text preservation.

The Apache License 2.0, captured in [[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]], is a clear example of this model. In the subagent-profile-adapter skill, it is paired with a split licensing structure: original documentation and assets are licensed under Creative Commons Attribution 4.0 International, while original executable files under `scripts/` are licensed under Apache License 2.0. The skill also states that complete license texts live in `LICENSES/` and that no third-party-derived material is included, so no separate third-party notices file is needed.

## Core Characteristics

- Grants wide permission to use, copy, modify, sublicense, and distribute.
- Usually allows incorporation into proprietary or mixed-license projects.
- Focuses on attribution, notice retention, and license text preservation rather than copyleft-style reciprocity.
- Often includes an explicit patent license to reduce downstream legal uncertainty.
- Uses clear warranty and liability disclaimers to limit author responsibility.

## What Makes It Permissive

Permissive licenses minimize downstream restrictions. Instead of requiring derivative works to remain under the same license, they usually let redistributors choose their own licensing terms, provided they keep required notices and do not misrepresent authorship or remove mandatory legal text.

This makes permissive licensing attractive for broad adoption, vendor integration, and reuse across different legal and technical ecosystems. It also aligns with [[concepts/open-source-attribution]], [[concepts/licensing-and-attribution]], and reuse patterns that preserve provenance while remaining easy to adopt.

## Apache License 2.0 as an Example

From the source document:

- The license defines key legal terms such as `Work`, `Derivative Works`, `Contribution`, and `Contributor`.
- It grants a perpetual, worldwide, royalty-free copyright license.
- It grants a patent license for claims necessarily infringed by contributor submissions.
- It requires redistribution of the license text and preservation of notices.
- It requires prominent marking of modified files.
- It includes an optional `NOTICE` handling rule for derivative distributions.
- It disclaims warranties and limits liability.

These details make Apache 2.0 especially useful as a permissive license with stronger patent language than some simpler permissive licenses.

## Relationship to Other Concepts

- [[concepts/license-conditions]]: permissive licenses still impose conditions, even if they are lightweight.
- [[concepts/licensing-and-attribution]]: attribution and notice preservation are central to permissive reuse.
- [[concepts/open-source-attribution]]: permissive licensing supports reuse while preserving author credit.
- [[concepts/supply-chain-security]]: explicit license terms and provenance help manage downstream risk.
- [[concepts/source-trust-levels]]: license terms can influence how confidently downstream users reuse a source.
- [[concepts/split-licensing]]: the source document demonstrates how a skill can separate documentation and executable code under different licenses.

## Practical Implications

- Teams can adopt permissively licensed components with fewer compatibility constraints.
- Downstream projects can repackage or extend the work without inheriting the same license terms.
- Legal review still matters, especially for patent clauses, trademark limits, and notice obligations.
- License compliance should be checked as part of [[concepts/license-compliance-requirements]] and [[concepts/preflight-checks]].
- Clear license segmentation by file type reduces ambiguity when a repository mixes documentation, assets, and executable scripts.

## Source Anchor

- [[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]] documents the Apache License 2.0 text used as the source example for this concept.
- [[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]] records the skill-level licensing split between `CC-BY-4.0` and `Apache-2.0`.

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt]]