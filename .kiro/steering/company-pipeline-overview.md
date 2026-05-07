---
inclusion: fileMatch
fileMatchPattern: "**/company/pipeline/**"
---

# Company Pipeline Overview — 13-Stage Development Pipeline

**Authority:** AGENTS.md § 4.4 Company — 13-Stage Development Pipeline  
**Applies To:** All company development pipelines (Mobile, Web, Backend API, Full-Stack)

---

## Pipeline Structure

The company uses a **13-stage development pipeline** (Stages 0-11) for all software development projects:

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

## Non-Negotiable Pipeline Rules

### 1. Technology Decision Lock (Stage 3)

**Rule:** ADRs and TSD are immutable after user approval at Stage 3.

- Any deviation requires a new ADR and full Stage 3 re-entry
- Never edit existing ADRs/TSD at Stage 4 or later
- Technology changes after Stage 3 approval are invalid

### 2. Trim-to-Pass Forbidden (Stage 8)

**Rule:** Removing features, security controls, or encryption to pass Stage 8 is a P0 defect.

- Never disable functionality to pass Integrity Verification
- Never weaken security controls to pass review
- This is not valid remediation — it's a blocking defect

### 3. Defect Severity Classification (All Stages)

**Severity Levels:**

- **P0** = Crash / data loss / security breach (blocks release)
- **P1** = Core feature broken (blocks release)
- **P2/P3** = User decides

**Rule:** P0/P1 classification is non-overridable by any agent.

### 4. Stage 6 Remediation Loop

**Rule:** After any remediation at Stage 6, the full review panel process repeats from the beginning.

- Do not resume at defect verification only
- Full panel must re-review all aspects
- No shortcuts after remediation

### 5. PRD + SRD Pairing (From Stage 1 Onward)

**Rule:** PRD and SRD travel as a unit through all subsequent stages.

- Both documents must be present
- Both must be approved together
- Both must be referenced in downstream artifacts

## Stage Gates with User Approval

Stages marked **User Approval? ✅** are **hard stops**:

- Stage 1: Requirements → PRD + SRD
- Stage 2: PRD → Web Prototype + IDS
- Stage 3: Prototype → UML Engineering Package
- Stage 4: UML → Implementation Plan + Gantt
- Stage 6: Development → Arch. & Conformance Review
- Stage 7: Arch. Review → Automated Testing
- Stage 10: Translation Production → Release Readiness Check

**Protocol:**

1. Present the completed deliverable
2. Explicitly request sign-off
3. **Wait** for user approval
4. Do not auto-advance to next stage

## Pipeline Variants

| Pipeline    | Pattern                            | Location                               |
| ----------- | ---------------------------------- | -------------------------------------- |
| Mobile      | Base + delta (`_base/` + delta.md) | `company/pipeline/mobile-development/` |
| Web         | Base + delta (`_base/` + delta.md) | `company/pipeline/web-development/`    |
| Backend API | Base + delta (`_base/` + delta.md) | `company/pipeline/backend-api/`        |
| Full-Stack  | Base + delta (`_base/` + delta.md) | `company/pipeline/full-stack/`         |
| Recruitment | Standalone (9 stages)              | `company/pipeline/recruitment/`        |

## Progress Monitoring (Stage 4+)

For any project at or beyond Stage 4, maintain:

- `progress.md` — Real-time state
- `session-log.md` — Audit trail
- `checkpoint.json` — Machine-readable milestones

**Escalation:** Any task exceeding estimate by >20% triggers CTO → CPO schedule risk notification.

## Related Steering Files

- `mobile-pipeline.md` — Mobile-specific rules
- `web-pipeline.md` — Web-specific rules
- `backend-pipeline.md` — Backend API-specific rules
- `full-stack-pipeline.md` — Full-stack-specific rules
- `recruitment-pipeline.md` — Recruitment-specific rules (9 stages)
