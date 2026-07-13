# OpenKB provider configuration by harness

OpenKB uses litellm model names in `okf/.openkb/config.yaml`. Configure the model explicitly before any LLM-backed command and disclose which provider will receive staged content.

Provenance: verified against <https://github.com/VectifyAI/OpenKB> source, openkb 0.4.4, retrieved 2026-07-10. If behavior differs or pins move, re-verify with the web tool and trust current upstream source over this summary.

## Credential resolution order

OpenKB resolves credentials in this order:

1. Shell environment variables.
2. `<kb>/.env`, which is `okf/.env` in this repository policy.
3. `~/.config/openkb/.env`.

`LLM_API_KEY` is a universal key routed by litellm to the detected provider. Provider-specific variables such as `ANTHROPIC_API_KEY` also work. Keep every `.env` file gitignored; interactive `openkb init` can write API keys into `okf/.env` if a key is typed at its prompt. This skill's own init path, `scripts/init_openkb_noninteractive.py` (see `references/workflow.md`, "Non-interactive `openkb init`"), always takes the "enter to skip" branch and never writes `.env` — set credentials via the resolution order above instead.

**Key location is a setup question — ask the user.** Both `.env` homes work (verified in cli.py: `okf/.env` loads first and wins over `~/.config/openkb/.env`; process env beats both). The global path is literally `~/.config/openkb/` on **every** OS, Windows included — openkb hardcodes `Path.home()/.config` and never uses `%APPDATA%`. Recommend `~/.config/openkb/.env` when one key serves every project (set once, user-wide); recommend `okf/.env` when this project needs its own provider or the user juggles several. Files beat env vars for persistence — suggest a `.env` first, exported variables as the fallback for CI/ephemeral shells. `check_prereqs.py` reports which homes exist (names only, never contents), warns when both exist (the project file wins), and notes when only the user-global one is in play.

**Credentials are hands-off for the agent.** Never ask for, generate, read, print, validate, copy, or move API keys, tokens, `.env` contents, or secret-manager entries; never create placeholder values; never inspect the environment to discover secrets. State only the required variable *name* and its expected *location*, verify the file is gitignored (by name), and continue: missing credentials never block the rest of the agentification — finish the non-secret configuration and report what the user must supply. If credentials are already present in the process, a minimal connectivity smoke test is allowed provided no variable, header, token, or secret-bearing response metadata is ever printed.

## Choosing a provider for the active harness

Work down this list, then ask the user when several options are viable. Do not assume the active harness is the provider the user wants to bill.

1. **Anthropic-based harness or key present**: use `model: anthropic/<model>` with `ANTHROPIC_API_KEY` or `LLM_API_KEY`.

   OpenKB 0.4.x has no Claude-Code/Anthropic OAuth provider and no equivalent of the old Claude local-login flow. Surface that difference to the user; Anthropic access is key-based through litellm.

2. **ChatGPT subscription**: use a `chatgpt/*` model. This is an OAuth subscription provider and does not need an API key.

3. **GitHub Copilot subscription**: use a `github_copilot/*` model and configure `litellm.extra_headers` with `Editor-Version` and `Copilot-Integration-Id`.

4. **OpenAI-compatible corporate gateway**: use litellm's `openai/<model>` naming and the gateway's base-url/key environment conventions. Keep the endpoint and credential source in the disclosure.

5. **Air-gapped local model**: use `ollama/<model>` or another local litellm runtime. For Ollama / LM Studio, upstream advises a long timeout and dropped unsupported params:

   ```yaml
   model: ollama/<local-model>
   language: en
   litellm:
     timeout: 1200
     drop_params: true
   ```

6. **No provider available**: use the zero-LLM skeleton generator and report that semantic completeness is limited.

Whatever the choice, the provider/model lives in `okf/.openkb/config.yaml` — which is **local and uncommitted**: every contributor picks their own LLM, and a committed provider choice would bind the whole team to one user's stack (and a committed `api_base` would leak internal endpoints). The committed surface is `okf/.openkb/config.yaml.example`: it carries the **project-shared** keys (`language`, `pageindex_threshold`, `entity_types` — these shape the compiled wiki and must match across contributors; `check_prereqs.py` warns on drift) plus commented provider-mode templates. New contributors copy it to `config.yaml` and choose a mode. As before, never copy the provider or model name into `AGENTS.md` or other orientation files: agent instructions stay LLM-vendor-agnostic.

## Backend connection modes

