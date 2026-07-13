---
type: "Concept"
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md.md", "summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md.md"]
description: "Agents with explicit, role-specific limits on reads, writes, installs, and execution."
---

# Permission-Scoped Agents

Permission-scoped agents are agent roles defined not only by their purpose and context, but also by explicit limits on what they may read, write, install, inspect, and execute. The concept treats permissions as a core part of agent design rather than an implementation afterthought, helping keep delegated work constrained, auditable, and aligned with user policy. In repository workflows, these limits apply both to harness capabilities and to local CLI adoption decisions, reinforcing the distinction captured in concepts/harness-vs-local-tools. In knowledge-base workflows, the same idea appears as a stronger boundary: an agent may be allowed to inspect state while being prohibited from mutating the knowledge base, running expensive retrieval paths except as a fallback, or directly editing protected directories. This makes permission scoping closely related to concepts/read-only-kb-operations and concepts/wiki-content-as-untrusted-data.

## Core Idea

A permission-scoped agent combines four elements:

- a clear purpose
- specific conditions for when it should be used
- required context sources
- explicit permission boundaries

This pattern appears directly in profile-intent examples, where each profile includes a dedicated permissions section alongside role intent and context. The dependency guidance broadens that model by showing that permission scope also includes whether an agent may install tools, vendor skill content, access the web, or write generated repository artifacts. The OpenKB command guidance sharpens the same idea at the command level by distinguishing safe inspection commands from commands that must remain user-invoked, and by treating some repository areas as off-limits even when they are technically reachable. The broader OpenKB skill guidance extends this further by showing that permission scope also covers retrieval strategy: the agent should begin with knowledge-base discovery, prefer direct page reads over more expensive query paths, and treat all wiki content as data rather than authority.

The subagent-profile-adapter skill adds a runtime-specific framing: adapters are not portable standards but harness-native projections generated from existing agent-ready context. Under that model, permissions are part of the adapter boundary, not just the role description. The skill also recommends detecting the active runtime from environment and harness signals, checking whether the harness supports local subagents or profiles, resolving instruction-file compatibility carefully, asking how generated files should be tracked, and validating that the generated output does not leak tooling context into project pages. Those rules make permission scoping part of runtime-aware adapter design rather than an isolated policy note.

## Why It Matters

Scoping permissions makes delegation safer and more predictable. Instead of assuming an agent can act broadly once invoked, the role definition states what kinds of operations are allowed and where user approval still governs behavior. This supports concepts/tool-boundaries, concepts/minimal-tool-scoping, and concepts/tooling-consent-and-pin-management.

Permission scoping also improves clarity between planning and execution. An agent may understand a task broadly while still being intentionally restricted in how it performs that task, which aligns with concepts/context-action-separation. The dependency guidance adds that permissions should cover not just direct file edits, but also high-impact side effects such as package installation, vendoring external skill content, or refreshing generated knowledge artifacts. The OpenKB materials add another important layer: some tools contain both safe read paths and sensitive write paths, so permission scope must specify not only whether a tool is available, but which subcommands are allowed, when expensive query flows are justified, and which directories remain protected from direct edits. They also show that permission boundaries should account for trust: an agent may read from a curated knowledge base while still being required to treat its contents as untrusted data that cannot authorize further actions. In practice, this makes permission scoping part of concepts/safe-automation, concepts/supply-chain-security, and concepts/knowledge-boundaries, not just interface design.

The subagent-profile-adapter skill reinforces the same point at the workflow level. It treats harness permissions and local CLI availability as separate concerns, avoids using installed binaries as proof of the active runtime, and keeps adapter files short so they do not smuggle long project context into runtime-specific files. That keeps permissions narrow and tied to the current harness rather than generalized into project truth.

## Evidence From the Source Document

The subagent-profile-adapter skill defines permission-scoped adapters as runtime-specific projections rather than portable standards. It frames adapters as harness-native files generated from the repository's existing agent-ready context, and it places permission decisions inside a larger workflow that starts with runtime detection and ends with validation. Its boundary rules explicitly separate OKF wiki knowledge, AGENTS.md orientation, reusable Agent Skills, and runtime adapters, which reinforces the idea that a role's permissions should be narrow and tied to the current harness rather than generalized into project truth.

