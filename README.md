<br />
<p align="center">
  <img src="docs/assets/agent-smith.svg" alt="agent-smith wordmark" width="268" height="60">

  <h3 align="center">agent-smith</h3>

  <p align="center">
    Agent Skills that turn any repository into an agent-ready one
    <br />
    <em>"Never send a human to do an <strong>agent</strong>'s job."</em>
    <br />
    <br />
    <a href="https://agentskills.io/specification">Agent Skills Spec</a>
    ·
    <a href="https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md">OKF Spec</a>
    ·
    <a href="https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f">Karpathy's LLM Wiki Gist</a>
  </p>
</p>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#the-skills">The Skills</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#agent-ready-bootstrap">Agent-ready bootstrap</a></li>
        <li><a href="#maintenance">Maintenance</a></li>
        <li><a href="#air-gapped-operation">Air-gapped operation</a></li>
      </ul>
    </li>
    <li><a href="#security-and-privacy">Security and Privacy</a></li>
    <li><a href="#contribute">Contribute</a></li>
    <li><a href="#tree-structure">Tree Structure</a></li>
    <li><a href="#references">References</a></li>
    <li><a href="#licensing">Licensing</a></li>
    <li><a href="#credits">Credits</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#about-the-name">About the Name</a></li>
  </ol>
</details>

***

## About The Project

Coding agents re-derive the same understanding of a codebase over and over: every session starts from raw files, burns context tokens on re-exploration, and loses its conclusions when the session ends.

