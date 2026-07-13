---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md.md"]
description: "Verifying tool telemetry claims and re-checking them across version changes."
---

# Telemetry Auditing

Telemetry auditing is the practice of verifying whether a toolchain sends usage data, analytics, update checks, or other background network traffic, and of re-checking those claims whenever versions change. In this wiki, it supports [[concepts/privacy-preserving-tooling]], [[concepts/consent-first-workflows]], and [[concepts/toolchain-pinning]] by turning privacy claims into an explicit, reviewable maintenance task.

## Why it matters

A tool can look local-first while still making hidden network requests through analytics, auto-updates, provider auto-detection, or optional cloud features. Telemetry auditing reduces that risk by checking the upstream project claims and the actual configured behavior before the tool is trusted in a workflow.

This is especially important for [[concepts/air-gapped-operation]] and [[concepts/local-by-default-tooling]], where even small amounts of background egress can violate the operating model.

## What the source document establishes

The source page on [[summaries/agents__skills__agent-ready-context__references__privacy-and-data-flows-md]] treats telemetry claims as a formal part of the privacy contract:

- `graphify` is described as having no telemetry, no usage tracking, and no analytics.
- `openkb` is described as having no analytics, telemetry, or update checks; tracing is disabled at startup.
- `uv` is also documented as having no telemetry.
- The document says these claims must be re-verified whenever a pinned version changes.
- The verification date should be recorded next to the pin.

## What gets audited

Telemetry auditing looks for more than obvious analytics SDKs. It should include:

- usage tracking or analytics endpoints;
- automatic update checks;
- tracing or observability uploads;
- hidden provider auto-selection that changes routing without user consent;
- optional cloud dependencies that can move data off machine state.

The document ties this directly to [[concepts/explicit-provider-routing]] and [[concepts/data-flow-disclosure]], because privacy is not just about “no telemetry” claims but also about whether a tool silently changes destinations for user content.

## Related controls

Telemetry auditing usually works alongside:

- [[concepts/provider-routing]] to keep destinations explicit;
- [[concepts/local-vs-shared-configuration]] to ensure secrets and settings do not leak through shared state;
- [[concepts/source-trust-levels]] when deciding whether a tool may consume a source at all;
- [[concepts/provenance-tracking]] to keep the audit evidence attached to the pinned version.

## Practical output

A good telemetry audit leaves behind a short, durable record:

- the tool and exact version or pin;
- the upstream source checked;
- the date of verification;
- the claim that was confirmed or rejected;
- any toggles or environment variables that change behavior.

That record helps future agents preserve the same privacy posture without re-learning the investigation from scratch.

## In this wiki

For OpenKB workflows, telemetry auditing is part of the broader governance around [[concepts/toolchain-pinning]], [[concepts/privacy-preserving-tooling]], and [[concepts/consent-first-tooling]]. It keeps local-first claims honest and makes re-verification a routine part of maintenance rather than an afterthought.