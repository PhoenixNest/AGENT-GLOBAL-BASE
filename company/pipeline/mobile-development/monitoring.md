# progress Monitoring & Recovery System

**Version:** 1.0  
**Effective Date:** April 1, 2026  
**Owner:** Chief Technology Officer (CTO)  
**Applicability:** All Stage 4+ projects (active from Implementation Planning onward)

---

## Overview

The progress Monitoring & Recovery System provides comprehensive oversight of pipeline progress, enabling rapid state assessment and seamless recovery after interruptions (e.g., power outages, session timeouts, agent handoffs).

This system is **mandatory** for all projects from Stage 4 onward, where development timelines extend over multiple sessions and the cost of lost progress is significant.

---

## System Architecture

The system comprises **three layers**:

| Layer       | Component            | Purpose                            | Update Frequency   |
| ----------- | -------------------- | ---------------------------------- | ------------------ |
| **Layer 1** | `progress.md`        | Real-time pipeline state           | Every milestone    |
| **Layer 2** | `sessions/*.md`      | Detailed session audit trail       | Per session        |
| **Layer 3** | `checkpoints/*.json` | Machine-readable milestone markers | At each checkpoint |

---

## Layer 1: progress.md (Real-Time State)

### Location

```
company/project/<project-name>/progress.md
```

### Purpose

Single source of truth for current pipeline state. Updated at every significant milestone. Must be readable at-a-glance by any stakeholder.

### Structure

```markdown
# Pipeline progress — <Project Name>

## Current State

- **Stage:** <N> (<Stage Name>)
- **Stage progress:** <XX>%
- **Platform Strategy:** <Android-only | iOS-only | Both Native | KMP Cross-Platform | Flutter Cross-Platform>
- **Status:** <Not Started | In progress | Gate Review | Complete>
- **Last Updated:** <YYYY-MM-DD HH:MM:SS UTC>
- **Session ID:** <session-YYYYMMDD-HHMMSS>

## Stage Status

| Stage | Name                   | Status         | Entry Date | Exit Date  | Artifacts Produced   | User Approval? |
| ----- | ---------------------- | -------------- | ---------- | ---------- | -------------------- | -------------- |
| 1     | Requirements           | ✅ Complete    | 2026-04-01 | 2026-04-01 | PRD v1, SRD v1       | ✅ Yes         |
| 2     | Design                 | ✅ Complete    | 2026-04-01 | 2026-04-01 | Prototype v2, IDS v2 | ✅ Yes         |
| 3     | Architecture           | 🟡 In progress | 2026-04-01 | —          | UML (draft)          | ✅ Yes         |
| 4     | Implementation Plan    | ⚪ Pending     | —          | —          | —                    | ✅ Yes         |
| 5     | Development            | ⚪ Pending     | —          | —          | —                    | ❌ No          |
| 6     | Code Review            | ⚪ Pending     | —          | —          | —                    | ✅ Yes         |
| 7     | Automated Testing      | ⚪ Pending     | —          | —          | —                    | ✅ Yes         |
| 8     | Integrity Verification | ⚪ Pending     | —          | —          | —                    | ❌ No          |
| 9     | i18n Engineering       | ⚪ Pending     | —          | —          | —                    | ❌ No          |
| 10    | Release Readiness      | ⚪ Pending     | —          | —          | —                    | ✅ Yes         |

## Current Stage Details (Stage <N>)

### Platform progress (Stage 5 only)

> Populated only during Stage 5. Inactive tracks show "N/A."
```

Stage 5: Development
Overall: 65%
├── KMP Shared (Track C — PRIMARY): 80% (Mei-Ling) — Ahead of schedule
├── Android Integration (Track A — LIGHT): 55% (Kofi, 2 eng) — On track
├── iOS Integration (Track B — LIGHT): 50% (Seo-Yeon, 2 eng) — Backend API dependency
├── Track A unused capacity: 5 engineers → reassigned to [test automation]
└── Track B unused capacity: 5 engineers → reassigned to [SDK migration prep]

