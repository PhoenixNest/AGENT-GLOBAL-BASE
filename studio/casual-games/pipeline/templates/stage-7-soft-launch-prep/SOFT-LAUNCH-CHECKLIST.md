# Soft Launch Preparation Checklist — Stage 7

> **Stage:** 7 — Soft Launch Prep
> **Producer:** Studio Director (Dr. Marcus Vogel) + Live Ops Lead
> **User Approval:** ✅ Required before advancing to Stage 8

---

## 1. Store Metadata

### App Store (iOS)

| Item                              | Status | Notes |
| :-------------------------------- | :----: | :---- |
| App name finalised                |   ☐    |       |
| App subtitle                      |   ☐    |       |
| Description (short + long)        |   ☐    |       |
| Keywords list                     |   ☐    |       |
| Screenshots (all required sizes)  |   ☐    |       |
| App preview video (optional)      |   ☐    |       |
| Privacy nutrition label complete  |   ☐    |       |
| App rating questionnaire complete |   ☐    |       |
| Age rating selected               |   ☐    |       |

### Google Play (Android)

| Item                           | Status | Notes |
| :----------------------------- | :----: | :---- |
| App title                      |   ☐    |       |
| Short description (80 chars)   |   ☐    |       |
| Full description               |   ☐    |       |
| Feature graphic                |   ☐    |       |
| Screenshots (phone + tablet)   |   ☐    |       |
| Promo video (optional)         |   ☐    |       |
| Data safety section complete   |   ☐    |       |
| Content rating questionnaire   |   ☐    |       |
| Sensitive permissions declared |   ☐    |       |

---

## 2. Analytics and Telemetry

| Requirement                                                        | Status | Notes |
| :----------------------------------------------------------------- | :----: | :---- |
| Analytics SDK initialised and sending events                       |   ☐    |       |
| Core events tracked (session start/end, level start/fail/complete) |   ☐    |       |
| Economy events tracked (currency earn, spend, IAP)                 |   ☐    |       |
| Retention events tracked (D1/D7/D30 cohort setup)                  |   ☐    |       |
| Funnel events tracked (onboarding completion, tutorial steps)      |   ☐    |       |
| Crash reporting active (Firebase Crashlytics or equivalent)        |   ☐    |       |
| Event validation confirmed in dashboard                            |   ☐    |       |
| No PII in event parameters                                         |   ☐    |       |

---

## 3. Monetisation Configuration

| Requirement                                      | Status | Notes |
| :----------------------------------------------- | :----: | :---- |
| All IAP products created in App Store Connect    |   ☐    |       |
| All IAP products created in Google Play Console  |   ☐    |       |
| IAP prices correct in all soft launch markets    |   ☐    |       |
| Server-side receipt validation live and tested   |   ☐    |       |
| Rewarded ad placements configured and tested     |   ☐    |       |
| Ad mediation initialisation tested               |   ☐    |       |
| No-ads IAP (if applicable) removes ads correctly |   ☐    |       |

---

## 4. User Acquisition Configuration (UAC)

| Requirement                                  | Status | Notes     |
| :------------------------------------------- | :----: | :-------- |
| UA budget for soft launch approved           |   ☐    | $[X,XXX]  |
| Target soft launch markets selected          |   ☐    | [Markets] |
| UA creative assets produced (video + static) |   ☐    |           |
| SKAdNetwork (iOS) attribution configured     |   ☐    |           |
| MMP (mobile measurement partner) integrated  |   ☐    |           |
| UA campaigns created (hold, do not activate) |   ☐    |           |

---

## 5. CSO Security Gate (Soft Launch)

| Requirement                                                | Status | CSO Sign-off |
| :--------------------------------------------------------- | :----: | :----------: |
| Penetration test completed                                 |   ☐    |      ☐       |
| All pentest findings P0/P1 resolved                        |   ☐    |      ☐       |
| GDPR consent flows tested in EU markets                    |   ☐    |      ☐       |
| CCPA opt-out flow tested (if US market included)           |   ☐    |      ☐       |
| Privacy policy URL live and current                        |   ☐    |      ☐       |
| Third-party SDK data collection declared in store listings |   ☐    |      ☐       |

**CSO Sign-off:** [Dr. Sarah Chen] — ☐ Approved / ☐ Approved with conditions / ☐ Rejected

---

## 6. Technical Readiness

| Requirement                                           | Status | Notes |
| :---------------------------------------------------- | :----: | :---- |
| Build passes all Stage 6 test criteria                |   ☐    |       |
| Backend infrastructure scaled for soft launch traffic |   ☐    |       |
| On-call rotation established                          |   ☐    |       |
| Incident response plan in place                       |   ☐    |       |
| Rollback plan defined                                 |   ☐    |       |

---

## 7. Stage 7 Gate Decision

| All items above complete?      | ☐ Yes / ☐ No                      |
| :----------------------------- | :-------------------------------- |
| CSO approved?                  | ☐ Yes / ☐ No                      |
| Studio Director recommendation | ☐ Proceed to Soft Launch / ☐ Hold |

**Notes:** [Any outstanding items or conditions]

---

**Produced by:** [Live Ops Lead] on YYYY-MM-DD
**CSO Sign-off:** [Dr. Sarah Chen] on YYYY-MM-DD
**Studio Director Sign-off:** [Dr. Marcus Vogel] on YYYY-MM-DD
**Awaiting User (CEO) approval to launch.**
