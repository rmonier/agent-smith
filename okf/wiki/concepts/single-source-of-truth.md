---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md"]
description: "One canonical artifact governs authority while other files stay derived."
---

# Single Source of Truth

Single source of truth is the practice of designating one canonical artifact as the authoritative version of some information, then making all local aliases, adapters, or derived forms refer back to that artifact rather than duplicating its content.

## Core Idea

A system follows this pattern when it answers two questions clearly:
- which file or document is authoritative
- how other tools, harnesses, or environments should reference it without creating competing copies

This reduces drift, keeps updates centralized, and makes maintenance more predictable. It also supports documentation architecture by separating canonical content from local integration details and aligns with agent context layering by keeping durable context distinct from runtime-specific projections.

A stronger version of the pattern appears when the canonical artifact is paired with explicit boundary rules: durable project knowledge stays in one place, while runtime-specific files remain thin access layers. In that form, single source of truth is not just about avoiding duplication; it is also about preserving knowledge boundaries and preventing generated runtime files from being mistaken for project truth.

The agent-ready-context guidance sharpens this further. Repository knowledge should live in the OKF wiki at `okf/wiki/`, staged source packs should be rebuilt deterministically under `okf/.okf-build/input/`, and generated output should not be written directly into `okf/raw/` or `okf/wiki/`. `AGENTS.md` remains the canonical orientation file, while harness-specific files stay local projections. The lifecycle guidance also treats the hash registry and compiled wiki as one unit: registry drift can silently suppress repairs, so a single source of truth must include both the canonical source set and the ingest state that tracks it.

## How the Source Document Illustrates It

[[summaries/agents__skills__subagent-profile-adapter__SKILL-md]] defines the governing rule: `AGENTS.md` remains the canonical orientation file even when a harness requires some other local instruction file, profile entry point, or harness-native adapter.

The skill treats harness-specific adapters as secondary projections of existing repository context rather than independent sources of truth. It instructs the agent to:
- keep `AGENTS.md` authoritative for orientation
- treat `okf/wiki/` as the durable project knowledge base
- derive subagent or profile adapters from existing repository context and skills
- create a local alias only when the active harness requires another file
- prefer a symlink to `AGENTS.md` before considering other compatibility mechanisms
- keep generated adapter files short and have them point back to `AGENTS.md`, `okf/wiki/`, and relevant skills instead of embedding duplicated project context

The document makes this rule broader than file aliasing alone. It frames subagent and profile adapters as runtime-specific projections that must never become the durable source of repository knowledge. That connects single source of truth to runtime adapter management, tooling context isolation, and harness native profiles.

