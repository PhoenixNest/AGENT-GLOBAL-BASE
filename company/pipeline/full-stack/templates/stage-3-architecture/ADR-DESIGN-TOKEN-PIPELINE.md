# ADR: Design Token Pipeline Strategy (Cross-Platform)

| Field         | Value                                                                     |
| ------------- | ------------------------------------------------------------------------- |
| **Status**    | Proposed                                                                  |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)                         |
| **Decision**  | Amazon Style Dictionary with JSON source and platform-specific transforms |
| **Date**      | YYYY-MM-DD                                                                |
| **Authors**   | CIO (primary), CDO, Frontend Lead, Mobile Leads                           |
| **Reviewers** | CTO (technology)                                                          |

---

## Decision

We will use **Amazon Style Dictionary** with JSON as the single source of truth to generate platform-specific design tokens: CSS custom properties (web), Swift UIColor extensions (iOS), and Android XML resources (Android).

## Rationale

Full-stack cross-platform products require consistent visual design across web, iOS, and Android. Manual design implementation leads to inconsistencies: different color values, typography scales, spacing units, and animation timings across platforms. This creates a fragmented user experience and increases maintenance burden when design updates occur. This ADR establishes a unified design token pipeline that generates platform-specific design tokens from a single source of truth.

### 1. Design Token Format: Style Dictionary (JSON)

**Technology:** Amazon Style Dictionary

**Rationale:**

- **Platform-agnostic** — Single JSON source generates CSS custom properties, iOS UIColor/Android ColorRes, Swift constants, Kotlin resources
- **Transformation pipeline** — Automatic conversion of token values to platform-specific formats (hex → UIColor, px → dp/sp)
- **Versioning** — Tokens versioned alongside code, enabling rollback if design changes cause issues
- **Figma integration** — Sync tokens from Figma design files via plugins (Figma Tokens, Supernova)

**Token Structure:**

```json
{
  "color": {
    "primary": {
      "500": { "value": "#3B82F6", "type": "color" },
      "600": { "value": "#2563EB", "type": "color" }
    },
    "neutral": {
      "100": { "value": "#F3F4F6", "type": "color" },
      "900": { "value": "#111827", "type": "color" }
    }
  },
  "spacing": {
    "xs": { "value": "4px", "type": "dimension" },
    "sm": { "value": "8px", "type": "dimension" },
    "md": { "value": "16px", "type": "dimension" },
    "lg": { "value": "24px", "type": "dimension" }
  },
  "typography": {
    "heading": {
      "h1": {
        "fontSize": { "value": "32px", "type": "dimension" },
        "fontWeight": { "value": "700", "type": "number" },
        "lineHeight": { "value": "40px", "type": "dimension" }
      }
    },
    "body": {
      "md": {
        "fontSize": { "value": "16px", "type": "dimension" },
        "fontWeight": { "value": "400", "type": "number" }
      }
    }
  },
  "animation": {
    "duration": {
      "fast": { "value": "150ms", "type": "duration" },
      "normal": { "value": "300ms", "type": "duration" },
      "slow": { "value": "500ms", "type": "duration" }
    },
    "easing": {
      "ease-in-out": {
        "value": "cubic-bezier(0.4, 0, 0.2, 1)",
        "type": "cubicBezier"
      }
    }
  }
}
```

---

### 2. Platform-Specific Token Generation

**Style Dictionary Configuration:**

#### Web: CSS Custom Properties

```javascript
// config/web.js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "clients/web/src/tokens/",
      files: [
        {
          destination: "design-tokens.css",
          format: "css/variables",
        },
      ],
    },
  },
};
```

**Generated Output:**

```css
/* clients/web/src/tokens/design-tokens.css */
:root {
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-900: #111827;

  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;

  --typography-heading-h1-font-size: 32px;
  --typography-heading-h1-font-weight: 700;
  --typography-heading-h1-line-height: 40px;

  --animation-duration-fast: 150ms;
  --animation-duration-normal: 300ms;
  --animation-easing-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

#### iOS: Swift UIColor Extensions

```javascript
// config/ios.js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    ios: {
      transformGroup: "ios",
      buildPath: "clients/ios/Sources/DesignTokens/",
      files: [
        {
          destination: "DesignTokens.swift",
          format: "ios-swift/class.swift",
        },
      ],
    },
  },
};
```

**Generated Output:**

```swift
// clients/ios/Sources/DesignTokens/DesignTokens.swift
import UIKit

public struct ColorToken {
    public static let primary500 = UIColor(red: 0.231, green: 0.510, blue: 0.965, alpha: 1.0)
    public static let primary600 = UIColor(red: 0.145, green: 0.380, blue: 0.922, alpha: 1.0)
    public static let neutral100 = UIColor(red: 0.953, green: 0.957, blue: 0.965, alpha: 1.0)
    public static let neutral900 = UIColor(red: 0.067, green: 0.094, blue: 0.145, alpha: 1.0)
}

