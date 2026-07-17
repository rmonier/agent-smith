# Security Policy

## Reporting a vulnerability

If you believe you've found a security issue in `agent-smith` — for
example, a way the skills could be tricked into exfiltrating repository
content, installing unpinned/unverified tooling, or bypassing the
consent-first install and data-flow-disclosure model — please report it
privately rather than opening a public issue.

Preferred: use GitHub's
[private vulnerability reporting](https://github.com/rmonier/agent-smith/security/advisories/new)
for this repository. Alternatively, reach the maintainer via
[GitHub](https://github.com/rmonier).

Please include:

- The skill or script involved and, if applicable, the harness/provider
  combination that reproduces it.
- Steps to reproduce, or the specific data flow you're concerned about.
- The potential impact as you see it (what an attacker or a misconfigured
  agent could actually do).

## What's in scope

The three product skills (`agent-ready-context`, `skill-creator`,
`subagent-profile-adapter`) and their bundled scripts. Issues in upstream
OpenWiki should generally be reported there, unless the issue is specifically
in how this repository installs, configures, stages, validates, or invokes it.
The same rule applies to any other upstream tool skill.

## Design background

This project's security and privacy model — consent-first installs,
pinned/integrity-checked tooling, explicit provider routing, data-flow
disclosure before LLM calls — is documented in
[README.md § Security and Privacy](README.md#security-and-privacy). Read
that first; many "is this safe?" questions are already answered there.

Vendor dependencies are never patched. Compatibility and policy adaptation
belong in project-owned wrappers, and an upstream incompatibility that cannot
be handled there is reported instead of hidden in a fork. OpenWiki state and
credentials remain local under gitignored `okf/.openwiki/`.

## Response

There's no formal SLA — this is a single-maintainer project — but reports
will be acknowledged and triaged as soon as practical, and credited in the
fix unless you ask otherwise.
