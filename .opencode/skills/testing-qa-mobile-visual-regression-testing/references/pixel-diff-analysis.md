# Pixel Diff Analysis

## Pixel Diff Analysis

### Threshold Configuration

Pixel diff thresholds determine what constitutes a meaningful visual change versus acceptable rendering variance.

**Threshold Levels:**

| Threshold | Pixel Change Tolerance | Use Case                           | False Positive Rate | False Negative Risk   |
| --------- | ---------------------- | ---------------------------------- | ------------------- | --------------------- |
| Strict    | 0.00% - 0.05%          | Pixel-perfect brand UI, typography | Low                 | High (font rendering) |
| Normal    | 0.05% - 0.5%           | General UI components              | Medium              | Low                   |
| Relaxed   | 0.5% - 2.0%            | Canvas/WebGL content, animations   | High                | Very Low              |

**Recommended Configuration:**

```yaml
visual-regression:
  thresholds:
    default: 0.1% # 0.1% pixel difference tolerance
    strict: 0.02% # For brand-critical screens
    relaxed: 1.0% # For dynamic content areas
  comparison:
    method: pixelmatch # Algorithm: pixelmatch, resemble, odiff
    alpha: 0.1 # Opacity of diff overlay
    threshold: 0.1 # Per-pixel sensitivity (0-1)
    includeAA: false # Ignore anti-aliasing differences
    ignoreAntialiasing: true # Reduce false positives from font rendering
  output:
    diff-format: png
    diff-color: ff0066 # Magenta diff highlights
```

### Ignore Regions

Define regions of the screenshot that should be excluded from comparison due to expected variance.

**Ignore Region Types:**

| Region Type            | Examples                             | Ignore Strategy                       |
| ---------------------- | ------------------------------------ | ------------------------------------- |
| Dynamic content        | Timestamps, user avatars, live feeds | Full region exclusion via coordinates |
| Animations             | Loading spinners, transitions        | Exclude animated elements             |
| System UI              | Status bar, navigation bar           | Exclude platform-specific chrome      |
| Third-party content    | Ads, embedded maps                   | Exclude external iframes              |
| User-generated content | Comments, posts                      | Mask content area                     |

**Region Definition (Rectangle-based):**

```json
{
  "ignoreRegions": [
    {
      "name": "status-bar",
      "coordinates": { "x": 0, "y": 0, "width": 1080, "height": 80 }
    },
    {
      "name": "timestamp-area",
      "selector": ".message-timestamp"
    },
    {
      "name": "scrollable-content",
      "selector": ".feed-list",
      "mode": "ignore-all"
    }
  ]
}
```

**Selector-based vs. Coordinate-based Regions:**

| Approach              | Advantages                             | Disadvantages             | Best For                        |
| --------------------- | -------------------------------------- | ------------------------- | ------------------------------- |
| CSS/XPath selectors   | Responsive to layout changes           | Requires accessible DOM   | Web, React Native with test IDs |
| Coordinate rectangles | Precise, tool-agnostic                 | Breaks on layout changes  | Mobile native screens           |
| AI-powered masking    | Automatic detection of dynamic content | Requires ML model, slower | Complex dynamic screens         |

### False Positive Reduction

False positives erode team trust in visual regression gating. Minimize them systematically.

**Common False Positive Causes and Mitigations:**

| Cause                             | Mitigation                                             | Expected Reduction |
| --------------------------------- | ------------------------------------------------------ | ------------------ |
| Anti-aliasing differences         | `ignoreAntialiasing: true`                             | 40-60% reduction   |
| Sub-pixel rendering variance      | Increase threshold to 0.1%                             | 20-30% reduction   |
| Font rendering across OS versions | Ignore text rendering regions or use relaxed threshold | 30-50% reduction   |
| Shadow/glow rendering differences | Use structural similarity (SSIM) comparison            | 15-25% reduction   |
| Image compression artifacts       | Use lossless PNG for all captures                      | Near 0%            |
| Hardware acceleration differences | Force software rendering in test environment           | 10-20% reduction   |
| Network-dependent assets          | Pre-bundle all assets in test build                    | Near 0%            |

**Validation Checklist Before Gate Enforcement:**

1. Run baseline vs. baseline comparison — should yield 0 diffs
2. Seed a known visual change — should be detected
3. Run same build twice on same device — should yield 0 diffs (reproducibility)
4. Test with ignore regions applied — verify dynamic content excluded
5. Verify threshold sensitivity with intentional 0.05% change — should NOT trigger at Normal threshold

---