public struct SpacingToken {
    public static let xs: CGFloat = 4.0
    public static let sm: CGFloat = 8.0
    public static let md: CGFloat = 16.0
    public static let lg: CGFloat = 24.0
}

public struct TypographyToken {
    public struct Heading {
        public static let h1FontSize: CGFloat = 32.0
        public static let h1FontWeight: UIFont.Weight = .bold
        public static let h1LineHeight: CGFloat = 40.0
    }
}

public struct AnimationToken {
    public static let durationFast = 0.15
    public static let durationNormal = 0.3
    public static let durationSlow = 0.5
}
```

#### Android: Kotlin Resources

```javascript
// config/android.js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    android: {
      transformGroup: "android",
      buildPath: "clients/android/app/src/main/res/",
      files: [
        {
          destination: "values/colors.xml",
          format: "android/resources",
          filter: {
            attributes: { category: "color" },
          },
        },
        {
          destination: "values/dimens.xml",
          format: "android/resources",
          filter: {
            attributes: { category: "dimension" },
          },
        },
      ],
    },
  },
};
```

**Generated Output:**

```xml
<!-- clients/android/app/src/main/res/values/colors.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="color_primary_500">#3B82F6</color>
    <color name="color_primary_600">#2563EB</color>
    <color name="color_neutral_100">#F3F4F6</color>
    <color name="color_neutral_900">#111827</color>
</resources>

<!-- clients/android/app/src/main/res/values/dimens.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <dimen name="spacing_xs">4dp</dimen>
    <dimen name="spacing_sm">8dp</dimen>
    <dimen name="spacing_md">16dp</dimen>
    <dimen name="spacing_lg">24dp</dimen>

    <dimen name="typography_heading_h1_font_size">32sp</dimen>
    <dimen name="typography_heading_h1_line_height">40sp</dimen>
</resources>
```

---

### 3. Drift Detection & Synchronization

**Problem:** Designer updates token in Figma, but engineers haven't regenerated platform tokens → visual inconsistency.

**Solution:** Automated drift detection + CI gate enforcement.

**Drift Detection Workflow:**

```yaml
# .github/workflows/design-token-sync.yml
name: Design Token Drift Detection

on:
  push:
    paths:
      - "tokens/**/*.json"
  schedule:
    - cron: "0 9 * * 1" # Weekly check on Mondays

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate tokens for all platforms
        run: |
          npx style-dictionary build --config config/web.js
          npx style-dictionary build --config config/ios.js
          npx style-dictionary build --config config/android.js

      - name: Check for uncommitted changes
        run: |
          if [[ -n $(git status --porcelain) ]]; then
            echo "❌ Design token drift detected!"
            echo "Generated tokens differ from committed versions."
            echo "Run 'npx style-dictionary build' locally and commit changes."
            git diff
            exit 1
          fi
          echo "✅ No drift detected. All platforms in sync."

      - name: Compare with Figma (if Figma Tokens plugin configured)
        run: |
          npx figma-tokens sync --token ${{ secrets.FIGMA_TOKEN }} --file-id ${{ secrets.FIGMA_FILE_ID }}
          # If Figma tokens differ from local tokens, alert team
```

**Alert Thresholds:**

- **Critical:** Token value changed but not regenerated for any platform → CI fails
- **Warning:** Token added but not used in any platform → Slack notification to designers + engineers
- **Info:** Token unused for >90 days → Quarterly audit flag for potential removal

---

### 4. Per-Platform Token Mapping

**Challenge:** Different platforms use different units/conventions for the same concept.

**Mapping Strategy:**

| Token Type  | Web (CSS) | iOS (Swift)        | Android (Kotlin)      | Transformation Rule                   |
| ----------- | --------- | ------------------ | --------------------- | ------------------------------------- |
| Color       | `#3B82F6` | `UIColor(r,g,b,a)` | `Color.parseColor`    | Hex → RGB conversion                  |
| Spacing     | `4px`     | `4.0` (points)     | `4dp`                 | px → points (iOS), px → dp (Android)  |
| Font Size   | `16px`    | `16.0` (points)    | `16sp`                | px → points (iOS), px → sp (Android)  |
| Duration    | `150ms`   | `0.15` (seconds)   | `150L` (milliseconds) | ms → seconds (iOS), keep ms (Android) |
| Font Weight | `700`     | `.bold`            | `Typeface.BOLD`       | Numeric → enum mapping                |

**Accessibility Scaling:**

iOS Dynamic Type and Android font scaling must be respected:

```swift
// iOS: Respect Dynamic Type
let fontSize = TypographyToken.heading.h1FontSize * UIFont.preferredFont(forTextStyle: .title1).pointSize / 17.0
```

```kotlin
// Android: Respect font scaling
val fontSize = resources.getDimensionPixelSize(R.dimen.typography_heading_h1_font_size)
val scaledFontSize = fontSize * resources.configuration.fontScale
```

---

