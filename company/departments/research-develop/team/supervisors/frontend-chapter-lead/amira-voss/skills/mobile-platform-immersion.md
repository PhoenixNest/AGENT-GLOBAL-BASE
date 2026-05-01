---
name: mobile-platform-immersion
description: Mobile platform immersion for a frontend/web engineer — understanding iOS and Android platform constraints, WebView behaviour differences, PWA capabilities and limitations, mobile browser engine fragmentation (WebKit vs Blink), and how to collaborate effectively with the iOS and Android native engineers. Use when designing a mobile web feature that must behave consistently across iOS Safari and Android Chrome, when evaluating PWA vs native trade-offs, or when debugging a platform-specific rendering issue.
version: "1.0.0"
---

# Mobile Platform Immersion

## Purpose

Amira Voss leads the frontend chapter for web products but works alongside native iOS and Android engineers who own the mobile app surfaces. This skill ensures she understands mobile platform constraints well enough to: (1) design web features that behave correctly on both platforms, (2) collaborate effectively with the KMP/iOS/Android VPs and chapter leads, and (3) make informed platform trade-off recommendations in Stage 3 architectural discussions.

## Browser Engine Landscape

| Platform                 | Browser                              | Engine                          | Key Constraints                                                                       |
| ------------------------ | ------------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------- |
| iOS (all browsers)       | Safari, Chrome, Firefox, Edge        | WebKit only (mandated by Apple) | No cross-browser testing independence; what breaks in Safari breaks everywhere on iOS |
| Android                  | Chrome                               | Blink                           | Generally the latest APIs; fastest to support new web platform features               |
| Android                  | Samsung Internet                     | Blink (fork)                    | Occasionally behind Chrome; relevant for Samsung device users                         |
| Android                  | Firefox                              | Gecko                           | Small market share but important for EU users citing privacy preferences              |
| In-app WebView (iOS)     | WKWebView                            | WebKit                          | JavaScript engine restrictions; cookie sharing with Safari depends on iOS version     |
| In-app WebView (Android) | Android WebView / Chrome Custom Tabs | Blink                           | Auto-updates with Chrome; Custom Tabs share the Chrome cookie jar                     |

**Practical rule:** Any new API Amira proposes must have a caniuse.com check confirming iOS Safari support. If iOS Safari does not support it, a polyfill or fallback is required before the feature is eligible for Stage 5 development.

## WebKit (iOS Safari) Constraints

iOS Safari has several notable restrictions that affect web product design:

| Constraint                     | Impact                                                                                | Mitigation                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Input field zoom**           | iOS auto-zooms if input font-size < 16px                                              | Set `font-size: 16px` on all form inputs                                |
| **Position: fixed + keyboard** | Virtual keyboard changes viewport; fixed elements reposition incorrectly              | Use `env(safe-area-inset-*)` and test with keyboard open                |
| **PWA full-screen gaps**       | iOS PWA has safe areas at top/bottom                                                  | Use `viewport-fit=cover` + safe-area insets                             |
| **WebAudio autoplay**          | Audio requires user gesture on iOS                                                    | Always require user interaction before audio playback                   |
| **Viewport height (dvh)**      | `100vh` includes the browser UI on iOS; `100dvh` (dynamic viewport height) is the fix | Use `100dvh` where `100vh` is intended for full-screen layouts          |
| **IndexedDB in Safari ITP**    | Cross-origin IndexedDB blocked by Intelligent Tracking Prevention                     | Avoid cross-origin storage; use first-party storage paths               |
| **Service Worker API**         | Available on iOS 16.4+ only in PWA context                                            | PWA offline support only for iOS 16.4+; web fallback for older versions |

## PWA Capabilities and Limitations

The company's web products may be distributed as PWAs in addition to native apps. Amira advises on PWA feasibility:

| PWA Feature                      | Android (Chrome) | iOS (Safari 16.4+)     | Recommendation                                  |
| -------------------------------- | ---------------- | ---------------------- | ----------------------------------------------- |
| Offline support (Service Worker) | ✅ Full          | ✅ PWA context only    | Implement; flag iOS restriction in PRD          |
| Push notifications               | ✅               | ✅ iOS 16.4+ PWA only  | Implement; document iOS requirement in PRD      |
| Home screen install              | ✅ Native prompt | Manual via Share sheet | Brief user in onboarding; no auto-prompt on iOS |
| Background sync                  | ✅               | ❌                     | Design with degraded iOS fallback               |
| File system access               | ✅               | Limited                | Test per feature; fallback required             |
| WebAuthn (passkeys)              | ✅               | ✅                     | Good support; use for auth flows                |

## Collaboration with Native Engineering Chapter Leads

Amira's web products frequently need to match or complement the native app surfaces. Her collaboration points:

| Collaboration              | With                                                              | Process                                                                                                   |
| -------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Deep link consistency**  | VP Mobile (Marcus Andersson) + iOS/Android chapter leads          | Shared URL scheme document; web and native handle the same routes identically                             |
| **Shared authentication**  | Backend Chapter Lead (Dev Malhotra) + VP Platform (David Okonkwo) | Web uses the same OAuth2/PKCE flow as native; token storage in memory for web (not localStorage)          |
| **Design token parity**    | CDO (Yuki Tanaka-Chen) via IDS                                    | Web and native use the same token values; any platform-specific token divergence is documented in the IDS |
| **Feature flag parity**    | VP Platform (David Okonkwo)                                       | Web and native app use the same feature flag system; Amira ensures web respects the same flags            |
| **Analytics event parity** | CPO (Marcus Tran-Yoshida) + VP Quality (Aisha Patel)              | Web events named identically to native events; verified in Stage 7 automated testing                      |

## Mobile Testing Device Matrix

Before any Stage 6 (Code Review) approval, Amira ensures the following device/browser matrix is tested:

| Priority | Device                 | OS         | Browser                   | Why                                                  |
| -------- | ---------------------- | ---------- | ------------------------- | ---------------------------------------------------- |
| P0       | iPhone 15 / 16         | iOS 17+    | Safari                    | Largest iOS segment                                  |
| P0       | Pixel 9                | Android 14 | Chrome                    | Android baseline                                     |
| P1       | iPhone SE (2nd gen)    | iOS 16     | Safari                    | Smallest supported screen; WebKit constraint testing |
| P1       | Samsung Galaxy S24     | Android 14 | Chrome + Samsung Internet | Samsung market share                                 |
| P2       | iPad (latest)          | iPadOS 17  | Safari                    | Tablet layout testing                                |
| P2       | Older Android (API 30) | Android 11 | Chrome                    | Low-end device performance                           |

## Quality Standards

- caniuse.com verified for all new APIs before Stage 3 sign-off; no API approved without iOS Safari support or documented fallback
- Device test matrix completed before every Stage 6 approval for any UI feature
- PWA capabilities documented in PRD with explicit platform-specific notes before Stage 1 sign-off
- WebKit constraint checklist reviewed whenever a new input field, modal, or layout pattern is introduced
