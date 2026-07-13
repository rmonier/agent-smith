---
sources: ["summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/repo-snapshot.md", "summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__transcribe-md.md", "summaries/agents__skills__graphify__references__query-md.md", "summaries/agents__skills__graphify__references__hooks-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__exports-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md", "summaries/agents__skills__graphify__-graphify_version.md", "summaries/agents__skills__agent-ready-context__assets__graphifyignore-template.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_source_pack-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/graphify-report.md"]
type: "Product"
description: "Graphify is a local-first repository graphing and analysis product."
---

# Graphify

Graphify is a repository graphing and structural analysis tool used in the agent-ready context workflow to inspect, refresh, and navigate project graph data before OpenKB ingestion.

## Role In This Document

The privacy-and-data-flows reference treats Graphify as part of the repository preparation pipeline and emphasizes that it must be routed explicitly, not left to provider auto-detection. It is used for code-only graph extraction locally, and for non-code sources only when the operator has disclosed the backend, model, endpoint, credential source, and data being sent before proceeding. The document also places Graphify inside a broader [[concepts/air-gapped-operation]] and [[concepts/explicit-provider-routing]] policy, with a local-only path always available.

## Key Facts

- The CLI is invoked as `graphify`.
- The Python package name is `graphifyy`.
- For code files, Graphify can operate locally with tree-sitter AST extraction and no network egress.
- For docs, PDFs, images, and video, Graphify may send content to the selected LLM backend unless `--backend ollama` is used.
- When Graphify needs semantic extraction for non-code sources, it reads process environment variables only and does not load `.env` files itself.
- The recommended secret-handling pattern is to source `okf/.env` into the shell so credentials remain in a gitignored file and never cross the agent context.
- The document requires an explicit `--backend <provider>` whenever non-code sources are processed, because auto-detection from exported API keys can silently route data to an unintended provider.
- In air-gapped mode, Graphify should use `--backend ollama` for non-code sources, and external docs should be provided as local files under `okf/.okf-build/input/external/`.
- Graphify is described as having no telemetry, no usage tracking, and no analytics; video/audio transcription runs locally via faster-whisper.
- The privacy reference also warns about a separate local-artifact leakage risk: files excluded only via `.git/info/exclude` or a global excludes file can still be scanned and committed into `graphify-out/` artifacts.
- The document ties Graphify to deterministic staging and KB-root safety by noting that staging and ingestion should remain inside the KB root to avoid absolute-path leakage in OpenKB registries.
- Output artifacts such as `graphify-out/cost.json`, `graphify-out/cache/`, and report files are intended to remain local and gitignored.
- The page instructs operators to announce the chosen backend before running and to re-check privacy claims whenever a pinned version changes.

## Related Concepts

- [[concepts/graph-structure-analysis]]
- [[concepts/incremental-graph-maintenance]]
- [[concepts/idempotent-graph-import]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/knowledge-graph-feedback-loops]]
- [[concepts/graph-integrity-diagnostics]]
- [[concepts/vendor-skills]]
- [[concepts/skill-vendoring]]
- [[concepts/deterministic-validation]]
- [[concepts/repo-ingestion-pipelines]]
- [[concepts/documentation-gaps]]
- [[concepts/cross-community-bridges]]
- [[concepts/openkb-build-workflow]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/explicit-provider-routing]]
- [[concepts/local-by-default-tooling]]
- [[concepts/local-artifact-leakage]]
- [[concepts/kb-root-staging]]
- [[concepts/telemetry-auditing]]
- [[concepts/air-gapped-operation]]

## Related Entities

- [[entities/graphifyy]]
- [[entities/openkb]]
- [[entities/uv]]
- [[entities/agents-skills]]
- [[entities/graphify-report-agent-smith]]
- [[entities/graphify-out-graph-report-md]]
- [[entities/okf]]
- [[entities/ollama]]
- [[entities/litellm]]

## Related Documents

- [[summaries/graphify-report]]
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]