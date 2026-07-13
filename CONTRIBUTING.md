# Contributing

Thanks for considering a contribution. This project's contribution model
is a little different from a typical repo — read
[README.md § Contribute](README.md#contribute) first for the two shapes a
contribution usually takes (extending an existing skill, or creating a new
one). This file covers the process and checks around that; it doesn't
repeat the workflow itself.

## Before you start

- By participating, you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
- Found a security issue rather than a bug? See [SECURITY.md](SECURITY.md)
  instead of opening a public issue.
- Check existing issues/PRs first to avoid duplicate work.

## Making a change

1. Describe the capability or correction you want to your agent (or make
   the edit directly, if you prefer) — see README's Contribute section for
   the two request shapes.
2. Keep the project's layering intact: **skills** are actions
   (`.agents/skills/`), the **OKF wiki** is durable context (`okf/wiki/`,
   not hand-edited outside its documented exceptions — see
   `okf/wiki/AGENTS.md`), and **`AGENTS.md`** is the orientation index.
   Don't blur these.
3. Preserve house standards for skill changes: consent-first pinned
   installs, registry-agnostic commands, minimal scoped `allowed-tools`,
   namespaced string-only `metadata` keys, `SKILL.md` under 500 lines with
   detail pushed to `references/`.

## Validating before you open a PR

Run whichever of these apply to your change:

```sh
# Any skill you touched
uv run .agents/skills/skill-creator/scripts/quick_validate.py .agents/skills/<skill-name>

# General repo readiness
uv run .agents/skills/agent-ready-context/scripts/check_prereqs.py --repo .

# Adapter/tooling-link policy changes
uv run .agents/skills/subagent-profile-adapter/scripts/validate_tooling_link_policy.py --repo .

# OKF bundle changes (only if you touched okf/wiki/ through the documented pipeline)
uv run .agents/skills/agent-ready-context/scripts/validate_okf_bundle.py okf/wiki --openkb-wiki
```

## Licensing hygiene

This repo uses scoped, per-file licensing declared in
[`REUSE.toml`](REUSE.toml) — see [LICENSING.md](LICENSING.md) for the full
map. If you add a new file:

- New original scripts under a skill's `scripts/` → Apache-2.0.
- New original docs (`SKILL.md`, `references/`, `assets/`, root-level
  Markdown) → CC-BY-4.0.
- Copying or adapting text from somewhere else, even a few sentences? Say
  so in your PR description and add an entry to the relevant
  `THIRD_PARTY_NOTICES.md`, with the upstream source, licence, and
  copyright holder — verified directly from the upstream source, not
  assumed.
- If you have the [`reuse`](https://reuse.software/) tool installed,
  `reuse lint` from the repo root will catch missing annotations.

## Pull requests

Describe what changed and why. If your change affects `AGENTS.md`, the
OKF wiki, or a skill's public behavior, call that out explicitly so it's
easy to review. There's no fixed review SLA — this is a single-maintainer
project — but PRs will get a response.
