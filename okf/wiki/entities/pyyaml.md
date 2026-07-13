---
sources: ["summaries/agent-skills-spec.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md"]
type: "Product"
description: "Python YAML library used for metadata and frontmatter validation."
---

# PyYAML

PyYAML is a Python library for parsing and emitting YAML. In this repository, it supports validation workflows that need to read frontmatter and structured metadata from Markdown and bundle files, including Agent Skills specifications and other metadata-backed documents.

## Role in the scripts

- Imported as `yaml` in validation utilities that need YAML parsing.
- Used by `validate_okf_bundle.py` to inspect YAML frontmatter in OKF bundles and OpenKB wiki pages.
- Also relevant to lightweight validators like `.agents/skills/skill-creator/scripts/quick_validate.py`, which parse `SKILL.md` frontmatter to check fields such as `name`, `description`, and optional `compatibility`.
- Supports the Agent Skills format by validating YAML frontmatter in `SKILL.md` files, where metadata fields like `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools` are defined.
- Enables scripts to distinguish valid metadata from malformed or missing frontmatter before deeper checks run.
- Supports deterministic validation by turning structured text into data that can be checked against repository rules.

## Why it matters here

The repository uses PyYAML as a shared parsing dependency for validation paths that enforce metadata conventions. That makes it possible to validate skill definitions, OKF bundle pages, and other frontmatter-backed documents with consistent behavior. It is especially relevant to [[concepts/skill-frontmatter-schema]], [[concepts/skill-validation-workflow]], and [[concepts/deterministic-validation]].

## Related pages

- [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[concepts/frontmatter-metadata]]
- [[concepts/okf-bundle-validation]]
- [[concepts/deterministic-validation]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/provenance-tracking]]
- [[entities/python]]
- [[concepts/agent-skill-specification]]
- [[concepts/skill-frontmatter-schema]]
- [[concepts/skill-validation-workflow]]

## Related Documents
- [[summaries/agent-skills-spec]]
