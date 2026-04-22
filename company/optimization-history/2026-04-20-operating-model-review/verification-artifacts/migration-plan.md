# Pipeline Migration Plan — Base + Deltas Refactor

> **Plan reference:** [`OPT-2026-04-20-001`](../../optimization-history/2026-04-20-operating-model-review/optimization-plan.md) Step 5 (FIND-P0-01 + FIND-P2-07).
> **Tracker reference:** [`../../optimization-history/2026-04-20-operating-model-review/execution-tracker.md`](../../optimization-history/2026-04-20-operating-model-review/execution-tracker.md) §3.1 Step 5.
> **Owner:** Software Architect Rafael Okonkwo (delegated from CTO Nakamura).
> **Window:** Days 1–30 of OPT-2026-04-20-001 (2026-04-21 → 2026-05-20).

---

## 1. Migration Phases

| Phase                | Day Range       | Scope                                                                                                                                                                                                                                                               | Risk Level           |
| -------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **P-0** Scaffold     | Day 1 (today)   | Author `_base/{README.md, pipeline.md, delta-template.md, migration-plan.md}` (this session — DONE)                                                                                                                                                                 | Low                  |
| **P-1** Base Content | Day 2 – Day 15  | Extract common content from the four existing pipelines into `_base/pipeline.md`. Resolve content disagreements (where the four files have drifted) by canonizing the most-elaborated version, then noting the divergence in `_base/migration-disagreement-log.md`. | Medium               |
| **P-2** Mobile Delta | Day 8 – Day 22  | Author `mobile-development/delta.md`. Mobile is the most-elaborated existing file (303 lines vs. ~290 for others), so it migrates first as the proof-of-pattern.                                                                                                    | Medium               |
| **P-3** Other Deltas | Day 15 – Day 29 | Author `web-development/delta.md`, `backend-api/delta.md`, `full-stack/delta.md` in parallel.                                                                                                                                                                       | Medium               |
| **P-4** Cross-Refs   | Day 22 – Day 30 | Update cross-references in `company/library/`, `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.lingma/`, `.qwen/`, `.gemini/`, `.github/`.                                                                                                                                  | High (broad surface) |
| **P-5** Verification | Within Day 30   | Independent Challenge round (per Plan FIND-P1-08) verifies refactor preserves all gate criteria from the four legacy files. Step 5 flips `🔵 → 🟢 → ✅`.                                                                                                            | Low                  |

**Day 30 deadline:** Per Plan §7.1 ("Stop the Bleeding"), Step 5 must close by Day 30. Phases P-1 through P-5 must complete in that window.

---

## 2. Equivalence Test (P-1 Acceptance)

Before any legacy `pipeline.md` is replaced, the canonical `_base/pipeline.md` + the new `delta.md` must produce a **derived view** that is equivalent to the legacy file. Equivalence is defined as:

| Equivalence dimension                           | Acceptance criterion                                                                                                                                                       |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage count + ordering**                      | All stages present in legacy file are present in derived view, in the same numeric order.                                                                                  |
| **Gate criteria**                               | Every gate-criteria checkbox in the legacy file is preserved in the derived view (either in base or delta).                                                                |
| **Personnel assignments**                       | Every named personnel role in the legacy file is preserved.                                                                                                                |
| **P0–P3 severity rules**                        | Identical text.                                                                                                                                                            |
| **Progress Sync Protocol**                      | Identical text.                                                                                                                                                            |
| **"Trim-to-pass" anti-pattern guard (KEEP-01)** | Identical text.                                                                                                                                                            |
| **No content silently dropped**                 | A diff of (legacy `pipeline.md`) vs. (derived view) must show **only** intentional changes from Steps 2/3/4/6/13/15. Any unintentional drop is a P0 defect against Step 5. |

The derived view is constructed by a small render script (one-screen Python) authored under P-1. It concatenates `_base/pipeline.md` + `<product>/delta.md` and substitutes `{{DELTA: …}}` blocks. The script lives at `company/pipeline/_base/render.py`.

---

## 3. Back-Compat Redirect Strategy (Per OPT-R4)

OPT-R4 risk: "Pipeline base + deltas refactor breaks references in existing project files."

