# CC-00 Maintenance Records — Laboratory Maintenance Log

**Classification:** Operational Maintenance Log
**Owner:** Core Component 00 Laboratory
**Director:** Dr. Elias Vance
**Operational Owner:** Ravi Deshmukh, Infrastructure Engineer
**Purpose:** Record of maintenance operations performed on CC-00 lab servers and engineering
resources

---

## Overview

This folder holds the history of maintenance work performed on CC-00 lab infrastructure — the
local dev environment, GPU/CUDA stack, shared dependency footprint, MCP server processes
(`workspace-knowledge`, `agent-memory`, `embedder-service`), and other lab-owned resources.
Created at CEO direction as a dedicated home for this operational history, separate from
`core-component-00/telescope/` (research investigations) and `company/recruitment/` (personnel).

---

## Directory Structure

```
core-component-00/platform/maintenance-records/
├── README.md                    ← This file
├── CLAUDE.md                    ← Claude Code operating layer for this folder
├── pipeline.md                  ← Canonical stage definitions
├── template/
│   ├── maintenance-record.md    ← Copy for every new topic's main record
│   └── log-entry.md             ← Copy for every stage/development within a topic
└── <YYYY-MM-DD-slug>/           ← One folder per maintenance topic
    ├── maintenance-record.md    ← Short, always-current summary
    └── log/                     ← Full account of each development, one file per entry
```

Each maintenance topic is a dated **folder**, matching `core-component-00/telescope/`'s shape —
see `CLAUDE.md` for the full authoring rule and `pipeline.md` for the stage definitions that
govern how a topic moves through it.

---

## Format Note (2026-08-13, two same-day revisions)

**Revision 1 — "new file per operation" → "one file per topic, dated sections":** the original
rule was meant to stop a record's history from being silently rewritten in place, but in practice
produced exactly what the CEO flagged the same day it was first used for real: three
near-duplicate files (discovery, execution, an incident found during execution) for what was
genuinely one continuous piece of work. The actual failure mode being guarded against — someone
editing history rather than appending to it — doesn't require a new _file_ to prevent, only a rule
against deleting or rewriting a prior _section_. Revised to one file per topic with dated `##`
sections, following the pattern `core-component-00/telescope/` already used for research
investigations.

**Revision 2 — "one growing file" → "one folder per topic, with a `log/` subfolder":** the CEO's
follow-up feedback was that a single file accumulating every section could itself become
unreadably large over a long-running topic, and that the original three-file split wasn't
inherently unacceptable — the goal is accessibility matching how leading labs actually document
maintenance work, not minimizing file count for its own sake. Dr. Vance consulted the full CC-00
crew and converged on: a short, always-current **summary** file (Zhao's "working-memory" framing)
plus a **`log/` subfolder** of individually-created, numbered entries holding the full
**episodic** detail — matching `telescope/`'s `research-report.md` + `supporting/` Programme
shape exactly, governed by a new `pipeline.md` covering stage gates, severity tagging, an
explicit topic-boundary test, and a staleness bound. `.claude/rules/mcp-governance.md`'s own
history remains the cautionary tale for the opposite failure — a single table cell regrowing into
an unreadable inline changelog — so the target is still the same middle ground `telescope/`
already found, just with the folder-plus-log mechanics needed to hold it at scale.

**Revision 3 — header fields, bold-label prose → a table (2026-09-01):** the CEO flagged that the
`2026-08-13-mcp-server-powershell-cross-platform` topic's header (Owner, Authorized/reviewed by,
System/resource affected, Severity, Status) had regrown into the exact anti-pattern this file
already names as the cautionary tale — `.claude/rules/mcp-governance.md`'s own history of a single
cell becoming an unreadable inline changelog. The immediate fix was trimming each field back to
current-state facts only (pointing to the Pipeline Stage Log / Open Follow-Up Items tables for
history instead of restating it); the CEO's follow-up direction was that the header itself should
render as a table, not bold-label paragraphs, matching how leading labs and this same document's
own Pipeline Stage Log / Open Follow-Up Items sections already present tabular data — a plainer
reading experience for maintainers scanning current state. `template/maintenance-record.md` and
this topic's own record were both converted; the field set and their meaning are unchanged, only
the rendering. Extended the same day to `template/log-entry.md`'s single-value fields (Part of / Pipeline stage, Trigger, State before, Outcome, Handoff to next stage) — `Actions taken` (a numbered list) and `Verification` (already a table) were left as-is, since they aren't single-value fields. This session's own new entries (`log/18`, `log/19` in the 2026-08-13 topic) were converted to match; prior entries in that topic (`log/01`–`log/17`) were deliberately **not** retrofitted — a `log/` entry is never edited or rewritten after the fact once it records history (see `CLAUDE.md` § Creating or Updating a Maintenance Record), and a template/format revision is not an exception to that rule.

---

## Creating or Updating a Maintenance Record

**New topic:** create folder `YYYY-MM-DD-<slug>/`, copy `template/maintenance-record.md` into it,
copy `template/log-entry.md` into `<slug>/log/01-<slug>.md` for the first development, add an
entry to the index below, run Prettier.

**Follow-up on an existing topic:** copy `template/log-entry.md` into `<slug>/log/NN-<slug>.md`
(next number, never edit a prior entry), update `<slug>/maintenance-record.md`'s header **Status**
and Pipeline Stage Log table, run Prettier.

