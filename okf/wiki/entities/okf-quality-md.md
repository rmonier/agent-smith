---
sources: ["summaries/okf-spec.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
type: "Work"
description: "Offline baseline for OKF v0.1 bundle quality and validation"
---

# OKF Quality and Offline Conformance Baseline

The **OKF Quality and Offline Conformance Baseline** is the embedded offline reference for OKF v0.1 validation and bundle structure. It describes how an agent can create, refresh, and validate an OKF bundle without network access, and it serves as the local quality baseline until the official spec is refreshed.

## What it covers

- A bundle is a directory tree of UTF-8 Markdown files, not a binary artifact or runtime service.
- The baseline treats `okf/wiki/` as the durable knowledge/context source of truth for agents, while repository source code remains the source of truth for code.
- It allows bundle transport as a Git repository, subdirectory, zip or tarball, or plain directory.
- It describes a typical layout with `index.md`, `log.md`, `AGENTS.md`, and grouped content areas such as `concepts/`, `summaries/`, `entities/`, `sources/`, `explorations/`, `reports/`, and `tooling/`.

## Validation rules

- Every non-reserved `.md` file must have parseable YAML frontmatter.
- Every concept document must have a non-empty `type` field.
- `index.md` and `log.md` are reserved navigation/history files and are not concept documents.
- Unknown `type` values, missing optional fields, and broken standard links are tolerated by the OKF spec.
- In `--openkb-wiki` mode, broken `wikilinks` are treated as errors and OpenKB-specific conventions are checked on top of the spec.

## OpenKB-specific guidance

- OpenKB concept pages use fields such as `type`, `description`, and `sources`.
- Summary pages use fields such as `sources`, `brief`, `doc_type`, and `full_text`.
- `explorations/findings/` pages should use `type: Finding` and be listed in the root `index.md` under `## Explorations`.
- The validator skips root `AGENTS.md`, `sources/`, and `reports/` when validating an OpenKB wiki, but still validates the main wiki areas and hand-authored `tooling/` pages.

## Tooling policy

- The local tooling rule is that `tooling -> project` is allowed, but `project concept pages -> tooling` is forbidden.
- The root `index.md` is an exception because bundle navigation must enumerate the bundle, including tooling context.
- Local tooling pages must include at least one outgoing wikilink to durable project knowledge.
- Tooling pages are local by default, and the committed `tooling/index.md` acts as the shared navigation stub.

## Validation commands

- OKF validation uses `uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki`.
- Tooling link policy validation uses `uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .`.

## Related pages

- [[concepts/okf-offline-conformance]]
- [[concepts/okf-validation]]
- [[concepts/openkb-wiki-validation-modes]]
- [[concepts/tooling-link-policy]]
- [[concepts/wiki-context-routing]]
- [[entities/okf]]
- [[entities/openkb-wiki]]
- [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]]

See also: [[summaries/okf-spec]]