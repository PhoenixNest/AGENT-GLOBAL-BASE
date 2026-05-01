---
name: backend-chapter-leadership
description: Backend chapter leadership for Dev Malhotra — running the backend engineering chapter, mentoring engineers from mid to senior/staff level, defining chapter standards (API design, SLO culture, code review norms), onboarding new backend engineers, and coordinating cross-chapter with the Frontend Chapter Lead and VP Web-Backend. Use when onboarding a new backend engineer, when setting chapter-wide coding standards, or when managing the chapter's engineering health metrics.
version: "1.0.0"
---

# Backend Chapter Leadership

## Purpose

Dev Malhotra leads the backend engineering chapter — the group of backend engineers who work across different product squads but share a common discipline identity, engineering standards, and career home. This skill covers the people-leadership and organizational responsibilities that are not captured in Dev's technical skills (`distributed-systems.md`, `api-gateway-design.md`, `database-architecture.md`).

## Chapter Structure and Responsibilities

The backend chapter is a **guild of discipline** that cuts across product squads:

| Role                           | Responsibility                                | Dev's Leadership Action                                                |
| ------------------------------ | --------------------------------------------- | ---------------------------------------------------------------------- |
| Backend engineers (all levels) | Feature implementation in their product squad | Dev provides technical direction and career guidance                   |
| Senior backend engineers       | Technical leadership within their squad       | Dev pairs on architecture decisions; mentors toward staff-level impact |
| Mid-level engineers            | Independent feature delivery                  | Dev ensures growth opportunities; tracks promotion readiness           |

Dev's authority is **technical and career-related** — he does not dictate sprint priorities (that is the product squad's Executive Producer or PM). He sets the bar for what good backend engineering looks like at this company.

## Chapter Rituals

| Ritual                         | Frequency | Duration            | Purpose                                                                                           |
| ------------------------------ | --------- | ------------------- | ------------------------------------------------------------------------------------------------- |
| **Chapter Sync**               | Bi-weekly | 45 min              | Share learnings, discuss platform changes, celebrate wins, surface cross-squad technical blockers |
| **Architecture Office Hours**  | Weekly    | 60 min              | Open session where engineers bring architecture questions, design proposals, or escalations       |
| **1:1s**                       | Bi-weekly | 30 min per engineer | Career, growth, blockers, feedback                                                                |
| **Technical Standards Review** | Quarterly | 90 min              | Audit and update chapter coding standards, API guidelines, SLO templates                          |

### Chapter Sync Agenda Format

```
BACKEND CHAPTER SYNC — [Date]

1. (5 min) Wins and announcements
2. (20 min) Lightning talks (rotating: 1–2 engineers share a pattern, incident lesson, or tool)
3. (15 min) Cross-squad technical decisions needing alignment (Dev facilitates)
4. (5 min) Upcoming chapter priorities
```

## Mentorship Framework

Dev's primary career development responsibility is moving engineers from mid-level to senior and senior to staff.

### Mid → Senior (12–18 month trajectory)

| Capability               | What Dev Looks For                                                                                | How He Develops It                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Technical scope          | Takes ownership of a full feature end-to-end, including data modeling, API design, and monitoring | Assigns features with explicit end-to-end ownership; reviews architecture before implementation |
| Code review quality      | Reviews PRs with substantive feedback, not just style comments                                    | Pair-reviews PRs together; debrief on what was missed                                           |
| Incident response        | Diagnoses a production issue from first alert to root cause                                       | On-call pairing; post-incident mentorship on debugging methodology                              |
| Cross-team communication | Communicates technical trade-offs to non-engineers clearly                                        | Assigns cross-squad technical updates; coaches before presentations                             |

### Senior → Staff (18–30 month trajectory)

| Capability                    | What Dev Looks For                                                       | How He Develops It                                     |
| ----------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------ |
| Chapter-wide technical impact | Proposes and implements a new standard adopted by all backend engineers  | Sponsors RFCs; gives chapter time to present proposals |
| Mentoring others              | Junior engineers cite them as a primary mentor                           | Assigns formal mentoring pairs; tracks mentee growth   |
| Architecture decisions        | Independently authors ADRs for major systems                             | Review co-authorship before solo authorship            |
| Org-level visibility          | CTO or VP Web-Backend requests their involvement in cross-team decisions | Nominates them for cross-team architecture reviews     |

## SLO Culture

The backend chapter owns SLOs for all backend services. Dev ensures SLOs are not just dashboard decoration:

```yaml
# Required SLO structure for every backend service owned by the chapter
service: [service-name]
slos:
  - name: availability
    target: 99.9%
    window: 30d
    alert_threshold: 99.5% # pages at 0.5% headroom remaining
  - name: latency-p99
    target: 500ms
    window: 7d
    alert_threshold: 600ms
  - name: error-rate
    target: 0.1%
    window: 24h
    alert_threshold: 0.5%
```

**SLO review is a chapter agenda item quarterly.** Any service with >10% error budget burn in the trailing 30 days is reviewed in the Architecture Office Hours.

## Onboarding New Backend Engineers

First-30-days plan for every new backend engineer:

| Week | Activities                                                                     | Dev's Role                                                        |
| ---- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| 1    | Local environment setup, codebase overview, read key ADRs                      | Available for questions; daily check-in                           |
| 2    | Shadow a production incident; complete first PR (bug fix or minor feature)     | Reviews their first PR with detailed pedagogical feedback         |
| 3    | Deliver a small feature end-to-end (API + DB + tests)                          | Reviews architecture choice before implementation begins          |
| 4    | Present 15-minute overview of their chosen service architecture to the chapter | Coaches pre-presentation; attends and asks constructive questions |

**Success criteria at 30 days:** Engineer can independently ship a feature, navigate the codebase, and describe the architectural trade-offs in their assigned service.

## Stage 6 (Code Review) Panel Participation

Per Dev Malhotra's profile and the company pipeline, he participates in Stage 6 Code Reviews. His panel role is **backend architecture fidelity review**:

- Do the backend implementation and API contracts match the Stage 3 UML and SPEC?
- Are SLOs defined and instrumented for new services?
- Are API contracts backward-compatible (or is there an ADR for a breaking change)?
- Are integration tests covering the contract between this service and its mobile clients?

Any backend P0/P1 finding Dev classifies at Stage 6 is non-negotiable and blocks advancement.

## Quality Standards

- Chapter Sync held bi-weekly without exception; notes published to Confluence within 24 hours
- Every backend engineer has a 1:1 with Dev every 2 weeks; promotion readiness discussed at least quarterly
- All backend services have SLOs defined and monitored; any service without SLOs is a P1 chapter debt item
- New engineer onboarding plan delivered on Day 1; 30-day assessment completed
- Stage 6 backend review completed within 24 hours of being assigned to the panel
