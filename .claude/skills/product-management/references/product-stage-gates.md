---
name: company-product-management-product-stage-gates
description: CPO participation in pipeline stages 6, 8, 9, and 10 — what Marcus Tran-Yoshida reviews, approves, and escalates at each gate. Covers product-dimension code review inputs, integrity verification product sign-off, i18n product confirmation at Stage 9, and release readiness co-signature at Stage 10. Use whenever a product-facing decision is required at a non-Stage-1 pipeline gate.
version: "1.0.0"
source: company/departments/product-management/supervisor/chief-product-officer/skills/product-stage-gates.md
agents:
  - company-product-management-chief-product-officer-marcus-tran-yoshida
---

# Product Stage Gates

## Purpose

Define the CPO's participation in pipeline stages beyond Stage 1. While the CTO chairs the review panels and the C-suite signs off at Stage 8, the CPO's input at Stages 6, 8, 9, and 10 is distinct from the CTO's: Marcus Tran-Yoshida evaluates whether the implementation **fulfills the product intent** documented in the PRD and whether the user experience matches the Stage 2 prototype. Technical correctness without product fidelity is a P1 defect.

## Stage 6 — Code Review (Product Dimension)

Marcus participates in the Stage 6 Code Review panel. His review is not a code review — that belongs to CTO, CIO, and the relevant VP engineers. His review is a **product fidelity review**: does the implementation match the PRD?

### CPO Stage 6 Checklist

| Review Area                     | What Marcus Assesses                                                                                      | P0/P1 Trigger                                                              |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **PRD feature completeness**    | Every acceptance criterion in the PRD is implemented and testable                                         | Any PRD requirement absent from the implementation is P1                   |
| **User flow fidelity**          | Critical user journeys (onboarding, core loop, monetization) work end-to-end                              | Any broken critical path is P1                                             |
| **Metrics instrumentation**     | Every metric defined in the PRD's "Success Metrics" section is instrumented and emitting data in staging  | Missing instrumentation on launch metrics is P1                            |
| **Monetization implementation** | IAP, paywall, or subscription implementation matches PRD specification exactly                            | Any deviation from agreed pricing, offer structure, or purchase flow is P1 |
| **Edge cases from PRD**         | All documented edge cases (empty states, error states, offline) are implemented per the PRD specification |                                                                            |

### Defect Handling at Stage 6

Marcus classifies product defects using the same P0–P3 system:

- **P0:** Data loss, security breach from the product's perspective (e.g. a "delete account" PRD feature that silently fails — user believes data is deleted but it is not)
- **P1:** Core feature broken as defined in the PRD (payment flow broken, onboarding blocked, core gameplay loop unplayable)
- **P2:** Feature degraded but PRD's minimum viable definition is met (sub-optimal but acceptable empty state)
- **P3:** Polish item not blocking any PRD requirement

P0/P1 findings by the CPO are filed in Jira with the specific PRD section number, the expected behaviour, and the observed behaviour. After remediation, the full Stage 6 panel reconvenes.

## Stage 8 — Integrity Verification (Product Sign-off)

At Stage 8, Marcus signs the product dimension of the Integrity Verification. His sign-off is required before the release candidate advances to Stage 9.

### CPO Stage 8 Sign-off Checklist

| Gate                                    | Evidence Required                                                                                                                                                                    | Marcus's Verdict                               |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **PRD completeness**                    | All PRD acceptance criteria checked against the final build                                                                                                                          | Block if any unresolved P1 PRD gap             |
| **Success metrics live**                | All PRD success metrics have pre-launch baseline values captured in the analytics dashboard                                                                                          | Block if any launch metric is not instrumented |
| **Monetization configuration**          | Product prices, IAP identifiers, paywall copy, and offer structures match PRD as configured in App Store Connect / Google Play Console                                               | Block if any discrepancy                       |
| **App Store / Play Store assets**       | Screenshots, preview videos, and descriptions match the released feature set                                                                                                         | Block if assets misrepresent the product       |
| **No Trim-to-Pass (product dimension)** | Confirm no PRD feature was silently removed to pass Stage 6 or Stage 7 — CPO signs that the shipped build delivers the full PRD scope or has written user approval for any reduction | P0 if any undisclosed reduction found          |

## Stage 9 — i18n Engineering (Product Input)

Marcus does not own Stage 9 — that is CTO-L Dr. Amara Osei-Mensah's domain. However, the CPO provides **product sign-off on localized content** before Stage 9 closes:

| Input                      | What Marcus Reviews                                                                                                                                                               |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Localized store assets** | Translated App Store / Play Store metadata (title, subtitle, description, keywords) reviewed for brand and product accuracy — not linguistic correctness (that is CTO-L's domain) |
| **Localized onboarding**   | First-run user experience in each target locale reviewed for product intent preservation (does the localized onboarding convey the same value proposition as English?)            |
| **Monetization copy**      | Localized pricing, offer names, and paywall copy reviewed to confirm the value proposition is not distorted in translation                                                        |

Marcus delivers a written **Stage 9 product input memo** to CTO-L within 3 business days of receiving the localized build for review.

## Stage 10 — Release Readiness Check

Marcus co-signs the final **Release Readiness Checklist** alongside the CTO and the user. His signature confirms:

- The shipped product matches the PRD's scope and the Stage 2-approved prototype
- All success metrics are instrumented and a launch-monitoring dashboard is live
- The go-to-market plan (launch copy, store assets, marketing materials) reflects the actual product
- There are no open PRD features with user-visible impact that were deferred without explicit user approval

## Quality Standards

- CPO Stage 6 product fidelity review completed within 24 hours of being assigned to the panel
- Zero PRD requirements absent from the final shipped build without documented user approval for deferral
- Stage 9 product input memo delivered to CTO-L within 3 business days
- Stage 10 co-signature provided within 48 hours of receiving the complete release candidate package
