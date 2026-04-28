# Accessibility Ownership Assignment

**Document Type:** Studio Accessibility Ownership & Compliance Plan
**Studio:** Casual Games
**Author:** Yuki Tanaka-Chen, Chief Design Officer
**Date:** April 12, 2026
**Status:** APPROVED — CDO + CSO audit conditions satisfied
**Audit References:** CDO Finding #9 (Accessibility Compliance Capability), CSO Finding #9 (Accessibility ownership gap — see CDO audit Item 9 cross-reference)

---

## 1. Executive Summary

### 1.1 Audit Finding

The CDO Design Audit (Item 9: Accessibility Compliance Capability) and the CSO Security Audit (cross-referenced in Item 9: Screen reader support gap) identified a **significant structural gap** in the Casual Games Studio:

> **No single person owns accessibility as a primary responsibility.** Capabilities are distributed across team members (UI Visual Artist for colorblind mode, Motion/UI Animator for reduced-motion, Lead Game Designer for cognitive controls) but are not centralized, documented, or enforced through a formal ownership chain.

Specific sub-gaps identified:

| Sub-Gap                                     | Severity | Audit Source   |
| ------------------------------------------- | -------- | -------------- |
| Screen reader support (VoiceOver/TalkBack)  | **P0**   | CDO Finding #9 |
| WCAG 2.1 AA compliance auditing             | **P0**   | CDO Finding #9 |
| Colorblind mode implementation ownership    | P1       | CDO Finding #9 |
| Motor accessibility (tap targets, one-hand) | P1       | CDO Finding #9 |
| Cognitive load controls ownership           | P1       | CDO Finding #9 |
| Reduced-motion preference compliance        | P1       | CDO Finding #9 |
| Visual indicators for audio cues            | P1       | CDO Finding #9 |

The CDO audit condition C1 requires: _"Accessibility ownership assigned — By Stage 0 start, explicitly assign accessibility compliance responsibility to a named team member."_

This document satisfies that condition by assigning explicit ownership, defining concrete deliverables, establishing acceptance criteria for Stage 2 prototype review, and creating a timeline from Stage 0 through Stage 8.

### 1.2 Resolution Summary

Two internal team members are assigned accessibility ownership, with oversight from the parent company CDO and an external consultant engagement planned before soft launch:

- **Elena Morozova** (UI Visual Artist) — Visual/UI accessibility, WCAG 2.1 AA auditing
- **Marco Bellini** (Motion/UI Animator) — Motion accessibility, reduced-motion compliance, IDS animation spec review

Both individuals scored **5/5 on Standards Signal** in their vetting assessments, confirming they have the quality discipline required for compliance work.

---

## 2. Assigned Owners

### 2.1 Elena Morozova — Visual/UI Accessibility & WCAG 2.1 AA Auditor

| Attribute         | Detail                             |
| ----------------- | ---------------------------------- |
| **Name**          | Elena Morozova                     |
| **Role**          | UI Visual Artist (Senior)          |
| **Reports To**    | Renaud Leclercq (Art Director)     |
| **Accessibility** | Visual/UI Accessibility Owner      |
| **Scope**         | All Tier 1 (Meta-UI) accessibility |
| **Vetting**       | 17/20, 5/5 Standards Signal        |

**Rationale for assignment:**

Elena's background makes her the strongest candidate for visual accessibility ownership:

- **RISD-trained** (BFA Graphic Design, Rhode Island School of Design) — same institution as the CDO, indicating strong foundational design education including accessibility principles
- **Design-system thinking** — Built reusable UI component library at King (30% production time reduction), demonstrating the systematic mindset required for accessibility auditing
- **Button state design expertise** — Expert in multi-state visual design (normal, pressed, disabled, locked), directly applicable to focus indicator and contrast compliance
- **Mobile UI optimization** — Strong knowledge of texture atlasing, 9-slice scaling, and asset compression — accessibility-compliant UI must still meet performance budgets
- **5/5 Standards Signal** — Highest possible score on quality standards discipline

