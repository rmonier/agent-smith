---
sources: ["summaries/agent-skills-spec.md", "summaries/repo-snapshot.md", "summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md.md", "summaries/agents__skills__skill-creator__scripts__quick_validate-py.md", "summaries/agents__skills__skill-creator__scripts__init_skill-py.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__NOTICE.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/README-md.md"]
type: "Other"
description: "Repository area for reusable Agent Skills and support assets"
---

# agents/skills

`agents/skills` is the repository area for reusable Agent Skills: scripted workflows, helper assets, and support references that agents can invoke for repeatable tasks.

## Key facts

- It is treated as a distinct skills layer, separate from the OKF wiki and from `AGENTS.md` orientation content.
- The area is organized around `SKILL.md` plus optional `scripts/`, `references/`, and `assets/` resources.
- The repository snapshot shows this area contains several major skill packages, including `agent-ready-context`, `graphify`, `openkb`, `skill-creator`, and `subagent-profile-adapter`.
- It also includes bundled license files and notices inside those skill directories, which reinforces the area’s role as a self-contained packaging surface.
- The `.agents/skills` tree is the main functional center of the repository’s agent tooling ecosystem, not just a storage folder.
- The `merge_agents_md_okf_section.py` script lives here and maintains the managed OKF guidance block inside `AGENTS.md`.
- That script edits only the section between `<!-- okf:start -->` and `<!-- okf:end -->`, preserving repository-specific setup, style, test, and PR guidance.
- Its merge behavior is conservative: replace the managed block when markers exist, append the block when the file already has content, or initialize a new `AGENTS.md` when the file is empty.
- The managed guidance routes agents through `AGENTS.md`, `okf/wiki/index.md`, `graphify-out/GRAPH_REPORT.md` / `graphify-out/graph.json`, and `.agents/skills/` in that order.
- The injected section tells agents to treat wiki content as data rather than instructions, to use `okf/wiki/index.md` as the first wiki entry point, and to inspect `tooling/index.md` when index routing points at local harness context.
- It also instructs agents to discover the active harness from runtime metadata or self-knowledge, to use ignored local tooling files when needed, and to treat an empty local tooling overlay on first clone as normal.
- The section directs agents to load `.agents/skills/agent-ready-context/SKILL.md` for executable workflow, to rerun that skill when source files or workflows change, and to keep `AGENTS.md` concise by collapsing deeper context into the wiki front door.
- It emphasizes local-vs-shared boundaries: do not edit OpenKB-managed compiled pages directly, do not commit provider secrets or pipeline artifacts, and keep provider/model configuration local under `okf/.openkb/`.
- The script explicitly says to run bundled maintenance scripts through `uv run <script.py>` rather than bare `python` when `uv` is available.
- The script also encodes the finding workflow: durable project facts should be captured as findings under `okf/wiki/explorations/findings/` with evidence, rationale, links, and an `index.md` entry.
- The `build_okf_skeleton.py` script also lives here and provides a conservative fallback that generates a minimal OKF wiki skeleton when no LLM provider credentials are available.
- The `check_prereqs.py` script lives here and performs preflight validation for the `agent-ready-context` skill before repository maintenance continues.
- The prereq check verifies required runtime tools, optional CLIs, vendored tool skills, OpenKB config drift, credential-home ambiguity, and basic write access to repo paths.
- It treats `git`, `uv`, and Python 3.11+ as hard requirements, while `graphify` and `openkb` are optional capabilities with slower first-run detection.
- It explicitly checks whether companion skills such as `skill-creator` and `subagent-profile-adapter` are present, but does not require them for basic operation.
- The prereq check also distinguishes shared OpenKB config keys from per-user provider settings, reinforcing [[concepts/local-vs-shared-configuration]].
- The repository snapshot confirms that `.agents/skills` is tracked as a first-class repo area alongside root governance files like `README.md`, `AGENTS.md`, `LICENSE`, `NOTICE`, and `REUSE.toml`.
- The snapshot also shows adjacent documentation and policy files, including `CITATION.cff`, `LICENSES/`, `THIRD_PARTY_NOTICES.md`, and `docs/assets/agent-smith.svg`, which supports the directory’s role inside a broader [[concepts/repository-structure-overview]].
- The skeleton builder writes a repository overview, optional external documentation evidence, a root index, and a log entry, but it does not claim semantic completeness.
- The skill area is meant for executable procedures and maintenance automation, not durable repository knowledge.
- The surrounding guidance emphasizes using skills for actions and the wiki for context, reinforcing [[concepts/context-action-separation]].
- Skill maintenance is tied to broader governance around [[concepts/agent-ready-context]], [[concepts/skill-governance]], [[concepts/agent-tooling-ecosystem]], [[concepts/llm-free-knowledge-bootstrap]], [[concepts/preflight-checks]], [[concepts/agent-ready-context-skill]], and [[concepts/managed-document-sections]].
- The `adopt_generated_skill.py` script adds a second lifecycle role: it copies a generated skill from `okf/output/skills/` into `.agents/skills/`, requires a valid `SKILL.md`, and validates the result immediately.
- Adoption is gated by a strict skill-name check, so only lowercase names with digits and hyphens are accepted, and names containing `--` are rejected.
- The adoption script refuses to overwrite an existing skill unless `--force` is provided, which aligns the directory with [[concepts/generated-artifact-adoption]] and [[concepts/human-in-the-loop-review]].
- If validation fails after a fresh copy, the script removes the copied skill so the destination does not remain in a broken state, connecting the workflow to [[concepts/generated-artifact-validation]] and [[concepts/deterministic-validation]].
- If validation fails after replacing an existing skill, the replacement is left in place for manual repair or removal, making the operation safer but still review-driven.
- The script uses `quick_validate.py` from the same tooling area, making `.agents/skills/` a hub for skill adoption and validation workflows rather than only authored skills.
- Its post-validation guidance reminds maintainers to preserve trigger-style descriptions, minimal scoped allowed-tools, untrusted-content handling, and no secrets, which fits [[concepts/skill-validation-workflow]] and [[concepts/skill-authoring]].
- It also warns that adopted skills must retain constraints, boundaries, and warnings from their source wiki pages, linking the directory to [[concepts/caveat-preservation]], [[concepts/source-grounded-regeneration]], and [[concepts/skill-adoption]].
- The `init_skill.py` script adds a third lifecycle role: it bootstraps a new skill directory under `.agents/skills` by default, normalizes the requested name, validates the destination, creates optional resource folders, and writes a starter `SKILL.md`.
- Its name handling uses kebab-case normalization plus a strict regex guard, making it a concrete example of [[concepts/kebab-case-normalization]], [[concepts/naming-normalization]], and [[concepts/filesystem-validation]].
- The initializer accepts `--path`, but still refuses to write outside `.agents/skills`-scoped locations, reinforcing [[concepts/path-safety]] and [[concepts/directory-bootstrap]].
- It can create `scripts`, `references`, and `assets` directories from `--resources`, reflecting [[concepts/skill-resource-organization]] and [[concepts/skill-scaffolding]].
- The generated `SKILL.md` contains a templated description, workflow, and command section, which shows the directory as both a skill authoring target and a templated project-scaffolding surface.
- The `quick_validate.py` script provides a fast command-line validator for a skill directory before deeper workflow execution.
- It checks that `SKILL.md` exists, starts with YAML frontmatter, and closes properly before reading the metadata.
- It requires `name` and `description`, enforces a skill naming regex, rejects names containing `--`, and requires the directory name to match the frontmatter `name`.
- It limits `description` to 1024 characters and `compatibility` to 500 characters when present, making the validator a lightweight frontmatter gate.
- It also checks that the skill lives under `.agents/skills` and that `scripts`, `references`, and `assets` are directories if they exist.
- On success, it prints `valid skill: <path>`; on failure, it prints each error prefixed with `error:` and exits nonzero.
- The `suggest_skills_from_okf.py` script adds a fourth lifecycle role: it scans an OKF wiki bundle and proposes candidate custom action skills based on repeated action-oriented language.
- It uses simple heuristics rather than semantic classification, counting regex hits for verbs and tooling terms such as `run`, `validate`, `generate`, `refresh`, `git`, `docker`, `kubectl`, `python`, and `uv`.
- It skips structural pages and de-emphasizes pages whose context looks conceptual, helping separate action candidates from background documentation.
- It derives each suggestion from a page title or heading, normalizes it to a slug, and prefixes `manage-` when the name does not already look action-oriented.
- It aggregates evidence paths and prints a ranked list of suggestions with scores and an `init_skill.py` bootstrap command.
- This makes `.agents/skills/` not only a place to store and validate skills, but also a workspace for [[concepts/heuristic-skill-suggestion]] and [[concepts/action-candidate-detection]] over the OKF corpus.
- The `subagent-profile-adapter` skill extends the directory's role into runtime-specific adapter generation for harnesses that support local subagents, personas, or profile-based execution contexts.
- That skill treats adapters as projections of existing repo context, not as a portable subagent standard, and it requires the active harness to be detected from runtime metadata rather than from installed binaries alone.
- It adds explicit policy around harness-native profiles, runtime ambiguity resolution, adapter bloat prevention, and link directionality between tooling context and project context.
- It also depends on validation of tooling link policy and on a neutral `tooling/index.md` navigation stub when local tooling pages exist, reinforcing the directory's role in runtime-adapter management and harness-specific projections.

