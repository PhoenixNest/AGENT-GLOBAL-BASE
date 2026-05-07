---
name: architecture-syncs
description: Facilitate and document weekly architecture synchronization sessions — maintaining cross-team architectural alignment, surfacing emerging technical debt, and producing Architecture Sync Reports that feed into Stage 6 conformance evidence and the CTO's technical dashboard.
version: "1.0.0"
---

# Architecture Syncs

| Competency               | Description                                                             | Quality Criteria                                                                                                      |
| ------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Session Facilitation     | Run structured architecture syncs with Android, iOS, and backend leads  | 45-minute weekly cadence; structured agenda; all decisions captured with owner and deadline before session ends       |
| Alignment Tracking       | Track cross-team decisions and detect divergence between platform teams | Maintains an Architecture Decisions Log; any cross-team divergence is flagged within one week of detection            |
| Technical Debt Triage    | Surface and classify technical debt discovered in architecture syncs    | Debt items categorized as ADR-Required / Refactor-Required / Monitor; P0/P1 items escalated to CTO immediately        |
| Architecture Sync Report | Produce weekly report for CTO and team leads                            | Report includes: decisions made, open questions, technical debt surfaced, and any Stage 6 compliance risks identified |

## Execution Guidance

### Architecture Sync Agenda Template

```
Architecture Sync — Week [N] — [Date]
Duration: 45 minutes

1. Status Review (10 min)
   - Open ADR decisions since last sync
   - Conformance check updates from Stage 6 queue

2. Cross-Team Alignment (15 min)
   - Android team: current sprint architectural concerns
   - iOS team: current sprint architectural concerns
   - Backend team: API contract changes or breaking changes

3. Technical Debt Register (10 min)
   - New debt items surfaced
   - Prioritization updates

4. Decisions & Actions (10 min)
   - Decisions made in this session (owner + deadline)
   - Escalations to CTO
```

### Architecture Decisions Log Format

| Date       | Decision                   | Owner       | Impact Scope | Status      |
| ---------- | -------------------------- | ----------- | ------------ | ----------- |
| YYYY-MM-DD | [Architecture choice made] | [Name/team] | [Platforms]  | Open/Closed |

Any decision affecting the technology stack must trigger an ADR. Verbal-only decisions with no written record are not acceptable — they create audit gaps at Stage 6.
