# CDO Stage 2 Prototype Review Checklist

> **Audit Condition 3 Remediation:** "CDO Stage 2 prototype review scheduled — I require a formal Stage 2 prototype review with the full creative team before advancing to Stage 3."
>
> **Status:** ✅ ADDRESSED — This checklist defines the formal Stage 2 prototype review process, participants, criteria, and sign-off requirements.
>
> **Author:** Yuki Tanaka-Chen (CDO)
>
> **Version:** 1.0
> **Date:** 2026-04-12
> **Review Status:** CDO-approved, ready for project use

---

## 1. Executive Summary

This document establishes the **CDO Stage 2 Prototype Review Checklist** — a formal gate review process that must be completed before any casual game project advances from Stage 2 (Design) to Stage 3 (Architecture). It was authored in direct response to a CDO audit finding that no formal Stage 2 prototype review process existed for the casual games studio.

### Purpose

- Ensure the **playable prototype, Game IDS, concept prototype, and playtest results** meet quality standards before engineering architecture begins
- Provide a **structured, repeatable review process** with clear pass/fail criteria
- Align the **full creative team** (Design, Art, Engineering, Writing) on a shared quality bar
- Create an **auditable record** of the review outcome for downstream stages

### Scope

This review covers all Stage 2 deliverables:

- Playable prototype (Unity greybox build)
- Game Interaction Design Specification (IDS)
- Concept prototype (Figma interactive flow)
- Tier 1 internal playtest report

### Pipeline Context

| Stage | Name         | This Review's Role                                 |
| ----- | ------------ | -------------------------------------------------- |
| 1     | Requirements | PRD + SRD completed — inputs to this review        |
| **2** | **Design**   | **This review is the Stage 2 gate**                |
| 3     | Architecture | Entry requires Stage 2 gate approval (this review) |

---

## 2. Review Participants

All participants must attend the full review session. Absenteeism requires a written proxy vote.

| Role                     | Name             | Review Responsibility                                                            |
| ------------------------ | ---------------- | -------------------------------------------------------------------------------- |
| **CDO (Review Chair)**   | Yuki Tanaka-Chen | Overall design quality, IDS conformance, platform-native patterns, accessibility |
| **Art Director**         | Renaud Leclercq  | Visual quality, art style consistency, VFX direction, promotional readiness      |
| **Lead Game Designer**   | Mei Watanabe     | Game feel, session design, progression, engagement hooks, gesture vocabulary     |
| **UI Visual Artist**     | Elena Morozova   | Component visual specs, layout, typography, iconography, responsive design       |
| **Motion/UI Animator**   | Marco Bellini    | Animation specs, timing, easing, juice, reduced-motion alternatives              |
| **Senior Game Engineer** | Dmitri Volkov    | Technical feasibility, performance budget, build stability, device compatibility |
| **UX Writer**            | Sarah Chen       | Copy tone-of-voice, localization readiness, microcopy clarity, error messaging   |

### Quorum

Minimum **5 of 7** participants must be present for the review to proceed. The CDO must always be present (no proxy for review chair).

---

## 3. Review Scope

### 3.1 Playable Prototype (Unity Greybox Build)

| Artifact         | Requirement                                                      |
| ---------------- | ---------------------------------------------------------------- |
| Build Platform   | `[iOS Simulator / Android Emulator / Physical Device]`           |
| Build Type       | Unity greybox (placeholder art, functional mechanics)            |
| Minimum Playable | Core gameplay loop functional from start to one complete session |
| Controls         | All planned gestures implemented and responsive                  |
| Performance      | Runs at ≥ 30fps on minimum-spec device                           |

### 3.2 Game IDS Template (Completeness and Conformance)

| Artifact              | Requirement                                         |
| --------------------- | --------------------------------------------------- |
| IDS Document          | Completed using `../design-guidelines.md` structure |
| Component Specs       | All planned UI components documented                |
| Animation Specs       | All planned animations documented                   |
| Platform Meta-UI      | iOS HIG / Material 3 patterns defined               |
| Accessibility         | WCAG 2.1 AA requirements specified                  |
| Conformance Checklist | ≥ 80% pass rate on IDS conformance checklist        |

