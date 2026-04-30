# Execution Tracker — [Plan ID]

<!-- Replace the title above with the Plan ID, e.g. "Execution Tracker — OPT-2026-05-15-001" -->

| Field              | Value                                                                                                                                                                |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tracker ID**     | TRK-YYYY-MM-DD-NNN                                                                                                                                                   |
| **Plan**           | [`OPT-YYYY-MM-DD-NNN`](./optimization-plan.md) v1.0 — OPEN — Pending CEO Review                                                                                      |
| **Plan Status**    | OPEN — Pending CEO Review                                                                                                                                            |
| **Tracker Owner**  | [Name + Title] (Plan-level DRI; per-step owners listed in §3)                                                                                                        |
| **Start Date**     | TBD (upon CEO approval)                                                                                                                                              |
| **Day 30**         | TBD                                                                                                                                                                  |
| **Day 60**         | TBD                                                                                                                                                                  |
| **Day 90**         | TBD (quarterly retrospective checkpoint — measures §11 Success Metrics against operational reality)                                                                  |
| **Update Cadence** | Daily Log §6 is append-only. Per-step status §3 mirrors Plan §9 within 24h. If §3 and Plan §9 disagree, **Plan §9 wins**; this tracker is fixed within 24h to match. |

---

## 1. Purpose

This tracker is the **operational counterpart** to the optimization plan. The plan defines _what_ and _who_; this tracker captures _when_ and _how it's progressing_, day by day.

**Hierarchy of truth:**

| Question                                                                    | Source of truth                                          |
| --------------------------------------------------------------------------- | -------------------------------------------------------- |
| What are the approved findings, owners, due dates, and acceptance criteria? | Plan §§4–6, §9                                           |
| What is the current lifecycle state of any step?                            | Plan §9 (canonical) — this tracker §3 mirrors within 24h |
| What changed today; who is blocked; what is at risk?                        | This tracker §6 (Daily Log) — append only                |
| What are the current dependency-driven sequencing decisions?                | This tracker §4                                          |
| Why was the plan modified (v1.0 → v1.1 → …)?                                | Plan §13 (Document Version History)                      |

If §3 and Plan §9 disagree, **Plan §9 wins**; this tracker is fixed within 24h to match.

---

## 2. Sequencing Model

<!-- Explain the intra-bucket dependency decisions not encoded in the plan's step list.
     The plan groups steps into 30/60/90-day buckets; the tracker resolves ordering within each bucket. -->

| Decision                                      | Rationale                                         |
| --------------------------------------------- | ------------------------------------------------- |
| [Step X starts first in the Days 0–30 bucket] | [Why — dependency, risk, resource availability]   |
| [Step Y runs in parallel with Step X]         | [Why — disjoint file sets, different DRI, etc.]   |
| [Step Z waits for Step X to complete]         | [Why — content dependency, shared resource, etc.] |

**Step dependency graph:**

```text
Day 1 ───────────────────────────────────► Day 30 ──────────────────► Day 60 ──────────────────► Day 90

Step 1 ──────► unlocks → Steps 2, 3
   │
Step 4 ──────► (parallel, no downstream deps)
   │
Step 2 ──────► (waits for Step 1)
   │
Step 3 ──────► (waits for Step 1)
   │
Step 5 ──┬──► (Day 30–60, depends on Step 2)
         │
Step 6 ──┘
   │
Step 7 ──────► (Day 60–90, depends on Steps 5–6)
```

---

## 3. Per-Step Status Mirror

Status emoji vocabulary: `⬜ Pending → 🟡 In Progress → 🔵 Implemented → 🟢 Verified → ✅ Closed`

### 3.1 Days 0–30 (Plan §9.1)

| Step | Status | Started | Last Updated | Plan Action (abbrev.) | DRI    | Dependency | Closure Notes |
| ---- | ------ | ------- | ------------ | --------------------- | ------ | ---------- | ------------- |
| 1    | ⬜     | —       | —            | [Action summary]      | [Role] | None       | —             |

### 3.2 Days 30–60 (Plan §9.2)

| Step | Status | Started | Last Updated | Plan Action (abbrev.) | DRI    | Dependency | Closure Notes |
| ---- | ------ | ------- | ------------ | --------------------- | ------ | ---------- | ------------- |
| 2    | ⬜     | —       | —            | [Action summary]      | [Role] | Step 1     | —             |

### 3.3 Days 60–90 (Plan §9.3)

| Step | Status | Started | Last Updated | Plan Action (abbrev.) | DRI    | Dependency | Closure Notes |
| ---- | ------ | ------- | ------------ | --------------------- | ------ | ---------- | ------------- |
| 3    | ⬜     | —       | —            | [Action summary]      | [Role] | Step 2     | —             |

---

## 4. Active Risks

<!-- Execution-layer risks observed during planning or surfaced during daily operation.
     Strategic risks belong in Plan §10; this section captures day-to-day execution risks only. -->

| Risk ID  | Risk               | Likelihood          | Impact              | Mitigation          | Status |
| -------- | ------------------ | ------------------- | ------------------- | ------------------- | ------ |
| TRK-R-01 | [Risk description] | High / Medium / Low | High / Medium / Low | [Mitigation action] | Open   |

---

## 5. Daily Status Snapshot

### Counts

| Status         | Count | Steps |
| -------------- | ----- | ----- |
| ⬜ Pending     | —     | All   |
| 🟡 In Progress | 0     | —     |
| 🔵 Implemented | 0     | —     |
| 🟢 Verified    | 0     | —     |
| ✅ Closed      | 0     | —     |

### Burn-Down vs. Days 0–30 / 30–60 / 60–90 Buckets

<!-- Update this table after each step closes or at each daily log entry. -->

| Metric                           | Target (Day 90) | Current | Delta |
| -------------------------------- | --------------- | ------- | ----- |
| Steps (Days 0–30) closed (`✅`)  | N by Day 30     | 0       | ⬜    |
| Steps (Days 30–60) closed (`✅`) | N by Day 60     | 0       | ⬜    |
| Steps (Days 60–90) closed (`✅`) | N by Day 90     | 0       | ⬜    |
| All steps at `✅ Closed`         | Day 90          | 0       | ⬜    |
| P0 findings closed               | N by Day 30     | 0       | ⬜    |
| P1 findings closed               | N by Day 60     | 0       | ⬜    |
| P2 findings closed               | N by Day 90     | 0       | ⬜    |

---

## 6. Daily Log (Append-Only)

<!-- Format: ### YYYY-MM-DD — <Author> followed by bulleted updates.
     Append only — never edit prior entries. -->

### YYYY-MM-DD — Tracker Authored

- **Tracker created.** [Plan ID] plan reviewed; execution tracker authored.
- **All steps at `⬜ Pending`.** Plan status is OPEN — Pending CEO Review. No execution begins until CEO approval.
- **Sequencing model (§2) defined.** Dependency graph resolves intra-bucket ordering not specified in the plan.
- **[N] tracker-layer risks identified.** [Brief summary of top risks.]
- **No blockers.** Awaiting CEO approval to begin Day 1.
- **Next checkpoint:** Upon CEO approval — Day 1 kickoff.

---

## 7. Document Version History

| Version | Date         | Author   | Changes         |
| ------- | ------------ | -------- | --------------- |
| 1.0     | [YYYY-MM-DD] | [Author] | Initial tracker |
