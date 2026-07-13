---
type: "Concept"
sources: ["summaries/agents__skills__agent-ready-context__references__openkb-providers-md.md", "summaries/agents__skills__graphify__references__github-and-merge-md.md", "summaries/agents__skills__agent-ready-context__references__dependencies-md.md", "summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py.md", "summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py.md", "summaries/agents__skills__skill-creator__references__dependencies-md.md", "summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py.md", "summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py.md"]
description: "Cross-platform tooling keeps automation reliable across OS and shell differences."
---

# Cross-Platform Tooling

Cross-platform tooling is the practice of designing scripts and automation so they behave predictably across operating systems, shell environments, filesystem conventions, and console configurations. In this wiki, it matters because repository automation should work in fresh or minimally prepared environments without assuming a specific developer machine setup, while still preserving [[concepts/deterministic-validation]] and reliable [[concepts/quality-gates]].

## Why It Matters

Tooling that works only on one platform creates hidden operational risk. A script may succeed on one machine but fail on another because of differences in executable resolution, path handling, symlink support, line endings, console encoding, default shell behavior, or how command shims are exposed to subprocesses. Cross-platform design reduces these avoidable failures and supports [[concepts/graceful-degradation]], [[concepts/offline-first-workflows]], and [[concepts/quality-gates]].

It also matters for repository validators, bootstrap tools, preflight checks, and local adapter utilities, not just build steps. Validation logic is only trustworthy when it can inspect the same content consistently on macOS, Linux, and Windows, even in lightly provisioned environments. Likewise, local repository customization should adapt to platform limits without forcing tracked repository changes, which connects to [[concepts/local-vs-shared-configuration]] and [[concepts/safe-automation]].

The preflight checker in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] makes this concrete by checking Python, `git`, `uv`, optional CLIs, repository writability, and OpenKB config drift in a way that works in fresh repositories and degrades cleanly when optional tooling is missing. It demonstrates that cross-platform tooling is not only about feature support, but also about predictable diagnostics and environment-sensitive fallback behavior.

## Example From the Source

[[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]] provides a concrete example of cross-platform design in a lightweight repository preflight checker, while [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]] extends the same idea into content validation for OKF and OpenKB-style repositories. [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] adds a complementary example focused on local harness adaptation: it creates a repository-local alias to [[entities/agents-md]] using a relative symlink when possible, but falls back to a small Markdown pointer file when symlinks are unavailable.

Key implementation choices across these scripts include:

- Resolving executables with `shutil.which` before invoking them.
- Running the resolved executable path rather than the bare command name.
- Accounting for Windows command shim behavior instead of assuming discovery implies successful execution.
- Using plain ASCII status markers instead of Unicode checkmarks.
- Avoiding unnecessary third-party dependencies for bootstrap tasks, while allowing optional isolation tooling such as [[entities/uv]].
- Using Python standard library facilities like `pathlib`, relative path computation, and recursive file traversal instead of shell-specific commands.
- Normalizing text handling, such as CRLF-to-LF conversion before parsing frontmatter.
- Falling back from a preferred OS feature, such as symlinks, to a simpler representation when configured to do so.
- Verifying repository capabilities directly, such as path writability, rather than inferring them from environment assumptions.
- Returning short, structured diagnostics suitable for both humans and automation.
- Comparing shared config keys against committed examples while leaving provider-specific settings local to each user.

These choices make the tooling more robust across macOS, Linux, and Windows environments.

## Key Patterns

### Explicit executable resolution

One cross-platform failure mode is that a command appears discoverable but cannot be launched correctly when passed to a subprocess by its bare name. The source material addresses this by resolving the command path first and then executing that resolved path. The preflight checker explicitly notes that Windows command shims may be found by `shutil.which` but not correctly resolved by subprocess when only the original command name is used.

This pattern improves reliability at the boundary between the script and external tools, and it connects closely to [[concepts/tool-boundaries]] and [[concepts/dependency-management]].

