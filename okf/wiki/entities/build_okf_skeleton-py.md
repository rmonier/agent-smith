---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md"]
type: "Work"
description: "Python utility that generates a conservative OKF wiki skeleton"
---

# build_okf_skeleton.py

`build_okf_skeleton.py` is a Python utility in the `agent-ready-context` skill that generates a conservative OKF wiki skeleton from staged source inputs. It serves as a zero-LLM fallback when no provider credentials are available, producing a minimal but navigable bundle rather than a semantically complete compilation.

## What It Does

- Reads repository and staging locations from CLI flags such as `--repo`, `--input`, and `--out`.
- Resolves the current git commit and records it in generated output.
- Creates `okf/wiki/` output folders, especially `concepts/` and `references/`.
- Writes a repository overview page with a short excerpt from `graphify-report.md` when available.
- Copies staged external markdown documents into `references/` and records them as evidence.
- Generates a root `index.md` and `log.md` so the wiki bundle is immediately navigable.

## Key Characteristics

- The script is explicitly conservative and does not claim semantic completeness.
- It uses `frontmatter()` to stamp generated pages with metadata such as title, description, tags, and `x-generator: okf-skeleton`.
- It uses `run_git()` to retrieve git metadata, returning `unknown` if git is unavailable or fails.
- It is built around filesystem staging and evidence preservation, aligning with [[concepts/source-pack-staging]], [[concepts/evidence-staging]], and [[concepts/llm-free-knowledge-bootstrap]].
- Its output structure supports [[concepts/repository-overview-generation]] and [[concepts/generated-content-governance]].
- It underpins an air-gapped, degraded-mode workflow in which the bundle can be generated locally and later reconciled with OpenKB validation.

## Output Pages

- `concepts/repo-overview.md` - repository metadata plus a Graphify excerpt.
- `concepts/external-documentation-evidence.md` - a map of copied external docs, if any exist.
- `references/*` - verbatim copies of staged external markdown files.
- `index.md` - bundle index listing generated concept pages.
- `log.md` - dated record of the skeleton generation run.

## Design Notes

The script favors traceability over interpretation. It keeps source evidence separate from compiled wiki pages, and it treats the resulting bundle as a starting point for later enrichment rather than an authoritative knowledge base. That makes it a practical implementation of [[concepts/graceful-degradation]] and [[concepts/evidence-grounded-answering]] in a no-LLM environment.

The newer privacy guidance also clarifies where this fallback fits in the broader pipeline: it is the local-only path that remains available when provider-backed tools are unavailable, while LLM-backed commands must still follow disclosure, explicit routing, and consent rules. In that framing, `build_okf_skeleton.py` is part of [[concepts/air-gapped-operation]], [[concepts/privacy-preserving-tooling]], [[concepts/local-by-default-tooling]], and [[concepts/data-flow-disclosure]].

## Related Pages

- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[entities/okf-wiki]]
- [[entities/graphify-report-agent-smith]]
- [[concepts/okf-wiki-governance]]
- [[concepts/openkb-build-workflow]]
- [[concepts/documentation-layer-separation]]
- [[concepts/air-gapped-operation]]
- [[concepts/privacy-preserving-tooling]]
- [[concepts/local-by-default-tooling]]
- [[concepts/data-flow-disclosure]]

## Related Documents
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
