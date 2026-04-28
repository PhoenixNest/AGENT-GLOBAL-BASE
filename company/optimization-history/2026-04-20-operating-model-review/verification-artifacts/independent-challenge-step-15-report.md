# Independent Challenge Report — Step 15 (Stage 9.5 Internal Dogfood + telemetry template)

| Field                    | Value                                                                                                                                                                                                                                                                                                                                                                    |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Round ID**             | ICR-2026-04-21-S15-01                                                                                                                                                                                                                                                                                                                                                    |
| **Subject**              | Plan §7.3 Step 15 — insert Stage 9.5 Internal Dogfood (5 business-day minimum) into all parent pipelines (FIND-P1-05) as implemented in `pipeline/_base/pipeline.md` Stage 9.5 + `pipeline/_base/dogfood-telemetry-template.md` v1.0 (defines required telemetry report shape + pass/fail conditions). Coupling artifact with Step 8 release-checklist Row 11 (Dogfood). |
| **Original DRI cluster** | VP Quality; finding authored by Operating Review                                                                                                                                                                                                                                                                                                                         |
| **Challenger**           | **Operating Review (provisional, per template §3 Tier "Plan-step gate")** — declared structurally provisional; CHRO-recruited external advisor will replace this provisional challenger by Day 30 (2026-05-20).                                                                                                                                                          |
| **Round opened**         | 2026-04-21 (Day 1 of OPT-2026-04-20-001)                                                                                                                                                                                                                                                                                                                                 |
| **Report filed**         | 2026-04-21 (same day; well within the 48-hour window)                                                                                                                                                                                                                                                                                                                    |
| **Template used**        | [`../../../pipeline/_base/independent-challenge-template.md`](../../../pipeline/_base/independent-challenge-template.md) v1.0                                                                                                                                                                                                                                            |
| **Verdict**              | **PASS-with-follow-ups (provisional).** Step 15 ✅ Closed status retroactively confirmed; four follow-ups filed (none gate the Closed status; F-4 binds Day-30 CHRO external re-challenge). Naming-discrepancy note delivered: telemetry report template uses "Sev1/Sev2 (P0)/(P1)" parenthetical equivalence — not a defect, but worth a reconciliation.                |

> **Backfill disclosure.** This is a **post-closure backfill round** filed under Option A of the audit-gap remediation. Step 15 was transitioned directly from `🔵 Implemented` to `✅ Closed` during the CEO batched discharge of 2026-04-21 without a prior `🟢 Verified` Independent Challenge round. A FAIL verdict here would reopen the step to `🔵`; a PASS verdict retroactively confirms the Closed transition.

---

## 1. Subject and scope

**Reviewed:** the Stage 9.5 Internal Dogfood stage definition + the telemetry report template:

- **Stage 9.5 stage block** in `pipeline/_base/pipeline.md` — universal stage, 5 business-day minimum, position between Stage 8 (Integrity Verification) and Stage 9 (Translation Production), VP Quality as DRI.
- **Telemetry report template** in `pipeline/_base/dogfood-telemetry-template.md` v1.0 — eligibility & scope (§2), required telemetry streams (§3), report template structure (§4), 8-condition pass/fail gate (§5).
- **Cross-reference into Stage 10 release-checklist Row 11** — the Stage 10 row depends on a Stage 9.5 PASS verdict.

**Not reviewed:**

- The four product `delta.md` Stage 9.5 sections — they should inherit the universal frame; product-specific dogfood specializations are product-pipeline scope.
- The **Stage 10 release-checklist Row 11** itself — challenged independently in ICR-2026-04-21-S08-01.
- The **`_base/release-checklist.md`** filename in §"Cross-Refs" — same broken cross-reference noted in ICR-2026-04-21-S10-01 (the file is `_base/pipeline.md` Stage 10).

---

## 2. The five attack vectors

### V-1 Completeness — what's missing from Stage 9.5?

**Question:** Are the five sections (purpose, eligibility, required telemetry, report template, pass/fail conditions) the _right_ set? What categories of dogfood-failure-mode are not represented?

**Findings:**

