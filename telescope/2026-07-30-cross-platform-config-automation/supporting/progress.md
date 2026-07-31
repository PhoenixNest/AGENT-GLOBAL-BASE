# Progress — Automated, Cross-Platform Claude Code Configuration

**Parent plan:** `implementation-plan.md`
**Led by:** Dr. Elias Vance, CC-00 Laboratory Director (CEO-approved lead for planning and execution)
**Last updated:** 2026-07-31

---

## Current Status

| Phase                                   | Owner                                          | Status         |
| ---------------------------------------- | ----------------------------------------------- | -------------- |
| Phase 1 — Inventory & Design              | Kwame Asante                                   | Folded into Phase 2 execution below |
| Phase 2 — Port & Parity-Test in Isolation | Kwame Asante + Connor O'Malley + Dr. Tomasz Wieczorek | **Complete** — all 15 hooks ported, independently verified, merged (11 bugs found and fixed) |
| Phase 3 — Unified Cutover                 | Dr. Elias Vance | **Complete** — committed (`57cc143`) and merged into `workspace/inspector` (`2de0b0a`) |
| Phase 4 — ASE Ratification & Cleanup      | Dr. Elias Vance                                | **Complete** — CLAUDE.md §3/§11 updated, research-report.md ratified and closed to Implemented, telescope/README.md index updated. Not yet committed — see open conflict noted in session-log.md |

---

## Execution Note

Per CEO direction, Phases 1 and 2 were executed via multi-agent orchestration (one agent
per hook performs the port; an independent second agent per hook adversarially verifies parity
and, for governance-critical hooks, fail-closed behavior) to shorten the development cycle, per
`core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
conventions where applicable.

**Phase 3 blocker resolved:** the originally-documented "no native Windows hardware available"
blocker turned out not to apply to this environment — it runs as Ubuntu-on-WSL2 on a genuine
Windows host, and the real Windows `powershell.exe`/`pwsh.exe` binaries are directly invocable
via their `/mnt/c/...` paths, with the WSL project directory reachable from them via the
`\\wsl.localhost\...` UNC path. This was verified live, not assumed: piped-JSON hook invocation,
`uv run` execution, and Python resolution were all confirmed working identically from a real
Windows PowerShell process against this exact repo.

**Phase 3 technical design (all verified against primary-source Claude Code docs, not assumed):**
- Every hook now invoked via **exec form** (`"command": "uv", "args": ["run",
  "${CLAUDE_PROJECT_DIR}/.claude/hooks/<name>.py"]`) — no shell involved at all, so there is no
  `python`/`python3` naming discrepancy (confirmed: this repo's own Linux/WSL side has no bare
  `python`, only `python3`) and no shell-quoting cross-platform risk.
- **Placeholder syntax matters**: exec-form `args` elements only substitute the **braced**
  `${CLAUDE_PROJECT_DIR}` form, not bare `$CLAUDE_PROJECT_DIR` — confirmed the hard way when a
  bare-form draft locked out every tool call in the live session (every `PreToolUse`/`PostToolUse`
  hook failed to spawn simultaneously, since the `"*"`-matcher `prompt-gate-enforcer` hook itself
  was broken); required an out-of-session fix. Documented so this exact mistake isn't repeated.
  Re-verified clean afterward: JSON valid, all 15 hook entries correctly braced, cross-platform
  test still passing on both sides post-fix.
- `defaultShell` is a **different** setting from hook execution (it only affects interactive `!`
  commands) and is intentionally left **unset** in the unified `settings.json` — Claude Code's own
  auto-detection (bash where available, PowerShell otherwise) already matches CLAUDE.md §1's
  documented Windows/Git-Bash exception, so no OS-conditional value is needed.
- `platform-settings/settings.bash.json` and `settings.powershell.json` are retired (deleted) —
  there is now exactly one `settings.json` for every OS. `.claude/scripts/init.py`'s
  `apply_bash_config()`/`_BASH_SETTINGS` copy-on-setup logic (the actual mechanism this whole
  initiative exists to eliminate) is removed accordingly; its unrelated, already-in-progress
  `install_uv`/`prime_mcp_venvs`/pwsh-normalization logic is untouched.
- `enabledMcpjsonServers` now includes `agent-memory` in the unified file (the old
  `settings.powershell.json` omitted it — judged to be drift, not a deliberate Windows exclusion,
  since it's a governance-passing, plain-Python MCP server with no OS-specific constraint).
- Both `uv` versions on this machine are confirmed aligned at `0.12.0` (Windows was updated
  during this phase; no residual skew).

**Known open item, out of scope for Phase 3 itself:** `settings.json` was already carrying a
dangling reference to `.claude/hooks/prompt-write-guard.sh`, which does not exist as a `.sh`,
`.ps1`, or `.py` file anywhere and is entirely absent from `settings.powershell.json` — a
pre-existing broken reference that predates this initiative. Dropped from the unified draft
(carrying forward a reference to a nonexistent file serves no purpose); tracked separately as
task #5 for a decision on whether it was ever meant to exist.

---

## Hooks In Scope (15)

`context-budget-alert`, `git-line-encoding-validator`, `harness-error-boundary-monitor`,
`harness-rate-limiter-turn-reset`, `harness-tool-rate-limiter`, `multi-agent-branch-naming-guard`,
`multi-agent-commit-format-guard`, `pipeline-context-injector`, `prompt-gate-clear`,
`prompt-gate-enforcer`, `prompt-optimizer`, `prompt-quality-gate`, `rag-index-sync`,
`retrieval-augmented-generation-freshness-flag`, `system-shell-syntax-guard`

Governance-critical (extra adversarial scrutiny for fail-closed behavior): `prompt-gate-enforcer`,
`prompt-optimizer`, `prompt-quality-gate`, `git-line-encoding-validator`,
`multi-agent-commit-format-guard`, `harness-tool-rate-limiter`, `multi-agent-branch-naming-guard`

---

## See Also

- `session-log.md` — chronological audit trail
- `checkpoint.json` — machine-readable milestone state
- `../research-report.md` — findings and rationale
- `implementation-plan.md` — full phased plan and division of responsibilities
