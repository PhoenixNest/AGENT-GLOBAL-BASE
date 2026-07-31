# Research Report — Automated, Cross-Platform Claude Code Configuration: Closing the `settings.json` OS-Fork Gap

---

## Metadata

| Field                | Value                                                                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-07-30-cross-platform-config-automation`                                                                                                                                            |
| **Date Started**     | 2026-07-30                                                                                                                                                                               |
| **Date Completed**   | 2026-07-30                                                                                                                                                                               |
| **Status**           | Complete — implemented (all 4 phases: hooks ported to Python, unified `settings.json` cutover live on `workspace/inspector`, originals removed, CLAUDE.md/AGENTS.md updated), 2026-07-31 |
| **Investigator**     | Kwame Asante (Harness Engineering, assigned lead) — Dr. Elias Vance (Director, accountable)                                                                                              |
| **Laboratory**       | Core Component 00                                                                                                                                                                        |
| **Module(s)**        | Harness Engineering (primary); Infrastructure (supporting)                                                                                                                               |
| **Priority**         | High                                                                                                                                                                                     |
| **Requestor**        | CEO                                                                                                                                                                                      |

---

## Executive Summary

> This investigation continues the workspace's standing goal of automated, out-of-the-box Claude Code configuration — a user should be able to check out this workspace on any device (Windows, macOS, Linux, or WSL) and have the correct configuration select itself, including when the same person moves between devices over time. Pursuing that goal this session surfaced a structural flaw blocking it: `.claude/settings.json` is a single git-tracked file whose _correct content depends on which OS reads it_ (PowerShell-flavored hooks on Windows, bash-flavored hooks on macOS/Linux/WSL), selected locally by `.claude/scripts/init.py`. Because the file is tracked, the same identity working across two OSes (e.g. Linux, then native Windows) can commit one flavor and have it silently overwrite the other on pull — breaking hooks with no obvious cause, and directly undermining the seamless-switch goal rather than serving it. We evaluated four remediation strategies and recommend eliminating the fork at its root: rewrite the ~15 `.ps1`/`.sh` hook script pairs in Python, invoked uniformly via `uv run python <hook>.py` — the same fix already proven this session for the `workspace-knowledge`/`agent-memory` MCP servers' `python`/`python3` PATH-naming problem. This yields one `settings.json`, byte-identical on every OS, permanently closing this failure class and fully realizing the original automated-configuration goal rather than continuing to patch around gaps in it.

---

## Investigation Scope

### What Was Investigated

> How this workspace's `.claude/settings.json` hook configuration behaves when the same git repository is used across multiple operating systems by the same user or team, given that `init.py` currently selects between two OS-specific variants (`platform-settings/settings.bash.json` and the PowerShell-flavored `settings.json`) and materializes the choice into a single tracked file.

### Why This Investigation Was Needed

> Earlier this session, `init.py`'s settings-selection logic was changed from "prefer pwsh whenever it's installed" to "select by OS" (Windows → pwsh, macOS/Linux/WSL → bash) at the CEO's request, matching `CLAUDE.md` §1's statement that the macOS/Linux interactive shell is bash. Verifying that change surfaced a second-order problem the CEO then raised directly: a user who runs `init.py` on Linux and commits the resulting bash-flavored `settings.json` will, on returning to native Windows and pulling that commit, have their working pwsh-flavored config silently replaced by one referencing `command: "bash"` — which frequently doesn't resolve at all on native Windows, breaking every hook.

### Out of Scope

> - The `.mcp.json` / `uv run` fix for the two Python MCP servers (already implemented and verified earlier this session — referenced here only as precedent)
> - Windows-native live verification (no Windows machine was available in this session; see Constraints and Risks)
> - Any other CC-00 module's portability posture (RAG, Context Engineering, Multi-Agent Engineering)

---

## Research Questions

1. Why does a single git-tracked `settings.json` fail to survive being synced across OSes for the same identity?
2. Which of the plausible mitigations (process discipline, git-hook auto-heal, gitignoring the file, removing the OS fork entirely) actually closes the failure mode rather than relocating it?
3. Does the `uv run python <script>` pattern already proven for the MCP servers generalize cleanly to the hook layer?
4. What would a full migration cost, and who in the CC-00 crew should own each part of it?

---

## Methodology

### Approach

> 1. **Live reproduction reasoning** — traced the actual failure mechanically: `init.py`'s OS branch (`.claude/scripts/init.py:429-495`) calls `apply_bash_config()`/`normalise_pwsh_path()`, both of which mutate the _tracked_ `.claude/settings.json` in place; nothing in git or Claude Code is aware that the correct value is machine-dependent.
> 2. **Option enumeration and elimination** — evaluated four candidate fixes (below) against the same two lenses the CEO posed: platform portability and out-of-the-box usability.
> 3. **Precedent check** — confirmed the proposed fix is not a new pattern: `.mcp.json`'s `workspace-knowledge`/`agent-memory` entries were moved from a bare `"command": "python"` (which failed with `ENOENT` on `python3`-only boxes) to `"command": "uv", "args": ["run", "--project", ...]` earlier this session, verified working end-to-end on this WSL machine.

### Tools and Resources

> - This session's own `.claude/scripts/init.py`, `.claude/platform-settings/*.json`, `.claude/hooks/*.{ps1,sh}`, `.mcp.json`
> - `git log`/`git show` against this workspace's own history for prior related work
> - Live verification tools available in this WSL/Ubuntu session (`uv`, `pwsh`, `python3`, `bash`)

### Constraints

> - No native Windows machine was available in this session — the Windows side of the cross-device failure is reasoned from the tracked hook definitions (`command: "bash"` requiring a POSIX shell absent by default on native Windows), not independently reproduced on Windows hardware
> - This report was produced within the same session that authored the `init.py` OS-selection change under review — an inherent conflict-of-interest the report tries to offset by treating that change's own limitation as the central finding, not a footnote

---

## Findings

### Finding 1: A single tracked file cannot safely hold OS-dependent content across a multi-OS git history

**A git-tracked file has exactly one value at any commit — it cannot vary by which machine checks it out.** `settings.json`'s hook `command` fields (`"bash"` vs `"pwsh"`) are OS-dependent by construction, yet the file lives in the same tracked slot regardless of which OS last wrote it. `init.py`'s job is to keep that slot _correct for the machine that just ran it_ — but nothing re-validates it between runs, and a `git pull`/branch switch can silently reintroduce a foreign-OS commit without triggering re-validation.

**Evidence:**

- `apply_bash_config()` (`init.py:130-152`, post this session's idempotency fix) and `normalise_pwsh_path()` (`init.py:85-107`) both write directly to the tracked `_SETTINGS` path
- `settings.local.json` and `.workspace-initialized` are correctly gitignored as machine-specific state (`.claude/.gitignore`), but `settings.json` itself — the file actually carrying the OS-dependent content — is not, and structurally cannot be without reopening the fresh-clone problem (Finding 2)
- No git hook (`core.hooksPath` unset, `.git/hooks/` has no active hooks — confirmed earlier this session) or Claude Code lifecycle event currently re-triggers `init.py` after a `pull`/`checkout`

**Implications:**

- Any team member switching OSes, or any team syncing this repo across heterogeneous machines, will eventually hit this — it is a matter of when, not if
- The bug is silent: hooks fail (often by simply not firing, or by throwing an interpreter-not-found error) with nothing pointing back to "a different OS committed this file"

---

### Finding 2: The tempting fix (gitignore `settings.json`) trades this bug for a worse one

**Hook definitions live _inside_ `settings.json` itself**, so if the file is untracked/absent on a fresh clone, there is nothing present to auto-trigger its own regeneration — no hook can fire to fix a file whose absence is precisely what disables all hooks. This was evaluated and rejected earlier this session for exactly this reason.

**Evidence:**

- Confirmed by direct inspection: `.claude/settings.json`'s `hooks` block is the _only_ mechanism Claude Code has for running anything automatically in this workspace; there is no separate, always-present bootstrap hook outside it
- A fresh clone with `settings.json` gitignored would have zero active hooks, zero MCP permissions, and zero `enabledMcpjsonServers` until a human manually remembers to run `python3 .claude/scripts/init.py` — a manual step with no enforcement, same class of failure as the one causing Finding 1

**Implications:**

- Gitignoring converts a "sometimes silently wrong" file into an "always silently absent until manually initialized" file — not a net improvement, and arguably worse since "wrong" hooks at least sometimes error loudly while "absent" hooks just don't exist

---

### Finding 3: The OS fork is removable at the root, not just patchable, using a pattern already proven this session

**The only reason `settings.json`'s content must differ by OS is that the hook _scripts themselves_ are written in two shell-specific languages** (`.ps1` and `.sh`). If the hooks were written in Python and invoked through a launcher that resolves identically on every OS, there would be nothing left to fork — one `settings.json`, one hook implementation per event, no drift possible.

**Evidence:**

- `.mcp.json` had the exact same shape of problem: `"command": "python"` resolved on Windows but threw `ENOENT` on this `python3`-only WSL box. It was fixed this session by changing to `"command": "uv", "args": ["run", "--project", "<dir>", "python", "<script>"]` — verified end-to-end (FastMCP startup banner, clean stdio handshake) on this machine, and structurally identical in syntax on Windows/macOS/Linux since `uv` itself abstracts the venv layout (`.venv/bin` vs `.venv/Scripts`) internally
- `init.py` was separately hardened this session to auto-install `uv` (mirroring its existing `pwsh` auto-install pattern) and pre-sync (`uv sync`) both MCP servers' environments — meaning `uv` is already an established, auto-provisioned dependency of this workspace, not a new one this proposal would introduce
- The same `uv run python <hook>.py` invocation shape would work for hooks with zero new infrastructure

**Implications:**

- This is a migration, not a new architecture: the launcher mechanism and the auto-install tooling already exist and are already verified working; what remains is porting ~15 script pairs' logic into Python and retiring the dual-template system (`platform-settings/settings.bash.json` / the pwsh-flavored `settings.json`, and the OS-branch in `init.py` that switches between them)

---

## Analysis

### Interpretation of Findings

> The three findings compose into a single conclusion: the workspace's hook layer has an OS fork it doesn't need, and that fork — not the OS-selection logic layered on top of it this session — is the actual root cause of the cross-device overwrite risk the CEO identified. Fixing the selection logic (as done earlier this session) makes the fork _correct more often_; it cannot make the fork _disappear_, because the fork is a property of the file format (two shell languages), not the selection algorithm choosing between them.

### Trade-offs Identified

| Option                                                    | Closes the root cause?                                              | New dependency?                            | Fresh-clone usability                                      | Effort             |
| --------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------- | ------------------ |
| Status quo + manual `init.py --force` discipline          | No — relocates to human memory                                      | None                                       | Unaffected                                                 | None               |
| Git-hook (`post-checkout`/`post-merge`) auto-heal         | Partially — still needs a working shell to invoke `init.py` at all  | `core.hooksPath` wiring                    | Unaffected if wired correctly                              | Low–Medium         |
| Gitignore `settings.json`                                 | No — trades "sometimes wrong" for "always absent until manual init" | None                                       | Regresses (Finding 2)                                      | Low                |
| **Python hook rewrite + `uv run` launcher (recommended)** | **Yes — removes the fork entirely**                                 | `uv` (already required and auto-installed) | Unaffected; single settings.json ships correct on every OS | Medium (migration) |

### Risks and Limitations

> - The migration touches security/governance-relevant hooks (`prompt-gate-enforcer`, `git-line-encoding-validator`, `multi-agent-commit-format-guard`) — any behavioral drift during the port must fail closed, not open; this requires adversarial parity testing, not just a syntax port
> - No Windows machine was available to verify the _current_ failure live end-to-end (see Constraints) or to verify the eventual Python-hook cutover on native Windows; that verification must happen on an actual Windows box or via a teammate/CI runner before the cutover is considered complete
> - `uv run`'s first-invocation dependency resolution has a real cost (demonstrated earlier this session: tens of seconds when a venv isn't pre-warmed) — the hook launcher must reuse the same `prime_mcp_venvs()`-style pre-sync pattern, or a per-hook venv miss could make `UserPromptSubmit`/`PreToolUse` hooks noticeably slow on first run after a dependency change

---

## Recommendations

### Primary Recommendation

> **Migrate all `.claude/hooks/*.{ps1,sh}` pairs to single Python implementations, invoked uniformly from `settings.json` via `uv run python <hook>.py`, then retire `platform-settings/` and `init.py`'s OS-branching entirely.**
>
> - One hook implementation per event (no `.ps1`/`.sh` twins)
> - One `settings.json`, committed, byte-identical on every OS
> - `init.py` simplifies to: ensure `uv` is present/installed (already implemented), `uv sync` the hooks' own dependency environment, done — no more settings-file branching or template copying

### Secondary Recommendations

1. **Do not delete the `.ps1`/`.sh` originals until Phase 3 is fully verified** — keep them as a rollback path through the migration, not as permanent parallel maintenance
2. **Extend `prime_mcp_venvs()`'s pattern to the hooks' own environment** so `uv run`'s dependency resolution never happens cold inside a live hook invocation
3. **Update `CLAUDE.md` §11 (Hook Resilience) and `AGENTS.md`** once the cutover lands — the current text describes PowerShell-only hook internals (e.g. `prompt-gate-enforcer.ps1`/`.sh`) that will no longer exist in that form

### Division of Responsibilities and Implementation Plan

> Full assigned-personnel breakdown and the phased delivery plan are maintained as a standalone
> document, not duplicated here: **`supporting/implementation-plan.md`**. This report is the
> consolidated research synthesis; that document is the executable plan derived from it, per the
> telescope Programme-shape convention (`telescope/CLAUDE.md`).

---

## References

### Internal Documentation

- `.claude/scripts/init.py` (this session's OS-selection and `uv` auto-install additions)
- `.claude/platform-settings/settings.bash.json`, `.claude/platform-settings/settings.powershell.json`
- `.mcp.json` (precedent: `uv run` fix for `workspace-knowledge`/`agent-memory`)
- `CLAUDE.md` §1 (platform-conditional shell) and §11 (Hook Resilience)
- `core-component-00/crew/README.md` (crew roster and module ownership)

### External Sources

- [uv documentation](https://docs.astral.sh/uv/) — `uv run` semantics and cross-platform venv resolution

### Related Work

- This session's live fix of `.mcp.json`'s `python`/`python3` PATH-naming problem (same root pattern, already verified working)
- This session's reconciliation of `platform-settings/settings.bash.json` drift and the OS-first selection change in `init.py` (the proximate trigger for this investigation)

---

## Recommendations Summary for Sign-Off

> **Primary Recommendation:** migrate hooks to Python, invoked via `uv run`, removing the OS fork at its root rather than continuing to patch the selection logic around it. CEO has already authorized this direction; this report is the pre-implementation research step, per that authorization, before Phase 1 begins.

**Director Ratification (2026-07-31):** All 4 phases of the implementation plan are complete —
hooks ported to Python and independently adversarially verified (Phase 1–2), the unified
`settings.json` cutover live on `workspace/inspector` with Windows-side execution verified live
via WSL interop rather than assumed (Phase 3), and the original `.ps1`/`.sh` scripts removed with
`CLAUDE.md`/`AGENTS.md` updated to match (Phase 4). I have reviewed the full implementation
against this report's findings and recommendations and find no deviation requiring further
research. Ratified as Laboratory Director.

> — Dr. Elias Vance

---

## Version History

| Version | Date       | Author                         | Changes                                                              |
| ------- | ---------- | ------------------------------ | -------------------------------------------------------------------- |
| 1.0     | 2026-07-30 | Kwame Asante / Dr. Elias Vance | Initial research report completed                                    |
| 2.0     | 2026-07-31 | Dr. Elias Vance                | Closed out: all 4 phases implemented, Director ratification recorded |

---

**Template Version:** 1.0
**Last Updated:** 2026-07-31
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
