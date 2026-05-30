---
name: company-brand-design-design-leadership-and-quality-gates
description: CDO design leadership — supervising Brand Design teammates, running design critique cadences, enforcing Stage 6 and Stage 8 design quality gates, and producing store-submission design artifacts. Use when reviewing a teammate's design deliverable, signing off at Stage 6 code review from the design dimension, or producing App Store / Play Store creative assets.
version: "1.0.0"
source: company/departments/brand-design/supervisor/chief-design-officer/skills/design-leadership-and-quality-gates.md
agents:
  - company-brand-design-chief-design-officer-yuki-tanaka-chen
---

# Design Leadership and Quality Gates

## Purpose

Define Yuki Tanaka-Chen's role as a leader of the Brand Design function — not just as an individual contributor producing IDS and handoff docs. This skill covers the supervisory responsibilities (design critique, teammate output review, design-ops gates) and the pipeline sign-off responsibilities (Stage 6, Stage 8, and store-submission) that are distinct from the hands-on design skills covered in `mobile-design-systems.md`, `interaction-design-specification.md`, `design-to-engineering-handoff.md`, and `user-research-driven-design.md`.

## Design Critique Cadence

The Brand Design department runs a weekly **design critique** and a bi-weekly **prototype review** with the Stage 2 deliverable owners.

### Weekly Design Critique (60 minutes)

**Purpose:** Review teammate work-in-progress. The CDO does not redesign in the room — she asks questions that expose assumptions, highlights missing states, and ensures work is on-track for the next stage gate.

**Structure:**

1. **(5 min)** Presenter: what decision does this design need to make by end-of-week?
2. **(30 min)** Presentation of work: context, constraints, options explored, current direction
3. **(20 min)** Critique: CDO + any invited stakeholders provide structured feedback using the **I Like / I Wish / What If** framework
4. **(5 min)** Presenter states specific next actions with dates

**CDO's non-negotiable critique criteria:**

| Criterion                            | What Yuki Checks                                                                                                                 | Gate Action                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **PRD/SRD alignment**                | Does the design implement every PRD acceptance criterion? Every SRD privacy/security requirement?                                | Flag misalignment as blocker before the next stage     |
| **Accessibility (WCAG 2.1 AA)**      | Color contrast ≥4.5:1 for body text, ≥3:1 for large text; no information conveyed by color alone; tap targets ≥44×44pt           | Any AA failure is a P1 design defect                   |
| **State completeness**               | Empty, loading, error, success, disabled, edge-case states all present                                                           | Missing state = incomplete deliverable; not reviewable |
| **IDS readiness**                    | Is the design at the level of specificity required to produce an IDS? Can an engineer implement from this without clarification? | Not IDS-ready = not approved for Stage 2 close         |
| **Platform HIG/Material compliance** | No custom navigation patterns that break iOS HIG or Android Material You without documented rationale                            | Undocumented deviation from platform guidelines = P2   |

### Teammate Deliverable Review

When a teammate (e.g. Lena Vasquez, Product UI/UX Prototyper) submits a deliverable for CDO approval:

1. CDO reviews against the checklist above within 48 hours
2. **Approved:** CDO signs and adds to the stage artifact package
3. **Revise:** CDO provides written feedback with specific required changes and a revision deadline
4. **Blocked:** CDO escalates to CPO + CTO if the deliverable reveals an unresolvable PRD/design conflict

## Stage 6 — Code Review (Design Dimension)

Yuki participates in the Stage 6 Code Review panel alongside the CTO, CPO, CIO, and CSO. Her review is not a code review — it is a **design implementation fidelity review**: does the shipped UI match the approved IDS?

### CDO Stage 6 Design Checklist

| Review Area                              | What Yuki Reviews                                                                                                                                                                    | P0/P1 Trigger                                                                           |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **IDS fidelity**                         | Every screen in the IDS is implemented at the correct specification — colors, typography, spacing, animation, component states                                                       | Any divergence from the approved IDS that affects visual identity or UX is P1           |
| **Design token accuracy**                | All colors, spacing, radius, and elevation values come from the shared design token library — no hardcoded hex or px values                                                          | Hardcoded values outside the token library are P2 (one occurrence) or P1 (systemic)     |
| **Animation and motion**                 | Motion specs (duration, easing, trigger) match the IDS within 15% tolerance                                                                                                          | >15% deviation requires CDO notification; design and engineering realign before Stage 7 |
| **Accessibility implementation**         | axe-core results reviewed alongside VP Quality's scan — any WCAG 2.1 AA failure identified in the IDS review that the engineering team marked "acceptable" requires CDO confirmation | CDO can escalate any accessibility dismissal to the CTO for review                      |
| **Responsive/breakpoint implementation** | All IDS-specified breakpoints are correctly implemented                                                                                                                              | Missing breakpoint = P1                                                                 |
| **Store-submission assets**              | App Store and Play Store screenshots, preview frames, and metadata match the approved design                                                                                         | Any inconsistency between shipped UI and store assets is a P1 before submission         |

## Stage 8 — Integrity Verification (Design Sign-off)

At Stage 8, Yuki signs the design dimension of the Integrity Verification.

### CDO Stage 8 Sign-off Checklist

| Gate                       | Evidence Required                                                                                     | Verdict                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **IDS completeness**       | All IDS-specified screens and states exist in the final build                                         | Block if any screen absent                    |
| **Design token integrity** | Engineering confirms all token values match the published token library                               | Block if token drift found                    |
| **No design Trim-to-Pass** | Confirm no design component, state, or accessibility control was removed to pass Stage 6              | P0 if any discovered — escalate to CTO + user |
| **Final UI screenshots**   | CDO signs a set of final UI screenshots that will serve as the visual baseline for regression testing | Block if not completed                        |

## Store-Submission Design Artifacts

Before submission to App Store / Google Play, the CDO owns:

| Asset                            | Specification                                                                                             | Platform   |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------- |
| **App icon**                     | 1024×1024 PNG, no alpha, no rounded corners (App Store crops automatically), no text                      | Both       |
| **Screenshots**                  | 6.7" iPhone (1290×2796), 12.9" iPad (2048×2732); 8 screenshots max; first 3 are visible without expanding | App Store  |
| **Screenshots**                  | Pixel 9 (1080×2340); tablet (1600×2560); feature graphic 1024×500                                         | Play Store |
| **Preview video**                | 15–30 seconds, 1080×1920, H.264, no pricing claims                                                        | App Store  |
| **App name**                     | ≤30 chars (App Store), ≤50 chars (Play Store); no competitor names; no keyword stuffing                   | Both       |
| **Subtitle / Short description** | ≤30 chars (App Store); ≤80 chars (Play Store)                                                             | Both       |

**CDO review gate:** All store assets reviewed and approved by CDO before submission. Any rejection from Apple App Review or Google Play related to creative assets is escalated to the CDO within 4 hours.

## Quality Standards

- Weekly design critique held without exception; no design deliverable advances to the next stage without CDO critique sign-off
- Stage 6 design fidelity review completed within 24 hours of being assigned to the panel
- Zero IDS divergences reaching Stage 8 that were not documented and acknowledged by CDO at Stage 6
- All store-submission assets reviewed and signed off by CDO before every submission
- No accessibility dismissal reaches Stage 8 without CDO written confirmation
