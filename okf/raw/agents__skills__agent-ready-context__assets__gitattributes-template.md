---
type: "source-file"
title: ".agents/skills/agent-ready-context/assets/gitattributes.template"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/agent-ready-context/assets/gitattributes.template"
source_path: ".agents/skills/agent-ready-context/assets/gitattributes.template"
source_kind: "other"
source_hash: "sha256:936dd58aa2f6c88af79bc137de2b935b5e4faaa934224364c9729cbbf132446d"
source_commit: "1ee94b6b1cbd3168d6dc0d0293dd251fb1c0070a"
tags: [source-file, other]
---

# .agents/skills/agent-ready-context/assets/gitattributes.template

~~~
# LF normalization keeps deterministic OKF staging hashes stable across platforms.
* text=auto eol=lf

# Binary files must never be text-normalized.
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.webp binary
*.pdf binary
*.zip binary
*.gz binary
*.tar binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
~~~
