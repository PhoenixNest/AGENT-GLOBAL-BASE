# Log Entry 15 — Execution — .mcp.json Git-Tracking Redesign Executed — 2026-08-30

Part of
`core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`).

**Trigger:** CEO approved `log/14`'s proposed design and directed execution ("The CEO has approved
your work. Now you can start your work").

**State before:** As left by `log/14` — proposal documented only, no code changed. Root `.mcp.json`
still git-tracked; no `.mcp.json.example`; `.gitignore` had no entry for `.mcp.json`;
`mcp-config-platform-check.py` still patch-in-place-only (no bootstrap-from-missing-file case).

**Actions taken:**

1. Created `.mcp.json.example` at repo root as the new committed template — same content as the
   current tracked `.mcp.json`, Windows default path preserved (matches the existing committed
   convention).
2. Added `.mcp.json` to root `.gitignore`, with a comment pointing at this maintenance topic.
3. Ran `git rm --cached .mcp.json` — untracks the file from git **without deleting the working
   copy on disk**, so this session's own live MCP connections were not disturbed.
4. Rewrote `.claude/hooks/mcp-config-platform-check.py`:
   - Added `TEMPLATE_FILENAME = ".mcp.json.example"`.
   - `main()` now checks whether `.mcp.json` exists; if not, reads `.mcp.json.example` as the
     source instead (`bootstrapping = True`) and runs it through the **same** per-server
     correction loop already used for the OS-mismatch case — no duplicated logic.
   - Write gate changed from `if not corrected: no-op` to `if not bootstrapping and not
corrected: no-op`, so a first-time bootstrap always writes the file (even if the template's
     default already matched this OS), while an ordinary session with an already-correct
     `.mcp.json` remains a zero-write no-op, matching the original hook's cost profile.
   - Split logging/messaging into `bootstrapped` vs. `corrected` decisions so the two cases are
     distinguishable in `hook-invocations.jsonl` and in the session's `additionalContext` message.
   - Updated the module docstring to explain the gitignore/bootstrap/patch-only-if-stale design
     and why full every-session regeneration (the `log/14` first draft) was rejected.
5. Updated `core-component-00/platform/model-context-protocol-servers/CLAUDE.md` § Python Environment (the interpreter-table
   row and the "Cross-platform path resolution" callout) to describe the new mechanism —
   gitignored/machine-local `.mcp.json`, bootstrap-once, patch-only-if-stale, and the new
   `git pull` non-propagation caveat for shared config in the template.
6. Updated `.claude/rules/mcp-governance.md`'s `workspace-knowledge` and `agent-memory` rows with a
   short 2026-08-30 addendum pointing at the new mechanism, without expanding either cell's
   existing condensed-history text (per the CEO's 2026-08-10 consolidation request that this table
   not regrow into an inline changelog).
7. Recorded the CEO's approval in this topic's `maintenance-record.md` header
   (**Authorized / reviewed by** field).

**Verification:**

| Check performed                                                                                                           | Result                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `python3 -c "import ast; ast.parse(...)"` on the rewritten hook                                                           | Syntax OK                                                                                                                                    |
| Simulated fresh clone: isolated temp repo, no `.mcp.json`, both OS venv interpreters present as Linux paths, ran the hook | `.mcp.json` generated from `.mcp.json.example`, both servers' paths correctly flipped Windows→Linux; `systemMessage` reported `bootstrapped` |
| Same temp repo, ran the hook again immediately after                                                                      | No-op — no output, no write (paths already resolved)                                                                                         |
| Same temp repo, manually reverted both paths to Windows (simulating an OS switch), ran the hook again                     | Both paths patched back to Linux; `systemMessage` reported `corrected` — matches the pre-existing (unchanged) stale-path behavior            |
| `git rm --cached .mcp.json` then `test -f .mcp.json`                                                                      | File remains present on disk; only git tracking removed — this session's live MCP servers were not disrupted                                 |

**Independent-review gate (pipeline.md stage 4):** Not yet satisfied. This entry's verification is
self-executed (Claude, within this session) against an isolated simulated clone, not the live
workspace. Per `pipeline.md`, `.mcp.json` and its bootstrap hook are a shared production resource —
`Status` may not read `Completed` until someone other than the executor has independently
confirmed the real behavior on the actual workspace: a genuine fresh-clone/first-session bootstrap
(the open question `log/14` flagged — whether Claude Code reads `.mcp.json` before or after
`SessionStart` hooks run when the file doesn't exist yet — is still unverified against the real
host) and a live `/mcp reconnect`, matching the discipline `log/11`→`log/13` followed for the
original self-healing hook.

**Outcome:** Implemented as approved. `.mcp.json` is gitignored and untracked (working copy
preserved); `.mcp.json.example` is the new committed template; the `SessionStart` hook bootstraps
once on a missing file and otherwise behaves exactly as before (patch-if-stale, no-op otherwise).
Governance docs (`mcp-servers/CLAUDE.md`, `.claude/rules/mcp-governance.md`) updated to match. No
git commit was made — per workspace convention, commits happen only when explicitly requested; all
changes are staged/present in the working tree only.

**Handoff to next stage:** Routes to Stage 4 — Verification, independent-review gate open (see
above). Needs: (1) a real session restart/first-clone check of `.mcp.json`-vs-`SessionStart` load
order, and (2) a live `/mcp reconnect` confirming both servers still connect cleanly under the new
bootstrap path — ideally run by the CEO or someone other than the executing session, per the
independent-review discipline this topic has followed throughout. Until then, `Status` reads
**Executed, pending verification**, not Completed.
