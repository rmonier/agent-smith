---
type: "Summary"
description: "Reference for adding URLs and watching folders in graphify workflows."
doc_type: short
full_text: "sources/agents__skills__graphify__references__add-watch-md.md"
---

# Add URL and Watch Folder Reference

This document is an operational reference for two non-default `graphify` workflows: adding a remote resource to the corpus with `/graphify add <url>`, and starting a background folder watcher with `--watch`.

## Main Purpose

The file explains how to:
- fetch a URL, ingest it into `./raw`, and then run the graph update pipeline
- launch a file watcher that reacts differently to code changes versus document or image changes
- handle ingestion errors explicitly rather than proceeding silently

## `/graphify add` Workflow

The add flow runs a Python one-liner through the configured `graphify` interpreter and calls an ingest function on a supplied URL.

Key behavior:
- the ingested resource is saved into `./raw`
- optional `author` and `contributor` values should be filled from user input when available
- `ValueError` and `RuntimeError` are treated as user-visible failures
- after a successful save, the system should automatically run the `--update` pipeline to merge the new material into the existing graph

This reflects a workflow built around repository ingestion, error handling, and incremental update pipelines such as [[concepts/incremental-graph-maintenance]].

## Supported URL Types

The ingest step auto-detects several kinds of remote resources:
- video URLs such as YouTube, downloaded as audio and transcribed on a later run
- Twitter/X posts, fetched through oEmbed and stored as Markdown
- arXiv entries, stored as abstract plus metadata in Markdown
- PDFs, downloaded directly
- images such as PNG, JPG, and WebP, downloaded for later vision extraction
- general webpages, converted to Markdown with `html2text`

This points to a multimodal intake pipeline spanning [[concepts/web-evidence-ingestion]] and [[concepts/multimodal-url-ingestion]].

## `--watch` Workflow

The watch mode starts a background process over a target folder using `graphify.watch` with a debounce interval.

Core behavior:
- code-file changes trigger immediate AST extraction, graph rebuild, and clustering
- this code-only path does not require LLM-based semantic re-extraction
- docs, papers, or image changes create a `graphify-out/needs_update` flag
- when semantic sources change, the user is prompted to run `/graphify --update` manually

The watcher is therefore split between a fast structural path for source code and a deferred semantic path for richer materials, connecting to file watching, AST extraction, and [[concepts/incremental-graph-maintenance]].

## Debounce and Agentic Use

The default debounce is 3 seconds, intended to wait for file activity to settle before rebuilding. This is especially useful when many agents or parallel processes write files in bursts.

The document recommends:
- keeping `--watch` running in a background terminal during agentic workflows
- relying on automatic rebuilds between waves of code changes
- performing a manual `/graphify --update` after waves that also modify docs, notes, or images

This operational guidance relates to debouncing, background automation, and [[concepts/skill-based-automation]].

## Key Takeaways

- adding a URL is an explicit ingest-and-update workflow, not part of the default build
- watch mode distinguishes between syntactic code updates and semantic document updates
- immediate rebuilds are optimized for code files, while richer content sets a deferred update flag
- the document is primarily a runbook for automation around corpus growth and graph freshness

## Related Concepts
- [[concepts/action-oriented-documentation]]
- [[concepts/knowledge-graph-analysis]]
- [[concepts/repository-ingestion]]
- [[concepts/dependency-management]]
- [[concepts/graceful-degradation]]

## Entities
- [[entities/graphify]]
- [[entities/graphifyy]]
- [[entities/uv]]
