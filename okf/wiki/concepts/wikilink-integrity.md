---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py.md", "summaries/README-md.md", "summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/graphify-report.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md"]
description: "Ensures internal wiki links resolve to valid, policy-compliant pages."
---

# Wikilink Integrity

Wikilink integrity is the requirement that internal `wikilinks` in an OpenKB-style wiki resolve to real, allowed pages inside the compiled wiki graph. In this repository's validation model, broken wikilinks are treated as a producer-side quality failure rather than a harmless formatting issue. The concept is grounded in the offline OKF quality baseline, the OpenKB wiki schema, repository-local validation, and the maintenance rules that keep navigation consistent across page creation, indexing, and tooling boundaries.

## Why it matters

Reliable wikilinks make the wiki navigable, machine-checkable, and safe to regenerate. When links resolve consistently, agents can follow context across pages without guessing whether a missing target is intentional, stale, or the result of an interrupted update.

This is especially important in systems built for [[concepts/durable-context]], where the wiki acts as long-lived operational memory, and for [[concepts/deterministic-validation]], where the same content should validate the same way every time.

The compiled wiki is not just a pile of notes; it is a managed navigation surface made up of `index.md`, `summaries/`, `concepts/`, `entities/`, and `explorations/`, with `sources/` holding imported material. Wikilinks are expected to resolve within that surface. Because the wiki is meant to be both human-browsable and tool-readable, link failures damage discovery, synthesis, and automated maintenance at once.

Wikilink integrity also supports source-backed maintenance: if internal links are guaranteed to resolve, repository-wide updates, page moves, regeneration passes, and newly added tooling context pages are easier to validate automatically before damaged context spreads. The harness documentation workflow reinforces this by requiring tooling pages to be represented correctly in the wiki index, tying link correctness to broader tooling-context maintenance.

The tooling link policy sharpens that boundary further. It allows pages under `okf/wiki/tooling/` to link outward to project pages, but it forbids project OKF concept pages and most indexes from linking back into tooling. The bundle-root `index.md` and `log.md` are exempt because they serve navigation and history roles, and when tooling contains non-reserved pages, the root `index.md` must reference `tooling/` in a clearly labeled harness-specific section. That policy keeps speculative or user-scoped tooling pages out of the compiled project graph while still preserving discoverability.

In other words, wikilink integrity is not only about whether a target exists, but whether the target belongs in the compiled knowledge graph at all.

## OKF baseline vs OpenKB policy

The OKF quality baseline described in [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]] says consumers should tolerate broken standard Markdown cross-links. That tolerance exists because a knowledge bundle may be partially generated or still under construction.

OpenKB applies a stricter rule for `wikilinks`. In `--openkb-wiki` validation mode, broken wikilinks are errors. The validator described in [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] makes that explicit: OpenKB operational areas such as `sources/`, `reports/`, and root `AGENTS.md` are excluded from page validation, but the wiki pages that remain are expected to maintain valid internal links.

The same validator also broadens integrity checks beyond link resolution. It warns on unclosed code fences, which helps catch truncated or badly merged pages, and it warns when sibling page names collapse to the same normalized slug, which helps surface near-duplicate concepts before navigation drifts. Those checks make wikilink integrity part of a wider [[concepts/deterministic-validation]] and [[concepts/graph-integrity-diagnostics]] posture rather than a narrow syntax check.

The wiki schema sharpens this distinction by defining a compiled wiki tree with explicit page classes and Obsidian-compatible link forms. In that model, a wikilink is not just presentation syntax; it is part of the repository's navigational contract.

The harness tooling workflow adds another repository-local expectation: when a harness-specific tooling page is created, the wiki index must also be updated so the new area is represented correctly. The tooling link policy makes that more specific by requiring a committed `tooling/index.md` stub whenever `okf/wiki/tooling/` contains non-reserved pages, and by requiring the bundle-root `index.md` to enumerate tooling as a harness-specific exception whenever local tooling exists. This means missing or unregistered link structure can be a validation problem even when the page content itself is present.

In practice, this creates a useful separation:

- OKF conformance defines the minimum bundle rules.
- OpenKB validation adds stronger local [[concepts/quality-gates]].
- Wikilinks are validated as part of repository integrity, not merely display formatting.
- Index-declared tooling areas help ensure new pages remain discoverable and policy-compliant.
- Local tooling pages remain outside project truth, so project pages must not depend on them.

## What counts as a broken wikilink

A wikilink is broken when it points to a page that does not exist in the managed wiki target set. In the validator implementation, that target set is built from every Markdown file's wiki-relative path without extension and its bare stem, so links can resolve either by full wiki-relative name or by page stem.

The validator also strips any `|alias` suffix and trims surrounding slashes before checking targets. This means a broken wikilink is not just a malformed string; it is a link whose normalized target still cannot be matched to any known page.

The schema document adds an operational expectation on top of that: links in the wiki should resolve after maintenance tooling runs, and broken links generally indicate hand-editing, an in-progress update, or interrupted maintenance rather than an accepted steady state.

