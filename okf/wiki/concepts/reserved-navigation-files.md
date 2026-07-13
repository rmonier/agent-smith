---
type: "Concept"
sources: ["summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md"]
description: "Special wiki files that preserve navigation while exempting reserved link rules."
---

# Reserved Navigation Files

Reserved navigation files are wiki pages that are exempt from some link-direction rules because they serve structural roles rather than ordinary content roles. In this wiki, the main examples are the bundle-root `index.md` and `log.md`, which function as navigation and history surfaces instead of regular project pages.

## What They Are

Reserved navigation files are deliberately protected from validation rules that would otherwise flag links into tooling or other special areas. Their purpose is to keep the wiki discoverable and operational even when those links are needed for harness navigation or provenance tracking.

The tooling link validator treats these files as special cases in a broader [[concepts/link-directionality]] policy. It scans Markdown pages for links, strips code spans and fenced blocks to avoid false positives, and then exempts the bundle-root `index.md` and `log.md` from the forbidden reverse-link rule.

The validator also treats the bundle-root index as a required outward-facing entry point when tooling pages exist: if `okf/wiki/tooling/` contains non-reserved pages, `index.md` must reference `tooling/` in a clearly labeled harness-specific section, and the committed `tooling/index.md` stub must exist so that the shared navigation target resolves on clones that do not have local tooling pages. That stub is the stable, user-neutral target that keeps the local overlay coherent across clones.

The implementation is deliberately narrow. It scans Markdown files under the wiki root, skips `AGENTS.md`, preserves line numbers while stripping code, and applies different checks depending on whether a page lives in tooling context or in the project graph. That means reserved navigation files are not just filename exceptions; they are part of the validator's structural model for separating local tooling from shared wiki content.

## Why They Matter

The tooling link policy treats reserved files differently from normal pages:

- `index.md` may reference `tooling/` when tooling pages exist, because it is the outward-facing entry point that keeps the bundle navigable.
- `log.md` is exempt from the forbidden direction because it records history rather than content dependencies.
- These files prevent strict link-direction enforcement from breaking the top-level wiki structure.
- The root `index.md` must reference tooling in a clearly labeled harness-specific section whenever non-reserved tooling pages exist.
- The committed `tooling/index.md` stub must exist so the root index target resolves on clones that do not have local tooling pages.
- Tooling context itself is user-scoped and local by default, so the reserved navigation surface is what makes the shared wiki still usable without exposing local pages as project truth.

This distinction supports [[concepts/link-directionality]] and [[concepts/reserved-wiki-files]]. It also aligns with [[concepts/tooling-context-governance]] by keeping tooling local while still exposing a stable navigation path.

## Key Behavior From the Validator

The linked validator enforces three related expectations:

- Project pages must not link back into `okf/wiki/tooling/`.
- The root `index.md` must explicitly reference `tooling/` when tooling pages exist, and the reference must appear in a clearly labeled harness-specific section.
- The committed `tooling/index.md` stub must exist so the root index target resolves on clones that do not have local tooling pages.

It also distinguishes page types and locations more carefully than a simple filename allowlist:

- Tooling pages may need a warning if they do not declare `scope: tooling` or `type: tooling-context`.
- Entity pages are intentionally excluded from the reverse-link restriction.
- Only project concept pages and navigation indexes are scanned for forbidden tooling references.
- The root `index.md` and `log.md` are the only reserved files explicitly exempted from the reverse-link error path.
- A valid tooling overlay is expected to remain local by default, with the committed navigation stub as the only shared artifact.

Reserved navigation files are the exception that makes the first rule workable without breaking the second and third.

## Design Implications

Reserved navigation files help separate structural metadata from content rules. They act as controlled escape hatches that preserve repository health while still allowing strict validation elsewhere. This supports [[concepts/validation-vs-health-reporting]], [[concepts/preflight-checks]], and [[concepts/okf-validation]].

The pattern also reflects a local-vs-shared boundary: tooling content is local-by-default, but the shared wiki still needs a committed navigation surface so the compiled bundle remains discoverable on fresh clones. That makes reserved navigation files part of broader [[concepts/local-by-default-tooling]] and [[concepts/tooling-context-isolation]] practices.

## Related Ideas

- [[concepts/reserved-markdown-files]]: broader class of filenames with special treatment.
- [[concepts/tooling-navigation-exceptions]]: exceptions that keep tooling discoverable from the root wiki.
- [[concepts/local-by-default-tooling]]: explains why tooling is kept local while still requiring a committed stub.
- [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]: source document that encodes and checks this policy.

See also: [[summaries/README-md]]

See also: [[summaries/agents__skills__agent-ready-context__assets__agents-md-okf-ready-template-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]

## Related Documents
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]]