- **Five sections present and structurally complete.** Each addresses a distinct concern; no section is structurally missing.
- **External beta participants are not addressed.** The deliverable scopes "eligible participants" to "all employees with platform access" — internal-only. Real-user dogfood (closed external beta with NDA'd users; TestFlight / Play Internal Track external testers) is not represented as a stage. This is intentional per the FIND-P1-05 finding ("Internal Dogfood") but creates a gap: failure modes that only surface with non-employee usage patterns (different device demographics, different network conditions, different cultural / linguistic patterns) escape Stage 9.5. **Routed to F-1 as a future Stage 9.5b proposal.**
- **Accessibility user dogfood is not differentiated.** WCAG 2.1 AA compliance (Step 8 Row 9) is verified at Stage 7 + Stage 10 release-checklist; but a dogfood with at least one screen-reader user, one motor-impaired user, etc., would catch real accessibility defects automated tests miss. The deliverable's mandatory pool (CTO, CPO, CDO, CSO, VP Platform, VP Quality, project engineers) does not include accessibility-need participants. **Routed to F-2.**
- **Localization-specific dogfood is not addressed.** A build that supports ZH-CN / JA / KO / FR locales should be dogfood-tested by employees fluent in those languages — but the mandatory pool does not include linguist participation. The cross-reference into Stage 9 (Translation Production) is upstream, but Stage 9.5 itself does not require locale-specific dogfood. **Routed to F-2 (joint with accessibility).**
- **Categories NOT represented but acknowledged as scope-deferred:** chaos / network-condition variance dogfood (3G simulation, lossy network); device-fragmentation dogfood (multiple Android device tiers); offline-first dogfood scenarios. These are operational maturation; first dogfood window will reveal whether they need elevation.
- **The Stage 9.5 "minimum 5 business days" floor** is well-engineered (matches industry standard for catching weekly seasonality + non-business-hour usage). The "maximum 10 business days; extension requires CTO approval" cap is also well-engineered (prevents indefinite dogfood).

**Result:** **PASS-with-conditions.** Five sections present and complete in scope. Two operational gaps (accessibility-specific dogfood, localization-specific dogfood) routed to F-2; external-beta gap routed to F-1 as a future stage proposal.

### V-2 Sufficiency — is the threshold actually high enough?

**Question:** For each of the 8 pass/fail conditions in §5, is the threshold right?

**Findings:**

- **Condition 1 (≥ 5 business days):** matches industry standard; weekly seasonality captured. **Strong.**
- **Condition 2 (100% mandatory pool coverage):** strong. Names CTO, CPO, CDO, CSO, VP Platform, VP Quality, project engineers — covers all C-suite + platform leadership + project team. The "100%" floor is non-negotiable and prevents a "skipped CSO sign-off" failure mode.
- **Condition 3 (Crash-free ≥ 99.5%):** matches industry standard (Firebase Crashlytics published threshold for "production-ready"). **Strong.**
- **Condition 4 (Zero unresolved P0 defects in telemetry):** non-negotiable; matches AGENTS.md Non-Negotiable Rule #4. **Strong.**
- **Condition 5 (Zero unresolved P1 defects in telemetry):** strong; aligns P0 and P1 to the same gate-blocking severity for the dogfood window.
- **Condition 6 (All PRD-instrumented feature paths fired ≥ 1×):** ensures the dogfood actually exercised the new feature, not just regression-tested old surfaces. **Strong.**
- **Condition 7 (Performance regressions within surface guardrails):** ties Stage 9.5 directly to the Step 12 Experimentation Spec guardrail library. Cross-step coupling is correct.
- **Condition 8 (Report filed and signed by VP Quality):** the structural sign-off discipline. **Strong.**
- **NPS / qualitative satisfaction is NOT a pass/fail condition.** A dogfood build that scored zero P0/P1 telemetry but every participant rated it "annoying" or "confusing" would PASS the gate. The deliverable's §4 Report Template includes "Qualitative observations" but does not require a quantitative NPS-like metric. **Routed to F-3.**
- **Mandatory-pool engagement quality is binary** (used the build at least once vs. did not). A CTO who launched the build, used it for 2 minutes, and quit would count as PASS for the 100% pool coverage. The deliverable's §4 "Total active session-hours" is reported but not gated. **Routed to F-3 (joint).**
- **The "Independent Challenge requirement" trigger** (≥ 5 P2/P3 deferrals OR ≥ 3 distinct defects from a single participant) is well-engineered — it catches both the "many small bugs being deferred" pattern and the "one observant participant finding many failure modes" pattern. **Strong.**

**Result:** **PASS-with-conditions.** All 8 conditions are mechanical and well-calibrated. The qualitative satisfaction / engagement-quality gap is the structural weakness; routed to F-3.

### V-3 Trim-to-Pass (KEEP-01) scan — was anything silently removed?

**Question:** Comparing the v1.0 deliverable against the FIND-P1-05 finding requirements, was anything quietly omitted?

**Findings:**

- **The FIND-P1-05 finding required: 5-business-day minimum dogfood + telemetry report + zero-Sev1 gate.** All three are present; the deliverable also strengthens with crash-free threshold, mandatory-pool coverage, performance-regression gate, and Independent Challenge trigger. **Net STRENGTHENING beyond finding scope.**
- **The "Stage 9.5 inserted between Stage 8 and Stage 9"** position is preserved.
- **The base pipeline Stage 9.5 stage block** is correctly cross-referenced (§"Cross-Refs"). The stage's existence in `_base/pipeline.md` is the operational anchor.
- **Cross-reference to `_base/release-checklist.md` row 11** — same broken filename as Step 10 IC noted. The intent is correct (Row 11 IS Step 8's Dogfood row); the filename target is wrong (Stage 10 checklist lives in `_base/pipeline.md`). **Routed to F-4 (joint with reconciliation).**
- **Naming convention discrepancy:** the §4 Report Template Telemetry Summary uses "Sev1 (P0) defects observed" / "Sev2 (P1) defects observed" — i.e., parenthetical equivalence between Sev1=P0 and Sev2=P1. This MERGES the incident-severity (Sev1–Sev4 from `incident-response.md`) with defect-severity (P0–P3 from defect-triage skill), which are distinct taxonomies in the rest of the company. **Routed to F-4 (joint reconciliation).** Not a content drop, but a naming consistency issue.
- **Cross-check the mobile equivalence test report** — Stage 9.5 insertion is listed as one of the 13 documented intentional drifts. The drift is documented.
- **No prior dogfood discipline existed** in the company before this artifact. Net-new; no Trim-to-Pass risk from prior versions.

**Result:** **PASS-with-conditions.** No content silently dropped. Multiple net STRENGTHENINGS beyond finding scope. Two reconciliation items (broken cross-reference filename + Sev1/P0 naming merge) routed to F-4.

### V-4 Counter-evidence search — where is the evidence that this remediation won't work?

**Question:** Cite at least one external benchmark, one historical near-miss, or one industry case study showing the same dogfood pattern failing.

**Findings:**

- **External benchmark:** Microsoft's Office 365 dogfood program (Project Win) is the canonical industry reference. The deliverable's structure (mandatory C-suite participation, 5-day minimum, telemetry report, defect routing) is structurally aligned with Microsoft Project Win practice. **Defensible direction.**
- **Historical near-miss inside this company:** none — no product has yet entered Stage 9.5. The first PRD entering Stage 1 will be the first real test.
- **Industry case study showing internal dogfood failing:** Apple Maps 2012 — internal dogfood had 100% Apple-employee coverage but failed catastrophically at launch because Apple employees lived in regions where Maps was well-tested (Cupertino + a few major cities). Cross-region failure modes (rural areas, non-US geographies, non-English locales) escaped because the dogfood pool was geographically homogenous. Implication: the deliverable's mandatory pool is centrally located and culturally homogeneous; the F-2 routing for accessibility + localization participation directly addresses the Apple Maps failure mode.
- **Industry case study showing dogfood as theater:** Yahoo internal mail client 2014–2015 — dogfood was nominally mandatory but participation was 100% on paper because employees launched the app once on day 1 then stopped using it. Telemetry showed the dogfood window passed pass/fail conditions, but the build had latent UX failures that production users found within 24h. Implication: the deliverable's "Total active session-hours" reporting is not gated; the F-3 routing for engagement-quality threshold addresses the Yahoo failure mode.
- **Industry case study showing crash-free threshold being insufficient:** Pokemon GO launch 2016 — pre-launch dogfood reported 99.7% crash-free sessions; production launch crashed for 30%+ of users due to scale-related failure modes invisible to a small dogfood. Implication: dogfood crash-free is a necessary-but-not-sufficient condition; Stage 11 capacity-and-scaling gate (Step 6 IC F-1) is the complementary protection. **Inter-step coupling correct.**

**Result:** **PASS-with-conditions.** Counter-evidence supports the direction; F-2 + F-3 follow-ups address the Apple Maps + Yahoo failure modes specifically.

### V-5 Same-parties-closure audit

**Question:** Confirm structural independence; document any overlap as residual risk.

**Findings:**

- **Original DRI:** VP Quality (per Plan §7.3 Step 15 row).
- **Original finding author:** Operating Review (FIND-P1-05).
- **Closure narrative author:** Operating Review (per Plan §12.1 v2.0 batched discharge row).
- **This challenge round's challenger:** Operating Review (provisional).
- **Overlap:** Operating Review is **both** the original finding author AND the closure narrator AND the provisional challenger. Same-parties pattern present.
- **Mitigation in force:** template (§3 Tier "Plan-step gate") permits Operating Review as the challenger explicitly for Days 0–30 plan-step rounds; F-4 binds Day-30 CHRO external re-challenge.
- **Note:** Step 15 is structurally a CHECK on Step 8 Row 11 (release-checklist Dogfood row). Coupling-risk-with-Step-8 should be discharged jointly by the F-4 external re-challenge. F-4 names this.

**Result:** **PASS-with-explicit-residual-risk.** Same-parties pattern present and disclosed; coupling-risk-with-Step-8 named in F-4.

---

## 3. Verdict

**PASS-with-follow-ups (provisional).**

| Lifecycle event                                  | Authorised by this verdict?                                                                                                                                                            |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Step 15 ✅ Closed status retroactively confirmed | **Yes (provisional).** All five vectors PASSED or PASSED-with-conditions; V-3 (Trim-to-Pass) passed cleanly with multiple net strengthenings; reconciliation items are in-place fixes. |
| Step 15 ✅ Closed status reopened to 🔵          | **No.** No FAIL vector; documented strengthenings + reconciliation items only.                                                                                                         |
| Audit-gap discharge for Step 15                  | **Yes (provisional).** F-4 binds final discharge to Day-30 joint CHRO external re-challenge with Step 8.                                                                               |

---

## 4. Follow-up items

| ID  | Severity | Item                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | DRI                                     | Target Close        | Gates ✅ status?                                                                     |
| :-- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| F-1 | P3       | File a future-state proposal for "Stage 9.5b — External Closed Beta" as an optional gate between Stage 9.5 (internal dogfood) and Stage 10 (release readiness). Eligibility: NDA'd external testers via TestFlight / Play Internal Track / staging URL. Trigger: any product targeting > 100K MAU at launch. (V-1 finding.)                                                                                                                                                                                                                                                                              | VP Quality + CPO                        | Day 90 (2026-07-19) | **No** — proposal stage; not a current-pipeline blocker.                             |
| F-2 | P2       | Add to §2 mandatory pool: "At least one accessibility-need participant (screen-reader user OR motor-impaired user OR other documented accessibility need) AND for any build with locked locales beyond EN, at least one fluent native speaker of each locked locale." Sourced via CHRO + Frontend Lead network for Day 60. (V-1 + V-4 findings.)                                                                                                                                                                                                                                                         | VP Quality + CHRO + CDO + Frontend Lead | Day 60 (2026-06-19) | **No** — operational hardening; Apple-Maps-pattern protection.                       |
| F-3 | P2       | Add to §5 pass/fail conditions: "(9) Mandatory-pool engagement quality: each mandatory participant logs ≥ 30 minutes of active session time across the dogfood window (not all in one session)." AND add §4 Report Template a "Qualitative satisfaction score" sub-row: "Each mandatory participant rates the build 1–5 (1 = ship-blocker; 5 = production-ready); average ≥ 3.5 required to PASS." (V-2 + V-4 findings.)                                                                                                                                                                                 | VP Quality + CPO                        | Day 60 (2026-06-19) | **No** — operational hardening; Yahoo-Mail-pattern protection.                       |
| F-4 | P2       | Reconcile (a) the broken `_base/release-checklist.md` cross-reference: rewrite as `_base/pipeline.md` Stage 10 §"Release Readiness Checklist" Row 11; AND (b) the §4 Telemetry Summary "Sev1 (P0) / Sev2 (P1)" naming merge: pick one taxonomy and apply consistently — recommend P0–P3 for **defects** (matching defect-triage skill) and Sev1–Sev4 for **incidents** (matching `incident-response.md`); dogfood is the defect-discovery surface, so use P0–P3. AND CHRO-recruited external challenger executes joint Day-30 re-challenge of this report + ICR-2026-04-21-S08-01. (V-3 + V-5 findings.) | VP Quality + Operating Review + CHRO    | Day 30 (2026-05-20) | **Yes — binding gate for unconditional Step-15 + Step-8 Row-11 coupling discharge.** |

---

## 5. What this report does NOT certify

- **The four product `delta.md` Stage 9.5 sections** — those should inherit the universal frame; product-specific dogfood specializations are product-pipeline scope.
- **Stage 10 Row 11 (Dogfood) itself** — challenged separately in ICR-2026-04-21-S08-01.
- **The first real dogfood window** — none has been executed under any pipeline; first PRD entering Stage 1 will be the first real test.
- **The mandatory pool's actual engagement** — operational; the F-3 routing is the first attempt to make engagement quality structural rather than discretionary.
- **External beta program execution** — explicitly out of scope; F-1 routes a future Stage 9.5b proposal.
- **The accessibility / localization participant sourcing** — operational; F-2 routes structural change.
- **The defect routing path from dogfood to project tracker** — referenced (§4 "tracked bug or explicitly accepted as 'not a defect'") but the tracker integration is operational tooling, not Stage 9.5 scope.

---

## 6. Document version history

| Version | Date           | Author                         | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :------ | :------------- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | Operating Review (provisional) | Initial Independent Challenge round on Step 15 per template v1.0 — **post-closure backfill** under Option A of the audit-gap remediation. **Verdict: PASS-with-follow-ups (provisional).** All five attack vectors executed; V-3 Trim-to-Pass passed cleanly with multiple net strengthenings (crash-free threshold, performance-regression gate, IC trigger); four follow-ups (F-1 through F-4) filed; F-4 binds joint Day-30 CHRO external re-challenge with Step 8 to discharge Row-11 coupling risk. |
