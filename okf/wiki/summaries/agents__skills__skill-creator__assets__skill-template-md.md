---
type: "Summary"
description: "Template for defining a reusable action-oriented agent skill file."
doc_type: short
full_text: "sources/agents__skills__skill-creator__assets__skill-template-md.md"
---

# Summary

This document is a template for creating an action-oriented agent skill in Markdown. It defines the expected frontmatter and section structure for a reusable skill specification.

## What the template includes

- Frontmatter fields for `name`, `description`, `license`, `compatibility`, and `metadata`
- A versioned `metadata` block with an example `owner`
- A title and short statement describing the skill's purpose
- Standard sections for `Workflow`, `Commands`, and `Edge cases`

## Intended use

The template is meant for skills that encapsulate a repeated operational procedure, such as a validation flow, transformation pipeline, tool integration, or command sequence. It encourages a deterministic and reusable format for documenting how an agent should perform a specific action.

## Structural guidance

### Frontmatter

The example frontmatter shows the minimum identity and maintenance metadata expected for a skill:

- `name` gives the skill identifier
- `description` explains when to use it
- `license` records usage terms
- `compatibility` captures tool requirements only when necessary
- `metadata.version` and `metadata.owner` support maintenance and ownership

### Workflow section

The workflow is presented as a short ordered procedure:

1. Perform the first deterministic step
2. Use bundled scripts or references only when needed
3. Validate the result

This emphasizes [[concepts/skill-based-automation]], [[concepts/deterministic-validation]], and predictable execution.

### Commands section

A dedicated commands block provides space for concrete shell usage, connecting the template to [[concepts/skill-based-automation]] and [[concepts/cross-platform-tooling]].

### Edge cases section

The template explicitly reserves space for important exceptions or failure modes, reinforcing graceful error handling and robust task design.

## Key ideas

- Skills should be documented as focused, repeatable procedures
- Deterministic steps and explicit validation are core expectations
- Tool or script usage should be included only when it materially supports the workflow
- Edge cases are treated as a first-class part of operational documentation

## Possible related concepts

- [[concepts/skill-based-automation]]
- [[concepts/deterministic-validation]]
- [[concepts/cross-platform-tooling]]
- graceful error handling

## Related Concepts
- [[concepts/tool-boundaries]]
- [[concepts/context-action-separation]]
- [[concepts/documentation-architecture]]
- [[concepts/quality-gates]]
- [[concepts/tooling-context-isolation]]
