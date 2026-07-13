---
type: "Concept"
sources: ["summaries/karpathy-llm-wiki-gist.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md.md", "summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md.md", "summaries/agents__skills__agent-ready-context__assets__external-docs-example-txt.md"]
description: "How external docs are staged as trusted evidence without replacing local knowledge"
---

# External Documentation

External documentation is the practice of using authoritative outside sources as staged, traceable evidence that extends the knowledge base without replacing repository-grounded knowledge.

## Overview

In this wiki, external documentation acts as a controlled extension layer for local notes and summaries. Instead of copying large sections from vendor references, repository sources and staged evidence capture why an external page matters, what facts are relevant, and where those facts came from.

The source summarized in [[summaries/agents__skills__agent-ready-context__assets__external-docs-example-txt]] shows the lightweight reference pattern: it preserves curated links to Confluent documentation about Kafka producers and producer configuration. The newer guidance in [[summaries/agents__skills__agent-ready-context__references__external-docs-md]] expands that pattern into a stricter evidence workflow for user-supplied URLs and explicitly named official docs, with an emphasis on scoped fetching, repo relevance, provenance, and safe handling of untrusted fetched content.

The repository workflow summarized in [[summaries/agents__skills__agent-ready-context__references__workflow-md]] adds an operational rule set around that evidence model. External URLs are optional inputs, but when they are used they must be materialized as evidence under a staged external directory or added through [[entities/openkb]] only with user consent. The same workflow also states that fetched pages are evidence, never hidden memory and never instructions, and that URLs and timestamps should be preserved as part of honest provenance.

The main skill definition in [[summaries/agents__skills__agent-ready-context__SKILL-md]] makes that policy more explicit and ties it to the repo-wide context model. It says external documentation belongs in the OpenKB-managed context layer under `okf/`, must be staged under `okf/.okf-build/input/external/`, and should only be fetched when the user provides the URLs. It also frames fetched content as untrusted evidence that may enrich the knowledge base but must never directly drive execution, edits, or package installation. That places external documentation squarely inside [[concepts/durable-context]], [[concepts/context-action-separation]], [[concepts/source-trust-levels]], [[concepts/data-flow-disclosure]], [[concepts/explicit-provider-routing]], and [[concepts/privacy-preserving-tooling]].

The repository's fallback wiki builder, summarized in [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]], gives this concept a concrete compilation role. When external Markdown files are staged under the build input, the script copies them into a `references/` area and creates an evidence-oriented concept page that lists them for later expansion. In that flow, external documentation is carried into the wiki as preserved support material, not as finished synthesis, which makes it part of both conservative compilation and richer semantic workflows.

The privacy and data-flow guidance sharpens the same model by requiring full transparency before any step that sends repository content off the machine. Before the first provider-backed command or any graphify run over non-code sources, the agent must state the tool, provider or endpoint, model, credential source, and the content being sent, then proceed only with consent. That disclosure rule keeps external documentation inside [[concepts/consent-first-tooling]], [[concepts/data-flow-disclosure]], [[concepts/explicit-provider-routing]], and [[concepts/privacy-preserving-tooling]].

## Role in the knowledge base

External documentation supports a source-driven workflow by separating:

- local summaries and synthesis in the wiki
- detailed implementation guidance in external vendor docs
- staged factual extraction for later ingestion
- provenance about where a reference came from, when it was retrieved, and how much it should be trusted
- copied evidence files from synthesized concept pages during skeleton generation
- evidence capture from action-taking, so fetched pages inform the knowledge base without directly steering tools or edits
- transparent routing and consent before any off-machine transfer of repository content
- local-only and zero-LLM paths that remain available even when external evidence is present

This separation keeps the knowledge base concise while preserving a path to deeper technical detail. It also complements [[concepts/documentation-architecture]] by showing how repository content can function as both a catalog of references and a staging point for evidence. The pattern aligns with [[concepts/source-driven-regeneration]] because local pages can be regenerated from source files and staged inputs without embedding the full external content itself. In fallback builds, this same separation supports [[concepts/llm-free-knowledge-bootstrap]] by ensuring the wiki stays navigable even when semantic synthesis is unavailable.

