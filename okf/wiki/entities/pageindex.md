---
sources: ["summaries/agents__skills__openkb__SKILL-md.md", "summaries/agents__skills__openkb__references__wiki-schema-md.md", "summaries/agents__skills__openkb__references__commands-md.md", "summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md", "summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md"]
type: "Product"
description: "OpenKB's local-by-default PDF handling product with optional cloud mode."
---

# PageIndex

PageIndex is OpenKB's PDF handling product for larger inputs during ingestion, used when a document crosses the configured `pageindex_threshold`. It acts as a boundary in the document-processing pipeline: local by default, optionally cloud-backed through `PAGEINDEX_API_KEY`, and visible in OpenKB's user-facing document classification for long PDFs.

## What it is

Across the provider, privacy, workflow, repository overview, graph report, command reference, and wiki schema materials, PageIndex appears as a specialized part of the PDF-ingestion path rather than a general-purpose model provider like [[entities/anthropic]] or [[entities/chatgpt]]. The agent-ready workflow treats it as one of the privacy-relevant [[concepts/tool-boundaries]] in OpenKB processing that operators should understand before compiling repository knowledge.

The provider guidance defines `pageindex_threshold` as the PDF page-count switch that triggers PageIndex handling and states that PageIndex runs locally by default. Only setting `PAGEINDEX_API_KEY` opts into PageIndex Cloud, which uploads the PDF for OCR and markdown conversion. That makes PageIndex not just an implementation detail, but a named boundary in the system's [[concepts/data-flow-disclosure]] and [[concepts/privacy-preserving-tooling]] model.

The privacy guidance adds a more explicit stage-by-stage rule: long PDFs go through local PageIndex by default, and PageIndex Cloud is used only when `PAGEINDEX_API_KEY` is set. It also treats that cloud path as a consent-sensitive external egress route that must be disclosed before use, reinforcing PageIndex's role in [[concepts/explicit-provider-routing]] and [[concepts/offline-first-workflows]].

The agent-ready skill adds a stronger repository-level policy around that behavior. It says repository content leaves the machine only toward providers the user explicitly approved, and it names leaving `PAGEINDEX_API_KEY` unset as one of the privacy-relevant toggles for keeping PDF handling local. This makes PageIndex part of the repository's broader [[concepts/tooling-consent-and-pin-management]] and [[concepts/source-trust-levels]] posture, even though it sits specifically in the PDF-processing layer rather than the main LLM-provider path.

The command reference adds an operational boundary around where PageIndex shows up in the CLI surface. `openkb list` exposes long PDFs as `pageindex` in its user-facing type column, with `Pages` populated for those longer PDF inputs, while shorter documents appear as `short`. This means PageIndex is visible not only as an ingestion component but also as part of OpenKB's document inventory model, tied to [[concepts/index-based-discovery]] and [[concepts/document-normalization]] rather than raw file-extension reporting.

The wiki schema makes that classification model more concrete. It defines long PDFs as `wiki/sources/<doc>.json` files rather than Markdown documents, with content represented as a paginated array of page objects rather than a single file. It also states that these files can be very large and should be accessed by slicing specific pages instead of reading the entire file. This places PageIndex directly inside [[concepts/page-indexed-sources]] and connects it to the repository's handling of large compiled artifacts.

The same wiki schema also clarifies that `pageindex` is a reading and organization mode in the wiki, not merely an implementation detail. In `wiki/index.md`, document entries use `(short)` or `(pageindex)` as stable type tags, and long PDFs are represented through paginated source JSON rather than short-doc Markdown. That gives PageIndex a durable place in OpenKB's [[concepts/documentation-architecture]] and [[concepts/index-based-discovery]] model as well as its ingestion pipeline.

The command reference also reinforces that PageIndex belongs inside protected OpenKB-managed processing flows rather than direct manual editing. Because the skill must not directly modify content under the knowledge base's `wiki/` or `.openkb/` directories and must not autonomously run write commands, PageIndex remains part of a governed ingestion path inside [[concepts/safe-automation]] and [[concepts/tool-boundaries]] rather than a freeform conversion step.

