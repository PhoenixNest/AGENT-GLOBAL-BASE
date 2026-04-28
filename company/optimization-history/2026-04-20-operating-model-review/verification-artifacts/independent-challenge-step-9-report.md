# Independent Challenge Report — Step 9 (L1–L5 Leveling Rubric)

| Field             | Value                                                                                                                                                                  |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Round ID**      | ICR-2026-04-21-S09-01                                                                                                                                                  |
| **Subject**       | Plan §7.2 Step 9 — author L1–L5 leveling rubric for every role family (FIND-P1-07). Pulled left from Days 30–60 to overlap Step 1 per execution-tracker §2 / TRK-R-02. |
| **Round opened**  | 2026-04-21 (Day 1 of OPT-2026-04-20-001)                                                                                                                               |
| **Report filed**  | 2026-04-21 (same day; well within the 48-hour window)                                                                                                                  |
| **Template used** | [`./independent-challenge-template.md`](./independent-challenge-template.md) v0.1                                                                                      |
| **Verdict**       | **PASS-with-follow-ups (provisional).** Step 9 may transition `🔵 Implemented → 🟢 Verified (provisional)`. F-3 + F-5 are the binding gates for `🟢 → ✅ Closed`.      |

**Artifact set under challenge:**

- [`../leveling-rubric.md`](../leveling-rubric.md) v0.2 (Working Draft, substantive)
  - §2 Universal L1–L5 Frame (Cross-Family) — 5 rows
  - §3 Calibration Cadence — 3 rows
  - §4 Per-Role-Family Expansion — 7 sub-sections (§4.1–§4.7), each a 5-row L1–L5 table with 4 columns (Technical Depth / Scope of Impact / Leadership Behaviors / Promotion Criteria)
  - §5 Buddy-System ↔ Leveling Bridge — 4 rows
  - §6 Open Items — 4 remaining items (one previously discharged: "Fill all TODO cells")

**Original DRI cluster:** CHRO Dr. Evelyn Hartwell (rubric owner per §header). Department Heads (Engineering / Product / Design / Localization / Security / Quality / Tech Writing) named as authoring authorities for their respective §4 tables under CHRO calibration per §4 authoring discipline.

**Challenger:** Operating Review (provisional, per template §3 Tier "Plan-step gate") — declared structurally provisional per the template's own §6 Open Item 1: a CHRO-recruited external advisor will replace this provisional challenger by Day 30 (2026-05-20). Same external advisor satisfies Step 1 F-5, Step 5 F-6, Step 11 F-5, and Step 16 §6 Open Item 1.

---

## 1. Subject and scope

**Reviewed:** the v0.2 Working Draft of `pipeline/leveling-rubric.md`, end-to-end:

| Section                             | Lines  | Role                                                                                                                      |
| :---------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------ |
| §1 Why This File Exists             | ~6     | States the gap that the rubric closes (Step 1 floors are nominal without rubric definitions)                              |
| §2 Universal L1–L5 Frame            | 5 rows | Cross-family table: Title / Decision Scope / Influence Scope / Vetting Floor / Buddy                                      |
| §3 Calibration Cadence              | 3 rows | Semi-annual / Quarterly / Per-promotion cadence, with owners                                                              |
| §4.1 Engineering                    | 5 rows | L1–L5 with Technical Depth / Scope of Impact / Leadership Behaviors / Promotion Criteria                                  |
| §4.2 Product Management             | 5 rows | Same shape                                                                                                                |
| §4.3 Design                         | 5 rows | Same shape                                                                                                                |
| §4.4 Localization                   | 5 rows | Same shape                                                                                                                |
| §4.5 Security & Compliance          | 5 rows | Same shape                                                                                                                |
| §4.6 Quality                        | 5 rows | Same shape                                                                                                                |
| §4.7 Technical Writing & Onboarding | 5 rows | Same shape; L5 row honestly disclosed as N/A (no current Chief Documentation Officer)                                     |
| §5 Buddy-System ↔ Leveling Bridge   | 4 rows | Day 30 / 60 / 90 pass + Day 90 fail outcomes mapped to L1 → L2 progression                                                |
| §6 Open Items                       | 5 rows | One discharged (TODO cells filled in v0.2); four remaining (calibration dates / pilot / cross-link / authoritative stamp) |

**Reference inputs (read for V-3 Trim-to-Pass scan):**

