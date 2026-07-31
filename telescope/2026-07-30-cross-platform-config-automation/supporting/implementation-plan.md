# Implementation Plan — Automated, Cross-Platform Claude Code Configuration

**Parent Investigation:** `2026-07-30-cross-platform-config-automation`
**Parent Report:** `../research-report.md`

---

## Metadata

| Field           | Value                                                             |
| --------------- | ----------------------------------------------------------------- |
| **Plan ID**     | `2026-07-30-cross-platform-config-automation/implementation-plan` |
| **Date**        | 2026-07-30                                                        |
| **Status**      | Authorized by CEO — not yet started                               |
| **Owner**       | Kwame Asante (Harness Engineering, assigned lead)                 |
| **Accountable** | Dr. Elias Vance, CC-00 Laboratory Director                        |
| **Laboratory**  | Core Component 00                                                 |
| **Requestor**   | CEO                                                               |

---

## Objective

Migrate all `.claude/hooks/*.{ps1,sh}` pairs to single Python implementations, invoked uniformly
from `settings.json` via `uv run python <hook>.py`, then retire `platform-settings/` and
`init.py`'s OS-branching entirely — removing the OS fork in `settings.json` at its root instead of
continuing to patch the selection logic around it. Full rationale, findings, and trade-off
analysis: `../research-report.md`.

---

## Division of Responsibilities (Assigned Personnel)

Assigned per the CC-00 crew roster (`core-component-00/crew/README.md`), matching each module's
actual mandate:

| Owner                                              | Responsibility                                                                                                                                                                                                                                             |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Kwame Asante** (Harness Engineering, lead)       | Owns the migration itself — ports all ~15 hook script pairs to Python; designs the shared stdin/stdout/exit-code contract; retires the `.ps1`/`.sh` originals and `platform-settings/` once cutover is verified                                            |
| **Connor O'Malley** (Harness Engineering, support) | Pairs on the port; independently re-verifies each ported hook's parity against its original before sign-off (bus-factor-2, per the crew's own composition assessment)                                                                                      |
| **Ravi Deshmukh** (Infrastructure)                 | Owns the `uv`-based launcher/provisioning layer feeding the hooks — extends the same `prime_mcp_venvs()` pre-sync pattern so hook environments are warm, not resolved cold on first fire                                                                   |
| **Dr. Tomasz Wieczorek** (Safety & Evaluation)     | Adversarially verifies the security/governance-relevant hooks (`prompt-gate-enforcer`, `git-line-encoding-validator`, `multi-agent-commit-format-guard`, the rate limiters) fail closed, not open, post-migration — required before sign-off, not optional |
| **Dr. Elias Vance** (Director)                     | ASE ratification of the cutover; cross-module architecture sign-off; final go/no-go before `platform-settings/` and the dual-template system are deleted                                                                                                   |

---

## Phased Plan

### Phase 1 — Inventory & Design

**Owner:** Kwame Asante (lead)

- Catalog all current hook pairs by trigger event (`UserPromptSubmit` / `PreToolUse` / `PostToolUse`) and current behavior
- Define the shared Python hook contract: stdin/stdout JSON shape, exit-code semantics, the `git rev-parse --show-toplevel`-equivalent repo-root resolution done once in a shared helper rather than per-hook
- Decide the on-disk layout (`.claude/hooks/*.py`) and the exact `uv run python <hook>.py` invocation `settings.json` will use

**Priority:** P0 · **Effort:** 1–2 days · **Impact:** High

### Phase 2 — Port & Parity-Test in Isolation

**Owner:** Kwame Asante + Connor O'Malley (worktree-isolated, one hook migrated and independently verified at a time)

- Port each `.ps1`/`.sh` pair to one Python implementation
- Direct behavioral diff against the original: same inputs → same stdout/exit code, for both the happy path and the deny/error paths
- Do **not** touch `settings.json` in this phase — originals stay live

**Priority:** P0 · **Effort:** 3–5 days · **Impact:** High

### Phase 3 — Unified Cutover

**Owner:** Kwame Asante (lead); Ravi Deshmukh (launcher/provisioning); Dr. Tomasz Wieczorek (adversarial sign-off)

- Retire `platform-settings/settings.bash.json` / `settings.powershell.json` and `init.py`'s OS-branch
- Cut `settings.json` over to the single Python-routed form; verify end-to-end on the reference WSL environment (already instrumented) and require actual Windows-hardware verification before declaring done — a CI runner or a teammate's Windows machine, not simulated (see `../research-report.md` § Risks and Limitations)
- Safety & Evaluation adversarial pass on every governance-relevant hook specifically for fail-closed behavior

**Priority:** P0 · **Effort:** 1–2 days · **Impact:** High

### Phase 4 — ASE Ratification & Cleanup

**Owner:** Dr. Elias Vance (sign-off)

- Director ratification of the cutover
- Delete the now-dead `.ps1`/`.sh` files and `platform-settings/`
- Update `CLAUDE.md` §11 (Hook Resilience) and `AGENTS.md` — current text describes PowerShell-only hook internals (e.g. `prompt-gate-enforcer.ps1`/`.sh`) that will no longer exist in that form
- Close the parent investigation's Status to "Implemented" in both `research-report.md` and its `README.md` index entry, in the same commit

**Priority:** P1 · **Effort:** 1 day · **Impact:** Medium

---

## Implementation Priority Summary

| Phase                                                         | Priority | Effort   | Impact |
| ------------------------------------------------------------- | -------- | -------- | ------ |
| Phase 1 — Inventory & shared Python hook contract design      | P0       | 1–2 days | High   |
| Phase 2 — Port + isolated parity testing (worktree)           | P0       | 3–5 days | High   |
| Phase 3 — Unified `settings.json` cutover + live verification | P0       | 1–2 days | High   |
| Phase 4 — ASE ratification + cleanup (delete originals, docs) | P1       | 1 day    | Medium |

---

## Additional Constraints Carried Over from the Research Report

- Do not delete the `.ps1`/`.sh` originals until Phase 3 is fully verified — keep them as a rollback path through the migration, not as permanent parallel maintenance
- Extend `prime_mcp_venvs()`'s pattern to the hooks' own environment so `uv run`'s dependency resolution never happens cold inside a live hook invocation
- No Windows machine was available at research time — Phase 3's live verification must happen on real Windows hardware, not be waived as "should work by analogy to WSL"

---

## Version History

| Version | Date       | Author       | Changes                                                                  |
| ------- | ---------- | ------------ | ------------------------------------------------------------------------ |
| 1.0     | 2026-07-30 | Kwame Asante | Split out of `research-report.md` into a standalone plan per CEO request |

---

**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
