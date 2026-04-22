# Project-Level Dashboard

| Field            | Value                                                                                                                               |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Dashboard ID** | DASH-COMPANY-001                                                                                                                    |
| **Status**       | Authoritative                                                                                                                       |
| **Owners**       | CTO Dr. Kenji Nakamura + VP Platform David Okonkwo                                                                                  |
| **Sourced From** | Per-project `progress.md` instances (Layer 1) + per-project `checkpoints/*.json` files (Layer 3).                                   |
| **Refresh**      | Daily during active execution windows; weekly during steady-state. Auto-refresh sections marked. Last hand-refresh: **2026-04-21**. |
| **Effective**    | 2026-04-21 — open for cross-project read; no project may bypass this dashboard once it enters Stage 1+ (PRD authored).              |

---

## 1. Purpose

This dashboard answers three CEO-grade questions in one place:

| Question                                             | Answered By |
| :--------------------------------------------------- | :---------- |
| Which PRDs are in flight, and what stage is each at? | §3          |
| What is the company's burn-down on P0/P1 defects?    | §4          |
| What is the cycle time for shipping work today?      | §5          |

It is **not** a substitute for per-project `progress.md` (Layer 1 of the AGENTS.md monitoring system) — the authoritative pipeline-state file for an individual PRD.

This dashboard **aggregates** that upstream source. If the dashboard disagrees with an upstream source, the upstream source wins; the dashboard is fixed within 24 hours.

---

## 2. Hierarchy of Truth

| Question                                       | Source of truth                                                                                     |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| Pipeline stage of any individual project's PRD | That project's `progress.md` Layer 1 file → this dashboard §3 (refresh on stage transition)         |
| P0/P1 defect inventory                         | Per-project `progress.md` Layer 1 defect counts → this dashboard §4                                 |
| Cycle time for an individual project           | That project's `checkpoints/*.json` Layer 3 files (Stage entry/exit timestamps) → this dashboard §5 |

---

## 3. Active Product Projects (PRDs in Flight)

> **Scope:** projects that have entered **Stage 1 (Requirements → PRD + SRD)** or beyond on either the company 10-stage pipeline or the studio 10-stage pipeline. Stage 0 (Discovery / Problem Validation) projects appear here once the first PRD draft exists; pure pre-PRD ideation does not.

| Project ID | Project Name | Pipeline | Stage | Stage Entry Date | Days In Stage | Owner | P0/P1 Open | Risk |
| :--------- | :----------- | :------- | :---- | :--------------- | :------------ | :---- | :--------- | :--- |
| _(none)_   | —            | —        | —     | —                | —             | —     | —          | —    |

**Baseline note.** No product projects are in flight today. The first product project entering Stage 1 will populate this table; until then, this section reads honestly as empty.

**When this section becomes non-empty:**

1. New row appended on first PRD draft commit.
2. `Stage` cell updated when a stage gate is signed off (per the relevant pipeline file's Definition of Done).
3. `Days In Stage` is `(today - Stage Entry Date)` and is the column the CEO uses to spot bottlenecks.
4. `P0/P1 Open` rolls up from that project's `progress.md` Layer 1 defect counts.
5. `Risk` is a one-emoji indicator: 🟢 on track; 🟡 watch; 🟠 elevated; 🔴 escalation required.

---

## 4. P0/P1 Defect Burn-Down (Cross-Project)

> Operational P0/P1 defects from active product projects (per `progress.md` Layer 1) roll up here.

| Project ID | P0 Open | P1 Open | Oldest Open Defect | DRI | Notes                                                  |
| :--------- | :------ | :------ | :----------------- | :-- | :----------------------------------------------------- |
| _(none)_   | 0       | 0       | —                  | —   | No active projects. Empty by design until §3 has rows. |

**Burn-down rule (when the table has rows):** P0 defects open more than **5 business days** trigger automatic CTO + relevant VP escalation. P1 defects open more than **10 business days** trigger CTO notification. Neither rule is overridable; both inherit from AGENTS.md "Non-Negotiable Rules."

---

## 5. Cycle-Time Tracker

> Per-project pipeline cycle time once §3 has rows.

| Project ID | Stage 1 Entry | Stage 5 Entry | Stage 10 Entry | Total Cycle (days) | Per-Stage Median | Notes                              |
| :--------- | :------------ | :------------ | :------------- | :----------------- | :--------------- | :--------------------------------- |
| _(none)_   | —             | —             | —              | —                  | —                | Empty by design until §3 has rows. |

**Calibration:** once a project completes its first full cycle, the per-stage median seeds a baseline against which subsequent projects are compared. A per-stage median > 1.5× the baseline triggers a CTO review of stage execution.

---

## 6. Refresh Cadence + Ownership

| Section | Refresh Trigger                       | Refresh DRI                     | Auto / Manual                                                  |
| :------ | :------------------------------------ | :------------------------------ | :------------------------------------------------------------- |
| §3      | New PRD draft / stage transition      | Project DRI (mirror within 24h) | Manual today; auto on Layer-1 `progress.md` integration        |
| §4      | New P0/P1 defect filed in any project | Project DRI (mirror within 24h) | Manual today; auto on Layer-1 integration                      |
| §5      | Stage transition                      | VP Platform (mirror within 24h) | Manual today; auto on Layer-3 `checkpoints/*.json` integration |

**Daily refresh:** during active execution windows the dashboard is hand-refreshed once per business day. The hand-refresh stamp at the top of this file (`Last hand-refresh`) carries the refresh marker.

**Weekly refresh:** during steady-state windows (no active product projects) the dashboard is refreshed every Monday morning.

---

## 7. Open Items / Next Iteration

| ID    | Item                                                                                                                                                                                             | Discharge Target    | DRI                    |
| :---- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ | :--------------------- |
| OI-01 | Auto-refresh integration: write a small script (`render-dashboard.py` or Markdown include) that pulls §3 + §4 directly from per-project `progress.md` files to eliminate the 24-hour mirror lag. | When N ≥ 3 projects | VP Platform + DevOps   |
| OI-02 | Per-project Layer-1 (`progress.md`) schema lock: agree on the exact field names (Stage, Stage Entry, P0 Open, P1 Open, Risk) so §3 and §4 can roll up programmatically rather than by hand.      | When N = 1 project  | CTO + VP Platform      |
| OI-03 | First-product onboarding: when the first PRD enters Stage 1, run a dry-run of §3 + §4 + §5 row population to validate the schema and the refresh cadence.                                        | Triggered by event  | CTO + Project DRI      |
| OI-04 | Cost / ROI columns: add `estimated cost`, `actual cost`, and `cost-to-date` columns to §3 once at least one product project is in flight (premature factoring with N=0 is the worse failure).    | When N = 1 project  | CTO + (future) Finance |

---

## 8. Document Version History

| Version | Date           | Author                             | Changes                                                                                                                                                                                                                                                                                                                             |
| :------ | :------------- | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | CTO Nakamura + VP Platform Okonkwo | Initial authoritative dashboard. §3 is empty by design (no product PRDs in flight); §4 + §5 are empty placeholders that activate on first PRD entering Stage 1. Four Open Items (OI-01…OI-04) routed. DRI: CTO Nakamura + VP Platform Okonkwo. Auto-refresh integration deferred until N ≥ 3 projects to avoid premature factoring. |

---

_End of Project-Level Dashboard DASH-COMPANY-001._
