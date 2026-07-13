---
type: "Summary"
description: "Script that retracts OpenKB orphan documents when repo sources disappear."
doc_type: short
full_text: "sources/agents__skills__agent-ready-context__scripts__prune_okf_orphans-py.md"
---

# `.agents/skills/agent-ready-context/scripts/prune_okf_orphans.py`

This script reconciles the OpenKB registry against the repository and retracts KB documents whose source files no longer exist. It is the deletion counterpart to the build-and-add pipeline: `openkb add` only ingests new content, while this script drives `openkb remove` to clean up orphaned documents, raw copies, and downstream pages.

## What it does

- Detects pipeline-owned registry entries whose staged document name is no longer expected from the current repo.
- Distinguishes between three orphan causes:
  - `deleted` - the repository path is gone
  - `renamed` - the content still exists under a new path, detected by comparing content hashes
  - `deselected` - the file still exists in git, but the current selection rules no longer stage it
- Supports a report-only default mode, a `--preview` dry run that shows per-page `openkb remove --dry-run` output, and `--apply` to execute the retraction.
- Refuses to treat non-pipeline documents as orphans by checking for the staging marker in registry metadata.
- Excludes pseudo-documents like `repo-snapshot` and `graphify-report`, which are always regenerated and have no backing repo file.

## Core ideas

### Registry reconciliation
The script reads `.openkb/hashes.json` and treats only documents created by this pipeline as candidates. It then compares those registry entries to the set of staged names that should exist for the current repository state.

### Manifest-first, git-fallback detection
If a freshly built source-pack manifest exists, the script uses it as the authority to avoid drift from the builder. If not, it reconstructs the expected staged names from git-tracked files using mirrored selection and slugging helpers.

This makes the script dependent on staying in sync with `build_okf_source_pack.py`, especially for:

- file selection rules
- slug generation
- bundle grouping

### Rename detection
For missing files, the script tries to determine whether the document was actually moved rather than deleted by comparing the old content hash against newly staged source content. When a rename is detected, it uses `openkb remove --keep-empty` so shared downstream pages can remain if the replacement document will repopulate them.

### Safety controls
The script includes a guard against mass orphaning, which usually means a wrong `--bundle-depth`, a stale manifest, or a mismatched KB/repo target. It also requires explicit confirmation for destructive application unless `--yes` is provided.

## Notable findings

- Deletion reconciliation is intentionally centralized here because it is the only OpenKB mutation path that is deterministic and does not require an LLM call.
- A raw staged file's `source_path` frontmatter is preferred over reversing the slug, because slugs can be lossy when path segments contain `__`.
- The manifest, when present, is treated as authoritative, but the script still emits an advisory if manifest-derived names disagree with what the current repository would stage.
- Documents the builder never creates from repository files are protected from accidental retraction through the `PSEUDO_DOC_NAMES` filter.

## Related concepts

- [[concepts/orphan-retraction]] - identifying and retracting KB content whose source disappeared
- [[concepts/source-pack-manifest]] - how repository paths become staged document names
- [[concepts/manifest-authoritative-reconciliation]] - preferring a built manifest over re-deriving expected output
- [[concepts/rename-vs-delete-detection]] - distinguishing deletion from move-based orphaning
- [[concepts/safe-automation]] - conservative checks before destructive KB operations

## Practical role

In the OpenKB ingestion flow, this script closes the loop after source deletion or repository reshaping. It keeps the KB from accumulating stale raw files and derived pages, while avoiding accidental removal of user-authored or externally ingested content.

## Related Concepts
- [[concepts/hash-registry-coherence]]
- [[concepts/source-pack-staging]]
- [[concepts/deterministic-validation]]
- [[concepts/self-reference-control]]
- [[concepts/generated-content-governance]]
- [[concepts/incremental-compilation]]
- [[concepts/registry-drift]]
- [[concepts/okf-wiki-governance]]
- [[concepts/okf-workflow-governance]]
- [[concepts/source-driven-regeneration]]
- [[concepts/single-source-of-truth]]
- [[concepts/document-normalization]]
- [[concepts/path-based-validation]]

## Entities
- [[entities/prune_okf_orphans-py]]
- [[entities/build_okf_source_pack-py]]
- [[entities/openkb-remove]]
- [[entities/openkb-cli]]
- [[entities/openkb]]
- [[entities/openkb-wiki]]
- [[entities/okf]]
- [[entities/okf-wiki]]
- [[entities/validate_okf_bundle-py]]
- [[entities/git]]
- [[entities/python]]
- [[entities/uv]]
- [[entities/repo-snapshot]]
- [[entities/openkb-add]]