In an OpenKB-managed workflow, that usually signals one of a small number of failures:

- a bad manual edit;
- a merge conflict resolved incorrectly;
- a page rename without link repair;
- an interrupted generation or lint run;
- a newly added page that was not integrated into index or policy-tracked navigation.

Because the source documents describe wikilinks as managed against a compile-time target set and checked automatically, a broken wikilink is treated as evidence of damage, not as an acceptable placeholder. The harness tooling guidance sharpens this further by showing that page creation alone is not enough; required index references must also be maintained to preserve navigability and validation health.

The tooling link policy adds a second class of target failure: a link can be technically resolvable but still inappropriate if it points into user-scoped tooling from project-side content, or if it points to a local page that should not be committed or enumerated from the wrong index. That makes wikilink integrity a question of both existence and directionality.

The validator's target set is intentionally broad but mechanical: every `.md` file contributes both its wiki-relative path without extension and its bare stem. That makes the resolution rule predictable, but it also means naming collisions and inconsistent page moves can create subtle integrity problems even when content still exists somewhere in the tree.

## Relationship to validation

The source documents place wikilink integrity inside `--openkb-wiki` validation behavior. That mode narrows validation to the wiki areas intended to obey OpenKB conventions, then layers additional checks beyond baseline OKF rules.

The validator also ignores fenced code blocks and inline code while scanning for wikilinks. This matters operationally: examples, snippets, or literal `target` text in code should not trigger false link failures. As a result, wikilink integrity is enforced as a content-structure rule rather than a naive text-pattern rule.

The same script treats parseability as a prerequisite for structural checks. If PyYAML is unavailable, YAML validation degrades rather than pretending the file is fine, which keeps the validator honest about its confidence level. That design fits the broader [[concepts/graceful-degradation]] pattern: it reports what it can verify and flags when a dependency blocks full validation.

The wiki schema complements this by describing which parts of the compiled artifact are meant to participate in internal navigation. `sources/` exists for converted source material, including page-indexed JSON for long PDFs, but navigational integrity is centered on the Markdown page graph represented by summaries, concepts, entities, explorations, and `index.md`. That makes link checking part of preserving a coherent compiled wiki rather than validating every stored artifact equally.

The harness documentation workflow shows that validation is not limited to per-page parsing. It also includes repository-structure expectations: tooling pages for harnesses must be summarized concisely, indexed in the proper section, and recorded in the log so that the wiki remains coherent as it evolves. In that sense, wikilink integrity participates in both direct target resolution and broader [[concepts/okf-validation]] behavior.

This makes wikilink integrity part of a broader validation strategy that also includes:

- spec-aware checking based on [[concepts/spec-authority]];
- offline execution support through [[concepts/offline-first-workflows]];
- reproducible repository checks through [[concepts/deterministic-validation]];
- filesystem-aware repository checks through [[concepts/filesystem-validation]];
- stronger local enforcement through [[concepts/quality-gates]].

## Relationship to editorial curation

Wikilink integrity is not only a validation concern; it is also a curation concern. The guarded editorial pass script exists because some accepted changes, such as merges and concept-sprawl consolidation, do not have a dedicated OpenKB command. Its job is to make last-resort hand edits safe by combining vendor checks with git-based policy invariants.

That script's `--brief` mode loads the agent with the live whitelist of valid wikilink targets from the installed OpenKB package. It uses the same whitelist middleware OpenKB injects into generation calls, and it can extend the allowed set with approved new page slugs for splits. This keeps the editing agent aligned with the same target rules that later validation will enforce.

Its `--check` mode then verifies the completed diff deterministically and without LLM involvement. It checks vendor failures such as broken links, stale index entries, orphaned pages, invalid frontmatter, and missing OKF fields, then adds local policy checks for scope, provenance, allowed new pages, and non-empty `sources:` lists on changed concept/entity pages.

This creates a direct operational link between wikilink integrity and [[concepts/editorial-curation-passes]]:

- curation must preserve target validity, not just content meaning;
- merges must rewire inbound links to the survivor page;
- deleted or renamed pages must be reflected in the root index;
- allowed new compiled pages require explicit approval;
- provenance lists must remain complete on touched compiled pages.

## Relationship to citations and standard links

Wikilink integrity should not be confused with external citation quality or ordinary Markdown linking. The source material separately allows claims to cite URLs, bundle-relative paths, or reference documents, aligning with [[concepts/knowledge-linking-and-citations]].

The important distinction is:

- standard Markdown links may be tolerated even when broken under the baseline OKF model;
- internal `wikilinks` are a managed OpenKB convention and are expected to resolve;
- policy-tracked wiki navigation, such as index entries for tooling pages, is part of maintaining those managed internal relationships.

The schema also makes the scope of those managed relationships more concrete by standardizing where summaries, concepts, entities, and explorations live and how wikilinks map onto those paths. This difference supports strict internal navigation without weakening compatibility with broader document ecosystems or [[concepts/external-documentation]].