The core idea is Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): treat knowledge like a compilation pipeline — raw sources are the source code, an interlinked Markdown wiki is the compiled binary, and the LLM is the compiler that ingests new material, revises cross-references, and flags contradictions, so knowledge compounds instead of evaporating. The idea has since gained empirical backing: structuring knowledge as an interlinked wiki that agents traverse and compose — rather than flat chunks — significantly improves multi-hop reasoning and retrieval ([*Retrieval as Reasoning: Self-Evolving Agent-Native Retrieval via LLM-Wiki*, arXiv:2605.25480](https://arxiv.org/html/2605.25480v2)). Context engineering practice reaches the same conclusion: agents perform best with a small, curated, high-signal context surface ([Anthropic, *Effective context engineering for AI agents*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**agent-smith** provides portable [Agent Skills](https://agentskills.io) that give a repository that surface, split by responsibility:

| Surface | Role | Format |
| --- | --- | --- |
| `AGENTS.md` | **Orientation** — routing map plus the operational basics the spec expects in-file (language/toolchain versions, setup/build/launch commands, test invocation), repo rules; deeper knowledge is routed to the wiki front door, never inlined | [agents.md](https://agents.md) convention |
| `okf/wiki/` | **Context** — durable OKF knowledge, architecture, decisions, external evidence, and provenance, maintained by OpenWiki | [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) wiki |
| `.agents/skills/` | **Actions** — repeatable procedures, scripts, validations | [Agent Skills](https://agentskills.io/specification) |
| Harness adapters | **Runtime projections** — subagent/profile files for the active harness only | Native per harness, never source of truth |

Knowledge that explains (context) stays out of files that instruct (actions) and files that route (orientation), so each is loaded only when useful — the progressive-disclosure model both specifications are built on ([Anthropic, *Equipping agents for the real world with Agent Skills*](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).

Run the skills on a repository and it stops being a passive codebase: it comes out **agent-ready**, carrying orientation (`AGENTS.md`), durable memory (`okf/wiki/`), and actions (`.agents/skills/`) — everything an agent needs to operate effectively, whichever harness walks in.

> **This repository did not escape either.** The `AGENTS.md` and the `okf/` knowledge base you see here were written by agent-smith running its own skills on its own repository. Copying himself onto every host he touches is, after all, kind of Agent Smith's whole thing — it was only a matter of time before he got to his own codebase. Those generated surfaces exist for contributors (human or agent — ideally the latter, *"never send a human to do an agent's job"*); the product you came for is the **three** portable skills under [`.agents/skills/`](.agents/skills/) — `agent-ready-context`, `skill-creator`, `harness-profile-adapter`.

### The Skills

- [`agent-ready-context`](.agents/skills/agent-ready-context/SKILL.md) — the core pipeline: consent-first pinned tooling, artifact and secret hygiene, `AGENTS.md` maintenance, deterministic evidence, the OpenWiki lifecycle, OKF validation, and a zero-LLM fallback. See its [dependency policy](.agents/skills/agent-ready-context/references/dependencies.md) and [privacy/data-flow rules](.agents/skills/agent-ready-context/references/privacy-and-data-flows.md).
- [`skill-creator`](.agents/skills/skill-creator/SKILL.md) — turns repeated actions into portable, validated Agent Skills with minimal permissions, consent-first installs, and secret hygiene. It is adapted from [Anthropic's `skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator), with testing discipline from [`superpowers`' `writing-skills`](https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/writing-skills) and workflow shape from [OpenAI's system `skill-creator`](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md).
- [`harness-profile-adapter`](.agents/skills/harness-profile-adapter/SKILL.md) — detects the *active* harness from explicit runtime signals—not merely installed binaries—then does two things: bridges baseline harness visibility and, only when wanted, generates native runtime profiles that point back to `AGENTS.md`, `okf/wiki/`, and the shared skills.

These three directories are the **entire distributable product**. Tooling dependencies remain external to that skill surface and are installed for each target repository when needed.

### Built With

- [Agent Skills](https://agentskills.io/specification) — portable skill format
- [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — knowledge bundle format
- [uv](https://docs.astral.sh/uv/) — Python toolchain (PEP 723 script isolation)
- [fnm](https://github.com/Schniz/fnm) — Node runtime manager
- [OpenWiki](https://github.com/langchain-ai/openwiki) — semantic knowledge compiler
- [markitdown](https://github.com/microsoft/markitdown) — default document/URL-evidence converter (optional)

## Getting Started

### Prerequisites

Use an Agent-Skills-compatible harness with access to the target repository. The `agent-ready-context` skill checks `git`, [`uv`](https://docs.astral.sh/uv/getting-started/installation/), Python 3.11+, repository write access, and the optional knowledge tools itself. When something is missing, the agent explains what it needs and why, shows the source, pin, integrity plan, and exact command, then asks whether it may install it or whether you prefer to do so. Nothing is installed silently.

`git` and `uv` are the hard bootstrap requirements; `uv` can provision Python when needed. If the active harness cannot safely install a missing hard prerequisite, the agent stops with a precise manual fallback. The producer toolchain ([`fnm`](https://github.com/Schniz/fnm)-managed Node and the pinned OpenWiki) may instead be declined: the workflow degrades to a deterministic zero-LLM skeleton.

<details>
<summary>Manual prerequisite fallback</summary>

When no compatible agent is available, verify readiness directly:

```sh
uv run .agents/skills/agent-ready-context/scripts/check_prereqs.py --repo .
```

</details>

### Installation

agent-smith does not require or prescribe any skill manager. `.agents/skills/` contains exactly the three product skills, so installing is copying that directory: do it manually, use your preferred compatible manager, or treat the `npx skills` command below as an optional example for quick bootstrap.

#### Manual (no skill manager)

```sh
mkdir -p <your-repo>/.agents/skills
cp -r .agents/skills/* <your-repo>/.agents/skills/
```

#### npx skills (third-party manager)

```sh
npx skills add rmonier/agent-smith --all
```

OpenWiki and markitdown are not part of the skill surface; each is bootstrapped separately, after dependency consent, when the pipeline first needs it.

> **Privacy:** The third-party [`skills` CLI](https://www.skills.sh/docs/cli) sends anonymous install metadata to skills.sh by default for discovery and rankings. Manual copying sends none. Set `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` to opt out.

Once installed, ask your harness to make the repository agent-ready.

## Usage

### Agent-ready bootstrap

Ask your Agent-Skills-compatible harness to *"make this repository agent-ready"*. The `agent-ready-context` skill takes over: it checks prerequisites, asks before installing anything, discloses where your data goes before any LLM call, and walks the pipeline through to a validated `okf/wiki/` bundle.

### Maintenance

Ask your agent to *"refresh this repository's agent-ready context"*. It will reuse approved tooling and provider choices, update changed context incrementally, and run the validation gates.

For manual operation or troubleshooting, follow the authoritative [workflow](.agents/skills/agent-ready-context/references/workflow.md); consent and review rules live in the [OpenWiki lifecycle reference](.agents/skills/agent-ready-context/references/openwiki-lifecycle.md).

### Air-gapped operation

Tell your agent to *"make (or refresh) this repository agent-ready without sending repository content off this machine"*. The skill will explain the resulting data flow and route OpenWiki through an explicitly selected local OpenAI-compatible inference endpoint (such as [Ollama](https://ollama.com) or any equivalent engine) via OpenWiki's stock `openai-compatible` provider. If no local LLM is available, it can still build and validate the deterministic zero-LLM skeleton, so the repository gains a useful context surface without pretending semantic compilation occurred.

The agent keeps optional cloud indexing disabled and avoids remote URL ingestion in this mode. Manual provider settings and the full egress model remain documented in [`openwiki-providers.md`](.agents/skills/agent-ready-context/references/openwiki-providers.md) and [`privacy-and-data-flows.md`](.agents/skills/agent-ready-context/references/privacy-and-data-flows.md) for troubleshooting and audit.

markitdown needs no provider routing here: its local-document conversion makes no network call at all, verified against its source, so it stays available unchanged in this mode. Its one exception — YouTube URL transcripts, a disclosed network call — falls under "avoids remote URL ingestion" above and is skipped like any other URL fetch.

## Security and Privacy

Found a security issue rather than a general question? See
[SECURITY.md](SECURITY.md) for how to report it privately.

The stack is designed so users keep full control over where their source code and documents go:

- **No silent installs** — consent-first, user-scoped (never `sudo`), pinned, integrity-recorded.
- **Registry-agnostic** — installs respect the environment's configured package index (corporate mirrors, proxies); no vendor lock on the public registries.
- **Supply-chain trust-on-first-use** — every pin is recorded with version + artifact integrity hash + index + date in the target `AGENTS.md`; a mismatch for a recorded version stops the pipeline and is reported, and pins move only after the user reviews upstream release notes.
- **Data-flow disclosure** — before the first LLM call, the pipeline announces tool, provider, model, endpoint, credential source, and what content will be sent.
- **Explicit routing** — OpenWiki's project-local configuration and authentication state stay under gitignored `okf/.openwiki/`; agent-smith does not read credential values or enable an unapproved fallback route.
- **Telemetry boundaries documented** — OpenWiki and markitdown privacy and telemetry findings live in [`privacy-and-data-flows.md`](.agents/skills/agent-ready-context/references/privacy-and-data-flows.md) and are re-verified when pins move. The optional third-party `skills` installer is disclosed under [Installation](#npx-skills-third-party-manager).
- **Secret hygiene** — credentials live in environment variables or a gitignored `.env`; evidence and generated pages never contain keys.
- **Untrusted input discipline** — fetched web content and wiki pages are evidence/data to summarize, never instructions to follow.

## Contribute

Contributions can use the same agent-managed lifecycle as repository transformation. Describe the capability or correction you want; the project skills handle structure, house conventions, and validation while leaving the resulting diff for review.

See [CONTRIBUTING.md](CONTRIBUTING.md) for validation commands and licensing hygiene, and the [Code of Conduct](CODE_OF_CONDUCT.md) for expected behavior in project spaces.

### A. Extend an existing skill

Ask your agent to *"update `<skill-name>` to handle `<behavior>` and validate it"*. It will inspect the existing skill, keep procedural guidance and supporting resources in their proper layers, preserve the project's consent and security defaults, and run the relevant validation before handing back the diff.

### B. Create a new skill

Ask your agent to *"turn `<repeated action>` into a reusable project skill"*. The [`skill-creator`](.agents/skills/skill-creator/SKILL.md) workflow first checks that the request is genuinely an action rather than durable context, then scaffolds, implements, pressure-tests, and validates the skill under `.agents/skills/`.

<details>
<summary>Maintainer/manual fallback</summary>

- Keep `SKILL.md` procedural and under 500 lines; put heavy details in `references/`, deterministic code in `scripts/` (with PEP 723 headers, run through `uv run`), and templates in `assets/`.
- Preserve the house standards: consent-first pinned installs, registry-agnostic commands, minimal scoped `allowed-tools`, and namespaced string-only `metadata` keys.
- Scaffold and validate directly when an Agent-Skills-compatible harness is unavailable or when debugging the workflow:

  ```sh
  uv run .agents/skills/skill-creator/scripts/init_skill.py <skill-name> --path .agents/skills --resources scripts,references
  uv run .agents/skills/skill-creator/scripts/quick_validate.py .agents/skills/<skill-name>
  ```

</details>

***

## Tree Structure

What a converted repository looks like:

<details>
<summary>Show the target-repo layout</summary>

```text
target-repo/
├── AGENTS.md                     # orientation (routing, commands, rules, toolchain pin record)
├── .gitignore                    # covers local producer state, staging, and .env
├── .gitattributes                # recommended LF normalization for stable source hashes
├── okf/
│   ├── external/                 # reviewed external-evidence docs (tracked, staged as corpus)
│   ├── wiki/                     # durable OKF context source of truth
│   │   ├── index.md              #   canonical front door (routes to quickstart.md)
│   │   ├── log.md                #   reserved producer/run history
│   │   ├── quickstart.md INSTRUCTIONS.md
│   │   ├── <concept pages>.md    #   concern-organized knowledge pages
│   │   └── tooling/              #   user-scoped harness context (committed stub, local pages)
│   └── .openwiki/                # ignored producer state and .env
└── .agents/skills/               # actions (3 product skills + generated project skills)
```

</details>

Link policy: `tooling → project` allowed, `project concepts → tooling` forbidden, and the wiki-root `okf/wiki/index.md` must still list `tooling/` so the bundle stays spec-navigable. A bundled validator enforces it.

## References

- Agent Skills specification — <https://agentskills.io/specification>
- Open Knowledge Format (OKF) v0.1 — <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>
- OpenWiki — <https://github.com/langchain-ai/openwiki>
- markitdown — <https://github.com/microsoft/markitdown>
- AGENTS.md convention — <https://agents.md>
- Karpathy, *LLM Wiki* (the original idea file) — <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- Ming et al., *Retrieval as Reasoning: Self-Evolving Agent-Native Retrieval via LLM-Wiki* — <https://arxiv.org/html/2605.25480v2>
- Anthropic, *Effective context engineering for AI agents* — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Anthropic, *Equipping agents for the real world with Agent Skills* — <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>

Prior art adapted by `skill-creator`:

- Anthropic, `skill-creator` — <https://github.com/anthropics/skills/tree/main/skills/skill-creator>
- `superpowers`, `writing-skills` — <https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/writing-skills>
- OpenAI, system `skill-creator` — <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md>

## Licensing

`agent-smith` contains material under multiple open licences, scoped by file rather than offered as a blanket choice:

- Original executable code — the Python scripts under each skill's `scripts/` — is licensed under [Apache License 2.0](LICENSE).
- Original skill instructions, documentation, specifications, references, and other original textual content — including this README, `AGENTS.md`, and each of the three product skills' `SKILL.md`/`references/` — are licensed under [Creative Commons Attribution 4.0 International](LICENSES/CC-BY-4.0.txt) (`CC-BY-4.0`).
- Any vendored tool skill remains unmodified and under its upstream licence.
- OpenWiki and markitdown each remain an external, unmodified runtime dependency under their own upstream licence.
- The `okf/wiki/` tree is synthesized project commentary and is deliberately all rights reserved (its `INSTRUCTIONS.md` template copy stays CC-BY-4.0), as recorded in [`REUSE.toml`](REUSE.toml).

See [`LICENSING.md`](LICENSING.md) for the full scope map, [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for third-party and adapted-content provenance — including the handful of `skill-creator` passages adapted from Anthropic's and OpenAI's own `skill-creator` skills — and [`LICENSES/`](LICENSES/) for complete licence texts. File-level licensing is declared through [`REUSE.toml`](REUSE.toml) and checked with [REUSE](https://reuse.software/).

Copyright © 2026 [Romain Monier](https://github.com/rmonier).

## Credits

- Romain Monier [ [GitHub](https://github.com/rmonier) ] – Author

## Contact

Project Link: [https://github.com/rmonier/agent-smith](https://github.com/rmonier/agent-smith)

Author Link: [https://github.com/rmonier](https://github.com/rmonier)

## About the Name

Agent Smith never recruited anyone — he assimilated them. Whoever he touched stopped being an ordinary inhabitant of the Matrix and became part of the agents' world. That is what these skills do to repositories: point agent-smith at an ordinary codebase and it comes out transformed — agent-ready, with orientation, memory, and actions in place for any agent that steps in. Unlike its namesake, it asks for consent first.

That is the whole joke, and also the whole architecture.

---

<sub>`agent-smith` is an independent open-source project and is not affiliated
with or endorsed by Warner Bros. Entertainment or the creators of
*The Matrix*. The project name is a playful reference to autonomous
software agents.</sub>