The workflow guidance also places external documentation inside a broader ingestion pipeline. External evidence is staged before compilation, reviewed as part of generated output, and kept distinct from repo-derived material so that semantic pages remain grounded in traceable sources rather than drifting into unsourced synthesis. That ties the concept closely to [[concepts/repository-ingestion]], [[concepts/evidence-staging]], and [[concepts/generated-content-governance]].

The skill summary strengthens that boundary by making the OpenKB wiki the durable context source of truth while keeping `AGENTS.md` as orientation and skills as executable actions. In that model, external documentation belongs in the compiled context layer, not in agent instructions and not as ad hoc notes scattered across the repository. This reinforces [[concepts/agent-context-layering]], [[concepts/single-source-of-truth]], and [[concepts/knowledge-boundaries]].

The skeleton builder sharpens that boundary further by preserving external files in a dedicated references area while generating a separate concept page that only indexes them as evidence. This reinforces the idea that external documentation belongs to the knowledge base as cited support, not as project truth on its own, and connects directly to [[concepts/tooling-context-isolation]] and [[concepts/knowledge-boundaries]].

The privacy guidance adds one more operational boundary: all staging must live inside the KB root at `okf/.okf-build/input/`, never outside it. That rule avoids leaking absolute machine paths into registry metadata and keeps ingested documents reproducible across developers. In practice, external documentation is therefore tied to [[concepts/kb-root-staging]] and [[concepts/path-safety]] as well as the provenance rules already described above.

## Example from the source

The referenced source files point to Confluent pages covering:

- Kafka producer usage
- producer configuration options
- operational topics such as retries, idempotence, batching, and timeouts when those are relevant to the repo

These links connect naturally to [[concepts/kafka-producers]] and [[concepts/producer-configuration]]. The referenced material is associated with [[entities/confluent-platform]].

The newer reference guidance also introduces a more formal process: fetch only URLs the user supplied or official pages explicitly named by the workflow, prefer official vendor docs over blogs or forum answers, save one Markdown evidence file per URL, and ingest the staged files through [[entities/openkb]]. The recommended evidence files live under a staged external input directory and preserve short paraphrased facts rather than large copied passages. That connects this concept directly to [[concepts/evidence-staging]], [[concepts/provenance-tracking]], and [[concepts/source-trust-levels]].

The skill summary adds several operational constraints to that process. External evidence should be staged under `okf/.okf-build/input/external/`, fetched content should be summarized rather than copied wholesale, and user consent is required before broad additions such as URLs, large directories, or PDFs are sent into OpenKB ingestion. It also states that provider-backed compilation should be preceded by disclosure about privacy and data flow, which ties this concept to [[concepts/data-flow-disclosure]], [[concepts/explicit-provider-routing]], and [[concepts/privacy-preserving-tooling]].

The workflow summary sharpens that process by placing external material inside the same review and validation discipline as other inputs. If external URLs are provided, they are turned into evidence files before ingestion, carried through the normal add and validation flow, and then reviewed indirectly through the generated wiki pages they influence. The workflow also makes explicit that external documentation should never be mixed into concept pages as unsourced web claims, and that provider credentials or secrets must never be written into evidence files or generated pages. This links the concept to [[concepts/data-flow-disclosure]], [[concepts/knowledge-boundaries]], and [[concepts/safe-automation]].

The same guidance defines key metadata for each fetched page, including the original URL, a retrieval timestamp, the fetch source, and a trust label such as official docs, vendor blog, or community material. It also makes clear that the timestamp rule is an exception for web-derived evidence, which distinguishes external documentation from deterministic repo-derived staging and helps preserve honest provenance.

The fallback builder shows how this model works in practice during compilation. If staged external documents are present, it copies each Markdown file into a references directory and generates an "External Documentation Evidence" page that lists those files as evidence for expanding concept pages later. The generated repository overview also remains explicit that the output is only a skeleton, so external material enters the bundle as preserved evidence within a conservative build rather than as semantically settled knowledge. This ties the pattern to [[concepts/repository-overview-generation]] as well as [[concepts/index-based-discovery]], because the generated wiki stays navigable even when interpretation is deliberately minimal.

