---
type: "Concept"
sources: ["summaries/agents__skills__graphify__references__extraction-spec-md.md", "summaries/agents__skills__graphify__references__add-watch-md.md"]
description: "Ingesting many URL types into a shared corpus through type-aware handling."
---

# Multimodal URL Ingestion

Multimodal URL ingestion is the practice of accepting many kinds of remote URLs and converting each into a corpus-ready local artifact through type-aware handling. In this workflow, a single add command can fetch a webpage, PDF, image, social post, academic paper, or video-related URL and normalize it into files that can later be incorporated into a knowledge graph.

This concept is illustrated by [[summaries/agents__skills__graphify__references__add-watch-md]], which describes a `graphify` add flow that fetches a URL, saves the result into `./raw`, and then runs an update pipeline so the new material becomes part of the existing graph.

## Core Idea

A multimodal ingestion pipeline does not treat every URL as generic web text. Instead, it detects the resource type and chooses a handling strategy appropriate to that medium:

- general webpages are converted to Markdown
- PDFs are downloaded directly
- images are downloaded for later vision-based extraction
- arXiv links are turned into metadata and abstract summaries
- Twitter/X links are converted into Markdown containing post text and author information
- video URLs such as YouTube are downloaded as audio inputs for later transcription

This makes the URL itself an entry point into a broader [[concepts/repository-ingestion]] or corpus-building workflow rather than just a pointer to external content.

## Why It Matters

Type-aware URL ingestion improves downstream knowledge extraction in several ways:

- it preserves more useful structure than flattening all links into plain text
- it supports multiple media types within one ingestion interface
- it separates fetch-time acquisition from later extraction steps such as transcription or vision analysis
- it enables consistent graph updates after new remote material is added

In practice, this supports [[concepts/web-evidence-ingestion]] by making external material easier to capture in reusable local form. It also complements [[concepts/document-normalization]] because different source types are converted into standard local artifacts such as Markdown, PDF, image, or text files.

## In the Graphify Workflow

In the source document, the add flow runs an ingest function over a supplied URL and writes the resulting artifact into `./raw`. After a successful save, the workflow automatically runs an update pass so the new source is merged into the graph. This connects multimodal acquisition directly to [[concepts/incremental-graph-maintenance]].

The source also shows that some media types are only partially processed at ingest time:

- videos are acquired first and transcribed on a later run
- images are downloaded first and interpreted on a later run
- text-like resources such as webpages, tweets, and arXiv records can often be normalized immediately

This staged behavior aligns with [[concepts/incremental-compilation]], where acquisition and semantic extraction happen in separate passes.

## Operational Characteristics

Multimodal URL ingestion usually includes a few important operational rules:

- the system auto-detects supported URL classes
- ingestion failures are surfaced explicitly rather than ignored
- saved outputs are placed in a predictable local corpus directory
- successful ingestion triggers follow-on processing to keep the graph current

These traits reinforce [[concepts/safe-automation]] and [[concepts/provenance-tracking]], since fetched resources become concrete local artifacts with a clear path into the knowledge system.

## Relationship to Other Concepts

Multimodal URL ingestion overlaps with several adjacent ideas:

- [[concepts/web-evidence-ingestion]]: focuses on capturing external web material as evidence
- [[concepts/document-normalization]]: focuses on converting heterogeneous inputs into standard forms
- [[concepts/incremental-graph-maintenance]]: focuses on updating the graph after new material arrives
- [[concepts/incremental-compilation]]: explains why some content is fetched now and semantically processed later
- [[concepts/knowledge-graph-analysis]]: benefits from richer, normalized source material entering the graph

## Source Basis

The main source for this concept is [[summaries/agents__skills__graphify__references__add-watch-md]], which documents URL ingestion behavior for a graph-building workflow and enumerates the supported resource types and post-ingestion update behavior.

See also: [[summaries/agents__skills__graphify__references__extraction-spec-md]]