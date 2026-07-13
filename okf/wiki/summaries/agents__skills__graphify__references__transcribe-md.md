---
type: "Summary"
description: "Guidance for transcribing detected video/audio into docs for graphify."
doc_type: short
full_text: "sources/agents__skills__graphify__references__transcribe-md.md"
---

# Summary

This reference document defines Graphify's optional transcription step for corpora that include detected video files. It explains when to load the guidance, how to derive a Whisper initial prompt from detected corpus themes, how to run transcription, and how to feed resulting transcripts back into the document-processing pipeline.

## Purpose

The document adds a preprocessing stage for media inputs that cannot be read directly. When `detect` reports one or more video files, those files should be transcribed to text first and then treated as normal docs during later ingestion steps.

## Key points

- The transcription step is conditional: skip it entirely if `detect` found zero `video` files.
- Video and audio content must be converted into transcript files before semantic processing.
- Transcript files become part of the docs list before dispatching semantic subagents in the later pipeline stage.
- The system should report how many transcripts were created and continue even if some files fail.

## Prompt construction strategy

A central idea is to create a domain-aware Whisper prompt from the corpus itself:

- Read top "god node" labels from `graphify-out/.graphify_detect.json` or a prior analysis file.
- Synthesize a one-sentence domain hint directly from those labels rather than making a separate API call.
- Append the formatting instruction: `Use proper punctuation and paragraph breaks.`
- If the corpus contains only video files and no other docs or code, fall back to the generic formatting prompt alone.

Examples in the source show prompts derived from topics like transformer research or Kubernetes/Helm operations. This reflects a broader pattern of [[concepts/domain-adaptive-prompting]] and [[concepts/transcription-pipeline-design]].

## Execution details

The document specifies environment-based configuration for the transcription step:

- `GRAPHIFY_WHISPER_MODEL` must be `export`ed so the child Python process can read it.
- `GRAPHIFY_WHISPER_PROMPT` must also be `export`ed with the generated domain hint.
- Default Whisper model is `base`, unless the user provided `--whisper-model <name>`.

The provided Python command:

- Loads detected video file paths from `graphify-out/.graphify_detect.json`
- Reads the prompt from `GRAPHIFY_WHISPER_PROMPT`
- Calls `graphify.transcribe.transcribe_all(video_files, initial_prompt=prompt)`
- Writes transcript paths as JSON to `graphify-out/.graphify_transcripts.json`
- Sends progress output to stderr to avoid corrupting JSON output

This captures an implementation concern around pipeline artifact management: machine-readable outputs should be written explicitly by Python rather than mixed with shell stdout.

## Operational behavior

After transcription completes:

- Read transcript paths from `graphify-out/.graphify_transcripts.json`
- Merge transcript files into the docs list for subsequent processing
- Print a status message such as `Transcribed N video file(s) -> treating as docs`
- Warn on per-file transcription failures but continue processing remaining files

## Notable implementation constraints

- The guidance is only relevant when media was detected, so loading is intentionally gated.
- Exporting environment variables is mandatory because a child Python process performs the transcription.
- JSON output must be written from Python code, not shell redirection, because progress output from Whisper or helpers could otherwise corrupt the file.

## Related concepts

- [[concepts/transcription-pipeline-design]]
- [[concepts/domain-adaptive-prompting]]
- pipeline artifact management
- media-to-text preprocessing

## Related Concepts
- [[concepts/action-oriented-documentation]]
- [[concepts/graceful-degradation]]
- [[concepts/progressive-disclosure]]
- [[concepts/skill-based-automation]]

## Entities
- [[entities/graphify]]
- [[entities/openkb]]
- [[entities/uv]]
