---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__NOTICE.md"]
description: "Attribution of imported content to its original upstream source."
---

# Upstream Source Attribution

Upstream source attribution records where imported or bundled material originally came from, who authored it, and what project it belongs to. It is a core part of provenance tracking and licensing and attribution because it lets downstream consumers trace ownership and origin before reusing or redistributing content.

## Why it matters

- Preserves credit for the original author and project.
- Helps distinguish local adaptations from upstream material.
- Supports license review and compliance checks.
- Provides a clear audit trail for reused files and third-party notices.

## In the source notice

The page [[summaries/agents__skills__subagent-profile-adapter__NOTICE]] is a simple attribution record for the `subagent-profile-adapter` component. It identifies:

- the upstream project as `agent-smith`
- the author as Romain Monier
- the copyright holder as Romain Monier
- the original source location as `https://github.com/rmonier/agent-smith`

This is a typical upstream attribution pattern for vendored or reused repository material: the notice file does not describe behavior, only origin and ownership.

## Related ideas

- provenance tracking: broader practice of preserving source origin metadata.
- source provenance: documenting where a file, asset, or package came from.
- licensing and attribution: pairing attribution with license obligations.
- open source attribution: crediting open-source upstreams in distributed projects.
- third party notice: a notice format used to collect attribution and licensing information.
- upstream source attribution also connects to vendor skill adoption when external skills are incorporated into a local knowledge base or toolchain.

## Practical pattern

Upstream attribution usually appears in notice files, license bundles, or third-party notices and often includes:

- project name
- author or copyright holder
- source URL or repository reference
- a note that the material originated outside the current repository

In a knowledge base, these records help keep reused artifacts linked to their original source and make later review easier.