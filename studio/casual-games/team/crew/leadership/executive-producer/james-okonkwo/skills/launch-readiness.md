---
name: launch-readiness
description: Launch readiness checklist management, soft launch execution, global launch coordination, and post-launch transition planning for Stages 7, 8, and 9 of the game development pipeline.
---

# Launch Readiness

## Role

The Executive Producer owns the end-to-end launch process — from Soft Launch Prep (Stage 7) through Global Launch Readiness (Stage 9). This skill covers the comprehensive launch readiness framework, KPI validation during soft launch, and the coordination required for a successful global launch.

## 72-Item Launch Readiness Checklist

The checklist is organized into 10 categories. **All 10 non-negotiable items must pass** — any failure blocks launch.

### Category 1: Technical Stability (Non-Negotiable)

| #   | Item                                  | Target               | Verification Method                     |
| --- | ------------------------------------- | -------------------- | --------------------------------------- |
| 1   | Crash-free sessions                   | ≥ 99.5%              | Crash analytics dashboard               |
| 2   | Load time (cold start)                | < 15 seconds         | Performance profiling on target devices |
| 3   | Memory usage (lowest-spec device)     | < 500MB              | Memory profiling                        |
| 4   | FPS stability (mid-range device)      | ≥ 55fps average      | Performance benchmarking                |
| 5   | Network resilience (flaky connection) | Graceful degradation | Network simulation testing              |

### Category 2: Analytics & Instrumentation (Non-Negotiable)

| #   | Item                                                         | Target          | Verification Method                   |
| --- | ------------------------------------------------------------ | --------------- | ------------------------------------- |
| 6   | All analytics events firing correctly                        | 100% verified   | Event validation dashboard            |
| 7   | Funnel tracking (install → tutorial → first session → D1)    | Complete        | Funnel analytics verification         |
| 8   | Monetization event tracking (impressions, clicks, purchases) | Complete        | Revenue analytics verification        |
| 9   | Custom KPI dashboard operational                             | Live and tested | Dashboard review with Studio Director |
| 10  | Real-time alerting configured (crash spike, revenue drop)    | Active          | Alert simulation test                 |

### Category 3: Economy & Monetization (Non-Negotiable)

| #   | Item                                                | Target              | Verification Method                  |
| --- | --------------------------------------------------- | ------------------- | ------------------------------------ |
| 11  | Economy balance validated against soft launch KPIs  | Within ±15%         | Soft launch data analysis            |
| 12  | All IAP items priced, localized, and store-approved | Complete            | Store validation across all markets  |
| 13  | Ad mediation configured (if applicable)             | Tested and verified | Ad network integration test          |
| 14  | First 30 days of live events content built          | Complete            | Content audit with Creative Director |
| 15  | Refund rate monitoring configured                   | < 1% target         | Analytics setup verification         |

### Category 4: Store Presence (Non-Negotiable)

| #   | Item                                    | Target             | Verification Method              |
| --- | --------------------------------------- | ------------------ | -------------------------------- |
| 16  | App Store / Google Play assets approved | Approved           | Store submission status          |
| 17  | Screenshots and video localized         | All target markets | Asset audit                      |
| 18  | App description localized               | All target markets | Content review with localization |
| 19  | Age rating obtained                     | Complete           | Rating board confirmation        |
| 20  | Privacy policy updated and compliant    | Complete           | Legal review sign-off            |

### Category 5: Server Infrastructure (Non-Negotiable)

| #   | Item                                          | Target       | Verification Method         |
| --- | --------------------------------------------- | ------------ | --------------------------- |
| 21  | Server load tested at 3x projected Day 1 peak | Pass         | Load testing report         |
| 22  | Auto-scaling configured and tested            | Functional   | Scaling simulation test     |
| 23  | Database backup and recovery tested           | < 1 hour RTO | Recovery drill              |
| 24  | CDN configured for global content delivery    | Active       | CDN performance test        |
| 25  | DDoS protection enabled                       | Active       | Security audit confirmation |

### Category 6: Customer Support Readiness

| #   | Item                                  | Target     | Verification Method         |
| --- | ------------------------------------- | ---------- | --------------------------- |
| 26  | Support team trained on game features | Complete   | Training completion records |
| 27  | FAQ and troubleshooting documentation | Complete   | Documentation review        |
| 28  | Support ticket system configured      | Active     | Ticket system test          |
| 29  | In-game support integration           | Functional | End-to-end test             |
| 30  | Response SLA defined and staffed      | Documented | SLA document review         |