Mitigation: maintain backward-compatible filenames as redirects for one quarter (until 2026-07-21).

After P-3 completes, each `company/pipeline/<pipeline-type>/pipeline.md` is replaced with a single-page redirect:

```markdown
# Pipeline (this file has moved)

This file has moved to a base + delta structure as of 2026-05-XX (Step 5 of OPT-2026-04-20-001).

- **Canonical 10-stage skeleton:** [`../_base/pipeline.md`](../_base/pipeline.md)
- **Pipeline-specific overlay:** [`./delta.md`](./delta.md)

This redirect remains in place until **2026-07-21** to give downstream references time to migrate. Any reference to this file should be updated to point at the base + delta pair.
```

The legacy file is **not deleted** during the migration window. Cross-reference updaters (Phase P-4) edit downstream files to point at `_base/pipeline.md` and `<product>/delta.md` directly. After 2026-07-21, the legacy redirects may be deleted in a follow-up plan.

---

## 4. Cross-Reference Inventory (Phase P-4 Targets)

Files known to reference legacy `<pipeline-type>/pipeline.md` paths:

| File                                                    | References to update | Owner            |
| ------------------------------------------------------- | -------------------- | ---------------- |
| `AGENTS.md`                                             | TBD (audit in P-1)   | Tech Writer      |
| `CLAUDE.md`                                             | Multiple             | Tech Writer      |
| `LINGMA.md`                                             | TBD                  | Tech Writer      |
| `QWEN.md`                                               | TBD                  | Tech Writer      |
| `GEMINI.md`                                             | TBD                  | Tech Writer      |
| `company/library/overview/pipeline.md`                  | Multiple             | Tech Writer      |
| `company/library/overview/company.md`                   | TBD                  | Tech Writer      |
| `company/library/overview/personnel.md`                 | TBD                  | Tech Writer      |
| `company/library/topics/architecture.md`                | TBD                  | Tech Writer      |
| `company/optimization-history/2026-04-20-...md`         | §14 traceability     | Operating Review |
| `.claude/agents/*.md`                                   | TBD                  | Tech Writer      |
| `.claude/skills/**/*`                                   | TBD                  | Tech Writer      |
| `.lingma/agents/*.md`, `.qwen/`, `.gemini/`, `.github/` | TBD                  | Tech Writer      |

The full audit is the first deliverable of Phase P-4. A script can produce the inventory: `rg -l 'pipeline/(mobile-development|web-development|backend-api|full-stack)/pipeline\.md'`.

---

## 5. Step Dependencies and Sequencing

Step 5 unlocks Steps 2, 3, 4, 6, 8, 13, 14, 15. The migration plan is structured so that:

- **Steps 2, 3, 4 wait for P-3 to complete** (then they edit `_base/pipeline.md` once instead of editing four legacy files).
- **Step 13 (Stage 6 rename) waits for P-1** (then it edits `_base/pipeline.md` directly).
- **Step 14 (versionable ADRs) waits for P-1**.
- **Steps 6, 15 (Stage 11 / Stage 9.5 inserts) wait for P-1**.
- **Step 8 (3 new release-checklist rows) edits the canonical checklist in `_base/pipeline.md` §"Release Readiness Checklist — Final Form"** (already pre-populated in this skeleton with NEW markers).

---

## 6. Definition of Done (Step 5)

Step 5 transitions to:

| Status           | Trigger                                                                                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `🔵 Implemented` | Phases P-0 through P-4 complete; equivalence test passes for all four product pipelines.                                                                       |
| `🟢 Verified`    | Independent Challenge round (per Plan FIND-P1-08) confirms no gate criteria silently dropped or weakened.                                                      |
| `✅ Closed`      | First post-migration project has executed at least one stage transition (e.g., Stage 1 → Stage 2) using the base + delta structure without operator confusion. |

---

## 7. Document Version History

| Version | Date           | Author             | Changes                                                                                                      |
| ------- | -------------- | ------------------ | ------------------------------------------------------------------------------------------------------------ |
| 0.1     | April 21, 2026 | Software Architect | Initial migration plan authored on Day 1 with Phase P-0 scaffold complete; Phases P-1 through P-5 sequenced. |
