# Threshold Sensitivity Check — Synthetic, Not Empirical Recalibration

**Parent Report:** `../research-report.md`
**Relates to:** P2 (threshold recalibration), Open Question 1
**Date:** 2026-07-12

---

## What this is, and what it is not

This is **not** the threshold recalibration the research report's P2 item and Open Question 1
call for. That recalibration requires real production session data (write frequency, actual
session lengths, actual importance distribution), and none exists yet: the `qdrant-memory`
instance shows `points_count = 0` across all three collections, and no JSONL memory logs exist on
disk — nothing has gone through `PersistentMemorySink` in production. Open Question 1 remains open.

What follows is a synthetic sanity check: running the actual `memory_maintenance.py` formulas
(`compute_decay_weight`, `next_status`, `cumulative_salience`) against hand-picked inputs, to
check the current defaults produce sane behavior in principle, before any real data exists to
validate them against. Treat every number below as illustrative, not as a validated threshold.

## Current defaults

| Constant                  | Value |
| ------------------------- | ----- |
| `BASE_STRENGTH_DAYS`      | 7.0   |
| `REINFORCEMENT_FACTOR`    | 0.5   |
| `DORMANT_THRESHOLD`       | 0.5   |
| `ARCHIVE_THRESHOLD`       | 0.15  |
| `ARCHIVE_GRACE_DAYS`      | 30.0  |
| `CONSOLIDATION_THRESHOLD` | 150.0 |

## Finding 1: Time-to-dormant scales as expected with access count

For an `importance=1.0` record, days until `decay_weight` crosses the dormant threshold (0.5):

| access_count | strength (days) | days to dormant | days to decay&lt;0.15 |
| ------------ | --------------- | --------------- | --------------------- |
| 0            | 7.0             | 4.85            | 13.28                 |
| 1            | 10.5            | 7.28            | 19.92                 |
| 3            | 17.5            | 12.13           | 33.20                 |
| 5            | 24.5            | 16.98           | 46.48                 |
| 10           | 42.0            | 29.11           | 79.68                 |
| 20           | 77.0            | 53.37           | 146.08                |

Behaves as designed — reinforcement extends survival — but note archival is always additionally
gated by the 30-day grace period regardless of how fast `decay_weight` itself drops, so a
never-reaccessed record sits `dormant` from ~day 5 until day 30 before it's even eligible for
archival. That's a ~25-day dormant window with no further decay-driven change, which may or may
not be the intended shape — worth checking against real access patterns once they exist.

## Finding 2 (the one worth flagging): records with `importance < 0.5` are born dormant

`decay_weight` at creation (t=0, `access_count=0`) equals `importance` itself (since
`e^0 = 1`). `DORMANT_THRESHOLD=0.5` means:

| importance | decay_weight at t=0 | status at t=0 |
| ---------- | ------------------- | ------------- |
| 1.00       | 1.000               | active        |
| 0.80       | 0.800               | active        |
| 0.60       | 0.600               | active        |
| 0.50       | 0.500               | active        |
| 0.40       | 0.400               | **dormant**   |
| 0.30       | 0.300               | **dormant**   |
| 0.15       | 0.150               | **dormant**   |
| 0.10       | 0.100               | **dormant**   |

Any record written with `importance < 0.5` is `dormant` from the moment it's created, before any
time has passed. `02-deployment-guidelines.md` §3 says `importance` is assigned by a "write-time
heuristic" — if that heuristic commonly scores below 0.5 (plausible for routine/low-salience
episodic events), a large fraction of memory could enter the corpus already dormant. This isn't
necessarily wrong — a low-importance memory arguably _should_ be deprioritized immediately — but
it means `DORMANT_THRESHOLD` and the importance-scoring heuristic are coupled in a way the report
doesn't discuss, and the write-time heuristic's actual output distribution should be checked
against this coupling once it exists, not assumed benign.

## Finding 3: consolidation threshold implies 30–250 episodic records per session to trigger

`CONSOLIDATION_THRESHOLD=150` (cumulative `importance × access_count`). Records needed to cross
it at various assumed per-record salience:

| importance | access_count | salience/record | records needed |
| ---------- | ------------ | --------------- | -------------- |
| 0.6        | 1            | 0.6             | 250            |
| 0.6        | 3            | 1.8             | 84             |
| 0.6        | 5            | 3.0             | 50             |
| 0.8        | 3            | 2.4             | 63             |
| 1.0        | 3            | 3.0             | 50             |
| 0.5        | 10           | 5.0             | 30             |

Generative Agents' original 150-point threshold (the source of this default, per the research
report) was tuned against that system's own simulated-agent-day event volume, which has no
established correspondence to this workspace's actual per-session episodic record count. Whether
50–250 records per session is a realistic bar for this workspace's actual usage is exactly what
Open Question 1 asks and what real data is needed to answer.

## What this does and doesn't resolve

- Does not close Open Question 1 — still requires production telemetry.
- Does not change any constant in `memory_maintenance.py` — no values were touched.
- Surfaces one coupling (`DORMANT_THRESHOLD` × importance-heuristic output) worth checking once
  the write-time importance heuristic exists and its output distribution is known.
- All numbers above are reproducible directly from `compute_decay_weight`/`next_status`/
  `cumulative_salience` — no new code was added, this is a read-only exercise of existing functions.

## Status

P2 remains blocked on real session data, per the original report. This document does not change
that — it's a bounds-check performed while waiting, not a substitute for the recalibration itself.
