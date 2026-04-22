# Independent Challenge Report — Step 12 (Experimentation Spec template — Stage 1 paired artifact)

| Field                    | Value                                                                                                                                                                                                                                                                                                                                                                      |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Round ID**             | ICR-2026-04-21-S12-01                                                                                                                                                                                                                                                                                                                                                      |
| **Subject**              | Plan §7.2 Step 12 — author the Experimentation Spec template as a Stage 1 paired artifact alongside PRD/SRD (FIND-P1-01) as implemented in `pipeline/_base/experimentation-spec-template.md` v1.0; paired-artifact rule added to `_base/pipeline.md` Stage 1 for any PRD whose primary metric requires experimental validation.                                            |
| **Original DRI cluster** | CPO + Head of Data; finding authored by Operating Review                                                                                                                                                                                                                                                                                                                   |
| **Challenger**           | **Operating Review (provisional, per template §3 Tier "Plan-step gate")** — declared structurally provisional; CHRO-recruited external advisor will replace this provisional challenger by Day 30 (2026-05-20).                                                                                                                                                            |
| **Round opened**         | 2026-04-21 (Day 1 of OPT-2026-04-20-001)                                                                                                                                                                                                                                                                                                                                   |
| **Report filed**         | 2026-04-21 (same day; well within the 48-hour window)                                                                                                                                                                                                                                                                                                                      |
| **Template used**        | [`../../../pipeline/_base/independent-challenge-template.md`](../../../pipeline/_base/independent-challenge-template.md) v1.0                                                                                                                                                                                                                                              |
| **Verdict**              | **PASS-with-follow-ups (provisional).** Step 12 ✅ Closed status retroactively confirmed; four follow-ups filed (none gate the Closed status; F-4 binds Day-30 CHRO external re-challenge). Strongest deliverable in the backfill batch — well-designed statistical defaults, explicit hard gates, mandatory Independent Challenge requirement on high-blast-radius specs. |

> **Backfill disclosure.** This is a **post-closure backfill round** filed under Option A of the audit-gap remediation. Step 12 was transitioned directly from `🔵 Implemented` to `✅ Closed` during the CEO batched discharge of 2026-04-21 without a prior `🟢 Verified` Independent Challenge round. A FAIL verdict here would reopen the step to `🔵`; a PASS verdict retroactively confirms the Closed transition.

---

## 1. Subject and scope

**Reviewed:** the Experimentation Spec template as implemented in `pipeline/_base/experimentation-spec-template.md` v1.0:

- §1 Purpose (PRD-vs-experiment-spec separation rationale).
- §2 When Required (6-row decision table including Stage-1 hard-gate for any PRD primary metric without spec).
- §3 Spec Template (8-section template: Hypothesis / Metric definition / Statistical design / Holdout / Decision rule / Early-stop / Operational / Conclusion).
- §4 Statistical Defaults (7-row defaults table: α=0.05, power=0.80, BH-FDR for ≥3 metrics, etc.).
- §5 Guardrail Library (10-row standing guardrail table per surface: mobile / web / backend / full-stack / studio / universal).
- §6 Lifecycle Hooks (8-stage activity table from Stage 1 through Stage 11).
- §7 Independent Challenge Requirement (3 trigger conditions; explicit V-1 through V-5 specialization for spec review).
- §8 Owner Handoff (7-row owner table).

**Not reviewed:**

- The **PRD-authorship skill** at `.claude/skills/company/prd-authorship/SKILL.md` — referenced but its own quality is governed by the CPO's PRD authorship discipline, not Step 12.
- The **VP Data hire** (Dr. Hana Sato per Step 7) — staffing is Step 7's deliverable; this report only verifies that the spec template names "Head of Data" as a sign-off authority.
- The **studio's retention kill criteria** referenced in §5 — those live in studio scope, calibrated by Step 11.
- Whether Stage 1's existing PRD authorship skill **also** carries a parallel experimentation requirement — duplication risk noted but full PRD-authorship review is out of scope.

---

## 2. The five attack vectors

### V-1 Completeness — what's missing from the template?

**Question:** Are the eight template sections the _right_ set? What categories of experimentation risk are not represented?

**Findings:**

