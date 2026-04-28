# Stage 7 and Stage 8 Integration

## Stage 7 and Stage 8 Integration

Accessibility testing is a required component of Stage 7 (Automated Testing) and Stage 8 (Integrity Verification).

### Stage 7 — Automated Testing Requirements

| Requirement                    | Description                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| Automated accessibility checks | Espresso and XCTest accessibility checks must pass in the test suite       |
| Screen reader manual testing   | TalkBack and VoiceOver testing completed on all user-facing screens        |
| Contrast audit                 | All text and UI elements measured and documented                           |
| Touch target audit             | All interactive elements verified against platform minimums                |
| Dynamic type testing           | Application tested at 200%+ font scaling on all screens                    |
| Defect reporting               | All accessibility defects classified (P0–P3) and included in Defect Report |
| Automated check pass rate      | 100% of automated accessibility checks must pass for Stage 7 sign-off      |

### Stage 8 — Integrity Verification

| Panel Member | Accessibility Verification Responsibility                        |
| ------------ | ---------------------------------------------------------------- |
| CTO          | Confirm all automated accessibility checks pass                  |
| CSO          | Verify accessibility does not introduce security vulnerabilities |
| CDO          | Confirm design specifications meet accessibility requirements    |
| CPO          | Confirm PRD accessibility requirements are satisfied             |

### Accessibility Gate Criteria Summary

| Stage | Accessibility Gate Criteria                                                            | Sign-off        |
| ----- | -------------------------------------------------------------------------------------- | --------------- |
| 7     | All automated accessibility checks pass; all manual tests documented; defects reported | CTO + Test Lead |
| 8     | No P0/P1 accessibility defects outstanding; P2/P3 presented to user for decision       | CTO Panel       |
| 10    | Accessibility verified as part of full release checklist; platform requirements met    | CTO + User      |

### Platform-Specific Accessibility Requirements

| Platform | Requirement                                      | Standard                                             |
| -------- | ------------------------------------------------ | ---------------------------------------------------- |
| Android  | Play Store accessibility compliance              | Google Play Developer Policy (accessibility section) |
| iOS      | App Store Review Guideline 5.1.1 (Accessibility) | Apple App Store Review Guidelines                    |
| Both     | WCAG 2.1 AA equivalent for mobile                | Industry best practice; referenced in regulations    |

---
