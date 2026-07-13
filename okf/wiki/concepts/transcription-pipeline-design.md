---
type: "Concept"
sources: ["summaries/agents__skills__graphify__SKILL-md.md", "summaries/agents__skills__graphify__references__update-md.md", "summaries/agents__skills__graphify__references__transcribe-md.md"]
description: "Designing media-to-text stages so mixed inputs become usable downstream."
---

# Transcription Pipeline Design

Transcription pipeline design is the practice of inserting a structured media-to-text step into a larger ingestion workflow so audio or video content can be processed like ordinary documents. In this wiki, the concept is illustrated by [[summaries/agents__skills__graphify__references__transcribe-md]] and reinforced by [[summaries/agents__skills__graphify__references__update-md]], which together show how Graphify handles detected video files before semantic analysis and during incremental updates.

## Core idea

Some repository inputs cannot be consumed directly by document-oriented analysis stages. A transcription pipeline converts those inputs into text artifacts early enough that downstream components can treat them as standard docs, while preserving clear boundaries between detection, transformation, and later semantic processing. This makes transcription a form of [[concepts/document-normalization]] for multimodal inputs and supports [[concepts/repository-ingestion]] workflows that must absorb mixed file types.

The update flow adds an important refinement: transcription is not just a preprocessing convenience, but a correctness requirement when changed media appears in an incremental run. Raw video or audio paths must be replaced with transcript paths before semantic subagents run, or later stages receive unreadable media inputs instead of text.

## Triggered, not universal

A key design principle is that transcription should be conditional rather than always-on:

- Run the step only when file detection reports one or more video files.
- Skip it entirely when no relevant media is present.
- Keep the transcription guidance unloaded for corpora that do not need it.
- In incremental mode, trigger transcription only for newly added or modified media files rather than the whole corpus.

This selective activation reflects [[concepts/minimal-tool-scoping]] and [[concepts/tool-boundaries]]: expensive or specialized tooling should be invoked only when the corpus structure justifies it. It also aligns with [[concepts/incremental-compilation]], where only changed inputs should be reprocessed.

## Prompting from corpus context

The source document emphasizes that transcription quality can be improved by deriving an initial Whisper prompt from the repository's own detected themes. The process is:

- Read top labels from detect output or a prior analysis artifact.
- Compose a short one-sentence domain hint from those labels.
- Append the instruction to use proper punctuation and paragraph breaks.
- Fall back to a generic prompt if the corpus contains only video files and no other docs or code.

This is a concrete case of [[concepts/domain-adaptive-prompting]]. Instead of treating transcription as a fully generic speech-to-text step, the pipeline uses available repository evidence to bias output toward the corpus domain.

## Pipeline artifacts and handoff

The design in [[summaries/agents__skills__graphify__references__transcribe-md]] depends on explicit intermediate artifacts:

- detect output lists media files to transcribe
- environment variables carry the selected model and initial prompt
- a transcript manifest records generated transcript paths
- those transcript paths are appended to the docs list before later dispatch

The update flow makes this handoff stricter. During an incremental run, detected changed files are first written into an intermediate detection artifact, then any changed video files are transcribed, and then that detection state must be rewritten so transcript paths move into the document set while media paths are removed from the video set. This artifact-driven handoff supports [[concepts/generated-artifact-adoption]] and [[concepts/incremental-compilation]]. Each stage writes concrete outputs that later stages can consume without recomputing earlier decisions.

## Operational safeguards

The reference documents highlight implementation details that matter for robust pipeline design:

- export environment variables so child processes inherit configuration
- write machine-readable JSON from Python rather than relying on shell redirection
- keep progress output separate from structured outputs
- continue processing even if transcription fails for an individual file
- print clear counts showing how many transcripts were produced
- rewrite incremental detection artifacts after transcription so downstream stages see text inputs rather than raw media paths
- run transcription before semantic extraction in update mode whenever changed media is present

These choices support [[concepts/graceful-degradation]], [[concepts/data-flow-disclosure]], and [[concepts/generated-content-governance]]. The system makes its transformations visible, keeps artifacts trustworthy, and avoids total pipeline failure when only part of the media set succeeds.

## Why it matters

Without a transcription stage, video and audio files remain opaque to document-centric knowledge extraction. A well-designed transcription pipeline lets multimodal repositories participate in the same indexing, summarization, and graph-building flow as text sources. In incremental workflows, it also prevents unreadable media files from leaking into downstream semantic stages and ensures that changed media can be merged back into the graph using the same document-oriented machinery as ordinary text. This extends ingestion coverage while preserving deterministic stage boundaries and explicit artifact exchange.

## Related pages

- [[summaries/agents__skills__graphify__references__transcribe-md]]
- [[summaries/agents__skills__graphify__references__update-md]]
- [[concepts/domain-adaptive-prompting]]
- [[concepts/document-normalization]]
- [[concepts/repository-ingestion]]
- [[concepts/generated-artifact-adoption]]
- [[concepts/incremental-compilation]]
- [[concepts/graceful-degradation]]
- [[concepts/tool-boundaries]]
- [[concepts/minimal-tool-scoping]]

See also: [[summaries/agents__skills__graphify__SKILL-md]]