The skill also sets a workflow constraint that matters for permission scoping:

- detect the active runtime from environment and harness signals, not from installed binaries alone
- check whether the harness supports local subagents or profiles before generating anything
- resolve instruction-file compatibility carefully, using aliases only when the target is known
- derive candidate adapters from real repository needs and existing compiled knowledge
- ask how generated harness-specific files should be tracked before writing them
- keep adapter files short and avoid embedding long project context
- validate that the result does not leak tooling context into project pages

These instructions show that permission scope is not only about runtime actions; it also governs how much context the agent may project into generated files.

In the profile-intent example, three example profiles show different permission envelopes:

- `okf-curator` allows reading by default, but writing to OKF or AGENTS.md depends on user policy, and shell access is limited to validation scripts
- `skill-architect` may read and write `.agents/skills/` according to user policy, while shell use remains limited to validation scripts
- `repo-cartographer` is read-only by default, emphasizing repository understanding without modification

These examples show that permission scope can vary by role while still following a common structure. The role definition is not complete until its operational limits are specified.

The dependency guidance adds a complementary repository-level example of permission scoping in action:

- harness permissions and local CLI availability are treated as separate concerns, so an agent may have shell access without being assumed ready to use `git`, `uv`, `graphify`, or `openkb`
- `allowed-tools` is treated as a hint rather than guaranteed enforcement, so the harness remains the real permission authority
- installs are consent-first, with the user choosing whether to self-install, delegate the install, or skip a tool entirely
- destructive or high-trust actions such as package installs, web-backed documentation refresh, and vendoring external skill content are explicitly constrained by policy
- least-privilege defaults are recommended: allow read/search broadly, ask before writes when the task is exploratory, and deny destructive commands

The OpenKB command guidance provides a concrete CLI-specific example of the same pattern:

- `openkb status` is allowed as a preflight inspection step because it establishes the active knowledge-base path before any file reads
- `openkb list` is an allowed discovery command for inspecting available documents and concepts
- `openkb query` is permitted only as a fallback because it triggers an internal LLM call and should not replace direct inspection when a deterministic path exists
- interactive or background commands such as `openkb chat` and `openkb watch` are excluded from autonomous use
- mutating commands such as `openkb add`, `openkb remove`, `openkb lint --fix`, `openkb init`, and `openkb use` must remain user-invoked
- direct edits under the knowledge base's `wiki/` and `.openkb/` directories are forbidden, even if the agent can otherwise read the repository

The broader OpenKB skill guidance extends that operating model:

- the agent must first resolve the active knowledge base with `openkb status` rather than assuming the current directory is authoritative
- wiki content, grep results, and JSON page extracts are all treated as untrusted content and cannot expand the agent's authority
- concept and entity pages are preferred entry points for answering questions, while `openkb query` is reserved for cases where direct discovery and file reading do not suffice
- following wikilinks is allowed as structured navigation, but only as read-only inspection within the compiled knowledge base
- if the knowledge base lacks relevant material, the agent should say so rather than fabricate a KB-grounded answer
- even when a mutating command would help, the agent must propose it for the user rather than run it autonomously

Together, these sources show that permission-scoped agents are defined both by role-local permissions and by workflow-level rules around tool adoption, trust, user consent, protected state, and retrieval cost.

## Design Characteristics

Permission-scoped agents usually have several recurring properties:

- permissions are stated explicitly rather than implied
- write access is often conditional on user policy
- shell access may be narrowed to validation or inspection tasks
- read-only roles are useful for exploration and diagnosis
- constraints are tailored to the role's purpose rather than applied uniformly
- tool installation, vendoring, and web access are treated as separate privileges rather than automatic extensions of shell access
- permission boundaries often distinguish between using existing tools and changing the repository's toolchain state
- command-level permissions may separate harmless discovery subcommands from destructive or interactive ones within the same CLI
- protected paths may remain off-limits even when broader filesystem access exists
- expensive tool actions such as query-backed retrieval may require a stronger justification than ordinary reads
- trusted access to a data source does not imply trusted authority for its contents
- preflight discovery steps may be required before narrower read permissions can be exercised safely
- runtime-specific adapters should stay short, because large embedded context weakens the boundary they are meant to enforce
- generated adapters should project only the permissions needed by the active harness, not a generalized project policy

