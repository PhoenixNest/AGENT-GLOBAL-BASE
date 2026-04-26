---
version: "1.0.0"
---

| Competency      | Description                                                                                               | Quality Criteria                                                                                                                                        |
| --------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WidgetKit       | Widget configuration, timeline providers, placeholder views, deep links, widget families, reloads         | Widgets display accurate data via timeline; placeholder matches loaded state; deep links navigate to correct app screen; supports all widget families   |
| App Intents     | Intent definition, parameter handling, Siri shortcuts, App Shortcuts, dynamic options, confirmation       | Intents properly defined with parameters; Siri suggestions contextual; dynamic options load efficiently; confirmation provides feedback                 |
| Share Extension | Share view controller, item handling, NSExtensionItem, SLComposeServiceViewController, content processing | All shareable content types handled; content processed in background; extension UI matches app design; proper error handling                            |
| Today Extension | Notification center widget, NCWidgetProviding, expanded/collapsed modes, quick actions                    | Today extension displays at-a-glance info; expanded mode for detailed content; quick actions launch app with context                                    |
| App Groups      | Shared container, UserDefaults suite, file sharing, Core Data sharing, real-time sync                     | App group configured in entitlements; shared data accessed correctly; file coordination for concurrent access; Core Data sharing with separate contexts |

## Pipeline Integration

- **Stage 4 (Implementation Plan):** Extension development tasks included: WidgetKit setup, App Intents definition, Share Extension configuration, App Groups entitlement.
- **Stage 5 (Development):** Primary skill for iOS extension development. All widgets, intents, and extensions built with proper data sharing.
- **Stage 6 (Code Review):** Extension review: timeline accuracy, App Intent parameter handling, Share Extension content processing, App Groups data integrity.
- **Stage 8 (Integrity Verification):** All extensions tested on target devices. Widget timeline accuracy verified. App Intents tested with Siri.

## Quality Standards

- Widget timeline entries cover **minimum 6 hours** with appropriate refresh policy
- Widget placeholder view **matches loaded state** visually — no jarring transition
- All widget families supported (**systemSmall, systemMedium, systemLarge**) unless design restricts
- App Intents have **meaningful phrases** for Siri — at least 2 phrase variations per intent
- Share Extension handles **URL, image, and text** content types at minimum
- App Groups configured in **entitlements** for main app and all extensions
- Shared data accessed via **file coordination** when concurrent access possible
- Widget data saved to **shared container** — widget never makes network requests directly
- App Intent confirmation provides **dialogue feedback** — silent intents are confusing
- Share Extension processes content in **background** — UI responsive during processing
- Today Extension supports both **expanded and collapsed** display modes

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
