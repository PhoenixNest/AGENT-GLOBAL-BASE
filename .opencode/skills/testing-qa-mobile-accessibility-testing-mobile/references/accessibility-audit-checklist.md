# Accessibility Audit Checklist

## Accessibility Audit Checklist

### Pre-Audit Preparation

- [ ] Identify all screens/screens flows to audit
- [ ] Prepare test devices (Android with TalkBack, iOS with VoiceOver)
- [ ] Install accessibility scanner tools
- [ ] Prepare contrast checking tools
- [ ] Prepare font scaling test scenarios
- [ ] Prepare color blindness simulation tools

### Screen Reader Audit

- [ ] All screens navigable via TalkBack
- [ ] All screens navigable via VoiceOver
- [ ] All interactive elements have meaningful labels
- [ ] Reading order is logical and matches visual order
- [ ] All element roles/types are correctly announced
- [ ] State changes are announced (checked/unchecked, expanded/collapsed)
- [ ] Focus management is correct on modal/dialog open/close
- [ ] Images have appropriate descriptions or are hidden
- [ ] Status messages are announced
- [ ] No dead ends or focus traps (except intentional modal traps)

### Touch Target Audit

- [ ] All touch targets meet minimum size (44x44pt iOS / 48x48dp Android)
- [ ] No overlapping touch targets
- [ ] Adequate spacing between adjacent targets
- [ ] All small icon buttons have expanded hit areas

### Contrast Audit

- [ ] All normal text meets 4.5:1 contrast ratio
- [ ] All large text meets 3:1 contrast ratio
- [ ] All UI components meet 3:1 contrast ratio
- [ ] Focus indicators are visible against all backgrounds
- [ ] Color is not the sole means of conveying information

### Dynamic Type Audit

- [ ] All text readable at maximum font scaling
- [ ] No text clipped or truncated
- [ ] No horizontal scrolling at 200% font size
- [ ] All interactive elements accessible at maximum font scaling
- [ ] Layout adapts gracefully

### Automated Testing

- [ ] Espresso accessibility checks integrated and passing
- [ ] XCTest accessibility checks integrated and passing
- [ ] Lint checks configured for accessibility
- [ ] CI/CD pipeline includes accessibility checks

---
