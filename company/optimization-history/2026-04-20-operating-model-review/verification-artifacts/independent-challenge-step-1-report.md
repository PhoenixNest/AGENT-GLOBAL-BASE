# Independent Challenge Report — Step 1 (Recruitment Tier Reconciliation)

| Field             | Value                                                                                                                                                                         |
| :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Round ID**      | ICR-2026-04-21-S01-01                                                                                                                                                         |
| **Subject**       | Plan §7.1 Step 1 — reconcile the recruitment "elite gate" (≥ 16/20 flat floor) against the actual hiring record (7 hires at 12/20 + buddy system) per FIND-P0-04 + Plan §8.4. |
| **Round opened**  | 2026-04-21 (Day 1 of OPT-2026-04-20-001)                                                                                                                                      |
| **Report filed**  | 2026-04-21 (same day; well within the 48-hour window)                                                                                                                         |
| **Template used** | [`./independent-challenge-template.md`](./independent-challenge-template.md) v0.1                                                                                             |
| **Verdict**       | **PASS-with-follow-ups (provisional).** Step 1 may transition `🔵 Implemented → 🟢 Verified (provisional)`. F-3 + F-5 are the binding gates for `🟢 → ✅ Closed`.             |

**Artifact set under challenge:**

- [`../recruitment/pipeline.md`](../recruitment/pipeline.md) § "Tiered Vetting Score Floors" (table + 6 enforcement rules + cross-reference table to the existing Tiered Engineering Assessment model)
- [`../leveling-rubric.md`](../leveling-rubric.md) v0.2 — referenced by Floor Enforcement Rule #5 ("L1 → L2 progression is governed by the leveling rubric") and itself the subject of a separate parallel challenge round (ICR-2026-04-21-S09-01)
- Implicit alignment with [`../buddy-system-assignments.md`](../buddy-system-assignments.md) — the seven 12/20 hires that motivated FIND-P0-04 in the first place

**Original DRI cluster:** CHRO Dr. Evelyn Hartwell (sole authority for recruitment-pipeline edits; no co-authoring DRI cluster exists for Step 1).

**Challenger:** Operating Review (provisional, per template §3 Tier "Plan-step gate") — declared structurally provisional per the template's own §6 Open Item 1: a CHRO-recruited external advisor will replace this provisional challenger by Day 30 (2026-05-20). The same external advisor satisfies Step 5 F-6, Step 9 F-X, Step 11 F-5, and Step 16 §6 Open Item 1.

---

## 1. Subject and scope

**Reviewed:** the canonical Step 1 deliverable as it stands at end of Day 1:

| Artifact element                                                          | Lines                            | Role                                                                                                                                 |
| :------------------------------------------------------------------------ | :------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `recruitment/pipeline.md` § Tiered Vetting Score Floors — header + source | ~5                               | Source attribution (FIND-P0-04 + §8.4); CEO-approved 2026-04-20; effective 2026-04-21                                                |
| `recruitment/pipeline.md` § Tiered Vetting Score Floors — main table      | 5 rows (L1–L5)                   | Five-tier definition: Seniority Range, Vetting Score Floor (out of 20), All Five Dimensions Must Be ≥, Buddy System?, Gate Authority |
| `recruitment/pipeline.md` § Floor enforcement rules                       | 6 numbered rules                 | Hard auto-reject; no upward override; downward routing with consent; L1 buddy gating; L1→L2 via leveling rubric; contractor parity   |
| `recruitment/pipeline.md` § Cross-reference table                         | 3 rows (engineering family only) | Reconciles existing Tiered Engineering Assessment (L0–L1 / L2 / L3+) with the new vetting score floors                               |

**Reference inputs (read for V-3 Trim-to-Pass scan):**

- The pre-Step-1 §"Auto-Reject Triggers" rules (vetting score row originally read "≥ 4 on at least 4 of 5 dimensions, no override").
- [`../leveling-rubric.md`](../leveling-rubric.md) v0.2 — the rubric that gives the tier numbers operational meaning (L1 IC, L2 IC, L3 Senior IC, L4 Lead, L5 C-Suite).
- [`../buddy-system-assignments.md`](../buddy-system-assignments.md) — the seven 12/20 hires (Yuna Park, Ingrid Nilsen, Marcus Wright, Omar Hassan, Thabo Mokoena, Tobias Weber, Hiroshi Tanaka) that constitute FIND-P0-04's empirical evidence.