The repository README adds that local-only PDF handling depends on leaving `PAGEINDEX_API_KEY` unset, and presents this as part of the project's support for air-gapped and privacy-preserving operation. The graph report reinforces this role indirectly: PageIndex is present as an entity in the compiled wiki structure, but it does not appear among the report's most connected nodes or main structural communities. That fits its role as a specific product in the ingestion stack rather than a repository-wide organizing abstraction. In graph terms, it is relevant to the repository's ingestion and privacy model without being one of the core navigation hubs described in [[summaries/graphify-report]].

The provider configuration reference sharpens the distinction between PageIndex and model-provider selection. OpenKB uses LiteLLM model names in `okf/.openkb/config.yaml`, but PageIndex is controlled separately through PDF-ingestion settings and the `PAGEINDEX_API_KEY` opt-in. That separation keeps PDF-processing policy distinct from choosing `anthropic/*`, `chatgpt/*`, `github_copilot/*`, `openai/*`, or `ollama/*` providers under [[concepts/provider-integration]] and [[concepts/explicit-provider-routing]].

The privacy-and-data-flows reference makes the routing and disclosure rules even more explicit. It says all repository-content egress must be announced before it happens, that tool routing must never silently choose a provider, and that PageIndex Cloud is simply one of the consent-sensitive routes in that broader policy. It also lists long PDFs through PageIndex as local by default, with cloud usage only when `PAGEINDEX_API_KEY` is set, and it frames that opt-in as part of the repository's general [[concepts/consent-first-tooling]], [[concepts/air-gapped-operation]], and [[concepts/privacy-preserving-tooling]] posture.

That same privacy guidance also distinguishes PageIndex from LLM provider selection by placing it in the PDF-ingestion stage rather than the model-routing stage. In practice, this means PageIndex is governed by the same disclosure and consent rules as other external-processing paths, but it is not chosen through litellm provider names. The document presents leaving `PAGEINDEX_API_KEY` unset as the key local-only toggle, and it treats PageIndex Cloud as a specialized OCR and markdown conversion path rather than a general inference backend.

## Key facts from the source