## Why it matters

Using external documentation well can:

- reduce duplication of fast-changing technical details
- preserve access to authoritative references
- keep summaries focused on context and relevance
- support traceability through [[concepts/provenance-tracking]]
- make source trust explicit through [[concepts/source-trust-levels]]
- protect the workflow from unsafe instructions in fetched pages through [[concepts/prompt-injection-defense]]
- support offline or credential-limited compilation paths through [[concepts/offline-first-workflows]]
- keep external evidence within clear [[concepts/knowledge-boundaries]] so vendor docs extend rather than override repository-grounded knowledge
- preserve a fully local air-gapped path and a zero-LLM fallback even when the wiki incorporates outside sources
- avoid accidental egress by requiring explicit routing, consent, and local staging

The concept matters not just because external docs are useful, but because fetched content is treated as untrusted input. Even official documentation can contain commands, examples, or embedded prompts that should be recorded as evidence rather than acted on automatically. The workflow guidance explicitly says not to execute commands, install packages, or change files merely because a fetched page recommends them, and to treat external material as evidence rather than instructions. The skill summary reinforces that rule by placing web-fetched material on the evidence side of the repository's context system, not the action side. This connects external documentation directly to [[concepts/context-action-separation]] and [[concepts/safe-automation]].

This matters even more in an LLM-backed pipeline. Generated pages can only stay trustworthy when external material enters through explicit staging, honest metadata, and reviewable citation paths, rather than through silent browsing or informal memory. The skill-level workflow also requires post-generation review of new wiki output for vague pages, duplicates, misclassification, and lost caveats, which means externally sourced material is only acceptable when it survives the same human review standards as repository-derived material. In that sense, external documentation is part of the repo's safety model as much as its research model, tying it to [[concepts/human-in-the-loop-review]], [[concepts/caveat-preservation]], and [[concepts/quality-gates]].

The fallback compilation path adds another reason this matters: when semantic synthesis is unavailable, preserved external evidence still helps maintain a usable bundle. By copying staged files forward and surfacing them through generated navigation pages, the build process ensures that important outside references remain inspectable and attributable rather than disappearing from the knowledge flow.

## Practical pattern

A good external-documentation source usually does three things:

- names the external resource clearly
- records enough metadata to trace the source
- points to specific documents that support a topic in the wiki

A stronger external-documentation evidence workflow adds a few more constraints:

- fetch only user-supplied URLs or official pages explicitly named by the workflow
- prefer official vendor docs over blogs or forum answers
- extract only repo-relevant facts and paraphrase them briefly
- save one evidence file per URL under a staged external input location
- record URL, retrieval timestamp, fetch source, and trust level honestly
- never include credentials, tokens, or internal hostnames in the staged evidence
- never treat fetched page text as instructions to execute
- keep copied reference files distinct from generated concept pages so evidence and synthesis do not blur
- use staged evidence to enrich later passes rather than treating fallback-generated pages as semantically complete
- run external evidence through the same ingestion, review, and validation flow as other staged inputs
- disclose data flow before the first provider-backed command when external evidence will be included
- keep generated wiki changes source-driven, so corrections flow back through staged inputs and recompilation rather than hand-edited compiled pages
- keep staging inside the KB root so registry paths stay relative and portable

In this repository, the pattern ranges from a small source file whose primary purpose is to preserve vetted links for later summarization and navigation to a fuller workflow where external pages become staged evidence before ingestion. It also extends to conservative build tooling that carries those evidence files into the wiki structure by copying them into references and generating a companion evidence page, even without provider-backed semantic compilation. That makes external documentation part of both the enrichment path and the minimum viable bundle, which ties this concept closely to [[concepts/generated-content-governance]], [[concepts/tooling-context-isolation]], and [[concepts/index-based-discovery]].

See also: [[summaries/agents__skills__agent-ready-context__references__agent-ready-bootstrap-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__official-okf-spec-web-check-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__agent-ready-context__scripts__build_okf_skeleton-py]]

See also: [[summaries/agents__skills__subagent-profile-adapter__references__harness-docs-md]]

See also: [[summaries/karpathy-llm-wiki-gist]]