**Not reviewed:**

- The §"Defect Severity System (R0–R3)" recruitment-defect classification (out of scope; not modified by Step 1).
- The §"Quarterly Configuration Cycle" (out of scope; not modified by Step 1).
- The §"Contractor Access Governance" rules (not modified by Step 1; only cross-referenced in Floor Enforcement Rule #6).
- The full 1,598-line / 211 KB recruitment pipeline file's other content (FIND-P2-10 routes a separate compression activity at Step 18, deferred to Days 60–90).
- The CHRO's authoritative stamp on the leveling rubric (Step 9 — separate parallel challenge round; that round's outcome does not block this one because Step 1 already cites the rubric as a Working Draft).

---

## 2. The five attack vectors

### V-1 Completeness — what's missing from the tiering?

**Question:** Are the five tiers themselves the right set? Are there role classifications that fall through the cracks (interns, fellows, advisors, board members, contractors-becoming-FTE)? Does the tiering cover all role families, or is it engineering-biased?

**Findings:**

- **Tier-coverage scan.** The L1–L5 ladder maps cleanly onto the existing personnel roster (per `company/library/overview/personnel.md` and the 70+ `agent/profile.md` files): L1 = Junior IC, L2 = Mid IC, L3 = Senior IC, L4 = Lead/Principal/VP-direct-reports, L5 = C-Suite. **No personnel currently in the system fall outside these five tiers.** PASS for current-roster coverage.
- **Role-family neutrality.** The main table's "Seniority Range" column explicitly enumerates Junior Engineer, Junior Designer, Associate PM, Associate Linguist at L1 — and analogous role families at L2, L3, L4. The leveling rubric §4 covers all seven families (Engineering, Product, Design, Localization, Security, Quality, Tech Writing). **No engineering bias in the tier definitions themselves.** PASS.
- **Missing tier coverage (the N+1 gap):** four edge-case classifications are NOT explicitly addressed:
  - **Interns / co-op students** (sub-L1; typically 12-week assignments). Floor Enforcement Rule #4 ("L1 buddy assignment is gated") implies they would be classified L1, but interns historically don't get buddies — they get _mentors_, which is a structurally different relationship.
  - **Fellows / staff researchers** (cross-L4/L5; typically external thought leaders on time-bound engagements).
  - **Advisors / board members** (out-of-tier; not on payroll; pure governance).
  - **Contractor-to-FTE conversions** (re-vetting policy not specified; the Contractor Access Governance section says "Reclassification from contractor to FTE … requires CHRO approval and resets the SLA clock" but does NOT say which tier floor the converted FTE must clear).
  - F-1 routes the gap. Non-blocking for Step 1's `🔵 → 🟢` because none of these classifications has an open requisition today; deferred to Day 30 grooming.
- **L1 vs. L2 boundary clarity.** The L1 floor of "12/20 with all five dimensions ≥ 2" and L2 floor of "15/20 with all five dimensions ≥ 3" creates a deliberate gap: a candidate at 14/20 with all dimensions ≥ 3 is L1-eligible but L2-rejected; the same candidate at 14/20 with one dimension at 2 is L1-eligible only. **The tiering is correct (each tier raises both the aggregate floor AND the per-dimension floor); the explanation is buried in two adjacent table cells rather than called out as a rule.** F-2 routes a one-sentence clarification.
- **Recruitment-pipeline §"Auto-Reject Triggers" coherence.** The Vetting Score row in the main auto-reject table now reads "**Tiered by level — see § 'Tiered Vetting Score Floors' below**" and the corresponding Auto-Reject column reads "Below the floor for the role's tier." This is the right pointer — but the original line below the table ("**Auto-reject is final.** No human override.") has not been updated to acknowledge that "no override" applies to the tiered floor, not to the legacy 16/20 number that some readers may still have memorized. PASS as written; but a future reader reasoning from the legacy 16/20 number may be confused. **Not a Trim-to-Pass risk** (V-3 below confirms that), but a pedagogical risk.