### 3.3 Concept Prototype (Figma Interactive Flow)

| Artifact          | Requirement                                              |
| ----------------- | -------------------------------------------------------- |
| Figma File        | Interactive prototype with all user flows                |
| Flow Completeness | Onboarding, core gameplay, settings, store, leaderboards |
| Fidelity          | Mid-to-high fidelity (visual direction established)      |
| Annotations       | Interaction notes, edge cases, state transitions         |

### 3.4 Tier 1 Internal Playtest Report

| Artifact              | Requirement                                                                           |
| --------------------- | ------------------------------------------------------------------------------------- |
| Test Participants     | ≥ 5 internal testers (cross-department)                                               |
| Test Duration         | ≥ 15 minutes per participant                                                          |
| Metrics Collected     | Time-to-first-action, session length, failure retry rate, subjective enjoyment (1–10) |
| Findings Documented   | All P0/P1 issues identified, P2/P3 logged                                             |
| Iterate Before Review | P0/P1 issues from playtest must be resolved before this review                        |

---

## 4. Review Checklist

### 4.1 Game Feel (10 Items)

| #    | Item                                                                 | Pass | Fail | N/A | Notes |
| ---- | -------------------------------------------------------------------- | :--: | :--: | :-: | ----- |
| GF1  | Input latency ≤ 100ms from tap to on-screen response                 |      |      |     |       |
| GF2  | Animation timing feels responsive (not sluggish, not frantic)        |      |      |     |       |
| GF3  | Camera shake used appropriately (impact events, not overused)        |      |      |     |       |
| GF4  | Hit-stop / freeze frames communicate impact clearly                  |      |      |     |       |
| GF5  | Haptic choreography aligned with visual feedback                     |      |      |     |       |
| GF6  | Juice level appropriate for game genre (playtest rating ≥ 4/5)       |      |      |     |       |
| GF7  | Failure feel communicates clearly, feels fair, invites retry         |      |      |     |       |
| GF8  | Instant retry available (≤ 1 second from failure to restart)         |      |      |     |       |
| GF9  | Session loop has natural pause points and engagement hooks           |      |      |     |       |
| GF10 | Core engagement hooks validated by playtest (retention intent ≥ 70%) |      |      |     |       |

### 4.2 Visual Quality (10 Items)

| #    | Item                                                                | Pass | Fail | N/A | Notes |
| ---- | ------------------------------------------------------------------- | :--: | :--: | :-: | ----- |
| VQ1  | Art style consistent across all screens and elements                |      |      |     |       |
| VQ2  | Visual pillars (from PRD) reflected in prototype                    |      |      |     |       |
| VQ3  | Color palette cohesive, accessible (colorblind-safe)                |      |      |     |       |
| VQ4  | Typography hierarchy clear (heading > body > caption)               |      |      |     |       |
| VQ5  | Iconography consistent style, recognizable at target size           |      |      |     |       |
| VQ6  | VFX quality appropriate for game genre and performance budget       |      |      |     |       |
| VQ7  | Lighting model consistent (if applicable)                           |      |      |     |       |
| VQ8  | Post-processing effects enhance without overwhelming                |      |      |     |       |
| VQ9  | UI chrome (borders, backgrounds, dividers) polished and intentional |      |      |     |       |
| VQ10 | Promotional art direction established (store screenshot ready)      |      |      |     |       |

### 4.3 Interaction Design (10 Items)

| #    | Item                                                               | Pass | Fail | N/A | Notes |
| ---- | ------------------------------------------------------------------ | :--: | :--: | :-: | ----- |
| ID1  | IDS conformance: all documented specs implemented in prototype     |      |      |     |       |
| ID2  | Gesture vocabulary matches IDS (tap, long press, swipe, pinch)     |      |      |     |       |
| ID3  | Edge cases handled (offline, slow network, interrupted IAP)        |      |      |     |       |
| ID4  | Responsive breakpoints tested (phone, tablet, foldable if scope)   |      |      |     |       |
| ID5  | Platform-native meta-UI patterns followed (iOS HIG / Material 3)   |      |      |     |       |
| ID6  | Accessibility: colorblind mode functional                          |      |      |     |       |
| ID7  | Accessibility: motor accessibility (tap targets, alternatives)     |      |      |     |       |
| ID8  | Accessibility: cognitive accessibility (clear hierarchy, patterns) |      |      |     |       |
| ID9  | Accessibility: screen reader labels present, logical focus order   |      |      |     |       |
| ID10 | Reduced-motion alternatives functional                             |      |      |     |       |

