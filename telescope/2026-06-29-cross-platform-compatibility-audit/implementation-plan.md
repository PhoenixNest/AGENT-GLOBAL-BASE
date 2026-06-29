# Implementation Plan — Cross-Platform Compatibility Hardening

**Related Report:** `telescope/2026-06-29-cross-platform-compatibility-audit/research-report.md`  
**Date:** 2026-06-29  
**Author:** Dr. Elias Vance, Laboratory Director — Core Component 00  
**Status:** Awaiting CEO Approval (RQ-04 Gate)  
**Requestor:** CEO

---

## Overview

This implementation plan translates the seven remediation items identified in the
cross-platform compatibility audit into a sequenced, phased delivery roadmap. It also
incorporates the two CEO-directed enhancement tasks (Q1 initialization script, Q2 Syntax
Guard upgrade) evaluated in the companion documents.

**Gate:** No implementation work begins until the CEO approves this plan (RQ-04).

---

## Implementation Scope

| #   | Item                                                                  | Source          | Priority | Effort  |
| --- | --------------------------------------------------------------------- | --------------- | -------- | ------- |
| 1   | Replace hardcoded `pwsh.exe` path in `settings.json` (12 entries)     | Audit Finding 1 | **P0**   | ~5 min  |
| 2   | Fix status-line absolute path in `settings.json` (2 entries)          | Audit Finding 2 | **P0**   | ~2 min  |
| 3   | Fix `server.py` venv bootstrap platform branch                        | Audit Finding 3 | **P1**   | ~10 min |
| 4   | Add platform guard to `system-powershell-syntax-guard.ps1`            | Audit Finding 4 | **P1**   | ~2 min  |
| 5   | Add parallel `Bash(...)` entries to `settings.json` permissions       | Audit Rec 5     | **P2**   | ~5 min  |
| 6   | Update `CLAUDE.md §1` with platform-conditional shell guidance        | Audit Rec 6     | **P2**   | ~5 min  |
| 7   | Q2: Upgrade Syntax Guard to bidirectional OS-aware guard; rename file | Q2 Evaluation   | **P1**   | ~2 h    |
| 8   | Q1 Branch A: `init.py` with pwsh install (macOS / Linux / Windows)    | Q1 Evaluation   | **P1**   | ~3 h    |
| 9   | Q1 Branch B: 14 bash hook translations (`.sh` files)                  | Q1 Evaluation   | **P1**   | ~8–12 h |
| 10  | OS detection spec document (shared Q1 + Q2 reference)                 | Q1 Evaluation   | **P2**   | ~30 min |

---

## Dependency Map

Items 1 and 2 are fully independent — they are point edits to `settings.json` with no
upstream or downstream blockers. They should be applied first to eliminate the P0s
immediately upon CEO approval.

Item 3 (`server.py` venv bootstrap) is independent of all other items. It can proceed
in parallel with items 1 and 2.

Item 4 (syntax guard platform guard) is a prerequisite for Item 7: the minimal guard
(`if ($IsLinux -or $IsMacOS) { exit 0 }`) is the P1 quick-fix; Item 7 replaces it with
the full bidirectional upgrade. Item 4 can ship as a standalone fix if Item 7 is delayed.

Item 5 (Bash permission entries) is independent but logically grouped with Item 1 — both
modify `settings.json`. Apply in the same editing pass.

Item 6 (`CLAUDE.md §1` update) is independent and can be applied at any time.

Item 8 (init script) depends on Item 10 (OS detection spec) — the spec should be drafted
first so the init script adopts the canonical detection primitives.

Item 9 (14 bash hook translations) is independent of Item 8 but the two ship together as
the complete Branch B deliverable. Item 9 is the dominant effort driver.

Item 7 (Q2 full Syntax Guard upgrade) is independent of Q1 work. It replaces Item 4 once
complete; Item 4 can be applied immediately as an interim fix.

---

## Phased Rollout

### Phase 1 — P0 Emergency Fixes (Day 1, ~30 min total)

**Goal:** Eliminate all P0 blockers so the workspace is deployable on any machine.

| Task                              | File                                                | Change                                                            |
| --------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------- |
| 1. Replace 12 hook executor paths | `.claude/settings.json`                             | `C:/PROGRA~1/PowerShell/7/pwsh.exe` → `pwsh`                      |
| 2. Fix 2 status-line paths        | `.claude/settings.json`                             | `C:/Users/ASUS/.claude/statusline.py` → `~/.claude/statusline.py` |
| 3. Fix `server.py` venv bootstrap | `.claude/mcp-servers/workspace-knowledge/server.py` | Add platform branch (4 lines)                                     |

