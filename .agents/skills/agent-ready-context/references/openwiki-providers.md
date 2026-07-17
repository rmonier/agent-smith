# OpenWiki provider policy

This skill is LLM-vendor-agnostic. OpenWiki owns provider and model selection
through its own configuration and login flow; the user chooses the route, and
this skill never hardcodes a provider, model, or endpoint into tracked project
files. The pinned tool is byte-for-byte upstream: provider adaptation belongs
in OpenWiki's stock configuration, never in vendor-source edits.

## Choosing a provider and model

- Use the provider/model the user already has access to and explicitly
  approves. Subscription OAuth routes and API-key routes are both acceptable
  when they are stock OpenWiki behavior and the user chose them.
- Never ask the user for a credential value, never set a provider API key
  yourself, and never enable a billable route the user did not select.
- Never switch provider or model silently — including on quota or auth
  failure. Report and stop instead.
- When pinning a new OpenWiki version, audit how it stores credentials and
  which endpoint families it calls for the selected route, and disclose those
  before first use.
- Root `AGENTS.md`, wiki pages, and committed templates stay provider-neutral;
  provider choice lives in OpenWiki's local, ignored state.

OpenWiki resolves provider settings from the process environment first, then
its local `.env`. Non-secret route-selection variables (provider, model id,
base URL, retry attempts) may be discussed and passed through the child
process environment; the credential value itself is filled only by the user
or by the stock login flow — never by the agent.

## Filling the local `.env`

There is deliberately no committed `.env` example file: `okf/.openwiki/` stays
gitignored in its entirety, and the agent never writes into the credential
home. Instead, this quick reference records the variable names OpenWiki reads
for provider routing; re-audit them against the pinned version at every pin
move. The user copies this shape into
the selected credential home — ignored `okf/.openwiki/.env` (default) or the
classic user-global `~/.openwiki/.env` (`--credential-home user`) — and fills
the values, or lets the stock login flow write its own OAuth state:

```dotenv
# Route selection (non-secret; may also be passed as child process env)
OPENWIKI_PROVIDER=<openai-chatgpt | anthropic | openai-compatible | ...>
OPENWIKI_MODEL_ID=<model id served by the selected route>
OPENWIKI_PROVIDER_RETRY_ATTEMPTS=<optional small integer>

# openai-compatible route only (local engines: Ollama, llama.cpp, vLLM, ...)
OPENAI_COMPATIBLE_BASE_URL=<http://host:port/v1>
OPENAI_COMPATIBLE_API_KEY=<user-filled; some local engines accept a non-secret placeholder>

# anthropic route only
ANTHROPIC_API_KEY=<user-filled>
# ANTHROPIC_BASE_URL=<optional endpoint override>

# OAuth routes (for example openai-chatgpt): no manual keys — run the stock
# login flow with user approval; it writes and owns its state in this file.
```

The agent may show this scaffold and name variables and locations, but never
fills in, reads back, or verifies credential values (see "Credentials are
hands-off" below).

## Local and air-gapped endpoints

OpenWiki's stock `openai-compatible` provider works with any inference engine
that serves the OpenAI v1 API on a user-controlled endpoint — for example
Ollama, llama.cpp, vLLM, or a local gateway. Point the provider's base-URL
variable at the endpoint, set the model id the engine serves, and supply
whatever key value the endpoint expects (some local engines accept a
non-secret placeholder). In this mode staged repository content never leaves
the machine; disclose the endpoint in the normal pre-run disclosure exactly
like a hosted provider, and prefer serial runs sized to the local engine's
capacity.

## Credentials are hands-off

The pinned upstream resolves its credential/OAuth state under the invoking
user's home (`~/.openwiki/.env`). By default the staged-run wrapper sets the
child process home to `<repo>/okf` — `USERPROFILE` on Windows, `HOME` on
POSIX — so OpenWiki itself reads and writes ignored `okf/.openwiki/.env`;
`--credential-home user` instead keeps the classic user-global
`~/.openwiki/.env`, with the same standing, for users who share one login
across repositories. The two homes are independent and never merged.
Locations and variable names may be discussed; values may not.

The agent must never:

- read, print, copy, move, validate, parse, diff, or back up the credential
  file;
- inspect process environment values to discover tokens or keys;
- create placeholder secrets or write credential state outside the ignored
  `okf/.openwiki/` home;
- run login/logout without the user's explicit approval;
- put credentials in `okf/.okf-build/`, evidence, logs, prompts, `AGENTS.md`,
  or committed config.

Authentication is a user-controlled setup action and the only interactive
bootstrap step: the stock CLI owns the browser window, callback, token
exchange, and file write. If no usable provider session is available, finish
local staging and deterministic validation, then stop before provider-backed
work and ask the user — do not probe alternate providers.

Keep `okf/.openwiki/` gitignored in its entirety.

## Tracing and telemetry

Keep optional observability integrations disabled unless the user explicitly
enables them, since traces can carry staged repository content:

```dotenv
LANGSMITH_TRACING=false
LANGCHAIN_TRACING_V2=false
OTEL_SDK_DISABLED=true
```

OpenWiki additionally ships opt-out anonymous CLI run telemetry (PostHog; per
upstream it records command/outcome/error category and setup-time
provider/connector names, never contents, paths, prompts, model ids, or IPs;
re-audit at every pin move). The staged runner exports both kill-switches by
default; the user opts in by setting them in their own environment:

```dotenv
OPENWIKI_TELEMETRY_DISABLED=1
DO_NOT_TRACK=1
```

Absence of a tracing key is never a reason to block a build or add one.

## Consent and disclosure before every provider phase

Before the first call, and again if anything changes, state:

```text
Tool: OpenWiki at exact pin <version-or-sha>
Execution root: <repo>/okf/.okf-build/<run-id>/worktree (never the live worktree)
Provider/model: <the user's selected route>
Endpoint family: <audited endpoints for that route>
Credential source: <selected credential home: ignored okf/.openwiki/.env (default) or user-global ~/.openwiki/.env> (values not inspected)
Content sent: the filtered staged repository corpus and staged openwiki pages
Tracing/telemetry: disabled
Cost boundary: <the user's selected route and its billing model>
```

Obtain explicit consent after this disclosure. Installation consent does not
imply egress consent, and egress consent does not imply permission to touch
the credential store.

## Quota and failure handling

Treat the provider's explicit quota/auth errors as authoritative. Before every
potentially long call:

1. persist completed local plan/evidence state;
2. keep the live wiki untouched;
3. record which run or phase is next;
4. bound retries.

On quota, OAuth, or routing failure, preserve the isolated stage and the exact
error category (without token or header data), then stop and report. Do not
loop on authentication and do not fall back to a different billable route.

## Verification order

Provider-backed verification is intentionally last:

1. Audit the pinned tool's credential storage, endpoints, and tracing defaults
   for the selected route.
2. Run the deterministic staging, validation, and no-op checks without
   credentials.
3. Ask for the separate interactive login when the user is ready.
4. After disclosure and consent, run one small staged smoke run and review its
   output before any full build.

No bulk run may be the first provider test.