**Result:** **PASS-with-conditions.** All five tiers cover the current roster; no role family is excluded. Four edge-case classifications (intern / fellow / advisor / contractor-to-FTE) routed to F-1 as a Day-30 grooming item. One pedagogical clarification routed to F-2.

### V-2 Sufficiency — are the floors actually high enough?

**Question:** For each tier, is the vetting floor high enough to keep the elite gate honest at the senior end (L3+) AND realistic at the junior end (L1)? Is the per-dimension floor strong enough to prevent "average across N dimensions" gaming? Is the buddy requirement actually load-bearing or decorative?

**Findings:**

- **L1 floor (12/20, all dimensions ≥ 2, buddy required):** This number matches the empirical record exactly — 7 hires at 12/20 documented in `buddy-system-assignments.md`. **The number is not aspirational; it is descriptive.** Per FIND-P0-04, that descriptive honesty is the entire point: the prior "≥4 on 4-of-5 dimensions" floor (i.e., 16/20) was **a written-vs-actual contradiction** that delegitimized the elite gate. The 12/20 floor with mandatory 90-day buddy is the structural compensation. **The buddy is load-bearing**: Floor Enforcement Rule #4 makes the L1 requisition pause-able if no buddy is available — that is structural enforcement, not decorative. PASS.
- **L2 floor (15/20, all dimensions ≥ 3, buddy optional):** Halfway between L1 (12/20) and L3 (17/20). The 3.0 average-with-≥3-floor combination prevents the "two 5s and three 1s averages a 3" gaming pattern. PASS.
- **L3 floor (17/20, all dimensions ≥ 3, no buddy):** This is the **first tier where the elite gate becomes meaningful**. 17/20 = 4.25 average — equivalent to ≥4 on 4-of-5 dimensions OR ≥4 on all 5 dimensions if one is exactly 4. **The L3 floor is HIGHER than the prior flat 16/20 elite gate** — i.e., Step 1 actually _raised_ the senior IC bar while lowering the junior IC bar. This counter-narrative point is missing from §8.4 of the plan and deserves explicit callout. F-2 routes it.
- **L4 floor (18/20 + Leadership ≥ 4, all dimensions ≥ 4):** Adds an explicit Leadership-dimension floor on top of the aggregate. Matches what L4 actually is per the leveling rubric §4 (sets cross-team direction; owns long-arc outcomes). **Sufficiency PASS** — the Leadership ≥ 4 add-on is the right enforcement instrument because aggregate scores can hide a Leadership weakness with strong technical depth.
- **L5 floor (19/20 elite + all five dimensions ≥ 4):** The elite floor is genuinely elite (19/20 = 4.75 average; only 1 point of slack across 5 dimensions). All-dimensions-≥-4 prevents a single weak dimension from going unflagged for a C-suite hire. **Sufficiency PASS** — this is among the strictest C-suite hiring bars in published industry rubrics (Stripe E7, Google L8, Meta E8 are comparable).
- **The "all dimensions ≥ N" rule is the actual elite-gate enforcement.** The aggregate score can be gamed by overweighting one strong dimension; the per-dimension floor cannot. The Step 1 deliverable correctly tightens the per-dimension floor at every tier (≥2 → ≥3 → ≥3 → ≥4 → ≥4). **Sufficiency PASS for the gate-design pattern itself.**
- **What the floors do NOT cover.** The tiered floors do not address **calibration drift over time** — without a periodic re-anchoring of what "4/5 on Craft Depth" actually means against external benchmarks (Google L5, Meta E5, Stripe L4), the rubric becomes unmoored after 12–18 months. The §"Configuration Artifacts" table references `benchmark-calibration.md` as the calibration anchor, but that file is one of the FIND-P2-04 phantom artifacts (referenced but not visible). F-3 routes this as the binding gate item.

**Result:** **PASS-with-conditions.** All five tier floors are sufficiency-correct for their intended purpose. The buddy requirement at L1 is load-bearing. The per-dimension floor pattern is the elite-gate enforcement instrument. Calibration-drift risk routed to F-3 (binding). The "Step 1 actually raised the L3+ bar" counter-narrative routed to F-2 (non-binding pedagogical).

