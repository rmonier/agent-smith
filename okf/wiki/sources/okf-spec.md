---
type: external-reference
title: Open Knowledge Format (OKF) v0.1 - Official Specification
resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
description: The official OKF v0.1 specification that okf/wiki/ and validate_okf_bundle.py implement and conform to.
tags: [external-docs, okf, spec]
timestamp: 2026-07-12T00:00:00Z
source: web-tool
trust: official-docs
---

# Open Knowledge Format (OKF) v0.1 - Complete Specification

## Overview

OKF is "an open, human- and agent-friendly format for representing *knowledge*" through a minimal structure: markdown files with YAML frontmatter organized in directories. The format prioritizes accessibility - readable without tools, parseable by agents, diffable in version control, and portable across systems.

## Core Principles

The specification emphasizes four primary goals:

1. Enable enrichment agents to write into a universal format
2. Guide consumption agents on reading and traversal
3. Facilitate knowledge exchange across organizations
4. Standardize minimal required fields for meaningful consumption

Notably, OKF explicitly avoids defining fixed taxonomies, prescribing infrastructure, or replacing domain-specific schemas like Avro or Protobuf.

## Key Structural Elements

**Bundle Organization:**
A knowledge bundle is a hierarchical directory of markdown files with optional `index.md` (directory listings) and `log.md` (chronological updates) at any level.

**Concept Documents:**
Each concept requires:
- A `type` field (required) - short string identifying the concept kind
- Optional: `title`, `description`, `resource` (canonical URI), `tags`, `timestamp`
- Markdown body with structural elements like schemas, examples, and citations

**Cross-linking:**
Two forms are supported: absolute bundle-relative links beginning with `/` (recommended for stability) and standard relative paths.

## Conformance Requirements

A bundle conforms to OKF v0.1 if every non-reserved `.md` file contains parseable YAML frontmatter with a non-empty `type` field. However, consumers must gracefully handle missing optional fields, unknown types, and broken links - reflecting the format's permissive design philosophy.

# Source

- https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- Retrieved: 2026-07-12
