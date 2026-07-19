#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
# SPDX-FileCopyrightText: 2026 Romain Monier <https://github.com/rmonier>
# SPDX-License-Identifier: Apache-2.0
"""Offline contract tests for the minimal stock-OpenWiki adapter."""
from __future__ import annotations

import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "agent-ready-context" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_prereqs  # noqa: E402
import establish_openwiki_session as session_establisher  # noqa: E402
import launch_visible_terminal as terminal_launcher  # noqa: E402
import prepare_external_evidence as external_evidence  # noqa: E402
import run_openwiki_staged as runner  # noqa: E402
import validate_openwiki_bundle as openwiki_validator  # noqa: E402


def git(repo: Path, *args: str) -> str:
    executable = shutil.which("git")
    if executable is None:
        raise unittest.SkipTest("git is unavailable")
    completed = subprocess.run(
        [executable, "-c", f"safe.directory={repo.as_posix()}", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr)
    return completed.stdout.strip()


def init_repo(repo: Path) -> None:
    repo.mkdir(parents=True)
    git(repo, "init")


def index_all(repo: Path) -> None:
    git(repo, "add", "--all")


def page(title: str, body: str = "Body") -> bytes:
    return (
        "---\n"
        "type: Concept\n"
        f"title: {title}\n"
        f"description: {title} fixture.\n"
        "---\n\n"
        f"# {title}\n\n{body}\n"
    ).encode()


def wiki_snapshot(*, marker: str = "base") -> dict[str, bytes]:
    return {
        "index.md": b"# Index\n\n[Quickstart](quickstart.md)\n",
        "quickstart.md": page("Quickstart", f"Start {marker}."),
        "INSTRUCTIONS.md": runner.INSTRUCTIONS_TEMPLATE.read_bytes(),
    }


class WorkspaceCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        init_repo(self.repo)


class CorpusAndStageTests(WorkspaceCase):
    def test_tracked_files_are_staged_byte_for_byte_without_binary_decoding(self) -> None:
        binary = b"\x00\xffPDF\r\n\x80\x00"
        files = {
            "README.md": b"# fixture\n",
            "assets/manual.pdf": binary,
            "assets/image.png": b"\x89PNG\r\n\x1a\n\x00\xff",
            "config/.env.example": b"TOKEN=placeholder\n",
            ".env": b"SECRET=never-stage\n",
            "build/generated.bin": b"generated",
            "user-excluded-dir/graph.json": b"{}",
            "okf/wiki/old.md": b"structurally excluded",
            "okf/external/vendor-doc.md": b"# reviewed external evidence\n",
        }
        for rel, raw in files.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        index_all(self.repo)

        corpus = runner.collect_corpus(self.repo, ["user-excluded-dir"])
        selected = {item.path for item in corpus.files}
        self.assertEqual(
            selected,
            {"README.md", "assets/image.png", "assets/manual.pdf", "config/.env.example", "okf/external/vendor-doc.md"},
        )

        stage = self.repo / "okf/.okf-build" / "bytes" / "worktree"
        stage.mkdir(parents=True)
        runner.materialize_corpus(self.repo, stage, corpus)
        self.assertEqual((stage / "assets/manual.pdf").read_bytes(), binary)
        self.assertEqual((stage / "assets/image.png").read_bytes(), files["assets/image.png"])

    def test_user_exclude_is_a_safe_repository_prefix(self) -> None:
        (self.repo / "src").mkdir()
        (self.repo / "src/a.py").write_text("a = 1\n", encoding="utf-8")
        (self.repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        index_all(self.repo)
        corpus = runner.collect_corpus(self.repo, ["src"])
        self.assertEqual([item.path for item in corpus.files], ["README.md"])
        with self.assertRaises(ValueError):
            runner.collect_corpus(self.repo, ["../outside"])

    def test_isolated_stage_has_no_remote_even_when_the_source_repo_does(self) -> None:
        git(self.repo, "remote", "add", "origin", "https://invalid.example/repo.git")
        git(self.repo, "remote", "add", "backup", "ssh://invalid.example/repo.git")
        (self.repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        index_all(self.repo)
        corpus = runner.collect_corpus(self.repo)
        stage = self.repo / "okf/.okf-build" / "remotes" / "worktree"
        pre_run, instructions = runner.prepare_stage(self.repo, stage, corpus, None)
        self.assertIn("README.md", pre_run)
        self.assertEqual(git(stage, "remote"), "")
        self.assertEqual((stage / "openwiki/INSTRUCTIONS.md").read_bytes(), instructions)

    def test_stage_adds_stock_only_frontmatter_to_reserved_log(self) -> None:
        (self.repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        accepted = wiki_snapshot()
        accepted_log = b"# Log\n\n## 2026-07-19\n\n- Existing history.\n"
        accepted["log.md"] = accepted_log
        runner._write_snapshot(self.repo / "okf/wiki", accepted)
        index_all(self.repo)

        corpus = runner.collect_corpus(self.repo)
        stage = self.repo / "okf/.okf-build" / "reserved-log" / "worktree"
        runner.prepare_stage(self.repo, stage, corpus, None)

        staged_log = (stage / "openwiki/log.md").read_bytes()
        self.assertTrue(staged_log.startswith(b"---\n"))
        self.assertTrue(staged_log.endswith(accepted_log))
        self.assertEqual((self.repo / "okf/wiki/log.md").read_bytes(), accepted_log)

    def test_stage_has_no_history_and_no_synthetic_revision(self) -> None:
        (self.repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        index_all(self.repo)
        corpus = runner.collect_corpus(self.repo)
        stage = self.repo / "okf/.okf-build" / "clone" / "worktree"
        pre_run, instructions = runner.prepare_stage(self.repo, stage, corpus, None)
        self.assertIn("README.md", pre_run)
        self.assertEqual((stage / "openwiki/INSTRUCTIONS.md").read_bytes(), instructions)
        with self.assertRaises(AssertionError):
            git(stage, "rev-parse", "--verify", "HEAD")

    def test_git_symlink_mode_is_not_materialized(self) -> None:
        (self.repo / "target.txt").write_text("target\n", encoding="utf-8")
        (self.repo / "link.txt").write_text("target.txt", encoding="utf-8")
        git(self.repo, "add", "target.txt", "link.txt")
        blob = git(self.repo, "hash-object", "-w", "link.txt")
        git(self.repo, "update-index", "--cacheinfo", f"120000,{blob},link.txt")
        corpus = runner.collect_corpus(self.repo)
        self.assertEqual(corpus.unsupported, ["link.txt"])
        self.assertNotIn("link.txt", {item.path for item in corpus.files})

    def test_dry_run_does_not_create_a_stage(self) -> None:
        (self.repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        index_all(self.repo)
        stdout = io.StringIO()
        with mock.patch.object(sys, "argv", ["run_openwiki_staged.py", "--repo", str(self.repo), "--run-id", "dry"]):
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(runner.main(), 0)
        self.assertIn("DRY_RUN", stdout.getvalue())
        self.assertFalse((self.repo / "okf/.okf-build").exists())


class StockOpenWikiInvocationTests(WorkspaceCase):
    def test_resolves_executable_before_subprocess_run(self) -> None:
        # On Windows, subprocess.run(["openwiki", ...]) fails with
        # WinError 2 even though shutil.which("openwiki") finds a real
        # pnpm-installed .CMD shim on PATH: CreateProcess does not do a
        # shell's PATHEXT search on a bare name. Reproduced live against a
        # real pnpm-11 install; guard the fix structurally so it can't
        # regress back to the bare-name form.
        resolved_path = str(self.repo / "resolved-openwiki-shim.CMD")
        stage = self.repo / "stage"
        stage.mkdir()
        with mock.patch.object(runner.shutil, "which", return_value=resolved_path) as which:
            with mock.patch.object(runner.subprocess, "run") as run:
                run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
                runner.run_stock_openwiki(self.repo, stage, ["openwiki", "code", "--update"], 60)
        which.assert_called_once_with("openwiki")
        argv, kwargs = run.call_args
        self.assertEqual(argv[0][0], resolved_path)
        self.assertEqual(argv[0][1:], ["code", "--update"])
        self.assertEqual(kwargs["cwd"], stage)

    def test_falls_back_to_bare_name_when_which_finds_nothing(self) -> None:
        # shutil.which can legitimately return None (PATH misconfigured, or
        # a POSIX environment where the bare name already resolves via
        # os.execvp's own PATH search); do not turn a resolution miss into
        # a hard failure before subprocess even gets a chance to try.
        stage = self.repo / "stage"
        stage.mkdir()
        with mock.patch.object(runner.shutil, "which", return_value=None):
            with mock.patch.object(runner.subprocess, "run") as run:
                run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
                runner.run_stock_openwiki(self.repo, stage, ["openwiki", "code", "--update"], 60)
        argv, _ = run.call_args
        self.assertEqual(argv[0][0], "openwiki")


class EstablishSessionTests(WorkspaceCase):
    def test_prepare_smoke_dir_creates_empty_directory(self) -> None:
        smoke = session_establisher.prepare_smoke_dir(self.repo)
        self.assertTrue(smoke.is_dir())
        # Empty except for its own .git (see test_prepare_smoke_dir_has_its_own_git_init).
        self.assertEqual({p.name for p in smoke.iterdir()}, {".git"})
        self.assertEqual(smoke, self.repo / "okf" / ".okf-build" / "oauth-smoke")

    def test_prepare_smoke_dir_has_its_own_git_init(self) -> None:
        # OpenWiki does not respect the literal invocation cwd as its scope:
        # it walks upward for the enclosing repository's .git and scopes
        # itself there. Reproduced live: without its own .git, the smoke
        # directory (a plain subdirectory of this repository) resolved
        # straight through to the real project root, and OpenWiki wrote a
        # stray openwiki/ and .github/workflows/ there instead of into the
        # throwaway directory. A separate .git one level down must exist so
        # OpenWiki's upward walk stops at the smoke directory itself.
        smoke = session_establisher.prepare_smoke_dir(self.repo)
        self.assertTrue((smoke / ".git").exists())
        self.assertNotEqual((smoke / ".git").resolve(), (self.repo / ".git").resolve())

    def test_prepare_smoke_dir_clears_stale_content(self) -> None:
        # A prior interrupted attempt could leave OpenWiki-managed content
        # behind - reproducing the exact non-empty-directory problem this
        # script exists to avoid, if left uncleared.
        smoke = self.repo / "okf" / ".okf-build" / "oauth-smoke"
        smoke.mkdir(parents=True)
        (smoke / "openwiki").mkdir()
        (smoke / "openwiki" / "index.md").write_text("stale", encoding="utf-8")
        result = session_establisher.prepare_smoke_dir(self.repo)
        self.assertEqual({p.name for p in result.iterdir()}, {".git"})

    def test_build_command_matches_the_known_working_shape(self) -> None:
        # Matches the one invocation empirically confirmed to trigger
        # OpenWiki's OAuth wizard: `openwiki code --init --modelId <id>
        # <message>`, run directly (not through run_openwiki_staged.py) in
        # a directory with no prior wiki content.
        command = session_establisher.build_command("gpt-5.4-mini", "hello")
        self.assertEqual(command, ["openwiki", "code", "--init", "--modelId", "gpt-5.4-mini", "hello"])

    def test_main_prints_the_launcher_command_with_the_right_pieces(self) -> None:
        stdout = io.StringIO()
        argv = ["establish_openwiki_session.py", "--repo", str(self.repo), "--model-id", "gpt-5.4-mini"]
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stdout(stdout):
                code = session_establisher.main()
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("launch_visible_terminal.py", output)
        self.assertIn("--env OPENWIKI_PROVIDER=openai-chatgpt", output)
        self.assertIn(str(self.repo / "okf"), output)
        self.assertIn("openwiki code --init --modelId gpt-5.4-mini", output)
        self.assertTrue((self.repo / "okf" / ".okf-build" / "oauth-smoke").is_dir())

    def test_is_wsl_true_when_wsl_distro_name_set(self) -> None:
        with mock.patch.dict(os.environ, {"WSL_DISTRO_NAME": "Ubuntu"}):
            self.assertTrue(session_establisher.is_wsl())

    def test_is_wsl_true_from_kernel_release_fallback(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(
                session_establisher.platform,
                "uname",
                return_value=mock.Mock(release="6.18.33.2-microsoft-standard-WSL2"),
            ):
                self.assertTrue(session_establisher.is_wsl())

    def test_is_wsl_false_on_a_plain_linux_kernel(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(
                session_establisher.platform, "uname", return_value=mock.Mock(release="6.8.0-generic")
            ):
                self.assertFalse(session_establisher.is_wsl())

    def test_detect_mode_prints_wsl_warning_only_when_detected(self) -> None:
        argv = ["establish_openwiki_session.py", "--repo", str(self.repo), "--model-id", "gpt-5.4-mini", "--detect"]
        for wsl, expect_warning in ((True, True), (False, False)):
            with self.subTest(wsl=wsl):
                stdout = io.StringIO()
                with mock.patch.object(session_establisher, "is_wsl", return_value=wsl):
                    with mock.patch.object(terminal_launcher, "detect", return_value="a new Windows console"):
                        with mock.patch.object(sys, "argv", argv):
                            with contextlib.redirect_stdout(stdout):
                                code = session_establisher.main()
                self.assertEqual(code, 0)
                self.assertEqual("WARNING: this looks like WSL" in stdout.getvalue(), expect_warning)

    def test_credential_path_matches_openwikis_own_env_js(self) -> None:
        home = self.repo / "okf"
        self.assertEqual(session_establisher.credential_path(home), home / ".openwiki" / ".env")

    def test_wait_for_stable_file_returns_true_once_size_stops_changing(self) -> None:
        target = self.repo / "credential.env"
        target.write_text("OPENAI_CHATGPT_ACCESS_TOKEN=\"x\"\n", encoding="utf-8")
        result = session_establisher.wait_for_stable_file(
            target, timeout=2.0, poll_interval=0.02, stability_seconds=0.1
        )
        self.assertTrue(result)

    def test_wait_for_stable_file_times_out_when_file_never_appears(self) -> None:
        target = self.repo / "never-appears.env"
        result = session_establisher.wait_for_stable_file(
            target, timeout=0.1, poll_interval=0.02, stability_seconds=0.1
        )
        self.assertFalse(result)

    def test_launch_dispatches_to_the_right_platform_function(self) -> None:
        with mock.patch.object(session_establisher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher, "launch_windows", return_value="ok") as launch_windows:
                result = session_establisher.launch(["openwiki"], Path("/smoke"), {})
        self.assertEqual(result, "ok")
        launch_windows.assert_called_once()

    def test_detect_mode_reports_mechanism_and_watched_path_without_launching(self) -> None:
        stdout = io.StringIO()
        argv = [
            "establish_openwiki_session.py",
            "--repo",
            str(self.repo),
            "--model-id",
            "gpt-5.4-mini",
            "--detect",
        ]
        with mock.patch.object(session_establisher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
                with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                    with mock.patch.object(sys, "argv", argv):
                        with contextlib.redirect_stdout(stdout):
                            code = session_establisher.main()
        self.assertEqual(code, 0)
        popen.assert_not_called()
        output = stdout.getvalue()
        self.assertIn("cmd.exe", output)
        self.assertIn(str(self.repo / "okf" / ".openwiki" / ".env"), output)
        # --detect must not touch the smoke directory either.
        self.assertFalse((self.repo / "okf" / ".okf-build" / "oauth-smoke").exists())

    def test_auto_close_terminates_once_credential_is_stable(self) -> None:
        argv = [
            "establish_openwiki_session.py",
            "--repo",
            str(self.repo),
            "--model-id",
            "gpt-5.4-mini",
            "--auto-close",
            "--timeout",
            "2",
        ]
        process = mock.Mock()
        env_path = self.repo / "okf" / ".openwiki" / ".env"

        def fake_launch(command: list[str], cwd: Path, env: dict[str, str]) -> mock.Mock:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.write_text("OPENAI_CHATGPT_ACCESS_TOKEN=\"x\"\n", encoding="utf-8")
            return process

        with mock.patch.object(session_establisher, "is_wsl", return_value=False):
            with mock.patch.object(session_establisher, "launch", side_effect=fake_launch):
                with mock.patch.object(
                    session_establisher, "wait_for_stable_file", return_value=True
                ) as wait_mock:
                    with mock.patch.object(
                        terminal_launcher, "terminate_process_tree", return_value=True
                    ) as terminate_mock:
                        with mock.patch.object(sys, "argv", argv):
                            code = session_establisher.main()
        self.assertEqual(code, 0)
        wait_mock.assert_called_once()
        terminate_mock.assert_called_once_with(process)

    def test_auto_close_leaves_window_open_on_timeout(self) -> None:
        argv = [
            "establish_openwiki_session.py",
            "--repo",
            str(self.repo),
            "--model-id",
            "gpt-5.4-mini",
            "--auto-close",
            "--timeout",
            "2",
        ]
        process = mock.Mock()
        with mock.patch.object(session_establisher, "is_wsl", return_value=False):
            with mock.patch.object(session_establisher, "launch", return_value=process):
                with mock.patch.object(session_establisher, "wait_for_stable_file", return_value=False):
                    with mock.patch.object(terminal_launcher, "terminate_process_tree") as terminate_mock:
                        with mock.patch.object(sys, "argv", argv):
                            code = session_establisher.main()
        self.assertEqual(code, 1)
        terminate_mock.assert_not_called()

    def test_auto_close_reports_when_graceful_stop_does_not_respond(self) -> None:
        argv = [
            "establish_openwiki_session.py",
            "--repo",
            str(self.repo),
            "--model-id",
            "gpt-5.4-mini",
            "--auto-close",
            "--timeout",
            "2",
        ]
        process = mock.Mock()
        stderr = io.StringIO()
        with mock.patch.object(session_establisher, "is_wsl", return_value=False):
            with mock.patch.object(session_establisher, "launch", return_value=process):
                with mock.patch.object(session_establisher, "wait_for_stable_file", return_value=True):
                    with mock.patch.object(terminal_launcher, "terminate_process_tree", return_value=False):
                        with mock.patch.object(sys, "argv", argv):
                            with contextlib.redirect_stderr(stderr):
                                code = session_establisher.main()
        # Credential is already safely written either way - not a hard failure.
        self.assertEqual(code, 0)
        self.assertIn("safe to close manually", stderr.getvalue())

    def test_auto_close_refuses_to_launch_under_wsl_without_acknowledgement(self) -> None:
        argv = [
            "establish_openwiki_session.py",
            "--repo",
            str(self.repo),
            "--model-id",
            "gpt-5.4-mini",
            "--auto-close",
        ]
        stderr = io.StringIO()
        with mock.patch.object(session_establisher, "is_wsl", return_value=True):
            with mock.patch.object(session_establisher, "launch") as launch_mock:
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stderr(stderr):
                        code = session_establisher.main()
        self.assertEqual(code, 3)
        launch_mock.assert_not_called()
        self.assertIn("WARNING: this looks like WSL", stderr.getvalue())
        self.assertIn("--acknowledge-wsl-risk", stderr.getvalue())
        # Refusing must happen before the smoke directory is even touched -
        # nothing should be prepared for a launch that never happens.
        self.assertFalse((self.repo / "okf" / ".okf-build" / "oauth-smoke").exists())

    def test_auto_close_proceeds_under_wsl_with_acknowledgement(self) -> None:
        argv = [
            "establish_openwiki_session.py",
            "--repo",
            str(self.repo),
            "--model-id",
            "gpt-5.4-mini",
            "--auto-close",
            "--acknowledge-wsl-risk",
            "--timeout",
            "2",
        ]
        process = mock.Mock()
        with mock.patch.object(session_establisher, "is_wsl", return_value=True):
            with mock.patch.object(session_establisher, "launch", return_value=process) as launch_mock:
                with mock.patch.object(session_establisher, "wait_for_stable_file", return_value=True):
                    with mock.patch.object(terminal_launcher, "terminate_process_tree", return_value=True):
                        with mock.patch.object(sys, "argv", argv):
                            code = session_establisher.main()
        self.assertEqual(code, 0)
        launch_mock.assert_called_once()


class CandidateMappingTests(WorkspaceCase):
    def setUp(self) -> None:
        super().setUp()
        (self.repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        accepted = wiki_snapshot()
        runner._write_snapshot(self.repo / "okf/wiki", accepted)
        index_all(self.repo)
        self.stage = self.repo / "okf/.okf-build/run/worktree"
        self.stage.mkdir(parents=True)
        corpus = runner.collect_corpus(self.repo)
        runner.materialize_corpus(self.repo, self.stage, corpus)
        accepted = runner.markdown_snapshot(self.repo / "okf/wiki")
        runner._write_snapshot(self.stage / "openwiki", accepted)
        self.accepted = runner.markdown_snapshot(self.repo / "okf/wiki")
        self.instructions = runner.protected_instructions(self.repo)
        self.pre_run = {
            path.relative_to(self.stage).as_posix()
            for path in self.stage.rglob("*")
            if path.is_file()
        }

    def _write_stock(self, citation: str = "README.md") -> None:
        stock = self.stage / "openwiki"
        shutil.rmtree(stock)
        generated = {
            "index.md": b"# Index\n\n[Quickstart](/openwiki/quickstart.md)\n",
            "quickstart.md": page(
                "Quickstart",
                "[Architecture](/openwiki/architecture/overview.md)\n\n"
                "## Citations\n"
                f"- `{citation}`\n"
                "- `/CLAUDE.md`\n"
                "- [External spec](https://example.com/spec) — tolerated reference\n",
            ),
            "architecture/overview.md": page(
                "Architecture",
                "```md\n## Citations\n- fenced example bullet with no path\n```\n\n"
                "## Citations\n- `README.md` — annotated evidence bullet",
            ),
            "INSTRUCTIONS.md": page("Vendor replacement", "changed"),
        }
        runner._write_snapshot(stock, generated)
        (stock / ".last-update.json").write_text("{}", encoding="utf-8")

    def test_mapping_restores_contract_normalizes_known_links_and_drops_generated_onboarding(self) -> None:
        self._write_stock()
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"
        mapped = runner.map_candidate(
            self.stage, candidate, candidate_state, self.pre_run, self.instructions, self.accepted
        )
        self.assertEqual(mapped["INSTRUCTIONS.md"], self.instructions)
        quickstart = mapped["quickstart.md"].decode()
        self.assertIn("](architecture/overview.md)", quickstart)
        self.assertNotIn("CLAUDE.md", quickstart)
        self.assertIn("`README.md`", quickstart)
        self.assertFalse((candidate / ".last-update.json").exists())
        self.assertTrue(candidate_state.is_file())

    def test_mapping_rejects_a_citation_absent_from_the_pre_run_stage(self) -> None:
        self._write_stock("missing.java")
        with self.assertRaisesRegex(RuntimeError, "absent before OpenWiki ran"):
            runner.map_candidate(
                self.stage,
                self.repo / "okf/.okf-build/run/candidate/wiki",
                self.repo / "okf/.okf-build/run/candidate/state/.last-update.json",
                self.pre_run,
                self.instructions,
                self.accepted,
            )

    def test_unknown_openwiki_link_is_not_rewritten(self) -> None:
        text = "[Missing](/openwiki/not-generated.md)"
        self.assertEqual(runner._normalize_stock_links(text, "index.md", {"index.md"}), text)

    def test_mapping_normalizes_generated_index_frontmatter(self) -> None:
        self._write_stock()
        stock = self.stage / "openwiki"
        (stock / "index.md").write_bytes(
            b'---\ntype: Documentation Index\ntitle: "OpenWiki"\ndescription: "Files and subdirectories in OpenWiki."\n---\n\n'
            b"# Files\n\n- [Quickstart](quickstart.md) - entry\n\n# Directories\n\n- [architecture/](architecture/)\n"
        )
        (stock / "architecture" / "index.md").write_bytes(
            b'---\ntype: Documentation Index\ntitle: "architecture"\ndescription: "Files and subdirectories in architecture."\n---\n\n'
            b"# Files\n\n- [Overview](overview.md) - page\n"
        )
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"
        mapped = runner.map_candidate(
            self.stage, candidate, candidate_state, self.pre_run, self.instructions, self.accepted
        )
        root = mapped["index.md"].decode()
        self.assertTrue(root.startswith('---\nokf_version: "0.1"\n---\n\n# Files'))
        self.assertNotIn("Documentation Index", root)
        sub = mapped["architecture/index.md"].decode()
        self.assertFalse(sub.startswith("---"))
        self.assertEqual(openwiki_validator.validate_openwiki(candidate), [])

    def test_mapping_preserves_root_index_when_page_set_is_unchanged(self) -> None:
        stock = self.stage / "openwiki"
        shutil.rmtree(stock)
        generated = dict(self.accepted)
        generated["index.md"] = (
            b"---\n"
            b"type: Documentation Index\n"
            b"title: OpenWiki\n"
            b"description: Generated index.\n"
            b"---\n\n"
            b"# Files\n\n- [Quickstart](quickstart.md)\n"
        )
        generated["quickstart.md"] = page(
            "Quickstart", "Start base.\n\n## Citations\n- `README.md`"
        )
        runner._write_snapshot(stock, generated)
        (stock / ".last-update.json").write_text("{}", encoding="utf-8")
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"

        mapped = runner.map_candidate(
            self.stage, candidate, candidate_state, self.pre_run, self.instructions, self.accepted
        )

        self.assertEqual(mapped["index.md"], self.accepted["index.md"])

    def test_mapping_normalizes_generated_markdown_to_lf(self) -> None:
        self._write_stock()
        stock_quickstart = self.stage / "openwiki/quickstart.md"
        stock_quickstart.write_bytes(stock_quickstart.read_bytes().replace(b"\n", b"\r\n"))
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"

        mapped = runner.map_candidate(
            self.stage, candidate, candidate_state, self.pre_run, self.instructions, self.accepted
        )

        self.assertNotIn(b"\r", mapped["quickstart.md"])

    def test_mapping_rejects_changed_body_with_stale_timestamp(self) -> None:
        stock = self.stage / "openwiki"
        shutil.rmtree(stock)
        accepted = dict(self.accepted)
        accepted["quickstart.md"] = page(
            "Quickstart",
            "Start base.\n\n## Citations\n- `README.md`",
        ).replace(b"description: Quickstart fixture.\n", b"description: Quickstart fixture.\ntimestamp: 2026-07-16T07:21:44.902Z\n")
        generated = dict(accepted)
        generated["quickstart.md"] = generated["quickstart.md"].replace(
            b"Start base.", b"Start changed."
        )
        runner._write_snapshot(stock, generated)
        (stock / ".last-update.json").write_text("{}", encoding="utf-8")

        with self.assertRaisesRegex(RuntimeError, "without advancing its existing timestamp"):
            runner.map_candidate(
                self.stage,
                self.repo / "okf/.okf-build/run/candidate/wiki",
                self.repo / "okf/.okf-build/run/candidate/state/.last-update.json",
                self.pre_run,
                self.instructions,
                accepted,
            )

    def test_mapping_rejects_timestamp_churn_without_body_change(self) -> None:
        stock = self.stage / "openwiki"
        shutil.rmtree(stock)
        accepted = dict(self.accepted)
        accepted["quickstart.md"] = page(
            "Quickstart",
            "Start base.\n\n## Citations\n- `README.md`",
        ).replace(b"description: Quickstart fixture.\n", b"description: Quickstart fixture.\ntimestamp: 2026-07-16T07:21:44.902Z\n")
        generated = dict(accepted)
        generated["quickstart.md"] = generated["quickstart.md"].replace(
            b"2026-07-16T07:21:44.902Z", b"2026-07-19T10:00:00Z"
        )
        runner._write_snapshot(stock, generated)
        (stock / ".last-update.json").write_text("{}", encoding="utf-8")

        with self.assertRaisesRegex(RuntimeError, "timestamp changed without a body change"):
            runner.map_candidate(
                self.stage,
                self.repo / "okf/.okf-build/run/candidate/wiki",
                self.repo / "okf/.okf-build/run/candidate/state/.last-update.json",
                self.pre_run,
                self.instructions,
                accepted,
            )

    def test_mapping_strips_stock_frontmatter_from_reserved_log(self) -> None:
        self._write_stock()
        stock = self.stage / "openwiki"
        stock_log = (
            b"---\n"
            b"type: OpenWiki Log\n"
            b"title: Log\n"
            b"description: Chronological update history for this wiki.\n"
            b"---\n\n"
            b"# Log\n\n## 2026-07-19\n\n- Refreshed.\n"
        )
        (stock / "log.md").write_bytes(stock_log)
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"

        mapped = runner.map_candidate(
            self.stage, candidate, candidate_state, self.pre_run, self.instructions, self.accepted
        )

        self.assertEqual(mapped["log.md"], b"# Log\n\n## 2026-07-19\n\n- Refreshed.\n")
        self.assertEqual(openwiki_validator.validate_openwiki(candidate), [])

    def test_mapping_drops_stray_producer_plan_scratch_file(self) -> None:
        self._write_stock()
        # A run where the model left the temporary plan behind instead of deleting it.
        (self.stage / "openwiki" / "_plan.md").write_bytes(page("Plan", "scratch with no citations"))
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"
        mapped = runner.map_candidate(
            self.stage, candidate, candidate_state, self.pre_run, self.instructions, self.accepted
        )
        self.assertNotIn("_plan.md", mapped)
        self.assertFalse((candidate / "_plan.md").exists())


class ValidationAndPromotionTests(WorkspaceCase):
    def test_thin_validator_uses_generic_okf_and_requires_index_route(self) -> None:
        valid = self.repo / "valid"
        runner._write_snapshot(valid, wiki_snapshot())
        self.assertEqual(openwiki_validator.validate_openwiki(valid), [])

        invalid = self.repo / "invalid"
        runner._write_snapshot(
            invalid,
            {
                "index.md": b"# Index\n\n[Elsewhere](elsewhere.md)\n",
                "quickstart.md": page("Quickstart"),
                "INSTRUCTIONS.md": runner.INSTRUCTIONS_TEMPLATE.read_bytes(),
            },
        )
        errors = openwiki_validator.validate_openwiki(invalid)
        self.assertTrue(any("route to quickstart" in error for error in errors))

    def test_unquoted_colon_in_frontmatter_value_fails_with_actionable_hint(self) -> None:
        # Regression: a real OpenWiki run generated `description: Describes the
        # decentralized transport layer: UDP peer discovery, ...` - an
        # unquoted colon inside the value, which PyYAML reads as a second,
        # nested mapping key and refuses to parse. The deterministic
        # validator must catch this loudly, with a hint pointing at the
        # actual fix, not just a raw parser traceback.
        broken = self.repo / "broken"
        runner._write_snapshot(
            broken,
            {
                "index.md": b"# Index\n\n[Quickstart](quickstart.md)\n",
                "quickstart.md": page("Quickstart"),
                "INSTRUCTIONS.md": runner.INSTRUCTIONS_TEMPLATE.read_bytes(),
                "transport.md": (
                    b"---\n"
                    b"type: Reference\n"
                    b"title: Transport Layer\n"
                    b"description: Describes the decentralized transport layer: UDP peer "
                    b"discovery, TCP one-to-one conversations, and the synchronizer that "
                    b"pushes shared database state between instances.\n"
                    b"---\n\n# Transport Layer\n\nBody.\n"
                ),
            },
        )
        errors = openwiki_validator.validate_openwiki(broken)
        self.assertTrue(any("invalid YAML frontmatter" in error for error in errors))
        self.assertTrue(any("wrap that value in double quotes" in error for error in errors))

    def test_promotion_is_markdown_only_transactional_and_supports_noop(self) -> None:
        accepted = wiki_snapshot(marker="old")
        runner._write_snapshot(self.repo / "okf/wiki", accepted)
        index_all(self.repo)

        run = self.repo / "okf/.okf-build/update"
        runner._write_snapshot(run / "baseline/wiki", accepted)
        candidate = wiki_snapshot(marker="new")
        runner._write_snapshot(run / "candidate/wiki", candidate)
        state = run / "candidate/state/.last-update.json"
        state.parent.mkdir(parents=True)
        state.write_text("{}", encoding="utf-8")
        self.assertEqual(runner.promote_candidate(self.repo, run), "PROMOTED")
        self.assertEqual(runner.markdown_snapshot(self.repo / "okf/wiki"), candidate)
        self.assertTrue((run / "transaction/previous-wiki").is_dir())
        self.assertEqual(
            (self.repo / "okf/.openwiki/.last-update.json").read_text(encoding="utf-8"),
            "{}",
        )

        tooling = self.repo / "okf/wiki/tooling"
        tooling.mkdir(parents=True)
        (tooling / "index.md").write_text("# Tooling\n\n[Project index](../index.md)\n", encoding="utf-8")

        noop = self.repo / "okf/.okf-build/noop"
        runner._write_snapshot(noop / "baseline/wiki", candidate)
        runner._write_snapshot(noop / "candidate/wiki", candidate)
        for rel in ("baseline/state/.last-update.json", "candidate/state/.last-update.json"):
            path = noop / rel
            path.parent.mkdir(parents=True)
            path.write_text("{}", encoding="utf-8")
        self.assertEqual(runner.promote_candidate(self.repo, noop), "NO_CHANGE")
        self.assertFalse((noop / "transaction").exists())

        update2 = self.repo / "okf/.okf-build/update2"
        runner._write_snapshot(update2 / "baseline/wiki", candidate)
        runner._write_snapshot(update2 / "candidate/wiki", wiki_snapshot(marker="third"))
        for rel in ("baseline/state/.last-update.json", "candidate/state/.last-update.json"):
            path = update2 / rel
            path.parent.mkdir(parents=True)
            path.write_text("{}", encoding="utf-8")
        self.assertEqual(runner.promote_candidate(self.repo, update2), "PROMOTED")
        self.assertTrue((tooling / "index.md").is_file(), "tooling overlay must survive promotion")
        live_index = (self.repo / "okf/wiki/index.md").read_text(encoding="utf-8")
        self.assertIn(
            "tooling/index.md",
            live_index,
            "promotion must restore the root-index tooling entry the producer cannot see",
        )

    def test_promotion_rejects_non_markdown_candidate_side_effects(self) -> None:
        accepted = wiki_snapshot()
        runner._write_snapshot(self.repo / "okf/wiki", accepted)
        index_all(self.repo)
        run = self.repo / "okf/.okf-build/reject"
        runner._write_snapshot(run / "baseline/wiki", accepted)
        runner._write_snapshot(run / "candidate/wiki", accepted)
        (run / "candidate/wiki/.last-update.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "non-Markdown"):
            runner.promote_candidate(self.repo, run)

    def test_child_home_is_project_okf_and_literal_command_is_stock_only(self) -> None:
        env = runner.child_environment(self.repo)
        self.assertEqual(env["HOME"], str(self.repo / "okf"))
        self.assertEqual(env["USERPROFILE"], str(self.repo / "okf"))
        user_env = runner.child_environment(self.repo, credential_home="user")
        self.assertEqual(user_env.get("HOME"), os.environ.get("HOME"))
        self.assertEqual(user_env.get("USERPROFILE"), os.environ.get("USERPROFILE"))
        for telemetry_env in (env, user_env):
            self.assertEqual(telemetry_env.get("OPENWIKI_TELEMETRY_DISABLED"), os.environ.get("OPENWIKI_TELEMETRY_DISABLED", "1"))
            self.assertEqual(telemetry_env.get("DO_NOT_TRACK"), os.environ.get("DO_NOT_TRACK", "1"))
        self.assertEqual(runner._literal_openwiki_command(["--", "openwiki", "init"]), ["openwiki", "init"])
        with self.assertRaises(ValueError):
            runner._literal_openwiki_command([sys.executable, "stub.py"])


class ExternalEvidenceTests(WorkspaceCase):
    def _argv(self, *extra: str) -> list[str]:
        return ["prepare_external_evidence.py", "--repo", str(self.repo), *extra]

    @staticmethod
    def _mock_conversion(body: str):
        def fake_run(cmd: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(cmd, 0, stdout=body, stderr="")

        return fake_run

    def test_url_shaped_source_is_rejected(self) -> None:
        argv = self._argv("--source", "https://example.com/doc.pdf", "--resource", "https://example.com/doc.pdf")
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(stderr):
                code = external_evidence.main()
        self.assertEqual(code, 2)
        self.assertIn("URL", stderr.getvalue())
        self.assertFalse((self.repo / "okf/.okf-build/external").exists())

    def test_audio_source_is_rejected_even_without_cli(self) -> None:
        source = self.repo / "clip.mp3"
        source.write_bytes(b"fake-mp3-bytes")
        argv = self._argv("--source", str(source), "--resource", "local-fixture:clip.mp3")
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(stderr):
                code = external_evidence.main()
        self.assertEqual(code, 2)
        self.assertIn("Google Web Speech", stderr.getvalue())
        self.assertFalse((self.repo / "okf/.okf-build/external").exists())

    def test_youtube_url_is_allowed_discloses_network_call_and_omits_source_hash(self) -> None:
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--resource", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--retrieved", "2026-07-18",
            "--out", str(out_dir),
        )
        stderr = io.StringIO()
        with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
            with mock.patch.object(
                external_evidence.subprocess, "run", side_effect=self._mock_conversion("Transcript text.\n")
            ):
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stderr(stderr):
                        code = external_evidence.main()
        self.assertEqual(code, 0)
        self.assertIn("YouTube URL", stderr.getvalue())
        self.assertIn("network call", stderr.getvalue())

        # topic defaults to the slugified video id
        target = out_dir / f"{external_evidence.slugify('dQw4w9WgXcQ')}.md"
        text = target.read_bytes().decode("utf-8")
        self.assertNotIn("x-source-sha256", text)
        self.assertIn('x-converter: "markitdown"', text)
        self.assertIn("Transcript text.\n", text)

    def test_non_youtube_url_still_rejected_alongside_youtube_source(self) -> None:
        self.assertFalse(external_evidence.is_youtube_url("https://example.com/watch?v=abc"))
        self.assertTrue(external_evidence.is_youtube_url("https://youtu.be/abc123"))
        self.assertTrue(external_evidence.is_youtube_url("https://www.youtube.com/watch?v=abc123"))
        self.assertTrue(external_evidence.is_youtube_url("https://music.youtube.com/watch?v=abc123"))

    def test_missing_cli_hints_install_and_writes_nothing(self) -> None:
        source = self.repo / "doc.txt"
        source.write_text("hello", encoding="utf-8")
        argv = self._argv("--source", str(source), "--resource", "https://example.com/doc")
        stderr = io.StringIO()
        with mock.patch.object(external_evidence.shutil, "which", return_value=None):
            with mock.patch.object(sys, "argv", argv):
                with contextlib.redirect_stderr(stderr):
                    code = external_evidence.main()
        self.assertEqual(code, 3)
        self.assertIn("uv tool install", stderr.getvalue())
        self.assertFalse((self.repo / "okf/.okf-build/external").exists())

    def test_out_inside_okf_external_is_refused(self) -> None:
        source = self.repo / "doc.txt"
        source.write_text("hello", encoding="utf-8")
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc",
            "--out", "okf/external",
        )
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(stderr):
                code = external_evidence.main()
        self.assertEqual(code, 2)
        self.assertIn("okf/external", stderr.getvalue())
        self.assertFalse((self.repo / "okf/external").exists())

    def test_successful_conversion_writes_expected_frontmatter_and_lf_newlines(self) -> None:
        source = self.repo / "doc.pdf"
        source.write_bytes(b"%PDF-1.4 fixture bytes")
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.pdf",
            "--topic", "sample-doc",
            "--trust", "official-docs",
            "--retrieved", "2026-07-18",
            "--out", str(out_dir),
        )
        with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
            with mock.patch.object(
                external_evidence.subprocess, "run", side_effect=self._mock_conversion("# Sample\n\nBody text.\n")
            ):
                with mock.patch.object(sys, "argv", argv):
                    code = external_evidence.main()
        self.assertEqual(code, 0)

        raw = (out_dir / "sample-doc.md").read_bytes()
        self.assertNotIn(b"\r\n", raw)
        text = raw.decode("utf-8")
        match = re.match(r"^---\n(.*?)\n---\n\n(.*)$", text, re.DOTALL)
        self.assertIsNotNone(match)
        front, body = match.group(1), match.group(2)
        keys = [line.split(":", 1)[0] for line in front.splitlines()]
        self.assertEqual(
            keys,
            ["type", "title", "description", "resource", "retrieved", "trust", "x-source-sha256", "x-converter"],
        )
        expected_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertIn('type: "external-evidence"', front)
        self.assertIn('resource: "https://example.com/doc.pdf"', front)
        self.assertIn('retrieved: "2026-07-18"', front)
        self.assertIn('trust: "official-docs"', front)
        self.assertIn(f'x-source-sha256: "{expected_sha}"', front)
        self.assertIn('x-converter: "markitdown"', front)
        self.assertEqual(body, "# Sample\n\nBody text.\n")

    def test_conversion_is_deterministic_across_runs(self) -> None:
        source = self.repo / "doc.html"
        source.write_bytes(b"<html>fixture</html>")
        out_a = self.repo / "run-a"
        out_b = self.repo / "run-b"
        for out_dir in (out_a, out_b):
            argv = self._argv(
                "--source", str(source),
                "--resource", "https://example.com/doc.html",
                "--topic", "sample",
                "--retrieved", "2026-07-18",
                "--out", str(out_dir),
            )
            with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
                with mock.patch.object(
                    external_evidence.subprocess, "run", side_effect=self._mock_conversion("Body.\n")
                ):
                    with mock.patch.object(sys, "argv", argv):
                        self.assertEqual(external_evidence.main(), 0)
        self.assertEqual((out_a / "sample.md").read_bytes(), (out_b / "sample.md").read_bytes())

    def test_reversible_mojibake_is_auto_fixed_and_disclosed(self) -> None:
        source = self.repo / "doc.pdf"
        source.write_bytes(b"%PDF-1.4 fixture bytes")
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.pdf",
            "--topic", "sample-doc",
            "--out", str(out_dir),
        )
        stderr = io.StringIO()
        with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
            with mock.patch.object(
                external_evidence.subprocess, "run",
                side_effect=self._mock_conversion("Bonjour, cafÃ© et naÃ¯vetÃ©.\n"),
            ):
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stderr(stderr):
                        code = external_evidence.main()
        self.assertEqual(code, 0)
        text = (out_dir / "sample-doc.md").read_text(encoding="utf-8")
        self.assertIn("x-encoding-fix", text)
        self.assertNotIn("x-encoding-warning", text)
        self.assertIn("café", text)
        self.assertIn("naïveté", text)
        self.assertNotIn("Ã©", text)
        self.assertIn("auto-corrected", stderr.getvalue())

    def test_unrecoverable_replacement_char_is_flagged_but_still_written(self) -> None:
        source = self.repo / "doc.pdf"
        source.write_bytes(b"%PDF-1.4 fixture bytes")
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.pdf",
            "--topic", "sample-doc",
            "--out", str(out_dir),
        )
        stderr = io.StringIO()
        with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
            with mock.patch.object(
                external_evidence.subprocess, "run",
                side_effect=self._mock_conversion("Broken � byte here.\n"),
            ):
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stderr(stderr):
                        code = external_evidence.main()
        self.assertEqual(code, 0)
        text = (out_dir / "sample-doc.md").read_text(encoding="utf-8")
        self.assertIn("x-encoding-warning", text)
        self.assertIn("Broken � byte here.", text)
        self.assertIn("ask the user to choose", stderr.getvalue())

    def test_unmapped_pdf_glyph_cid_placeholder_is_flagged_not_auto_fixed(self) -> None:
        # Regression for the reported failure mode in jsvine/pdfplumber#1280
        # (ligatures decode to the replacement character regardless of
        # expand_ligatures) and its sibling in microsoft/markitdown#1290
        # (unmapped glyphs surface as raw (cid:NNN) tokens instead). Both are
        # lossy at the source - the embedded font's glyph-to-Unicode mapping
        # already failed - so detect_mojibake must catch the CID form and
        # try_fix_mojibake must never claim a fix for pure ASCII noise.
        source = self.repo / "doc.pdf"
        source.write_bytes(b"%PDF-1.4 fixture bytes")
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.pdf",
            "--topic", "sample-doc",
            "--out", str(out_dir),
        )
        stderr = io.StringIO()
        with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
            with mock.patch.object(
                external_evidence.subprocess, "run",
                side_effect=self._mock_conversion("Broken text (cid:588)(cid:607)(cid:623) here.\n"),
            ):
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stderr(stderr):
                        code = external_evidence.main()
        self.assertEqual(code, 0)
        text = (out_dir / "sample-doc.md").read_text(encoding="utf-8")
        self.assertIn("x-encoding-warning", text)
        self.assertNotIn("x-encoding-fix", text)
        self.assertIn("(cid:588)", text)  # written verbatim, never silently dropped
        self.assertIn("pdfplumber#1280", stderr.getvalue())
        self.assertIn("markitdown#1290", stderr.getvalue())

    def test_mojibake_already_in_text_source_is_attributed_to_source_not_converter(self) -> None:
        source = self.repo / "already-bad.html"
        source.write_text("<p>cafÃ© was already like this</p>", encoding="utf-8")
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.html",
            "--topic", "sample-html",
            "--out", str(out_dir),
        )
        stderr = io.StringIO()
        with mock.patch.object(external_evidence.shutil, "which", return_value="/usr/bin/markitdown"):
            with mock.patch.object(external_evidence, "try_fix_mojibake", return_value=None):
                with mock.patch.object(
                    external_evidence.subprocess, "run",
                    side_effect=self._mock_conversion("<p>cafÃ© was already like this</p>\n"),
                ):
                    with mock.patch.object(sys, "argv", argv):
                        with contextlib.redirect_stderr(stderr):
                            code = external_evidence.main()
        self.assertEqual(code, 0)
        self.assertIn("already appear in the local source file itself", stderr.getvalue())

    def test_converter_cmd_uses_alternative_tool_and_records_its_name(self) -> None:
        source = self.repo / "doc.pdf"
        source.write_bytes(b"%PDF-1.4 fixture bytes")
        out_dir = self.repo / "okf/.okf-build/external"
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.pdf",
            "--topic", "sample-doc",
            "--out", str(out_dir),
            "--converter-cmd", "pandoc -f pdf -t gfm",
        )
        with mock.patch.object(
            external_evidence.subprocess, "run",
            side_effect=self._mock_conversion("# Clean\n\nNo issues here.\n"),
        ) as run_mock:
            with mock.patch.object(sys, "argv", argv):
                code = external_evidence.main()
        self.assertEqual(code, 0)
        text = (out_dir / "sample-doc.md").read_text(encoding="utf-8")
        self.assertIn('x-converter: "pandoc"', text)
        called_argv = run_mock.call_args.args[0]
        self.assertEqual(called_argv, ["pandoc", "-f", "pdf", "-t", "gfm", str(source)])

    def test_converter_cmd_rejects_youtube_url_exception(self) -> None:
        argv = self._argv(
            "--source", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--resource", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "--converter-cmd", "some-other-tool",
        )
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(stderr):
                code = external_evidence.main()
        self.assertEqual(code, 2)
        self.assertIn("URL", stderr.getvalue())

    def test_converter_cmd_blank_string_is_rejected(self) -> None:
        source = self.repo / "doc.pdf"
        source.write_bytes(b"%PDF-1.4 fixture bytes")
        argv = self._argv(
            "--source", str(source),
            "--resource", "https://example.com/doc.pdf",
            "--converter-cmd", "   ",
        )
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(stderr):
                code = external_evidence.main()
        self.assertEqual(code, 2)
        self.assertIn("did not parse to a command", stderr.getvalue())


class VisibleTerminalLauncherTests(unittest.TestCase):
    def test_parse_env_overrides_accepts_key_value_pairs(self) -> None:
        self.assertEqual(
            terminal_launcher.parse_env_overrides(["A=1", "B=two words"]),
            {"A": "1", "B": "two words"},
        )
        self.assertEqual(terminal_launcher.parse_env_overrides([]), {})

    def test_parse_env_overrides_rejects_missing_equals_or_empty_key(self) -> None:
        with self.assertRaises(ValueError):
            terminal_launcher.parse_env_overrides(["NOEQUALS"])
        with self.assertRaises(ValueError):
            terminal_launcher.parse_env_overrides(["=value"])

    def test_windows_launch_falls_back_to_cmd_when_no_powershell_found(self) -> None:
        with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_windows(
                    ["openwiki", "code", "--init"], Path("C:/repo"), {"HOME": "C:/repo/okf"}
                )
        self.assertTrue(result)
        popen.assert_called_once()
        args, kwargs = popen.call_args
        self.assertEqual(args[0][0], "cmd.exe")
        self.assertEqual(args[0][1], "/c")
        batch_path = Path(args[0][2])
        self.addCleanup(lambda: batch_path.unlink(missing_ok=True))
        content = batch_path.read_text()
        self.assertIn("openwiki code --init", content)
        self.assertIn("pause", content)
        self.assertIn("del ", content)
        self.assertEqual(
            kwargs["creationflags"],
            terminal_launcher._CREATE_NEW_CONSOLE | terminal_launcher._CREATE_NEW_PROCESS_GROUP,
        )
        self.assertEqual(kwargs["env"]["HOME"], "C:/repo/okf")

    def test_windows_cmd_batch_file_survives_a_flag_looking_argument(self) -> None:
        # Regression for a real bug: cmd.exe /c "<already-quoted command> &
        # pause" as one Popen argv element gets double-quoted by Popen's own
        # list2cmdline pass. cmd.exe does not honor the resulting \" as an
        # escaped quote, so an argument containing " - " arrived at the
        # target program as a detached "-" token ("Unknown option: -").
        # Writing a batch file means list2cmdline only ever runs once.
        text = "Update the wiki pages - preserve manual bodies untouched."
        with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                terminal_launcher.launch_windows(
                    ["openwiki", "code", "--update", "--print", text], Path("C:/repo"), {}
                )
        args, _ = popen.call_args
        batch_path = Path(args[0][2])
        self.addCleanup(lambda: batch_path.unlink(missing_ok=True))
        content = batch_path.read_text()
        self.assertIn(f'"{text}"', content)
        self.assertNotIn('\\"', content)

    def test_windows_launch_prefers_pwsh_over_powershell_and_cmd(self) -> None:
        def which(name: str) -> str | None:
            return "C:/tools/pwsh.exe" if name == "pwsh" else None

        with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_windows(
                    ["openwiki", "code", "--init"], Path("C:/repo"), {"HOME": "C:/repo/okf"}
                )
        self.assertTrue(result)
        args, kwargs = popen.call_args
        self.assertEqual(args[0][0], "C:/tools/pwsh.exe")
        self.assertIn("-NoProfile", args[0])
        self.assertIn("openwiki", args[0][-1])
        self.assertIn("Read-Host", args[0][-1])
        self.assertEqual(
            kwargs["creationflags"],
            terminal_launcher._CREATE_NEW_CONSOLE | terminal_launcher._CREATE_NEW_PROCESS_GROUP,
        )
        self.assertEqual(kwargs["env"]["HOME"], "C:/repo/okf")

    def test_windows_launch_falls_back_to_powershell_when_no_pwsh(self) -> None:
        def which(name: str) -> str | None:
            return "C:/tools/powershell.exe" if name == "powershell" else None

        with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                terminal_launcher.launch_windows(["openwiki"], Path("C:/repo"), {})
        args, _ = popen.call_args
        self.assertEqual(args[0][0], "C:/tools/powershell.exe")
        self.assertIn("-NoProfile", args[0])

    def test_macos_launch_returns_false_without_osascript(self) -> None:
        with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_macos(["echo", "hi"], Path("/repo"), {})
        self.assertFalse(result)
        popen.assert_not_called()

    def test_macos_launch_targets_terminal_app_via_osascript(self) -> None:
        with mock.patch.object(terminal_launcher.shutil, "which", return_value="/usr/bin/osascript"):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_macos(
                    ["openwiki", "code", "--init"], Path("/repo"), {"OPENWIKI_PROVIDER": "openai-chatgpt"}
                )
        self.assertTrue(result)
        args, _ = popen.call_args
        self.assertEqual(args[0][0], "osascript")
        script = args[0][2]
        self.assertIn("Terminal", script)
        self.assertIn("OPENWIKI_PROVIDER", script)
        # Terminal.app's do script types this into whatever the user's
        # default login shell is (zsh since Catalina); zsh's read -p means
        # something different (read from a coprocess, not show a prompt),
        # so the pause step must run under an explicitly forced bash rather
        # than depend on the user's shell choice.
        self.assertIn("bash -c", script)

    def test_linux_launch_prefers_xdg_terminal_exec_when_present(self) -> None:
        def which(name: str) -> str | None:
            if name == terminal_launcher._XDG_TERMINAL_EXEC:
                return "/usr/bin/xdg-terminal-exec"
            if name == "xterm":
                return "/usr/bin/xterm"
            return None

        with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_linux(
                    ["openwiki", "code", "--init"], Path("/repo"), {}, {}
                )
        self.assertTrue(result)
        args, _ = popen.call_args
        self.assertEqual(args[0][0], "/usr/bin/xdg-terminal-exec")
        # xdg-terminal-exec takes the command directly, no -e/-- prefix flag.
        self.assertNotIn("-e", args[0])
        self.assertNotIn("xterm", args[0][0])

    def test_linux_launch_tries_terminals_in_order_and_stops_at_first_found(self) -> None:
        def which(name: str) -> str | None:
            return "/usr/bin/xterm" if name == "xterm" else None

        with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_linux(
                    ["openwiki", "code", "--init"], Path("/repo"), {}, {}
                )
        self.assertTrue(result)
        args, _ = popen.call_args
        self.assertIn("/usr/bin/xterm", args[0])
        self.assertIn("-e", args[0])

    def test_linux_launch_returns_false_when_no_terminal_found(self) -> None:
        with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                result = terminal_launcher.launch_linux(["echo", "hi"], Path("/repo"), {}, {})
        self.assertFalse(result)
        popen.assert_not_called()

    def test_main_exits_3_with_no_command(self) -> None:
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", ["launch_visible_terminal.py"]):
            with contextlib.redirect_stderr(stderr):
                code = terminal_launcher.main()
        self.assertEqual(code, 3)

    def test_main_exits_2_when_no_mechanism_found(self) -> None:
        argv = ["launch_visible_terminal.py", "--", "echo", "hi"]
        stderr = io.StringIO()
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Plan9"):
            with mock.patch.object(sys, "argv", argv):
                with contextlib.redirect_stderr(stderr):
                    code = terminal_launcher.main()
        self.assertEqual(code, 2)
        self.assertIn("echo hi", stderr.getvalue())

    def test_main_dispatches_to_windows_launcher_and_reports_success(self) -> None:
        argv = ["launch_visible_terminal.py", "--env", "HOME=/repo/okf", "--", "openwiki", "code", "--init"]
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher, "launch_windows", return_value=True) as launch:
                with mock.patch.object(sys, "argv", argv):
                    code = terminal_launcher.main()
        self.assertEqual(code, 0)
        launch.assert_called_once()
        _, _, env = launch.call_args[0]
        self.assertEqual(env["HOME"], "/repo/okf")

    def test_detect_mode_reports_windows_mechanism_without_launching(self) -> None:
        argv = ["launch_visible_terminal.py", "--detect"]
        stdout = io.StringIO()
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
                with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                    with mock.patch.object(sys, "argv", argv):
                        with contextlib.redirect_stdout(stdout):
                            code = terminal_launcher.main()
        self.assertEqual(code, 0)
        self.assertIn("cmd.exe", stdout.getvalue())
        popen.assert_not_called()

    def test_detect_mode_reports_pwsh_when_present(self) -> None:
        argv = ["launch_visible_terminal.py", "--detect"]
        stdout = io.StringIO()

        def which(name: str) -> str | None:
            return "C:/tools/pwsh.exe" if name == "pwsh" else None

        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
                with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                    with mock.patch.object(sys, "argv", argv):
                        with contextlib.redirect_stdout(stdout):
                            code = terminal_launcher.main()
        self.assertEqual(code, 0)
        self.assertIn("pwsh", stdout.getvalue())
        popen.assert_not_called()

    def test_detect_mode_never_requires_a_command(self) -> None:
        # --detect alone, no "-- <command>", must not hit the "no command given" error.
        argv = ["launch_visible_terminal.py", "--detect"]
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            with mock.patch.object(sys, "argv", argv):
                code = terminal_launcher.main()
        self.assertEqual(code, 0)

    def test_detect_mode_exits_2_when_nothing_found(self) -> None:
        argv = ["launch_visible_terminal.py", "--detect"]
        stderr = io.StringIO()
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Linux"):
            with mock.patch.object(terminal_launcher.shutil, "which", return_value=None):
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stderr(stderr):
                        code = terminal_launcher.main()
        self.assertEqual(code, 2)

    def test_detect_then_launch_agree_on_the_same_mechanism(self) -> None:
        # The whole point of --detect: what it reports must be what actually gets used.
        def which(name: str) -> str | None:
            return "/usr/bin/gnome-terminal" if name == "gnome-terminal" else None

        with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
            description = terminal_launcher.detect("Linux")
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                terminal_launcher.launch_linux(["openwiki"], Path("/repo"), {}, {})
        self.assertEqual(description, "gnome-terminal")
        args, _ = popen.call_args
        self.assertEqual(args[0][0], "/usr/bin/gnome-terminal")

    def test_detect_never_calls_popen_on_any_platform(self) -> None:
        # Hard structural guarantee, not just a code-review claim: detection
        # must be impossible to accidentally wire up to actually launching
        # anything, on any of the three platforms this script supports, even
        # after future edits to this file.
        def popen_must_not_be_called(*args: object, **kwargs: object) -> None:
            raise AssertionError(f"Popen must never be called during detect(); got args={args} kwargs={kwargs}")

        def which(name: str) -> str | None:
            # Report every known binary as present, so detection takes the
            # "found something" branch on each platform - that branch is
            # exactly where an accidental Popen call would be most likely.
            return f"/usr/bin/{name}"

        with mock.patch.object(terminal_launcher.subprocess, "Popen", side_effect=popen_must_not_be_called):
            with mock.patch.object(terminal_launcher.shutil, "which", side_effect=which):
                for system in ("Windows", "Darwin", "Linux"):
                    result = terminal_launcher.detect(system)
                    self.assertIsNotNone(result, f"expected a mechanism to be found for {system}")

    def test_terminate_returns_true_immediately_if_already_exited(self) -> None:
        process = mock.Mock()
        process.poll.return_value = 0
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            result = terminal_launcher.terminate_process_tree(process)
        self.assertTrue(result)
        process.send_signal.assert_not_called()

    def test_terminate_windows_sends_ctrl_break_and_waits(self) -> None:
        process = mock.Mock()
        process.poll.return_value = None
        process.wait.return_value = 0
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            result = terminal_launcher.terminate_process_tree(process, grace_seconds=5.0)
        self.assertTrue(result)
        process.send_signal.assert_called_once_with(terminal_launcher._CTRL_BREAK_EVENT)
        process.wait.assert_called_once_with(timeout=5.0)

    def test_terminate_windows_escalates_to_taskkill_when_graceful_signal_ignored(self) -> None:
        # Verified live: a real spawned pwsh console did not respond to
        # CTRL_BREAK_EVENT within the grace period. taskkill /T /F is the
        # fallback - a Windows builtin, not a third-party dependency, and
        # the only way to guarantee the whole tree (not just the direct
        # child) actually stops.
        process = mock.Mock()
        process.poll.return_value = None
        process.pid = 4242
        process.wait.side_effect = [
            terminal_launcher.subprocess.TimeoutExpired(cmd="x", timeout=5.0),
            0,
        ]
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher.subprocess, "run") as run:
                result = terminal_launcher.terminate_process_tree(process)
        self.assertTrue(result)
        run.assert_called_once_with(
            ["taskkill", "/T", "/F", "/PID", "4242"], capture_output=True, check=False
        )

    def test_terminate_windows_reports_false_when_still_alive_after_taskkill(self) -> None:
        process = mock.Mock()
        process.poll.return_value = None
        process.pid = 4242
        process.wait.side_effect = terminal_launcher.subprocess.TimeoutExpired(cmd="x", timeout=5.0)
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Windows"):
            with mock.patch.object(terminal_launcher.subprocess, "run") as run:
                result = terminal_launcher.terminate_process_tree(process)
        self.assertFalse(result)
        run.assert_called_once()

    def test_terminate_linux_kills_process_group(self) -> None:
        process = mock.Mock()
        process.poll.return_value = None
        process.pid = 4321
        process.wait.return_value = 0
        # os.getpgid/os.killpg are POSIX-only and do not exist in the os
        # module at all on Windows (where this suite also runs); create=True
        # lets the mock stand in regardless of the host platform.
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Linux"):
            with mock.patch.object(terminal_launcher.os, "getpgid", return_value=4321, create=True) as getpgid:
                with mock.patch.object(terminal_launcher.os, "killpg", create=True) as killpg:
                    result = terminal_launcher.terminate_process_tree(process)
        self.assertTrue(result)
        getpgid.assert_called_once_with(4321)
        killpg.assert_called_once_with(4321, terminal_launcher.signal.SIGTERM)

    def test_terminate_linux_escalates_to_sigkill_when_sigterm_ignored(self) -> None:
        # Unlike SIGTERM, SIGKILL cannot be caught or ignored, so this
        # escalation stays pure Python (no taskkill-equivalent shellout
        # needed on POSIX).
        process = mock.Mock()
        process.poll.return_value = None
        process.pid = 4321
        process.wait.side_effect = [
            terminal_launcher.subprocess.TimeoutExpired(cmd="x", timeout=5.0),
            0,
        ]
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Linux"):
            with mock.patch.object(terminal_launcher.os, "getpgid", return_value=4321, create=True):
                with mock.patch.object(terminal_launcher.os, "killpg", create=True) as killpg:
                    result = terminal_launcher.terminate_process_tree(process)
        self.assertTrue(result)
        killpg.assert_any_call(4321, terminal_launcher.signal.SIGTERM)
        killpg.assert_any_call(4321, terminal_launcher._SIGKILL)

    def test_terminate_darwin_not_supported(self) -> None:
        # launch_macos() returns osascript's own process, not the actual
        # spawned command's - there is nothing to target yet.
        process = mock.Mock()
        process.poll.return_value = None
        with mock.patch.object(terminal_launcher.platform, "system", return_value="Darwin"):
            result = terminal_launcher.terminate_process_tree(process)
        self.assertFalse(result)
        process.send_signal.assert_not_called()


class PrerequisiteTests(unittest.TestCase):
    def test_preflight_only_reports_command_readiness(self) -> None:
        def completed(argv: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            stdout = "true\n" if "rev-parse" in argv else ""
            return subprocess.CompletedProcess(argv, 0, stdout=stdout, stderr="")

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(check_prereqs.shutil, "which", side_effect=lambda name: f"/tools/{name}"):
                with mock.patch.object(check_prereqs.subprocess, "run", side_effect=completed):
                    result = check_prereqs.check(Path(tmp))
        self.assertTrue(result["ok"])
        self.assertEqual(set(result["required"]), {"python>=3.11", "git", "uv", "git-worktree"})
        self.assertEqual(set(result["optional"]), {"fnm", "node", "corepack", "pnpm", "openwiki", "markitdown"})
        self.assertEqual(set(result["writable_paths"]), {"okf/.okf-build", "okf", ".agents/skills"})

    def test_openwiki_version_parses_help_banner_not_a_flag(self) -> None:
        # The pinned CLI has no --version flag (it prints "Unknown option:
        # --version" and exits nonzero); check_prereqs must not surface that
        # error text as if it were a version string.
        banner = "  ___\n╭──╮\n│ >_ OpenWiki v0.2.0 agent docs for codebases │\n╰──╯\n"
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(check_prereqs.shutil, "which", return_value="/tools/openwiki"):
                with mock.patch.object(
                    check_prereqs.subprocess,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, stdout=banner),
                ):
                    ok, detail = check_prereqs.openwiki_version(Path(tmp))
        self.assertTrue(ok)
        self.assertEqual(detail, "OpenWiki v0.2.0")

    def test_openwiki_version_reports_not_found_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(check_prereqs.shutil, "which", return_value=None):
                ok, detail = check_prereqs.openwiki_version(Path(tmp))
        self.assertFalse(ok)
        self.assertEqual(detail, "not found")


if __name__ == "__main__":
    unittest.main()
