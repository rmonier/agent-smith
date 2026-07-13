---
sources: ["summaries/agents__skills__agent-ready-context__references__workflow-md.md", "summaries/agents__skills__agent-ready-context__scripts__merge_agents_md_okf_section-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__references__okf-quality-md.md", "summaries/graphify-report.md", "summaries/README-md.md", "summaries/agents__skills__agent-ready-context__SKILL-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__SKILL-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__validate_tooling_link_policy-py.md", "summaries/agents__skills__subagent-profile-adapter__references__tooling-context-policy-md.md"]
type: "Work"
description: "Validation script for tooling-link policy in subagent adapter workflows"
---

# Validate Tooling Link Policy Script

`validate_tooling_link_policy.py` is a validation script used by the [[entities/subagent-profile-adapter]] skill to check that tooling-related wiki pages follow the project’s link and boundary rules.

## What It Does

The script validates that project wiki content does not link back into `okf/wiki/tooling/`, while allowing the bundle-root wiki index to enumerate tooling pages in the special harness-specific section required by the skill.

It is part of the broader agent-ready repository workflow described by [[summaries/agents__skills__agent-ready-context__SKILL-md]], where OKF wiki content is the durable context source of truth and tooling context stays separate from compiled project knowledge.

## Key Facts

- It is invoked as part of the subagent/profile adapter validation workflow described in [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]].
- It checks the tooling link policy after adapter files are written.
- It helps enforce [[concepts/tooling-link-policy]], [[concepts/tooling-context-isolation]], and [[concepts/link-directionality]].
- It supports the boundary between project knowledge and harness-specific context described in [[concepts/tooling-context-governance]] and [[concepts/runtime-adapter-management]].
- It fits the agent-ready context model where skills are actions, the OKF wiki is compiled context, and `AGENTS.md` is only an orientation layer.
- It aligns with the repository policy that local tooling pages are user-scoped and should not become project truth.

## Role In The Workflow

The script is a quality gate for harness adapter generation. It verifies that generated tooling context stays local, short, and appropriately separated from compiled project knowledge, matching the skill’s emphasis on [[concepts/generated-artifact-validation]] and [[concepts/consent-first-tooling]].

In the agent-ready context workflow, it also fits alongside deterministic staging, validation, and the special handling of tooling navigation pages in the OpenKB wiki.

## Related Pages

- [[entities/subagent-profile-adapter]]
- [[summaries/agents__skills__subagent-profile-adapter__SKILL-md]]
- [[summaries/agents__skills__agent-ready-context__SKILL-md]]
- [[entities/validate_tooling_link_policy-py]]

See also: [[summaries/README-md]]