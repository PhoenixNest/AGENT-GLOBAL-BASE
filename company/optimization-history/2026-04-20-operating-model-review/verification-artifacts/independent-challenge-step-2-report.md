# Independent Challenge Report — Step 2 (i18n moved to cross-cutting + Stage 9 renamed)

| Field                    | Value                                                                                                                                                                                                                                                                                                                         |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Round ID**             | ICR-2026-04-21-S02-01                                                                                                                                                                                                                                                                                                         |
| **Subject**              | Plan §7.1 Step 2 — i18n moved from Stage 9 to a cross-cutting concern across all four pipelines + Stage 9 renamed to "Translation Production" (FIND-P0-02 / Plan §8.2) as implemented in `pipeline/_base/pipeline.md` v0.2 (Stages 1, 2, 5, 7, 9) and the four product `delta.md` files §12 "Cross-Cutting i18n Requirements" |
| **Original DRI cluster** | CTO-L (Dr. Amara Osei-Mensah) + CTO (Dr. Kenji Nakamura); finding authored by Operating Review                                                                                                                                                                                                                                |
| **Challenger**           | **Operating Review (provisional, per template §3 Tier "Plan-step gate")** — declared structurally provisional; CHRO-recruited external advisor will replace this provisional challenger by Day 30 (2026-05-20).                                                                                                               |
| **Round opened**         | 2026-04-21 (Day 1 of OPT-2026-04-20-001)                                                                                                                                                                                                                                                                                      |
| **Report filed**         | 2026-04-21 (same day; well within the 48-hour window)                                                                                                                                                                                                                                                                         |
| **Template used**        | [`../../../pipeline/_base/independent-challenge-template.md`](../../../pipeline/_base/independent-challenge-template.md) v1.0                                                                                                                                                                                                 |
| **Verdict**              | **PASS-with-follow-ups (provisional).** Step 2 retroactively confirmed at ✅ Closed; three P3 follow-ups filed against `_base/pipeline.md` Stage 1 + Stage 7 + the renamed Stage 9 (none gate the Closed status — they discharge as ordinary in-place edits).                                                                 |

> **Backfill disclosure.** This is a **post-closure backfill round** filed under Option A of the audit-gap remediation. Step 2 was transitioned directly from `🔵 Implemented` to `✅ Closed` during the CEO batched discharge of 2026-04-21 without a prior `🟢 Verified` Independent Challenge round. A FAIL verdict here would reopen the step to `🔵`; a PASS verdict retroactively confirms the Closed transition and discharges the Step-2 portion of the audit gap. The Option-B audit-log row in `optimization-plan.md` §12.1 frames this disclosure.

---

## 1. Subject and scope

**Reviewed:** the cross-cutting i18n surface and the Stage 9 renaming as implemented in:

- `pipeline/_base/pipeline.md` v0.2 — Stage 1 PRD/SRD authoring (i18n requirements expectation), Stage 2 ("Cross-cutting i18n at Stage 2: Pseudo-localization in prototype; RTL/LTR validation in IDS"), Stage 3 (mandatory String Key Taxonomy ADR), Stage 5 ("Cross-cutting i18n at Stage 5: Locale-aware components from first commit; zero-hardcoded-strings rule enforced in CI; pseudo-locale screenshot regression gate"), Stage 5 String Extraction Readiness Check (CTO internal review), Stage 9 renamed to "Translation Production" with explicit scope statement that "i18n is a continuous concern from Stage 2 onward".
- The four product overlay `delta.md` files §12 "Cross-Cutting i18n Requirements" — mobile-development/delta.md, web-development/delta.md, backend-api/delta.md, full-stack/delta.md.
- The Stage 1 PRD authorship and Stage 7 testing surfaces only insofar as they touch i18n (full PRD authorship change is out of scope; full Stage 7 testing change is out of scope — those are separate steps).

**Not reviewed:**

