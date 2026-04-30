---
name: studio-engineering-qa-team-leadership
description: People leadership and team management for the Casual Games Studio QA team — SDET delegation, sprint cadence, feedback and growth, Stage 6 gate ownership, and Stage 7 soft launch readiness sign-off. Owned by Amara Osei (Lead QA Engineer). Use when managing the QA team, delegating automation tracks, or producing stage gate deliverables. Trigger: QA team management, SDET leadership, Stage 6 sign-off, Stage 7 readiness, QA delegation, performance review, sprint planning.
version: "1.0.0"
---

# QA Team Leadership

**Skill Owner:** Amara Osei | **Version:** 1.0 | **Date:** 2026-04-30

## Description

People leadership and operational management of the Casual Games Studio's SDET team. Amara Osei manages three direct reports across gameplay automation and performance testing, sets the QA strategy, delegates test tracks, and holds the sole authority over Stage 6 and Stage 7 QA sign-off.

## Team Structure

| Direct Report         | Role             | Primary Focus Area                                                             |
| --------------------- | ---------------- | ------------------------------------------------------------------------------ |
| **Amir Hassan**       | SDET Gameplay #1 | Test framework architecture; gameplay automation suite; CI integration         |
| **Lin Zhang**         | SDET Gameplay #2 | Device-specific execution; physical device farm runs; iOS/Android parity       |
| **Priya Subramanian** | SDET Performance | FPS benchmarking; memory profiling; thermal stress; load testing (client-side) |

Each SDET has a distinct, non-overlapping ownership domain. Amara coordinates their work through sprint planning and monitors their outputs through the cadence described below.

## Sprint Cadence

### Weekly SDET Sync (30 Minutes)

Held weekly with all three SDETs. Agenda:

1. Status update from each SDET (in-progress tasks, blockers)
2. Review of open bug counts and triage queue (Lin Zhang leads this portion)
3. Upcoming CI run schedule and device farm availability (Amir + Lin)
4. Performance test schedule for the week (Priya Subramanian)

Amara chairs this meeting. It is not optional — all three SDETs attend. Decisions made in this sync are the authoritative direction for the week.

### Individual 1:1s (Biweekly, 45 Minutes Each)

Amara holds a biweekly 1:1 with each SDET. These are structured as:

- **First 15 minutes:** Work status — any blockers, technical questions, help needed
- **Next 15 minutes:** Quality of work — review of recent output, feedback on test coverage or reports
- **Final 15 minutes:** Growth and development — progress against quarterly development goals

1:1s are not cancellable by Amara except under exceptional circumstances. They are the primary feedback channel between Amara and each SDET.

## Task Delegation Model

Amara drives all QA planning through a test plan that she authors at the start of each studio pipeline stage gate. Delegation follows a fixed pattern:

### Amara Authors the Test Plan

Amara writes the test plan for each stage gate. It specifies:

- Scope (which game systems, features, and platforms are in scope)
- Priority ranking (which test tracks are blocking vs informational)
- Pass/fail criteria (explicit thresholds for each test type)
- Timeline (when each track must deliver results)

### Delegation by Track

| Automation Track         | Delegated To      | Deliverable                                                           |
| ------------------------ | ----------------- | --------------------------------------------------------------------- |
| Test framework and suite | Amir Hassan       | Updated/new test suite code; CI integration; test run results         |
| Device matrix execution  | Lin Zhang         | Device Test Report (per-device pass/fail matrix; iOS parity status)   |
| Performance testing      | Priya Subramanian | Performance Test Report (FPS, memory, thermal, GPU metrics vs budget) |

### Results Flow Back to Amara

Each SDET reports results to Amara — not to engineering leads or the Studio Director directly. Amara consolidates the three reports, evaluates them against the test plan criteria, and issues a single QA verdict.

## Feedback and Growth

### Quarterly Skill Assessments

Amara conducts a structured quarterly skill assessment with each SDET using the following dimensions:

| Dimension             | What It Measures                                                             |
| --------------------- | ---------------------------------------------------------------------------- |
| Technical depth       | Quality of test design, framework correctness, profiling accuracy            |
| Coverage completeness | Whether assigned test tracks met the coverage thresholds in the test plan    |
| Communication         | Clarity of reports, proactive escalation of blockers                         |
| Collaboration         | Effectiveness of cross-team handoffs (with engineering leads, Amara herself) |

Assessment outcomes are documented and shared with each SDET. They feed into the next quarter's development goals.

### Career Development Conversations

Amara holds a dedicated career development conversation with each SDET once per quarter (separate from the quarterly assessment). These conversations focus on:

- Where the SDET wants to grow (technical specialisation, leadership, breadth)
- What opportunities exist within the studio's upcoming pipeline stages
- Any skills gaps Amara has observed, and how to close them

### Escalation to Dmitri Volkov

If an SDET's growth is blocked by a **resourcing issue** — insufficient time, tooling unavailability, or scope that exceeds the team's current headcount — Amara escalates to Dmitri Volkov (Senior Game Engineer). Amara does not absorb resourcing constraints silently.

## Stage 6 Gate Ownership

**Amara Osei is the sole sign-off authority for Stage 6 (Automated Testing) completion on the QA dimension.**

No SDET can independently declare Stage 6 passed. The gate process:

1. Each SDET delivers their track results (test run, device report, performance report) to Amara.
2. Amara reviews all three reports against the Stage 6 test plan pass/fail criteria.
3. Amara makes one of three decisions:
   - **Pass** — all criteria met; Stage 6 QA dimension cleared.
   - **Conditional pass** — minor open items approved for deferral; Amara documents the deferral and the conditions under which it may be closed post-Stage 6.
   - **Fail** — blocking issues identified; Amara specifies the required remediation and re-review scope.
4. Amara communicates the decision to Dmitri Volkov and the Studio Director.

## Stage 7 Readiness Sign-off

At Stage 7 (Soft Launch Prep), Amara produces the **QA Soft Launch Readiness Sign-off** document. This is the formal QA attestation that the game is ready for soft launch from a quality standpoint.

### Document Contents

| Section                | Content                                                                          |
| ---------------------- | -------------------------------------------------------------------------------- |
| Stage 6 Gate Summary   | Recap of Stage 6 verdict, open deferrals, and deferral conditions                |
| Open Bug Status        | Count of open P0/P1/P2/P3 bugs; confirmation that zero P0/P1 are open            |
| Device Matrix Coverage | Summary of Android device matrix and iOS parity coverage from Lin Zhang's report |
| Performance Baseline   | Soft launch performance baseline (FPS, memory, thermal) from Priya Subramanian   |
| Risk Assessment        | Any known quality risks entering soft launch; mitigation strategies              |
| Sign-off Statement     | Amara's formal attestation                                                       |

### Review Chain

The QA Soft Launch Readiness Sign-off is reviewed by **James Okonkwo (Executive Producer)** before Stage 7 can advance to Stage 8. Amara presents the document to James; any EP concerns are resolved before the sign-off is finalised.
