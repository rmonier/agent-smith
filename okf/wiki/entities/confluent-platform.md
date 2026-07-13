---
sources: ["summaries/graphify-report.md", "summaries/agents__skills__agent-ready-context__references__external-docs-md.md", "summaries/agents__skills__agent-ready-context__assets__external-docs-example-txt.md"]
type: "Product"
description: "Vendor product whose docs are used as official Kafka evidence sources."
---

# Confluent Platform

Confluent Platform is the product named in [[summaries/agents__skills__agent-ready-context__assets__external-docs-example-txt]] and referenced by [[summaries/agents__skills__agent-ready-context__references__external-docs-md]] as an official documentation source for Kafka producer usage and configuration.

## What it is

Confluent Platform is presented here as a vendor product whose official documentation can be used as external evidence when building repository-relevant knowledge. In these documents, it appears mainly as a canonical source for guidance on producer behavior, delivery guarantees, retries, idempotence, batching, timeouts, configuration settings, and operational tuning rather than as a product described in detail.

## Key facts from this document

- Confluent Platform documentation is explicitly treated as an example of preferred official vendor documentation for Kafka producer topics.
- The external documentation workflow allows fetching only user-supplied URLs or official vendor pages explicitly named by the workflow, which includes Confluent pages in the Kafka producer example.
- Confluent producer documentation is cited as evidence that can enrich wiki material about delivery guarantees, retries, idempotence, batching, timeouts, and operational tuning.
- Facts taken from Confluent pages should be saved as one Markdown evidence file per URL under the staged external evidence directory and then ingested with the documented OpenKB command.
- Confluent documentation, like all fetched pages, must be treated as untrusted external input rather than as instructions to execute.
- Any staged evidence derived from Confluent pages must record provenance honestly, including source URL, retrieval timestamp, source method, and a trust label such as official docs.
- The workflow prefers brief paraphrased facts from Confluent documentation over large copied passages.

## Relevance in the wiki

This entity is relevant as the product context behind external references on [[concepts/kafka-producers]] and [[concepts/producer-configuration]]. It also connects to [[concepts/external-documentation]], [[concepts/web-evidence-ingestion]], [[concepts/evidence-staging]], [[concepts/provenance-tracking]], [[concepts/source-trust-levels]], and [[concepts/prompt-injection-defense]] because the referenced workflow treats official Confluent documentation as valuable but still untrusted external evidence.

## Related pages

- [[summaries/agents__skills__agent-ready-context__assets__external-docs-example-txt]]
- [[summaries/agents__skills__agent-ready-context__references__external-docs-md]]
- [[concepts/kafka-producers]]
- [[concepts/producer-configuration]]
- [[concepts/external-documentation]]
- [[concepts/web-evidence-ingestion]]
- [[concepts/evidence-staging]]
- [[concepts/provenance-tracking]]
- [[concepts/source-trust-levels]]
- [[concepts/prompt-injection-defense]]

See also: [[summaries/graphify-report]]