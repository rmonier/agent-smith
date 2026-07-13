---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__NOTICE.md", "summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__skill-creator__NOTICE.md"]
description: "How projects attribute upstream sources, authors, and license boundaries."
---

# Open Source Attribution

Open source attribution is the practice of clearly identifying original authors, upstream sources, licenses, and reuse boundaries for adapted material. It keeps provenance visible, supports license compliance, and makes it easier to audit how a project incorporates outside work.

## What it requires

- Naming the original creator or organization
- Pointing to the upstream source or repository
- Stating the applicable license
- Noting which parts were reused, adapted, or incorporated
- Preserving required notice files and third-party acknowledgments
- Separating attribution by file type when different license terms apply
- Recording component-level ownership when a repository bundles multiple derived parts

## Why it matters

Attribution is a core part of [[concepts/licensing-and-attribution]] and a practical requirement for [[concepts/license-compliance-requirements]]. It supports [[concepts/provenance-tracking]], reduces confusion about ownership, and helps downstream users understand what came from where.

It also strengthens compliance workflows by making the legal and factual history of the content explicit rather than implicit. When a project uses split licensing, attribution needs to explain not just who made the material, but which files fall under which license terms.

## Example from the source document

The document [[summaries/agents__skills__subagent-profile-adapter__NOTICE]] shows a minimal but important attribution notice for a bundled component:

- It identifies the component as `agent-smith — subagent-profile-adapter`
- It credits Romain Monier as the copyright holder
- It links the original source to `https://github.com/rmonier/agent-smith`
- It frames the file as a repository notice rather than functional code
- It provides a provenance anchor for the adapted skill component

Taken together with [[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]], this shows how a repository can separate a concise notice file from more detailed licensing documentation while still keeping attribution auditable.

## Related ideas

- [[concepts/attribution-based-reuse]]
- [[concepts/creative-commons-attribution-4-0]]
- [[concepts/apache-license-2-0]]
- [[concepts/license-segmentation-by-file-type]]
- [[concepts/licensing-and-attribution]]
- [[concepts/provenance-tracking]]
- [[concepts/license-compliance-requirements]]

## Practical takeaway

A good attribution notice does not just say that outside material was used; it makes reuse auditable by connecting authorship, source, and license in one place, and by clearly separating different license obligations when a repository mixes documentation and executable code.

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]]

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt]]