---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md"]
description: "Merges docs by updating only a managed section and preserving local content."
---

# Conservative Document Merging

Conservative document merging is an update strategy that changes only a narrow, explicitly managed portion of a file while preserving all other existing content. In this repository pattern, the merger treats the document as partly owned by automation and partly owned by humans, and it avoids rewriting repository-specific guidance outside the managed block.

## Core idea

The script in [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]] implements a conservative merge policy for `AGENTS.md` files. It uses HTML comment sentinels to delimit a section that can be safely replaced, appended, or created without disturbing the rest of the file.

This approach supports [[concepts/documentation-layer-separation]] by keeping orientation content separate from project-specific instructions, and it aligns with [[concepts/managed-document-sections]] by making the editable region explicit and machine-readable.

## How it works

The merge behavior follows three cases:

- If both `<!-- okf:start -->` and `<!-- okf:end -->` are present, the script replaces only the content between them.
- If the file already has content but no managed block, the script appends the managed section to the end.
- If the file is empty or missing, the script creates a new `AGENTS.md` with a title and the managed section.

This keeps the operation idempotent enough for repeated refreshes while still respecting pre-existing content. It is a practical example of [[concepts/agent-ready-context]] maintenance.

## Why the conservative approach matters

Conservative merging reduces the risk of accidentally deleting or overriding local repository guidance such as setup notes, test commands, security warnings, or workflow conventions. That makes it safer than a full rewrite and better suited for [[concepts/document-normalization]] tasks where structure should be standardized without flattening meaningful variation.

It also supports [[concepts/caveat-preservation]] because the script preserves the user's existing material instead of forcing the generated guidance to become the only text in the file.

## Relationship to repository governance

This pattern is part of broader [[concepts/agents-md-maintenance]] and [[concepts/okf-workflow-governance]]. The managed section acts as a routing layer rather than a knowledge store: it points agents toward `okf/wiki/index.md`, skills, and other context sources without duplicating the full procedure.

That separation is important for [[concepts/context-action-separation]] and [[concepts/knowledge-layer-separation]]:

- `AGENTS.md` provides orientation and local rules.
- The OKF wiki provides durable compiled context.
- Skills provide executable procedures.

## Key properties

- Uses explicit start/end markers to define ownership boundaries.
- Preserves existing file content outside the managed block.
- Can initialize a new file when none exists.
- Keeps generated guidance concise and routing-focused.
- Encodes a repeatable maintenance pattern for agent-facing documentation.

## Related ideas

- [[concepts/conservative-document-merging]] is closely related to [[concepts/documentation-cohesion]] because both aim to avoid unnecessary churn.
- It reinforces [[concepts/single-source-of-truth]] by steering agents toward the right source rather than duplicating all content.
- It fits [[concepts/safe-automation]] by making changes bounded, predictable, and reversible through subsequent reruns.