**Known gap and mitigation:**

Elena has not formally been trained in WCAG 2.1 AA auditing. This is addressed by:

1. CDO providing WCAG 2.1 AA auditing training and checklists during Stage 0
2. Automated contrast checking tools integrated into the asset pipeline (see Section 5)
3. External accessibility consultant review before soft launch (Section 5)

---

### 2.2 Marco Bellini — Motion Accessibility & IDS Animation Spec Compliance

| Attribute         | Detail                                                   |
| ----------------- | -------------------------------------------------------- |
| **Name**          | Marco Bellini                                            |
| **Role**          | Motion/UI Animator (Senior)                              |
| **Reports To**    | Renaud Leclercq (Art Director)                           |
| **Accessibility** | Motion Accessibility Owner                               |
| **Scope**         | Animation specs, reduced-motion, game feel accessibility |
| **Vetting**       | 17/20, 5/5 Standards Signal                              |

**Rationale for assignment:**

Marco is the natural owner for motion accessibility:

- **Reduced-motion preference already built into his workflow** — His `animation-specs.md` skill explicitly includes accessibility notes fields and "Respect reduced-motion preference" as a built-in spec requirement
- **IDS-equivalent documentation capability** — His spec format (animation name, duration, easing curve, states, keyframes, performance budget, low-end fallback, accessibility notes) is functionally equivalent to the CDO's IDS format
- **60fps performance awareness** — Designs animations that maintain frame rate targets through frame budgeting and LOD animation — accessibility includes performance accessibility for low-end devices
- **300+ UI transition animations** at Supercell — Deep experience with the exact animation types that need reduced-motion alternatives
- **5/5 Standards Signal** — Highest possible score on quality standards discipline

**Known gap and mitigation:**

Marco is primarily a 2D/UI animator with limited 3D animation experience. For gameplay animations (3D character movement, VFX timing), he will collaborate with the Technical Artist (Lena Kovac) and VFX Artist (Javier Moreno) to ensure reduced-motion alternatives extend to gameplay effects.

---

### 2.3 Supporting Contributors (Not Owners)

The following team members have accessibility-relevant responsibilities but are **not** primary owners. They execute tasks assigned by Elena or Marco:

| Team Member   | Role               | Accessibility Contribution                            | Reports To (for accessibility) |
| ------------- | ------------------ | ----------------------------------------------------- | ------------------------------ |
| Lena Kovac    | Technical Artist   | Shader-based colorblind mode implementation           | Elena Morozova                 |
| Javier Moreno | VFX Artist         | Visual indicators for audio cues (VFX layer)          | Marco Bellini                  |
| Mei Watanabe  | Lead Game Designer | One-hand mode design, cognitive load game mechanics   | Elena Morozova (coordination)  |
| Sarah Chen    | UX Writer          | Clear language, localization-ready accessibility copy | Elena Morozova                 |
| Kenji Yamada  | Audio Designer     | Audio-visual sync, haptic alternatives                | Marco Bellini                  |

---

## 3. Specific Responsibilities & Deliverables

### 3.1 Elena Morozova — Visual/UI Accessibility