- OpenKB uses `pageindex_threshold` to decide when PDF input should trigger PageIndex handling.
- The example configuration sets `pageindex_threshold: 20`, so the threshold is based on PDF page count.
- The provider guidance explicitly describes PageIndex handling as part of `okf/.openkb/config.yaml` behavior.
- PageIndex runs locally by default.
- Setting `PAGEINDEX_API_KEY` opts into PageIndex Cloud.
- PageIndex Cloud uploads the PDF for OCR and markdown conversion.
- In privacy-sensitive or air-gapped operation, leaving `PAGEINDEX_API_KEY` unset preserves local-only PDF handling.
- The privacy guidance treats PageIndex Cloud as an optional external egress path that must be disclosed before use.
- The documented network behavior for larger PDFs is local PageIndex by default, with cloud use only when explicitly enabled through the API key.
- The privacy guidance identifies leaving `PAGEINDEX_API_KEY` unset as one of the key privacy-relevant toggles for keeping PDF handling local.
- Air-gapped operation explicitly depends on not setting `PAGEINDEX_API_KEY`, alongside avoiding URL ingestion and other external fetch paths.
- Before the first LLM-backed compile flow or any workflow whose outbound behavior changes, operators are expected to disclose tool, provider or endpoint, credential source, and what content is being sent; PageIndex Cloud belongs within that same [[concepts/data-flow-disclosure]] discipline when enabled.
- The provider guidance frames PageIndex Cloud as separate from litellm-backed model-provider configuration, which keeps PDF-processing behavior distinct from LLM-provider selection under [[concepts/provider-integration]].
- The agent-ready skill explicitly states that repository content leaves the machine only toward providers the user explicitly approved, making PageIndex Cloud a consent-sensitive exception path rather than a default behavior.
- The skill also says the privacy-relevant toggles include explicit model/provider configuration and leaving `PAGEINDEX_API_KEY` unset for local PDF processing.
- The skill treats fetched or externally processed material as untrusted by default and requires disclosure before off-machine processing paths are used, which sharpens how PageIndex fits within [[concepts/prompt-injection-defense]] and [[concepts/knowledge-boundaries]].
- The README describes PageIndex Cloud usage as conditional and local handling as the baseline, reinforcing an [[concepts/offline-first-workflows]] posture for PDF ingestion.
- The README also treats `PAGEINDEX_API_KEY` as a clear operational switch in the stack's [[concepts/configuration-precedence]] and [[concepts/data-flow-disclosure]] model.
- The graph report includes PageIndex as a named entity in the repository knowledge graph, confirming that it is significant enough to surface in repository-wide structural analysis.
- The graph report does not place PageIndex among the highest-connectivity entities or major community hubs, which suggests its significance is localized to ingestion, privacy, and configuration concerns rather than to overall repository coordination.
- `openkb list` shows long PDFs as `pageindex` in the exposed `Type` column rather than surfacing a raw file extension.
- In `openkb list`, the `Pages` column is populated for these long PDF entries, making PageIndex-related handling visible in document inventory output.
- The command reference describes `pageindex` as the public display form for long PDFs, which situates PageIndex inside OpenKB's user-facing classification layer as well as its ingestion pipeline.
- The command guidance says agents should prefer direct inspection before expensive query flows, so PageIndex-related long PDFs are intended to remain discoverable through structured CLI listing rather than only through retrieval.
- The command reference forbids autonomous write commands and direct edits under `wiki/` or `.openkb/`, reinforcing that PageIndex behavior belongs to protected OpenKB-managed workflows rather than ad hoc manual mutation.
- The wiki schema defines long PDFs as `wiki/sources/<doc>.json` files rather than Markdown documents.
- Those source JSON files store a paginated array of objects with `page`, `content`, and `images` fields.
- The wiki schema explicitly recommends slicing specific pages from PageIndex JSON with `jq` instead of reading the entire file.
- The schema presents `pageindex` as one of the two stable document types shown in `wiki/index.md`, alongside `short`.
- In the schema's short-vs-long classification, PDFs at or above the threshold are treated as PageIndex documents, while shorter PDFs and non-PDFs remain `short`.
- The schema describes the `pageindex` label as a document-type convention used across summaries, sources, and index entries, not just as an internal backend term.
- The configuration reference shows that PageIndex is not the same as choosing a LiteLLM model provider, even though both live in the broader OpenKB runtime setup.
- The configuration reference also reinforces that local `config.yaml` choices are user-specific and uncommitted, while shared defaults live in the example file.
- The privacy-and-data-flows reference says the agent must announce the tool, provider or endpoint, model, credential source, and content being sent before any step that sends repository content off-machine.
- That same reference requires explicit routing for tools so they never silently choose a provider.
- It identifies leaving `PAGEINDEX_API_KEY` unset as the way to keep long-PDF handling local.
- It treats PageIndex Cloud as a consent-sensitive route that must be disclosed before use.
- It places PageIndex within a broader air-gapped and zero-LLM fallback policy for the knowledge base.

## Why it matters

PageIndex matters because it changes the data-flow and privacy posture of PDF ingestion. Local default behavior aligns with [[concepts/offline-first-workflows]] and [[concepts/privacy-preserving-tooling]], while enabling the cloud path introduces a different handling model that should be surfaced through [[concepts/data-flow-disclosure]] and handled with the same care as other external processing paths.

Within the broader repository compilation workflow, PageIndex also fits into [[concepts/provider-integration]], [[concepts/tool-boundaries]], and [[concepts/repository-ingestion]]. Its cloud opt-in behavior is governed by the same consent and configuration discipline reflected in [[concepts/tooling-consent-and-pin-management]] and [[concepts/configuration-precedence]].

The command guidance makes an additional boundary clearer on the read side: PageIndex is not only a backend PDF-processing component but also part of OpenKB's visible document classification surface, where long PDFs appear as `pageindex` in `openkb list`. That makes it relevant to [[concepts/index-based-discovery]], [[concepts/document-normalization]], and the practical distinction between user-facing document types and internal implementation details.

The wiki schema extends that point by showing that PageIndex also shapes how long documents are stored and navigated inside the compiled wiki. Because long PDFs are represented as paginated JSON sources and carried through the `pageindex` type in summaries and index entries, PageIndex is part of OpenKB's [[concepts/documentation-architecture]] as well as its ingestion runtime. Its importance is therefore both operational and structural.

The newer guidance also reinforces that PageIndex behavior sits inside a governed CLI workflow: discover the knowledge base first, inspect through read-only commands, and avoid autonomous mutation of OpenKB-managed state. That supports the repository's broader [[concepts/safe-automation]] and [[concepts/knowledge-base-discovery]] practices.

