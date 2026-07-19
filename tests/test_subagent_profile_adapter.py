#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Contract tests for subagent-profile-adapter's local alias helper."""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "subagent-profile-adapter" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ensure_local_alias as alias_tool  # noqa: E402


class AliasWorkspaceCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir(parents=True)
        (self.repo / ".git").mkdir()

    def _argv(self, *extra: str) -> list[str]:
        return ["ensure_local_alias.py", "--repo", str(self.repo), *extra]

    def _run(self, *extra: str) -> tuple[int, str]:
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", self._argv(*extra)):
            with contextlib.redirect_stderr(stderr):
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    code = alias_tool.main()
        return code, stdout.getvalue() + stderr.getvalue()


class FileAliasTests(AliasWorkspaceCase):
    def test_symlink_created_and_excluded(self) -> None:
        (self.repo / "AGENTS.md").write_text("# orientation\n", encoding="utf-8")
        code, output = self._run("--source", "AGENTS.md", "--alias", "HARNESS.md")
        self.assertEqual(code, 0)
        alias = self.repo / "HARNESS.md"
        self.assertTrue(alias.is_symlink())
        self.assertEqual((alias.parent / os.readlink(alias)).resolve(), (self.repo / "AGENTS.md").resolve())
        exclude = (self.repo / ".git" / "info" / "exclude").read_text(encoding="utf-8")
        self.assertIn("HARNESS.md", exclude)
        self.assertIn("symlink", output)

    def test_pointer_file_fallback_when_symlink_unavailable(self) -> None:
        (self.repo / "AGENTS.md").write_text("# orientation\n", encoding="utf-8")
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            code, output = self._run("--source", "AGENTS.md", "--alias", "HARNESS.md")
        self.assertEqual(code, 0)
        alias = self.repo / "HARNESS.md"
        self.assertFalse(alias.is_symlink())
        self.assertTrue(alias.is_file())
        self.assertIn("AGENTS.md", alias.read_text(encoding="utf-8"))
        self.assertIn("pointer-file", output)

    def test_fallback_fail_reports_error_and_writes_nothing(self) -> None:
        (self.repo / "AGENTS.md").write_text("# orientation\n", encoding="utf-8")
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            code, output = self._run("--source", "AGENTS.md", "--alias", "HARNESS.md", "--fallback", "fail")
        self.assertEqual(code, 1)
        self.assertFalse((self.repo / "HARNESS.md").exists())
        self.assertIn("failed to create symlink", output)

    def test_rerun_is_idempotent(self) -> None:
        (self.repo / "AGENTS.md").write_text("# orientation\n", encoding="utf-8")
        self.assertEqual(self._run("--source", "AGENTS.md", "--alias", "HARNESS.md")[0], 0)
        code, output = self._run("--source", "AGENTS.md", "--alias", "HARNESS.md")
        self.assertEqual(code, 0)
        self.assertIn("already exists", output)

    def test_existing_unrelated_file_requires_force(self) -> None:
        (self.repo / "AGENTS.md").write_text("# orientation\n", encoding="utf-8")
        (self.repo / "HARNESS.md").write_text("unrelated content\n", encoding="utf-8")
        code, output = self._run("--source", "AGENTS.md", "--alias", "HARNESS.md")
        self.assertEqual(code, 1)
        self.assertIn("not a local alias", output)
        self.assertEqual((self.repo / "HARNESS.md").read_text(encoding="utf-8"), "unrelated content\n")

        code, output = self._run("--source", "AGENTS.md", "--alias", "HARNESS.md", "--force")
        self.assertEqual(code, 0)
        self.assertTrue((self.repo / "HARNESS.md").is_symlink())


