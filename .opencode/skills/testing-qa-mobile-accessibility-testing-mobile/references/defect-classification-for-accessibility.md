# Defect Classification for Accessibility

## Defect Classification for Accessibility

Accessibility defects are classified using the P0–P3 severity system aligned with the company's defect classification standard.

### Accessibility Defect Severity Table

| Level  | Definition                  | Accessibility Impact                                                                                | Release Impact                  | Examples                                                                                                                                                                                                                            |
| ------ | --------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P0** | Complete barrier to access  | Core functionality entirely inaccessible to screen reader users or users with specific disabilities | Blocks release — non-negotiable | - Entire screen has no accessibility labels<br>- Form submission impossible without vision<br>- Security vulnerability exposing user data via accessibility API                                                                     |
| **P1** | Major accessibility barrier | Significant functionality degraded or confusing; workarounds exist but are non-trivial              | Blocks release — non-negotiable | - Touch targets below minimum size on critical buttons<br>- Contrast ratio below 3:1 on primary action buttons<br>- Screen reader navigation order makes screen unusable<br>- Dynamic type causes text clipping on critical content |
| **P2** | Minor accessibility barrier | Some functionality degraded but usable with effort                                                  | User decides to fix or defer    | - Secondary text contrast slightly below 4.5:1 (e.g., 4.0:1)<br>- Missing accessibility hints on non-critical elements<br>- Minor layout shift at maximum dynamic type that does not block access                                   |
| **P3** | Polish / enhancement        | Improves experience but does not block access                                                       | User decides to fix or defer    | - Accessibility announcement could be more descriptive<br>- Focus indicator could be more visible (but meets minimum)<br>- Minor inconsistency in announcement format                                                               |

### P0 Accessibility Defects (Non-Negotiable — Always Block Release)

| #   | Defect Description                                  | WCAG SC |
| --- | --------------------------------------------------- | ------- |
| 1   | Screen cannot be navigated via screen reader at all | 4.1.2   |
| 2   | Form submission requires vision                     | 1.1.1   |
| 3   | Critical action has no accessibility label          | 4.1.2   |
| 4   | Modal dialog does not trap focus                    | 2.4.3   |
| 5   | CAPTCHA with no accessible alternative              | 1.1.1   |

### P1 Accessibility Defects (Non-Negotiable — Always Block Release)

| #   | Defect Description                                                       | WCAG SC |
| --- | ------------------------------------------------------------------------ | ------- |
| 1   | Touch targets below 44x44pt (iOS) / 48x48dp (Android) on primary actions | 2.5.8   |
| 2   | Contrast ratio below 3:1 for UI components                               | 1.4.11  |
| 3   | Contrast ratio below 4.5:1 for body text                                 | 1.4.3   |
| 4   | Screen reader reading order is illogical/confusing                       | 1.3.2   |
| 5   | Text clipped or truncated at 200% font scaling                           | 1.4.4   |
| 6   | Color is the sole means of conveying critical information                | 1.4.1   |
| 7   | Gesture-only control with no single-pointer alternative                  | 2.5.1   |

### P2 Accessibility Defects (User Decides)

| #   | Defect Description                                                         | WCAG SC |
| --- | -------------------------------------------------------------------------- | ------- |
| 1   | Contrast ratio slightly below threshold (4.0:1 vs 4.5:1) on secondary text | 1.4.3   |
| 2   | Missing accessibility hints on non-critical elements                       | 4.1.2   |
| 3   | Minor layout issues at maximum dynamic type                                | 1.4.4   |
| 4   | Inconsistent announcement format across screens                            | 4.1.2   |
| 5   | Focus indicator meets minimum but could be more visible                    | 2.4.7   |

### P3 Accessibility Defects (User Decides)

| #   | Defect Description                                   | WCAG SC |
| --- | ---------------------------------------------------- | ------- |
| 1   | Accessibility announcement could be more descriptive | N/A     |
| 2   | Minor inconsistency in trait reporting               | N/A     |
| 3   | Polish improvement for VoiceOver/TalkBack experience | N/A     |

---
