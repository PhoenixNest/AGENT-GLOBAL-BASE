# academic-neural-unit-00/knowledge-base/ — ANU-00 Knowledge Base

The durable research output of Academic Neural Unit 00. Every chartered research programme has an
entry here, opened at charter time and completed as findings arrive.

This folder is referenced as the canonical filing destination by all eight ANU-00 research-design
and ingestion skill files; it is established here as an empty structure ahead of first use, the
same way `academic-neural-unit-00/CLAUDE.md` § Knowledge Base Convention establishes the naming
convention ahead of first use.

---

## Structure

```
knowledge-base/
├── README.md                          ← this file
├── open-question-log.md               ← standing register, append-only (one instance)
├── taxonomy-change-record.md          ← taxonomy + its change log, append-only (one instance)
└── YYYY-MM-DD-<slug>/                 ← one folder per chartered programme
    ├── charter.md                     ← opened at charter time
    ├── research-report.md             ← opened at charter time, completed as findings arrive
    ├── observations/                  ← reproducible incident records raised during the work (if any)
    │   └── <short-slug>.md
    └── referrals/                     ← referral notes raised by this programme (if any)
        └── <short-slug>.md
```

The dated `YYYY-MM-DD-<slug>/research-report.md` pattern matches the research-archive convention
already used by `company/telescope/`, `studio/casual-games/telescope/`, and
`core-component-00/telescope/` — adopted for navigational consistency across the workspace, **not**
as a link to any of those archives or the systems that own them.

---

## Filing a New Entry

1. Charter the programme first — `research-programme-chartering.md`. A programme is not filed here
   before Dr. Mokoena ratifies it.
2. Create `YYYY-MM-DD-<slug>/` and copy in both templates from
   `academic-neural-unit-00/templates/`:
   - `templates/programme-records/research-programme-charter.md` → `charter.md`
   - `templates/knowledge-base/research-report.md` → `research-report.md`
3. Fill in the charter fully; open the report with §0–§2 filled and the findings sections empty.
   **An opened report with empty findings is the correct state for a programme in progress** — it
   is what makes the programme discoverable from the moment it starts.
4. Check the taxonomy category before ingesting. If the entry does not fit cleanly, resolve the gap
   with the Knowledge Systems Engineer first — never force-fit
   (`knowledge-base-ingestion-architecture.md` §1).
5. Record cross-references bidirectionally at ingestion time, not as a later cleanup pass (§3 of
   that skill).
6. **While the research runs**, file each reproducible incident — an unexpected run, a failure, an
   example worth keeping — into `observations/` from
   `templates/programme-records/observation-record.md`, at the time it happens rather than at
   write-up. Exact conditions are recoverable while the setup is live and largely are not
   afterwards. Every observation ends in a disposition: it feeds a claim in the report's §4
   register, supports a negative finding in §6.2, is parked in `open-question-log.md`, or is
   discarded as environmental. A discarded observation is kept, not deleted — knowing what was
   ruled out is reusable.

---

## Conventions

| Document                    | Pattern       | Meaning                                                                                                             |
| --------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------- |
| `charter.md`                | Point-in-time | Re-chartered as a new file if it changes materially; never edited in place                                          |
| `observations/<slug>.md`    | Point-in-time | A later, different observation is a new file; editing a filed one destroys the reproducibility it exists to provide |
| `research-report.md`        | Point-in-time | A materially different finding is a new dated entry with a cross-reference                                          |
| `open-question-log.md`      | Append-only   | One instance for the entity; rows are never deleted or renumbered                                                   |
| `taxonomy-change-record.md` | Append-only   | One instance; §1 shows current state, §2 records every change                                                       |

Do not mix the two patterns. This is the same distinction root `templates/README.md` § Usage draws
between snapshot records and running decision logs.

---

## Boundary Note

Entries here are pre-implementation research findings. A finding that implies production tooling is
recorded as a referral note (`templates/programme-records/referral-note.md`) and scoped out — it
does not become ANU-00 work, and filing it creates no obligation on ANU-00 or on anyone else. See
`academic-neural-unit-00/CLAUDE.md` § The Stage-of-Inquiry Test.
