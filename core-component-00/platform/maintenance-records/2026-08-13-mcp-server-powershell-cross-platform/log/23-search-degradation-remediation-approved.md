# Log Entry 23 — Approval — 2026-09-01

| Field            | Detail                                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 2 — Approval (`core-component-00/platform/maintenance-records/pipeline.md`) |
| **Trigger**      | `log/22`'s two remediation recommendations for Item #9: (1) provision the two required embedding models via `_shared/provision_model.py`, (2) recreate the broken `AGENTS.md` symlinks with the correct target.    |
| **State before** | Both recommendations documented, neither executed; Item #9 open pending Approval.                                                                                                                                  |

**Actions taken:**

1. CEO approved both remediations and directed Execution.
2. **Correction to `log/22`:** re-derived the broken-symlink list independently via `git ls-files -s | grep AGENTS.md` and a blob-hash diff against `git cat-file -p`, rather than trusting `log/22`'s prose transcription. Found **8** broken symlinks, not 9 as `log/22` stated — `log/22` miscounted by including root `AGENTS.md`, which is `git ls-files -s`-confirmed mode `100644` (a real file, intentionally distinct content per `CLAUDE.md` §10 — "comprehensive reference, not auto-loaded"), not a symlink at all. Per this workspace's own rule that a prior `log/` entry is never edited after the fact, `log/22` is left as-is; this entry records the correction rather than rewriting it.

**Verification:**

N/A — this is an approval-stage entry recording a decision and a factual correction, not a code change.

| Field                     | Detail                                                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | Both remediations approved for Execution, with the symlink-fix scope corrected to the actual 8 broken files (enumerated in `log/24`). |
| **Handoff to next stage** | Routes to stage 3 — Execution, recorded in `log/24`.                                                                                  |
