# Maintenance Record — [System/Resource Name] — [YYYY-MM-DD]

<!-- Copy this file into core-component-00/maintenance-records/ (not into template/ itself) when
     a maintenance operation is performed on a CC-00 lab server or engineering resource — the
     local dev environment, GPU/CUDA stack, shared dependency footprint, MCP server processes
     (workspace-knowledge, agent-memory, embedder-service), or any other lab-owned infrastructure.
     Name the copy `YYYY-MM-DD-<slug>.md` (e.g. `2026-08-13-embedder-service-idle-timeout-tune.md`)
     to match the workspace's dated-record convention (templates/README.md, telescope/README.md).
     This is a point-in-time snapshot, not a living document — a follow-up operation on the same
     resource gets a new file, not an edit to this one; link back to the prior record instead. -->

**Date:** [YYYY-MM-DD]
**Performed by:** [Name, role — the crew member(s) who did the work, e.g. Ravi Deshmukh
(Infrastructure Engineer)]
**Authorized / reviewed by:** [Name, role — who signed off, if the operation required approval
beyond the performer's own authority. State "Self-authorized — within [role]'s documented
authority scope" if no separate approval was needed. An operation that changes cross-module
architecture (a shared service's design, not just its configuration or a routine dependency bump)
is outside the Infrastructure Engineer's unilateral authority per `crew/CLAUDE.md` § Authority
Scope — name Dr. Vance or the relevant module lead as approver instead of self-authorizing.]
**System / resource affected:** [Named server, dev environment, dependency stack, MCP server
process, GPU/CUDA configuration, CI tooling, etc. — be specific enough that a reader can locate
the affected component without cross-referencing another document. For any change touching a
Python environment, name the specific venv/interpreter (e.g. `mcp-servers/.venv/`) — the shared
venv is a documented convention, and a bare `python` resolving to the system interpreter is a
known defect class (`.claude/rules/mcp-governance.md`).]
**Maintenance type:** [Routine / Scheduled / Emergency / Incident response / Dependency update /
Decommission — pick the closest fit]
**Status:** [Completed / Completed with follow-up open / Rolled back / In progress]

---

## 1. Scope & Trigger

<!-- What made this maintenance necessary now — a schedule, an incident, drift detected during
     onboarding, a version conflict, an idle-timeout tune, etc. If this traces back to an incident
     or an existing research/telescope report, link it here rather than re-describing it. -->

[One or two sentences: why this operation happened, and what triggered it.]

---

## 2. Pre-Maintenance State

<!-- Capture the baseline before any change is made, so the actions below are a provable diff,
     not an unverifiable claim of improvement. -->

[What state the system/resource was in immediately before the operation — version numbers,
observed symptoms, configuration values, or "nominal, routine schedule" if there was no issue.]

---

## 3. Actions Taken

<!-- Numbered, in the order performed. Each action should be specific enough that another crew
     member could reproduce it from this record alone. -->

1. [Action taken]
2. [Action taken]

---

## 4. Verification

<!-- Prove the system was actually checked after the change, not just assumed healthy. Mirrors
     the workspace's "we verified, we didn't just assert" discipline (templates/review-records/
     final-review.md) — list what was actually run or inspected, not a restated intention. -->

| Check performed                                                                         | Result                       |
| --------------------------------------------------------------------------------------- | ---------------------------- |
| [Specific check, e.g. `torch.cuda.is_available()`, pytest suite, health-check endpoint] | [Pass/Fail + observed value] |

---

## 5. Outcome & Follow-Up

<!-- Distinguish a fully closed operation from one with a genuine open item — don't let the two
     read the same way. If nothing is open, say so explicitly rather than omitting the line. -->

**Outcome:** [What changed as a result, in plain terms.]

**Open follow-up items:** [None / list, each with an owner and, if known, a target date.]

---

## 6. Related Records

<!-- Link prior maintenance records for the same resource, the telescope research report or ADR
     that motivated this operation (if any), and any downstream document this record feeds. If
     the affected resource is a registered MCP server, also add/update its row in
     `.claude/rules/mcp-governance.md` to point here rather than narrating the change inline —
     that file's own history is what happens when infra changes accumulate as inline prose
     instead of dedicated records. -->

- [File/path — what it is]
