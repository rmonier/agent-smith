# Profile adapter authoring

Profile adapters are native files for the active harness. Their format must be determined from current harness documentation, not from hardcoded renderers.

## Minimal profile intent

Each adapter should answer:

- What specialized task does this context handle?
- When should the harness invoke it?
- Which skills may it use?
- Which repository context should it consult?
- What permissions should be narrowed?
- What must it not do?

## Recommended candidate profiles

Create only candidates that match actual repository needs:

- `okf-curator`: refreshes and validates `okf/wiki/` and evidence pages.
- `skill-architect`: evaluates repeated actions and creates or updates custom skills.
- `repo-cartographer`: explores the repository read-only and summarizes structure.
- `security-reviewer`: reviews auth, secrets, CI/CD, supply chain, IaC, and risky defaults.
- `dependency-scout`: retrieves official external docs and stages evidence.

## Anti-bloat rules

Profile adapters must not embed:

- long project architecture;
- copies of OKF pages;
- full external docs;
- long troubleshooting narratives;
- vendor docs beyond the fields needed to make the file valid.

They should reference:

- `AGENTS.md` for orientation;
- `okf/wiki/` for source-of-truth context;
- `.agents/skills/` for actions.
