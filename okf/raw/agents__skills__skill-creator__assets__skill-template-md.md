---
type: "source-file"
title: ".agents/skills/skill-creator/assets/skill-template.md"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/skill-creator/assets/skill-template.md"
source_path: ".agents/skills/skill-creator/assets/skill-template.md"
source_kind: "markdown"
source_hash: "sha256:4aa54ad78001220c0e146977bc5059d2706c754de3c1ad5937a4b285d00ba383"
source_commit: "bca94c0d3aeaad4aa9c430aba0f2ba6a2dc1e1ee"
tags: [source-file, markdown]
---

# .agents/skills/skill-creator/assets/skill-template.md

~~~
---
name: example-action-skill
description: Performs a repeated action. Use when the agent/harness needs to run this specific workflow, validation, transformation, tool integration, or command sequence.
license: MIT
compatibility: Describe required tools only if needed.
metadata:
  version: "0.1.0"
  owner: project
---

# Example Action Skill

State the action this skill performs.

## Workflow

1. Do the first deterministic step.
2. Use bundled scripts or references only when needed.
3. Validate the result.

## Commands

```bash
# example command
```

## Edge cases

- List the important action-specific edge cases.
~~~
