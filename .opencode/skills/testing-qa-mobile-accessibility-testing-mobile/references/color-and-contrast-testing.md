# Color and Contrast Testing

## Color and Contrast Testing

Color and contrast testing ensures that text and UI elements are perceivable by users with low vision and various forms of color blindness.

### Contrast Ratio Requirements

| Content Type                             | Minimum Ratio | WCAG SC   | Notes                                                   |
| ---------------------------------------- | ------------- | --------- | ------------------------------------------------------- |
| Normal text (less than 18pt/14pt bold)   | 4.5 : 1       | 1.4.3 AA  | Most body text falls in this category                   |
| Large text (18pt+ or 14pt+ bold)         | 3 : 1         | 1.4.3 AA  | Headers, titles, and prominent labels                   |
| UI components and graphical objects      | 3 : 1         | 1.4.11 AA | Borders, icons, form field boundaries, chart elements   |
| Incidental/inactive elements             | Exempt        | 1.4.3     | Disabled text, decorative elements, logotypes           |
| Active user interface components (focus) | 3 : 1         | 2.4.7 AA  | Focus indicator must be visible against all backgrounds |

### Contrast Testing Procedure

1. **Identify all text elements** in the application (body text, headers, labels, buttons, links)
2. **Identify all UI components** that require contrast (icons, borders, form field outlines, dividers)
3. **Measure foreground/background color values** — use hex codes from design system or inspect rendered colors
4. **Calculate contrast ratio** — use a contrast checker tool (e.g., WebAIM, Colour Contrast Analyser)
5. **Compare against requirements** — 4.5:1 for normal text, 3:1 for large text and UI components
6. **Test on actual device screens** — calibrated display, not design tool color values
7. **Test in various lighting conditions** — indoor, outdoor, low-light

### Color Blindness Testing

Simulate the following types of color vision deficiency:

| Type              | Prevalence   | Affected Colors       | Testing Approach                                                         |
| ----------------- | ------------ | --------------------- | ------------------------------------------------------------------------ |
| **Protanopia**    | 1% of men    | Red weakness          | Use color blindness simulator; verify red elements still distinguishable |
| **Deuteranopia**  | 5% of men    | Green weakness        | Most common CVD; verify green elements distinguishable from background   |
| **Tritanopia**    | 0.01% of men | Blue weakness         | Verify blue/yellow distinctions                                          |
| **Achromatopsia** | 0.003%       | Total color blindness | Test in grayscale mode; all info must be perceivable                     |

### Color Information Testing Checklist

- [ ] Color is NOT the sole means of conveying information (WCAG 1.4.1)
- [ ] Error states use icon + color + text (not color alone)
- [ ] Required form fields indicated by asterisk or text (not red color alone)
- [ ] Success states use icon + color + text
- [ ] Charts/graphs use patterns, labels, or textures in addition to color
- [ ] Links are visually distinguishable from surrounding text (underline or other indicator)
- [ ] Status indicators combine color with icon/text/shape
- [ ] Form validation messages are perceivable without relying on color

### Contrast Audit Results Template

| Element             | Foreground | Background | Ratio  | Required | Pass/Fail | Notes          |
| ------------------- | ---------- | ---------- | ------ | -------- | --------- | -------------- |
| Body text           | #1A1A1A    | #FFFFFF    | 18.4:1 | 4.5:1    | PASS      |                |
| Secondary text      | #757575    | #FFFFFF    | 4.6:1  | 4.5:1    | PASS      | Borderline     |
| Disabled text       | #BDBDBD    | #FFFFFF    | 2.1:1  | Exempt   | N/A       | Disabled state |
| Primary button text | #FFFFFF    | #1976D2    | 4.5:1  | 4.5:1    | PASS      | Exact minimum  |
| Icon (inactive tab) | #9E9E9E    | #FFFFFF    | 2.9:1  | 3:1      | FAIL      | P2 defect      |
| Error message text  | #D32F2F    | #FFFFFF    | 5.4:1  | 4.5:1    | PASS      |                |
| Focus indicator     | #1976D2    | #FFFFFF    | 4.5:1  | 3:1      | PASS      |                |

---
