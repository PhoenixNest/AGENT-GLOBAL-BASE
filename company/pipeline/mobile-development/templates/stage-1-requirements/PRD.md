# Product Requirements Document (PRD)

**Project:** [Project Name]
**Version:** v1
**Author:** CPO (Marcus Tran-Yoshida)
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Approved
**Platform(s):** [Android | iOS | Both]

---

## 1. Product Vision

Brief statement of what the product is, who it serves, and why it matters.

---

## 2. Target Audience

| Segment     | Description    | Primary Need     |
| ----------- | -------------- | ---------------- |
| [Segment 1] | [Who they are] | [What they need] |
| [Segment 2] | [Who they are] | [What they need] |

---

## 3. Platform Requirements

| Platform | Minimum OS | Target Devices    | Notes |
| -------- | ---------- | ----------------- | ----- |
| Android  | API [XX]+  | [Device families] |       |
| iOS      | iOS [XX]+  | [Device families] |       |

---

## 4. Core Features

### 4.1 [Feature Name]

| Aspect                  | Detail                                                                           |
| ----------------------- | -------------------------------------------------------------------------------- |
| **JTBD Statement**      | When [situation], I want to [motivation] so I can [expected outcome]             |
| **Job Type**            | [Functional / Emotional / Social]                                                |
| **User Story**          | As a [user], I want to [action] so that [benefit]                                |
| **Acceptance Criteria** | [Specific, testable criteria]                                                    |
| **Platform Parity**     | [Same on both / Android-specific / iOS-specific]                                 |
| **Priority**            | P0 (Must) / P1 (Should) / P2 (Nice to have)                                      |
| **Success Metric**      | [Metric name, e.g., "paywall conversion lift"]                                   |
| **Success Threshold**   | [Quantified, e.g., "+1.5pp conversion vs control"]                               |
| **Failure Threshold**   | [Quantified, e.g., "<0.5pp lift after 14 days"]                                  |
| **Kill Condition**      | If [metric] < [threshold] after [time window], feature is deprecated and removed |
| **Review Cadence**      | [e.g., 7-day, 14-day, 30-day checkpoints]                                        |

### 4.2 [Feature Name]

[Repeat structure with JTBD, acceptance criteria, and kill conditions]

---

## 5. User Journeys

### 5.1 [Journey Name]

1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## 5.1 Edge Case Matrix

| PRD Feature | Edge Case                      | Expected Behavior                          | Platform | Severity |
| ----------- | ------------------------------ | ------------------------------------------ | -------- | -------- |
| REQ-001     | No network on paywall load     | Show cached paywall, disable purchase CTA  | Both     | P1       |
| REQ-001     | IAP interrupted by call        | Resume flow from payment step, not restart | Both     | P1       |
| REQ-002     | Low storage (<100MB)           | Clear cache, warn user, allow continue     | Android  | P2       |
| REQ-003     | Notification deep-link expired | Show fallback screen with retry option     | iOS      | P2       |

---

## 6. Performance Requirements

| Metric           | Threshold                                        | Platform |
| ---------------- | ------------------------------------------------ | -------- |
| Cold start       | < 2 seconds                                      | Both     |
| Frame rate       | 60fps (no drops below 55fps on critical screens) | Both     |
| Memory footprint | < 150MB baseline                                 | Both     |
| Network payload  | < 500KB for initial screen load                  | Both     |

---

## 7. Accessibility Requirements

All UI components must meet WCAG 2.1 AA standards:

- Minimum touch target: 48dp (Android) / 44pt (iOS)
- Color contrast ratio: 4.5:1 (normal text) / 3:1 (large text)
- Screen reader labels on all interactive elements
- Dynamic type support at 200% font scale
- Reduced motion alternatives for all animations

---

## 8. Localisation Requirements

### 8.1 Target Languages

