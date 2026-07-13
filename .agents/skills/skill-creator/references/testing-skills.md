# Testing skills with pressure scenarios

Before considering a skill complete, test it with at least one pressure scenario.

A pressure scenario is a realistic prompt or task that previously caused the agent to:

- forget a required step
- rewrite fragile code instead of using a deterministic script
- mix context with action
- edit vendor skills directly
- write large knowledge into AGENTS.md
- omit validation or provenance

## Baseline-first cycle

Test against observed failures, not hypothetical ones:

1. **Baseline (red)**: run the pressure scenario *without* the skill available. Record exactly how the agent fails — the missed steps, the fragile rewrites, the rationalizations it uses to skip discipline.
2. **Write (green)**: write the minimal skill content that addresses those recorded failures. Resist adding rules for problems you have not seen.
3. **Close loopholes (refactor)**: rerun the scenario *with* the skill. Where the agent still slips through, add an explicit counter — stating the reasoning, not just a prohibition.
4. Run `uv run scripts/quick_validate.py <skill-dir>`.

Create and test one skill at a time; batch-created skills ship untested failure modes together.

For scripts, execute the script on a temporary sample and include the command/result in the handoff summary.
