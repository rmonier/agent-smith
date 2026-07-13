---
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/README-md.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md", "summaries/repo-snapshot.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md.md"]
type: "Other"
description: "Repository-level ignore file used to manage shared exclusion policy"
---

# .gitignore

`.gitignore` is the repository-level ignore file used to keep selected paths out of git tracking.

## In This Document

The subagent-profile-adapter skill treats `.gitignore` as one of the supported ways to track generated harness-specific files when the user or repo policy wants the ignore rule to apply to every contributor. It contrasts that choice with local-only exclusions in `.git/info/exclude`.

For harness-specific adapter outputs, the skill recommends asking how generated files should be tracked before writing them:

- local-only via `.git/info/exclude`
- ignored for all via `.gitignore`
- committed as shared team adapters

The skill also frames runtime adapters as runtime-specific projections rather than durable project truth, so `.gitignore` belongs to repository policy rather than knowledge capture. That separation aligns with [[concepts/runtime-adapter-management]], [[concepts/knowledge-layer-separation]], and [[concepts/generated-artifact-adoption]].

The tooling-context policy adds a narrower exception for `okf/wiki/tooling/`: that tree is user-scoped and local by default, with a committed `okf/wiki/tooling/index.md` stub and bundle-root index entry when tooling content exists. Its default `.gitignore` pattern keeps local tooling pages out of git while preserving the committed stub, so `.gitignore` is the shared-ignore mechanism for that policy boundary.

The OpenKB repo build workflow also requires `.gitignore` to cover build and cache paths such as `okf/.okf-build/`, `okf/output/`, `okf/wiki/reports/`, `graphify-out/cost.json`, `graphify-out/cache/`, `__pycache__/`, `.env`, and `okf/.env`. In that workflow, `.gitignore` is part of the deterministic staging setup that keeps generated artifacts, caches, and local secrets out of version control.

The privacy-and-data-flows guidance adds a second, subtler role for `.gitignore`: it is a boundary for committed history, not just provider egress. A file excluded only through `.git/info/exclude` or a global excludesfile can still be scanned by `graphify update`, and if it produces graph nodes, that content can be baked into committed `graphify-out/graph.json` or `GRAPH_REPORT.md`. In that sense, `.gitignore` is the shared exclusion mechanism that helps prevent local-only content from crossing into repository history. The same guidance also says staging for OpenKB must live inside the KB root (`okf/.okf-build/input/`), and `.gitignore` should keep that build tree and related caches from leaking into the repository.

The skill adds an explicit tracking-policy step before writing harness adapters, so `.gitignore` is no longer just a passive repo file; it becomes part of the consent and policy decision for generated outputs.

## Key Role

The document treats `.gitignore` as a shared, intentional repository policy tool rather than the default choice for harness-specific adapter files. That distinction supports [[concepts/local-vs-shared-ignore]], [[concepts/consent-first-workflows]], and [[concepts/runtime-adapter-management]].

It also fits the broader pattern of keeping runtime-specific projections separate from durable project knowledge, so that generated adapters remain governed by repository policy rather than hidden in local state.

In the OpenKB workflow, `.gitignore` also helps enforce build hygiene by excluding OKF build output, graphify caches, and local environment files from the repository. That makes it part of [[concepts/deterministic-builds]], [[concepts/source-pack-staging]], and [[concepts/preflight-checks]].

The privacy guidance strengthens this role by treating `.gitignore` as the repository-level control that keeps local-only files from entering committed shared artifacts, especially where `graphify update` does not consult local-only exclusions.

## Related Context

- [[summaries/agents__skills__subagent-profile-adapter__references__git-tracking-policy-md]] explains when to prefer `.git/info/exclude` over `.gitignore`.
- [[entities/git-info-exclude]] is the local-only alternative used for per-user exclusions.
- [[concepts/git-tracking-policy]] captures the broader policy pattern around generated adapter files.
- [[concepts/tooling-context-pages]] and [[concepts/tooling-navigation-exceptions]] are relevant to the `okf/wiki/tooling/` exception described in the policy.
- [[summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md]] defines the tooling-specific default ignore pattern and committed stub boundary.
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]] defines the OpenKB build workflow requirements that `.gitignore` must satisfy.
- [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]] adds the distinction between local-only exclusions and shared repository history leakage.

## Practical Implication

If a file should be ignored by everyone cloning the repository, `.gitignore` is the mechanism the document recommends. If the ignore rule is only for one local checkout, the document favors `.git/info/exclude` instead.

For generated harness adapters, the skill asks the user to choose the tracking policy first, then writes files that match that choice.

For OpenKB builds, the repo should keep the KB build tree, output directories, cache files, and local env files ignored so staging and validation stay deterministic and clean.

For privacy-sensitive workflows, relying on `.gitignore` is also a way to reduce the chance that local-only artifacts get swept into shared graph outputs or committed registry files.

## Related Documents

- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]

See also: [[summaries/repo-snapshot]]

See also: [[summaries/README-md]]