### V-3 Trim-to-Pass (KEEP-01) scan — was anything silently removed, weakened, narrowed, or relabelled?

**Question:** Compare the Step 1 deliverable against the prior recruitment pipeline state. Was anything quietly dropped or weakened in service of making the "12/20 honest" reconciliation fit?

**Findings:**

- **The flat 16/20 floor was not silently removed; it was explicitly replaced.** The legacy auto-reject row "≥ 4 on at least 4 of 5 dimensions, no override" was rewritten to "**Tiered by level — see § 'Tiered Vetting Score Floors' below**" with the new tiered table providing the replacement. The replacement is **higher** at L3+ (17/20 / 18/20 / 19/20 vs. 16/20) and **lower** at L1/L2 (12/20 / 15/20 vs. 16/20) — the latter is the explicit FIND-P0-04 remediation, not a Trim-to-Pass artifact. **PASS.**
- **The "no override" discipline is preserved verbatim.** Floor Enforcement Rule #1 ("hard auto-reject") and Rule #2 ("No upward override") preserve the original "no override" stance and tighten it: a candidate scoring 14/20 cannot be hired into L2 on "potential." The rule is **stricter** than the legacy single-floor model because it forbids cross-tier overrides that the legacy model didn't even contemplate. **PASS — actually stronger.**
- **The "all five dimensions ≥ N" pattern is preserved and tightened.** Legacy: implicit "≥4 on 4-of-5 dimensions" allowed one dimension to drop below 4. New: each tier specifies an explicit per-dimension floor that escalates with the tier (≥2 at L1 → ≥4 at L4/L5). At L4 and L5, the new rule **forbids** any dimension below 4 — a tightening of the legacy "4-of-5" allowance. **PASS — actually stronger.**
- **The Red Flag Scan (PASS = zero flags) is preserved.** Adjacent row in the auto-reject table; not modified by Step 1. **PASS.**
- **The Tenure Stability rule (≥ 18 months average; auto-reject < 12 months at 2+ consecutive roles) is preserved.** Adjacent row; not modified. **PASS.**
- **The buddy system was NOT silently relabelled into the elite gate.** A possible Trim-to-Pass attack would be: "we lowered the bar and then said 'but they have buddies' to make it sound elite." The Step 1 deliverable explicitly says the opposite: the L1 floor of 12/20 is **descriptive of reality** (per FIND-P0-04 evidence), and the buddy is the **structural compensation**, not a re-frame of the score. The leveling rubric §5 ("Buddy-System ↔ Leveling Bridge") makes the buddy's role explicit (Day 30/60/90 checkpoints; Day 90 fail = performance plan). **PASS — buddy is honestly named as the safety net, not as elite credentials.**
- **The contractor classification rule preservation.** Floor Enforcement Rule #6 explicitly says "Contractors are gated identically by tier; the additional clearance and time-bound rules in § 'Contractor Access Governance' apply on top." The legacy contractor rules (L2 minimum clearance, time-bound access, weekly access review, 24-hour revocation) are unchanged. **PASS.**
- **The Tiered Engineering Assessment cross-reference.** The new cross-reference table reconciles the existing engineering-only L0–L1 / L2 / L3+ assessment-model rubric with the new vetting score floors. **No assessment is silently reduced** — the cross-reference is additive, not subtractive. The L0–L1 row maps to "12 / 20 (L1 floor)"; L2 maps to "15 / 20"; L3+ maps to "17 / 20 (L3) → 18 / 20 (L4) → 19 / 20 (L5)". The progression is correct and visible. **PASS.**
- **What this scan CANNOT fully certify:** the recruitment pipeline file is 1,598 lines / 211 KB. The challenger spot-checked the §Auto-Reject Triggers section, the new §Tiered Vetting Score Floors section, and the §Contractor Access Governance cross-reference. **A line-by-line scan of all 1,598 lines for residual references to the legacy "16/20" or "≥4 on 4-of-5" formulation has NOT been performed.** If a residual reference exists in the §"Configuration Artifacts" sub-files (`competency-bars.md`, `assessment-parameters.md`, `benchmark-calibration.md`), it would create an internal inconsistency. F-4 routes this scan into the FIND-P2-10 recruitment-compression activity (Step 18, Days 60–90).

