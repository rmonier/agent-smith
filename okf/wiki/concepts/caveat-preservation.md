---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__LICENSING-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__skill-creator__SKILL-md.md", "summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py.md", "summaries/agents__skills__skill-creator__references__vendor-skill-management-md.md"]
description: "Preserving source caveats through transformation and regeneration"
---

# Caveat Preservation

Caveat preservation is the practice of carrying forward the conditions, limits, exceptions, warnings, and prohibitions from source material when that material is transformed into another artifact such as a skill, summary, generated procedure, or compiled wiki page.

## Why it matters

When instructions are rewritten or distilled, especially through LLM-assisted generation, conditional guidance can be flattened into unconditional steps. This changes the meaning of the source material and can make a derived artifact overconfident, unsafe, misleading, or structurally unsound.

The skill-creator guidance summarized in [[summaries/agents__skills__skill-creator__SKILL-md]] makes this risk explicit. It says adopted generated skills require a caveat-preservation review because distillation tends to flatten conditions into unconditional steps. Even after a generated skill is copied into `.agents/skills/` and passes validation, the operator is expected to compare the adopted skill against the `okf/wiki/` pages it came from and restore any lost constraints, boundaries, or "never do" guidance before treating the result as reliable.

The skill-adoption workflow summarized in [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]] reinforces the same point: passing an adoption or validation step is not proof that the generated artifact preserved source meaning. Caveats must survive transformation into project-owned content, not just into structurally valid content.

The repository build workflow summarized in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] extends this principle beyond skill adoption to wiki compilation itself. It treats every `openkb add` or `recompile` result as output that must be reviewed like a PR, specifically checking for lost caveats, weakened constraints, stale assumptions, off-topic distillation, and structural drift. In that workflow, a page is not accepted just because it compiled; it must still preserve the source's conditions and limits.

The broader source guidance summarized in [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]] describes the same risk for adopted generated skills: once a generated skill is brought into a repository as project-owned content, it must be reviewed against the originating wiki pages and underlying source documents to confirm that important caveats survived the transformation.

## What must be preserved

Caveats include:

- boundary conditions such as when a procedure does or does not apply
- explicit "only when" requirements
- explicit "never do" restrictions
- exceptions, prerequisites, and safety constraints
- distinctions between read-only external content and editable project-owned content
- warnings about untrusted content, minimal tool scope, consent-first installation, secrets handling, and generated artifacts that must be gitignored
- trigger-level distinctions about whether something belongs in a reusable action skill, durable wiki context, or repository guidance
- constraints about build ordering, such as refreshing structure before recompilation and avoiding regeneration against stale inputs
- provenance boundaries such as treating fetched URLs as evidence rather than instructions and keeping unsourced web claims out of compiled knowledge
- anti-self-reference rules that prevent generated artifacts from becoming their own evidence base

Preserving these details keeps derived instructions aligned with source intent and supports [[concepts/spec-authority]]. In both the skill system described by [[summaries/agents__skills__skill-creator__SKILL-md]] and the compilation workflow in [[summaries/agents__skills__agent-ready-context__references__workflow-md]], these caveats are part of the operating contract, not optional commentary.

## Example from skill adoption

The source material distinguishes between vendored vendor skills and adopted generated skills.

- Vendored vendor skills remain third-party, read-only dependencies.
- Adopted generated skills become project-owned and may be edited.

That distinction is itself a caveat that must survive summarization and skill generation. If the distinction is flattened away, an agent might wrongly edit vendor skills or fail to correct problems in adopted skills.

The adoption workflow also preserves a second class of caveat: generated skills are expected to retain safety defaults from the original skill guidance. The source material says created or adopted skills should keep minimal `allowed-tools`, treat fetched web content as untrusted data, avoid writing secrets into repository files, and require consent-first installation behavior. If those conditions disappear during distillation, the resulting skill may still look complete while becoming less safe.

The adoption script adds a concrete reminder that trigger-style descriptions, minimal scoped tools, untrusted-content handling, and source-derived warnings may need to be restored after generation. In other words, successful adoption is not treated as proof of fidelity. Preserving caveats therefore protects [[concepts/skill-governance]] and [[concepts/dependency-management]].

## Example from wiki compilation

