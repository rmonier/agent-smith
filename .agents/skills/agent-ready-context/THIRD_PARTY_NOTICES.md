# Third-party notices

## OpenKB-derived compatibility fallback

- Local file: `scripts/editorial_pass.py`, the `_MIRRORED_KNOWN_TARGETS_USER`
  string constant and the `_format_targets_mirrored` function
  (approximately lines 131-154).
- Upstream repository: <https://github.com/VectifyAI/OpenKB>
- Upstream source file: `openkb/agent/compiler.py`
- Upstream symbols: `_KNOWN_TARGETS_USER` (copied verbatim) and
  `_format_known_targets` (logic mirrored)
- Upstream release: tag `v0.4.4`, commit
  `bd9fe3989e71fc8012b19eb305662fa307f0a799` — verified directly against the
  fetched upstream source, not assumed from the in-file comment
- Licence: Apache-2.0
- Copyright: 2026 Vectify AI (per the upstream repository's `LICENSE` file)
- Modifications: `_format_targets_mirrored` is a from-scratch reimplementation
  matching the upstream function's behaviour (no docstring, renamed);
  `_MIRRORED_KNOWN_TARGETS_USER` is an unmodified verbatim copy of the
  upstream string.

This fallback is used only when `openkb.agent.compiler`'s private
(underscore-prefixed, no-stability-guarantee) API cannot be imported from
the installed OpenKB tool environment — a best-effort degradation path that
never affects `editorial_pass.py --check`'s correctness gates, only the
wording of the `--brief` briefing text. The rest of the script uses OpenKB's
stable public API (`openkb.lint`) as an external dependency, imported and
executed by the installed tool's own interpreter — not copied code — and
carries no separate notice for that reason (see `LICENSING.md`).

The script's own module docstring and inline comments already document
this at the point of use; this file is the formal provenance record.