### Conservative console output

Terminal output that looks fine on one system can become unreadable or error-prone on another. The preflight script uses `+` and `!` markers instead of Unicode symbols because some Windows consoles may use cp1252 and fail to print checkmarks correctly.

This is a practical example of designing for broad compatibility rather than idealized output formatting.

### Minimal runtime assumptions

Cross-platform tooling is easier to trust when it does not depend on a large, preconfigured environment. The preflight checker intentionally avoids third-party dependencies and can run with bare `python3`, while still preferring `uv run` for isolation. It treats `uv` as a hard prerequisite, but still provides a degraded fallback path for running the script itself when the user has not yet installed it. It also distinguishes between hard prerequisites and optional tooling, so repositories can still be inspected even when some preferred tools are absent. The validator follows a similar pattern: it can execute without PyYAML, but it degrades clearly by reporting that YAML parseability cannot be fully validated locally.

The local alias helper follows the same principle in a different domain: it does not assume symlink support is available everywhere and can substitute a plain Markdown pointer file instead. That balance supports [[concepts/tooling-context-isolation]], [[concepts/tooling-consent-and-pin-management]], [[concepts/llm-free-knowledge-bootstrap]], and [[concepts/graceful-degradation]].

### Capability testing over assumption

Instead of assuming the filesystem and repository layout behave as expected, the preflight checker tests writability by creating and removing a probe file. This is more portable than inferring capability from configuration alone and aligns with [[concepts/filesystem-validation]] and [[concepts/deterministic-validation]].

The validator applies the same mindset at the content level: rather than assuming files are well-formed, it checks UTF-8 readability, YAML structure, required frontmatter, reserved-file rules, and internal link integrity directly from repository contents.

The alias helper extends this pattern to local adaptation. It attempts symlink creation directly, catches failure, and then either degrades to a pointer file or exits according to explicit policy. This is a stronger cross-platform strategy than assuming symlink behavior from operating system identity alone.

The preflight checker also applies capability testing to repository configuration: it checks whether `okf/.openkb/config.yaml` exists, compares the shared keys `language`, `pageindex_threshold`, and `entity_types` against `config.yaml.example`, and warns when local and committed shared settings drift. That approach keeps cross-platform compatibility checks tied to the same source of truth for all contributors.

### Platform-neutral file and text handling

Cross-platform reliability often depends on avoiding shell-specific behavior and normalizing file content before parsing. The validator uses `pathlib` for filesystem traversal and converts CRLF to LF before splitting frontmatter, making Markdown parsing less sensitive to operating-system line ending differences.

The alias helper uses `pathlib` plus relative path calculations to keep aliases repository-local and portable across directory layouts, and it normalizes stored exclude paths with forward slashes before writing them to `.git/info/exclude`. These patterns are closely related to [[concepts/line-ending-normalization]] and [[concepts/path-safety]] and help keep repository automation portable and reproducible.

The preflight checker adds another practical layer here by using a small scalar-only YAML reader to compare shared config keys without depending on a full YAML parser. That keeps the drift check lightweight while still surfacing mismatches in config surfaces that should remain aligned across contributors.

### Standard-library-first automation

The preflight checker emphasizes portability by relying on the Python standard library for command discovery, process execution, filesystem probing, JSON output, and CLI argument parsing. The validator similarly emphasizes OS-agnostic implementation by relying on `pathlib`, `tempfile`, and `subprocess` rather than shell commands or symlink-dependent behavior.

The alias helper reinforces the same approach: it uses only standard library modules such as `argparse`, `os`, and `pathlib` to manage paths, Git-local exclusions, and fallback behavior. That approach strengthens [[concepts/offline-first-workflows]] and reduces friction during [[concepts/repository-ingestion]].

### Local adaptation without repository drift

Cross-platform tooling often has to bridge differences in external harness expectations without changing shared repository policy. The alias helper does this by creating a local alias to [[entities/agents-md]] and recording that alias in `.git/info/exclude` rather than modifying tracked ignore files.