| #   | Responsibility                                                                                                                    | Deliverable                                                   | Due By      | Standard                                          |
| --- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ----------- | ------------------------------------------------- |
| E1  | **WCAG 2.1 AA contrast audit** — All text ≥ 4.5:1, all UI elements ≥ 3:1                                                          | `contrast-audit-report.md` per build                          | Every build | WCAG 2.1 AA 1.4.3, 1.4.11                         |
| E2  | **Colorblind mode design** — 3 presets (Deuteranopia, Protanopia, Tritanopia) with shifted game-critical color palettes           | `colorblind-palette-spec.md` + visual mockups                 | Stage 2     | Game Accessibility Guidelines §3.1                |
| E3  | **Tap target compliance** — All interactive elements ≥ 44×44pt (iOS) / ≥ 48×48dp (Android) with ≥ 8pt spacing                     | `tap-target-audit.md` with annotated screenshots              | Stage 2     | iOS HIG, Material Design                          |
| E4  | **Focus indicator design** — Visible focus ring on all interactive meta-UI elements                                               | Focus indicator style guide + implementation notes            | Stage 2     | WCAG 2.1 AA 2.4.7                                 |
| E5  | **Screen reader accessibility labels** — All meta-UI elements have meaningful VoiceOver/TalkBack labels                           | `accessibility-labels.csv` (string key, label text, platform) | Stage 2     | iOS UIAccessibility, Android ContentDescription   |
| E6  | **Text scaling support** — UI layout tested at 200% text enlargement via Unity TextMeshPro dynamic sizing                         | `text-scaling-test-report.md` with screenshots                | Stage 3     | WCAG 2.1 AA 1.4.4                                 |
| E7  | **High contrast mode** — Alternative color scheme with maximum contrast between game elements                                     | `high-contrast-spec.md` + visual mockups                      | Stage 3     | Game Accessibility Guidelines §3.1                |
| E8  | **Accessibility settings UI** — Design settings screen with toggles for colorblind mode, reduced motion, text size, high contrast | Settings screen mockups + IDS spec                            | Stage 2     | Platform-native (iOS HIG / Material)              |
| E9  | **Automated contrast tooling** — Integrate contrast checker into asset pipeline (CI gate)                                         | Pipeline configuration + tooling documentation                | Stage 4     | Automated, fails build on violation               |
| E10 | **Accessibility regression checklist** — Per-release accessibility verification checklist                                         | `accessibility-release-checklist.md`                          | Stage 5     | Based on §5.2 of game-accessibility-guidelines.md |

### 3.2 Marco Bellini — Motion Accessibility

| #   | Responsibility                                                                                                                                                                           | Deliverable                                            | Due By  | Standard                                 |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------- | ---------------------------------------- |
| M1  | **Reduced-motion preference detection** — Game detects and respects OS-level Reduce Motion setting (iOS UIAccessibilityReduceMotion, Android Settings.System.TRANSITION_ANIMATION_SCALE) | `reduced-motion-implementation-spec.md`                | Stage 2 | iOS HIG, Android accessibility           |
| M2  | **Animation alternative specs** — Every animation in the GDS Package has a reduced-motion alternative (fade-only, instant transition, or disabled)                                       | `animation-alternatives-matrix.md`                     | Stage 2 | IDS conformance                          |
| M3  | **IDS animation spec compliance** — All animation specs include accessibility notes field (reduced-motion behavior, seizure risk assessment, duration limits)                            | Updated `animation-specs.md` template with a11y fields | Stage 1 | CDO IDS format                           |
| M4  | **Seizure-safe animation** — No animation exceeds 3 flashes per second; no full-screen flashing effects                                                                                  | `seizure-safety-audit.md`                              | Stage 2 | WCAG 2.1 AA 2.3.1                        |
| M5  | **Performance accessibility** — Animation LOD system ensures 60fps on low-end devices (graceful degradation: fewer particles, shorter duration, simpler easing)                          | `animation-performance-spec.md` with device tiers      | Stage 3 | 60fps target, Mali-G57 baseline          |
| M6  | **Haptic alternative design** — Haptic feedback patterns as substitute for audio cues (deaf/hard-of-hearing players)                                                                     | `haptic-patterns-spec.md`                              | Stage 3 | iOS CoreHaptics, Android VibrationEffect |
| M7  | **VFX reduced-motion coordination** — Work with VFX Artist (Javier Moreno) to ensure combat VFX and particle effects have reduced-motion variants                                        | `vfx-reduced-motion-spec.md`                           | Stage 3 | Game Accessibility Guidelines §3.4       |
| M8  | **Animation duration tokens** — Define duration tokens in design system with accessibility-aware limits (min 100ms, max 500ms for UI transitions)                                        | `duration-tokens.md` in design system                  | Stage 1 | WCAG 2.1 AA 2.2.1 (timing)               |

