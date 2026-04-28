# Dynamic Type Testing

## Dynamic Type Testing

Dynamic type (font scaling) testing ensures that the application remains usable when users increase or decrease the system font size.

### Platform Font Scaling

| Platform | Feature                  | Scaling Range   | Access Path                                         |
| -------- | ------------------------ | --------------- | --------------------------------------------------- |
| Android  | Display Size + Font Size | 0.85x to 2.0x+  | Settings > Accessibility > Font size / Display size |
| iOS      | Dynamic Type             | 0.5x to 5.0x+   | Settings > Accessibility > Display & Text Size      |
| Android  | Bold Text                | Weight increase | Settings > Accessibility > Bold text                |
| iOS      | Bold Text                | Weight increase | Settings > Accessibility > Display & Text Size      |

### Dynamic Type Testing Procedure

1. **Set system font size to maximum** (200%+ on Android, largest on iOS)
2. **Navigate through every screen** in the application
3. **Verify the following for each screen:**
   - [ ] All text remains readable at maximum scale
   - [ ] No text is clipped or truncated
   - [ ] No text overlaps with other elements
   - [ ] Content reflows vertically (no horizontal scrolling required)
   - [ ] All interactive elements remain accessible and tappable
   - [ ] Modal dialogs adapt to larger text
   - [ ] Navigation bars and toolbars accommodate larger text
   - [ ] Bottom navigation/tab bars remain usable
   - [ ] Forms remain usable with enlarged labels and input text
   - [ ] Images with embedded text remain legible or have alternatives
   - [ ] Lists adapt row height for larger content

### Text Spacing Requirements (WCAG 1.4.12)

When users override text spacing, the following must be supported without loss of content or functionality:

| Property          | Override Value  | Requirement                          |
| ----------------- | --------------- | ------------------------------------ |
| Line height       | 1.5x font size  | Lines must not overlap or clip       |
| Paragraph spacing | 2x font size    | Paragraphs must be visually distinct |
| Letter spacing    | 0.12x font size | Characters must not overlap          |
| Word spacing      | 0.16x font size | Words must not overlap               |

### Dynamic Type Defect Classification

| Defect                                          | Severity | Rationale                                          |
| ----------------------------------------------- | -------- | -------------------------------------------------- |
| Text clipped/truncated at 200% font size        | P1       | Content not perceivable; violates WCAG 1.4.4       |
| Horizontal scrolling required at 200%           | P1       | Layout does not reflow; violates WCAG 1.4.10       |
| Interactive elements unreachable at 200%        | P1       | Functionality lost; violates WCAG 1.4.4            |
| Text overlaps other elements at 200%            | P2       | Content perceivable but degraded; borderline P1    |
| Layout looks awkward but all content accessible | P3       | Cosmetic issue; all content and function preserved |
| Minor icon alignment shift at maximum font size | P3       | Cosmetic polish; no content or function loss       |

---