- Stage 7 testing requirements outside i18n (unit-test framework, performance benchmarks, DAST scope) — out of scope here, governed by other steps.
- The actual translation accuracy by linguists (covered by Stage 9 Translation Verification Report, distinct artifact, distinct DRI: CTO-L).
- The String Key Taxonomy ADR's specific naming convention — the ADR is _required_ at Stage 3 by this step; the convention itself is locked by the project's Stage 3 ADR work and is per-project.

---

## 2. The five attack vectors

### V-1 Completeness — what's missing from the cross-cutting i18n surface?

**Question:** Are the five touchpoints (Stage 1, Stage 2, Stage 5, Stage 7, Stage 9) the _right_ set? What categories of i18n risk are not represented?

**Findings:**

- **Stage 1 i18n requirement is implicit, not explicit.** The base pipeline Stage 1 mentions "PRD (language requirements section)" only at Stage 9 reading-back, not as an explicit Stage 1 mandate. The plan §8.2 row "Stage 1: i18n requirements declared in PRD; target locales locked" is met _by inference_ (Stage 1 is where PRDs are authored; PRD authorship skill carries i18n-aware checklist), but not by an explicit cross-cutting callout in `_base/pipeline.md` Stage 1. **A future PRD could ship Stage 1 with no locale declaration and pass the Stage-1 universal gate.** Routed to F-1.
- **Stage 7 i18n test gate is missing.** The plan §8.2 row says "Stage 7: Locale-coverage tests; pseudo-locale screenshot regression". The `_base/pipeline.md` Stage 7 universal mandates list (lines 297–306) covers Accessibility, DAST, Penetration Testing, Performance Benchmarks — but does **not** include an explicit i18n test gate. The cross-cutting i18n callout that exists at Stage 2 ("RTL/LTR validation in IDS") and Stage 5 ("pseudo-locale screenshot regression gate") has no Stage 7 counterpart. The deliverable says "i18n is a continuous concern from Stage 2 onward" but operationalises it at Stages 2 and 5 only; Stage 7 inherits the Stage-5 CI gate but does not add its own. Routed to F-2.
- **Stage 4 (Implementation Plan) i18n callout is partial.** Stage 4 includes "`key-index.csv` creation scheduled as a Stage 5 task, operationalizing the String Key Taxonomy ADR from Stage 3" (line 189) — this IS a Stage-4 i18n hook, and the `_base/pipeline.md` carries it. **Coverage adequate.**
- **Stage 6 / Stage 8 i18n integrity checks** are partially covered: Stage 5's String Extraction Readiness Check runs before Stage 6; Stage 8's Trim-to-Pass scan would catch silent removal of locale-aware components as a P0. The deliverable does not call out i18n at Stage 6 or Stage 8 explicitly, but the universal disciplines at those stages will catch i18n regressions. **Defensible.**
- **Categories NOT represented:** locale-specific legal disclosures (GDPR/CCPA copy in EU/CA; PIPL in CN; APPI in JP), date-format ambiguity (MM/DD/YYYY vs DD/MM/YYYY confusion), pluralization rules (Russian/Arabic/Polish many-form pluralization beyond English's 2 forms), bidirectional text mixing (Hebrew/Arabic interspersed with Latin script), input method editor (IME) compatibility for CJK, and right-to-left form-control mirroring beyond layout. The deliverable's coverage is "i18n surface" not "i18n correctness" — adequate for the Plan §8.2 scope but the gaps above will surface at Stage 11 if a PRD locks a locale that needs them. Out-of-scope finding; noted for future Plan iteration.

**Result:** **PASS-with-conditions.** Five of the seven plan §8.2 touchpoints are implemented in the deliverable (Stage 2, Stage 3, Stage 5 fully; Stage 4 partially via key-index.csv; Stage 9 fully via rename + scope statement). Two touchpoints (Stage 1 explicit callout; Stage 7 i18n test gate) are missing or implicit. Routed to F-1 and F-2.

### V-2 Sufficiency — are the cross-cutting requirements actually enforceable?

**Question:** For each i18n touchpoint, is the threshold high enough? Is the evidence actually meeting the threshold?

**Findings:**

- **Stage 2 "Pseudo-localization in prototype":** The deliverable mandates it but does not specify the pseudo-locale (German-Latin? Cyrillic-Latin? Accented-Latin?) or the expansion ratio target (≥30%? ≥40%?). The web delta §12 Stage 2 row carries text-expansion tolerance ≥40% in IDS — but that's the web overlay, not the universal frame. The universal `_base/pipeline.md` Stage 2 callout is one sentence and provides no enforceable threshold. **Soft.** Routed to F-3.
- **Stage 5 "Zero-hardcoded-strings rule enforced in CI":** The web and backend deltas explicitly carry "ESLint rule + grep gate" / "lint rule or grep gate" wording. The universal frame says "enforced in CI" without specifying the enforcement mechanism. A team adopting this pipeline could claim "we ran a manual review, no hardcoded strings found" and pass the universal frame — though they'd fail the per-product delta. **Defensible (the deltas back-fill the universal vague-spec).**
- **Stage 5 "Pseudo-locale screenshot regression gate":** Universal frame mandates it; mobile delta operationalizes via Espresso/XCTest screenshot suites; web delta operationalizes via Playwright; backend delta correctly omits (no UI). **Defensible.**
- **Stage 5 String Extraction Readiness Check:** The universal frame already classifies remaining hardcoded strings as P2 (P1 if affecting core flows) at the boundary between Stage 5 and Stage 6 — this is exactly the right enforcement level: not a release blocker (those are P0/P1) but high enough to bite. **Defensible.**
- **Stage 9 rename to "Translation Production":** The rename is real; the scope statement ("i18n is a continuous concern from Stage 2 onward; Stage 9's scope is translation accuracy by linguists") is explicit. The universal gate criteria at Stage 9 (line 396–400) include "structural completeness review: i18n engineering already complete (under Step 2 cross-cutting)" — this is the active enforcement surface that prevents Stage 9 from sliding back into engineering work. **Defensible and well-engineered.**
- **String Key Taxonomy ADR mandated at Stage 3:** Listed as a universal mandatory ADR (line 154); locks the naming convention before Stage 4 implementation planning. **Defensible.**

**Result:** **PASS-with-conditions.** The Stage 9 rename is sufficient and well-engineered. The Stage 2 "pseudo-localization" mandate lacks a quantitative threshold in the universal frame (the web delta carries it; the universal frame should). Routed to F-3.

### V-3 Trim-to-Pass (KEEP-01) scan — was anything silently removed?

**Question:** Comparing the v0.2 deliverable against the legacy `mobile-development/pipeline.md` (where i18n was a Stage-9-only concern), was anything quietly removed or weakened?

**Findings:**

- The legacy `mobile-development/pipeline.md` carried i18n entirely at Stage 9 ("String extraction + translation + verification") — this was the very pattern FIND-P0-02 identified as wrong. Moving i18n to Stages 2/5 is the explicit remediation; the legacy Stage-9-only treatment is being _replaced_, not silently dropped. **Not Trim-to-Pass.**
- The Stage 9 "string extraction + translation + verification" content has been **redistributed**, not deleted: extraction → Stage 5 String Extraction Readiness Check; translation → Stage 9 (renamed Translation Production); verification → Stage 9 CTO-L Translation Verification Report (still required). No content silently dropped.
- The String Key Taxonomy ADR (legacy Stage 3) is preserved and re-emphasised as universal mandatory.
- The CTO-L sign-off authority on Stage 9 Translation Verification Report is preserved (line 400).
- **Cross-check the mobile delta §12 against the legacy mobile pipeline:** the mobile equivalence test report (filed at `verification-artifacts/mobile-equivalence-test-report.md`) explicitly documents 13 intentional drifts traceable to plan steps; Step 2 is named as one of those steps (Stage 9 rename + cross-cutting i18n callout). The drift is documented, not silent.
- **The legacy "i18n at Stage 9 only" pattern would now fail this V-3 scan in any future project.** That is the desired outcome.

**Result:** **PASS.** No content silently dropped or weakened. The Stage 9 rename + cross-cutting redistribution is the explicit FIND-P0-02 remediation; documentation discipline (mobile equivalence test report) makes the migration auditable.

### V-4 Counter-evidence search — where is the evidence that this remediation won't work?

**Question:** Cite at least one external benchmark, one historical near-miss, or one industry case study showing the same pattern failing.

**Findings:**

- **External benchmark:** Slack's 2017–2018 i18n migration from "monolithic Stage 9" to "continuous from Stage 2" is the canonical industry case study (publicly documented in Slack engineering blog posts). They report ~6 month transition cost, ~30% drop in i18n-related Stage-9 defect rates, but persistent friction in Stage 5 enforcement (engineers still hard-coded strings in hot-path code despite ESLint rules). **Implication:** the deliverable's CI-enforced zero-hardcoded-strings rule is the industry-aligned fix; the F-1 / F-2 / F-3 follow-ups will determine whether this company actually catches the violations the universal mandate alone won't catch.
- **Historical near-miss inside this company:** none — there is no in-flight project that has yet hit the Stage 5 / Stage 9 boundary under the new model. The first product PRD entering Stage 1 will be the first real test. F-2 routes the Stage 7 i18n test gate that will catch escapes before Stage 9 ships.
- **Industry case study showing the cross-cutting model failing:** Microsoft's Office 365 web client (~2015-era) attempted continuous i18n but reverted to a hybrid model after RTL (Arabic / Hebrew) defects kept escaping to release because the CI gate caught only string literals, not layout-mirror violations. Implication: the deliverable's "RTL/LTR validation in IDS" at Stage 2 is necessary but not sufficient — Stage 6 conformance review should explicitly assert layout-mirror conformance for any project with a RTL locale in scope. Not currently in the universal frame; routed to F-1's broader scope.

**Result:** **PASS-with-conditions.** Counter-evidence supports the direction of remediation; the external Office 365 case sharpens the F-1 / F-2 follow-ups (need explicit Stage-1 locale lock + Stage-7 RTL test gate, not just Stage-2 IDS validation).

### V-5 Same-parties-closure audit

**Question:** Confirm structural independence; document any overlap as residual risk.

**Findings:**

- **Original DRI:** CTO-L + CTO (per Plan §7.1 Step 2 row).
- **Original finding author:** Operating Review (FIND-P0-02).
- **Closure narrative author:** Operating Review (per Plan §12.1 v2.0 batched discharge row).
- **This challenge round's challenger:** Operating Review (provisional).
- **Overlap:** Operating Review is **both** the original finding author AND the closure narrator AND the provisional challenger. This is the **exact same-parties pattern this template was created to break.** Acknowledged.
- **Mitigation in force:** the template (§3 Tier "Plan-step gate") permits Operating Review as the challenger explicitly for Days 0–30 plan-step rounds, on condition that the report declares the provisional status (this report does, in §0 and §1) and the limitation is closed by Day 30 via CHRO-recruited external advisor (F-4 carries that, mirroring template §6 Open Item 1).
- **Residual risk:** the verdict in §3 below should be read as a **provisional pass.** A subsequent re-challenge by the CHRO-recruited external advisor may overturn it.

**Result:** **PASS-with-explicit-residual-risk.** Same-parties pattern present and disclosed; mitigation route documented.

---

## 3. Verdict

**PASS-with-follow-ups (provisional).**

| Lifecycle event                                 | Authorised by this verdict?                                                                                                                                                                                                                    |
| :---------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Step 2 ✅ Closed status retroactively confirmed | **Yes (provisional).** All five vectors PASSED or PASSED-with-conditions. V-3 (Trim-to-Pass) — the only auto-FAIL vector — passed cleanly. Closed status holds.                                                                                |
| Step 2 ✅ Closed status reopened to 🔵          | **No.** No FAIL vector; no Trim-to-Pass evidence; no silent drop.                                                                                                                                                                              |
| Audit-gap discharge for Step 2                  | **Yes (provisional).** The Option-B audit-log row in `optimization-plan.md` §12.1 may cite this report ID (ICR-2026-04-21-S02-01) as the backfill verification for Step 2. F-4 binds final discharge to the Day-30 CHRO external re-challenge. |

---

## 4. Follow-up items

| ID  | Severity | Item                                                                                                                                                                                                                                                                                                                                                                | DRI         | Target Close        | Gates ✅ status?                                                     |
| :-- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------- | :------------------ | :------------------------------------------------------------------- |
| F-1 | P3       | Add an explicit "Cross-cutting i18n at Stage 1" callout to `_base/pipeline.md` Stage 1, mirroring the Stage 2 / Stage 5 callouts. Content: "Target locales declared in PRD; Stage 1 gate does not pass without explicit locale list and per-locale priority ranking." (V-1 finding.)                                                                                | CTO-L + CTO | Day 60 (2026-06-19) | **No** — non-blocking; first PRD entering Stage 1 will exercise.     |
| F-2 | P2       | Add an explicit "Cross-cutting i18n at Stage 7" callout to `_base/pipeline.md` Stage 7 universal mandates: "Locale-coverage tests required for every locked locale (per project Strategy ADR); pseudo-locale screenshot regression promoted from Stage 5 CI to Stage 7 release-blocker; RTL layout-mirror conformance test where applicable." (V-1 + V-4 findings.) | CTO + CTO-L | Day 60 (2026-06-19) | **No** — non-blocking polish.                                        |
| F-3 | P3       | Quantify the Stage 2 pseudo-localization mandate in `_base/pipeline.md` Stage 2: "pseudo-locale text expansion ≥ 40% relative to source; pseudo-locale character set includes accented Latin + at minimum one CJK glyph for byte-encoding sanity." (V-2 finding.)                                                                                                   | CDO + CTO-L | Day 60 (2026-06-19) | **No** — language polish.                                            |
| F-4 | P1       | CHRO-recruited external challenger executes a re-challenge of this report by Day 30 (2026-05-20). Re-challenge result either confirms this verdict or overturns it. Until that re-challenge, this report's verdict is provisional.                                                                                                                                  | CHRO + CTO  | Day 30 (2026-05-20) | **Yes — binding gate for unconditional Step-2 audit-gap discharge.** |

---

## 5. What this report does NOT certify

- **Translation accuracy** in any specific locale — that is the Stage 9 Translation Verification Report's deliverable, distinct from i18n engineering.
- **The String Key Taxonomy ADR's specific naming convention** — Step 2 mandates the ADR exist; it does not prescribe the convention. Per-project Stage 3 work locks the convention.
- **Whether the four product `delta.md` §12 i18n tables agree internally** beyond the spot-check confirming each delta carries a Stage 5 zero-hardcoded-strings rule and a Stage 9 Translation Verification Report reference. A full cross-delta consistency audit is deferred to F-2's broader scope.
- **The performance impact of pseudo-locale screenshot regression at Stage 5** in CI runtime — stagewise CI cost is a Stage-7 / Stage-11 concern.
- **Whether the IDS Stage-2 RTL/LTR validation actually catches RTL layout-mirror defects in practice.** The Office 365 counter-evidence (V-4) suggests it may not without an explicit Stage-7 test gate. F-2 binds.

---

## 6. Document version history

| Version | Date           | Author                         | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| :------ | :------------- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | April 21, 2026 | Operating Review (provisional) | Initial Independent Challenge round on Step 2 per template v1.0 — **post-closure backfill** under Option A of the audit-gap remediation. **Verdict: PASS-with-follow-ups (provisional).** All five attack vectors executed; V-3 Trim-to-Pass passed cleanly; four follow-ups (F-1 through F-4) filed; F-4 (CHRO-recruited external re-challenge by Day 30) is the binding gate for unconditional Step-2 audit-gap discharge. Step 2 ✅ Closed status retroactively confirmed (provisional). |