```

### Cross-Track Dependencies (Stage 5 only)

> Shows blocking relationships between tracks.

| Dependency | Blocking | Blocked By | Status |
|------------|----------|------------|--------|
| KMP shared module data layer | Android adapter, iOS adapter | — | ✅ Resolved |
| Backend API v2 | iOS integration | Backend team | 🔴 Blocked |

### Completed

- [x] <Task 1>
- [x] <Task 2>

### In progress

- [ ] <Current task being worked on>

### Pending

- [ ] <Upcoming task>
- [ ] Stage <N> Gate Review
- [ ] User approval

## Resume Instructions

**If interrupted, resume here:**

1. <Specific file to open>
2. <Specific section to complete>
3. <Next action to take>

## Session Log

| Session ID              | Date       | Duration | Accomplishments       | Next Steps   |
| ----------------------- | ---------- | -------- | --------------------- | ------------ |
| session-20260401-143000 | 2026-04-01 | 45 min   | <Accomplishment list> | <Next steps> |

## Risk Flags

| Risk          | Severity | Mitigation | Owner |
| ------------- | -------- | ---------- | ----- | ------ | ------- |
| <Description> | <Low     | Medium     | High> | <Plan> | <Owner> |

## Security Gate Failures

> Tracks CI/CD security gate failures with severity, owner, and SLA for remediation.

| Gate          | Failure Details          | Severity | Owner | SLA    | Resolved?    |
| ------------- | ------------------------ | -------- | ----- | ------ | ------------ |
| [SAST]        | [Finding description]    | [P0/P1/P2] | [Name] | [X hrs] | ☐ Yes / ☐ No |
| [DAST]        | [Finding description]    | [P0/P1/P2] | [Name] | [X hrs] | ☐ Yes / ☐ No |
| [Dependency]  | [CVE details]            | [P0/P1/P2] | [Name] | [X hrs] | ☐ Yes / ☐ No |
| [Pen Test]    | [Finding description]    | [P0/P1/P2] | [Name] | [X days] | ☐ Yes / ☐ No |

## Technology Risk Register

> Tracks technology-specific risks: ADR compliance status, technology decision health, vendor/dependency vulnerabilities, platform SDK deprecation timelines.

| Risk | ADR Reference | Current Status | Likelihood | Impact | Mitigation | Owner | Review Date |
|------|--------------|----------------|-----------|--------|------------|-------|-------------|
| [e.g., KMP iOS target regression] | ADR-NNN | [Active / Monitoring / Resolved] | [Low/Med/High] | [Low/Med/High] | [Plan] | [Name] | YYYY-MM-DD |
| [e.g., Tink library CVE] | TSD §4 | [Active / Monitoring / Resolved] | [Low/Med/High] | [Low/Med/High] | [Plan] | [Name] | YYYY-MM-DD |
| [e.g., Android API 24 deprecation] | — | [Active / Monitoring / Resolved] | [Low/Med/High] | [Low/Med/High] | [Plan] | [Name] | YYYY-MM-DD |

## Security Metrics (Stage 5+)

> Tracked per platform during development.

| Metric | Android | iOS | KMP Shared |
|--------|---------|-----|------------|
| SRD requirements implemented | X/Y | X/Y | X/Y |
| SAST findings (open) | P0:0, P1:0, P2:X | P0:0, P1:0, P2:X | P0:0, P1:0, P2:X |
| Dependency vulnerabilities | 0 critical, X high | 0 critical, X high | 0 critical, X high |
| Security review coverage | XX% | XX% | XX% |

## Translation progress (Stage 9)

> Tracked during i18n Engineering. Expanded per-language detail with BLEU/TER scores.

| Language | Total Strings | TM Leverage % | Post-Editing % | BLEU Score | TER Score | Linguistic QA Pass Rate | Status |
|----------|--------------|---------------|----------------|------------|-----------|------------------------|--------|
| English  | [N]           | —             | —              | —          | —         | —                      | ✅ Complete |
| Chinese  | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                    | 🟡 In progress |
| Japanese | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                    | ⚪ Pending |
| Korean   | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                    | ⚪ Pending |
| French   | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                    | ⚪ Pending |

### Stage 9 Checkpoint Status

| Phase | Status | Owner | Output |
|-------|--------|-------|--------|
| String Extraction Readiness | ☐ Not Started / 🟡 In progress / ✅ Complete | Tomas Dvoracek | Pre-audit results |
| Phase A: R&D Extraction | ☐ Not Started / 🟡 In progress / ✅ Complete | Tomas Dvoracek | STRING-EXTRACTION-HANDOFF.md |
| Phase B: TMS Translation | ☐ Not Started / 🟡 In progress / ✅ Complete | CTO-L | Translation package |
| Linguistic QA | ☐ Not Started / 🟡 In progress / ✅ Complete | Linguists | QA results per language |
| Platform Resource Validation | ☐ Not Started / 🟡 In progress / ✅ Complete | CTO-L | Resource file audit |
| TRANSLATION-VERIFICATION-REPORT.md | ☐ Not Started / 🟡 In progress / ✅ Complete | CTO-L | Final report |
```

