# Privacy, data flows, and air-gapped operation

The pipeline must give the user full transparency and control over where their source code and documents go. These are commitments, not suggestions:

1. **Transparency**: before any step that sends repository content off the machine, announce the tool, provider/endpoint, model, credential source, and what content will be sent, then proceed only with consent.
2. **Explicit routing**: never let a tool silently choose a provider. OpenKB uses explicit litellm config; graphify gets an explicit `--backend` when non-code sources are processed.
3. **Independence**: a fully local air-gapped path and a zero-LLM path must always remain available.
4. **No telemetry tooling**: the pinned toolchain must not phone home. Re-verify the claims below whenever a pin moves.

## What leaves the machine, stage by stage

| Stage | Data involved | Destination | Fully local option |
| --- | --- | --- | --- |
| `check_prereqs`, source pack, skeleton, validators | repo files | nowhere (local scripts) | already local |
| `graphify` on code files | source code AST | nowhere; tree-sitter runs locally | already local |
| `graphify` on docs/PDFs/images/video | document content | the selected LLM backend | `--backend ollama` |
| `openkb add/recompile/lint/query/chat/skill/deck` | staged sources, wiki pages, prompts | configured litellm provider | `model: ollama/<model>` |
| Long PDFs through PageIndex | PDF content | local PageIndex by default; PageIndex Cloud only when `PAGEINDEX_API_KEY` is set | leave `PAGEINDEX_API_KEY` unset |
| `openkb add <url>` | URL and fetched page content | the target URL, then configured provider during compilation | skip URL ingestion; stage local files |
| external docs evidence via web tool | the URLs fetched | the fetched sites | skip, or user provides files locally |
| OKF spec baseline refresh | nothing sensitive (reads public spec) | github.com | skip; embedded baseline |

Cost/cache files (`graphify-out/cost.json`, `graphify-out/cache/`, `okf/output/`, `okf/wiki/reports/`) are local-only or generated artifacts; keep them gitignored so they never leak environment details.

