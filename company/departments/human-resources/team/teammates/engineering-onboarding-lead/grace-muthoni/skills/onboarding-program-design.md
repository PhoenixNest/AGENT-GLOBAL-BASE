# Engineering Onboarding Program Design

**Category:** Talent Operations / Onboarding
**Owner:** Engineering Onboarding Lead

## Overview

Designs and operates the end-to-end engineering onboarding program for the 57-person FTE roster, from pre-boarding logistics through the 90-day ramp-to-productivity milestone. The program follows a 4-stage model (Day 1 → Week 1 → Month 1 → Month 3) with automated environment provisioning, structured buddy assignments, and measurable competency gates at each stage transition.

This skill covers program architecture, cohort scheduling, environment automation workflows, buddy system design, cross-functional coordination with platform leads, and continuous improvement based on ramp-time analytics and new-hire satisfaction NPS.

## Competency Dimensions

| Dimension | Description | Proficiency Indicators |
|-----------|-------------|----------------------|
| Program Architecture | Design multi-stage onboarding curricula scaled to 50+ FTE across multiple role families | Can design a 4-stage program with explicit gate criteria, deliverables, and success metrics per stage |
| Environment Automation | Integrate with engineering tooling to automate dev environment provisioning | Achieves ≥80% zero-touch environment setup; reduces Day-1 friction to <2 hours |
| Buddy System Design | Match new hires with experienced engineers for guided ramp-up | Buddy pair retention ≥90%; buddy satisfaction score ≥4.2/5 |
| Cohort Scheduling | Plan and stagger onboarding waves to avoid team capacity overload | No team onboards >3 hires in a single wave; wave overlap <15% |
| Ramp-Time Optimization | Measure and reduce time-to-first-PR, time-to-first-deploy, time-to-autonomous | Reduces median time-to-first-PR from 14 days to ≤7 days; time-to-autonomous ≤60 days |
| Cross-Functional Coordination | Align with CTO, platform leads, and IT for resource readiness | 100% of hires have day-1-ready accounts, hardware, and repo access |

## Execution Guidance

### 4-Stage Onboarding Model

#### Stage 1: Day 1 — Orientation & Environment Ready
- **Objective:** New hire has working development environment and understands company context
- **Deliverables:**
  - Hardware provisioned (laptop, peripherals, security key)
  - All accounts created: SSO, Git, CI/CD, Slack, Jira, internal wiki
  - Development environment script executed (`./scripts/setup-dev.sh` or equivalent per platform)
  - Company overview session (mission, pipeline, department structure, defect severity system)
  - Team intro meeting with direct supervisor and assigned buddy
  - HR paperwork completion (benefits, IP agreement, code of conduct acknowledgment)
- **Gate Criteria:** Environment compiles and runs the hello-world build on target platform; new hire can navigate the repo, file a test issue, and submit a dummy PR
- **Owner:** Engineering Onboarding Lead + IT Support
- **Duration:** 1 day

#### Stage 2: Week 1 — Context & First Contribution
- **Objective:** New hire understands the codebase architecture and makes their first merged contribution
- **Deliverables:**
  - Architecture walkthrough with Software Architect (UML diagrams, ADRs, TSD review)
  - Pipeline orientation: 10-stage development lifecycle, gate criteria, defect classification
  - First assigned task: good-first-issue label, scope limited to documentation, tests, or minor bug fix
  - Code review participation: new hire reviews ≥1 peer PR (guided by buddy)
  - Security training: OWASP MASVS basics, SRD overview, secure coding standards
  - Buddy check-in: 30-minute daily syncs, end-of-week retrospective
- **Gate Criteria:** First PR merged (even if trivial); new hire can explain the pipeline stages and their team's role within it
- **Owner:** Buddy + Direct Supervisor
- **Duration:** 5 business days

#### Stage 3: Month 1 — Competent Contributor
- **Objective:** New hire independently completes small-to-medium features and participates in code reviews
- **Deliverables:**
  - Assigned to a feature story within their platform track (Android, iOS, Cross-Platform)
  - Participates in ≥3 code reviews as a reviewer (not just author)
  - Completes platform-specific deep-dive: e.g., Android lifecycle, iOS ATS, Flutter widget tree
  - Writes their first ADR contribution (under mentorship) or updates an existing one
  - Mid-month 1:1 with supervisor: goal alignment, feedback exchange, competency self-assessment
  - Shadow a gate review panel (Stage 6, 8, or 10 depending on project timeline)
- **Gate Criteria:** ≥3 PRs merged independently; supervisor rates new hire as "meets expectations" on competency matrix for their role family; no P0/P1 defects introduced
- **Owner:** Direct Supervisor + Buddy
- **Duration:** 3 weeks (Day 6 → Day 30)

#### Stage 4: Month 3 — Autonomous Engineer
- **Objective:** New hire operates autonomously, owns features end-to-end, and contributes to team decisions
- **Deliverables:**
  - Owns a feature from implementation through Stage 6 code review sign-off
  - Authors ≥1 ADR independently
  - Participates in architecture discussions and technology selection evaluations
  - Mentors a newer hire or intern (role reversal from Stage 2)
  - Completes probationary review with CHRO and direct supervisor
  - Presents a tech talk or post-mortem to the engineering team
- **Gate Criteria:** Feature shipped to production or Stage 8+; ADR accepted by architecture panel; probationary review passed; supervisor rates "exceeds expectations" or "strong meets" on competency matrix
- **Owner:** Direct Supervisor + CHRO
- **Duration:** 8 weeks (Day 31 → Day 90)

