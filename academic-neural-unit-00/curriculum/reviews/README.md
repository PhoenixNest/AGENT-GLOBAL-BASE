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
├── YYYY-MM-DD-<round-slug>/        ← one round (internal+external cycle shape)
│   ├── internal/                   ← if the round includes internal cluster review
│   ├── external/                   ← if the round includes external blind review
│   └── comprehensive-review.md     ← if the round includes a Lead synthesis
├── YYYY-MM-DD-<round-slug>/        ← a round whose own plan defines named phases instead
│   ├── phase-<n>-<phase-title>/    ← one subfolder per phase that produced an artifact
│   │   └── ...                     ← that phase's report(s), named for content, not phase again
│   └── phase-<n>-<phase-title>/
│       └── ...
└── YYYY-MM-DD-<round-slug>/        ← the next round, independent of the others
    └── ...
```

**Two subfolder shapes, not one.** `internal/`/`external/`/`comprehensive-review.md` is the shape
for a round following the Pass 1→2→3(→4) internal/external/synthesis cycle. `phase-<n>-<phase-
title>/` is the shape for a round whose own governing plan document defines a numbered phase
sequence (e.g. a remediation plan's §6 production workflow) — one subfolder per phase that actually
produced a filed artifact, named and numbered to match that plan's own phase list exactly, skipping
phases with no artifact (a decision-point phase, or a phase whose output is code/content changes
filed elsewhere, not a report in this folder). Because the subfolder names are numbered, a plain
directory listing sorts in production/reading order without needing an index file — pick whichever
shape matches how the round's own plan is structured; don't force one round's shape onto another.

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
- Not every round needs all three `internal/`/`external/`/`comprehensive-review.md` subfolders — a
  full cycle has all three; a narrower follow-up (like a remediation re-review) may have only its
  own report files directly in the round folder, as `2026-08-19-remediation-review/` does. A round
  using the `phase-<n>-<phase-title>/` shape only gets subfolders for phases that filed a report —
  see `2026-08-26-external-audience-remediation/` for a worked example (`phase-1-audit/`,
  `phase-4-review/`, `phase-5-verification/`; no `phase-2-`/`phase-3-` folders, since that round's
  plan's Phase 2 was a CEO decision point with no artifact and Phase 3's output is curriculum
  content edits, not a report filed here).
- Cross-references between rounds use absolute paths through the dated folders
  (`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md`), never a bare `reviews/...` path
  that assumes a flat structure.

## Existing Rounds

| Round                                       | Date       | Contents                                                                                                                                                                              |
| ------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `2026-08-18-first-review-cycle/`            | 2026-08-18 | Pass 1 (5 internal cluster reviews), Pass 2 (2 external blind reviews), Pass 3 (Lead's comprehensive synthesis)                                                                       |
| `2026-08-19-remediation-review/`            | 2026-08-19 | Pass 4: 4 independent re-reviews of the blocking-severity documents, plus the Lead's closing remediation synthesis                                                                    |
| `2026-08-26-external-audience-remediation/` | 2026-08-26 | `phase-<n>-<phase-title>/` shape, per the remediation plan's §6 workflow: `phase-1-audit/` (2 audit reports), `phase-4-review/` (2 reviews + Lead synthesis), `phase-5-verification/` |

## Why Not Just Number the Rounds ("Pass N")

`curriculum/README.md` §6 already uses "Pass 1/2/3/4" for the _stages within_ a review round
(internal → external → synthesis → remediation) — that numbering is fine on its own and is kept.
But naming a _round-identifying folder_ after only that stage number (the original `pass-4/` name)
reads as an opaque version tag to anyone who has not memorized the stage numbering, and it does not
scale once there is a second full review cycle with its own Pass 1/2/3. Dating the folder and
naming what the round actually was keeps both readable on their own and avoids collision when the
next round begins.

**This does not rule out numbered subfolders inside an already-dated round.** The
`phase-<n>-<phase-title>/` shape above pairs a number with a description (exactly what this
section asks for), and it sits underneath a folder that is already dated and named — it never
stands alone as a round's only identity, so it doesn't reintroduce the opaque-version-tag problem
this section originally raised.