### 4.4 Copy & Content (5 Items)

| #   | Item                                                                  | Pass | Fail | N/A | Notes |
| --- | --------------------------------------------------------------------- | :--: | :--: | :-: | ----- |
| CC1 | Tone-of-voice consistent across all screens                           |      |      |     |       |
| CC2 | Localization readiness: no hardcoded strings in UI                    |      |      |     |       |
| CC3 | Text expansion tolerance: UI accommodates +30% string length          |      |      |     |       |
| CC4 | Microcopy clear and action-oriented ("Play" not "Start Game Session") |      |      |     |       |
| CC5 | Error state messaging helpful and non-blaming                         |      |      |     |       |

### 4.5 Technical Feasibility (5 Items)

| #   | Item                                                                | Pass | Fail | N/A | Notes |
| --- | ------------------------------------------------------------------- | :--: | :--: | :-: | ----- |
| TF1 | Performance budget: ≥ 30fps minimum on minimum-spec device          |      |      |     |       |
| TF2 | Memory budget: ≤ 150MB RAM on minimum-spec device                   |      |      |     |       |
| TF3 | Asset pipeline readiness: placeholder-to-final art pipeline defined |      |      |     |       |
| TF4 | Build stability: no crashes during 15-minute play session           |      |      |     |       |
| TF5 | Device compatibility: tested on ≥ 2 device types (phone + tablet)   |      |      |     |       |

---

## 5. Pass/Fail Criteria

### 5.1 Scoring

| Metric                      | Threshold                                       |
| --------------------------- | ----------------------------------------------- |
| **Total Items**             | 40                                              |
| **PASS Rate Required**      | See determination table below                   |
| **Accessibility Items**     | All 5 (ID6–ID10) must Pass — no exceptions      |
| **"Not Implemented" Items** | Zero allowed for PASS; ≤ 3 for CONDITIONAL PASS |

### 5.2 Determination

| Result               | Criteria                                                                       | Action                                                                                              |
| -------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| **PASS**             | ≥ 90% pass rate (≥ 36/40), zero "Not Implemented", all accessibility Pass      | ✅ Advance to Stage 3 (Architecture)                                                                |
| **CONDITIONAL PASS** | 70–89% pass rate (28–35/40), ≤ 3 "Not Implemented", all accessibility Pass     | ⚠️ Advance to Stage 3 with written remediation plan; CDO reviews remediation within 5 business days |
| **FAIL**             | < 70% pass rate (< 28/40), OR any accessibility Fail, OR > 3 "Not Implemented" | 🛑 STOP — CTO notifies CPO; remediation required before Stage 3; re-review scheduled                |

### 5.3 Defect Classification

Items marked **Fail** are classified by severity before remediation:

| Level | Definition in Stage 2 Context                             | Action             |
| ----- | --------------------------------------------------------- | ------------------ |
| P0    | Core gameplay loop non-functional; crash; security gap    | Non-negotiable fix |
| P1    | Core feature broken; major UX failure; accessibility fail | Non-negotiable fix |
| P2    | Minor feature degraded; cosmetic issue                    | User decides       |
| P3    | Polish / nice-to-have                                     | User decides       |

---

## 6. Review Process

### 6.1 Pre-Review (48 Hours Before)

| Action                                      | Owner              | Deadline    |
| ------------------------------------------- | ------------------ | ----------- |
| Distribute prototype build (download link)  | CDO                | T-48 hours  |
| Distribute IDS document                     | CDO                | T-48 hours  |
| Distribute Figma prototype link             | CDO                | T-48 hours  |
| Distribute Tier 1 playtest report           | Lead Game Designer | T-48 hours  |
| Participants review materials independently | All participants   | T-48 to T-0 |
| Participants submit preliminary findings    | All participants   | T-24 hours  |
| CDO compiles review agenda from findings    | CDO                | T-12 hours  |

