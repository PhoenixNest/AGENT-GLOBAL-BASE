# Recruitment

Canonical home for all company-wide recruitment governance — active plans, completed hiring history, and reusable templates. The **how** a single candidate moves through vetting is defined in [`company/pipeline/recruitment/pipeline.md`](../pipeline/recruitment/pipeline.md); this folder is the **what** — what was planned, what was hired, and the starting point for the next cycle.

---

## 1. Folder Structure

```text
company/recruitment/
├── README.md          ← this index
├── template/          ← reusable templates for every new hiring cycle
│   ├── recruitment-plan.md       ← strategic plan: roles, org, phases, compensation
│   ├── candidate-evaluation.md   ← per-candidate scorecard (one copy per candidate)
│   └── phase-summary.md          ← cohort close-out record (one copy per phase)
└── <department>-<fy>-<quarter>/  ← active hiring cycle (created when a new plan opens)
    ├── recruitment-plan.md
    ├── recruitment-sequence.md
    ├── recruitment-checkpoint.md
    └── phase-N-summary.md
```

---

## 2. Conventions

| Convention           | Rule                                                                                                                                                                                         |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Filename pattern** | Each hiring cycle gets its own sub-folder: `<department>-<fy>-<quarter>/` containing the master plan and companion artifacts.                                                                |
| **Status lifecycle** | `Draft → Approved → In Progress → Complete`                                                                                                                                                  |
| **Edit policy**      | Approved plans are read-only for headcount and compensation content. Checkpoint and sequence files are updated throughout execution.                                                         |
| **Retention policy** | Completed cycles are removed once all hires are onboarded and their agent profiles are published. The agent profiles are the living record; the recruitment folder is a transient workspace. |

---

## 3. Active Hiring Cycles

| Plan ID | Department | FY / Quarter | Headcount | Status | Folder |
| ------- | ---------- | ------------ | --------- | ------ | ------ |

> Add rows here when a new hiring cycle opens. Remove the row when the cycle is complete and the folder is deleted.

---

## 4. How to File a New Hiring Cycle

**Templates:** [`template/recruitment-plan.md`](./template/recruitment-plan.md) · [`template/candidate-evaluation.md`](./template/candidate-evaluation.md) · [`template/phase-summary.md`](./template/phase-summary.md)

| Step | Action                                                                                                                                                                                                                            |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Confirm the business need with the relevant VP and CHRO. Define the role scope, level (L1–L5 per the leveling rubric at [`company/pipeline/recruitment/pipeline.md`](../pipeline/recruitment/pipeline.md)), and target headcount. |
| 2    | Copy [`template/recruitment-plan.md`](./template/recruitment-plan.md) and fill in all sections. Name the file `<department>-<fy>-<quarter>.md` (flat) or create a sub-folder of the same name for multi-artifact cycles.          |
| 3    | Add a row to §3 Active Hiring Cycles above. Set status to `Draft` or `Approved`.                                                                                                                                                  |
| 4    | As candidates enter the pipeline, create one [`template/candidate-evaluation.md`](./template/candidate-evaluation.md) copy per candidate. File inside the cycle's sub-folder.                                                     |
| 5    | At the close of each phase, file a [`template/phase-summary.md`](./template/phase-summary.md) capturing who was hired, vetting scores, conditions resolved, and lessons learned.                                                  |
| 6    | When the full cycle is complete and all agent profiles are published, remove the cycle folder and its §3 row.                                                                                                                     |

---

## 5. Relationship to the Recruitment Pipeline

The 9-stage vetting pipeline is defined in [`company/pipeline/recruitment/pipeline.md`](../pipeline/recruitment/pipeline.md). That document governs **how a single candidate is evaluated** — stages, scoring, vetting authorities, and tier floors. Templates in this folder reference pipeline stages by number; if the pipeline changes, the templates remain valid.

---

## 6. Cross-References

| Topic                    | Location                                                                                                                                                    |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 9-stage vetting pipeline | [`company/pipeline/recruitment/pipeline.md`](../pipeline/recruitment/pipeline.md)                                                                           |
| Leveling rubric          | [`company/pipeline/recruitment/pipeline.md`](../pipeline/recruitment/pipeline.md)                                                                           |
| Department roster        | [`company/library/overview/personnel.md`](../library/overview/personnel.md)                                                                                 |
| CHRO profile             | [`company/departments/human-resources/supervisor/chief-human-resources-officer/`](../departments/human-resources/supervisor/chief-human-resources-officer/) |

---

## 7. Document Version History

| Version | Date           | Author | Changes                                                                                                                             |
| ------- | -------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 30, 2026 | —      | Initial structure established. Templates created. Retention policy: completed cycles are removed once agent profiles are published. |