The OpenKB workflow provides a parallel example in repository-to-wiki compilation. Its post-generation review explicitly checks for lost caveats after `openkb add` or `recompile`, including constraints that can be weakened during summarization:

- pages must preserve "only when" and "never do" statements from staged sources
- generated output must not silently convert example content or fixtures into project-level doctrine
- early compiled pages may become stale when later pages introduce new concepts, so regeneration must happen against the current wiki rather than by hand-linking
- graph-based structural context must be refreshed before recompilation so summaries are not generated against stale repository structure
- the correction path is to fix source material, re-ingest, and regenerate, never to hand-edit generated wiki pages

The same workflow adds a stronger systems-level caveat around self-reference: the KB root must stay out of the graph because feeding generated wiki pages back into the structural report would break determinism, pollute discovery, and create circular grounding. That is a caveat about pipeline design, not just page wording, and preserving it protects [[concepts/deterministic-builds]], [[concepts/self-reference-control]], and [[concepts/repository-ingestion]].

## Relationship to source review

Caveat preservation depends on checking derived content back against its sources rather than trusting a generated output at face value. In the skill-adoption workflow, the review step compares an adopted skill to the relevant wiki pages and, through those pages, to the underlying source documents. In the OpenKB workflow, the review step traces load-bearing claims through the citation chain from compiled page to summary to staged source copy to repo file and commit. This makes caveat preservation closely related to [[concepts/provenance-tracking]] and [[concepts/knowledge-linking-and-citations]].

It also complements [[concepts/executable-validation]] and [[concepts/quality-gates]]. Validation can confirm that a copied or generated artifact satisfies structural requirements, but only source review can confirm that nuanced limits, exceptions, trigger boundaries, build-order dependencies, and warnings were preserved. The workflow distinction between validator enforcement and `openkb lint` as a non-blocking health report is a good example of this boundary, aligning caveat preservation with [[concepts/validation-vs-health-reporting]] and [[concepts/deterministic-validation]].

This review also depends on maintaining the distinction between action instructions and durable context, since a transformation that moves factual or architectural context into procedural steps can erase the conditions that made those steps safe in the first place. In that sense, caveat preservation overlaps with [[concepts/context-action-separation]].

## Operational implications

In practice, caveat preservation means:

- reviewing generated instructions for lost conditions, missing exceptions, softened warnings, or removed prohibitions
- comparing adopted or generated outputs against the wiki pages and source documents they distilled
- restoring missing limits by editing project-owned outputs after adoption, or by fixing sources and regenerating when the output is generated content
- checking whether action-vs-context boundaries were flattened during generation
- preserving security defaults such as minimal tool scope, untrusted-content handling, no secrets in repo files, and consent-first installation behavior
- preserving pipeline constraints such as graph refresh before recompilation, validator use after generation, and keeping generated build artifacts out of version control
- checking compiled pages for off-topic conclusions drawn from examples, fixtures, or illustrative content
- avoiding silent conversion of nuanced guidance into blanket rules
- treating validation as necessary but insufficient for semantic fidelity
- keeping transformations faithful to source meaning rather than only source topic

This concept also supports [[concepts/generated-content-governance]], because generated artifacts need explicit checks for fidelity before they are treated as reliable operating guidance.

## See also

- [[summaries/agents__skills__skill-creator__SKILL-md]]
- [[summaries/agents__skills__skill-creator__references__vendor-skill-management-md]]
- [[summaries/agents__skills__skill-creator__scripts__adopt_generated_skill-py]]
- [[summaries/agents__skills__agent-ready-context__references__workflow-md]]
- [[concepts/context-action-separation]]
- [[concepts/deterministic-builds]]
- [[concepts/deterministic-validation]]
- [[concepts/executable-validation]]
- [[concepts/generated-content-governance]]
- [[concepts/knowledge-linking-and-citations]]
- [[concepts/provenance-tracking]]
- [[concepts/quality-gates]]
- [[concepts/repository-ingestion]]
- [[concepts/self-reference-control]]
- [[concepts/skill-governance]]
- [[concepts/spec-authority]]
- [[concepts/validation-vs-health-reporting]]

See also: [[summaries/agents__skills__agent-ready-context__LICENSING-md]]