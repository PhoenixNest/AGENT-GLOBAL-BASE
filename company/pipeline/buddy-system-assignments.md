# Buddy System Assignments — Pipeline Expansion

**Date:** April 13, 2026
**Owner:** VP Engineering + HR (Grace Muthoni)
**Applicability:** All new pipelines (Web, Backend API, Full-Stack Cross-Platform)
**Duration:** 90-day ramp-up per engineer (Day 30/60/90 checkpoints)

---

## Purpose

Seven engineers hired with 12/20 vetting scores require structured mentorship. Each buddy pair has 30/60/90-day checkpoints with defined skill targets. Buddies conduct paired code reviews, architecture discussions, and skill gap remediation.

---

## Web Application Pipeline (P1) — Buddy Assignments

| Junior Engineer          | Score | Buddy (Senior)          | Buddy Score | Pipeline Track | 30-Day Target                        | 60-Day Target                       | 90-Day Target                   |
| ------------------------ | ----- | ----------------------- | ----------- | -------------- | ------------------------------------ | ----------------------------------- | ------------------------------- |
| **Yuna Park** (Frontend) | 12/20 | Elena Kim (Sr Frontend) | 18/20       | Track W-FE     | React patterns, Next.js SSR/SSG      | State management, performance opt   | Independent component ownership |
| **Ingrid Nilsen** (BE)   | 12/20 | Aisha Mohammed (Sr BE)  | 15/20       | Track W-BE     | Node.js/TypeScript API patterns      | Database design, migration patterns | Independent endpoint delivery   |
| **Marcus Wright** (FS)   | 12/20 | Nina Petrova (Sr FS)    | 15/20       | Track W-FS     | Full-stack flow, deployment pipeline | Integration patterns, CI/CD         | Cross-layer task ownership      |

## Backend API Pipeline (P2) — Buddy Assignments

| Junior Engineer        | Score | Buddy (Senior)         | Buddy Score | Pipeline Track | 30-Day Target                         | 60-Day Target                      | 90-Day Target                   |
| ---------------------- | ----- | ---------------------- | ----------- | -------------- | ------------------------------------- | ---------------------------------- | ------------------------------- |
| **Omar Hassan** (BE)   | 12/20 | Viktor Horvath (Sr BE) | 15/20       | Track B-API    | Go REST API patterns, testing         | Microservices, event-driven design | Independent service delivery    |
| **Ingrid Nilsen** (BE) | 12/20 | Aisha Mohammed (Sr BE) | 15/20       | Track B-DATA   | PostgreSQL schema design, migrations  | Read replicas, caching patterns    | Independent data layer delivery |
| **Thabo Mokoena** (BE) | 12/20 | Kael Jensen (Sr BE)    | 15/20       | Track B-RT     | WebSocket patterns, real-time systems | Kafka streams, observability       | Independent real-time delivery  |

## Full-Stack Cross-Platform Pipeline (P3) — Buddy Assignments

| Junior Engineer          | Score | Buddy (Senior)          | Buddy Score | Pipeline Track | 30-Day Target                       | 60-Day Target                        | 90-Day Target                    |
| ------------------------ | ----- | ----------------------- | ----------- | -------------- | ----------------------------------- | ------------------------------------ | -------------------------------- |
| **Yuna Park** (Frontend) | 12/20 | Elena Kim (Sr Frontend) | 18/20       | Track FS-WFE   | React patterns, cross-platform UI   | Performance optimization, a11y       | Independent web delivery         |
| **Marcus Wright** (FS)   | 12/20 | Nina Petrova (Sr FS)    | 15/20       | Track FS-INT   | Cross-platform integration patterns | Parity testing, release coordination | Independent integration delivery |

## Shared Assignments (All Pipelines)

| Junior Engineer          | Score | Buddy (Senior)         | Buddy Score | Focus Area               | Checkpoint Schedule               |
| ------------------------ | ----- | ---------------------- | ----------- | ------------------------ | --------------------------------- |
| **Tobias Weber** (SDET)  | 12/20 | Ananya Krishnan (SDET) | 15/20       | Mobile test automation   | Day 30/60/90 paired test reviews  |
| **Hiroshi Tanaka** (iOS) | 12/20 | Lars Eriksson (Sr iOS) | 17/20       | SwiftUI, UIKit migration | Day 30/60/90 SwiftUI code reviews |

---

## Buddy Protocol

### Responsibilities (Buddy)

1. **Paired code review** — Review all junior's PRs within 24 hours
2. **Architecture guidance** — Weekly 1:1 architecture discussions
3. **Skill gap remediation** — Identify specific knowledge gaps and provide resources
4. **Checkpoint assessments** — Formal 30/60/90-day evaluations with written feedback
5. **Escalation** — If junior is not progressing, escalate to VP Engineering at 60-day checkpoint

### Responsibilities (Junior)

1. **Proactive learning** — Complete assigned skill targets before each checkpoint
2. **Code quality** — Follow team standards, address all review feedback
3. **Documentation** — Maintain DEVELOPMENT-LOG.md entries with learning notes
4. **Checkpoint preparation** — Demonstrate skill targets at each checkpoint

### Checkpoint Format

| Checkpoint | Assessment Criteria        | Format                          | Outcome                                            |
| ---------- | -------------------------- | ------------------------------- | -------------------------------------------------- |
| **Day 30** | Baseline skill acquisition | Paired coding exercise + review | Pass → continue / Fail → extend 30 days            |
| **Day 60** | Independent task execution | Solo coding task + buddy review | Pass → continue / Fail → VP Engineering review     |
| **Day 90** | Full pipeline contribution | Independent feature delivery    | Pass → buddy system ends / Fail → performance plan |

---

## Tracking

Buddy system progress is tracked in:

- `company/project/<project-name>/PROGRESS.md` — Session logs note buddy pairings
- `company/project/<project-name>/sessions/` — Buddy assessment notes in session logs
- `company/project/<project-name>/checkpoints/` — Checkpoint JSON includes buddy progress field
