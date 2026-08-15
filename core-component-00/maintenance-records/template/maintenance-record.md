# Maintenance Record — [System/Resource Name]

<!-- Copy this file into a NEW FOLDER core-component-00/maintenance-records/YYYY-MM-DD-<slug>/
     (not into template/ itself) when a maintenance TOPIC opens on a CC-00 lab server or
     engineering resource — the local dev environment, GPU/CUDA stack, shared dependency
     footprint, MCP server processes (workspace-knowledge, agent-memory, embedder-service), or any
     other lab-owned infrastructure. Name the folder `YYYY-MM-DD-<slug>/`, dated to when the topic
     first opened (e.g. `2026-08-13-embedder-service-idle-timeout-tune/`), and this file inside it
     is always named `maintenance-record.md`.

     Governed by core-component-00/maintenance-records/pipeline.md — read it before opening a
     topic. This file is the SHORT, always-current summary (Zhao's "working memory" — see
     core-component-00/maintenance-records/README.md § Format Note): header fields, a
     one-row-per-stage table linking to the full detail, and the current Open Follow-Up Items. It
     should stay small even as the topic grows, because the full account of each development
     lives in log/ instead (see core-component-00/maintenance-records/template/log-entry.md).

     One folder per TOPIC, not per operation. A topic covers everything that happens to that
     system/resource concern over time — investigation, execution, an incident found during
     execution, later follow-ups — as numbered entries in log/. The topic-boundary test for
     "is this the same topic" is in core-component-00/maintenance-records/pipeline.md — don't guess. -->

**Owner:** [Name, role — the crew member(s) responsible for this topic overall, e.g. Ravi Deshmukh
(Infrastructure Engineer)]
**Authorized / reviewed by:** [Name, role — who signed off at pipeline stage 2 (Approval). State
"Self-authorized — within [role]'s documented authority scope" if no separate approval was
needed. An operation that changes cross-module architecture is outside the Infrastructure
Engineer's unilateral authority per `crew/CLAUDE.md` § Authority Scope — name Dr. Vance or the
relevant module lead as approver instead of self-authorizing. If different stages had different
approvers, note that here.]
**System / resource affected:** [Named server, dev environment, dependency stack, MCP server
process, GPU/CUDA configuration, CI tooling, etc. — be specific enough that a reader can locate
the affected component without cross-referencing another document, AND specific enough to serve
as the anchor for core-component-00/maintenance-records/pipeline.md's topic-boundary test. For any change touching a Python
environment, name the specific venv/interpreter — a bare `python` resolving to the system
interpreter is a known defect class (`.claude/rules/mcp-governance.md`).]
**Severity:** [P0 (live service broken) / P1 (confirmed defect, not yet broken live) / P2
(non-blocking gap) / P3 (routine) — assigned at pipeline stage 1, per core-component-00/maintenance-records/pipeline.md's Severity
tagging table. Update if severity changes mid-topic (e.g. a P1 escalates to P0 during Execution).]
**Status:** [Current truth as of the most recent log/ entry — e.g. "Open", "Investigating",
"Plan ready", "In progress", "Completed", "Completed with follow-up open", "Reopened — see
log/NN-....md". Update this line every time a new log/ entry is added; per core-component-00/maintenance-records/pipeline.md's
staleness bound, this must never lag what the log/ entries actually say.]

---

## Pipeline Stage Log

Per `core-component-00/maintenance-records/pipeline.md`. One row per stage reached so far, oldest
first — the full `log/` entry's path plus a one- or two-sentence summary, not the full account
(that's in the linked entry).

| Stage             | Entry                                                                      | Summary                |
| ----------------- | -------------------------------------------------------------------------- | ---------------------- |
| 1 — Investigation | `core-component-00/maintenance-records/YYYY-MM-DD-<slug>/log/01-<slug>.md` | [one-sentence summary] |

<!-- Add a row per subsequent stage reached. If the topic reopens (a new problem found during
     Execution or Verification), add a row like "3→1 — Reopen" per pipeline.md's loop-back edge,
     referencing the incident's own log/ entry by its full path, and continue numbering log/
     entries forward (don't renumber or delete prior entries). -->

---

## Open Follow-Up Items

<!-- None / list, each with an owner and, if known, a target date. An item still open when a
     stage closes carries forward here until a later log/ entry closes it — reference that entry
     by filename when it does. -->

[None / table]

---

## Related Records

<!-- Link prior maintenance records for OTHER topics that relate to this one, the telescope
     research report or ADR that motivated this topic (if any), and any downstream document this
     record feeds. If the affected resource is a registered MCP server, also add/update its row
     in `.claude/rules/mcp-governance.md` to point here rather than narrating the change inline —
     that file's own history is what happens when infra changes accumulate as inline prose
     instead of dedicated records. -->

- [File/path — what it is]