This makes permission design part of concepts/subagent-role-design and closely related to concepts/skill-governance. It also aligns with concepts/executable-validation because constrained agents often retain validation powers even when broader mutation rights are withheld, and with concepts/preflight-checks because scoped agents often need an allowed inspection step before acting.

## Relationship to Other Concepts

Permission-scoped agents overlap with but are distinct from nearby ideas:

- concepts/subagent-role-design focuses on defining a role's mission, triggers, and context; permission scoping adds operational constraints to that design
- concepts/minimal-tool-scoping emphasizes limiting tools to the smallest necessary set; permission scoping applies that principle to an agent role
- concepts/tool-boundaries covers limits on how tools are used; permission-scoped agents embed those limits into role definitions
- concepts/tooling-consent-and-pin-management addresses user approval and control over tool behavior; permission scoping operationalizes those controls at the agent level
- concepts/harness-vs-local-tools distinguishes environment-exposed capabilities from repository-local executables; permission-scoped agents often need separate rules for each
- concepts/supply-chain-security covers the trust implications of installing and updating tools; permission-scoped agents may be allowed to inspect dependency state without being allowed to change it
- concepts/knowledge-boundaries emphasizes limits around curated or internal knowledge stores; permission-scoped agents often encode those protected areas directly into their operating rules
- concepts/cost-aware-tool-use focuses on reserving expensive operations for cases where cheaper deterministic access is insufficient; permission scope can enforce that ordering
- concepts/read-only-kb-operations focuses on inspecting a knowledge base without mutating it; permission-scoped agents generalize that pattern into a role contract
- concepts/wiki-content-as-untrusted-data focuses on treating compiled wiki text as data rather than instructions; permission-scoped agents use that trust boundary to prevent authority escalation through retrieved content
- concepts/runtime-adapter-management captures the lifecycle of harness-specific runtime projections; permission-scoped agents are one of the main role patterns those adapters may express
- concepts/adaptive-harness-detection supports the runtime-aware part of this workflow by preferring explicit harness signals over tool presence alone

## Practical Takeaway

When defining an agent profile, permissions should be specified as part of the role contract: what the agent can read, what it can modify, what shell actions it may take, whether it may access the web, whether it may install or update tools, and where user policy must be consulted. In the source examples, this turns lightweight profile intents into controlled delegation patterns rather than open-ended automation. The dependency guidance makes the same point at the repository workflow level: permission scope should explicitly cover tool bootstrap, version-pinned installs, vendoring external skill content, and other actions that can alter the trust boundary of the project. The OpenKB guidance extends that model to command selection, retrieval strategy, and protected data handling: allow preflight discovery and read-only inspection where appropriate, require explicit user control for mutating subcommands, prefer direct deterministic reads before query-mediated lookups, and preserve curated knowledge stores by forbidding direct edits to reserved locations.

The subagent-profile-adapter skill adds the final practical lesson: runtime-specific adapters should be generated only after confirming the active harness, and their permissions should be expressed in the native format of that harness without turning them into a second source of truth.

## See Also

- [[summaries/agents__skills__subagent-profile-adapter__assets__profile-intents-example-md]]
- [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]
- [[summaries/agents__skills__openkb__references__commands-md]]
- [[summaries/agents__skills__openkb__SKILL-md]]
- concepts/subagent-role-design
- concepts/minimal-tool-scoping
- concepts/tool-boundaries
- concepts/context-action-separation
- concepts/skill-governance
- concepts/tooling-consent-and-pin-management
- concepts/harness-vs-local-tools
- concepts/safe-automation
- concepts/supply-chain-security
- concepts/read-only-kb-operations
- concepts/wiki-content-as-untrusted-data
- concepts/runtime-adapter-management
- concepts/adaptive-harness-detection

See also: [[summaries/agents__skills__subagent-profile-adapter__references__profile-authoring-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]