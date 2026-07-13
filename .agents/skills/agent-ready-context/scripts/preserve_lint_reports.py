#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Copy `openkb lint` reports out of the wiki into the gitignored evidence dir.

`openkb --kb-dir <kb> lint` always writes its findings to
`<kb>/wiki/reports/lint_*.md` and never fails on findings, so nothing forces
this step to happen — it is easy to run lint, see a clean exit, and move on
without ever preserving or triaging the report. Run this immediately after
every `openkb lint` (and `lint --fix`, which reruns lint) so the report has a
stable, wiki-independent location before anything under okf/wiki/reports/
is touched again.

Copies (never moves) every `lint_*.md` report not already present at the
destination, so re-running is a no-op for reports already preserved. Also
skips the `<kb>/wiki/reports/` copies for a later lint run — see the
'stale lint report' orphan false-positive note in
`references/openkb-lifecycle.md` if a final clean structural lint is needed.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy openkb lint reports out of the wiki into the gitignored evidence dir."
    )
    parser.add_argument("--repo", default=".", help="repository root")
    parser.add_argument("--kb-dir", default="okf", help="OpenKB KB root relative to --repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    src_dir = repo / args.kb_dir / "wiki" / "reports"
    dst_dir = repo / args.kb_dir / ".okf-build" / "reports"

    if not src_dir.is_dir():
        print(f"No {src_dir} directory yet -- nothing to preserve (has `openkb lint` run?).")
        return 0

    reports = sorted(src_dir.glob("lint_*.md"))
    if not reports:
        print(f"No lint_*.md reports found under {src_dir}.")
        return 0

    dst_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    already: list[str] = []
    for report in reports:
        dst = dst_dir / report.name
        if dst.exists():
            already.append(report.name)
            continue
        shutil.copy2(report, dst)
        copied.append(report.name)

    if copied:
        print(f"Preserved {len(copied)} report(s) to {dst_dir}:")
        for name in copied:
            print(f"  + {name}")
    if already:
        print(f"{len(already)} report(s) already preserved (unchanged):")
        for name in already:
            print(f"  = {name}")
    print(
        "\nNext: triage every semantic finding in the newest report into the "
        "three classes in references/openkb-lifecycle.md -- preserving the "
        "report is not the same as triaging it."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
