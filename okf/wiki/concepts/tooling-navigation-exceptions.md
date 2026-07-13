---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md"]
description: "A narrow carve-out letting reserved wiki navigation files point into tooling."
---

# Tooling Navigation Exceptions

Tooling navigation exceptions are narrowly defined allowances that let reserved wiki navigation files point into tooling-specific context without breaking the broader separation between project knowledge and harness-specific material. The goal is to preserve discoverability while maintaining [[concepts/tooling-context-isolation]] and link direction rules.

## Core idea

In a wiki that separates general project content from tooling-specific pages, most links from project pages back into tooling context are treated as forbidden dependencies. A tooling navigation exception creates a limited carve-out for pages whose role is navigation or history rather than substantive project documentation.

This prevents the wiki from becoming stranded or undiscoverable while still preserving [[concepts/knowledge-boundaries]] and [[concepts/tool-boundaries]]. It also supports the broader policy that harness-specific runtime artifacts and profile adapters should stay local by default, using `.git/info/exclude` rather than shared repository ignores unless the team explicitly chooses otherwise.

## How the concept appears in the source

[[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]] encodes this concept as an explicit policy rule, and [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]] extends the broader OKF framing around reserved files and bundle navigation:

- pages under `okf/wiki/tooling/` may link outward to project pages;
- ordinary project wiki pages must not link back into tooling context;
- the bundle-root `index.md` and `log.md` are exempt from that forbidden direction;
- when tooling contains non-reserved pages, the root `index.md` must include a reference to tooling in a clearly labeled harness-specific section;
- root `index.md` may act as a bundle-navigation surface that is allowed to enumerate tooling without creating a project dependency;
- reserved `index.md` and `log.md` files are navigation and history files, not ordinary concept documents.

This makes the exception structural, not ad hoc. It is allowed only for reserved files with a well-defined navigation role, and only to support bundle usability.

The same source family also defines the adjacent git-tracking policy for harness adapters and tooling context: by default, adapter files are local-only and ignored via `.git/info/exclude`, while the committed `okf/wiki/tooling/index.md` stub is the only shared navigation artifact. The tooling context policy also permits fuller harness documentation only when a detected or user-selected harness is actively in use. That local-default approach mirrors the navigation exception's emphasis on narrow, deliberate carve-outs instead of broad coupling.

## Why the exception exists

Without a navigation exception, a strict isolation policy can make tooling content effectively invisible from the bundle root. That would preserve separation, but at the cost of navigability.

The exception balances two competing needs:

- maintain strong [[concepts/tooling-context-isolation]] separation from normal project documentation;
- preserve [[concepts/index-based-discovery]] for readers who need to find harness-specific material;
- keep the bundle conformant with reserved-file rules and navigation expectations;
- avoid turning navigation links into general-purpose cross-context coupling;
- keep the policy enforceable through [[concepts/executable-validation]] and [[concepts/quality-gates]].

The same reasoning applies to git tracking of generated adapters and tooling pages: keeping them local by default protects the repository from harness-specific noise, while still allowing shared tracking when the team deliberately opts in. Both cases treat exceptions as controlled access paths, not informal convenience.

## Reserved-file scope

The source documents treat root `index.md` and `log.md` as special cases. Their purpose is not to assert project facts about tooling, but to serve as bundle navigation and history surfaces. Because of that role, a link from those pages into tooling is interpreted as sanctioned access rather than a forbidden dependency.

This connects closely to [[concepts/reserved-wiki-files]] and [[concepts/documentation-architecture]]. It also reflects the OKF baseline rule that subdirectory `index.md` files are body-only navigation pages, while the bundle-root `index.md` can carry bundle-level navigation responsibilities.

The git-tracking policy adds a parallel operational rule: adapter files should usually stay out of shared tracking, and if an alias filename is required for a harness, the preferred remedy is a local symlink to `AGENTS.md` added to `.git/info/exclude`. That keeps instruction-file aliases aligned with the reserved-file model instead of turning them into shared repository conventions.

## Required navigation, not optional leakage

An important detail from the source is that the exception is not just permissive; in one case it becomes required. If `okf/wiki/tooling/` contains non-reserved pages, the root `index.md` must link to tooling. A bundle that contains tooling pages but offers no entry point from the root index fails validation.

That requirement reframes the exception as part of the wiki's information architecture rather than a loophole. The exception exists to maintain access paths, not to weaken [[concepts/tooling-context-isolation]]. It also reinforces the OKF idea that consumers should tolerate partial or broken links in general, while OpenKB-specific validation may still enforce stronger local expectations for wiki integrity.

The committed tooling stub is part of the same design: it is user-neutral, stable across clones, and keeps the root index pointing at a target that always resolves, even though the real harness pages stay local. That makes the exception compatible with [[concepts/consent-first-tooling]] and [[concepts/local-tooling-boundaries]].

## Enforcement pattern

The source validator implements this concept through path-based checks:

- it scans Markdown files under the OKF wiki tree;
- it treats files inside `tooling/` differently from ordinary project pages;
- it allows tooling references from root `index.md` and `log.md` only;
- it records whether root `index.md` links to tooling;
- it emits an error if tooling pages exist but root `index.md` does not reference them;
- it relies on the distinction between reserved navigation files and normal concept pages.

This is an example of [[concepts/path-based-validation]], [[concepts/filesystem-validation]], [[concepts/okf-validation]], and [[concepts/quality-gates]]. The same validation mindset also underpins the git-tracking policy: defaults are enforced by repository location and ignore scope, with explicit exceptions only where the harness or team has a clear, documented reason.

## Relationship to neighboring concepts

Tooling navigation exceptions are best understood as a companion to several nearby concepts:

- [[concepts/link-directionality]] defines the default one-way rule;
- [[concepts/tooling-context-isolation]] defines the boundary being protected;
- [[concepts/tooling-context-pages]] defines the special class of pages on the tooling side of that boundary;
- [[concepts/reserved-wiki-files]] explains why a small set of files receives different treatment;
- [[concepts/index-based-discovery]] explains why the root index must remain an entry point;
- [[concepts/okf-validation]] explains how the rule is checked in practice.

The git-tracking policy is adjacent to this cluster because it applies the same local-default philosophy to adapter files and instruction aliases. Both topics are about keeping harness-specific state discoverable when needed, but private by default unless a shared convention is explicitly chosen.

## Practical takeaway

A tooling navigation exception should be:

- explicit rather than implied;
- limited to reserved navigation or history pages;
- justified by discoverability needs;
- aligned with the OKF reserved-file model;
- enforced automatically so the exception does not spread into ordinary content.

In this way, the exception preserves navigability without collapsing the separation between project knowledge and tooling-specific context established in [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]] and the broader OKF quality baseline in [[summaries/agents__skills__agent-ready-context__references__okf-quality-md]]. It also fits the git-tracking guidance for harness adapters and tooling context: local-only by default, shared only by explicit consent.

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]]
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]


See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]