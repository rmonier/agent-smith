---
type: "Summary"
description: "Generates a conservative OKF wiki skeleton from staged repository inputs."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md"
---

# Summary

`build_okf_skeleton.py` is a fallback script that generates a minimal OKF wiki skeleton from a staged source pack when no LLM provider credentials are available. It is explicitly conservative: it produces a repository overview, optional external documentation evidence, a root index, and a log entry, but does not attempt semantic completeness.

## What It Does

- Reads repository and staged input paths from CLI flags:
  - `--repo` for the git repository root
  - `--input` for the staged OKF build input directory
  - `--out` for the generated wiki output directory
- Creates the expected wiki folders under `okf/wiki/`, especially `concepts/` and `references/`.
- Captures the current git commit with `git rev-parse HEAD` and includes it in generated output.
- If present, extracts up to 80 lines from `graphify-report.md` into a generated overview page.
- Copies any staged external markdown documents from `input/external/` into `references/` and records them in a generated evidence page.
- Writes a root `index.md` and `log.md` so the bundle is navigable and traceable.

## Generated Pages

- `concepts/repo-overview.md` — a basic repository overview with commit metadata and a Graphify excerpt.
- `concepts/external-documentation-evidence.md` — a map of staged external docs used as enrichment evidence, if any exist.
- `references/*` — verbatim copies of staged external markdown documents.
- `index.md` — a simple bundle index listing generated concept pages.
- `log.md` — a dated log entry noting that a conservative skeleton was generated.

## Implementation Details

- `slugify()` lowercases and normalizes text into a URL-friendly slug, though it is not used in the current flow.
- `frontmatter()` builds wiki frontmatter with `type`, `title`, `description`, `tags`, and `x-generator: okf-skeleton`.
- `run_git()` wraps git execution and returns `unknown` on failure, making the script tolerant of non-git or broken environments.
- The script uses `pathlib` for filesystem handling and writes UTF-8 encoded markdown files.

## Notable Design Choices

- The script is intentionally non-semantic: it creates a safe starting point rather than an authoritative knowledge extraction.
- It treats external documentation as evidence material rather than as compiled knowledge.
- The root index keeps a special note for `tooling/` content, preserving the repository boundary that compiled concept pages should not depend on harness-specific pages.

## Key Ideas for Cross-Document Linking

- [[concepts/repository-overview-generation]] could capture the general shape of repository-wide summaries produced from build metadata.
- [[concepts/graph-structure-analysis]] could cover the role of Graphify reports as structural input for knowledge compilation.
- [[concepts/evidence-backed-skill-initialization]] could describe how staged external docs are separated from compiled pages.
- [[concepts/llm-free-knowledge-bootstrap]] could unify fallback generation flows that emit minimal navigable wiki bundles.
- [[concepts/tooling-boundaries]] could explain the rule that tooling context remains outside project truth.

## Findings

- This script provides a zero-LLM fallback path for OpenKB migration, ensuring a usable baseline wiki can still be produced.
- It favors traceability over completeness by anchoring output to git commit metadata and staged evidence files.
- The generated bundle is deliberately minimal, making it a scaffold for later enrichment rather than a final knowledge product.

## Relationship To The Wiki Model

This file supports the transition from raw staged sources to a structured wiki by creating the first layer of compiled pages. It aligns with the wiki's separation between source material, summaries, concepts, and references, while preserving a narrow and auditable generation path.

## Related Concepts
- [[concepts/graceful-degradation]]
- [[concepts/repository-transformation-pipelines]]
- [[concepts/source-pack-staging]]
- [[concepts/repository-ingestion]]
- [[concepts/knowledge-lifecycle-governance]]
- [[concepts/compiled-knowledge-bases]]

## Entities
- [[entities/build_okf_skeleton-py]]
- [[entities/openkb]]
- [[entities/okf-wiki]]
- [[entities/graphify-report-agent-smith]]
- [[entities/tooling]]
- [[entities/git]]
- [[entities/python]]
- [[entities/agents-skills]]
- [[entities/okf-spec]]
- [[entities/validate_okf_bundle-py]]
- [[entities/repo-snapshot]]
- [[entities/references-official-okf-spec-web-check-md]]
- [[entities/okf-wiki-index-md]]