### Automated Environment Setup

- **Infrastructure-as-Code for Dev Environments:** Each platform (Android, iOS, Flutter, KMP) maintains a `setup-dev.sh` / `setup-dev.ps1` script in `company/project/<project>/platforms/<platform>/scripts/` that installs SDKs, configures emulators, pulls dependencies, and validates the build
- **Pre-Boarding Trigger:** Onboarding Lead receives new-hire details 5 business days before start date; triggers environment provisioning workflow
- **Zero-Touch Target:** ≥80% of environment setup completed before new hire's Day 1 login; remaining steps documented and estimated at <2 hours
- **Fallback Protocol:** If automated setup fails, IT Support has a manual runbook with estimated 4-hour resolution SLA
- **Validation Checklist:** Automated script outputs a pass/fail report; Onboarding Lead reviews and confirms before Day 1

### Buddy System Design

- **Matching Criteria:** Buddy is a teammate (not supervisor) from the same platform track, ≥6 months tenure, rated "meets expectations" or higher, and volunteers for the role
- **Buddy Responsibilities:**
  - Daily 15-minute check-ins during Week 1, then 3x/week through Month 1
  - First point of contact for "stupid questions" (reduces new-hire anxiety)
  - Reviews new hire's first 5 PRs before they are submitted to the broader team
  - Provides candid feedback to Onboarding Lead at each stage gate
  - Escalates blockers to supervisor if unresolved within 24 hours
- **Buddy Load Limit:** No engineer serves as buddy for >1 new hire simultaneously
- **Recognition:** Buddy service counts toward performance review "Leadership Signal" dimension; eligible for quarterly peer recognition bonus
- **Buddy Training:** 2-hour onboarding session covering active listening, feedback delivery, escalation protocols, and cultural inclusion

### Cohort Scheduling & Capacity Planning

- **Wave Size:** 3-5 new hires per wave, staggered by 1 week between waves
- **Team Capacity:** No platform team onboards >3 hires in any 30-day window
- **Cross-Platform Balance:** Waves mix Android, iOS, and Cross-Platform hires to distribute buddy load
- **Conflict Avoidance:** Onboarding Lead checks project pipeline calendar; avoids scheduling new-hire waves during Stage 6, 8, or 10 gate review weeks (when team capacity is consumed by panel duties)
- **Remote/Hybrid Consideration:** For remote hires, Day 1 includes virtual environment validation session; buddy check-ins are video-first

### Ramp-Time Metrics & Optimization

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| Time-to-first-PR | 14 days | ≤7 days | Git timestamp: first PR opened by new hire |
| Time-to-first-merge | 16 days | ≤9 days | Git timestamp: first PR merged |
| Time-to-first-deploy | 30 days | ≤21 days | CI/CD pipeline log: first deployment by new hire |
| Time-to-autonomous | 90 days | ≤60 days | Supervisor assessment at probationary review |
| Onboarding NPS | +35 | ≥+50 | Survey at Day 30 and Day 90 |
| 90-day retention | 92% | ≥96% | HRIS data |

- **Optimization Levers:**
  - Improve setup script reliability (reduces Day 1 friction)
  - Expand good-first-issue backlog (reduces time-to-first-PR)
  - Increase buddy training quality (improves new-hire confidence)
  - Refactor competency matrix for clarity (reduces ambiguity in expectations)
  - Quarterly onboarding program retrospective with recent hires

## Pipeline Integration

| Pipeline Stage | Onboarding Relevance |
|----------------|---------------------|
| Stage 1 (Requirements) | Not applicable — onboarding does not intersect with PRD/SRD creation |
| Stage 2 (Design) | New hires in Month 1+ may participate in design reviews as observers |
| Stage 3 (Architecture) | Month 3 hires author ADRs; Week 1 hires attend architecture walkthroughs |
| Stage 4 (Implementation Plan) | Not directly applicable — new hires consume, not create, implementation plans |
| Stage 5 (Development) | **Primary integration point** — new hires contribute code from Week 1 onward under buddy supervision |
| Stage 6 (Code Review) | Month 1+ hires participate as reviewers; Month 3 hires author PRs that enter code review |
| Stage 7 (Testing) | Month 1+ hires write unit tests; Month 3+ contributes to integration test suite |
| Stage 8 (Integrity Verification) | Not applicable — panel-only stage; new hires may observe |
| Stage 9 (i18n) | Not applicable — specialized to Localization team |
| Stage 10 (Release) | Not applicable — panel-only stage; new hires may observe |

## Quality Standards

- **Environment Readiness:** 100% of new hires have working dev environment by end of Day 1 (validated by setup script output + Onboarding Lead confirmation)
- **Buddy Coverage:** 100% of new hires assigned a trained buddy before Day 1; zero buddy overload (max 1 active pairing per engineer)
- **Gate Pass Rate:** ≥90% of new hires pass each stage gate on first attempt; failures trigger individualized remediation plan within 48 hours
- **Ramp-Time Target:** Median time-to-first-merge ≤9 days across all role families; measured quarterly and reported to CTO
- **Onboarding NPS:** ≥+50 at Day 90; any cohort scoring below +40 triggers root-cause analysis and program revision
- **Documentation Currency:** Onboarding runbook updated within 5 business days of any pipeline, tooling, or process change
- **Probationary Pass Rate:** ≥85% of new hires pass probationary review; failures documented with specific competency gaps and exit process per HR policy