**A different leak class: local files into committed git history, not into an LLM provider.** `graphify update` merges only `.gitignore` and `.graphifyignore` when deciding what to scan (verified by reading `graphify/detect.py`'s `_load_graphifyignore`) — it has no visibility into `.git/info/exclude` or a user's global excludesfile. A harness-local file excluded only through one of those two (never through `.gitignore`/`.graphifyignore`) is still scanned, and if it produces real graph nodes, that content can be baked into `graphify-out/graph.json`/`GRAPH_REPORT.md` — files this pipeline commits and pushes, visible to every clone and collaborator. This is not egress to a provider; it is local-only content crossing into shared, committed history. See "Local-artifact leakage risk" in `references/workflow.md` for the pre-commit review step and the reactive (never preemptive) fix.

**Rule — staging must live inside the KB root (`okf/.okf-build/input/`), never outside.** Rationale (verified openkb 0.4.4 and main, 2026-07-10): `okf/.openkb/hashes.json` stores each ingested document's `path` metadata KB-relative only for files *inside* the KB root; anything ingested from outside is recorded as an **absolute machine path** — leaking the username and directory tree into a committed file and producing cross-developer diff noise. Dedupe and determinism are hash-keyed and unaffected either way, but never point `--out` or `openkb add` at a staging directory outside `okf/`. If a registry entry with an absolute path is ever found (pre-relocation KB, or a stray outside add), the document was staged from outside the KB root: re-stage inside and re-add it, or rebuild the KB — do not hand-edit the registry outside a deliberate, hash-preserving migration.

## Telemetry status of the toolchain

- `graphify` (graphifyy): upstream states **"no telemetry, no usage tracking, no analytics"**; video/audio transcription runs locally via faster-whisper; `cost.json` is documented as local-only. (Verified against <https://github.com/safishamsi/graphify>, 2026-07-05.)
- `openkb`: verified against <https://github.com/VectifyAI/OpenKB> source, openkb 0.4.4, retrieved 2026-07-10: no analytics, telemetry, or update checks; openai-agents tracing is disabled at startup. Network egress is only the configured LLM provider via litellm, optional PageIndex Cloud when `PAGEINDEX_API_KEY` is set, URL fetches for user-approved `openkb add <url>`, and the user's browser for `openkb feedback`.
- `uv`: no telemetry per upstream documentation.

There is nothing to disable for OpenKB telemetry. The privacy-relevant toggles are leaving `PAGEINDEX_API_KEY` unset for local-only PDF handling and avoiding `openkb add <url>` unless the user approves the URL fetch. `openkb use` writes only local global config under `~/.config/openkb/global.yaml`.

Re-check these claims from the upstream repositories whenever a pinned version changes, and record the check date next to the pin.

## Explicit backend rule for graphify

graphify can auto-detect a provider from exported API keys. On a developer machine with several keys exported, that silently routes documents to a provider the user never chose. Therefore:

- **Always pass an explicit `--backend <provider>`** when non-code sources are processed; never rely on key auto-detection.
- For code-only repositories, prefer code-only extraction: it needs no key and nothing leaves the machine.
- Announce the chosen backend before running.

When graphify does need a key (verified 0.9.10: **only** when semantic extraction of docs/papers/images is explicitly routed through an authenticated backend — code extraction is AST-only, `graphify query` is fully local, and community labels have a deterministic hub-name fallback), graphify reads process env only (`OPENAI_API_KEY`/`OLLAMA_API_KEY`); it loads no `.env` itself. Use the **sourcing pattern** so the secret persists in the gitignored file and never crosses the agent's context:

```bash
# POSIX shells
set -a; . okf/.env; set +a; graphify extract <docs-path> --backend openai --model "$OPENAI_MODEL"
```

```powershell
# PowerShell (Windows)
Get-Content okf/.env | ForEach-Object { if ($_ -match '^\s*([^#=]+)=(.*)$') { Set-Item -Path "env:$($Matches[1].Trim())" -Value $Matches[2].Trim() } }
graphify extract <docs-path> --backend openai --model "$env:OPENAI_MODEL"
```

The agent may compose these commands but must never `cat`, `echo`, `printenv`, or otherwise surface the file or its variable values in output. Do not use this pattern for the standard pipeline — it never needs a graphify key.

Structural guarantees worth knowing when reasoning about secrets: `build_okf_source_pack.py` stages only `git ls-files` output, so an untracked gitignored `.env` can never enter the KB; and graphify's detect stage treats `.env` files as secret stores to exclude from extraction. Neither pipeline can ingest credentials even by accident.

## Air-gapped recipe

`okf/.openkb/config.yaml`:

```yaml
model: ollama/<local-model>
language: en
litellm:
  timeout: 1200
  drop_params: true
```

Also in air-gapped mode:

- do not set `LLM_API_KEY`, provider-specific API keys, or `PAGEINDEX_API_KEY`;
- skip URL ingestion and web baseline checks;
- run graphify with `--backend ollama` when non-code sources are processed;
- let the user provide external docs as local files under `okf/.okf-build/input/external/`.

**Zero-LLM fallback**: `build_okf_skeleton.py` writes a conservative bundle directly to `okf/wiki/`. It is degraded mode: report the limitation, hand edits are permitted, and reconcile later with OpenKB `lint`/`recompile` if OpenKB is adopted.

## Disclosure before first compile

Before the first OpenKB LLM-backed command (`add`, `recompile`, `lint`, `query`, `chat`, `skill`, or `deck` — `lint` includes an LLM knowledge check over wiki content, not only structural checks) or graphify run over non-code sources, state in one short block: tool, provider, model, endpoint, credential source (shell env, `okf/.env`, or `~/.config/openkb/.env`), and what content is being sent (for example `okf/.okf-build/input` staged sources). Repeat the disclosure when any of those change. Record the chosen provider policy in the target `AGENTS.md` so future agents follow the same routing.