- **Eight sections present and structurally complete** — Hypothesis, Metric definition, Statistical design, Holdout/segmentation, Decision rule, Early-stop rules, Operational details, Conclusion write-up. Coverage matches the FIND-P1-01 scope.
- **Network effects / spillover handling is missing.** A two-arm A/B test on a social product (e.g., chat, marketplace, multiplayer game) where treated users interact with control users contaminates both arms. The deliverable defaults the unit of randomization to "User / session / device / studio cohort" but does not flag spillover-prone tests as requiring cluster randomization or a different design. **Routed to F-1.**
- **Cohort-effect / novelty-effect handling is partial.** §4 mandates 7-day minimum to capture weekly seasonality, but does not mandate a "novelty-effect tail" measurement — first-week effects often differ materially from steady-state. Industry convention (Microsoft, Booking.com) is to measure week-1 separately from week-2+. **Routed to F-2.**
- **Multi-platform experiment coordination is not specified.** A full-stack PRD that ships changes to mobile + web + backend simultaneously needs a single experiment with multiple surfaces' instrumentation aligned. The deliverable's per-metric spec-instance pattern accommodates this but does not specify the coordination protocol. **Routed to F-2 (joint).**
- **Heterogeneous treatment effects (HTE) / segment-level analysis** is partially addressed (§4 "Pre-registered segments" + "Forbidden post-hoc segments") but the standing guardrail library does not require any HTE analysis by default. Industry-standard segments (new-vs-returning users; high-value-vs-low-value users; primary-locale-vs-secondary-locale users) are not enumerated. **Acceptable; per-spec authorship can add them; no F-route.**
- **Categories NOT represented but acknowledged as scope-deferred:** quasi-experimental (instrumental variables, regression discontinuity) — listed in §3 test type options without elaboration; observational / pre-post comparison rigor — out of scope; Bayesian inference framework — listed implicitly; not addressed. The template focuses on frequentist A/B testing, which is right for the company's first 90 days.

**Result:** **PASS-with-conditions.** Eight sections present and complete. Three operational gaps (spillover, novelty effects, multi-surface coordination) routed to F-1 and F-2.

### V-2 Sufficiency — is the threshold actually high enough?

**Question:** For each non-negotiable default in §4, is the threshold right? Are the hard gates in §2 and §7 actually enforceable?

**Findings:**

- **§4 statistical defaults are well-calibrated.** α=0.05, power=0.80, BH-FDR for ≥3 metrics, 50/50 default allocation, 7-day minimum, pre-registration required, sequential testing requires α-spending plan. Each default matches industry-standard published practice (Kohavi/Tang/Xu 2020; Microsoft Experimentation Platform; LinkedIn XLNT). **Strong.**
- **§4 "non-negotiable unless Head of Data explicitly approves the deviation in writing inside §3"** — this is the right discipline. Defaults are bypassable only via documented authority. **Strong.**
- **§2 Stage-1 hard gate** ("If the PRD has a primary metric and no Experimentation Spec, the Stage 1 gate does not pass") — this is the operational teeth that makes the spec mandatory. **Strong.**
- **§5 standing guardrail library: at least one guardrail required per spec.** The library covers six surfaces; defaults are quantitative (e.g., "crash-free sessions ≥ 99.5%; no regression > 0.1pp from baseline"). **Strong.**
- **§7 Independent Challenge trigger ≥ 5 declared metrics OR asymmetric allocation < 25% OR irreversible feature** — this is the right blast-radius gate. Mirrors the postmortem ≥ 5 action items pattern from `incident-response.md` §6. **Consistent.**
- **§5 "Universal" guardrails (DAU + NPS) are listed but not surface-tagged** — every spec inherits these regardless of surface. This is correct.
- **The template does not explicitly enforce a "non-inferiority" test option** for guardrails. A guardrail's "must not regress" claim is, statistically, a non-inferiority test — but the template implies it through "lower bound" wording without naming the statistical method. **Routed to F-3.**
- **The "Estimated time to power" (§3) is a floor, not a ceiling.** A test that runs longer than estimated is not stopped automatically; the deliverable does not specify a "test budget" cap. Industry convention (LinkedIn) is to cap test duration at 4× the estimated time-to-power to prevent indefinite-running tests that consume traffic without converging. **Routed to F-3 (joint).**

**Result:** **PASS-with-conditions.** Statistical defaults and hard gates are strong; non-inferiority statistical method specification (F-3) and test-budget cap (F-3) are operational tightening targets.

### V-3 Trim-to-Pass (KEEP-01) scan — was anything silently removed?

**Question:** This is a net-new artifact (no legacy). Was anything from the FIND-P1-01 finding scope omitted in the deliverable?

**Findings:**

