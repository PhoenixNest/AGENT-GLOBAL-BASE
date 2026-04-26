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