### 5. Versioning & Backward Compatibility

**Token Versioning Strategy:**

| Change Type           | Version Bump        | Examples                                | Migration Required?     |
| --------------------- | ------------------- | --------------------------------------- | ----------------------- |
| Breaking change       | Major (1→2)         | Remove token, rename token, change type | Yes                     |
| Non-breaking addition | Minor (1.0→1.1)     | Add new token, add token variant        | No                      |
| Value adjustment      | Patch (1.0.0→1.0.1) | Change color hex, adjust spacing value  | No (visual update only) |

**Deprecation Policy:**

- **Deprecated tokens** marked with `deprecated: true` metadata
- **Grace period:** 90 days before removal
- **Migration guide:** Published alongside deprecation announcement
- **Linting warning:** Style Dictionary warns when deprecated token is used

**Example:**

```json
{
  "color": {
    "legacy-blue": {
      "value": "#0000FF",
      "type": "color",
      "deprecated": true,
      "deprecationMessage": "Use color.primary.500 instead",
      "deprecatedSince": "2026-01-01",
      "removeAfter": "2026-04-01"
    }
  }
}
```

---

## Alternatives Considered

### Alternative 1: Manual Token Management (No Automation)

**Pros:** Full control, no tooling complexity  
**Cons:** Drift between platforms, manual updates error-prone, designer-engineer handoff friction  
**Rejected because:** Violates principle of "single source of truth"; manual synchronization doesn't scale beyond 10 tokens.

### Alternative 2: Figma Variables Only (No Code Generation)

**Pros:** Designers work directly in Figma, real-time preview  
**Cons:** No programmatic access in code, requires manual transcription to CSS/Swift/Kotlin  
**Rejected because:** Engineers need typed tokens in code for autocomplete, compile-time validation, refactoring support.

### Alternative 3: CSS-in-JS Shared Library (Web-Only)

**Pros:** Type-safe tokens for web, easy sharing via npm  
**Cons:** Doesn't solve iOS/Android token consistency, web-centric approach  
**Rejected because:** Full-stack product requires cross-platform consistency; web-only solution creates fragmentation.

---

## Consequences

### Positive

- **Visual consistency** — Same color, spacing, typography across web, iOS, Android
- **Designer-engineer alignment** — Single source of truth eliminates translation errors
- **Rapid iteration** — Designer updates token in Figma → all platforms updated in <5 minutes
- **Accessibility compliance** — Centralized control over font scaling, color contrast ratios

### Negative

- **Initial setup cost** — Style Dictionary configuration, CI/CD integration (~2 weeks effort)
- **Learning curve** — Designers must understand token structure, engineers must understand transformation pipeline
- **Build overhead** — Token generation adds ~30 seconds to CI pipeline

### Risks & Mitigations

| Risk                                  | Likelihood | Impact | Mitigation                                                                             |
| ------------------------------------- | ---------- | ------ | -------------------------------------------------------------------------------------- |
| Token drift (Figma ≠ code)            | High       | High   | Automated drift detection CI gate, weekly sync checks, alert on mismatch               |
| Breaking token changes                | Medium     | Medium | Deprecation policy with 90-day grace period, linting warnings, migration guides        |
| Platform-specific edge cases          | Medium     | Low    | Per-platform transformation rules documented, manual override mechanism for exceptions |
| Performance impact (large token sets) | Low        | Low    | Tree-shaking unused tokens, code-splitting by feature module                           |

---

## Implementation Plan

**Phase 1 (Week 1-2):** Token definition

- Audit existing design system (colors, spacing, typography, animations)
- Define token taxonomy (naming convention, hierarchy)
- Create initial JSON token files

**Phase 2 (Week 3-4):** Style Dictionary setup

- Configure Style Dictionary for web, iOS, Android
- Set up transformation pipelines (hex → UIColor, px → dp/sp)
- Generate first version of platform-specific tokens

**Phase 3 (Week 5-6):** Figma integration

- Install Figma Tokens plugin
- Sync Figma variables with JSON token files
- Set up automated sync workflow (Figma → GitHub)

**Phase 4 (Week 7-8):** Drift detection & governance

- Implement CI gate for drift detection
- Document token lifecycle (creation, usage, deprecation, removal)
- Train designers + engineers on token workflow

---

## Compliance Alignment

- **WCAG 2.1 AA:** Centralized color contrast ratio validation (ensure all color combinations meet 4.5:1 ratio)
- **SRD Section 10.2:** "Design token pipeline with per-platform accessibility scaling (Dynamic Type, font scaling)"
- **IDS.md:** "Design tokens defined in IDS must be operationalized via automated pipeline"

---

## References

- [Amazon Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Figma Tokens Plugin](https://www.figma.com/community/plugin/843461159747178978)
- [Design Tokens W3C Community Group](https://design-tokens.github.io/community-group/)
- SRD.md Section 10.2 (Design Token Accessibility), IDS.md (Interaction Design Specification)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
