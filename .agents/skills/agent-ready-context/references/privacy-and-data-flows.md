# Privacy, data flows, and air-gapped operation

The pipeline must give the user full transparency and control over where their source code and documents go. These are commitments, not suggestions:

1. **Transparency**: before any step that sends repository content off the machine, announce the tool, provider/endpoint, model, credential source, and what content will be sent, then proceed only with consent.
2. **Explicit routing**: never let a tool silently choose a provider. OpenWiki's provider/model route is the user's explicit choice, configured through its own provider selection; the skill never switches it, including on quota or auth failure.
3. **Independence**: a fully local air-gapped path and a zero-LLM path must always remain available.
4. **No telemetry tooling**: the pinned toolchain must not phone home. Re-verify the claims below whenever a pin moves.

## What leaves the machine, stage by stage

| Stage | Data involved | Destination | Fully local option |
| --- | --- | --- | --- |
| `check_prereqs`, staging dry-run, skeleton, validators | repo files | nowhere (local scripts) | already local |
| OpenWiki install | package/source requests, native-dependency assets | configured npm registry, official upstream, disclosed asset endpoints | defer install; continue zero-LLM work |
| OpenWiki login/refresh | the selected provider's auth protocol data | that provider's audited auth endpoints | local OpenAI-compatible endpoint needs no hosted login |
| OpenWiki `code --init`/`--update` (staged) | filtered staged corpus, accepted staged wiki, prompts | the selected provider's audited model endpoints | `openai-compatible` provider against a local engine |
| external docs evidence via web tool | the URLs fetched | the fetched sites | skip, or user provides files locally |
| `prepare_external_evidence.py` (markitdown, local files) | user-provided local documents | nowhere (local conversion, verified against installed package source) | already local |
| `prepare_external_evidence.py` (markitdown, YouTube URLs only) | the YouTube URL given as `--source` | YouTube's transcript API | skip; provide a transcript as a local file instead |
| OKF spec baseline refresh | nothing sensitive (reads public spec) | github.com | skip; embedded baseline |

Keep generated artifacts (`okf/.okf-build/`, local producer state under `okf/.openwiki/`, caches) gitignored so they never leak environment details.

**Staging is an explicit Git-tracked allowlist, not an ignore-respecting crawl.** The corpus contains tracked regular files minus canonical memory (`okf/`, with the `okf/external/` evidence carve-out), the adapter's build root, generated caches, and secret-like filenames; anything else that must not reach the provider is excluded per run with `--exclude`. The accepted wiki enters the stage only through the wrapper's separate prior-memory channel (minus the user-scoped `tooling/` overlay), so it cannot cite itself as repository evidence, and every generated citation must resolve within the immutable pre-run stage. Evidence uses repository-relative paths only; an absolute path or username in evidence is a hard failure.

## Telemetry status of the toolchain

- `openwiki`: the pinned candidate's tracing/observability integrations (LangSmith, LangChain tracing, OTEL) stay disabled through their documented environment switches; network egress is only the selected provider route and disclosed install-time asset endpoints. OpenWiki ships opt-out anonymous CLI run telemetry (PostHog; event-level per its documentation, never contents/paths/prompts); the staged runner exports `OPENWIKI_TELEMETRY_DISABLED=1` and `DO_NOT_TRACK=1` by default, so staged runs stay silent unless the user opts in. Re-audit at every pin move.
- `fnm`: no telemetry per upstream documentation.
- `uv`: no telemetry per upstream documentation.
- `markitdown`: no telemetry, verified at pin time against the installed package source, not just docs. Local-file conversion never touches the network: its HTTP session only activates on the URI-conversion code path, which local paths never reach — confirmed by reading `_markitdown.py`/`convert_local`, not assumed. Two verified exceptions, both handled explicitly by the wrapper: YouTube URLs are passed through with a printed disclosure (markitdown fetches the transcript directly — no local-file equivalent exists); audio sources (`.wav`/`.mp3`/`.m4a`/`.mp4`) are rejected outright, because markitdown's transcription silently calls the Google Web Speech API with the actual audio content and no opt-out when the `[audio-transcription]`/`[all]` extras are installed. Re-verify this source-level audit at every pin move, and record the check with the pin.

Re-check these claims from the upstream repositories whenever a pinned version changes, and record the check date next to the pin.

## Credentials are hands-off

OpenWiki resolves its credential state under the invoking user's home (`~/.openwiki/.env`). The staged-run wrapper sets only the child process home to `<repo>/okf` (`USERPROFILE` on Windows, `HOME` on POSIX), so OpenWiki itself reads and writes ignored `okf/.openwiki/.env`. The agent may name the path and variable names but must never read, print, parse, validate, copy, migrate, back up, or write credential values, and must not inspect process environment values for secrets. The upstream CLI — never an automation wrapper — owns login: browser, callback, token exchange, and file write.

Structural guarantees worth knowing when reasoning about secrets: the staged corpus contains only `git ls-files` output minus secret-like filenames, so an untracked gitignored `.env` can never enter the stage; and the wrapper never reads provider state at all.

## Air-gapped recipe

Route OpenWiki through a local OpenAI-compatible inference endpoint (Ollama, llama.cpp, vLLM, or an equivalent engine) via its stock `openai-compatible` provider: point the provider's base-URL variable at the endpoint, set the model id the engine serves, and supply whatever key value the endpoint expects. Also in air-gapped mode:

- do not set hosted-provider API keys;
- skip URL ingestion and web baseline checks;
- let the user provide external documents as local files prepared into `okf/external/` evidence pages.

**Zero-LLM fallback**: `build_okf_skeleton.py` writes a conservative bundle directly to `okf/wiki/`. It is degraded mode: report the limitation, hand edits are permitted, and reconcile later with a staged OpenWiki update when a provider becomes available.

## Disclosure before first provider call

Before the first provider-backed OpenWiki run, state in one short block: tool pin, isolated execution root (`okf/.okf-build/<run-id>/worktree`, never the live worktree), provider/model, endpoint family, credential source (location only, values not inspected), what content is being sent (the filtered staged corpus and staged openwiki pages), tracing state, and the cost boundary. Repeat the disclosure when any of those change. Installation consent, login consent, and provider-egress consent remain distinct. Keep provider/model choice in OpenWiki's local, ignored state so committed files stay provider-neutral.

Before long calls, persist plan/evidence progress. On quota, auth, or routing error, preserve the isolated stage, record only a redacted error category, leave live memory untouched, and stop. Never retry unboundedly or change providers silently.
