# company/optimization-history/ — Optimization Record Archive

Append-only archive of all company optimization plans and their execution records.

---

## Critical Rule: This Directory Is Append-Only

**Never edit or delete past entries.** Every optimization record is a permanent historical artifact.
Adding new entries is the only permitted operation. Modifying or removing an existing entry is a
governance violation.

---

## What Lives Here

```
optimization-history/
├── README.md                               ← Archive index
├── template/                               ← Templates for new optimization records
└── YYYY-MM-DD-<slug>/                      ← One folder per optimization event
    ├── optimization-plan.md                ← The plan (what, why, how)
    └── execution-tracker.md                ← Progress and outcomes
```

---

## Folder Naming Convention

```
YYYY-MM-DD-<slug>/
```

Where:

- `YYYY-MM-DD` is the date the optimization was initiated
- `<slug>` is a kebab-case descriptive label

Examples:

```
2026-06-15-pipeline-stage-consolidation/
2026-08-10-recruitment-cycle-review/
```

---

## Required Files per Record

| File                   | Purpose                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------ |
| `optimization-plan.md` | Documents what is being optimized, the rationale, the approach, and success criteria |
| `execution-tracker.md` | Tracks progress through the optimization, records outcomes, and notes deviations     |

Both files are required. A folder with only one file is incomplete.

---

## Creating a New Record

1. Create a new folder: `YYYY-MM-DD-<slug>/`
2. Copy templates from `template/` (if available)
3. Complete `optimization-plan.md` before starting execution
4. Update `execution-tracker.md` as the optimization progresses
5. Do **not** modify any existing folder — only add new ones

---

## Rules

- **Append-only.** Never modify or delete a past entry under any circumstances.
- Folder names must follow the `YYYY-MM-DD-<slug>/` convention exactly.
- Both `optimization-plan.md` and `execution-tracker.md` are required per record.
- This archive is a governance artifact — its integrity supports organizational learning and audit.
