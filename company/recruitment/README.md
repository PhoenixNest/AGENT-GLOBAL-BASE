# Recruitment

Canonical home for all company-wide recruitment governance — active plans, completed hiring history, and reusable templates. The **how** a single candidate moves through vetting is defined in [`company/pipeline/recruitment/pipeline.md`](company/pipeline/recruitment/pipeline.md); this folder is the **what** — what was planned, what was hired, and the starting point for the next cycle.

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

| Convention           | Rule                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Filename pattern** | Each hiring cycle gets its own sub-folder: `<department>-<fy>-<quarter>/` containing the master plan and companion artifacts.                                                                                                                                                                                                                                                                                                 |
| **Status lifecycle** | `Draft → Approved → In Progress → Complete`                                                                                                                                                                                                                                                                                                                                                                                   |
| **Edit policy**      | Approved plans are read-only for headcount and compensation content. Checkpoint and sequence files are updated throughout execution.                                                                                                                                                                                                                                                                                          |
| **Retention policy** | Completed cycles are removed once all hires are onboarded and their agent profiles are published. The agent profiles are the living record; the recruitment folder is a transient workspace.                                                                                                                                                                                                                                  |
| **Deferral review**  | Any staffing or composition assessment (e.g. a department head's own post-hire capacity review) that recommends **deferring action on a named risk** — not hiring for it, not fixing it, "revisit next cycle" — must route to the CEO or CHRO for confirmation before the deferral is treated as final. The assessor's own "not urgent" judgment is not the last word when the assessor also bears the cost of acting sooner. |

---

## 3. Active Hiring Cycles

| Plan ID                             | Department                                                                                                          | FY / Quarter | Headcount        | Status                                                                                                                                                                                                                                                                         | Folder                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `core-component-00-fy2026-q3`       | Core Component 00                                                                                                   | FY2026 Q3    | 11 (11/11 hired) | Complete — organized by document type (`candidates/`, `phase-summaries/`), includes `reflection.md`; eligible for cleanup per retention policy, pending CEO review                                                                                                             | [`core-component-00-fy2026-q3/`](./core-component-00-fy2026-q3/)             |
| `academic-neural-unit-00-fy2026-q3` | Academic Neural Unit 00 (independent entity, not a Company department — cycle filed here per standard CHRO channel) | FY2026 Q3    | 10 (10/10 hired) | Complete — 2 phases (Phase 1: full-scale cohort per CEO override of a phased recommendation; Phase 2: Elite Expansion Cohort under Mokoena's CEO-delegated execution authority); see `hiring-outcome-report.md`; eligible for cleanup per retention policy, pending CEO review | [`academic-neural-unit-00-fy2026-q3/`](./academic-neural-unit-00-fy2026-q3/) |

> Add rows here when a new hiring cycle opens. Remove the row when the cycle is complete and the folder is deleted.

---

## 4. How to File a New Hiring Cycle

**Templates:** [`template/recruitment-plan.md`](./template/recruitment-plan.md) · [`template/candidate-evaluation.md`](./template/candidate-evaluation.md) · [`template/phase-summary.md`](./template/phase-summary.md)

| Step | Action                                                                                                                                                                                                                                 |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Confirm the business need with the relevant VP and CHRO. Define the role scope, level (L1–L5 per the leveling rubric at [`company/pipeline/recruitment/pipeline.md`](company/pipeline/recruitment/pipeline.md)), and target headcount. |
| 2    | Copy [`template/recruitment-plan.md`](./template/recruitment-plan.md) and fill in all sections. Name the file `<department>-<fy>-<quarter>.md` (flat) or create a sub-folder of the same name for multi-artifact cycles.               |
| 3    | Add a row to §3 Active Hiring Cycles above. Set status to `Draft` or `Approved`.                                                                                                                                                       |
| 4    | As candidates enter the pipeline, create one [`template/candidate-evaluation.md`](./template/candidate-evaluation.md) copy per candidate. File inside the cycle's sub-folder.                                                          |
| 5    | At the close of each phase, file a [`template/phase-summary.md`](./template/phase-summary.md) capturing who was hired, vetting scores, conditions resolved, and lessons learned.                                                       |
| 6    | When the full cycle is complete and all agent profiles are published, remove the cycle folder and its §3 row.                                                                                                                          |

---

## 5. Relationship to the Recruitment Pipeline

The 9-stage vetting pipeline is defined in [`company/pipeline/recruitment/pipeline.md`](company/pipeline/recruitment/pipeline.md). That document governs **how a single candidate is evaluated** — stages, scoring, vetting authorities, and tier floors. Templates in this folder reference pipeline stages by number; if the pipeline changes, the templates remain valid.

---

## 6. Cross-References

| Topic                    | Location                                                                                                                                                         |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 9-stage vetting pipeline | [`company/pipeline/recruitment/pipeline.md`](company/pipeline/recruitment/pipeline.md)                                                                           |
| Leveling rubric          | [`company/pipeline/recruitment/pipeline.md`](company/pipeline/recruitment/pipeline.md)                                                                           |
| Department roster        | [`company/library/overview/personnel.md`](company/library/overview/personnel.md)                                                                                 |
| CHRO profile             | [`company/departments/human-resources/supervisor/chief-human-resources-officer/`](company/departments/human-resources/supervisor/chief-human-resources-officer/) |

---

## 7. Document Version History

| Version | Date           | Author | Changes                                                                                                                             |
| ------- | -------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 30, 2026 | —      | Initial structure established. Templates created. Retention policy: completed cycles are removed once agent profiles are published. |
