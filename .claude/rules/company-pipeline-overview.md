---
paths:
  - "**/company/pipeline/**"
description: Company 13-stage development pipeline rules — active for pipeline folder work
---

# Company Pipeline Overview — 13-Stage Development Pipeline

**Applies To:** All company development pipelines (Mobile, Web, Backend API, Full-Stack)

---

## Pipeline Structure

| #   | Stage                                            | Key Producers     | User Approval? |
| --- | ------------------------------------------------ | ----------------- | -------------- |
| 0   | Problem Validation                               | CPO / VP          | ❌             |
| 1   | Requirements → PRD + SRD                         | CPO / VP, CSO     | ✅             |
| 2   | PRD → Web Prototype + IDS                        | CDO               | ✅             |
| 3   | Prototype → UML Engineering Package              | CTO, CIO          | ✅             |
| 4   | UML → Implementation Plan + Gantt                | CTO               | ✅             |
| 5   | Plan → Software Development                      | CTO               | ❌             |
| 6   | Development → Arch. & Conformance Review         | CTO + full panel  | ✅             |
| 7   | Arch. Review → Automated Testing                 | CTO + Test Lead   | ✅             |
| 8   | Testing → Integrity Verification                 | CTO + all C-suite | ❌             |
| 9   | Integrity Verification → Translation Production  | CTO-L + R&D       | ❌             |
| 9.5 | Internal Dogfood                                 | VP Quality        | ❌             |
| 10  | Translation Production → Release Readiness Check | CTO + User        | ✅             |
| 11  | Live Operations (continuous)                     | VP Platform       | ⚠️ QBR         |

---

## Non-Negotiable Pipeline Rules

### Technology Decision Lock (Stage 3)

ADRs and TSD are **immutable** after user approval at Stage 3. Any deviation requires a new ADR and full Stage 3 re-entry — never edit at Stage 4 or later.

### Trim-to-Pass Forbidden (Stage 8)

Removing features, security controls, or encryption to pass Stage 8 is a **P0 defect** — not valid remediation.

### Defect Severity

- **P0** = Crash / data loss / security breach (blocks release)
- **P1** = Core feature broken (blocks release)
- **P2/P3** = User decides

P0/P1 classification is non-overridable.

### Stage 6 Remediation Loop

After any remediation at Stage 6, the **full review panel process repeats from the beginning**.

### PRD + SRD Pairing

From Stage 1 onward, PRD and SRD travel as a unit. Both must be present and approved together.

---

## Stage Gates (User Approval ✅ = Hard Stop)

Stages 1, 2, 3, 4, 6, 7, 10 require explicit user sign-off. Present deliverable → request sign-off → **wait**.

---

## Progress Monitoring (Stage 4+)

Maintain `progress.md`, `session-log.md`, `checkpoint.json` in the project folder.
