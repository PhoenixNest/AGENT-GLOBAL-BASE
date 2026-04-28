# Responsive Layout Verification

## Responsive Layout Verification

### Breakpoint Validation

Verify that the UI correctly adapts at defined responsive breakpoints.

**Standard Breakpoint Matrix:**

| Breakpoint Name | Width  | Target Devices                  | Verification Focus                |
| --------------- | ------ | ------------------------------- | --------------------------------- |
| xs              | 320px  | iPhone SE, small Android phones | Content fit, no horizontal scroll |
| sm              | 375px  | iPhone 15, Pixel 7              | Primary mobile layout             |
| md              | 768px  | iPad, small tablets             | Tablet-specific layout            |
| lg              | 1024px | iPad Pro, small desktops        | Multi-column layouts              |
| xl              | 1440px | Desktop monitors                | Full-width layouts                |
| xxl             | 1920px | Large monitors                  | Max-width constraints             |

**Breakpoint Verification Rules:**

| Rule                  | Description                                      | Enforcement                       |
| --------------------- | ------------------------------------------------ | --------------------------------- |
| No horizontal scroll  | Content must fit within viewport width           | Automated scroll detection        |
| Touch target minimum  | 44x44dp on mobile, 48x48dp on Android            | Automated hit-target analysis     |
| Text readability      | No text truncation without ellipsis/tooltip      | Automated text overflow detection |
| Navigation adaptation | Nav pattern changes appropriately at breakpoints | Manual review of nav state        |
| Image scaling         | Images scale proportionally without distortion   | Automated aspect ratio check      |

### Orientation Testing

Verify layout correctness in both portrait and landscape orientations.

| Orientation                    | Platform      | Required Screens        | Notes                                 |
| ------------------------------ | ------------- | ----------------------- | ------------------------------------- |
| Portrait                       | iOS + Android | All user-facing screens | Primary usage mode                    |
| Landscape                      | iOS + Android | All user-facing screens | Media consumption, keyboard scenarios |
| Split-screen (Android)         | Android 7.0+  | Top 5 user journeys     | Multi-window support                  |
| Slide over / Split view (iPad) | iPadOS        | Top 5 user journeys     | iPad multitasking                     |

**Orientation-Specific Checks:**

| Check                    | Portrait                         | Landscape                                 |
| ------------------------ | -------------------------------- | ----------------------------------------- |
| Safe area insets         | Top notch, bottom home indicator | Side notches (if applicable)              |
| Keyboard overlay         | Bottom content not obscured      | Reduced vertical space handled            |
| Image/video aspect ratio | Full width maintained            | Letterboxing/pillarboxing correct         |
| Navigation               | Bottom tab bar or drawer         | Side navigation or compact bar            |
| Scroll direction         | Vertical primary                 | Horizontal may be primary on some screens |

### Dynamic Type Verification

Verify layout integrity when users change system font size settings.

| Setting             | Scale Factor | Platforms     | Risk Level                 |
| ------------------- | ------------ | ------------- | -------------------------- |
| Default             | 1.0x         | iOS + Android | Baseline                   |
| Large               | 1.3x         | iOS + Android | Medium — text overflow     |
| Extra Large         | 1.5x         | iOS + Android | High — layout break        |
| Accessibility (Max) | 2.0x+        | iOS + Android | Critical — reflow required |

**Dynamic Type Test Execution:**

```yaml
dynamic-type-tests:
  - name: "text-reflow-small"
    font-scale: 1.3
    expected: "All text readable without truncation"

  - name: "text-reflow-medium"
    font-scale: 1.5
    expected: "Layout reflows; no overlap"

  - name: "text-reflow-large"
    font-scale: 2.0
    expected: "Content remains accessible; scrolling enabled"

  execution:
    platform: [ios, android]
    screens: "all-user-facing"
    capture-mode: "screenshot-per-screen-per-scale"
```

### RTL (Right-to-Left) Layout Verification

Verify correct mirroring of UI for RTL languages (Arabic, Hebrew, Persian, Urdu).

| Element                   | RTL Behavior                         | Verification                                 |
| ------------------------- | ------------------------------------ | -------------------------------------------- |
| Navigation back button    | Flips to right side                  | Screenshot comparison with mirrored baseline |
| Text alignment            | Right-aligned by default             | Verify all body text                         |
| Icons with directionality | Arrow icons flip                     | Chevron, back, forward icons                 |
| Progress indicators       | LTR progress (rightward) even in RTL | Confirm no flip on progress bars             |
| Media playback controls   | Unchanged (LTR)                      | Verify no unwanted mirroring                 |
| Numbers                   | LTR (Western numerals)               | Verify number rendering                      |
| Mixed content (bidi)      | Correct bidirectional rendering      | Test with mixed Arabic/English text          |

**RTL Test Execution:**

```yaml
rtl-tests:
  locales:
    - ar # Arabic
    - he # Hebrew
    - fa # Persian
    - ur # Urdu
  verification:
    - "All layout directions mirrored correctly"
    - "Non-mirgradable elements preserved (media, progress)"
    - "Text truncation handled at RTL boundary"
  baseline: "RTL-specific baselines required (not mirrored LTR)"
```

---