## Operational implications

Treating broken wikilinks as errors improves trust in the wiki as a working system. It helps preserve navigation structure, reduces silent drift, and supports source-backed regeneration workflows. It also makes the wiki easier for agents to use safely, since unresolved links are surfaced immediately instead of being interpreted as partial context.

The validator's implementation reinforces this by making wikilink checking deterministic and repository-wide: it computes a stable set of valid targets from the current Markdown tree, skips excluded operational files, and fails the run when a scanned page links to a nonexistent target.

Its near-duplicate slug warning adds another operational benefit: link integrity is preserved not only by checking whether targets exist, but also by discouraging page name collisions that can confuse human navigation and future link maintenance. Together with the unclosed-fence warning, this turns the validator into a lightweight integrity sweep for the compiled graph.

The schema adds a discovery dimension to the same idea. `index.md` is the top-level catalog for documents, concepts, entities, and explorations, with persistent sections and one-line descriptions. When links and index entries are both maintained, the wiki stays both resolvable and discoverable; when either drifts, the page graph becomes harder for humans and tools to trust.

The harness tooling guidance extends the operational picture: when new harness reference pages are added, they should be summarized into concise tooling context pages, listed in the appropriate index section, and recorded in the log. The tooling link policy narrows that further by saying the committed stub is user-neutral, local pages stay user-scoped, and every local tooling page should still link outward to durable project knowledge so it is not an orphan. This reduces the risk that valid standalone pages become effectively invisible or policy-invalid because surrounding navigation was not updated.

In operational terms, wikilink integrity supports:

- stable cross-page navigation;
- safer regeneration and refactoring;
- earlier detection of damaged knowledge graphs;
- clearer boundaries between valid context and missing context;
- stronger consistency between page creation, indexing, validation, and tooling isolation.

These benefits reinforce [[concepts/documentation-architecture]] and the OpenKB emphasis on machine-checked, durable knowledge under [[entities/openkb]].

## Source grounding

The main source for this concept is [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]], which explains that broken `wikilinks` are errors in OpenKB validation mode even though broken standard Markdown cross-links are tolerated under baseline OKF consumer behavior.

[[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] adds implementation detail: wikilink targets are resolved from page paths and stems, `|alias` text is ignored, code spans and fenced blocks are excluded from scanning, broken wikilinks fail validation in `--openkb-wiki` mode, and the same pass also warns about unclosed code fences and slug-colliding sibling pages.

[[summaries/agents__skills__openkb__references__wiki-schema-md]] adds structural context: the compiled wiki tree is organized into summaries, concepts, entities, explorations, sources, index, and log; wikilinks use Obsidian-compatible forms; and maintenance tooling is expected to leave links in a resolvable state.

[[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]] adds maintenance context: harness tooling pages must be summarized sparingly, placed in a dedicated tooling path, reflected in `index.md`, and recorded in `log.md`; otherwise policy validation can fail even when the page content itself is present.

[[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]] adds a stricter boundary for local tooling knowledge: harness and adapter context are allowed only in constrained cases, tooling content stays user-scoped by default, the committed stub is neutral, and project pages must not depend on local tooling pages.

The guarded curation pass implementation in [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]] reinforces the same idea from the maintenance side. Its `--brief` mode loads the live vendor wikilink whitelist, and its `--check` mode enforces scope, provenance, allowed-page creation, and vendor structural checks. That script makes wikilink integrity part of a broader editorial curation workflow rather than a one-off lint rule.

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/graphify-report]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]

See also: [[summaries/README-md]]

## Updated OKF baseline

The embedded OKF v0.1 quality baseline reinforces the same integrity model: a bundle is a UTF-8 Markdown directory tree, non-reserved `.md` files need parseable YAML frontmatter, and `index.md`/`log.md` are reserved navigation files. In that baseline, standard Markdown cross-links may be broken without violating conformance, but OpenKB's `--openkb-wiki` mode intentionally tightens the local quality bar for `wikilinks` and related wiki-graph checks.

That baseline also clarifies why integrity must be understood at two levels. OKF conformance is about the minimum structure a bundle must satisfy, while OpenKB wiki validation adds repository-specific rules for navigation, page classes, and local tooling separation. Wikilink integrity sits at the overlap of those layers: it is a structural rule for the compiled wiki graph, and it is also a practical maintenance rule for keeping the bundle useful offline.

The baseline further shows that bundled knowledge is meant to be portable across transports such as Git, archives, and plain directories. Because the target may be copied or regenerated offline, link correctness cannot rely on external services. That makes deterministic local resolution a core requirement rather than a convenience.

In the same baseline, tooling is explicitly treated as a local-by-default concern in this repository policy, but the bundle root index must still enumerate it so the wiki remains navigable. This strengthens the core lesson of wikilink integrity: navigation only works when the page graph, the index, and the validation model are all kept in sync.

## Related Documents
- [[summaries/agents__skills__agent-ready-context__scripts__editorial_pass-py]]
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]