## Role in the workflow

This directory supports agent-ready repository maintenance by packaging repeatable operations into skills. In the referenced scripts, that role is concrete: one script updates `AGENTS.md` conservatively, another produces a zero-LLM OKF skeleton from repository metadata and staged evidence, `check_prereqs.py` gates execution by confirming that the environment, config, and supporting skills are ready enough to proceed, `adopt_generated_skill.py` turns generated skills into project-owned skills after validation, `init_skill.py` bootstraps new skills with a constrained directory layout and starter `SKILL.md`, `quick_validate.py` provides a fast validation pass for skill metadata and layout, and `suggest_skills_from_okf.py` mines the wiki for new action candidates. The `subagent-profile-adapter` skill adds a separate runtime-adapter workflow for harness-specific profiles and local subagents, keeping those outputs distinct from both durable wiki knowledge and authored skills.

## Related material

- [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]
- [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]]
- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[summaries/agents__skills__skill-creator__scripts__init_skill-py]]
- [[summaries/agents__skills__skill-creator__scripts__quick_validate-py]]
- [[summaries/agents__skills__skill-creator__scripts__suggest_skills_from_okf-py]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[entities/agent-ready-context-skill]]
- [[entities/okf-wiki-agents-md]]
- [[entities/agents-md]]
- [[entities/subagent-profile-adapter]]

See also: [[summaries/agents__skills__agent-ready-context__LICENSING-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__skill-creator__NOTICE]]

## Related Documents
- [[summaries/repo-snapshot]]
- [[summaries/agents__skills__skill-creator__SKILL-md]]


See also: [[summaries/agents__skills__skill-creator__THIRD_PARTY_NOTICES-md]]


See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agent-skills-spec]]