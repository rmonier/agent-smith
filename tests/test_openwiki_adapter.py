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
        mapped = runner.map_candidate(self.stage, candidate, candidate_state, self.pre_run, self.instructions)
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
        mapped = runner.map_candidate(self.stage, candidate, candidate_state, self.pre_run, self.instructions)
        root = mapped["index.md"].decode()
        self.assertTrue(root.startswith('---\nokf_version: "0.1"\n---\n\n# Files'))
        self.assertNotIn("Documentation Index", root)
        sub = mapped["architecture/index.md"].decode()
        self.assertFalse(sub.startswith("---"))
        self.assertEqual(openwiki_validator.validate_openwiki(candidate), [])

    def test_mapping_drops_stray_producer_plan_scratch_file(self) -> None:
        self._write_stock()
        # A run where the model left the temporary plan behind instead of deleting it.
        (self.stage / "openwiki" / "_plan.md").write_bytes(page("Plan", "scratch with no citations"))
        candidate = self.repo / "okf/.okf-build/run/candidate/wiki"
        candidate_state = self.repo / "okf/.okf-build/run/candidate/state/.last-update.json"
        mapped = runner.map_candidate(self.stage, candidate, candidate_state, self.pre_run, self.instructions)
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

    def test_windows_launch_uses_new_console_and_pauses_after(self) -> None:
        with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
            result = terminal_launcher.launch_windows(
                ["openwiki", "code", "--init"], Path("C:/repo"), {"HOME": "C:/repo/okf"}
            )
        self.assertTrue(result)
        popen.assert_called_once()
        args, kwargs = popen.call_args
        self.assertEqual(args[0][0], "cmd.exe")
        self.assertIn("openwiki code --init", args[0][2])
        self.assertIn("pause", args[0][2])
        self.assertEqual(kwargs["creationflags"], terminal_launcher.subprocess.CREATE_NEW_CONSOLE)
        self.assertEqual(kwargs["env"]["HOME"], "C:/repo/okf")

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
            with mock.patch.object(terminal_launcher.subprocess, "Popen") as popen:
                with mock.patch.object(sys, "argv", argv):
                    with contextlib.redirect_stdout(stdout):
                        code = terminal_launcher.main()
        self.assertEqual(code, 0)
        self.assertIn("cmd.exe", stdout.getvalue())
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


if __name__ == "__main__":
    unittest.main()