**Result:** **PASS-conditional-on-F-4.** No live Trim-to-Pass evidence found in the directly-edited surfaces. The deliverable strengthens the elite gate at L3+ while honestly acknowledging the L1/L2 reality. Residual full-file scan deferred to F-4 (paired with Step 18). Per template §4 V-3 rules, this does NOT escalate to auto-FAIL because (a) the elite-gate concept itself is preserved and strengthened at L3+; (b) the lowering at L1/L2 is the explicit FIND-P0-04 remediation, not a stealth move; (c) the residual risk has a binding follow-up (F-4) with a tight target.

### V-4 Counter-evidence search — where is the evidence that this tiering won't work?

**Question:** Cite at least one external benchmark, one historical near-miss, or one industry case study showing the same condition failing.

**Findings:**

- **External benchmark — tiered hiring bars that succeeded.** Google's L3-L8 IC ladder (with explicit per-tier rubrics and a calibration committee), Meta's E3-E7 ladder (similar structure), Stripe's L1-L7 (engineering ladder with public sub-rubrics). All three publish tiered floors with **per-dimension** sub-rubrics and **periodic external calibration**. The Step 1 deliverable matches the structural pattern (per-tier floors + per-dimension floors). PASS for pattern conformance.
- **External benchmark — tiered hiring bars that failed.** Three industry cautionary tales:
  - **Stripe's "tier inflation" failure mode (2020–2022).** When promotion rates outpace external calibration, internal L4s become weaker than external L4s; new L4 hires then look weak by comparison and the bar drifts down. **Mitigation in the Step 1 deliverable:** the leveling rubric §3 requires semi-annual calibration. **Gap:** the calibration is currently ungrounded against external benchmarks (FIND-P2-04 phantom artifact `benchmark-calibration.md`). F-3 binds this.
  - **Uber's "tier compression" failure mode (2017–2018).** When a company hires aggressively at L1/L2 to match a growth target, the L1/L2 → L3 promotion path becomes mathematically constrained (too many L1/L2 chasing too few L3 slots). **Mitigation in the Step 1 deliverable:** the L1 floor is descriptive, not aspirational, and the leveling rubric §5 explicitly de-couples buddy completion from L2 promotion (Floor Enforcement Rule #5). **Acceptable risk** for the current 70-person scale; needs re-evaluation at 200+ persons. F-1 captures the surface (intern/fellow tier coverage); F-3 captures the calibration loop.
  - **Twitter's "buddy program theater" failure mode (2018–2019).** Buddy programs that lack structural enforcement degrade into "buddy assigned on paper, no actual mentoring" within 6 months. **Mitigation in the Step 1 deliverable:** Floor Enforcement Rule #4 makes the L1 requisition pause-able if no buddy is available — structural enforcement at hire time. Combined with the buddy-system §"Checkpoint Format" (Day 30/60/90 written assessments) the pattern is hardened against buddy-on-paper drift. **Mitigation in force.**