### 3.3 Cross-Owner Responsibilities

| #   | Responsibility                                                                                               | Primary Owner | Supporting Owner   | Deliverable                         | Due By     |
| --- | ------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | ----------------------------------- | ---------- |
| X1  | **Accessibility acceptance criteria for Stage 2**                                                            | Elena + Marco | CDO (review)       | `stage2-accessibility-checklist.md` | Stage 2    |
| X2  | **Accessibility SBOM** — Inventory of all accessibility implementations, tools, and third-party dependencies | Elena         | Marco              | `accessibility-sbom.md`             | Stage 3    |
| X3  | **One-hand mode validation** — Verify all core gameplay completable with single thumb                        | Marco         | Mei Watanabe       | `one-hand-mode-test-report.md`      | Stage 3    |
| X4  | **Accessibility playtest coordination** — Coordinate with playtest participants who use assistive technology | Elena         | Producer (James)   | `accessibility-playtest-report.md`  | Stage 3, 5 |
| X5  | **Accessibility gate review** — Present accessibility status at each stage gate                              | Elena + Marco | CDO (panel member) | Gate review presentation + sign-off | Each stage |

---

## 4. Accessibility Acceptance Criteria — Stage 2 Prototype Review

The following criteria **must be met** before the Stage 2 prototype can advance to gate review. These are in addition to the standard Stage 2 gate criteria (D1 ≥ 25%, session ≥ 5 min, fun validation ≥ 40%).

### 4.1 Tier 1: Meta-UI (WCAG 2.1 AA) — Mandatory

| #   | Criterion                                                          | Pass Condition                                            | Verified By        |
| --- | ------------------------------------------------------------------ | --------------------------------------------------------- | ------------------ |
| A1  | All text meets ≥ 4.5:1 contrast ratio on all backgrounds           | Automated scan returns zero violations                    | Elena + tooling    |
| A2  | All UI elements meet ≥ 3:1 contrast ratio against adjacent colors  | Automated scan returns zero violations                    | Elena + tooling    |
| A3  | All interactive elements meet minimum tap target size              | iOS: ≥ 44×44pt; Android: ≥ 48×48dp; spacing ≥ 8pt         | Elena              |
| A4  | Focus indicators visible on all interactive elements               | Tab/focus navigation shows clear visual ring              | Elena              |
| A5  | All meta-UI elements have accessibility labels                     | VoiceOver (iOS) and TalkBack (Android) read all elements  | Elena + emulator   |
| A6  | Reduced-motion preference is detected and respected                | OS-level setting disables non-essential animations        | Marco              |
| A7  | No animation exceeds 3 flashes per second                          | Frame-by-frame analysis of all animations                 | Marco              |
| A8  | Colorblind mode (3 presets) functional in prototype                | Deuteranopia, Protanopia, Tritanopia toggles work         | Elena + Lena Kovac |
| A9  | Accessibility settings screen designed and included in prototype   | Settings UI mockup with all accessibility toggles         | Elena              |
| A10 | IDS animation specs include accessibility notes for all animations | Every animation spec has reduced-motion alternative noted | Marco              |

### 4.2 Tier 2: Gameplay — Target (Strive for, not gate-blocking at Stage 2)

| #   | Criterion                                              | Pass Condition                                     | Verified By          |
| --- | ------------------------------------------------------ | -------------------------------------------------- | -------------------- |
| G1  | Core gameplay completable with one hand                | Single-thumb playtest completes one game loop      | Marco + Mei Watanabe |
| G2  | Visual indicators present for all audio cues           | Every sound effect has a visual counterpart        | Marco + Javier       |
| G3  | Pause works in all game states                         | Pause button functional during all gameplay phases | Marco                |
| G4  | Clear objective display visible on screen              | Current goal readable at all times                 | Elena + Mei Watanabe |
| G5  | Separate volume controls (music/SFX/voice) in settings | Three independent sliders functional               | Elena                |

### 4.3 Stage 2 Accessibility Sign-Off