The provider guidance makes one additional boundary especially clear: PageIndex behavior is configured alongside other OpenKB runtime settings, but it is not the same thing as choosing a LiteLLM model provider. That distinction helps separate PDF-processing policy from LLM-provider selection and supports cleaner [[concepts/single-source-of-truth]] configuration practice.

The agent-ready skill strengthens this interpretation by placing PageIndex inside the repository's larger privacy and external-processing rules: off-machine handling is never assumed, disclosure is required when the route changes, and local execution remains the preferred baseline. That makes PageIndex a concrete example of how [[concepts/durable-context]] and operational policy meet at a specific product boundary.

The privacy-and-data-flows reference deepens that reading by making PageIndex part of a formal consent model: tool routing is explicit, egress is announced, and the local path must always remain available. In that framing, PageIndex is a product that supports both ordinary ingestion and privacy-preserving operation, depending on whether the cloud opt-in is enabled.

The graph report adds one more useful perspective: PageIndex is structurally visible but not central. That makes it a good example of a component whose operational importance comes from boundary conditions and risk posture, not from being a high-degree hub. In this wiki, it is best understood as part of the repository's [[concepts/repository-ingestion]], [[concepts/data-flow-disclosure]], and [[concepts/privacy-preserving-tooling]] story rather than as a top-level organizing concept.

## Context in this wiki

- Discussed in [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]
- Further constrained by [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]]
- Operationally framed by [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- Referenced in [[summaries/agents__skills__openkb__references__commands-md]] for CLI-visible document typing and command boundaries
- Defined structurally in [[summaries/agents__skills__openkb__references__wiki-schema-md]] for long-document storage, indexing, and page-sliced access
- Mentioned in [[summaries/README-md]] as part of air-gapped operation guidance
- Structurally situated by [[summaries/graphify-report]]
- Used by [[entities/openkb]]
- Distinct from the litellm-backed model provider path represented by [[entities/litellm]]

## Practical note

When PageIndex Cloud is enabled, the PDF is uploaded for OCR and markdown conversion, so operators should disclose that change in processing behavior before ingestion workflows begin. For local-only or air-gapped workflows, the guidance is to leave `PAGEINDEX_API_KEY` unset so long-PDF handling stays on-machine, preserving the default local processing model and avoiding unnecessary external data flow.

The provider guidance adds that this behavior should be understood as part of OpenKB's explicit runtime configuration, with PageIndex settings living in the same operational surface as other ingestion controls while remaining distinct from model-provider choice. The privacy guidance further specifies that local-only PDF handling is the default baseline and that PageIndex Cloud is activated only through an explicit credential-driven opt-in, which places it squarely inside the repository's [[concepts/data-flow-disclosure]] and [[concepts/privacy-preserving-tooling]] rules.

The command reference adds that agents can recognize PageIndex-related documents through `openkb list`, where long PDFs are displayed as `pageindex` and may carry a page count. That makes PageIndex discoverable through normal KB inspection without requiring costly query flows and keeps it aligned with [[concepts/index-based-discovery]] and [[concepts/cost-aware-tool-use]].

The wiki schema adds a practical reading rule: PageIndex-backed source files can be very large, so operators should inspect specific pages rather than loading the full JSON artifact. In practice, that means treating `pageindex` documents as page-addressable compiled sources, which reinforces [[concepts/page-indexed-sources]] and supports efficient, selective access to long PDFs.

The same command guidance further clarifies the operator expectation: repository content should leave the machine only toward explicitly approved providers, OpenKB-managed state should not be patched directly, and mutation commands should remain user-invoked. This keeps PageIndex aligned with the repository's [[concepts/safe-automation]] and [[concepts/preflight-checks]] habits rather than treating it as an invisible implementation detail.

The privacy-and-data-flows reference adds the last important operational boundary: before any run that changes outbound behavior, the agent must disclose the tool, provider or endpoint, model, credential source, and the content being sent. When PageIndex Cloud is in play, that disclosure applies to the OCR and markdown conversion path just as it does to any other external-processing route.

The graph report does not change the operating guidance, but it does confirm the scope of PageIndex's role: it is visible in the repository knowledge graph as a recognized product, while remaining secondary to broader hubs like validation, provenance, and workflow documentation. That makes it a focused entity page rather than a cross-cutting concept page.

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-lifecycle-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__workflow-md]]

See also: [[summaries/agents__skills__openkb__SKILL-md]]