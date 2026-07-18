# OpenWiki provider policy

This skill is LLM-vendor-agnostic. OpenWiki owns provider and model selection
through its own configuration and login flow; the user chooses the route, and
this skill never hardcodes a provider, model, or endpoint into tracked project
files. The pinned tool is byte-for-byte upstream: provider adaptation belongs
in OpenWiki's stock configuration, never in vendor-source edits.

## Choosing a provider and model

**Ask which provider first, before anything else in this reference applies**
— it determines which flow follows. Everything below was
established once, at pin-selection time, by running the CLI's own `/provider`
and `/model` menus and reading its own on-screen labels and notices; re-run
those same CLI-observable checks after any pin move, rather than assuming
this table still matches. As pinned (`openwiki 0.2.0`), the live `/provider`
menu lists these routes, in three distinct auth shapes, not two:

- **OAuth** — `openai-chatgpt` only. The onboarding step for this route is
  labeled "ChatGPT login"; every other route's onboarding step is instead
  labeled "Provider key" — that on-screen label is what actually
  distinguishes them, observable by running the CLI, not an internal flag.
  This route needs "Establishing the first session" below and a real
  interactive terminal.
- **API key** — every other route in the menu except one: `openai`,
  `openai-compatible`, `anthropic`, `gemini`, `openrouter`, `baseten`,
  `bedrock`, `fireworks`, `nebius`, `nvidia`. Only needs the `.env` scaffold
  in "Filling the local `.env`," never an interactive terminal.
- **Keyless** — `gemini-enterprise` is neither: it authenticates via Google
  Application Default Credentials against a Cloud project + location, a
  GCloud-CLI-owned mechanism this skill does not drive at all. Out of scope
  for both flows above; point the user at `gcloud auth
  application-default login` themselves if they choose this route.

After the user names a model, run that provider's `/model` menu (or its
"Ensure `<ENV_VAR>` is set" notice after `/provider`) to confirm it before
proceeding — some providers (`bedrock`, `openai-compatible`) show no preset
list at all (account/region- or endpoint-specific; the user pastes a model
ID directly), so "no presets" is expected for those two, not a bug.

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
home — the user always creates/edits the file themselves, copy-paste, start
to finish. What the agent *should* do: once the user has answered "which
provider" (see above) and, for an API-key route, "which model," show the
scaffold below with those two non-secret lines already filled in to match —
not generic placeholders — while the secret key line stays a placeholder for
the user to fill. This still is not the agent writing into the credential
home (nothing is written anywhere by the agent); it only makes the template
the user copies match what they already told the agent, so re-confirm
`OPENWIKI_PROVIDER`/`OPENWIKI_MODEL_ID` still name real variables at every
pin move — the CLI's own "Ensure `<ENV_VAR>` is set" notice after selecting
a provider names them directly — and never invent a value the user did not
state:

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

## Establishing the first session

**This section applies only to OAuth routes (currently `openai-chatgpt`).**
API-key and `openai-compatible` routes need none of it: set the credential
via env var or `.env` before the first run (see "Filling the local `.env`"
above), and even the very first `--execute` proceeds fully non-interactively
— nothing below applies to those routes.

There is no separate `openwiki auth <provider>` command for the core model —
per the pinned CLI's own `--help` output and running `openwiki auth` bare:
that subcommand only covers unrelated ingestion connectors (`slack`,
`gmail`, `x`, `notion`), a different credential domain entirely. The core
model's OAuth
login is not a standalone command at all — it triggers automatically, inside
a normal `openwiki code --init`/`--update` call, the first time that call
needs the model and finds no usable credential. **Establishing the first
session is therefore not a special "smoke" or "login-only" operation: it is
simply the first real `run_openwiki_staged.py --execute` run**, done exactly
as documented elsewhere in this skill, from a real interactive terminal —
because an OAuth token cannot be pre-supplied any other way; it does not
exist until a human completes the browser flow at least once:

1. Set `OPENWIKI_PROVIDER=<selected-route>` if it is not already the
   resolved default — there is no `--provider` CLI flag in the pinned
   version; provider selection is env-var-only. `--modelId <model-id>` *is*
   a real CLI flag, for a non-default model.
2. Run the staged wrapper's `--execute` exactly as documented in
   `references/workflow.md` and this skill's Commands section — never a
   separate, hand-rolled directory. The wrapper already builds the isolated,
   uniquely run-id'd worktree that keeps OpenWiki's hardcoded `openwiki/`
   output quarantined there; a directory outside that mechanism loses that
   guarantee and risks colliding with a real `openwiki/` folder if one ever
   exists at a target repo's root. If OpenWiki's own first-run setup wizard
   offers to change the wiki output scope/path (shown as "Wiki scope" in its
   onboarding screen), leave it at its stock default — this skill's mapping
   and promotion logic assumes that exact convention, and changing it there
   would silently break it. Every other wizard field the user hasn't been
   asked about stays at its default too.
3. The run needs a real interactive terminal, not just a live tool-call
   process, because the CLI renders an Ink-based onboarding UI and needs a
   real TTY to do so. Verify a TTY exists before starting the call (check
   that stdin/stdout are a real terminal; exit cleanly with a stated reason
   if not — do not fail confusingly or hang). If the harness's own shell
   tool cannot give the user a live, visible session, spawn a separate
   visible terminal — see "Launching a visible terminal" below; never do
   this without asking first.
4. OpenWiki detects the missing session and opens the OAuth authorize URL in
   the user's default browser itself — self-contained; this skill never
   constructs a login URL. The user completes sign-in there.
5. OpenWiki's own localhost callback listener completes the token exchange
   and writes the credential file. The run then proceeds as a normal staged
   `--execute` — review its `review.diff` and promote like any other run;
   it is a real candidate, not a throwaway.