| Role                       | Sign-Off | Date | Notes |
| -------------------------- | -------- | ---- | ----- |
| Elena Morozova (Owner)     | ☐        |      |       |
| Marco Bellini (Owner)      | ☐        |      |       |
| Renaud Leclercq (Art Dir.) | ☐        |      |       |
| Yuki Tanaka-Chen (CDO)     | ☐        |      |       |

**Gate condition:** All Tier 1 criteria (A1–A10) must pass. Tier 2 criteria (G1–G5) are documented as targets with remediation plans for any failures.

---

## 5. External Consultant Engagement Plan

### 5.1 Rationale

Per the CDO audit recommendation and the Game Accessibility Guidelines (§5.1), an **external accessibility consultant** must be engaged before soft launch. Internal team members (Elena and Marco) are capable but not formally trained accessibility specialists. An external consultant provides:

1. **Independent validation** — Unbiased assessment of accessibility compliance
2. **Specialized expertise** — Screen reader optimization, assistive technology testing, legal compliance
3. **Risk mitigation** — Reduces liability exposure for WCAG 2.1 AA and COPPA accessibility requirements
4. **Industry benchmarking** — Comparison against competitor accessibility standards

### 5.2 Engagement Timeline

| Phase                       | Timing           | Duration | Activities                                                                |
| --------------------------- | ---------------- | -------- | ------------------------------------------------------------------------- |
| **Research & Selection**    | Stage 3 start    | 2 weeks  | RFP issued, 3 candidates evaluated, contract negotiated                   |
| **Onboarding**              | Stage 4 start    | 1 week   | Consultant receives GDD, PRD, SRD, accessibility SBOM, prototype builds   |
| **Mid-Production Audit**    | Stage 5 (75%)    | 2 weeks  | Comprehensive accessibility audit of feature-complete build               |
| **Pre-Soft-Launch Audit**   | Stage 7 prep     | 2 weeks  | Final accessibility validation, legal compliance review, remediation plan |
| **Post-Soft-Launch Review** | Stage 8 (Week 4) | 1 week   | Real-world accessibility data analysis, iteration recommendations         |

### 5.3 Consultant Selection Criteria

| Criterion                                | Weight | Minimum Requirement                                        |
| ---------------------------------------- | ------ | ---------------------------------------------------------- |
| Game accessibility experience            | 30%    | 3+ shipped game titles with accessibility features         |
| WCAG 2.1 AA / legal compliance expertise | 25%    | Demonstrated compliance audit experience                   |
| Assistive technology testing capability  | 20%    | In-house screen reader, switch control, eye-tracking tools |
| Mobile platform expertise                | 15%    | iOS VoiceOver + Android TalkBack deep knowledge            |
| Cost                                     | 10%    | Within $15K–$30K total engagement budget                   |

### 5.4 Recommended Firms (Initial Research)

| Firm                          | Strengths                                        | Estimated Cost |
| ----------------------------- | ------------------------------------------------ | -------------- |
| AbleGamers Foundation         | Non-profit, game-specific expertise, playtesting | $10K–$20K      |
| SpecialEffect                 | UK-based, motor accessibility specialists        | £8K–£15K       |
| Can I Play That? (consulting) | Independent game accessibility audits            | $12K–$25K      |

_Final selection to be made by Stage 3 start. Budget allocated from studio contingency fund with CDO approval._

### 5.5 Consultant Deliverables

| Deliverable                           | Timing                      | Owner              |
| ------------------------------------- | --------------------------- | ------------------ |
| Accessibility audit report            | Mid-production + Pre-launch | Consultant         |
| Remediation priority list (P0–P3)     | Each audit                  | Consultant         |
| Legal compliance assessment           | Pre-launch                  | Consultant         |
| Accessibility playtest facilitation   | Mid-production              | Consultant + Elena |
| Post-launch iteration recommendations | Post-soft-launch            | Consultant         |

---

## 6. Timeline — Stage 0 Through Stage 8

