---
sources: ["summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__subagent-profile-adapter__LICENSING-md.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt.md", "summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__NOTICE.md", "summaries/agents__skills__skill-creator__LICENSING-md.md", "summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt.md", "summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__agent-ready-context__NOTICE.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md"]
type: "Work"
description: "Permissive open-source license used across the repo's scripts and notices."
---

# Apache License 2.0

The Apache License 2.0 is a permissive open-source software license used for code, documentation, and other source materials. It grants broad reuse rights while requiring preservation of the license text, attribution notices, and any applicable NOTICE file content.

In this wiki, it governs the original executable files under `scripts/` in `[[entities/agent-ready-context-skill]]`, including the original executable files in `[[entities/skill-creator]]` and `[[entities/subagent-profile-adapter]]`. It also covers the OpenKB-derived compatibility fallback embedded in `scripts/editorial_pass.py`, the `scripts/init_skill.py` skill bootstrapper, and the local-alias helper `scripts/ensure_local_alias.py`, alongside the license text referenced by `[[summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt]]` and `[[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]]`.

The `[[summaries/agents__skills__skill-creator__NOTICE]]` page adds that `[[entities/skill-creator]]` incorporates a small number of passages adapted from Anthropic's and OpenAI's own skill-creator skills, with the exact passages and sources listed in `[[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]`.

The README for `agent-smith` reinforces this same licensing boundary: the original executable files under each skill's `scripts/` are Apache-2.0, while the original skill instructions, documentation, specifications, and references are CC-BY-4.0. It also states that vendored `openkb` and `graphify` skills remain under their upstream licenses, and that the compiled `okf/` wiki is internal working context rather than part of the licensed product surface.

## In This Wiki

- Used for original executable files in `[[entities/agent-ready-context-skill]]`
- Used for original executable files in `[[entities/skill-creator]]`
- Used for original executable files in `[[entities/subagent-profile-adapter]]`
- Applied to the embedded fallback in `scripts/editorial_pass.py`, including the verbatim `_MIRRORED_KNOWN_TARGETS_USER` string and the reimplemented `_format_targets_mirrored` behavior
- Applied to `scripts/init_skill.py`, which bootstraps new skill directories and writes a starter `SKILL.md`
- Applied to `scripts/ensure_local_alias.py`, which creates a local alias to `AGENTS.md`, prefers a relative symlink, and falls back to a pointer file when symlinks are unavailable
- Used by `scripts/ensure_local_alias.py` to support local-only harness aliasing while recording the alias in `.git/info/exclude`
- Referenced alongside `[[entities/creative-commons-attribution-4-0-international-public-license]]` in the skill's licensing split
- Noted in the skill's license notice as the governing license for `scripts/`
- Also appears as a standalone license text in `[[summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt]]` and `[[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]]`
- Defined in the skill's licensing file as the license for original executable files under `scripts/`
- Used in the skill-creator notice to describe adapted passages from Anthropic and OpenAI source material under Apache-2.0
- Extended by `[[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]` to record the adapted passages that closely track upstream wording and require notice under Apache-2.0 section 4(c)
- Documented as part of the provenance check that named Anthropic `skill-creator`, OpenAI system `skill-creator`, and `superpowers`' `writing-skills` as the compared upstream sources
- Paired with an explicit re-verification warning: the upstream copyright holders, years, and licence terms should be checked again before relying on the adaptation
- Reused by `[[entities/subagent-profile-adapter]]` as the governing license for its staged Apache-2.0 source file, reinforcing the same license lineage across related skill packages
- Newly confirmed in `[[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]]` as the license for original executable files under `scripts/` and for the skill's original documentation split by file type
- Explicitly paired in that licensing file with `CC-BY-4.0` for `SKILL.md`, `references/`, `assets/`, and other original documentation
- Stated to have no third-party-derived material in `[[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]]`, so no `THIRD_PARTY_NOTICES.md` is required for that skill
- Linked in `[[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]]` to the original source repository `agent-smith`, with copyright attributed to Romain Monier for 2026
- Reinforced in the README's licensing section as part of the repo-wide split between code, documentation, vendored tools, and internal working context