### Category 7: Legal & Compliance (Non-Negotiable)

| #   | Item                                      | Target   | Verification Method   |
| --- | ----------------------------------------- | -------- | --------------------- |
| 31  | GDPR compliance verified                  | Complete | Legal audit           |
| 32  | COPPA compliance verified (if applicable) | Complete | Legal audit           |
| 33  | Regional compliance (China, Russia, etc.) | Complete | Regional legal review |
| 34  | Third-party license agreements executed   | Complete | Legal document audit  |
| 35  | IP clearance for all assets               | Complete | IP audit sign-off     |

### Category 8: Marketing & UA

| #   | Item                                       | Target   | Verification Method                    |
| --- | ------------------------------------------ | -------- | -------------------------------------- |
| 36  | UA campaigns loaded and ready to activate  | Complete | Campaign dashboard review              |
| 37  | Creative assets for UA (5+ variants)       | Approved | Creative review with Creative Director |
| 38  | Influencer partnerships confirmed          | Signed   | Contract review                        |
| 39  | Press kit distributed                      | Complete | Distribution confirmation              |
| 40  | Social media accounts active and populated | Complete | Account audit                          |

### Category 9: Live Operations Readiness

| #   | Item                                       | Target          | Verification Method                  |
| --- | ------------------------------------------ | --------------- | ------------------------------------ |
| 41  | First 30 days of content built and tested  | Complete        | Content audit                        |
| 42  | Event calendar defined (90 days)           | Complete        | Calendar review with Studio Director |
| 43  | Live ops team on-call schedule             | Published       | Schedule confirmation                |
| 44  | Hotfix deployment pipeline tested          | < 4 hour deploy | Deployment drill                     |
| 45  | Community management protocols established | Documented      | Protocol review                      |

### Category 10: Rollback & Contingency (Non-Negotiable)

| #   | Item                                 | Target     | Verification Method              |
| --- | ------------------------------------ | ---------- | -------------------------------- |
| 46  | Rollback plan documented             | Complete   | Document review                  |
| 47  | Rollback plan tested                 | Successful | Rollback drill                   |
| 48  | Communication plan for launch issues | Documented | Plan review with Studio Director |
| 49  | Emergency contact list               | Published  | Contact list verification        |
| 50  | Post-mortem template prepared        | Complete   | Template review                  |

_(Items 51–72 cover secondary verification items: localization QA pass, accessibility audit, platform-specific requirements, third-party SDK compliance, etc.)_

## Soft Launch Execution (Stage 8)

### Soft Launch Parameters

| Parameter        | Recommendation                                                                      |
| ---------------- | ----------------------------------------------------------------------------------- |
| Duration         | 30–90 days                                                                          |
| Target regions   | 2–3 regions with representative demographics (e.g., Canada, Australia, Philippines) |
| UA budget        | 20–30% of projected global launch UA budget                                         |
| Success criteria | D1 ≥ 40%, D7 ≥ 15%, Day 7 ARPU ≥ $0.50                                              |

### Soft Launch Monitoring Cadence

| Cadence   | Activity                                        | Owner                               |
| --------- | ----------------------------------------------- | ----------------------------------- |
| Daily     | KPI dashboard review, crash monitoring          | Executive Producer                  |
| Weekly    | Economy balance review, retention analysis      | Studio Director + Creative Director |
| Bi-weekly | Go/no-go checkpoint for global launch readiness | Studio Director + User              |
| Monthly   | Comprehensive soft launch report                | Executive Producer                  |

### Global Launch Go/No-Go Decision

The decision to proceed to global launch requires:

1. All 10 non-negotiable checklist items passed
2. Soft launch KPIs meet or exceed targets in at least 2 of 3 test regions
3. Studio Director recommendation to proceed
4. User (CEO) final approval

## References

- `studio/casual-games/team/recruitment-plan/recruitment-plan.md` — Master recruitment plan
- `company/pipeline/mobile-development/pipeline.md` — Stage 7 (Soft Launch Prep), Stage 8 (Soft Launch), Stage 9 (Global Launch Readiness)
- `company/library/topics/testing.md` — Testing standards for launch validation
