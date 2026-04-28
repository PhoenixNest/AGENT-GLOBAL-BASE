# Dogfood Telemetry Report — Template

| Field             | Value                                                         |
| ----------------- | ------------------------------------------------------------- |
| **Document Type** | Stage 9.5 deliverable template                                |
| **Scope**         | All product pipelines (mobile, web, backend, full-stack)      |
| **Owner**         | VP Quality (DRI)                                              |
| **Effective**     | First Stage 9.5 entry post-publication                        |
| **Cross-Refs**    | Base pipeline Stage 9.5 · `_base/release-checklist.md` row 11 |

---

## 1. Purpose

Stage 9.5 sits between Integrity Verification (Stage 8) and Translation Production (Stage 9). It exists because pure automation has never been sufficient to find the failure modes that real users surface in the first hour of contact with a new build.

The Dogfood Telemetry Report is the artifact Stage 9.5 produces. It is filed at the end of the dogfood window (minimum five business days), proves that the build was actually exercised by humans, and routes any defects discovered through the standard P0–P3 system before the build is allowed to move into Stage 9.

---

## 2. Eligibility and Scope

| Field                      | Value                                                                                                             |
| :------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| Build under dogfood        | Specific build ID(s) and surface                                                                                  |
| Dogfood channel            | Internal Beta / TestFlight (iOS) / Play Internal Track (Android) / staging URL (web) / staging endpoint (backend) |
| Eligible participants      | All employees with platform access                                                                                |
| Mandatory participant pool | Engineers on the project team; CTO; CPO; CDO; CSO; VP Platform; VP Quality                                        |
| Minimum window             | 5 business days (per the universal mandate)                                                                       |
| Maximum window             | 10 business days; extension requires CTO approval                                                                 |
| Telemetry consent          | Explicit; participants are notified that their dogfood usage is logged                                            |
| Privacy scope              | No PII outside what production already collects; consent screen presented at first launch                         |

---

## 3. Required Telemetry

The following streams must be active for the dogfood window. If any stream is missing, the Stage 9.5 gate **does not pass**.

| Stream                                  | Purpose                                                              | Source                       |
| :-------------------------------------- | :------------------------------------------------------------------- | :--------------------------- |
| Crash / unhandled-exception reports     | Detect unhandled defects                                             | Crash reporter (per surface) |
| Active session count + duration         | Confirm the build was actually used                                  | Analytics SDK                |
| Feature usage (per PRD instrumentation) | Confirm new feature paths are exercised                              | Analytics SDK                |
| Performance counters                    | Catch regressions invisible to automated tests (cold-start, P95 TTI) | Performance SDK              |
| Error log capture                       | Capture warnings + handled errors that may indicate latent defects   | Logging pipeline             |
| Bug report channel                      | Single Slack channel + ticket form for participant-filed bugs        | Internal tooling             |
| Heatmap / session replay                | (Web/mobile UI builds only) Surface confusing UI flows               | Optional but recommended     |

---

## 4. Report Template

Author at `company/project/<project>/dogfood/<build-id>-dogfood-report.md`.

```markdown
# Dogfood Telemetry Report — Build <id>

| Field                        | Value                                               |
| :--------------------------- | :-------------------------------------------------- |
| Report ID                    | DOG-YYYY-MM-DD-<short slug>                         |
| Build ID(s)                  | <list>                                              |
| Surface                      | mobile (iOS / Android) / web / backend / full-stack |
| Dogfood channel              | <channel id>                                        |
| Window opened                | YYYY-MM-DD                                          |
| Window closed                | YYYY-MM-DD                                          |
| Active participants          | <count>                                             |
| Mandatory pool participation | <X of Y> (must be 100% to pass)                     |
| Total active session-hours   | <hours>                                             |
| DRI                          | VP Quality (or delegate)                            |
| Verdict                      | PASS / PASS-with-defects / FAIL                     |

## 1. Telemetry summary

| Metric                      | Value | Target / Threshold                      |
| :-------------------------- | :---- | :-------------------------------------- |
| Crash-free sessions rate    |       | ≥ 99.5% (P0 if below)                   |
| Sev1 (P0) defects observed  |       | 0 (mandatory; any > 0 = FAIL)           |
| Sev2 (P1) defects observed  |       | 0 unresolved (any unresolved P1 = FAIL) |
| New feature path coverage   |       | All PRD-instrumented paths fired ≥ 1×   |
| Cold-start P95 (mobile/web) |       | ≤ baseline + 100 ms                     |
| Backend API P99 latency     |       | ≤ baseline × 1.05                       |

## 2. Defects discovered

| Bug ID | Title | Severity (P0–P3) | Reporter | Owner | Status |
| :----- | :---- | :--------------- | :------- | :---- | :----- |

## 3. Qualitative observations

Free-form bullets from participants — UX confusion, copy issues, inconsistencies, surprises. Each bullet either has a tracked bug or is explicitly accepted as "not a defect" with rationale.

## 4. Participation audit

- Mandatory pool roster (CTO, CPO, CDO, CSO, VP Platform, VP Quality, project engineers): list with confirmation each used the build at least once.
- Total participants from broader employee pool: <count>.
- Sessions outside business hours (real-life usage signal): <count>.

## 5. Decisions and follow-ups

| Decision                                      | Rationale                                | Owner      |
| :-------------------------------------------- | :--------------------------------------- | :--------- |
| Proceed to Stage 9 (Translation Production)   |                                          | VP Quality |
| Block Stage 9; remediate and re-enter dogfood |                                          | VP Quality |
| Defer P2/P3 follow-ups                        | User authority per defect severity rules | CPO        |

## 6. Independent Challenge requirement

If the report defers ≥ 5 P2/P3 defects to backlog OR if any single participant reported ≥ 3 distinct defects, an Independent Challenge round per `_base/independent-challenge-template.md` is mandatory before the report is filed PASS.

## 7. Document version history

| Version | Date | Author | Changes |
```

---

## 5. Pass / Fail Conditions

The Stage 9.5 gate passes only when **all** of the following are true:

1. The dogfood window was at least five business days.
2. The mandatory participation pool (CTO, CPO, CDO, CSO, VP Platform, VP Quality, project engineering team) was 100% covered.
3. Crash-free sessions ≥ 99.5%.
4. Zero unresolved P0 defects in telemetry.
5. Zero unresolved P1 defects in telemetry.
6. All PRD-instrumented feature paths fired at least once.
7. Performance regressions within the surface guardrails (no P0 / P1 perf defect open).
8. The Dogfood Telemetry Report is filed and signed by VP Quality.

Failing any of (1)–(7) returns the build to the team that owns the failing condition; the dogfood window may be extended (≤ 10 business days) or the build may be returned to Stage 5 / Stage 7 for remediation, depending on the severity.

---

## 6. Document Version History

| Version | Date           | Author     | Changes                                                                                                                                             |
| :------ | :------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | VP Quality | Initial publication. 5-business-day minimum, 100% mandatory-pool coverage, crash-free ≥ 99.5%, zero P0/P1 unresolved, all instrumented paths fired. |
