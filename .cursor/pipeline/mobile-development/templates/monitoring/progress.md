# Pipeline Progress — [Project Name]

## Current State

- **Stage:** <N> (<Stage Name>)
- **Stage Progress:** <XX>%
- **Platform Strategy:** <Android-only | iOS-only | Both Native | KMP Cross-Platform | Flutter Cross-Platform>
- **Status:** <Not Started | In Progress | Gate Review | Complete>
- **Last Updated:** <YYYY-MM-DD HH:MM:SS UTC>
- **Session ID:** <session-YYYYMMDD-HHMMSS>

## Stage Status

| Stage | Name                   | Status     | Entry Date | Exit Date | Artifacts Produced | User Approval? |
| ----- | ---------------------- | ---------- | ---------- | --------- | ------------------ | -------------- |
| 1     | Requirements           | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 2     | Design                 | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 3     | Architecture           | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 4     | Implementation Plan    | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 5     | Development            | ⚪ Pending | —          | —         | —                  | ❌ No          |
| 6     | Code Review            | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 7     | Automated Testing      | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 8     | Integrity Verification | ⚪ Pending | —          | —         | —                  | ❌ No          |
| 9     | i18n Engineering       | ⚪ Pending | —          | —         | —                  | ❌ No          |
| 10    | Release Readiness      | ⚪ Pending | —          | —         | —                  | ✅ Yes         |

## Current Stage Details (Stage <N>)

### Platform Progress (Stage 5 only)

> Populated only during Stage 5. Inactive tracks show "N/A."

```
Stage 5: Development
Overall: [XX]%
├── [Track C or Track A] — [Status]
├── [Track B] — [Status]
└── Track [X] unused capacity: [N] engineers → reassigned to [task]
```

### Cross-Track Dependencies (Stage 5 only)

> Shows blocking relationships between tracks.

| Dependency   | Blocking         | Blocked By | Status                                                    |
| ------------ | ---------------- | ---------- | --------------------------------------------------------- |
| [Dependency] | [What's blocked] | [Blocker]  | ☐ Not Started / 🟡 In Progress / ✅ Resolved / 🔴 Blocked |

### Completed

- [x] [Task 1]
- [x] [Task 2]

### In Progress

- [ ] [Current task being worked on]

### Pending

- [ ] [Upcoming task]
- [ ] Stage <N> Gate Review
- [ ] User approval

## Resume Instructions

**If interrupted, resume here:**

1. [Specific file to open]
2. [Specific section to complete]
3. [Next action to take]

## Session Log

| Session ID                | Date       | Duration | Accomplishments       | Next Steps   |
| ------------------------- | ---------- | -------- | --------------------- | ------------ |
| [session-YYYYMMDD-HHMMSS] | YYYY-MM-DD | [X min]  | [Accomplishment list] | [Next steps] |

## Risk Flags

| Risk          | Severity              | Mitigation | Owner  |
| ------------- | --------------------- | ---------- | ------ |
| [Description] | [Low / Medium / High] | [Plan]     | [Name] |

## Security Gate Failures

> Tracks CI/CD security gate failures with severity, owner, and SLA for remediation.

| Gate         | Failure Details       | Severity   | Owner  | SLA      | Resolved?    |
| ------------ | --------------------- | ---------- | ------ | -------- | ------------ |
| [SAST]       | [Finding description] | [P0/P1/P2] | [Name] | [X hrs]  | ☐ Yes / ☐ No |
| [DAST]       | [Finding description] | [P0/P1/P2] | [Name] | [X hrs]  | ☐ Yes / ☐ No |
| [Dependency] | [CVE details]         | [P0/P1/P2] | [Name] | [X hrs]  | ☐ Yes / ☐ No |
| [Pen Test]   | [Finding description] | [P0/P1/P2] | [Name] | [X days] | ☐ Yes / ☐ No |

## Technology Risk Register

> Tracks technology-specific risks: ADR compliance status, technology decision health, vendor/dependency vulnerabilities, platform SDK deprecation timelines.

| Risk                               | ADR Reference | Current Status                   | Likelihood     | Impact         | Mitigation | Owner  | Review Date |
| ---------------------------------- | ------------- | -------------------------------- | -------------- | -------------- | ---------- | ------ | ----------- |
| [e.g., KMP iOS target regression]  | ADR-NNN       | [Active / Monitoring / Resolved] | [Low/Med/High] | [Low/Med/High] | [Plan]     | [Name] | YYYY-MM-DD  |
| [e.g., Tink library CVE]           | TSD §4        | [Active / Monitoring / Resolved] | [Low/Med/High] | [Low/Med/High] | [Plan]     | [Name] | YYYY-MM-DD  |
| [e.g., Android API 24 deprecation] | —             | [Active / Monitoring / Resolved] | [Low/Med/High] | [Low/Med/High] | [Plan]     | [Name] | YYYY-MM-DD  |

## Security Metrics (Stage 5+)

> Tracked per platform during development.

| Metric                       | Android            | iOS                | KMP Shared         |
| ---------------------------- | ------------------ | ------------------ | ------------------ |
| SRD requirements implemented | X/Y                | X/Y                | X/Y                |
| SAST findings (open)         | P0:0, P1:0, P2:X   | P0:0, P1:0, P2:X   | P0:0, P1:0, P2:X   |
| Dependency vulnerabilities   | 0 critical, X high | 0 critical, X high | 0 critical, X high |
| Security review coverage     | XX%                | XX%                | XX%                |

## Translation Progress (Stage 9)

> Tracked during i18n Engineering. Expanded per-language detail with BLEU/TER scores.

| Language | Total Strings | TM Leverage % | Post-Editing % | BLEU Score | TER Score | Linguistic QA Pass Rate | Status         |
| -------- | ------------- | ------------- | -------------- | ---------- | --------- | ----------------------- | -------------- |
| English  | [N]           | —             | —              | —          | —         | —                       | ✅ Complete    |
| Chinese  | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                     | 🟡 In Progress |
| Japanese | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                     | ⚪ Pending     |
| Korean   | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                     | ⚪ Pending     |
| French   | [N]           | XX%           | XX%            | [0.XX]     | [XX%]     | XX%                     | ⚪ Pending     |

### Stage 9 Checkpoint Status

| Phase                              | Status                                       | Owner          | Output                       |
| ---------------------------------- | -------------------------------------------- | -------------- | ---------------------------- |
| String Extraction Readiness        | ☐ Not Started / 🟡 In Progress / ✅ Complete | Tomas Dvoracek | Pre-audit results            |
| Phase A: R&D Extraction            | ☐ Not Started / 🟡 In Progress / ✅ Complete | Tomas Dvoracek | STRING-EXTRACTION-HANDOFF.md |
| Phase B: TMS Translation           | ☐ Not Started / 🟡 In Progress / ✅ Complete | CTO-L          | Translation package          |
| Linguistic QA                      | ☐ Not Started / 🟡 In Progress / ✅ Complete | Linguists      | QA results per language      |
| Platform Resource Validation       | ☐ Not Started / 🟡 In Progress / ✅ Complete | CTO-L          | Resource file audit          |
| TRANSLATION-VERIFICATION-REPORT.md | ☐ Not Started / 🟡 In Progress / ✅ Complete | CTO-L          | Final report                 |