**Deliverable:** A `settings.json` and `server.py` that work on Windows, macOS, and Linux
without manual intervention, assuming `pwsh` is installed and on PATH.

**Gate:** None — apply immediately upon CEO plan approval.

---

### Phase 2 — P1 Configuration Fixes (Day 1, ~30 min total)

**Goal:** Eliminate false positives on POSIX platforms and add permission entries.

| Task                                   | File                                               | Change                                                                                    |
| -------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 4. Syntax guard interim platform guard | `.claude/hooks/system-powershell-syntax-guard.ps1` | Add `if ($IsLinux -or $IsMacOS) { exit 0 }` at line 10                                    |
| 5. Add Bash permission entries         | `.claude/settings.json`                            | Add `Bash(git *)`, `Bash(python *)`, `Bash(prettier *)`, `Bash(ruff *)`, `Bash(pytest *)` |
| 6. Update `CLAUDE.md §1`               | `CLAUDE.md`                                        | Add platform-conditional shell guidance note                                              |

**Deliverable:** A workspace where POSIX users do not receive false PowerShell correction
notices and do not face unexpected permission prompts on common tools.

**Gate:** None — apply immediately after Phase 1.

---

### Phase 3 — Q2 Syntax Guard Full Upgrade (~2 h)

**Goal:** Replace the interim platform guard (Phase 2, Task 4) with the full bidirectional
OS-aware Syntax Guard as designed in `q2-syntax-guard-upgrade-evaluation.md`.

| Task                   | Detail                                                                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Rewrite hook logic     | Windows path: existing 11 PS-guard patterns unchanged. macOS/Linux path: 15 new inverse patterns flagging PS constructs on POSIX. |
| Rename file            | `system-powershell-syntax-guard.ps1` → `system-shell-syntax-guard.ps1`                                                            |
| Update `settings.json` | One hook entry updated to reference new filename                                                                                  |
| Update documentation   | Any references to the old filename in workspace docs                                                                              |

**Deliverable:** A single hook file that correctly guards shell syntax on all three
platforms without false positives or false negatives.

**Gate:** None after CEO plan approval — but Phase 2 Task 4 must be applied first as an
interim measure if Phase 3 is delayed.

---

### Phase 4 — Q1 Initialization Script (~12–15 h total)

**Goal:** Deliver a first-run initialization script that handles cross-platform setup
automatically, eliminating the need for any manual `settings.json` editing by end users.

#### Phase 4a — OS Detection Spec (~30 min)

Create `.claude/scripts/os-detection-spec.md` documenting the canonical OS detection
primitives for Python (`platform.system()`) and PowerShell (`$IsWindows`, `$IsLinux`,
`$IsMacOS`). This is the shared reference for all future hook authors and script writers.

#### Phase 4b — Branch A: pwsh Installation (~3 h)

Write `init.py` at `.claude/scripts/` implementing:

- First-run sentinel check (`.claude/.workspace-initialized`)
- OS detection via `platform.system()`
- `pwsh` already-installed check
- macOS: `brew install --cask powershell` (Homebrew) with direct `.pkg` fallback
- Linux: `snap install powershell --classic` with `apt`/`dnf`/`zypper` fallbacks
- Windows: `winget install Microsoft.PowerShell` with MSI fallback
- Post-install: patch `settings.json` hook executor paths to `pwsh`
- Post-install: patch status-line path to `~/.claude/statusline.py`
- Sentinel file write

#### Phase 4c — Branch B: 14 Bash Hook Translations (~8–12 h)

For each of the 14 `.ps1` hook files, produce a `.sh` equivalent in `.claude/hooks/`:

| Hook                                 | Complexity | Key Translation Challenge                      |
| ------------------------------------ | ---------- | ---------------------------------------------- |
| `prompt-optimizer.sh`                | High       | JSON I/O via `python3 -c`; regex via `grep -P` |
| `pipeline-context-injector.sh`       | High       | JSON I/O; stage pattern matching               |
| `harness-tool-rate-limiter.sh`       | High       | JSON I/O; counter state file management        |
| `rag-index-sync.sh`                  | Medium     | JSON I/O; file path ops                        |
| `harness-error-boundary.sh`          | Medium     | JSON I/O; exit code handling                   |
| `context-budget-monitor.sh`          | Medium     | JSON I/O; arithmetic                           |
| `system-shell-syntax-guard.sh`       | Medium     | Regex pattern matching (inverse of PS guard)   |
| `git-commit-format-guard.sh`         | Medium     | Git output parsing                             |
| `git-branch-naming-guard.sh`         | Low-Medium | String pattern matching                        |
| `write-guard.sh`                     | Low        | File path matching                             |
| `git-line-encoding-validator.sh`     | Low        | File content check                             |
| `multi-agent-branch-naming-guard.sh` | Low        | String pattern matching                        |
| `harness-write-guard.sh`             | Low        | Path matching                                  |
| `git-error-boundary.sh`              | Low        | Exit code handling                             |