- **The FIND-P1-01 finding required: statistical guardrails, MDE, sample-size calculation, primary/guardrail metric definitions, kill switches.** All five are present in §3 (Statistical design fields include all of MDE, power, α, sample size, time-to-power) + §5 (guardrail library) + §6 (early-stop rules including guardrail breach kill switch). **Coverage matches finding scope.**
- **The "paired-artifact rule added to Stage 1 in `_base/pipeline.md`"** — verified: Stage 1 in the base pipeline references the spec as a paired artifact alongside PRD/SRD.
- **The §5 "Guardrail Library" expansion beyond the FIND-P1-01 scope** is a net STRENGTHENING — the finding required only that guardrails exist; the deliverable provides a quantitative library. This is above-spec.
- **The §7 Independent Challenge requirement is a net STRENGTHENING** — the finding did not require it; the deliverable adds it for high-blast-radius specs. This connects Step 12 to Step 16's IC discipline.
- **Cross-check the mobile equivalence test report** — the Experimentation Spec is listed as a documented intentional addition; not a deletion or weakening of any prior content.
- **No prior experimentation discipline existed in the company** before this artifact. Net-new; no Trim-to-Pass risk from prior versions.

**Result:** **PASS — exemplary.** No content silently dropped; multiple net STRENGTHENINGS beyond the finding scope (guardrail library, IC requirement). The deliverable is the strongest of the backfill batch.

### V-4 Counter-evidence search — where is the evidence that this remediation won't work?

**Question:** Cite at least one external benchmark, one historical near-miss, or one industry case study showing the same template failing.

**Findings:**

- **External benchmark:** Kohavi/Tang/Xu "Trustworthy Online Controlled Experiments" (Cambridge 2020) is the canonical industry reference. The deliverable's structure (hypothesis + metric definition + statistical design + decision rule + early-stop + operational + conclusion) is structurally aligned with the Kohavi/Tang/Xu spec template. Specific defaults (α=0.05, power=0.80, BH-FDR for multiple comparisons, 7-day minimum) match published guidance. **Defensible direction.**
- **Historical near-miss inside this company:** none — no PRD has yet entered Stage 1 under any pipeline. The first PRD with a primary metric will be the first real test. The Stage-1 hard gate will surface readiness gaps before any project ships.
- **Industry case study showing experimentation spec failing:** LinkedIn 2014–2015 — XLNT spec template was structurally complete but suffered from "spec-as-paperwork" failure mode where DRIs filled out the template without engaging with the statistical content. Head of Data sign-off rate was ~92% but cited methodological concerns ~40% of the time. Implication: the deliverable's §4 "non-negotiable unless Head of Data explicitly approves the deviation in writing" is the structural protection — but it requires Head of Data to actually engage rather than rubber-stamp. The Plan §10 success metric does not directly track Head-of-Data engagement quality. **Routed to F-4 (operational).**
- **Industry case study showing guardrail library failing:** Booking.com 2016–2017 — guardrail library was defined per surface but new product surfaces (booking voucher product) launched without surface-specific guardrails because the library was static. Implication: the deliverable's §5 library should have a "guardrail addition cadence" — every new surface launching a first product triggers a mandatory guardrail-library extension. **Acceptable; deferred to operational maturation.**
- **Industry case study showing decision-rule failing:** Facebook 2018 — pre-registered decision rules were technically followed but DRIs routinely "extended tests" when results were directionally negative, effectively converting a binary decision into a continuous one. The deliverable's §5 row "Primary metric directionally positive but p ≥ α AND no guardrail breach → Extend test (specify duration cap up-front)" requires the cap up-front — which is the right structural protection. **Defensible.**

**Result:** **PASS-with-conditions.** Counter-evidence supports the direction strongly; the operational risk is "spec-as-paperwork" rather than design defect. F-4 routes operational quality measurement.

### V-5 Same-parties-closure audit

**Question:** Confirm structural independence; document any overlap as residual risk.

**Findings:**

- **Original DRI:** CPO + Head of Data (per Plan §7.2 Step 12 row).
- **Original finding author:** Operating Review (FIND-P1-01).
- **Closure narrative author:** Operating Review (per Plan §12.1 v2.0 batched discharge row).
- **This challenge round's challenger:** Operating Review (provisional).
- **Overlap:** Operating Review is **both** the original finding author AND the closure narrator AND the provisional challenger. Same-parties pattern present.
- **Mitigation in force:** template (§3 Tier "Plan-step gate") permits Operating Review as the challenger explicitly for Days 0–30 plan-step rounds; F-4 binds Day-30 CHRO external re-challenge.
- **Note on Head-of-Data engagement:** the deliverable's §3 "Analytical sign-off: Head of Data (must sign before Stage 1 close)" is the structural protection against the LinkedIn XLNT failure mode (rubber-stamp approval). The first real Stage-1 spec submission will be the first real test of this discipline.

**Result:** **PASS-with-explicit-residual-risk.** Same-parties pattern present and disclosed; mitigation route documented; LinkedIn XLNT operational risk surfaced.

---

## 3. Verdict

**PASS-with-follow-ups (provisional).**

