# Log Entry 14 — Investigation (Follow-Up) — .mcp.json Git-Tracking Redesign Proposed — 2026-08-30

Part of
`core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 1 — Investigation (follow-up)
(`core-component-00/maintenance-records/pipeline.md`).

**Trigger:** CEO observed that root `.mcp.json` is still a tracked file, and that Item #1's
2026-08-26 fix (the `SessionStart` self-healing hook, `log/11`) rewrites it in place on disk every
session for whichever OS is running. CEO's concern: this uncommitted, hook-written state could be
accidentally committed, which would ship an OS-specific interpreter path as the new tracked
default and break the MCP server for any user on a different OS who then pulls it — the same class
of failure the 2026-08-25 reopen (`log/10`) was caused by, just introduced by a commit this time
instead of a stale manual edit. CEO asked for a design assessment and, separately, approved
switching this session's working branch to `core00/dev/engineering` for this discussion.

**State before:** Item #1 closed and verified (`log/13`) — `.mcp.json` is git-tracked, its
committed default holds a Windows interpreter path, and `mcp-config-platform-check.py` patches
that path in place, locally, every `SessionStart`, only when the resolved path doesn't exist on
the current OS (a no-op most sessions). This session's own working tree reproduced the exact
symptom under discussion: `.mcp.json` showed as modified (`M .mcp.json`) from the hook's own
Windows→Linux path correction, uncommitted.

**Actions taken:**

1. Confirmed via `git diff`, `git log -- .mcp.json`, and reading `mcp-config-platform-check.py`
   directly that the working-tree diff was the self-healing hook's own correction (not a manual
   edit or a prior commit) — ruled out before any design discussion started.
2. Proposed an initial redesign: replace the committed `.mcp.json` with a committed
   `.mcp.json.example` template, add real `.mcp.json` to `.gitignore`, and have the `SessionStart`
   hook fully regenerate `.mcp.json` from the template every session (substituting the
   OS-appropriate interpreter path) so shared, non-path config in the template (e.g.
   `agent-memory`'s `MEMORY_QDRANT_URL`) keeps propagating without relying on git tracking the
   real file.
3. CEO pushed back on the "regenerate every session" premise: a per-session rewrite carries a real
   cost/risk if it happens near an already-connected MCP server (the same class of risk the
   2026-08-13 bare-`uv` incident and this topic's other `.mcp.json`-write incidents fall under),
   and OS switching is rare in normal operating practice — paying that cost every session to guard
   a rare event is the wrong trade.
4. Revised the proposal to a **generate-once** model: the hook checks first (does `.mcp.json`
   exist, does its `command` path resolve on this OS); it is a no-op unless the file is missing
   (first pull — generate from `.mcp.json.example`) or the resolved path has actually gone stale
   (an OS switch — patch just the path, as today). This keeps the hook's cost/risk profile close
   to identical to the existing `log/11` implementation; only the bootstrap-from-template case for
   a missing file is new.
5. Flagged, but did not resolve or implement, two open questions surfaced by the design assessment
   (see Outcome).

**Verification:**

| Check performed                                                                                  | Result                                                                                                                            |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `git diff .mcp.json` / `git log --oneline -- .mcp.json`, cross-checked against the hook's source | Confirmed the working-tree diff under discussion was `mcp-config-platform-check.py`'s own correction, not a commit or manual edit |
| `git branch --show-current`                                                                      | `core00/dev/engineering` — CEO's branch switch confirmed in effect for this session                                               |

No code changes were made or verified in this entry — this is a documented design proposal only,
per the CEO's explicit instruction to log first and review after. No independent-review gate
applies yet (nothing has been executed against the shared `.mcp.json` resource).

**Outcome:** A revised design is proposed but **not implemented**: commit `.mcp.json.example` as
the template, gitignore the real `.mcp.json`, and change `mcp-config-platform-check.py` from
"patch in place if OS-mismatched" to "generate from template if missing, else patch in place if
OS-mismatched, else no-op" — same trigger conditions as today, plus a first-pull bootstrap case.
Two caveats were raised, not resolved:

- **Unverified:** whether Claude Code reads `.mcp.json` for server registration before or after
  `SessionStart` hooks run on a genuinely fresh clone with no `.mcp.json` yet — if registration
  happens first, a first-time user would need a manual `/mcp reconnect` or session restart after
  the hook creates the file. Needs an actual first-clone test before this is treated as
  transparent.
- **Accepted trade-off, not solved here:** once `.mcp.json` is gitignored and only
  generated/patched (not regenerated every session), non-path shared config in
  `.mcp.json.example` (e.g. `agent-memory`'s `MEMORY_QDRANT_URL`) stops propagating via ordinary
  `git pull` the way it does today. Proposed mitigation is a documentation note in
  `mcp-servers/CLAUDE.md` ("changed shared config in the template? delete your local `.mcp.json`
  to pick it up"), not new hook logic — deferred to the CEO's judgment on whether that's
  sufficient or whether automatic propagation should be built.

No files were changed as part of this entry. `.mcp.json` remains git-tracked; `.mcp.json.example`,
`.gitignore`, and `mcp-config-platform-check.py` are all unmodified.

**Handoff to next stage:** Routes to Stage 2 — Approval. Per `pipeline.md`, no Execution stage may
start without an explicit approval record in `maintenance-record.md`'s **Authorized / reviewed
by** field. CEO stated intent to review this entry before deciding; Execution (creating
`.mcp.json.example`, editing `.gitignore`, rewriting the hook, updating
`.claude/rules/mcp-governance.md`'s Registered Servers table and `mcp-servers/CLAUDE.md`) is
explicitly deferred pending that review.