### Stage 0: Portfolio Review + Art Direction (Weeks 1–3)

| Week | Milestone                                                           | Owner          | Deliverable                    |
| ---- | ------------------------------------------------------------------- | -------------- | ------------------------------ |
| W1   | Accessibility ownership document created (this document)            | CDO + Elena    | `ACCESSIBILITY-OWNERSHIP.md`   |
| W1   | WCAG 2.1 AA training provided to Elena (CDO-led workshop)           | CDO → Elena    | Training materials + checklist |
| W2   | IDS animation spec template updated with accessibility notes fields | Marco          | `animation-specs.md` v2 (a11y) |
| W2   | Duration tokens defined with accessibility-aware limits             | Marco          | `duration-tokens.md`           |
| W3   | Art Direction Brief includes accessibility requirements             | Renaud + Elena | Updated Art Direction Brief    |
| W3   | Style Guide v1 includes contrast ratio specifications               | Elena          | Style Guide v1 §Accessibility  |

**Gate check:** Accessibility ownership assigned ✅ (CDO audit condition C1 satisfied)

---

### Stage 1: Concept (Weeks 4–6)

| Week | Milestone                                             | Owner         | Deliverable                         |
| ---- | ----------------------------------------------------- | ------------- | ----------------------------------- |
| W4   | Colorblind mode design spec (3 presets) drafted       | Elena + Lena  | `colorblind-palette-spec.md`        |
| W4   | Accessibility settings UI requirements added to PRD   | Elena → CPO   | PRD §Accessibility Requirements     |
| W5   | Tap target compliance requirements added to SRD       | Elena → CSO   | SRD §Accessibility Security         |
| W5   | Accessibility SBOM initiated                          | Elena         | `accessibility-sbom.md` v1          |
| W6   | Accessibility acceptance criteria drafted for Stage 2 | Elena + Marco | `stage2-accessibility-checklist.md` |

---

### Stage 2: Prototype (Weeks 7–10)

| Week | Milestone                                                                     | Owner         | Deliverable                             |
| ---- | ----------------------------------------------------------------------------- | ------------- | --------------------------------------- |
| W7   | Contrast audit on prototype (automated + manual)                              | Elena         | `contrast-audit-report.md` v1           |
| W7   | Tap target audit on prototype                                                 | Elena         | `tap-target-audit.md` v1                |
| W8   | Reduced-motion detection implementation in prototype                          | Marco         | `reduced-motion-implementation-spec.md` |
| W8   | Animation alternatives matrix (every animation has reduced-motion variant)    | Marco         | `animation-alternatives-matrix.md`      |
| W8   | Seizure safety audit of all animations                                        | Marco         | `seizure-safety-audit.md`               |
| W9   | Screen reader labels defined for all meta-UI elements                         | Elena         | `accessibility-labels.csv` v1           |
| W9   | Accessibility settings screen designed and prototyped                         | Elena         | Settings screen mockup                  |
| W10  | **Stage 2 accessibility gate review** — All Tier 1 criteria (A1–A10) verified | Elena + Marco | Gate review sign-off                    |
| W10  | Tier 2 (gameplay) criteria assessed with remediation plans for failures       | Elena + Marco | `accessibility-gap-remediation.md`      |

**Gate check:** All Tier 1 criteria pass → Stage 2 approved

---

### Stage 3: Vertical Slice (Weeks 11–16)

| Week | Milestone                                                   | Owner            | Deliverable                       |
| ---- | ----------------------------------------------------------- | ---------------- | --------------------------------- |
| W11  | Text scaling test at 200% enlargement                       | Elena            | `text-scaling-test-report.md`     |
| W12  | High contrast mode design spec                              | Elena            | `high-contrast-spec.md`           |
| W12  | Haptic alternative patterns designed                        | Marco            | `haptic-patterns-spec.md`         |
| W13  | VFX reduced-motion variants coordinated with Javier Moreno  | Marco + Javier   | `vfx-reduced-motion-spec.md`      |
| W13  | One-hand mode validation playtest                           | Marco + Mei      | `one-hand-mode-test-report.md` v1 |
| W14  | External accessibility consultant RFP issued                | Elena + Producer | RFP document                      |
| W15  | Consultant selection and contract signed                    | CDO + Producer   | Signed contract                   |
| W16  | Accessibility SBOM updated with all Stage 3 implementations | Elena            | `accessibility-sbom.md` v2        |