[[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] is a direct implementation of this concept.

The script treats `AGENTS.md` as the canonical instruction file and creates a harness-specific local alias only when needed. Instead of generating a second independently maintained instruction document, it does one of two things:
- creates a relative symlink to the canonical file
- writes a small pointer file that explicitly tells readers to use the canonical file

In both cases, the local alias exists only as an access mechanism. The actual content authority remains in one place. This is a concrete example of harness-native profiles being handled without fragmenting repository guidance.

The newer agent-ready-context lifecycle extends the same pattern into the KB pipeline itself. It treats the OKF wiki under `okf/wiki/` as the durable context source of truth, requires deterministic staging under `okf/.okf-build/input/`, and forbids generated output from being written directly into `okf/raw/` or `okf/wiki/`. It also reserves a narrow hand-edited namespace for tooling pages and findings, while keeping the compiled wiki as the authoritative context surface. That preserves a single authoritative project context layer even when harness-specific evidence is recorded, reinforcing link directionality and tooling navigation exceptions.

## Why It Matters

Using a single source of truth helps prevent several common failures:
- duplicated instructions diverge over time
- harness-specific files become accidentally authoritative
- users update the wrong file
- repository policy gets mixed with local tooling requirements
- generated adapters start carrying stale copies of project context
- tooling documentation begins to influence project concepts in the wrong direction
- compiled KB pages get edited directly instead of being regenerated from staged sources
- registry drift causes future ingests to skip documents that should have been repaired

The source material addresses these risks by defining adapters as runtime-specific outputs, not canonical knowledge artifacts. It also defaults to local-only handling for harness-specific files unless a user or repository policy says otherwise, tying this concept closely to local-vs-shared configuration, runtime adapter management, and safe automation.

The document also shows that single source of truth depends on correct runtime identification. If an agent guesses the wrong harness based only on installed tools, it may generate the wrong adapters and create competing local conventions. That is why the workflow emphasizes harness-vs-local-tools, runtime-signal-prioritization, and runtime-ambiguity-resolution before any adapter is written.

The agent-ready-context skill adds another important dependency: it treats `okf/.openkb/hashes.json` as a dedupe registry whose drift can silently suppress future ingests. Maintaining a single source of truth therefore requires not just one canonical file, but also a coherent ingest registry and a disciplined correction loop when wiki output is weak or wrong.

## Mechanisms That Support the Pattern

### Canonical file designation

The skill explicitly states that `AGENTS.md` remains the canonical orientation file. The aliasing helper then validates that the source file exists before doing anything else. This ensures the adaptation flow starts from a real authoritative artifact. More broadly, the document distinguishes canonical orientation, durable wiki context, reusable skills, and runtime adapters so each layer has a clear role rather than overlapping authority.

### Indirection instead of duplication

A symlink preserves exact identity with the source file. When symlinks are unavailable, the pointer file still preserves conceptual authority by directing readers back to the original file rather than copying its contents. At the profile level, the skill applies the same principle by keeping adapter files short and having them reference canonical repository context instead of restating it. This is also a form of graceful degradation.

### Runtime-specific adaptation

The skill frames subagent and profile files as harness-native adapters generated for the active runtime only. They are intentionally projections of existing context, not new primary documents. It also warns against hardcoded vendor renderers and requires using current documentation to implement native formats directly. That preserves authority centrally while still supporting runtime integration, which connects this concept to tool boundaries, context-action separation, and spec authority.

### Local-only adaptation

The alias path is intended for a specific harness requirement, but the script avoids encoding vendor-specific rules. The broader skill likewise asks the user how generated files should be tracked and defaults to local-only handling when no team policy exists. The adaptation remains optional and scoped, while the canonical document remains stable for the repository as a whole. This also aligns with generated artifact adoption and generated content governance.

### Safety boundaries

The script requires the alias to stay inside the repository, refuses unsafe replacements, and recognizes an already-correct alias as success. The skill adds another boundary by prohibiting large copies of wiki or project content inside profile files, requiring validation of adapter placement, and checking that project pages do not link back into harness tooling context. Together these checks reinforce path safety, filesystem validation, and deterministic validation while protecting the canonical source from accidental replacement or dilution.

### KB pipeline authority

The agent-ready-context workflow extends the same idea to the wiki build pipeline. It stages deterministic input first, ingests through OpenKB, then reviews generated pages before accepting them. If generated pages are weak, duplicated, or misclassified, the correction loop should happen in source documents and staged inputs rather than by hand-editing compiled wiki pages. That keeps compiled knowledge derivative and preserves a single authoritative input path.

## Relationship to Other Concepts

Single source of truth often works together with:
- [[concepts/documentation-source-priority]], when multiple candidate references exist but one must be authoritative
- [[concepts/local-vs-shared-configuration]], when local adapters should not become shared repository policy
- [[concepts/cross-platform-tooling]], when different environments need different access methods to the same source
- [[concepts/runtime-adapter-management]], when harness-native files must stay derived rather than canonical
- [[concepts/safe-automation]], when tooling must preserve authority without risking accidental overwrite
- [[concepts/tooling-context-isolation]], when runtime-specific knowledge must remain separate from durable project context
- [[concepts/link-directionality]], when navigation exceptions must not become dependency reversals
- [[concepts/documentation-cohesion]], when multiple supporting artifacts should still resolve back to one authoritative center
- [[concepts/hash-registry-coherence]], when ingestion state must stay aligned with the canonical source set
- [[concepts/source-driven-regeneration]], when compiled output must remain downstream of staged source material
- [[concepts/registry-drift]], when stale registry entries can silently prevent repair of missing wiki output
- [[concepts/okf-workflow-governance]], when the KB lifecycle needs a clear authority model across staging, ingest, and validation

## Practical Takeaway

When a tool, harness, or environment requires a special filename, profile, or alternate entry point, the preferred solution is usually not to create a second maintained copy. Instead, keep one canonical artifact and make the environment-specific layer point back to it.

That is the pattern demonstrated by [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]] and [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]]: adapt access locally, preserve authority centrally.

The newer agent-ready-context material sharpens that takeaway: not only should the canonical file remain singular, but surrounding tooling pages, harness notes, and generated profiles must also preserve the same authority structure. Runtime adapters may exist, but they should stay thin, documented, validated, and clearly subordinate to the repository's canonical context. In the OKF workflow, that means the staged source pack, the hash registry, the compiled wiki, and `AGENTS.md` all serve the same authority chain rather than competing with it.

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py]]