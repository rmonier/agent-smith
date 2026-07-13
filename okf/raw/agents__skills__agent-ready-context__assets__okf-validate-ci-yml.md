---
type: "source-file"
title: ".agents/skills/agent-ready-context/assets/okf-validate.ci.yml"
description: "Repository source file staged for OpenKB ingestion."
resource: ".agents/skills/agent-ready-context/assets/okf-validate.ci.yml"
source_path: ".agents/skills/agent-ready-context/assets/okf-validate.ci.yml"
source_kind: "text"
source_hash: "sha256:5656e022c3c94714dce12a64b4d510f66ac8292137bfff7fbae82f03f9119a6d"
source_commit: "1ee94b6b1cbd3168d6dc0d0293dd251fb1c0070a"
tags: [source-file, text]
---

# .agents/skills/agent-ready-context/assets/okf-validate.ci.yml

~~~
# OKF validation gate — GitHub Actions template.
# Install (consent-first) by copying to .github/workflows/okf-validate.yml
# in the target repository; adapt the single `uv run` step for other CI providers.
#
# Zero-LLM by design: the validator needs no API key and sends nothing anywhere,
# and it exits nonzero on structural violations, so it can gate merges.
# `openkb lint` is deliberately NOT run here: it is an LLM-backed health report
# that always completes without failing the build — run it locally instead.
#
# Action refs use major-version tags; pin them to full commit SHAs if the
# target organization's policy requires it.
name: okf-validate
on:
  pull_request:
    paths:
      - "okf/**"
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - name: Validate OKF bundle (structural, zero-LLM)
        run: uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki
~~~