### Status Indicators

| Symbol | Meaning                        |
| ------ | ------------------------------ |
| ✅     | Complete (gate approved)       |
| 🟡     | In progress (active work)      |
| 🟠     | Gate Review (pending approval) |
| ⚪     | Pending (not started)          |
| 🔴     | Blocked (requires resolution)  |

### Update Triggers

| Event              | Action                                            |
| ------------------ | ------------------------------------------------- |
| Stage entry        | Add stage entry date, set status to 🟡            |
| Milestone complete | Update stage progress %, check off completed task |
| Session start      | Add session ID to Current State                   |
| Session end        | Add row to Session Log                            |
| Gate review        | Set status to 🟠, add exit date when approved     |
| Stage complete     | Set status to ✅, add exit date                   |

---

## Layer 2: Session Logs (Audit Trail)

### Location

```
company/project/<project-name>/sessions/<session-id>.md
```

### Purpose

Detailed log of each work session for audit, recovery, and continuous improvement. Creates a complete historical record of all work performed.

### Structure

```markdown
# Session: <session-id>

**Date:** <YYYY-MM-DD>  
**Start Time:** <HH:MM:SS UTC>  
**End Time:** <HH:MM:SS UTC> (or "In progress" if interrupted)  
**Stage:** <N> (<Stage Name>)  
**Agents Involved:** <List of agents/subagents>  
**Session Lead:** <Primary responsible agent>

## Objectives

1. <Objective 1>
2. <Objective 2>

## Activities

| Time  | Activity      | Output               | Status       |
| ----- | ------------- | -------------------- | ------------ |
| HH:MM | <Description> | <Artifact or result> | ✅ / 🟡 / ❌ |

## Artifacts Created

- `<file path 1>`
- `<file path 2>`

## Artifacts Modified

- `<file path>` — <Description of changes>

## Issues Encountered

| Time  | Issue         | Resolution     | Impact |
| ----- | ------------- | -------------- | ------ | ----- | ------ |
| HH:MM | <Description> | <How resolved> | <None  | Minor | Major> |

## Decisions Made

| Time  | Decision   | Rationale | Owner |
| ----- | ---------- | --------- | ----- |
| HH:MM | <Decision> | <Why>     | <Who> |

## Next Session Priorities

1. <Priority 1>
2. <Priority 2>

## Interruption Recovery

**If this session was interrupted:**

- Last completed: <Last successful milestone>
- In progress: <What was being worked on>
- Resume: <Specific instructions to continue>

## Time Tracking

| Category  | Estimated | Actual  | Variance |
| --------- | --------- | ------- | -------- |
| <Task 1>  | <X> min   | <Y> min | +/- <Z>% |
| <Task 2>  | <X> min   | <Y> min | +/- <Z>% |
| **Total** | <X> min   | <Y> min | +/- <Z>% |

**progress Sync Alert:** <If variance >20%, note: "CTO → CPO notification sent">
```

### Session ID Format

```
session-YYYYMMDD-HHMMSS
```

**Example:** `session-20260401-143000` (April 1, 2026, 14:30:00 UTC)

### Session Lifecycle

| Phase                 | Action                                                   |
| --------------------- | -------------------------------------------------------- |
| **Start**             | Create session log file with header + objectives         |
| **During**            | Update Activities table in real-time                     |
| **End (normal)**      | Complete all sections, mark End Time                     |
| **End (interrupted)** | Fill Interruption Recovery section, leave End Time blank |

---

## Layer 3: Checkpoint Files (Milestone Markers)

### Location

```
company/project/<project-name>/checkpoints/<stage>-<milestone>.json
```

### Purpose