6. Never simulate keyboard or mouse input to drive any of this (no
   `SendKeys`, `AppActivate`, or equivalent OS-level input injection) — that
   takes control of whatever window currently has focus on the user's
   desktop and is unacceptable without the user's explicit, per-action
   consent. If a step genuinely cannot be done non-interactively, stop and
   ask the user to run the exact command themselves.
7. Redirecting `HOME`/`USERPROFILE` can have unwanted side effects beyond
   OpenWiki itself. Per `--help`, there is no CLI flag or documented env var
   to point OpenWiki's own state at `okf/` any other way, and the resulting
   credential file was empirically confirmed (existence only, contents never
   read) to land wherever `HOME`/`USERPROFILE` point at launch time — so
   this redirect is still the only way to keep OpenWiki's own state under
   `okf/`. But the operating system or other tools in the process tree may
   also key their own local caches off that same home directory, and lazily
   create things there that have nothing to do with OpenWiki or this
   pipeline. One
   confirmed example: on Windows, a stray `okf/AppData/` directory appears
   after the browser step — Windows' own shell/WinINet cache, lazily
   created the first time a process with `USERPROFILE` redirected touches
   `ShellExecute`/WinINet, triggered by OpenWiki's own browser-open call.
   Treat any such unexpected file or directory under the redirected home the
   same way: harmless, but never assume it belongs in the shared, committed
   `.gitignore` — it is a side effect of *this specific machine and OS*, not
   something every clone will see. Add a local-only entry to
   `.git/info/exclude` instead (never committed, per-clone), only once it is
   actually observed rather than pre-emptively, and re-check `--help` for a
   home-directory override at every pin move.

### Launching a visible terminal

When the harness's own tool calls cannot give the user a live, interactive
session (common for sandboxed shell tools — a captured-output tool call is
not the same thing as a window a human can see and click into), a separate,
visible terminal running the exact wrapper command lets the human — not the
agent — complete the interactive part (just the browser step; the CLI
invocation itself needs no further input once launched).

**Ask before spawning it, every time.** Disclose which method and which
terminal application will be used, then wait for explicit approval —
opening a window on the user's desktop without asking raises the same
transparency and privacy concerns as any other unannounced action, even
though it is far less invasive than simulating input.

Try these in order, once approved, stopping at the first that works:

1. **A genuine harness-native live-terminal feature**, if the current
   harness has one (a real UI surface the user can see and type into — not
   merely "the harness can run shell commands," which is a different,
   agent-facing capability that does not give the human a live view).
2. **`scripts/launch_visible_terminal.py`** — generic, not
   OpenWiki-specific; it spawns a detached, visible terminal for an
   arbitrary command via `subprocess.CREATE_NEW_CONSOLE` on Windows,
   `osascript`/Terminal.app on macOS, or on Linux `xdg-terminal-exec` (a
   freedesktop.org spec that delegates to the user's actual configured
   default terminal, correct rather than guessed, when present) falling back
   to a best-effort search through common terminal emulator binaries.
   Window creation has no bash/sh-native equivalent — it is inherently a
   windowing-system (X11/Wayland) concern, not a shell one, which is why
   this needs an external mechanism at all.

   **Always two calls, on every OS, never one** — detection and launching
   are deliberately separate, because which terminal will be used cannot be
   disclosed honestly before it is known:

   ```bash
   # 1. Detect only - launches nothing, just reports the mechanism:
   uv run .agents/skills/agent-ready-context/scripts/launch_visible_terminal.py --detect
   ```

   Disclose that exact answer to the user (for example "this will open
   Terminal.app via osascript" or "this will open your configured default
   terminal via xdg-terminal-exec") and wait for explicit approval — the
   same approval gate applies regardless of which platform it resolves to.
   Only after approval, run the same command again without `--detect`:

   ```bash
   # 2. Only after the user approves the disclosed mechanism:
   uv run .agents/skills/agent-ready-context/scripts/launch_visible_terminal.py \
     --cwd <repo> \
     --env HOME=<credential-home> --env USERPROFILE=<credential-home> \
     --env OPENWIKI_PROVIDER=<selected-route> \
     -- uv run .agents/skills/agent-ready-context/scripts/run_openwiki_staged.py \
        --repo . --run-id <id> --execute -- openwiki code --init --modelId <model-id> "<brief>"
   ```

   Exit code `2` from either call means no mechanism was found for this
   platform (expected on many Linux desktops) — that is not a script bug, it
   is the signal to try the next step.
3. **The harness's own tool-call capability anyway**, as a lower-confidence
   attempt, only after step 2 reports no mechanism found. It may not render
   the CLI's interactive onboarding correctly (no live TTY a human can
   watch), but it costs little to try before giving up to a fully manual
   step.
4. **The universal fallback**: state the exact command and ask the user to
   run it themselves in their own terminal. This always works, never risks
   the wrong window receiving anything, and is not a failure mode to
   avoid — it is a legitimate, always-available option, not just a last
   resort to minimize.

When a detached launch is approved, verify PATH (and any package-manager
bin directory, such as `PNPM_HOME` for a pnpm-managed OpenWiki install)
resolves *inside that launch context specifically* before relying on it — a
separate shell or process can have a different environment than the one
that performed the install, and registry-level or profile-level PATH
changes do not propagate to already-running processes.

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
3. After disclosure and consent, when the user is ready, run the first
   staged `--execute` from a real interactive terminal. There is no separate
   "login" step to run beforehand — if no session exists, this single call
   is also the interactive login: OpenWiki triggers its own OAuth flow
   automatically partway through (see "Establishing the first session"
   above).
4. Review that first run's output like any other staged run — `review.diff`,
   citation grounding — before promoting it or running a larger one.

No bulk run may be the first provider test.