class DirectoryAliasTests(AliasWorkspaceCase):
    def _make_skills_dir(self) -> Path:
        skills = self.repo / ".agents" / "skills" / "demo-skill"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text("---\nname: demo-skill\n---\nBody\n", encoding="utf-8")
        return self.repo / ".agents" / "skills"

    def test_symlink_created_for_directory(self) -> None:
        self._make_skills_dir()
        code, output = self._run("--source", ".agents/skills", "--alias", ".harness/skills")
        self.assertEqual(code, 0)
        alias = self.repo / ".harness" / "skills"
        self.assertTrue(alias.is_dir())
        self.assertTrue((alias / "demo-skill" / "SKILL.md").is_file())
        self.assertIn("symlink", output)

    # The next three exercise create_directory_alias() directly rather than
    # through main(): patching os.name away from the real host platform is
    # only safe when no fresh Path(...) gets constructed while it's patched
    # (pathlib dispatches WindowsPath/PosixPath from os.name at construction
    # time - verified directly: patching os.name then calling Path(...) on
    # this Windows host raises NotImplementedError). main() constructs Path
    # objects from argv on every call, so it can't be used here; alias/source
    # below are already-constructed Path objects, so calling methods on them
    # or passing them into create_directory_alias is unaffected.

    def test_junction_fallback_on_windows_when_symlink_fails(self) -> None:
        skills_dir = self._make_skills_dir()
        alias = self.repo / ".harness" / "skills"
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            with mock.patch.object(alias_tool.os, "name", "nt"):
                with mock.patch.object(
                    alias_tool.subprocess,
                    "run",
                    return_value=mock.Mock(returncode=0, stdout="Junction created", stderr=""),
                ) as run_mock:
                    mode = alias_tool.create_directory_alias(alias, skills_dir)
        self.assertEqual(mode, "junction")
        args = run_mock.call_args.args[0]
        self.assertEqual(args[:3], ["cmd", "/c", "mklink"])
        self.assertIn("/J", args)

    def test_directory_alias_hard_fails_when_symlink_and_junction_both_fail(self) -> None:
        skills_dir = self._make_skills_dir()
        alias = self.repo / ".harness" / "skills"
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            with mock.patch.object(alias_tool.os, "name", "nt"):
                with mock.patch.object(
                    alias_tool.subprocess,
                    "run",
                    return_value=mock.Mock(returncode=1, stdout="", stderr="Access is denied"),
                ):
                    with self.assertRaisesRegex(OSError, "junction fallback also failed"):
                        alias_tool.create_directory_alias(alias, skills_dir)

    def test_directory_alias_does_not_attempt_junction_off_windows(self) -> None:
        skills_dir = self._make_skills_dir()
        alias = self.repo / ".harness" / "skills"
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            with mock.patch.object(alias_tool.os, "name", "posix"):
                with mock.patch.object(alias_tool.subprocess, "run") as run_mock:
                    with self.assertRaisesRegex(OSError, "no privilege"):
                        alias_tool.create_directory_alias(alias, skills_dir)
        run_mock.assert_not_called()

    def test_directory_alias_failure_is_reported_by_the_cli_without_writing_anything(self) -> None:
        # CLI-level coverage of the hard-failure path, using the real host
        # platform (no os.name patching) so main()'s own Path construction
        # is never at risk.
        self._make_skills_dir()
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            with mock.patch.object(
                alias_tool, "create_directory_alias", side_effect=OSError("symlink and junction both failed")
            ):
                code, output = self._run("--source", ".agents/skills", "--alias", ".harness/skills")
        self.assertEqual(code, 1)
        self.assertFalse((self.repo / ".harness" / "skills").exists())
        self.assertIn("no text-pointer fallback", output)

    def test_rerun_is_idempotent_for_directory(self) -> None:
        self._make_skills_dir()
        self.assertEqual(self._run("--source", ".agents/skills", "--alias", ".harness/skills")[0], 0)
        code, output = self._run("--source", ".agents/skills", "--alias", ".harness/skills")
        self.assertEqual(code, 0)
        self.assertIn("already exists", output)

    def test_refuses_to_replace_real_directory_even_with_force(self) -> None:
        self._make_skills_dir()
        real_dir = self.repo / ".harness" / "skills"
        real_dir.mkdir(parents=True)
        (real_dir / "keep-me.txt").write_text("user data\n", encoding="utf-8")
        code, output = self._run("--source", ".agents/skills", "--alias", ".harness/skills", "--force")
        self.assertEqual(code, 1)
        self.assertIn("refusing to replace a real directory", output)
        self.assertTrue((real_dir / "keep-me.txt").exists())

    def test_junction_removal_deletes_only_reparse_point_not_target_content(self) -> None:
        # Exercises the real OS mechanism (skips only if this host cannot
        # create a junction without elevation) to guard the exact failure
        # mode this helper exists to avoid: destroying the aliased target
        # while replacing a stale alias.
        if os.name != "nt":
            raise unittest.SkipTest("junctions are Windows-specific")
        skills = self._make_skills_dir()
        alias = self.repo / ".harness" / "skills"
        alias.parent.mkdir(parents=True)
        completed = alias_tool.subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(alias), str(skills)],
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise unittest.SkipTest(f"cannot create a junction on this host: {completed.stderr}")
        self.assertTrue(alias_tool.is_reparse_alias(alias))
        alias_tool.remove_existing_alias(alias)
        self.assertFalse(alias.exists())
        self.assertTrue((skills / "demo-skill" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