Machine-readable checkpoint for automated recovery, progress queries, and integration with tooling. Enables programmatic state assessment.

### Structure

```json
{
  "checkpoint_id": "<stage>-<milestone-name>",
  "stage": <N>,
  "milestone": "<Human-readable milestone name>",
  "timestamp": "<ISO 8601 timestamp>",
  "session_id": "<session-YYYYMMDD-HHMMSS>",
  "platform_strategy": "<Android-only | iOS-only | Both Native | KMP Cross-Platform | Flutter Cross-Platform>",
  "platform_breakdown": {
    "track_a_android": {
      "status": "<FULL | LIGHT | Dormant | N/A>",
      "progress_percent": <XX>,
      "lead": "<Name>",
      "engineers_assigned": <N>,
      "engineers_active": <N>,
      "blockers": ["<Blocker description or empty array>"]
    },
    "track_b_ios": {
      "status": "<FULL | LIGHT | Dormant | N/A>",
      "progress_percent": <XX>,
      "lead": "<Name>",
      "engineers_assigned": <N>,
      "engineers_active": <N>,
      "blockers": ["<Blocker description or empty array>"]
    },
    "track_c_cross_platform": {
      "status": "<PRIMARY | Dormant | N/A>",
      "technology": "<KMP | Flutter | N/A>",
      "progress_percent": <XX>,
      "lead": "<Name>",
      "engineers_assigned": <N>,
      "engineers_active": <N>,
      "blockers": ["<Blocker description or empty array>"]
    }
  },
  "artifacts": [
    "relative/path/to/artifact1.md",
    "relative/path/to/artifact2.html"
  ],
  "gate_criteria": {
    "<criterion_1>": true,
    "<criterion_2>": false,
    "<criterion_3>": true
  },
  "resume_point": {
    "next_task": "<Description of next task>",
    "file_to_open": "relative/path/to/file.ext",
    "section": "<Section name or line number>",
    "context": "<Additional context for resumption>"
  },
  "metrics": {
    "stage_progress_percent": <XX>,
    "total_time_spent_min": <YY>,
    "tasks_completed": <ZZ>,
    "tasks_remaining": <WW>
  },
  "security_state": {
    "srd_compliance_percent": <XX>,
    "masvs_categories_compliant": ["AUTH", "STORAGE", "CRYPTO", "NETWORK", "PLATFORM", "RESILIENCE"],
    "open_security_findings": {
      "p0": <N>,
      "p1": <N>,
      "p2": <N>,
      "p3": <N>
    },
    "sast_findings": {
      "android": {"p0": 0, "p1": 0, "p2": <N>},
      "ios": {"p0": 0, "p1": 0, "p2": <N>}
    },
    "dependency_vulnerabilities": {
      "critical": 0,
      "high": <N>,
      "medium": <N>
    },
    "pen_test_status": "<Not Started | In progress | Complete | Failed>",
    "dast_status": "<Not Started | In progress | Complete | Failed>"
  },
  "technology_state": {
    "adr_compliance": {
      "ADR-NNN Platform Strategy": "<Compliant | Deviation | N/A>",
      "ADR-NNN String Key Taxonomy": "<Compliant | Deviation | N/A>",
      "ADR-NNN Security Crypto": "<Compliant | Deviation | N/A>",
      "ADR-NNN Security Storage": "<Compliant | Deviation | N/A>",
      "ADR-NNN Security Pinning": "<Compliant | Deviation | N/A>",
      "ADR-NNN Security Platform": "<Compliant | Deviation | N/A>"
    },
    "tsd_technology_versions": {
      "android_networking": "[library + version]",
      "ios_networking": "[library + version]",
      "android_storage": "[library + version]",
      "ios_storage": "[library + version]"
    },
    "open_technology_exceptions": <N>
  },
  "risks": [
    {
      "description": "<Risk description>",
      "severity": "<Low | Medium | High>",
      "mitigation": "<Plan>"
    }
  ],
  "milestone_history": [
    {
      "milestone": "<Milestone name>",
      "timestamp": "<ISO 8601>",
      "progress_percent": <XX>,
      "session_id": "<session-YYYYMMDD-HHMMSS>"
    }
  ]
}
```

### Checkpoint Triggers