### 6.2 Review Session (4 Hours)

| Time Slot | Category                          | Lead               | Duration |
| --------- | --------------------------------- | ------------------ | -------- |
| 0:00–0:10 | Opening & context                 | CDO                | 10 min   |
| 0:10–1:10 | Game Feel walkthrough             | Lead Game Designer | 60 min   |
| 1:10–2:10 | Visual Quality walkthrough        | Art Director       | 60 min   |
| 2:10–2:40 | **Break**                         | —                  | 30 min   |
| 2:40–3:10 | Interaction Design walkthrough    | CDO                | 30 min   |
| 3:10–3:25 | Copy & Content walkthrough        | UX Writer          | 15 min   |
| 3:25–3:40 | Technical Feasibility walkthrough | Senior Engineer    | 15 min   |
| 3:40–4:00 | Scoring, decision, next steps     | CDO                | 20 min   |

### 6.3 Post-Review (Within 5 Business Days)

| Action                                        | Owner                         | Deadline          |
| --------------------------------------------- | ----------------------------- | ----------------- |
| Compile written review report with findings   | CDO                           | T+2 business days |
| Distribute report to all participants         | CDO                           | T+2 business days |
| If CONDITIONAL PASS: submit remediation plan  | Responsible owner per finding | T+5 business days |
| CDO reviews and approves remediation plan     | CDO                           | T+5 business days |
| If FAIL: schedule re-review after remediation | CDO + CPO                     | As needed         |

---

## 7. Sign-Off Table

All four mandatory signatories must approve for a PASS or CONDITIONAL PASS determination. **Any single FAIL vote triggers remediation.**

| Role                     | Name             | Vote (Pass / Fail) | Signature | Date | Notes |
| ------------------------ | ---------------- | :----------------: | --------- | ---- | ----- |
| **CDO (Chair)**          | Yuki Tanaka-Chen |                    |           |      |       |
| **Art Director**         | Renaud Leclercq  |                    |           |      |       |
| **Lead Game Designer**   | Mei Watanabe     |                    |           |      |       |
| **Senior Game Engineer** | Dmitri Volkov    |                    |           |      |       |

### Veto Rule

If **any single signatory votes FAIL**, the review outcome is **FAIL** regardless of overall pass rate. The vetoing party must document specific findings that justify the FAIL vote.

### Conditional Pass Sign-Off

For CONDITIONAL PASS outcomes, all signatories must additionally approve the remediation plan:

| Role                     | Name             | Remediation Plan Approved? | Signature | Date |
| ------------------------ | ---------------- | :------------------------: | --------- | ---- |
| **CDO**                  | Yuki Tanaka-Chen |                            |           |      |
| **Art Director**         | Renaud Leclercq  |                            |           |      |
| **Lead Game Designer**   | Mei Watanabe     |                            |           |      |
| **Senior Game Engineer** | Dmitri Volkov    |                            |           |      |

---

## 8. Review Report Template

After each review, the CDO produces a written report using this structure:

```markdown
# Stage 2 Prototype Review Report — [Game Title]

- **Date:** [YYYY-MM-DD]
- **Review Chair:** Yuki Tanaka-Chen (CDO)
- **Participants:** [List attendees and absentees]
- **Overall Result:** PASS / CONDITIONAL PASS / FAIL

## Summary

[Brief narrative of review outcome]

## Scoring

- Game Feel: [X]/10 Pass
- Visual Quality: [X]/10 Pass
- Interaction Design: [X]/10 Pass
- Copy & Content: [X]/5 Pass
- Technical Feasibility: [X]/5 Pass
- **Total:** [X]/40 ([X]%)

## Defects Found

| ID  | Category | Item | Severity | Description | Owner | Due Date |
| --- | -------- | ---- | -------- | ----------- | ----- | -------- |

## Remediation Plan (if CONDITIONAL PASS or FAIL)

[Detailed plan with owners, deadlines, and acceptance criteria]

## Sign-Off

[Signatures as above]
```

---

_Document End — CDO Stage 2 Prototype Review Checklist v1.0 — Studio Casual Games Design Department_