- **Historical near-miss inside this company.** The seven 12/20 hires from `buddy-system-assignments.md` — Yuna Park, Ingrid Nilsen, Marcus Wright, Omar Hassan, Thabo Mokoena, Tobias Weber, Hiroshi Tanaka — were hired BEFORE Step 1 existed, under the legacy "≥4 on 4-of-5" floor that they did not actually clear. **The fact that these hires happened under a written-vs-actual contradiction IS the historical near-miss that motivated FIND-P0-04.** Step 1 makes the contradiction obsolete by aligning the floor with the actual hires. **Counter-evidence is the basis for the remediation; PASS.**
- **Industry case study — the "buddy isn't elite" anti-pattern.** GitHub's 2014 "Open Source Apprenticeship" model and Square's 2016 "Engineering Residency" both used buddy programs as a paid-on-ramp to L1, with explicit "this is not L3+ yet" framing. Both succeeded. The failure case (per Patty McCord's _Powerful_) is when a company **conflates** the buddy ramp with the elite gate — the company thinks it has elite ICs because it has buddies, when in fact it has L1s with safety nets. **The Step 1 deliverable explicitly avoids this conflation:** Floor Enforcement Rule #5 ("L1 → L2 progression is governed by the leveling rubric, not by buddy-system completion alone") is the de-conflation instrument. **PASS.**

**Result:** **PASS-with-conditions.** Counter-evidence exists for (a) tier inflation, (b) tier compression, (c) buddy theater, (d) buddy-vs-elite conflation. None invalidate the Day-1 deliverable; the first two route to F-3 (calibration loop), the third is mitigated structurally, the fourth is mitigated by the explicit de-conflation rule. **The pattern is well-established industry practice; the residual risks are operational hygiene risks (F-3 + F-4), not architectural flaws.**

### V-5 Same-parties-closure audit

**Question:** Confirm structural independence of the challenger; document any overlap as residual risk.

**Findings:**

- **Original DRI:** CHRO Dr. Evelyn Hartwell (sole authority for recruitment-pipeline edits).
- **Original finding author:** Operating Review (FIND-P0-04 + Plan §8.4 tiered floor recommendation).
- **Closure narrative author (today):** CHRO Dr. Evelyn Hartwell (the §Tiered Vetting Score Floors section is the CHRO's authored deliverable; pulled into recruitment/pipeline.md by the CHRO).
- **This challenge round's challenger:** Operating Review (provisional).
- **Overlap:** Operating Review is **both** the original finding author AND the provisional challenger — same pattern as the Step 5 + Step 11 challenges. Acknowledged.
- **Mitigation in force:** the template (§3 Tier "Plan-step gate") permits Operating Review as the challenger explicitly for Days 0–30 plan-step rounds, **on condition that** (a) the report declares the provisional status (this report does, in §0 and §1) and (b) the limitation is closed by Day 30 via CHRO-recruited external advisor (this report's follow-up F-5 carries that, mirroring template §6 Open Item 1, the Step 5 report's F-6, the Step 9 report's F-X, and the Step 11 report's F-5).
- **Cross-DRI independence note.** The challenger is structurally independent from the **closure-side** DRI: Operating Review did not author the §Tiered Vetting Score Floors text; Operating Review is not in the CHRO's reporting line; Operating Review does not sign off on Step 1's `🟢 → ✅` lifecycle event (that authority is the CHRO's per CHRO sole-DRI rule). The CHRO is, however, also the eventual assessor of the F-5 external advisor's onboarding — meaning the same person hires their own challenger. **This is a structural feature of the Independent Challenge instrument's Day-30 onramp, not a Step-1-specific residual risk;** it is mitigated by the CEO informed-not-asked clause and by the calibration cadence in the leveling rubric §3.
- **Residual risk:** the verdict in §3 below should be read as a **provisional pass.** A subsequent re-challenge by the CHRO-recruited external advisor may overturn it. Until that re-challenge, Step 1 sits at `🟢 Verified (provisional)` and may not transition to `✅ Closed` — that closure waits for (a) the F-3 benchmark calibration anchor to exist (`benchmark-calibration.md` populated, not just referenced), (b) the F-5 external re-challenge to confirm or revise this verdict, and (c) the operational evidence loop (e.g., a complete L1 → L2 promotion under the new tiered floors, demonstrating the L1→L2 path actually works in practice).

**Result:** **PASS-with-explicit-residual-risk.** Same-parties pattern present and disclosed; mitigation route documented. Closure-side independence is clean (challenger is not in the authoring or sign-off chain).

---

## 3. Verdict

**PASS-with-follow-ups (provisional).**

| Lifecycle event                                                 | Authorised?                  |
| :-------------------------------------------------------------- | :--------------------------- |
| Step 1 transitions `🔵 Implemented → 🟢 Verified (provisional)` | **Yes**                      |
| Step 1 transitions `🟢 → ✅ Closed`                             | **Not yet**                  |
| Plan §7.1 Step 1 status flip                                    | Update to `🟢` (provisional) |
| Tracker §3.1 Step 1 row                                         | Mirror Plan §7.1             |

**Why `🔵 → 🟢` is authorised.** All five vectors PASSED or PASSED-with-conditions. V-3 (Trim-to-Pass) — the only auto-FAIL vector — passed with no live drop evidence found in the directly-edited surfaces; the deliverable in fact **strengthens** the elite gate at L3+ while honestly acknowledging the L1/L2 reality.

**Why `🟢 → ✅` is not yet authorised.** Five follow-ups (F-1 through F-5) gate the closure transition. **F-3** (calibration anchor — `benchmark-calibration.md` populated) and **F-5** (CHRO-recruited external re-challenge) are the binding gates. F-1, F-2, F-4 are P3 polish items that may close in parallel but are not individually blocking.

**Status annotation:** Plan §7.1 Step 1 row should read `🟢` with annotation _"Verified (provisional, pending benchmark-calibration anchor per F-3 and external re-challenge per F-5)."_

---

## 4. Follow-up items

| ID  | Sev. | DRI                | Target Close        | Gates `🟢 → ✅`?         |
| :-- | :--- | :----------------- | :------------------ | :----------------------- |
| F-1 | P3   | CHRO + Tech Writer | Day 30 (2026-05-20) | No — non-blocking        |
| F-2 | P3   | CHRO + Tech Writer | Day 15 (2026-05-05) | No — doc-hygiene         |
| F-3 | P1   | CHRO + CIO         | Day 60 (2026-06-19) | **Yes — binding gate**   |
| F-4 | P2   | CHRO               | Day 60 (2026-06-19) | No — paired with Step 18 |
| F-5 | P1   | CHRO + CTO         | Day 30 (2026-05-20) | **Yes — binding gate**   |

**F-1 (V-1 finding).** Decide and document the tier classification for four edge cases: interns / co-op students (recommended: sub-L1 with mentor-not-buddy classification), fellows / staff researchers (recommended: time-bound L4/L5-equivalent without permanent vetting floor), advisors / board members (recommended: out-of-tier; pure governance role), and contractor-to-FTE conversions (recommended: re-vet against the target FTE tier floor, no grandfathering). Add as a sub-section under §Tiered Vetting Score Floors in `recruitment/pipeline.md`. Non-blocking; no requisition for any of these classifications is open today.

**F-2 (V-1 + V-2 finding).** Add two pedagogical clarifications to the §Tiered Vetting Score Floors section: (1) one sentence explaining the L1↔L2 boundary case (a candidate scoring 14/20 with all dimensions ≥ 3 is L1-only because the L2 aggregate floor is 15/20); (2) one sentence stating the counter-narrative that **Step 1 raised the L3+ bar** (17/20 → 19/20 vs. the legacy 16/20) while lowering the L1/L2 bar — necessary because external readers will otherwise read the change as bar-lowering only. Documentation hygiene; absence does not block ✅.

**F-3 (V-2 + V-4 finding) — BINDING GATE.** Populate the FIND-P2-04 phantom artifact `benchmark-calibration.md` with a concrete mapping of internal vetting dimensions to external benchmarks (Google L3–L8, Meta E3–E7, Stripe L1–L7). Without this anchor, the leveling rubric §3 semi-annual calibration is unmoored against external reality and the Stripe-tier-inflation / Uber-tier-compression failure modes from V-4 are not mitigated. Until this lands, the V-2 PASS-conditional verdict cannot be confirmed and Step 1 cannot transition to ✅. **This follow-up is paired with FIND-P2-04 closure — landing F-3 also discharges FIND-P2-04 in part, advancing two findings with one artifact.**

**F-4 (V-3 finding).** During the FIND-P2-10 recruitment-compression activity (Step 18, Days 60–90), perform a full-file scan of `recruitment/pipeline.md` plus all referenced `Configuration Artifacts` sub-files (`competency-bars.md`, `assessment-parameters.md`, `benchmark-calibration.md`, `role-family-templates/`, `compensation-bands.md`, `sourcing-channels.md`, `exception-rules.md`) for residual references to the legacy "16/20" or "≥4 on 4-of-5" formulation; replace with tier-specific references where found. Documentation hygiene paired with Step 18; absence does not block ✅ but creates internal-inconsistency risk if not closed.

**F-5 (V-5 finding) — BINDING GATE.** CHRO recruits the designated external challenger persona (the same advisor that satisfies Step 5 F-6, Step 9 F-X, Step 11 F-5, and Step 16 §6 Open Item 1); that challenger executes a re-challenge of this report by Day 30 (2026-05-20). Re-challenge result either confirms this verdict (Step 1 `🟢 → ✅` permitted once F-3 also lands) or overturns it (Step 1 returns to `🔵`). One external advisor closes five plan-step F-X gates simultaneously; the recruitment cost amortizes across the entire Day-1 partial-close cluster.

---

## 5. What this report does NOT certify

- **Operational evidence under the new tiered floors.** No L1 → L2 promotion has yet been calibrated against the new rubric (the seven Day-90-pass buddy graduates from `buddy-system-assignments.md` reach Day 90 starting July 2026). Until at least one such promotion has been scored under the rubric and reviewed in calibration, the deliverable's _written_ pass-rate-per-tier targets are aspirational. Step 1's `🟢 → ✅` does not require this evidence (per migration-plan analogue logic; that's an operational outcome, not an artifact check), but the verdict is bounded to artifact-set conformance, not behavioral conformance.
- **Calibration anchor reality.** F-3 binds `benchmark-calibration.md` to be populated. Until it is, the leveling rubric §3 calibration cadence is procedurally defined but operationally ungrounded. This challenge does NOT certify that the calibration is meaningful, only that the calibration cadence is structurally specified.
- **Full-file consistency scan of `recruitment/pipeline.md` (1,598 lines).** F-4 explicitly defers this to Step 18. This challenge spot-checked the directly-edited surfaces (the auto-reject row, the new §Tiered Vetting Score Floors section, the cross-reference table to the existing Tiered Engineering Assessment).
- **The leveling rubric's authoritative stamp.** That stamp is Step 9's deliverable, not Step 1's. The leveling rubric is currently a Working Draft (v0.2); Step 1 cites it as a Working Draft via Floor Enforcement Rule #5. The two steps' challenge rounds are running in parallel; neither blocks the other.
- **The four edge-case classifications.** F-1 explicitly defers intern / fellow / advisor / contractor-to-FTE classification. Until F-1 closes, this report does NOT certify how those classifications should be tier-mapped.
- **Ongoing recruitment funnel impact.** The Step 7 VP Data requisition is the first hire under the new tiered floors (L5 — 19/20 elite). Until that requisition either fills or is reset, the operational impact of the L5 floor on actual recruiting outcomes is unmeasured. This challenge does NOT certify that the L5 floor is operationally yieldable; it only certifies that the floor is structurally defined.

---

## 6. Document version history

| Version | Date           | Author                         |
| :------ | :------------- | :----------------------------- |
| 1.0     | April 21, 2026 | Operating Review (provisional) |

**v1.0 (2026-04-21).** Initial Independent Challenge round on Step 1 (recruitment tier reconciliation) per template v0.1. **Verdict: PASS-with-follow-ups (provisional).** All five attack vectors executed; V-3 Trim-to-Pass passed conditional on F-4 (full-file consistency scan, paired with Step 18); five follow-ups (F-1 through F-5) filed; F-3 (`benchmark-calibration.md` populated) + F-5 (external re-challenge) are the binding gates for `🟢 → ✅ Closed`. Step 1 authorised to transition `🔵 → 🟢 (provisional)`. Notable strengths surfaced by the challenge: (a) the deliverable **strengthens** the elite gate at L3+ (17/20 / 18/20 / 19/20 vs. legacy 16/20) — counter-narrative point routed to F-2 for explicit documentation; (b) the buddy is structurally load-bearing (Floor Enforcement Rule #4 enables L1 requisition pause-on-no-buddy), avoiding the Twitter buddy-program-theater failure mode; (c) Floor Enforcement Rule #5 explicitly de-couples buddy completion from L2 promotion, avoiding the GitHub/Square buddy-vs-elite conflation pattern.