| Stage | Checkpoint File                 | Milestone                                           |
| ----- | ------------------------------- | --------------------------------------------------- |
| 1     | `stage1-gate-approved.json`     | PRD + SRD complete, user approved                   |
| 2     | `stage2-gate-approved.json`     | Prototype + IDS complete, user approved             |
| 3     | `stage3-gate-approved.json`     | UML + ADRs + TSD complete, user approved            |
| 4     | `stage4-gate-approved.json`     | Implementation Plan + Gantt complete, user approved |
| 5     | `stage5-gate-approved.json`     | Development complete, CTO internal review passed    |
| 6     | `stage6-gate-approved.json`     | Defects remediated, panel sign-off complete         |
| 7     | `stage7-gate-approved.json`     | Test suite complete, 100% pass rate                 |
| 8     | `stage8-gate-approved.json`     | Integrity verification sign-off                     |
| 9     | `stage9-gate-approved.json`     | Localization complete, CTO-L report issued          |
| 10    | `stage10-release-decision.json` | Release checklist complete, user release decision   |

**File Naming Convention:**

- **During stage:** `stage<N>-in-progress.json` (updated at each milestone)
- **Gate review:** `stage<N>-gate-review.json` (ready for panel)
- **Approved:** `stage<N>-gate-approved.json` (user approved, stage complete)

**Milestone History:** Each checkpoint file contains a `milestone_history` array tracking all key milestones within that stage, eliminating the need for multiple checkpoint files per stage.

---

## Recovery Protocol

### After Interruption (e.g., Power Outage)

**Step 1: Read progress.md**

```
→ Identify current stage
→ Note last completed milestone
→ Check Session ID for latest session
```

**Step 2: Read Latest Session Log**

```
→ Open sessions/<session-id>.md
→ Review "Interruption Recovery" section
→ Understand what was in progress
```

**Step 3: Read Latest Checkpoint JSON**

```
→ Open checkpoints/latest-*.json
→ Parse machine-readable resume_point
→ Get exact file and section to resume
```

**Step 4: Resume Work**

```
→ Open specified file
→ Navigate to specified section
→ Continue from documented position
→ Update progress.md with new session ID
```

### Example Recovery Flow

```
INTERRUPTION DETECTED

1. Agent reads: company/project/android-todos-app/progress.md
   → Current Stage: 2 (Design)
   → Session ID: session-20260401-143000
   → In progress: Enhanced IDS document

2. Agent reads: sessions/session-20260401-143000.md
   → Last completed: Prototype v2 build
   → In progress: IDS sections 4-6
   → Resume: "Complete sections 4-6 (Gesture Vocabulary, State Diagrams, Edge Cases)"

3. Agent reads: checkpoints/stage2-ids-draft.json
   → resume_point.file_to_open: "design/interaction-specs/v1/draft/IDS.md"
   → resume_point.section: "4. Gesture Vocabulary"

4. Agent resumes:
   → Opens IDS.md
   → Navigates to section 4
   → Continues writing
   → Creates new session: session-20260401-160000
   → Updates progress.md
```

---

## progress Sync Protocol

### Activation

Active from **Stage 4 onward** (Implementation Planning through Release).

### Monitoring Rules

| Rule                       | Threshold                                       | Action                                                                  |
| -------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------- |
| **Task Duration Variance** | Actual > Estimated × 1.2 (20% overrun)          | CTO → CPO notification                                                  |
| **Per-Platform Variance**  | One platform >20% behind another                | CTO → CPO notification (fires even if overall average looks acceptable) |
| **Milestone Slip**         | Planned date passed, milestone incomplete       | Flag in progress.md, C-suite alert                                      |
| **Session Gap**            | No session log in >48 hours during active stage | Automated reminder to session lead                                      |

### Notification Format

```markdown
**progress Sync Alert**

**Project:** <Project Name>  
**Stage:** <N> (<Stage Name>)  
**Task:** <Task name>  
**Estimated Duration:** <X> minutes  
**Actual Duration:** <Y> minutes  
**Variance:** +<Z>%

**Impact:** <Description of schedule risk>  
**Mitigation Plan:** <Proposed action>

**CTO Recommendation:** <Fix / Defer / Escalate>
```

### Weekly Summary Format

From Stage 4 onward, CTO produces weekly progress summaries:

