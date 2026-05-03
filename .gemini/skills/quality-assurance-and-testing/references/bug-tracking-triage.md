---
name: bug-tracking-triage
description: Automated bug triage, ML-based defect classification, and quality metrics tracking for game QA.
version: "1.0.0"
---

# Bug Tracking & Triage

## Overview

This skill covers automated defect management systems for game QA, including ML-based bug classification, automated triage workflows, and quality metrics dashboards.

## Tools & Platforms

| Tool                 | Purpose                                |
| -------------------- | -------------------------------------- |
| Jira                 | Defect tracking, workflow management   |
| Custom ML Classifier | Automated bug categorization           |
| Quality Dashboard    | Real-time defect metrics visualization |

## Core Methodologies

### 1. Automated Bug Triage Pipeline

```
Bug Report → NLP Classification → Severity Prediction → Auto-Assign → Notification
     ↓
Duplicate Detection (embedding similarity)
     ↓
If duplicate → Link to original, close
If new → Route to appropriate team
```

### 2. Defect Classification

| Dimension | Categories                              | Classification Method       |
| --------- | --------------------------------------- | --------------------------- |
| Type      | Crash, Gameplay, UI, Audio, Performance | ML (fine-tuned transformer) |
| Severity  | P0, P1, P2, P3                          | Rule-based + ML confidence  |
| Component | Gameplay, Engine, Backend, UI, Audio    | Keyword + context analysis  |
| Platform  | iOS, Android, Both                      | Auto-detected from report   |

### 3. Quality Metrics Dashboard

| Metric                | Target             | Alert Threshold |
| --------------------- | ------------------ | --------------- |
| Defect detection rate | > 95%              | < 90%           |
| False positive rate   | < 5%               | > 10%           |
| Triage time           | < 15 min/batch     | > 30 min        |
| Defect escape rate    | < 2% to production | > 5%            |
| Open defect aging     | < 7 days avg       | > 14 days       |

## Studio-Specific Triage Workflow

### Jira Issue Lifecycle

All bugs discovered by Lin Zhang (or flagged from automated test runs) follow this state machine in Jira:

```
Open → In Triage → Confirmed → In Fix → Verification → Closed
         ↓
     Duplicate / Won't Fix → Closed (with justification)
```

| State            | Owner        | Meaning                                                                      |
| ---------------- | ------------ | ---------------------------------------------------------------------------- |
| **Open**         | Reporter     | Bug filed; not yet reviewed                                                  |
| **In Triage**    | Lin Zhang    | Lin reviews, classifies severity, identifies component, checks for duplicate |
| **Confirmed**    | Amara Osei   | Amara validates the bug is real, severity is correct, and it's in scope      |
| **In Fix**       | Assigned dev | Developer is actively fixing; Lin monitors for age                           |
| **Verification** | Lin Zhang    | Fix merged; Lin re-tests on device farm to confirm resolution                |
| **Closed**       | Lin Zhang    | Verified fixed (or correctly closed as Won't Fix / Duplicate)                |

### Routing by Division

After triage confirmation, Lin routes bugs to the appropriate engineering sub-team:

| Bug Category           | Routed To                                         |
| ---------------------- | ------------------------------------------------- |
| Audio bugs             | Kenji Watanabe / Hiroshi Tanaka (Audio division)  |
| Art / visual bugs      | Renaud Dupont (Art division lead)                 |
| Backend / economy bugs | Priya Nair (Senior Backend Engineer)              |
| Engine / physics bugs  | Viktor Stahl (Senior Engine Engineer)             |
| Gameplay logic bugs    | Sofia Martinez or Ryu Tanaka (Gameplay Engineers) |
| UI / animation bugs    | Ryu Tanaka (Gameplay Engineer #2)                 |

Amara Osei (Lead QA) is CC'd on all P0 and P1 routing actions. Unresolvable routing ambiguities are escalated to Amara for a decision.

### Stage 6 and Stage 7 Exit Criteria for Bug Severity

Exit criteria govern when the studio may advance from Stage 6 (Automated Testing) to Stage 7 (Soft Launch Prep), and from Stage 7 to Stage 8 (Soft Launch):

| Gate             | P0 (Crash / Data Loss / Security) | P1 (Core Feature Broken) | P2 / P3                                                |
| ---------------- | --------------------------------- | ------------------------ | ------------------------------------------------------ |
| **Stage 6 exit** | Zero open P0s                     | Zero open P1s            | Amara Osei approves deferral list                      |
| **Stage 7 exit** | Zero open P0s                     | Zero open P1s            | Studio Director and/or EP approves deferral in writing |

Lin Zhang is responsible for maintaining the open bug count report that feeds these gate reviews. She does not make the pass/fail determination — that authority rests with Amara Osei (Stage 6) and the Studio Director / Executive Producer (Stage 7).