| Language              | Locale Code | Priority | Market Rationale   | Linguist Assigned |
| --------------------- | ----------- | -------- | ------------------ | ----------------- |
| English               | en-US       | Primary  | Source language    | —                 |
| [Chinese Simplified]  | zh-CN       | [High]   | [Market rationale] | [Name]            |
| [Chinese Traditional] | zh-TW       | [High]   | [Market rationale] | [Name]            |

### 8.2 Locale-Specific Formatting

| Format              | Requirement                                                      |
| ------------------- | ---------------------------------------------------------------- |
| Date/time           | [ISO 8601 with locale display — e.g., yyyy/MM/dd for JA]         |
| Number format       | [Locale-specific separators — e.g., 1,000.50 vs 1.000,50]        |
| Currency            | [Symbol placement, decimal precision per locale]                 |
| Calendar            | [Gregorian default; note locale exceptions — e.g., Japanese era] |
| RTL layout          | [Yes/No — if Arabic, Hebrew, or Persian targeted]                |
| Text expansion      | [Design must accommodate +35% for German, +25% for Romance]      |
| Regional compliance | [Note locale-specific content regulations — e.g., China ICP]     |

---

## 9. Analytics Instrumentation

### 9.1 Event Definitions

| Event Name           | Trigger Condition            | Payload Fields                                      | PRD Feature | Owner        |
| -------------------- | ---------------------------- | --------------------------------------------------- | ----------- | ------------ |
| [e.g., paywall_view] | User lands on paywall screen | `paywall_variant`, `session_id`, `user_cohort`      | REQ-001     | Data Science |
| [e.g., sub_start]    | User completes IAP flow      | `tier`, `platform`, `trial_eligible`, `revenue_usd` | REQ-002     | Data Science |

### 9.2 Metric Calculations

| Metric               | Formula                                     | Data Source     | PRD Feature | Target |
| -------------------- | ------------------------------------------- | --------------- | ----------- | ------ |
| [e.g., sub_conv]     | `count(sub_start) / count(paywall_view)`    | Events above    | REQ-001     | ≥ 5.0% |
| [e.g., D7_retention] | `count(DAU on D7) / count(new_users on D0)` | Cohort analysis | REQ-003     | ≥ 35%  |

### 9.3 Kill Conditions per Feature

| PRD Feature | Success Threshold | Failure Threshold | Review Window | Action on Failure  |
| ----------- | ----------------- | ----------------- | ------------- | ------------------ |
| REQ-001     | [X]               | [Y]               | 14 days       | Deprecate + remove |

---

## 10. Commercial Assessment

| Aspect                          | Detail                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| **Revenue Model**               | [Freemium / Subscription / One-time IAP / Ad-supported]                            |
| **Pricing Tiers**               | [Free: $0 / Pro: $X.XX mo / Premium: $Y.YY mo]                                     |
| **IAP Product IDs**             | [com.project.pro.monthly, com.project.premium.yearly]                              |
| **Engineering Cost**            | [X engineer-weeks across all platforms]                                            |
| **Projected ARR Lift**          | [$Z at [N]% conversion, [M] MAU]                                                   |
| **Revenue-to-Cost Payback**     | [N months to recover engineering investment]                                       |
| **Platform Fees**               | [Apple 15-30% / Google 15-30% — net revenue after fees]                            |
| **Kill Condition (Commercial)** | If projected ARR < engineering cost at [N] months, scope reduced or feature killed |

---

## 11. Out of Scope

Explicitly list what is NOT included in this version:

- [Item 1]
- [Item 2]

---

## 12. Dependencies

| Dependency                           | Source       | Status                              |
| ------------------------------------ | ------------ | ----------------------------------- |
| [Backend API / Design System / etc.] | [Team/Owner] | [Available / In Progress / Blocked] |

---

_Approved by CPO (Marcus Tran-Yoshida) on YYYY-MM-DD_
_Paired artifact: SRD v1 (see paired artifact convention)_
