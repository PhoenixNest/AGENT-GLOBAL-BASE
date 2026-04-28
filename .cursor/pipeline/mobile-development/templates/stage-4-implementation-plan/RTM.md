# Requirements Traceability Matrix (RTM)

**Project:** [Project Name]
**Author:** CTO (Dr. Kenji Nakamura) + CPO (Marcus Tran-Yoshida)
**Date:** YYYY-MM-DD
**Version:** v1
**Referenced Artifacts:** PRD v1, SRD v1, IDS v1, UML Package v1, Implementation Plan v1

---

## Purpose

The RTM maps each PRD requirement through design, implementation, and testing — ensuring no requirement is silently dropped, added, or reinterpreted without explicit traceability. This is the primary evidence document for Stage 6 Code Review (Criterion 1: "All PRD requirements implemented") and Stage 10 Release Checklist Item 1.

---

## Traceability Matrix

| PRD ID  | PRD Requirement (User Story) | Priority | IDS Section(s) | UML Element(s)         | Implementation Task(s) | Test Case(s) | Status                                       |
| ------- | ---------------------------- | -------- | -------------- | ---------------------- | ---------------------- | ------------ | -------------------------------------------- |
| REQ-001 | [As a user, I want to...]    | P0/P1/P2 | IDS §X.X       | [Class/Component name] | T-XXX                  | TC-XXX       | ☐ Not Started / 🟡 In Progress / ✅ Complete |
| REQ-002 | [As a user, I want to...]    | P0/P1/P2 | IDS §X.X       | [Class/Component name] | T-XXX                  | TC-XXX       | ☐ Not Started / 🟡 In Progress / ✅ Complete |
| REQ-003 | [As a user, I want to...]    | P0/P1/P2 | IDS §X.X       | [Class/Component name] | T-XXX                  | TC-XXX       | ☐ Not Started / 🟡 In Progress / ✅ Complete |

> **PRD ID format:** REQ-NNN (sequential, starting from REQ-001)
> **Priority:** Matches PRD priority classification (P0 = Must Have, P1 = Should Have, P2 = Nice to Have)

---

## Security Requirements Traceability

| SRD ID  | SRD Requirement   | Priority | IDS Section(s) | UML Element(s) | SIS Section | Implementation Task(s) | Test Case(s) | Status                                       |
| ------- | ----------------- | -------- | -------------- | -------------- | ----------- | ---------------------- | ------------ | -------------------------------------------- |
| SEC-001 | [SRD requirement] | P0/P1/P2 | [IDS §X.X]     | [Component]    | SIS §X.X    | T-XXX                  | TC-XXX       | ☐ Not Started / 🟡 In Progress / ✅ Complete |
| SEC-002 | [SRD requirement] | P0/P1/P2 | [IDS §X.X]     | [Component]    | SIS §X.X    | T-XXX                  | TC-XXX       | ☐ Not Started / 🟡 In Progress / ✅ Complete |

> **SRD ID format:** SEC-NNN (sequential, starting from SEC-001)

---

## Coverage Summary

| Category         | Total   | Implemented | Tested  | Pass Rate |
| ---------------- | ------- | ----------- | ------- | --------- |
| PRD Requirements | [N]     | [N]         | [N]     | [XX]%     |
| SRD Requirements | [N]     | [N]         | [N]     | [XX]%     |
| **Total**        | **[N]** | **[N]**     | **[N]** | **[XX]%** |

**Gate criterion:** 100% PRD/SRD requirement coverage required for Stage 6 sign-off. Any "Not Implemented" requirement is at minimum a **P1 defect**.

---

## Change Log

| Date       | Version | Change Description                       | Author |
| ---------- | ------- | ---------------------------------------- | ------ |
| YYYY-MM-DD | v1      | Initial RTM created from PRD v1 + SRD v1 | [Name] |
| YYYY-MM-DD | v2      | [Description]                            | [Name] |

---

**Reviewed by CPO (Marcus Tran-Yoshida) on YYYY-MM-DD**
**Reviewed by CTO (Dr. Kenji Nakamura) on YYYY-MM-DD**
