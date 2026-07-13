---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
description: "Policy for stable committed navigation to local tooling pages"
---

# Tooling Stub Resolving

Tooling stub resolving is the practice of keeping a committed, user-neutral entry point for local tooling pages so the wiki remains coherent across clones while still treating tooling context as user-scoped and outside project truth. It also supports runtime-specific adapter workflows by giving harness documentation a stable navigation target without exposing local harness details as shared project knowledge.

## What the stub does

The policy establishes that `okf/wiki/tooling/index.md` is the single committed navigation stub for the tooling overlay. It must resolve on every clone even though the detailed harness and provider pages live locally and are not committed.

The stub exists to prevent dangling references and to preserve wikilink integrity when tooling content differs between users or machines. It is intentionally neutral: it does not name specific harnesses, models, or users, but it can still anchor locally generated harness adapters and validation notes that belong only to the current environment.

## Why resolving matters

Without a stable stub, the root index would either:

- point to pages that do not exist on other clones, or
- omit the tooling subtree entirely and hide valid local context

Tooling stub resolving therefore supports progressive disclosure without turning tooling into project knowledge. The committed root index can point to the stub, while local pages remain discoverable by directory listing and can hold harness-specific adapter context, validation evidence, or runtime notes.

## Core rules from the policy

- Keep tooling context in only two cases: harness build records and opt-in adapter/profile tooling context.
- Store the committed navigation stub at `okf/wiki/tooling/index.md`.
- Do not enumerate local tooling pages in committed index files.
- Ensure local tooling pages include at least one outgoing wikilink to durable project knowledge.
- Use the stub as the stable target for the bundle-root index entry.
- Treat harness-specific adapter files as runtime projections, not as a source of truth.
- Prefer short adapter files that point back to `AGENTS.md`, `okf/wiki/`, and relevant skills instead of embedding long context.
- Keep the adapter workflow tied to runtime detection, harness capability checks, and explicit user policy for tracking generated files.

These rules connect stub resolving to local by default tooling, tooling context isolation, runtime adapter management, and tooling link policy.

## Operational behavior

The document treats stub resolving as part of wiki maintenance rather than a knowledge-capture problem. When tooling content exists, the root index must include a labeled tooling section that links to the committed stub. That entry is the only project-side navigation allowed into tooling.

This keeps project pages from depending on local overlay content while still making the overlay visible to spec-driven consumers. In practice, stub resolving is a small but important piece of reserved navigation files and knowledge base navigation discipline, and it gives subagent/profile adapter workflows a safe place to point without promoting harness details into compiled knowledge.

## Related ideas

- [[concepts/tooling-context-pages]] for the broader structure of tooling pages
- [[concepts/tooling-navigation-exception]] for the special root-index rule
- [[concepts/tooling-boundaries]] for the separation between project knowledge and user-scoped runtime context
- [[concepts/git-tracking-policy]] for how the stub fits with local-by-default file tracking
- [[concepts/wikilink-resolution]] for how durable links are kept valid across the wiki
- [[concepts/runtime-adapter-management]] for harness-specific adapter generation and maintenance
- [[concepts/harness-native-profiles]] for runtime-projected subagent or profile files
- [[concepts/runtime-ambiguity-resolution]] for deciding which harness to target when the active runtime is unclear

## Source

Derived from [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]].

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/agents__skills__agent-ready-context__SKILL-md]]