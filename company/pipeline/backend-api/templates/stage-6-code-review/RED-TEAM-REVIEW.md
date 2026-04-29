# Red Team Review Protocol — Stage 6 Adversarial Quality Gate

> **Addresses Gap:** #6 (No formalized adversarial quality review)

---

## Purpose

The Red Team Review is a **dedicated adversarial analysis** performed during Stage 6 (Code Review) by a designated reviewer whose sole objective is to **find flaws, weaknesses, and failure modes** — not to confirm compliance.

This is distinct from the standard Tier 1 cross-review. Standard reviewers assess quality; the Red Team reviewer **actively attacks** the codebase and architecture.

---

## Red Team Reviewer Assignment

| Stage                      | Red Team Reviewer                                        | Why This Agent                                                       |
| :------------------------- | :------------------------------------------------------- | :------------------------------------------------------------------- |
| **Stage 3** (Architecture) | Senior Software Architect (Dr. Elena Rostova)            | Applies STRIDE threat model adversarially against CTO's architecture |
| **Stage 6** (Code Review)  | CSO (Dr. Sarah Chen) **or** designated Security Engineer | Security-first perspective; explicitly seeks exploitable patterns    |
| **Stage 8** (Integrity)    | VP Quality (Aisha Patel)                                 | Independence from development chain; focused on regression detection |

---

## Red Team Review Checklist — Stage 6

The Red Team reviewer must independently assess the following attack surfaces:

### A. Security Attack Surface

| Attack Vector                | Check                                                         | Finding   | Severity |
| :--------------------------- | :------------------------------------------------------------ | :-------- | :------- |
| **Input validation bypass**  | Can any user input reach backend without sanitization?        | [Finding] | [P0–P3]  |
| **Authentication bypass**    | Can any endpoint be accessed without valid credentials?       | [Finding] | [P0–P3]  |
| **Authorization escalation** | Can a lower-privilege user access higher-privilege resources? | [Finding] | [P0–P3]  |
| **Data exposure**            | Are sensitive fields logged, cached, or exposed in responses? | [Finding] | [P0–P3]  |
| **Cryptographic weakness**   | Any use of deprecated algorithms or weak key sizes?           | [Finding] | [P0–P3]  |
| **Secret hardcoding**        | Any API keys, passwords, or tokens in source code?            | [Finding] | [P0–P3]  |

### B. Architectural Integrity

| Check                                                                         | Finding   | Severity |
| :---------------------------------------------------------------------------- | :-------- | :------- |
| **ADR compliance** — Does the implementation match all Stage 3 ADRs?          | [Finding] | [P0–P3]  |
| **Unauthorized dependencies** — Any libraries not approved in TSD?            | [Finding] | [P0–P3]  |
| **Layer violation** — Does any module bypass the defined architecture layers? | [Finding] | [P0–P3]  |
| **Single point of failure** — Are there undocumented SPOFs?                   | [Finding] | [P0–P3]  |

### C. Failure Mode Analysis

| Failure Scenario             | Handled?     | Finding   | Severity |
| :--------------------------- | :----------- | :-------- | :------- |
| **Network offline**          | ☐ Yes / ☐ No | [Finding] | [P0–P3]  |
| **Backend timeout**          | ☐ Yes / ☐ No | [Finding] | [P0–P3]  |
| **Disk full**                | ☐ Yes / ☐ No | [Finding] | [P0–P3]  |
| **Invalid state transition** | ☐ Yes / ☐ No | [Finding] | [P0–P3]  |
| **Concurrent access race**   | ☐ Yes / ☐ No | [Finding] | [P0–P3]  |
| **Memory pressure (OOM)**    | ☐ Yes / ☐ No | [Finding] | [P0–P3]  |

### D. Anti-Pattern Detection

| Anti-Pattern                                                       | Found?       | Location | Severity |
| :----------------------------------------------------------------- | :----------- | :------- | :------- |
| **Trim-to-pass** — Was any functionality removed to pass tests?    | ☐ Yes / ☐ No | [File]   | P0       |
| **God class / module** — Any class >500 lines or >10 dependencies? | ☐ Yes / ☐ No | [File]   | [P2–P3]  |
| **Shotgun surgery** — Does one change require touching >5 files?   | ☐ Yes / ☐ No | [Files]  | [P2–P3]  |
| **Test coupling** — Do tests rely on implementation details?       | ☐ Yes / ☐ No | [File]   | [P2–P3]  |
| **Magic numbers/strings** — Hardcoded values without constants?    | ☐ Yes / ☐ No | [File]   | [P3]     |

---

## Red Team Report Format

```markdown
## Red Team Report — Stage 6

**Project:** [Project Name]
**Red Team Reviewer:** [Name / Role]
**Date:** YYYY-MM-DD
**Scope:** [Files/modules reviewed]
**Time spent:** [Hours]

### Executive Summary

[1-2 paragraph summary of overall security and quality posture]

### Critical Findings (P0/P1)

[Numbered list with file references]

### Significant Findings (P2)

[Numbered list]

### Minor Findings (P3)

[Numbered list]

### Overall Assessment

☐ PASS — No critical or major findings
☐ CONDITIONAL PASS — P1 findings require remediation
☐ FAIL — P0 findings present; stage cannot advance

**Signed:** [Red Team Reviewer] on YYYY-MM-DD
```

---

## Integration with Existing Stage 6 Process

The Red Team Review is **additive** — it does not replace any existing review:

1. **Pre-Tier 1 automated gates** run first (SAST, secret scanning, dependency scan, linting, unit tests)
2. **Tier 1 platform lead cross-reviews** proceed as normal
3. **Red Team Review** runs in **parallel** with Tier 1 cross-reviews
4. Red Team findings are **merged** into the main Defect Report
5. C-Suite panel sign-off now requires **6 signatures** (CPO, CDO, CTO, CIO, CSO + Red Team)

---

## Automated Diff Analysis — Stage 8 Baseline Check

To complement the Red Team review, Stage 8 Integrity Verification **must** include an automated baseline comparison:

```
Stage 6 Baseline (code at gate pass) → Stage 8 Code
Any deleted functionality = automatic P0 flag ("trim-to-pass" detection)
```

**Implementation:** Run `git diff --stat` between the Stage 6 tag and Stage 8 tag. Any file with net-negative lines of non-test, non-comment code triggers a manual review.

---

## When to Use

- **Mandatory** at Stage 6 for all projects
- **Recommended** at Stage 3 (architecture review) for high-risk projects
- **Mandatory** at Stage 8 (automated baseline diff only)