Full authoring rules, including what counts as "the same topic" vs. a genuinely new one:
`CLAUDE.md` (this folder) and `pipeline.md` (stage gates, severity, topic-boundary test).

---

## Maintenance Log Index

Add a row here for each new topic (or update the row's Status when a topic gets a new `log/`
entry), newest-opened first.

| Date opened | Record                                                                                                                 | System / Resource                                                                                                                                                                                                                                                                                                      | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-13  | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md` | Root `.mcp.json`, `agent-memory/server.py`, `manage_embedder_service.py` (new, replacing the retired `.ps1`), `register_backup_task.py` (new 2026-08-14), both server READMEs, `.claude/hooks/mcp-config-platform-check.py` (new), `workspace-knowledge/server.py` + `workspace-knowledge/_vendor/proxytypes.py` (new) | **Completed 2026-08-26, two follow-up items open** — `.mcp.json`'s cross-platform launch-path bug re-closed via a durable `SessionStart` self-healing hook plus a Windows venv sync and a vendored `jsonref`/`proxytypes` compatibility shim; CEO's live `/mcp reconnect` confirmed both servers fully healthy, non-degraded. DR-scheduling still unverified on non-Windows. **2026-08-30:** Item #6 (Executed, pending verification) — CEO flagged that the self-healing hook's per-session `.mcp.json` rewrite could be accidentally committed; a generate-once template + gitignore redesign was proposed, CEO-approved, and implemented (`.mcp.json` now gitignored, `.mcp.json.example` is the committed template), self-tested against a simulated fresh clone; **Both closed 2026-08-30**, independently confirmed via the CEO's live `/mcp reconnect`. Item #7 (found during the same check): `workspace-knowledge` had briefly failed `CONNECTION_CLOSED` on an unrelated, pre-existing bug — `server.py` shadowing a working real `proxytypes` package with the `log/12` vendor shim — fixed by making the shim conditional and confirmed reconnected cleanly. **Reopened 2026-09-01 — Item #8 (open):** on a Linux machine whose `.venv` was never bootstrapped for either server, `/mcp` failed `ENOENT` for both; `mcp-config-platform-check.py` confirmed working correctly but out-of-scope by design for a fully-missing venv. CEO approved building a new, independent `SessionStart` hook to run `uv sync` in that case, rather than extending the existing hook. Design approved; Execution not yet started. Item #3 (Linux/macOS DR scheduling) also remains open — see the record for detail. **Item #8 (2026-09-01, Linux venv-bootstrap gap): CLOSED** — built and registered a new independent `SessionStart` hook (`mcp-venv-bootstrap.py`) that runs `uv sync` when `mcp-config-platform-check.py` reports a venv missing for both OSes; CEO's live `/mcp reconnect` confirmed both servers reconnected. **Item #9 (2026-09-01, degraded search paths): OPEN** — `health_check` calls made during that verification found `agent-memory`'s embedder-service unavailable and `workspace-knowledge` on BM25-only fallback (FAISS init failing on a missing `AGENTS.md` path); neither blocks connectivity, not yet investigated. **Item #9: root-caused 2026-09-01** — `agent-memory`'s embedder-service crashes because `_shared/models/` was never provisioned on this machine (same class of gap as Item #8); `workspace-knowledge`'s FAISS init crashes on one of 9 `AGENTS.md` symlinks committed with a corrupted trailing-newline target by the `c8efa649` reorg. Two remediations recommended, pending CEO Approval. **Item #9: CLOSED 2026-09-01** — CEO approved both remediations; both executed and live-verified: models provisioned (`agent-memory` search fully restored), and the real broken-symlink count corrected to 8 (not 9) and all 8 fixed (`workspace-knowledge`'s symlink-caused crash confirmed gone). **Item #10 (2026-09-01): CLOSED** — fixing the symlink exposed a distinct code defect: `workspace-knowledge/server.py`'s FAISS-index write path never created its output directory first. Fixed with a `mkdir(parents=True, exist_ok=True)` guard; the CEO's live `/mcp reconnect` plus a full `rebuild_index`/`health_check` round-trip confirmed the fix end-to-end (`hybrid_qdrant`, no degradation). **All items in this topic are now closed except Item #3** (P3, Linux/macOS DR scheduling, unrelated). **2026-09-01 WSL compatibility check (CEO-requested):** confirmed no gap — both hooks are OS-detection-agnostic (file-existence-based, not `sys.platform`-branched) and the repo runs on WSL2's native ext4, not Windows-mounted drvfs, so Item #9's symlink repair and Item #10's `mkdir` fix get full native POSIX semantics; no new item opened |

---

## Related Documentation

| Document                         | Purpose                                                        |
| -------------------------------- | -------------------------------------------------------------- |
| `pipeline.md`                    | Canonical stage definitions, gates, severity tagging           |
| `template/maintenance-record.md` | The main-record template — full field-by-field authoring guide |
| `template/log-entry.md`          | The per-stage log-entry template                               |
| `core-component-00/telescope/`   | Research investigation archive (not operational maintenance)   |
| `core-component-00/README.md`    | CC-00 Laboratory overview                                      |

---

## Contact

**Laboratory Director:** Dr. Elias Vance
**Infrastructure Engineer:** Ravi Deshmukh
**Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`,
`core-component-00/crew/infrastructure/ravi-deshmukh/agent/profile.md`
**Authority:** AGENTS.md § 6. Core Component 00
