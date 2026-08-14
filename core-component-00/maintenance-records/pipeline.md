# CC-00 Maintenance Pipeline

Canonical stage definitions for a CC-00 maintenance topic (`core-component-00/maintenance-records/`).
Per workspace convention (`templates/README.md`, `company/pipeline/*/pipeline.md`), this file — not
`CLAUDE.md`, not `README.md` — is the authoritative source of truth for pipeline stages and gates.

Scaled deliberately lighter than the Company's 13-stage or Studio's 11-stage pipelines: CC-00
maintenance work is lab-internal operational upkeep, not a product-development lifecycle. Six
stages, one loop-back edge.

---

## Topology

Farouk's framing (`crew/multi-agent-engineering/idris-farouk/`): this is a **Pipeline topology
with an explicit loop-back edge**, not a straight line — a maintenance topic can discover a new
problem _during_ Execution (exactly what happened 2026-08-13: a Remediation stage's own change
broke live service) and must return to Investigation rather than pretend the pipeline only moves
forward. Model that loop as a first-class edge, not an exception.

```
Trigger → Investigation → Approval → Execution → Verification → Close
              ↑                                        │
              └──────────── Reopen (new problem found) ─┘
```

---

## Stages

| #   | Stage                 | Entry criterion                                          | Exit criterion                                                                                                                                                                                                          | Owner                                                                              | Gate                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --- | --------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0   | **Trigger**           | A request, observation, or scheduled event opens a topic | Folder `<YYYY-MM-DD-slug>/` created with `maintenance-record.md`; `Status: Open`                                                                                                                                        | Whoever notices the trigger                                                        | None — opening a topic needs no approval                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 1   | **Investigation**     | Topic open, root cause/scope not yet established         | Findings written to `log/NN-investigation.md`; severity tagged (P0–P3, Asante's bounded-stage discipline — see below); `Status: Investigating` → `Status: Plan ready`                                                   | Domain-appropriate crew member (infra, module lead, or Dr. Vance for cross-module) | None to _investigate_; publishing findings as authoritative requires the investigator to have actually read the affected code/config, not inferred from filenames (per the 2026-08-13 Discovery stage's own practice)                                                                                                                                                                                                                                                                                                   |
| 2   | **Approval**          | A remediation plan exists                                | Sign-off recorded in `maintenance-record.md`'s **Authorized / reviewed by** field, per the existing authority model (self-authorized within documented scope, or named approver)                                        | Whoever holds authority per `crew/CLAUDE.md` § Authority Scope                     | **Required.** No Execution stage starts without an explicit approval record — self-authorization is a valid _outcome_ of this gate, not a way to skip it                                                                                                                                                                                                                                                                                                                                                                |
| 3   | **Execution**         | Plan approved                                            | Changes made and logged to `log/NN-execution.md`, one entry per distinct action; `Status: In Progress` → `Status: Executed, pending verification`                                                                       | The approved owner                                                                 | None to execute once approved; **if a new problem is found mid-execution** (a change breaks something else), do not keep executing — open a `log/NN-incident.md` entry immediately and route to the Reopen edge below                                                                                                                                                                                                                                                                                                   |
| 4   | **Verification**      | Execution stage has a testable claim                     | Verification table in the relevant `log/` entry, actual commands/checks run and their results — never a restated intention (mirrors `templates/review-records/final-review.md`'s existing discipline)                   | The approved owner, by default                                                     | **Independent-review gate (Wieczorek's ask):** for any change touching a shared production resource other agents/sessions depend on (a registered MCP server, `.mcp.json`, a shared venv, a cross-module contract) — `Status` may not read `Completed` until someone _other than the executor_ has reviewed the change, even briefly. Self-verification by the implementer is not sufficient for this class of change, the same reasoning ASGF audit execution and independent audit are kept structurally separate for |
| 5   | **Close (or Reopen)** | Verification passed, or a new problem was found          | **Close:** `Status: Completed` (or `Completed with follow-up open` if minor items remain — see below). **Reopen:** append a new `log/NN-incident.md` entry, set `Status: Reopened — see <entry>`, and return to stage 1 | Whoever completes verification                                                     | None to close a fully verified topic; **escalation path (Yusuf's ask):** if a topic stalls — owner unavailable, blocked on a decision — the topic does not sit silently. Escalate to the owner's reporting lead (module lead, or Dr. Vance for cross-cutting roles) after a stall becomes apparent, and note the escalation as its own `log/` entry so the stall itself is part of the record, not invisible                                                                                                            |

---

## Severity tagging (Investigation stage)

Asante's bounded-stage discipline: every topic gets a severity tag at Investigation, so
Verification's rigor scales to what's actually at stake rather than being uniform:

| Tag    | Meaning                                                             | Verification bar                                                                                                                   |
| ------ | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **P0** | Live service broken for an active session/user                      | Independent-review gate mandatory; foreground/manual verification required, not just automated tests                               |
| **P1** | Confirmed defect, not yet broken live, or broken with a workaround  | Independent-review gate mandatory for shared-resource changes; automated verification acceptable if it genuinely covers the change |
| **P2** | Documentation, non-blocking gap, or a defect with no current impact | Independent-review gate optional at the owner's discretion                                                                         |
| **P3** | Routine maintenance, scheduled dependency bump                      | No independent review required                                                                                                     |

---

## Topic-boundary test (Nwosu-Chen's falsifiability requirement)

A new development belongs in an **existing** topic's folder (new `log/` entry, updated `Status`)
if it satisfies **both**:

1. It concerns the same system/resource named in that topic's `maintenance-record.md` **System /
   resource affected** field (not merely a related system — the same one).
2. It was caused by, discovered during, or is a direct follow-up to that topic's prior stages.

A development satisfying only one, or neither, gets a **new** topic folder, even if it's thematically
similar (e.g. "another PowerShell dependency found in a different, unrelated server" is a new
topic; "the fix for _this_ PowerShell dependency broke something else in _this same_ server" is
not). When genuinely ambiguous, default to a new topic — a spurious extra folder costs a reader one
click; a wrongly-merged topic costs them re-deriving which stage's claims are still true.

---

## Staleness bound (Almeida's freshness requirement)

A topic's `Status` field must be updated within the same working session that changes what it
reports as true. A `Status` line that hasn't been touched since a stage that materially changed
reality (a revert, a reopen, a new blocking finding) is not a documentation nicety gap — it is the
record actively lying. If a `Status` update cannot happen immediately (owner unavailable mid-stage),
the topic is stalled per stage 5's escalation path above, not merely "pending."

---

## Related Documentation

- `CLAUDE.md` (this folder) — directory structure, when a topic gets a folder vs. remains a
  single file, and the authoring mechanics of `maintenance-record.md` / `log/` entries.
- `README.md` (this folder) — index of open/closed topics, format-revision history.
- `template/` — copy-ready templates for `maintenance-record.md` and a `log/` entry.
- `crew/CLAUDE.md` § Authority Scope — who can approve what, referenced by stage 2's gate.
- `templates/review-records/final-review.md` — the verification-discipline precedent stage 4 follows.