---

### Stage 4: Production Planning (Weeks 17–19)

| Week | Milestone                                                        | Owner             | Deliverable                        |
| ---- | ---------------------------------------------------------------- | ----------------- | ---------------------------------- |
| W17  | Accessibility requirements incorporated into implementation plan | Elena → CTO       | Implementation Plan §Accessibility |
| W17  | Consultant onboarding — GDD, PRD, SRD, accessibility SBOM shared | Elena             | Consultant onboarding package      |
| W18  | Accessibility testing scope added to QA test plan                | Elena → Test Lead | QA Test Plan §Accessibility        |
| W18  | Automated contrast tooling integrated into CI pipeline           | Elena + Eng       | CI gate configuration              |
| W19  | Accessibility budget confirmed (consultant + tooling)            | Producer + CDO    | Budget approval                    |

---

### Stage 5: Full Production (Weeks 20–36)

| Milepoint | Milestone                                                     | Owner         | Deliverable                          |
| --------- | ------------------------------------------------------------- | ------------- | ------------------------------------ |
| 50%       | Mid-production accessibility check (informal)                 | Elena         | `mid-production-a11y-check.md`       |
| 60%       | Design Fidelity Checkpoint includes accessibility conformance | CDO + Elena   | DFC §Accessibility results           |
| 75%       | **External consultant mid-production audit** (2 weeks)        | Consultant    | Accessibility audit report v1        |
| 75%       | Remediation of consultant findings (P0/P1 mandatory)          | Elena + Marco | Remediation log                      |
| 90%       | Accessibility regression checklist completed                  | Elena         | `accessibility-release-checklist.md` |
| 90%       | One-hand mode validation (updated)                            | Marco + Mei   | `one-hand-mode-test-report.md` v2    |

---

### Stage 6: Automated Testing (Weeks 37–40)

| Week | Milestone                                                                    | Owner             | Deliverable                      |
| ---- | ---------------------------------------------------------------------------- | ----------------- | -------------------------------- |
| W37  | Accessibility automated tests integrated into test suite                     | Elena + Test Lead | Test suite §Accessibility        |
| W38  | Screen reader testing (VoiceOver iOS + TalkBack Android) on production build | Elena             | `screen-reader-test-report.md`   |
| W39  | Colorblind mode manual verification across all game screens                  | Elena             | `colorblind-verification.md`     |
| W39  | Reduced-motion compliance verification                                       | Marco             | `reduced-motion-verification.md` |
| W40  | Accessibility defects classified (P0–P3) and remediated                      | Elena + Marco     | Defect log                       |

---

### Stage 7: Soft Launch Prep (Weeks 41–44)

| Week | Milestone                                                                  | Owner         | Deliverable                         |
| ---- | -------------------------------------------------------------------------- | ------------- | ----------------------------------- |
| W41  | **External consultant pre-soft-launch audit** (2 weeks)                    | Consultant    | Accessibility audit report v2       |
| W42  | Remediation of consultant findings (P0/P1 mandatory, P2/P3 user decision)  | Elena + Marco | Remediation log v2                  |
| W43  | Accessibility compliance sign-off from CDO                                 | CDO           | CDO accessibility sign-off          |
| W43  | Accessibility compliance sign-off from CSO (privacy/accessibility overlap) | CSO           | CSO accessibility sign-off          |
| W44  | Soft launch build validated — all accessibility criteria met               | Elena + Marco | Soft launch accessibility clearance |

---

### Stage 8: Soft Launch (Weeks 45–52)