The preflight checker reflects a related principle at the diagnostic level: it checks for repository-local vendored skills, companion skills, writable internal paths, and OpenKB config drift without mutating shared project structure beyond temporary probe files. It also distinguishes between per-user config locations and shared config surfaces, warning when `okf/.openkb/config.yaml` diverges from `config.yaml.example` on the keys that are intended to stay in sync. This keeps compatibility checks informative while minimizing unintended repository drift. Together, these patterns tie cross-platform tooling to [[concepts/local-vs-shared-configuration]] and [[concepts/single-source-of-truth]].

## Design Principles

Cross-platform tooling often follows a few recurring principles:

- Prefer direct capability checks over environment guesses.
- Keep output compatible with limited or legacy terminals.
- Resolve external tools explicitly before execution.
- Minimize dependencies required for bootstrap tasks.
- Normalize text and path handling before applying validation rules.
- Use standard library abstractions instead of shell-specific behavior when practical.
- Distinguish hard failures from optional enhancements.
- Keep local compatibility shims separate from shared repository state.
- Produce diagnostics that can be read by both humans and machines.
- Treat command discovery, writability, and feature support as testable conditions rather than assumptions.
- Compare only the config keys that are meant to be shared, while leaving per-user provider choices local.

These principles also reinforce [[concepts/skill-based-automation]] and [[concepts/repository-ingestion]], where tools must operate consistently across different repositories and local setups.

## Relationship to Other Concepts

Cross-platform tooling overlaps with several nearby concepts in this wiki:

- [[concepts/filesystem-validation]] because filesystem semantics vary by platform.
- [[concepts/graceful-degradation]] because optional tools or preferred runtimes may be unavailable.
- [[concepts/tooling-context-isolation]] because execution wrappers such as [[entities/uv]] help standardize behavior.
- [[concepts/dependency-management]] because every added dependency increases platform-specific risk.
- [[concepts/line-ending-normalization]] because text parsing must tolerate OS-specific newline conventions.
- [[concepts/path-safety]] because repository-local adaptation depends on preventing unsafe path escapes.
- [[concepts/local-vs-shared-configuration]] because some compatibility adjustments should remain untracked and machine-local.
- [[concepts/deterministic-validation]] because validation is only repeatable when platform differences are controlled.
- [[concepts/preflight-checks]] because repository readiness checks are only useful when they behave consistently across environments.
- [[concepts/quality-gates]] because reliable automation depends on repeatable execution conditions.
- [[concepts/configuration-precedence]] because the checker distinguishes project-local config, user-global config, and committed examples.
- [[concepts/vendor-skill-adoption]] because installed CLIs should be paired with vendored skill copies when they are expected to run in-repo.

## Practical Takeaway

A tool is cross-platform not because it claims broad support, but because it actively accounts for platform differences in command discovery, process execution, console output, filesystem behavior, symlink availability, local Git policy, config precedence, and text normalization. The scripts summarized in [[summaries/agents__skills__agent-ready-context__scripts__check_prereqs-py]], [[summaries/agents__skills__agent-ready-context__scripts__validate_okf_bundle-py]], and [[summaries/agents__skills__subagent-profile-adapter__scripts__ensure_local_alias-py]] demonstrate this by favoring conservative output, explicit executable handling, dependency-light bootstrap behavior, direct validation of repository capabilities, graceful fallback from unavailable platform features, config drift checks, and platform-neutral parsing and path management.

See also: [[summaries/agents__skills__skill-creator__references__dependencies-md]]

See also: [[summaries/agents__skills__subagent-profile-adapter__scripts__inspect_runtime_context-py]]

See also: [[summaries/agents__skills__agent-ready-context__references__dependencies-md]]

See also: [[summaries/agents__skills__graphify__references__github-and-merge-md]]

See also: [[summaries/agents__skills__agent-ready-context__references__openkb-providers-md]]