Configure only non-secret settings (endpoint, model, timeouts); credentials follow the hands-off rules above. Prefer the file (`config.yaml`) over env vars for persistence. OpenKB 0.4.4 facts that shape these modes: request timeout may be a root-level `timeout:` key or `litellm.timeout` (the nested value wins); the `litellm:` mapping passes module settings (`api_base`, `drop_params`, `num_retries`) through to LiteLLM; and `api_base` can alternatively come from LiteLLM's native env vars (`OPENAI_BASE_URL`/`OPENAI_API_BASE`, `OLLAMA_API_BASE`) when a file entry is undesirable.

OpenKB 0.4.4 also accepts an optional positive integer `concurrency:` cap for PageIndex indexing and concept/entity compilation. The compile stage otherwise defaults to five concurrent LLM calls. This does not parallelize separate documents in a directory add; tune it per provider and lower it if rate limits appear.

**Mode A — native Ollama endpoint, no API auth** (`model: ollama_chat/<model>`): set `litellm.api_base` to the **native** Ollama root — no `/v1`. No key anywhere.

**Mode B — authenticated OpenAI-compatible API** (`model: openai/<model-id>`): set `litellm.api_base` to the gateway URL, which normally **includes `/v1`**. The key is `LLM_API_KEY` in a `.env` home per the setup question above — never in this file.

**Mode C — OAuth provider** (`model: chatgpt/<model>` or `github_copilot/*`): no key, no `api_base` — do not add either "for consistency", and never rewrite the model to `openai/*`.

Graphify note: its Ollama backend speaks the OpenAI-compatible dialect at `<host>/v1` while openkb's `ollama_chat/` wants the native root — **same host, different paths**; one URL string cannot serve both. Graphify config is env-based (`OLLAMA_BASE_URL`, `OPENAI_BASE_URL`/`OPENAI_MODEL` — `GRAPHIFY_OPENAI_MODEL` wins when both are set; `GRAPHIFY_API_TIMEOUT`), needed **only** if graphify's semantic extraction is explicitly routed through an authenticated backend — see the conditional sourcing pattern in `references/privacy-and-data-flows.md`. The standard pipeline never needs it: code extraction is AST-only and `graphify query` is fully local. `GRAPHIFY_OLLAMA_NUM_CTX` is an override; graphify auto-derives context size (capped 131072) — set it only when a long-context model can beat the cap.

## Example config

The committed template is `okf/.openkb/config.yaml.example`; the local `okf/.openkb/config.yaml` looks like:

```yaml
model: anthropic/<model>   # per-user choice; modes A/B/C above
language: en               # project-shared - keep matching the example
pageindex_threshold: 20    # project-shared
concurrency: 5             # optional per-user LLM-call cap during ingest
timeout: 1200              # root-level request timeout (seconds)
litellm:
  drop_params: true
```

`language` defaults to `en` and can be set during init with `--language <code>`. `pageindex_threshold` is the PDF page count that triggers PageIndex handling. PageIndex runs locally by default; only setting `PAGEINDEX_API_KEY` opts into PageIndex Cloud and uploads the PDF for OCR/markdown conversion.

## Verification

After configuration, run cheap read-only checks first:

```bash
openkb --kb-dir ./okf status
openkb --kb-dir ./okf list
```

Then test with a small single-file `openkb --kb-dir ./okf add <file>` before bulk ingestion. Before that first add/recompile/lint/query/chat/skill/deck command, disclose tool, provider, model, endpoint, credential source, and what content will be sent. The full disclosure format lives in `references/privacy-and-data-flows.md`.

## Dependency-schema failures are not provider verdicts

If an LLM-backed command fails locally while constructing token-usage metadata — for example, a Pydantic error saying `InputTokensDetails.cache_write_tokens` is required — do not classify the provider, model, or KB content as broken and do not waive the failed phase. The failure is provider-independent: it lives in the tool environment's Python dependencies (OpenKB's pinned Agents SDK against a floating transitive `openai` client library) and reproduces with any configured provider, ollama included, because the Agents SDK builds its usage objects locally before any model call.

Check the known-incompatibility note in `references/openkb-lifecycle.md` (quality gate) first — it records the symptom signature, the upstream issue links, and the remedy: reinstall the tool with the transitive constraint recorded in its uv receipt, under the same consent rule as any tool install or upgrade. Re-verify against upstream source, issues, and release notes only when the observed error does not match that recorded signature. Never patch vendored tool skills, and never treat a structural-only lint report as a successful semantic lint.