```markdown
# Weekly progress Summary — <Project Name>

**Week:** <YYYY-Www> (ISO week number)  
**Stage:** <N> (<Stage Name>)  
**Stage progress:** <XX>% → <YY>% (this week)

## Accomplishments This Week

- <Accomplishment 1>
- <Accomplishment 2>

## Planned vs. Actual

| Metric          | Planned | Actual  | Variance |
| --------------- | ------- | ------- | -------- |
| Tasks completed | <N>     | <M>     | <+/- X%> |
| Time spent      | <X> hrs | <Y> hrs | <+/- Z%> |

## Risks & Mitigations

| Risk          | Status  | Action Taken |
| ------------- | ------- | ------------ | ---------- | ------ |
| <Description> | <Active | Resolved     | Escalated> | <Plan> |

## Next Week Priorities

1. <Priority 1>
2. <Priority 2>
```

---

## Implementation Guidelines

### When to Create

| Project Phase | Action                                  |
| ------------- | --------------------------------------- |
| **Stage 1-3** | Optional (lightweight tracking only)    |
| **Stage 4+**  | **Mandatory** (full three-layer system) |

### Who Updates

| Layer        | Responsible        | Frequency          |
| ------------ | ------------------ | ------------------ |
| progress.md  | Session Lead       | Every milestone    |
| Session Logs | All agents         | Per session        |
| Checkpoints  | CTO / Session Lead | At each checkpoint |

### Tooling Integration

The system is designed to be tool-agnostic but supports integration with:

| Tool Type              | Integration Point                           |
| ---------------------- | ------------------------------------------- |
| **Time Tracking**      | Session log time tracking tables            |
| **Project Management** | Checkpoint JSON for Gantt updates           |
| **CI/CD**              | Checkpoint triggers for pipeline automation |
| **Reporting**          | progress.md parsing for dashboards          |

---

## Agent Systems Engineering (ASE) — Governance Layer

In addition to the three-layer monitoring system above, all pipelines operate under the **ASE Framework** — a 4-layer governance methodology for multi-agent coordination. The ASE templates are co-located with the monitoring templates:

| ASE Template                            | Layer               | Purpose                                    |
| --------------------------------------- | ------------------- | ------------------------------------------ |
| `stage-transition-summary.md`           | Context Engineering | Cross-stage context handoff                |
| `stage-transition-schemas.md`           | Harness Engineering | JSON schema contracts for gate enforcement |
| `schema-validation-spec.md`             | Harness Engineering | Automated validation rules                 |
| `inter-agent-communication-protocol.md` | Context + Harness   | Agent message formats and routing          |
| `mvc-context-profile.md`                | Context Engineering | Agent context window management            |
| `knowledge-transfer-protocol.md`        | RAG / Memory        | 3-tier learning loop                       |
| `rag-integration-blueprint.md`          | RAG / Memory        | Semantic retrieval architecture            |
| `adr-ase-001.md`                        | Governance          | ASE adoption decision record               |

**Stage 6 ASE Templates:**

| Template                      | Purpose                             |
| ----------------------------- | ----------------------------------- |
| `RED-TEAM-REVIEW.md`          | Adversarial review protocol         |
| `stage-transition-summary.md` | Stage 6-specific transition summary |

> **Template location:** `company/pipeline/mobile-development/templates/monitoring/` and `templates/stage-6-code-review/`
> **Full ASE specification:** See `company/library/overview/pipeline.md` § Agent Systems Engineering (ASE) Framework.

---

## Document History

| Version | Date       | Author     | Changes                              |
| ------- | ---------- | ---------- | ------------------------------------ |
| 1.0     | 2026-04-01 | CTO Office | Initial system definition            |
| 1.1     | 2026-04-29 | Lead Agent | Added ASE Framework governance layer |

---

## Related Documents

- **Pipeline Definition:** `pipeline.md`
- **Progress Sync Protocol:** See Section "Progress Sync Protocol" in pipeline.md
- **Project Directory Structure:** Refer to project root documentation for directory conventions
- **ASE Framework Templates:** `templates/monitoring/` (8 ASE templates + 3 base monitoring templates)
- **ASE Governance ADR:** `templates/monitoring/adr-ase-001.md`

---

**Compliance:** This system is mandatory for all Stage 4+ projects. Non-compliance must be documented in session logs with justification.