| Week | Milestone                                                              | Owner           | Deliverable                          |
| ---- | ---------------------------------------------------------------------- | --------------- | ------------------------------------ |
| W45  | Soft launch in Tier 1 markets (Canada, Australia)                      | Studio          | Live build                           |
| W46  | Accessibility feedback monitoring (app store reviews, support tickets) | Elena           | `accessibility-feedback-log.md`      |
| W48  | Accessibility data analysis from live cohort                           | Elena + Analyst | `accessibility-live-data-report.md`  |
| W49  | **External consultant post-soft-launch review** (1 week)               | Consultant      | Post-launch accessibility assessment |
| W50  | Iteration plan based on consultant recommendations                     | Elena + Marco   | `accessibility-iteration-plan.md`    |
| W52  | Soft launch gate review — accessibility status included                | Elena + Marco   | Gate review presentation             |

---

## 7. Escalation & Oversight

### 7.1 Reporting Chain

```
Elena Morozova ──┐
                 ├──→ Renaud Leclercq (Art Director) ──→ Yuki Tanaka-Chen (CDO)
Marco Bellini ───┘
```

### 7.2 Escalation Triggers

| Trigger                                                      | Escalate To           | Response Time |
| ------------------------------------------------------------ | --------------------- | ------------- |
| P0 accessibility defect found (screen reader, contrast)      | CDO immediately       | 24 hours      |
| P1 accessibility defect found (colorblind, motor, cognitive) | Art Director → CDO    | 48 hours      |
| Stage gate accessibility criteria not met                    | CDO + Studio Director | Before gate   |
| Consultant recommends P0 remediation                         | CDO + Producer        | 24 hours      |
| Accessibility regression detected in any build               | Elena → Art Director  | Next build    |

### 7.3 CDO Oversight Commitment

As CDO, I commit to:

1. **Reviewing all accessibility audit reports** before stage gate reviews
2. **Conducting personal accessibility testing** on both platforms (iOS VoiceOver + Android TalkBack) before Stage 6 gate review
3. **Participating in the external consultant review** sessions remotely
4. **Providing WCAG 2.1 AA auditing training** to Elena during Stage 0
5. **Ensuring accessibility is included in Stage 10 Release Readiness** checklist item #2 (Design — all CDO/IDS specifications accurately realised)

---

## 8. Audit Condition Satisfaction

### CDO Audit Condition C1: "Accessibility ownership assigned"

| Requirement                             | Status       | Evidence              |
| --------------------------------------- | ------------ | --------------------- |
| Named owner for visual/UI accessibility | ✅ Satisfied | Elena Morozova (§2.1) |
| Named owner for motion accessibility    | ✅ Satisfied | Marco Bellini (§2.2)  |
| Documented in Stage 0 deliverables      | ✅ Satisfied | This document         |
| Specific responsibilities defined       | ✅ Satisfied | §3.1, §3.2, §3.3      |
| Stage 2 acceptance criteria defined     | ✅ Satisfied | §4                    |
| External consultant engagement planned  | ✅ Satisfied | §5                    |
| Timeline from Stage 0 through Stage 8   | ✅ Satisfied | §6                    |
| Oversight and escalation chain defined  | ✅ Satisfied | §7                    |

### CSO Audit Cross-Reference

| CSO Concern                                | Accessibility Resolution                            |
| ------------------------------------------ | --------------------------------------------------- |
| Screen reader support gap (CDO Finding #9) | Elena owns VoiceOver/TalkBack labels (§3.1, E5)     |
| No accessibility gate owner                | Elena + Marco own Stage 2 accessibility gate (§4.3) |
| Accessibility not in SRD                   | Tap target compliance added to SRD (§6, Stage 1 W5) |

---

**Signed:** Yuki Tanaka-Chen, Chief Design Officer
**Date:** April 12, 2026
**Approved by:** Renaud Leclercq (Art Director, Casual Games Studio)
**CC:** Dr. Sarah Chen (CSO), Marcus Tran-Yoshida (CPO), Studio Director (Marcus Vogel)
