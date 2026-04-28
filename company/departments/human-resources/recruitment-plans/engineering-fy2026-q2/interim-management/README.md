# Interim Management Structure — Confirmation

**Document Type:** Interim Management Confirmation
**Version:** 1.1 (Expanded — v1.6 Recruitment Plan Alignment)
**Date:** April 3, 2026
**Owner:** CTO Office (Dr. Kenji Nakamura)
**Purpose:** Confirm interim management assignments for the phased onboarding period while VPs ramp up.

---

## Context

Because 57 FTEs are hired across **3 phased waves** (VPs → Chapter Leads → Engineers in batches), VPs and Chapter Leads will not be fully ramped when their direct reports arrive. Existing personnel provide interim management to ensure continuity during the onboarding period.

**Changes from v1.0:** CTO now covers Platform Engineering; CDO covers Frontend Engineering; Rafael Okonkwo extends scope to cover Backend Chapter Lead oversight.

---

## Interim Management Assignments

| Existing Personnel           | Role                        | Interim Authority                                                                                       | Duration      | Handoff Trigger                              |
| ---------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------- |
| Kofi Asante-Mensah           | Android Chapter Lead        | Manages 6 Android engineers (3 Senior + 3 Mid)                                                          | 4–6 weeks     | VP of Mobile completes onboarding            |
| Seo-Yeon Park                | iOS Chapter Lead            | Manages 6 iOS engineers (3 Senior + 3 Mid)                                                              | 4–6 weeks     | VP of Mobile completes onboarding            |
| Mei-Ling Johansson           | Cross-Platform Chapter Lead | Manages 2 Cross-Platform engineers                                                                      | 4–6 weeks     | VP of Mobile completes onboarding            |
| Priscilla Oduya              | Test Lead                   | Manages 3 SDETs (2 Mobile + 1 Web/Backend) + Test Automation Lead                                       | 4–6 weeks     | VP of Quality completes onboarding           |
| Rafael Okonkwo               | Software Architect          | Architecture governance + manages Senior Software Architect + **Backend Chapter Lead oversight**        | 4–6 weeks     | VP of Web & Backend completes onboarding     |
| **Dr. Kenji Nakamura (CTO)** | **CTO**                     | **Platform Engineering oversight (DevOps Lead + SRE team)**                                             | **4–6 weeks** | **VP of Platform completes onboarding**      |
| **Yuki Tanaka-Chen (CDO)**   | **CDO**                     | **Frontend Engineering oversight (design-system alignment + IDS fidelity only; NOT people management)** | **4–6 weeks** | **VP of Web & Backend completes onboarding** |
| Engineering Onboarding Lead  | Onboarding Lead             | Owns phased onboarding program from Phase 1 Day 1                                                       | Ongoing       | N/A (permanent role)                         |

---

## Interim Authority Scope

### Kofi Asante-Mensah (Android)

- Code review approval for all Android PRs
- Task assignment and sprint planning for Android team
- Technical decision-making within Android domain
- Escalation to CTO for cross-platform disputes
- Stage 5 (Development) progress reporting for Android

### Seo-Yeon Park (iOS)

- Code review approval for all iOS PRs
- Task assignment and sprint planning for iOS team
- Technical decision-making within iOS domain
- Escalation to CTO for cross-platform disputes
- Stage 5 (Development) progress reporting for iOS

### Mei-Ling Johansson (Cross-Platform)

- Code review approval for all Cross-Platform PRs
- Task assignment and sprint planning for Cross-Platform team
- Technical decision-making within KMP/Flutter domain
- Escalation to CTO for platform-specific disputes
- Stage 5 (Development) progress reporting for Cross-Platform

### Priscilla Oduya (Testing)

- Test strategy and execution for all divisions
- Test Automation Lead management
- SDET task assignment and sprint planning
- Stage 7 (Automated Testing) ownership
- Defect classification (P0–P3) authority

### Rafael Okonkwo (Architecture)

- ADR review and approval
- TSD compliance auditing
- Architecture governance across all divisions
- Senior Software Architect management
- Stage 3 (UML Engineering Package) ownership
- **Backend Chapter Lead oversight** (until VP of Web & Backend ramps)

### Dr. Kenji Nakamura — CTO (Platform Engineering)

- DevOps Lead task assignment and sprint planning
- SRE team management
- Infrastructure technical decision-making
- Stage 5 (Development) progress reporting for Platform

### Yuki Tanaka-Chen — CDO (Frontend Engineering)

- **Design-system alignment review only** — NOT people management
- IDS fidelity checks for Frontend team output
- Design quality standards enforcement
- Escalation to CTO for P0/P1 design defects
- **Out of scope:** Backend architecture, infrastructure, people management, sprint planning

---

## Handoff Protocol

When a VP completes onboarding (estimated 4–6 weeks):

1. **VP confirms readiness** to CTO
2. **CTO approves handoff** after VP demonstrates:
   - Understanding of division architecture
   - Familiarity with all team members
   - Ability to make technical decisions
   - Understanding of pipeline stage ownership
3. **Interim manager briefs VP** on:
   - Current project status
   - Open technical decisions
   - Team dynamics and individual performance
   - Outstanding risks and blockers
4. **Formal handoff documented** in PROGRESS.md
5. **Interim manager returns to Chapter Lead role** (for Kofi, Seo-Yeon, Mei-Ling) or continues in existing role (Priscilla, Rafael)

---

## Escalation Path During Interim Period

```
Engineer → Interim Manager → CTO → User (if required)
```

- Interim managers have full authority within their domain
- Cross-domain disputes escalate to CTO
- User escalation only for P0/P1 defects or pipeline gate decisions
- **CDO escalation path:** Design defect → CTO (not directly to User)

---

## Confirmation Status

| Interim Manager              | Status                 | Notes                                                        |
| ---------------------------- | ---------------------- | ------------------------------------------------------------ |
| Kofi Asante-Mensah           | ✅ Confirmed           | Android engineers (6)                                        |
| Seo-Yeon Park                | ✅ Confirmed           | iOS engineers (6)                                            |
| Mei-Ling Johansson           | ✅ Confirmed           | Cross-Platform engineers (2)                                 |
| Priscilla Oduya              | ✅ Confirmed           | SDETs + Test Automation Lead                                 |
| Rafael Okonkwo               | ✅ Confirmed           | Architecture + Backend Chapter Lead oversight                |
| **Dr. Kenji Nakamura (CTO)** | **✅ Confirmed**       | **Platform Engineering (DevOps/SRE)**                        |
| **Yuki Tanaka-Chen (CDO)**   | **✅ Confirmed**       | **Frontend Engineering (design-system + IDS fidelity only)** |
| Engineering Onboarding Lead  | ⏳ Role not yet filled | Priority Phase 2 hire                                        |