## Related Concepts

- [[concepts/apache-license-2-0]]
- [[concepts/license-compliance-requirements]]
- [[concepts/permissive-open-source-licensing]]
- [[concepts/attribution-based-reuse]]
- [[concepts/clean-room-reimplementation]]
- [[concepts/compatibility-fallback]]
- [[concepts/provenance-tracking]]
- [[concepts/source-provenance]]
- [[concepts/license-conditions]]
- [[concepts/licensing-and-attribution]]
- [[concepts/open-source-attribution]]
- [[concepts/split-licensing]]
- [[concepts/instruction-file-aliasing]]
- [[concepts/local-only-repo-artifacts]]
- [[concepts/symlink-fallback]]
- [[concepts/git-tracking-policy]]
- [[concepts/context-surface-management]]
- [[concepts/knowledge-compilation-pipeline]]
- [[concepts/progressive-disclosure]]
- [[concepts/agent-ready-context]]
- [[concepts/agent-ready-repositories]]
- [[concepts/portable-skill-contract]]
- [[concepts/skill-vendoring]]
- [[concepts/toolchain-pinning]]

## Notes

- The Apache 2.0 text defines the standard rights to reproduce, prepare derivative works, publicly display and perform, sublicense, and distribute the work.
- It includes an explicit patent license from contributors, with termination if patent litigation is initiated over the work or a contribution.
- Redistribution must include the license copy, modified-file notices, retained attribution notices, and any required NOTICE file content.
- The upstream fallback provenance records the Apache-2.0 license, copyright attribution to Vectify AI, and the exact upstream source and release used for verification.
- `[[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]` documents the copied or closely adapted passages, upstream sources, and the notice rationale for the embedded fallback.
- The notice also records that most of `SKILL.md` is independent expression, with only three short passages considered close enough to upstream wording to warrant attribution.
- The license is used here to support code reuse while keeping provenance and attribution explicit.
- The fallback is described as a best-effort degradation path that affects only `--brief` wording, not `editorial_pass.py --check` correctness gates.
- The licensing file for `[[entities/skill-creator]]` also states that the complete license texts are available under `LICENSES/`.
- The skill-creator notice explicitly attributes the directory to Romain Monier and points to the original `rmonier/agent-smith` repository.
- `scripts/init_skill.py` carries Apache-2.0 headers and is presented as repository source staged for OpenKB ingestion, reinforcing the license's role in downstream knowledge capture.
- `scripts/ensure_local_alias.py` follows the same Apache-2.0 lineage and adds a cross-platform local alias mechanism for harness-specific instruction-file discovery.
- `scripts/ensure_local_alias.py` also demonstrates a local-only artifact pattern by updating `.git/info/exclude` so the alias stays out of version control by default.
- `[[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]` further clarifies that no notice was recorded for `superpowers`' `writing-skills` because no licence file was found and no closely tracked passage was identified.
- The staged license file for `[[entities/subagent-profile-adapter]]` is a direct copy of the canonical Apache 2.0 text, so its main wiki contribution is confirmation of the license's authoritative wording rather than new substantive terms.

## Related Documents
- [[summaries/README-md]]

- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/agents__skills__skill-creator__LICENSING-md]]
- [[summaries/agents__skills__agent-ready-context__LICENSING-md]]
- [[summaries/agents__skills__agent-ready-context__THIRD_PARTY_NOTICES-md]]
- [[summaries/agents__skills__skill-creator__LICENSES__Apache-2-0-txt]]
- [[summaries/agents__skills__subagent-profile-adapter__LICENSES__Apache-2-0-txt]]
- [[summaries/agents__skills__subagent-profile-adapter__LICENSING-md]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]

See also: [[summaries/agents__skills__agent-ready-context__NOTICE]]

See also: [[summaries/agents__skills__subagent-profile-adapter__LICENSES__CC-BY-4-0-txt]]