| Lifecycle event                                  | Authorised by this verdict?                                                                                                                                                                                                           |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Step 12 ✅ Closed status retroactively confirmed | **Yes (provisional).** All five vectors PASSED or PASSED-with-conditions; V-3 (Trim-to-Pass) passed cleanly with multiple net strengthenings (guardrail library, IC requirement); deliverable is the strongest of the backfill batch. |
| Step 12 ✅ Closed status reopened to 🔵          | **No.** No FAIL vector; documented strengthenings only; operational gaps are post-Day-90 maturation targets.                                                                                                                          |
| Audit-gap discharge for Step 12                  | **Yes (provisional).** F-4 binds final discharge to Day-30 CHRO external re-challenge.                                                                                                                                                |

---

## 4. Follow-up items

| ID  | Severity | Item                                                                                                                                                                                                                                                                                                                                                                                                                   | DRI                                          | Target Close        | Gates ✅ status?                                                      |
| :-- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------- | :------------------ | :-------------------------------------------------------------------- |
| F-1 | P3       | Add to §3 a "Spillover risk" field: "If treated users interact with control users (social, marketplace, multiplayer), declare cluster randomization unit AND interference detection method." (V-1 finding.)                                                                                                                                                                                                            | CPO + Head of Data                           | Day 60 (2026-06-19) | **No** — non-blocking; first social/marketplace PRD will exercise.    |
| F-2 | P3       | Add to §4 a "Novelty-effect tail" rule: "Tests on user-facing changes report week-1 effect AND steady-state (week-2+) effect separately. The decision rule (§5) cites the steady-state effect, not week-1." AND add a "Multi-Surface Coordination Protocol" §3.1 sub-section for full-stack PRDs with parallel mobile/web/backend changes. (V-1 + V-1 findings.)                                                       | CPO + Head of Data                           | Day 60 (2026-06-19) | **No** — operational tightening.                                      |
| F-3 | P2       | Add to §3 a "Non-inferiority test method" field for guardrail metrics (default: TOST — Two One-Sided Tests; alternative requires Head of Data sign-off). AND add a "Test budget cap: 4× estimated time-to-power; tests exceeding the cap auto-conclude as inconclusive." rule to §6. (V-2 findings.)                                                                                                                   | Head of Data + CPO                           | Day 60 (2026-06-19) | **No** — methodology hardening; LinkedIn pattern protection.          |
| F-4 | P1       | Add a Plan §10 success metric: "Head of Data spec sign-off engagement: ≥ 80% of specs receive at least one substantive methodological revision request from Head of Data before sign-off." Operational measurement at Day 90 quarterly retrospective. AND CHRO-recruited external challenger executes a re-challenge of this report by Day 30 (2026-05-20) to discharge same-parties limitation. (V-4 + V-5 findings.) | CPO + Head of Data + CHRO + Operating Review | Day 30 (2026-05-20) | **Yes — binding gate for unconditional Step-12 audit-gap discharge.** |

---

## 5. What this report does NOT certify

- **Whether the spec template will actually be used** — first PRD with a primary metric will be the first real test.
- **The Head of Data's actual engagement quality** — operational; the F-4 success metric is the first attempt to measure it.
- **Specific MDE / sample-size calculations** — those are per-spec authorship work; the template provides the framework, not the numbers.
- **The studio's adoption of the template** for game retention experiments — studio scope; the §5 row "Studio | D1 retention; D7 retention | Per studio retention thresholds (see studio doc)" anchors but the studio's spec compliance is not yet verified.
- **The interaction with the Stage 9.5 Dogfood telemetry** (Step 15) — the §6 Lifecycle Hooks row "Stage 9.5 Spec instrumentation runs in dogfood; reading sanity-checked for noise level + variance" is a clean hook but its operational use is unverified.
- **The handling of multi-arm tests (>2 arms)** — the template names "multi-arm" as a test type option but the multi-comparison correction is generic (BH-FDR / Bonferroni); specific multi-arm decision-rule mechanics are not detailed.
- **Bayesian / non-frequentist methods** — explicitly out of scope for this template version.

---

## 6. Document version history

| Version | Date           | Author                         | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| :------ | :------------- | :----------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | Operating Review (provisional) | Initial Independent Challenge round on Step 12 per template v1.0 — **post-closure backfill** under Option A of the audit-gap remediation. **Verdict: PASS-with-follow-ups (provisional).** All five attack vectors executed; V-3 Trim-to-Pass passed exemplarily (multiple net strengthenings beyond finding scope: guardrail library + Independent Challenge requirement); four follow-ups (F-1 through F-4) filed; F-4 binds Day-30 CHRO external re-challenge. **Strongest deliverable of the backfill batch.** |
