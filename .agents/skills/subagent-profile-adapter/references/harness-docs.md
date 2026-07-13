# Harness documentation handling

When harness profile semantics are unknown or may have changed, retrieve current documentation before writing adapters.

## Source priority

1. Official local documentation shipped with the harness, if available in the current environment.
2. Official web documentation.
3. User-provided documentation URL or snippet.
4. Community examples only as secondary evidence.

## OKF record

Write a concise tooling-context page under:

```text
okf/wiki/tooling/harnesses/<harness>.md
```

Include:

- official source URL or local reference;
- retrieval timestamp;
- supported profile/subagent paths;
- required frontmatter fields;
- permissions/tool model if documented;
- instruction-file behavior if documented;
- generation policy chosen by the user.

Do not copy long documentation pages. Summarize only the fields needed for adapter creation and cite/link the source.

After writing a tooling page, update the bundle-root `okf/wiki/index.md` so it lists `tooling/` in its clearly labeled harness-specific section, and record the change in `okf/wiki/log.md`. Ensure `okf/wiki/AGENTS.md` declares the custom section. See `references/tooling-context-policy.md`; the link-policy validator fails when tooling pages exist without that index entry.
