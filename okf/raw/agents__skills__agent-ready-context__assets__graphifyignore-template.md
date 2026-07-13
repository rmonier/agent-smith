---
type: "source-file"
title: ".agents/skills/agent-ready-context/assets/graphifyignore.template"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/agent-ready-context/assets/graphifyignore.template"
source_path: ".agents/skills/agent-ready-context/assets/graphifyignore.template"
source_kind: "other"
source_hash: "sha256:4832a465ba284b8683c950a357c39c4f69818a30df442878929e05b693e2f479"
source_commit: "94e7b8ea04ed67c19b4aebc5fce5a341bbb71671"
tags: [source-file, other]
---

# .agents/skills/agent-ready-context/assets/graphifyignore.template

~~~
# Keep the compiled knowledge base out of the repo graph. The wiki is a map
# of this repository, not part of the territory: mapping it feeds generated
# pages back into the graph report that OpenKB re-ingests - a feedback loop
# that never converges. See agent-ready-context/references/workflow.md,
# "Self-reference policy".
okf/
~~~