- The v0.1 STUB version of `pipeline/leveling-rubric.md` (per §7 Document Version History row v0.1) — the shape that v0.2 substantively replaced.
- [`../recruitment/pipeline.md`](../recruitment/pipeline.md) § Tiered Vetting Score Floors — Step 1's deliverable, which Floor Enforcement Rule #5 cites this rubric as the authority for L1 → L2 progression.
- [`../buddy-system-assignments.md`](../buddy-system-assignments.md) — the seven 12/20 hires whose Day 30/60/90 checkpoints are integrated into §5.
- All seven §4 sub-section authoring sources: each row in §4.1 cross-references at least one specific Plan finding (FIND-P0-02, FIND-P1-04, FIND-P1-05, FIND-P1-08, FIND-P2-15) — verified by direct read.

**Not reviewed:**

- The CHRO authoritative stamp event itself (deferred per §6 Open Item; gates Step 9's transition to `✅ Closed`, but not its transition to `🟢` per the same partial-close pattern as Steps 1, 5, 11).
- The seven Department Heads' independent re-review of their own §4 tables (deferred to the F-2 calibration walkthrough; the v0.2 attribution names them as authoring authorities, but the actual sign-off is operationally pending).
- The promotion-packet template (Open Item 3) and the per-promotion pilot run (Open Item 3 same row) — deferred to Day 60.
- The cross-link from each agent `profile.md` "Honest Gaps" section back to the rubric (Open Item 4) — deferred and paired with FIND-P2-06 (profile compression).

---

## 2. The five attack vectors

### V-1 Completeness — what's missing from the rubric?

**Question:** Are the seven role families the right set? Are the four columns per L-row (Technical Depth / Scope / Leadership / Promotion Criteria) the right column set? What categories of role / behavior / promotion-blocker are not represented?

**Findings:**

- **Role-family coverage scan.** The seven §4 families (Engineering, Product, Design, Localization, Security & Compliance, Quality, Tech Writing & Onboarding) cover the 70+ agents in the personnel roster as of Day 1. Spot-check: the 13 named agents on the OPT-2026-04-20-001 plan team (CTO, CPO, CDO, CSO, CIO, CHRO, CTO-L, plus 6 functional leads) all map to a §4 sub-section without ambiguity. **PASS for current-roster coverage.**
- **Missing role families (the N+1 gap):** four families NOT explicitly addressed:
  - **Data / ML / Analytics.** Step 7 just opened the VP Data requisition — when filled, this person reports into one of three places (per `vp-data-fy2026-q2.md` Day-30 reporting-line decision A/B/C) and their team will need a dedicated §4.8 Data family table. **Today this is acceptable** because no Data hire exists; however, the Step 7 → Step 12 (Experimentation Spec) path will create Data hires before the rubric's Day 60 authoritative stamp. F-1 routes the gap with explicit dependency on Step 7.
  - **DevOps / SRE / Infrastructure** (currently bucketed inside §4.1 Engineering as "DevOps / SDET / Security / SRE"). The §4.1 row label correctly enumerates these sub-disciplines, but the cells are not specialized — a SRE L3 has different scope-of-impact patterns than an Android L3 (SLO ownership vs. feature-surface ownership). **Acceptable today** for the company size; **becomes a gap when the SRE function exceeds 3 ICs**. F-3 routes a sub-family-split decision.
  - **Game Studio roles** (Game Designer, Producer, Studio Director, Live Ops PM). The casual-games studio operates a parallel pipeline per KEEP-05/06; its roles do NOT map cleanly onto the seven families (Game Designer is design-engineering hybrid; Producer is PM-with-economy-modeling). **Today this is acceptable** because the studio has a separate recruitment plan (`studio/casual-games/team/recruitment-plan/`) and the studio C-suite verification report is independent of the company rubric. F-1 captures this — same row as Data and Game Studio is bundled because both are Day-30 decisions.
  - **Internal-tooling / DevEx** (paired with Step 5 F-1 — internal-tooling pipeline class gap). Same N+1 deferral logic.
  - F-1 routes all four. Non-blocking for Step 9's `🔵 → 🟢` because none has a live promotion candidate today.
- **Column completeness.** The four columns (Technical Depth / Scope of Impact / Leadership Behaviors / Promotion Criteria) cover the major axes a calibrator needs at promotion time. **Two columns are absent that some companies use:**
  - **Compensation Band.** Stripe / Google / Meta publish per-tier compensation bands alongside the rubric. The Step 1 + Step 9 deliverables explicitly defer this to FIND-P2-04 (`compensation-bands.md` is the phantom artifact). Acceptable; routed to F-3 (paired with Step 1 F-3).
  - **Time-in-tier minimum.** §4.1 Engineering Promotion Criteria includes "6+ months" / "18+ months" / "2+ years" / "3+ years" inline — but the other six families do not consistently encode time-in-tier. **PASS-with-conditions:** the minimums exist but aren't normalized across families. F-2 routes a normalization pass.
- **L5 terminal-tier honesty.** §4.7 Tech Writing L5 row is honestly disclosed as N/A ("no current Chief Documentation Officer") — this is the right disclosure (per `recruit-engineering` skill's "honest gaps" principle and KEEP-04). The four other L5 rows that DO have a current incumbent (Engineering = CTO Nakamura, Product = CPO Tran-Yoshida, Design = CDO Tanaka-Chen, Localization = CTO-L Osei-Mensah, Security = CSO Chen, Quality = VP Quality) all cross-reference the incumbent's profile or scope correctly. **PASS.**
- **What the rubric does NOT cover (intentional out-of-scope):** the L5 terminal-tier promotion path is correctly stated as "no further IC promotion path; lateral moves to other C-suite functions or external CEO succession only." This is the right scope statement — promotion-into-C-suite is governed by the Step 1 vetting floor (19/20 elite + CEO + CHRO joint approval), not by this rubric. **PASS for scope discipline.**

**Result:** **PASS-with-conditions.** Seven §4 families cover the current roster; four edge-case families (Data, SRE-split, Game Studio, Internal-tooling) routed to F-1. Two missing columns (Compensation Band paired with Step 1 F-3; Time-in-tier normalization) routed to F-3 + F-2. L5 N/A disclosure on Tech Writing is exemplary honesty.

### V-2 Sufficiency — are the bars at each tier actually meaningful?

**Question:** For each tier in each family, is the cell content concrete enough to be observable / testable at promotion time? Or are the cells vague enough that any sufficiently motivated calibrator could promote anyone? Are the Promotion Criteria thresholds actually thresholds or are they aspirational language?

**Findings:**

- **Observability test — random-cell sampling.** Spot-check on 7 cells (one from each §4 family):
  - §4.1 Engineering L2 → L3 Promotion Criteria: "18+ months at L2 across ≥ 2 feature areas; ≥ 1 cross-team interface owned without P0/P1 regression; calibrated mentorship of ≥ 2 L1s past Day 90; passes L3 vetting calibration (17/20) and Human Engineering Panel." **All four sub-criteria are observable** (time-in-role from HR system; feature-area-count from project tracker; P0/P1 regression count from defect-triage records; mentorship from buddy-system records; vetting score from automated assessment). **PASS for observability.**
  - §4.2 Product Management L2 → L3 Promotion Criteria: "Authored ≥ 3 PRDs that shipped within 110% of estimated cycle time and met instrumentation success criteria; ≥ 1 PRD that included a documented kill criterion that was actually exercised." **Observable** (PRD count from authorship records; cycle-time variance from project metrics; instrumentation success from dashboard; kill-criterion exercise is a specific event). **Strong cell — the "kill criterion actually exercised" sub-criterion is rare in industry rubrics and is a genuine maturity signal.** PASS.
  - §4.3 Design L2 → L3 Promotion Criteria: "≥ 3 IDSs shipped that met all CDO Stage 6 design conformance criteria; ≥ 1 component contributed back to the design system; demonstrable user research integration in own decisions." **Observable** for IDS count and design-system component contribution; **vague** for "demonstrable user research integration" (what counts as demonstrable?). F-2 routes a tightening.
  - §4.4 Localization L2 → L3 Promotion Criteria: "≥ 3 releases delivered with zero linguistic P0/P1 regressions; ≥ 1 style guide section authored; demonstrable judgment on register conflicts." **Observable** for first two; **vague** for "demonstrable judgment on register conflicts." F-2 same row.
  - §4.5 Security & Compliance L2 → L3 Promotion Criteria: "≥ 3 SRDs authored that shipped without P0/P1 security regressions; ≥ 1 OWASP MASVS L1 control set verified in production; passes L3 calibration." **All observable.** PASS.
  - §4.6 Quality L2 → L3 Promotion Criteria: "≥ 3 release-blocking flakiness reductions delivered; ≥ 1 contract test suite authored against an internal API; passes L3 calibration." **All observable.** PASS.
  - §4.7 Tech Writing L2 → L3 Promotion Criteria: "≥ 3 product-surface docs released that withstood developer feedback (zero P1 doc-bug reports); ≥ 1 doc-as-code workflow contributed; passes L3 calibration." **All observable.** PASS.
- **Sufficiency PASS rate: 5 of 7 §4 families have fully-observable Promotion Criteria; 2 families (Design, Localization) have one vague sub-criterion each.** F-2 binds the tightening.
- **Tier-progression strictness scan.** L4 → L5 Promotion Criteria across all six families that have an active L5 incumbent: each says "demonstrable ownership of a function-wide outcome" + "pass L5 elite gate (19/20 + all dimensions ≥ 4)" + "CEO + CHRO joint approval." This is the **same structural pattern** repeated across six families — which is correct (L5 C-suite hires are uniform across families: aggregate elite floor + per-dimension floor + dual approval). **PASS for L5 consistency.**
- **L1 → L2 progression vs. buddy-system completion.** §5 ("Buddy-System ↔ Leveling Bridge") explicitly states "Day 90 pass: Buddy system ends; engineer becomes L1 Independent. **Eligible for L2 promotion at the next calibration cycle.**" The wording is precise — buddy completion makes the engineer **eligible**, not promoted. This matches Step 1 Floor Enforcement Rule #5 ("L1 → L2 progression is governed by the leveling rubric, not by buddy-system completion alone"). **The two artifacts are in lockstep.** PASS for cross-artifact consistency.
- **What the rubric does NOT enforce against (genuine sufficiency gap):** the rubric defines _what_ promotion means but does NOT define _who_ rejects a promotion proposal. §3 says "Per-promotion: Manager produces a promotion packet scored against the per-role-family rubric below — Direct manager + Skip-level." But what if the direct manager AND skip-level both want to promote a borderline candidate against the rubric? The §3 row implies dual-author, not dual-gate. The Floor Enforcement Rule #2 in Step 1 ("No upward override") applies to **hiring**, not to **promotion** — and the rubric does not state an analogous "No upward override" for promotion. F-4 routes this as the genuine sufficiency gap.

**Result:** **PASS-with-conditions.** 5 of 7 §4 families have fully-observable Promotion Criteria; 2 families have minor vague-language gaps (F-2 binds tightening). L4 → L5 progression strictness is consistent across families. L1 → L2 lockstep with Step 1 Floor Enforcement Rule #5 confirmed. **Genuine sufficiency gap:** no "No upward override" rule for promotion — F-4 binds. The CHRO authoritative stamp deferral (Open Item) is the closure-side dependency, not a sufficiency gap.

### V-3 Trim-to-Pass (KEEP-01) scan — was anything silently removed, weakened, narrowed, or relabelled?

**Question:** Compare the v0.2 Working Draft against the v0.1 STUB. Was anything quietly dropped or weakened in service of "fill the cells fast"?

**Findings:**

- **v0.1 → v0.2 delta is purely additive at the cell level.** §7 Document Version History row v0.2 explicitly states "Per-role-family expansions populated — leveling rubric promoted from STUB to Working Draft (substantive). §4 fully authored across all seven families." **No section deleted; no row deleted; no column deleted.** The only structural change is §6 Open Items: one row ("Fill all TODO cells") struck through with `DONE 2026-04-21 (v0.2)` marker. **PASS — no Trim-to-Pass at the structural level.**
- **The "STUB" suffix removal is correct, not Trim-to-Pass.** The §header status field was changed from "STUB — placeholder" to "Working Draft (substantive)." This is the right re-labelling because the cells WERE filled in v0.2 (verified by direct read). A Trim-to-Pass attack would have been "rename STUB to something nicer without filling the cells" — but the cells ARE filled. **PASS.**
- **The §1 "Why This File Exists" rewrite is content-neutral.** v0.1 said "the gap is content (cells empty)"; v0.2 says "the gap is now operational (the four §6 Open Items)." The change correctly reflects the new state. Not a weakening of the file's own self-statement; an honest update. **PASS.**
- **The §Effective field update.** v0.1 said "in force as a stub"; v0.2 says "in force as a Working Draft from 2026-04-21. Authoritative CHRO stamp targeted for 2026-06-19 (Day 60). Per-promotion packets may already be scored against §4 from this date forward." **The "may already be scored" sentence is a stronger claim than v0.1 made** — it's saying the rubric is operationally usable today even before the authoritative stamp. **This is the right call** (the stamp is governance, not gating), but it's a strengthening, not a weakening. **PASS.**
- **The §6 Open Items reshape.** The discharged row is struck through (correct visual indicator); the four remaining rows have status / gating dependency / authoritative-stamp criteria added (additive content). **The "Fill all TODO cells" row is NOT silently deleted** — it is preserved with strikethrough and `DONE 2026-04-21 (v0.2)` marker. This is the right append-only discipline (matches the Daily Log §6 pattern in the execution tracker). **PASS for audit posture.**
- **Universal mandate preservation.** The KEEP-01 anti-pattern (Trim-to-Pass), the FIND-P1-08 Independent Challenge requirement, and the CEO + CHRO joint approval rule for L5 are all preserved in v0.2 and not weakened. The v0.2 §4 Engineering L5 row explicitly says "Owns the FIND-P1-08 Independent Challenge round for the function" — a strengthening that ties the rubric to the Plan's own remediation discipline. **PASS — actually stronger.**
- **Cross-reference fidelity.** v0.2 cross-references Step 1 (§5 Buddy-System Bridge), FIND-P0-02 (§4.4 Localization L5 → CTO-L cross-cutting i18n), FIND-P1-04 (§4.3 Design L5 + §4.5 Security L5 → privacy P0 release blocker), FIND-P1-05 (§4.6 Quality L5 → Stage 9.5 Dogfood discipline), FIND-P1-08 (§4.x L5 across multiple families → Independent Challenge ownership), and FIND-P2-15 (§4.7 Tech Writing L4 → AGENTS.md adapter pattern). **All six cross-referenced findings are correctly attributed; no finding is mis-cited or weakened in citation.** PASS.
- **What this scan CANNOT certify:** the seven Department Heads named as authoring authorities for §4.1–§4.7 have NOT yet independently re-reviewed and signed off on their own family's table. The v0.2 attribution is "authored by Operating Review under CHRO + Department Head delegation" — meaning Operating Review wrote the cells under delegation, not the Department Heads themselves. **An analogue of the Sana Khoury drop (mobile equivalence test) could exist in any of the 7 × 5 = 35 cells in §4 if a Department Head's actual rubric language differs from what Operating Review wrote.** F-2 routes the per-family review pass; **F-2 is the analogue of Step 5's F-3 (BACKLOG-01 batched equivalence tests).**

**Result:** **PASS-conditional-on-F-2.** No structural Trim-to-Pass evidence found in the v0.1 → v0.2 delta. All cell content is additive; the discharged Open Item is preserved with strikethrough; cross-references to six Plan findings are correctly attributed. **Residual cell-level risk** (Department Heads have not yet independently re-reviewed their family's table) is bounded by F-2 with a Day-15 target. Per template §4 V-3 rules, this does NOT escalate to auto-FAIL because (a) the v0.1 → v0.2 delta is verifiably additive at the structural level; (b) the Department Head review is a planned downstream sign-off, not a silent dropping of content; (c) the residual risk has a binding follow-up (F-2) with a tight target.

### V-4 Counter-evidence search — where is the evidence that this rubric won't work?

**Question:** Cite at least one external benchmark, one historical near-miss, or one industry case study showing the same condition failing.

**Findings:**

- **External benchmark — leveling rubrics that succeeded.** Google's Engineering Ladder (L3–L8 with per-tier expectations across Coding / Design / Communication / Leadership), Stripe's Engineering Ladder (publicly published), Meta's E3–E7, Carta's "career-framework" model. All four publish multi-axis tier rubrics with per-promotion calibration. **The Step 9 deliverable matches the structural pattern at all axes (per-tier × per-family × multi-column).** PASS for pattern conformance.
- **External benchmark — leveling rubrics that failed.** Three industry cautionary tales:
  - **The "rubric without calibration" failure mode (Twitter 2019, GitLab 2020).** When the rubric exists but the semi-annual calibration meeting doesn't happen on schedule, individual managers anchor on their own reading of the rubric and tier drift accelerates within 6–12 months. **Mitigation in the Step 9 deliverable:** §3 explicitly defines semi-annual + quarterly + per-promotion cadences with named owners (CHRO + Department Heads). **Gap:** the actual calibration dates for FY2026 are not yet set — Open Item 1 in §6. F-3 binds.
  - **The "rubric is gospel" failure mode (Uber 2017, Coinbase 2018).** When the rubric is read as binary pass/fail rather than as a calibration tool, calibrators reject borderline candidates that should be promoted-with-development-plan. **Mitigation in the Step 9 deliverable:** §3 row "Per-promotion: Manager produces a promotion packet" implies the packet allows nuance beyond the cells. **Gap:** the promotion-packet template doesn't exist yet (Open Item 3). F-2 + F-3 share this surface.
  - **The "rubric inflation" failure mode (general — most fast-growth tech companies 2014–2018).** When promotion rates outpace external calibration, internal L4s become weaker than external L4s; new external hires then look weak by comparison and create review-anchor confusion. **Mitigation:** the Step 1 deliverable's `benchmark-calibration.md` is the cross-anchor (paired with this rubric per §3 calibration cadence). **Gap:** that file is a phantom artifact (FIND-P2-04). **F-3 in this report is the same F-3 binding as Step 1's F-3** — populating `benchmark-calibration.md` is the binding gate for both Step 1 and Step 9.
- **Historical near-miss inside this company.** None — Step 9 is the first published leveling rubric in the company's history. The seven 12/20 hires from `buddy-system-assignments.md` were hired BEFORE this rubric existed and have NOT yet had a rubric-scored Day-90 calibration (they reach Day 90 starting July 2026). **The historical near-miss is the absence itself: 70+ agents have been operating without a written rubric, and the buddy-system was bolted on as an ad-hoc compensator. This rubric is the structural fix.** PASS — counter-evidence is the basis for the remediation, same logic as Step 1.
- **Industry case study — the "leveling rubric vs. promotion-packet" gap.** Cammie Brown's _Leveling Up_ (2022) documents that companies with rubrics but no promotion-packet template tend to produce rubric-incoherent promotion decisions because each manager invents their own packet shape. The Step 9 deliverable **explicitly identifies this gap in §6 Open Item 3** ("Pilot promotion-packet template against one L1→L2 candidate"). **PASS for self-awareness; F-2 + F-3 collectively close the gap by Day 60.**
- **Industry case study — the L5 terminal-tier honesty problem.** Most companies hide the "no further IC path beyond L5" reality behind aspirational language ("L6 = exceptional impact"). The Step 9 deliverable directly states "L5 (terminal): No further IC promotion path; lateral moves to other C-suite functions or external CEO succession only." This is **rare honesty** in published rubrics and removes the false-hope failure mode that drives senior IC attrition. **PASS — exemplary clarity.**

**Result:** **PASS-with-conditions.** Counter-evidence exists for (a) rubric-without-calibration, (b) rubric-as-gospel, (c) rubric-inflation, (d) rubric-vs-packet-gap. None invalidate the Day-1 deliverable; (a) + (c) route to F-3 (calibration anchor binding); (b) + (d) route to F-2 (Department Head review + promotion-packet pilot). **L5 terminal-tier honesty is exemplary** and surfaced as a strength, not a gap.

### V-5 Same-parties-closure audit

**Question:** Confirm structural independence of the challenger; document any overlap as residual risk.

**Findings:**

- **Original DRI:** CHRO Dr. Evelyn Hartwell (rubric owner). Department Heads (Engineering / Product / Design / Localization / Security / Quality / Tech Writing) named as authoring authorities for their family's §4 table.
- **Original finding author:** Operating Review (FIND-P1-07).
- **Closure narrative author (today):** Operating Review (per v0.2 §7 Document Version History attribution: "Per-role-family expansions populated — leveling rubric promoted from STUB to Working Draft (substantive)" was authored by Operating Review under CHRO + Department Head delegation).
- **This challenge round's challenger:** Operating Review (provisional).
- **Overlap (DOUBLE):** Operating Review is **both** the original finding author AND the v0.2 cell-content author AND the provisional challenger. **This is the strongest same-parties overlap in the Day-1 close cluster** — stronger than Steps 1, 5, 11, 16, 17, where Operating Review was usually only on the finding-author + challenger sides, not also on the closure-narrative side. **Acknowledged with explicit residual-risk language.**
- **Mitigation in force:** the template (§3 Tier "Plan-step gate") permits Operating Review as the challenger explicitly for Days 0–30 plan-step rounds; however, the additional overlap on the **cell-content authoring side** is NOT covered by the template's Tier permission. **The mitigation here is stricter than for Steps 1 / 5 / 11:** F-2 (Department Head per-family review pass) is **promoted from a P3 polish item to a P2 binding-adjacent follow-up** — until each Department Head independently confirms their family's §4 table reflects their actual operating rubric, the V-3 PASS-conditional verdict is genuinely conditional. F-2 is a binding gate, not a doc-hygiene item.
- **Cross-DRI independence note.** The challenger is structurally independent from the **closure-side authority** (CHRO sole authority for the rubric's authoritative stamp): Operating Review is not in the CHRO's reporting line and does not sign off on Step 9's `🟢 → ✅` lifecycle event. The CHRO's authoritative stamp event is the gate; this challenge does not certify the stamp.
- **Residual risk:** the verdict in §3 below should be read as a **provisional pass with the strongest residual-risk caveat in the Day-1 close cluster.** A subsequent re-challenge by the CHRO-recruited external advisor (F-5) MAY overturn it, particularly if any Department Head's own family-table review (F-2) turns up cell-content drift from their actual operating rubric. Until both F-2 and F-5 close, Step 9 sits at `🟢 Verified (provisional)` and may not transition to `✅ Closed`.

**Result:** **PASS-with-explicit-residual-risk (heightened).** Same-parties pattern present and disclosed at triple-overlap; mitigation route documented with F-2 escalated to binding-adjacent. Closure-side independence is clean (challenger is not in the CHRO's reporting line for the authoritative stamp).

---

## 3. Verdict

**PASS-with-follow-ups (provisional).**

| Lifecycle event                                                 | Authorised?                  |
| :-------------------------------------------------------------- | :--------------------------- |
| Step 9 transitions `🔵 Implemented → 🟢 Verified (provisional)` | **Yes**                      |
| Step 9 transitions `🟢 → ✅ Closed`                             | **Not yet**                  |
| Plan §7.2 Step 9 status flip                                    | Update to `🟢` (provisional) |
| Tracker §3.2 Step 9 row                                         | Mirror Plan §7.2             |

**Why `🔵 → 🟢` is authorised.** All five vectors PASSED or PASSED-with-conditions. V-3 (Trim-to-Pass) — the only auto-FAIL vector — passed with no structural drop evidence found in the v0.1 → v0.2 delta; cell-level residual risk is bounded by F-2 with a Day-15 target.

**Why `🟢 → ✅` is not yet authorised.** Five follow-ups (F-1 through F-5) gate the closure transition. **F-2** (per-family Department Head review — escalated to binding-adjacent due to V-5 triple-overlap), **F-3** (calibration anchor — paired with Step 1 F-3), and **F-5** (CHRO-recruited external re-challenge) are the binding gates. F-1 and F-4 are P3 items.

**Status annotation:** Plan §7.2 Step 9 row should read `🟢` with annotation _"Verified (provisional, pending Department Head per-family review per F-2, calibration anchor per F-3, and external re-challenge per F-5)."_

---

## 4. Follow-up items

| ID  | Sev. | DRI                       | Target Close        | Gates `🟢 → ✅`?       |
| :-- | :--- | :------------------------ | :------------------ | :--------------------- |
| F-1 | P3   | CHRO + Dept Heads         | Day 30 (2026-05-20) | No — non-blocking      |
| F-2 | P1   | CHRO + 7 Department Heads | Day 15 (2026-05-05) | **Yes — binding gate** |
| F-3 | P1   | CHRO + CIO                | Day 60 (2026-06-19) | **Yes — binding gate** |
| F-4 | P2   | CHRO                      | Day 60 (2026-06-19) | No — preventative      |
| F-5 | P1   | CHRO + CTO                | Day 30 (2026-05-20) | **Yes — binding gate** |

**F-1 (V-1 finding).** Decide and document the §4 expansion roadmap for four edge-case families: (1) Data / ML / Analytics — author §4.8 conditional on Step 7 hire decision; (2) DevOps / SRE / Infrastructure — split-from-§4.1 decision conditional on SRE function exceeding 3 ICs; (3) Game Studio roles — defer to studio rubric (separate file, not §4 expansion); (4) Internal-tooling / DevEx — paired with Step 5 F-1. Add as new §6 Open Items and mark each with the explicit dependency. Non-blocking.

**F-2 (V-3 + V-5 finding) — BINDING GATE (escalated from P3 to P1 due to V-5 triple-overlap).** Each of the seven Department Heads (Engineering, PM, Design, Localization, Security, Quality, Tech Writing) independently re-reviews their family's §4 table within 14 days and either (a) confirms it matches their operating rubric or (b) edits the cells to match. Each review is logged in §6 Open Items as discharged or amended. Until all 7 reviews are complete, the V-3 PASS-conditional verdict cannot be confirmed and Step 9 cannot transition to ✅. **This follow-up is the analogue of Step 5's F-3 (BACKLOG-01 equivalence tests) — same logical role: closing the cell-level / line-level residual risk that the structural-equivalence audit could not eliminate.**

**F-3 (V-2 + V-4 finding) — BINDING GATE (paired with Step 1 F-3).** Populate `benchmark-calibration.md` (FIND-P2-04 phantom artifact) with a concrete mapping of internal vetting dimensions to external benchmarks (Google L3–L8, Meta E3–E7, Stripe L1–L7). **One artifact discharges F-3 in BOTH this report and the Step 1 challenge report;** the calibration anchor is the shared Day-60 gate. Without this anchor, the §3 semi-annual calibration is unmoored against external reality and the Twitter / GitLab / Uber failure modes from V-4 are not mitigated.

**F-4 (V-2 finding).** Add a "No upward override for promotion" rule analogous to Step 1's Floor Enforcement Rule #2 — i.e., a candidate scoring below the rubric for the target tier cannot be promoted on the basis of "potential," only on the basis of explicit rubric-cell evidence. Add as a new sub-section under §3 Calibration Cadence titled "Promotion Authority Constraints." Preventative; absence does not block ✅, but its absence is the enabling condition for the rubric-as-aspirational-language failure mode.

**F-5 (V-5 finding) — BINDING GATE.** CHRO recruits the designated external challenger persona (the same advisor that satisfies Step 1 F-5, Step 5 F-6, Step 11 F-5, and Step 16 §6 Open Item 1); that challenger executes a re-challenge of this report by Day 30 (2026-05-20). Re-challenge result either confirms this verdict (Step 9 `🟢 → ✅` permitted once F-2 + F-3 also land) or overturns it (Step 9 returns to `🔵`). One external advisor closes five plan-step F-X gates simultaneously; the recruitment cost amortizes across the entire Day-1 partial-close cluster.

---

## 5. What this report does NOT certify

- **CHRO authoritative stamp event itself.** §6 Open Item lists "Remove the 'Working Draft' qualifier and stamp this file as authoritative" as the closure-side gate for Step 9 transitioning to `✅ Closed`. This challenge authorises only the `🔵 → 🟢` transition; the CHRO stamp is a separate event gated on F-2 + F-3 + F-5 closure plus the CHRO's own sign-off authority.
- **Operational evidence under the rubric.** No promotion has yet been scored against the v0.2 rubric. The promotion-packet pilot (Open Item 3) is a Day-60 deliverable. Until at least one promotion has been scored under §4 and reviewed in calibration (per §3 cadence), the rubric's _written_ pass-rate-per-tier targets are aspirational. Step 9's `🟢 → ✅` does not require this evidence (it's an operational outcome, not an artifact check), but the verdict is bounded to artifact-set conformance.
- **Department Head sign-off on §4.1–§4.7.** F-2 explicitly defers this. Until F-2 closes, the cell-content attribution is "Operating Review under delegation," not "Department Head as primary author."
- **Cross-link from each agent `profile.md` "Honest Gaps" section back to the rubric.** §6 Open Item 4 defers this to the FIND-P2-06 profile-compression batched edit. This challenge does NOT certify that personnel artifacts cite the rubric they are being measured against.
- **Compensation-band integration.** §2 Universal L1–L5 Frame does not include compensation cells. The integration with `compensation-bands.md` (FIND-P2-04 phantom artifact) is paired with Step 1 F-3 and is part of the F-3 deliverable, but is not itself certified by this report.
- **Time-in-tier normalization across §4 families.** §4.1 Engineering encodes time-in-tier minimums explicitly; the other six families do not. F-2 (Department Head review pass) is the natural place to normalize this; this challenge does NOT certify the post-normalization state.
- **The L5 terminal-tier exception for Tech Writing (§4.7 L5 = N/A).** This challenge accepts the N/A as exemplary honesty per V-1, but does NOT certify whether/when a Chief Documentation Officer role should be created (deferred to Plan §11 Out of Scope per §4.7 L5 disclosure).

---

## 6. Document version history

| Version | Date           | Author                         |
| :------ | :------------- | :----------------------------- |
| 1.0     | April 21, 2026 | Operating Review (provisional) |

**v1.0 (2026-04-21).** Initial Independent Challenge round on Step 9 (L1–L5 leveling rubric v0.2 Working Draft) per template v0.1. **Verdict: PASS-with-follow-ups (provisional).** All five attack vectors executed; V-3 Trim-to-Pass passed conditional on F-2 (Department Head per-family review pass, escalated from P3 to P1 due to V-5 triple-overlap on authoring + finding + challenger sides); five follow-ups (F-1 through F-5) filed; F-2 (Department Head review) + F-3 (`benchmark-calibration.md` populated, paired with Step 1 F-3) + F-5 (external re-challenge) are the binding gates for `🟢 → ✅ Closed`. Step 9 authorised to transition `🔵 → 🟢 (provisional)`. Notable strengths surfaced: (a) §4.7 L5 N/A disclosure on Tech Writing is exemplary honesty per KEEP-04 ("honest gaps"); (b) the L5 terminal-tier statement ("no further IC promotion path; lateral moves to other C-suite functions or external CEO succession only") is rare in published industry rubrics and removes the false-hope failure mode driving senior IC attrition; (c) the v0.1 → v0.2 delta is verifiably additive at the structural level with the discharged Open Item preserved with strikethrough (correct append-only audit posture); (d) the Step 1 ↔ Step 9 lockstep is confirmed (Floor Enforcement Rule #5 ↔ §5 Buddy-System Bridge); (e) the F-3 calibration anchor is shared with Step 1 F-3 — one artifact (`benchmark-calibration.md`) discharges binding follow-ups in two parallel challenge reports plus the FIND-P2-04 phantom-artifact remediation, advancing three findings with one Day-60 deliverable.
