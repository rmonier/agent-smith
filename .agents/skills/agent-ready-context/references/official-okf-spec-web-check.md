# Optional official OKF spec web refresh

This skill is **offline-first**: it contains enough OKF v0.1 rules in `references/okf-quality.md` and `scripts/validate_okf_bundle.py` to generate and validate a bundle without network access.

Use this reference when web access is available and the task needs the freshest OKF guidance.

Authoritative sources to open with the web tool:

- `https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md`
- `https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md`

## Refresh procedure

1. Open the official `SPEC.md` with the web tool.
2. Check the current OKF version, bundle structure, reserved filenames, concept document rules, version declaration rule, and conformance section.
3. Open the official `README.md` only when tooling, examples, or reference-agent behavior are needed.
4. Compare the current official spec with the embedded baseline in `references/okf-quality.md`.
5. Run local validation:

```bash
uv run .agents/skills/agent-ready-context/scripts/validate_openwiki_bundle.py --repo .
```

6. If the local validator conflicts with the fresh official spec, follow the official spec and report which local rule appears stale or too strict.

## Embedded baseline remains authoritative offline

When the web tool is unavailable, do not stop the workflow. Use the embedded OKF v0.1 baseline in `references/okf-quality.md` and validate locally.