All translations use only `bash` + `python3` (pre-installed on macOS/Linux). No `jq` or
other external dependencies. JSON parsing uses `python3 -c "import sys,json; ..."` inline.

Write a Branch B `settings.json` override (`.claude/settings.branch-b.json`) that wires
all hooks to their `.sh` equivalents. The init script copies this file to
`.claude/settings.json` when the user declines pwsh installation.

**Deliverable:** `init.py` at `.claude/scripts/`, 14 `.sh` files in `.claude/hooks/`,
`.claude/settings.branch-b.json`, `.claude/scripts/os-detection-spec.md`.

**Gate:** None after CEO plan approval.

---

## Documentation Updates (Post-Implementation)

Per the RQ-02 table, the following documents require updating when the fixes are applied:

| Document                                                                               | Update Required                                                                 |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `telescope/2026-06-29-cross-platform-compatibility-audit/research-report.md`           | Update status to "Implemented"; add v1.3 version history entry                  |
| `telescope/2026-06-29-cross-platform-compatibility-audit/q1-init-script-evaluation.md` | Mark implementation complete; link to `init.py`                                 |
| `.claude/rules/mcp-governance.md`                                                      | Update `workspace-knowledge` server entry to note cross-platform venv bootstrap |
| `.claude/mcp-servers/workspace-knowledge/README.md`                                    | Add POSIX setup instructions (venv rebuild command)                             |
| Version history entries                                                                | Add to all modified files                                                       |

---

## Commit Plan

| Phase   | Commit Message                                                                                |
| ------- | --------------------------------------------------------------------------------------------- |
| Phase 1 | `chore(claude): apply P0 cross-platform fixes — pwsh path and statusline path`                |
| Phase 2 | `chore(claude): apply P1/P2 fixes — syntax guard, Bash permissions, CLAUDE.md shell guidance` |
| Phase 3 | `chore(hooks): upgrade syntax guard to bidirectional OS-aware shell guard`                    |
| Phase 4 | `feat(claude): add cross-platform init script with pwsh install and bash hook translations`   |

Each commit must include a multi-line body (single-line commits are P2 defects per
`git-workflow.md`).

---

## Effort Summary

| Phase                                        | Scope                       | Estimated Effort |
| -------------------------------------------- | --------------------------- | ---------------- |
| Phase 1 — P0 Fixes                           | 3 file edits                | ~30 min          |
| Phase 2 — P1/P2 Config Fixes                 | 3 file edits                | ~30 min          |
| Phase 3 — Q2 Syntax Guard Full Upgrade       | 1 new file, 1 settings edit | ~2 h             |
| Phase 4 — Q1 Init Script + Bash Translations | 17 new files                | ~12–15 h         |
| Documentation updates                        | 5 files                     | ~1 h             |
| **Total**                                    |                             | **~16–19 h**     |

---

## Risks

| Risk                                                                               | Severity | Mitigation                                                                            |
| ---------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------- |
| Bash hook translations introduce behavioral divergence from PS originals           | P1       | Unit-test each `.sh` hook against the same inputs used to validate the `.ps1` version |
| `init.py` Branch A fails on corporate-managed macOS (MDM blocks Homebrew installs) | P1       | Document manual fallback URL; graceful exit with clear instructions                   |
| Phase 4c effort exceeds estimate (hooks more complex than sampled)                 | P2       | Time-box per hook at 50 min; escalate to CEO if >3 hooks exceed box                   |
| `settings.json` patching in `init.py` corrupts existing user customizations        | P1       | Read-modify-write JSON (never overwrite); backup original before patching             |

---

**Document Version:** 1.0  
**Date:** 2026-06-29  
**Authority:** Core Component 00 Laboratory — Dr. Elias Vance  
**Gate Status:** Awaiting CEO Approval (RQ-04)
