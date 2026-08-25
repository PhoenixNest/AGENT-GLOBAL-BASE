# curriculum/reviews/ — Dated Review-Round Convention

The curriculum will go through multiple rounds of internal and external review over its life —
not just the first production run. Filing every round's reports flat into `reviews/internal/` and
`reviews/external/` would mix rounds together with no way to tell which report belongs to which
review cycle, or which one is current. This folder is organized instead by **dated round**, the
same `YYYY-MM-DD-<slug>/` pattern `academic-neural-unit-00/knowledge-base/` uses.

---

## Rule

Every review round — whether a full internal+external cycle or a narrower follow-up like a
remediation re-review — gets its own subfolder here:

```
reviews/
├── README.md                       ← this file
├── reader-feedback-log.md          ← continuous log, not a dated round — see below
├── YYYY-MM-DD-<round-slug>/        ← one round
│   ├── internal/                   ← if the round includes internal cluster review
│   ├── external/                   ← if the round includes external blind review
│   └── comprehensive-review.md     ← if the round includes a Lead synthesis
└── YYYY-MM-DD-<round-slug>/        ← the next round, independent of the first
    └── ...
```

**One exception to the dated-round rule:** `reader-feedback-log.md` sits directly in `reviews/`,
not inside a dated folder. Unlike a review round — a point-in-time, named-reviewer verdict — it is
a single append-only document that accumulates reader-reported issues and their resolutions
continuously across many sessions and dates. Giving it its own dated folder per entry would
fragment a document whose entire value is being one continuous, greppable history; it dates each
entry internally instead. It cross-references round folders where an entry overlaps with a
tracked finding, but is not itself a round.

- **Date** = the date the round's reports were filed (matching the date already on the reports
  themselves — do not invent a different one).
- **Slug** = a short, specific description of what the round was — `first-review-cycle`,
  `remediation-review`, `second-full-review`, `pre-publication-audit`, whatever actually describes
  it. Not a sequence number alone (`round-2` on its own tells a reader nothing); pair a number with
  a description if both are useful (`2026-11-03-second-full-review`).
- Not every round needs all three subfolders — a full cycle has `internal/`, `external/`, and
  `comprehensive-review.md`; a narrower follow-up (like a remediation re-review) may have only its
  own report files directly in the round folder, as `2026-08-19-remediation-review/` does.
- Cross-references between rounds use relative paths through the dated folders
  (`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md`), never a bare `reviews/...` path
  that assumes a flat structure.

## Existing Rounds

| Round                            | Date       | Contents                                                                                                           |
| -------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| `2026-08-18-first-review-cycle/` | 2026-08-18 | Pass 1 (5 internal cluster reviews), Pass 2 (2 external blind reviews), Pass 3 (Lead's comprehensive synthesis)    |
| `2026-08-19-remediation-review/` | 2026-08-19 | Pass 4: 4 independent re-reviews of the blocking-severity documents, plus the Lead's closing remediation synthesis |

## Why Not Just Number the Rounds ("Pass N")

`curriculum/README.md` §6 already uses "Pass 1/2/3/4" for the _stages within_ a review round
(internal → external → synthesis → remediation) — that numbering is fine on its own and is kept.
But naming a _folder_ after only that stage number (the original `pass-4/` name) reads as an
opaque version tag to anyone who has not memorized the stage numbering, and it does not scale once
there is a second full review cycle with its own Pass 1/2/3. Dating the folder and naming what the
round actually was keeps both readable on their own and avoids collision when the next round
begins.
