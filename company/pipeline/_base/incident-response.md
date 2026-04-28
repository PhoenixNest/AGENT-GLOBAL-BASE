# Incident Response Model — Universal

| Field             | Value                                                              |
| ----------------- | ------------------------------------------------------------------ |
| **Document Type** | Operating instrument (Stage 11 Live Operations companion artifact) |
| **Scope**         | All product pipelines (mobile, web, backend, full-stack)           |
| **Owner**         | VP Platform (DRI) + CSO (security incidents)                       |
| **Effective**     | Day 1 of Stage 11 (first release ship)                             |
| **Cross-Refs**    | Base pipeline Stage 11 · `_base/release-checklist.md` row 12       |

---

## 1. Purpose

Stage 11 begins the moment the first release reaches users and never closes for the lifetime of the product. Real production traffic generates failure modes that no automated test or dogfood window can fully predict. This document defines the **operating contract** for responding to those failures: how incidents are classified, who is on the hook to respond, how authority for irreversible actions (rollback, customer comms, regulatory disclosure) is delegated, and how the company learns blamelessly from every Sev1 / Sev2.

The model is universal across product types. Product-specific specializations (e.g., mobile crash-rate SLOs, web CDN failover, backend capacity scaling triggers) live in the per-product `delta.md` Stage 11 sections.

---

## 2. Severity Ladder

Severity is assigned at the moment of incident declaration by the on-call DRI and may be raised (never silently lowered) by any C-suite member during the response. Customer-facing incidents are scored by user impact, not by internal effort to fix.

| Severity | Definition                                                                                                                                         | Response time (page → ack)              | Comms cadence                                                               | Postmortem required?         |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------- | :-------------------------------------------------------------------------- | :--------------------------- |
| **Sev1** | Total outage OR data loss OR active security breach OR widespread crash (≥ 1% of DAU) OR regulatory exposure                                       | ≤ 5 minutes (24×7)                      | Status page within 15 min; internal Slack every 30 min until mitigated      | **Mandatory**, blameless     |
| **Sev2** | Major feature degraded for ≥ 10% of users OR sustained latency SLO breach OR partial-outage on non-critical surface OR a Sev3 trending toward Sev1 | ≤ 15 minutes (business + on-call hours) | Internal Slack every hour until mitigated; status page only on user reports | **Mandatory**, blameless     |
| **Sev3** | Minor feature degraded OR isolated user reports OR cosmetic regression OR error budget burn rate elevated but not breaching                        | ≤ 4 business hours                      | Daily standup mention until closed                                          | Recommended (DRI discretion) |
| **Sev4** | Tracked observation; no active impact (e.g., an alert firing on a single host that is being replaced)                                              | Within sprint                           | None required                                                               | Not required                 |

**Auto-escalation rules.** A Sev2 unmitigated for > 2 hours auto-escalates to Sev1. A Sev3 with growth rate > 2× per hour auto-escalates to Sev2. The escalation is mechanical; the on-call DRI does not have to ask permission.

**Security incidents** (any unauthorized access, data exfiltration, credential leak, or active exploit) are **always** declared at Sev1 minimum; the CSO joins the response within the page-ack window.

---

## 3. On-Call Rotation

| Surface                                 | Primary on-call                                                   | Secondary on-call                                  | Escalation                                                                        |
| :-------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------- | :-------------------------------------------------------------------------------- |
| **Mobile (iOS/Android client)**         | Mobile platform on-call (rotating across iOS/Android engineers)   | VP Mobile                                          | CTO → CPO                                                                         |
| **Web (frontend + edge)**               | Web platform on-call (rotating across frontend engineers)         | Frontend Chapter Lead                              | VP Web/Backend → CTO                                                              |
| **Backend (services + data plane)**     | Backend service-on-call (per service; defined in service runbook) | Backend Chapter Lead                               | VP Web/Backend → CTO                                                              |
| **Infrastructure / SRE**                | SRE on-call                                                       | DevOps Lead                                        | VP Platform → CTO                                                                 |
| **Security**                            | Security Engineer on-call (24×7)                                  | Security Lead                                      | CSO (all Sev1 security incidents page CSO directly)                               |
| **Localization (release-language bug)** | Localization Engineer on-call                                     | Per-language linguist (assigned in release record) | CTO-L (only invoked when a translation defect is causing user-visible regression) |

**Rotation rules.**

1. **Coverage.** 24×7 for Sev1; business-hours-plus-on-call coverage for Sev2.
2. **Handoff.** Daily handoff at fixed times (per surface); written handoff log is mandatory; gaps are a P1 process defect.
3. **Backup.** Every primary on-call has a named secondary; the secondary owns the page if the primary does not ack within the response time SLO above.
4. **Compensation and humanity.** No on-call rotation exceeds one week consecutive. The on-call engineer is exempt from non-incident work for the duration of an active Sev1 / Sev2.
5. **Cross-team.** A Sev1 spanning multiple surfaces is jointly led by the surface DRIs; the **Incident Commander** (named at incident declaration) coordinates and is the single voice to leadership.

---

## 4. Authority and Delegation

The single most important rule of incident response: **the on-call DRI has authority to take any irreversible action required to mitigate a Sev1 / Sev2 without convening C-suite.** Convening burns minutes; mitigation buys minutes back.

| Action                                                | Authority                                                                               | Notification (informed-not-asked)                |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------- | :----------------------------------------------- |
| Roll back the most recent release                     | On-call DRI                                                                             | CTO + CPO within 15 min of execution             |
| Roll back to a release older than the most recent     | On-call DRI + Surface VP                                                                | CTO + CPO within 15 min of execution             |
| Take a customer-facing surface offline (status: down) | Incident Commander                                                                      | CPO (customer comms) + CSO (if security-related) |
| Disable a feature flag affecting paying customers     | On-call DRI                                                                             | CPO within 30 min                                |
| Issue a public status page update                     | Incident Commander (template-only updates); CPO sign-off required for narrative updates | —                                                |
| Rotate credentials / revoke tokens                    | Security Engineer on-call                                                               | CSO within 15 min                                |
| Notify regulators (data breach disclosure)            | CSO (jointly with future GC)                                                            | CEO informed at decision time                    |
| Reach out to law enforcement                          | CSO + CEO                                                                               | —                                                |

**The convene-the-panel anti-pattern.** Stage 11 explicitly does not require the C-suite full panel for any operational mitigation decision. The panel exists to retrospectively review postmortems (§6) and to set policy at QBRs (§7); they do not participate in the active fight.

---

## 5. Incident Lifecycle

```text
                  ┌─────────────┐
                  │ DETECT      │  alert / user report / synthetic monitor
                  └──────┬──────┘
                         │ ack within SLO
                  ┌──────▼──────┐
                  │ DECLARE     │  severity assigned; Incident Commander named; comms started
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │ MITIGATE    │  stop the bleeding (rollback, flag flip, capacity add)
                  └──────┬──────┘
                         │ user impact ends
                  ┌──────▼──────┐
                  │ RESOLVE     │  full restoration verified by synthetic + user-report decay
                  └──────┬──────┘
                         │ within 5 business days for Sev1, 10 for Sev2
                  ┌──────▼──────┐
                  │ POSTMORTEM  │  blameless review (§6); action items tracked to closure
                  └─────────────┘
```

**Resolve ≠ Postmortem.** Resolve closes the customer-impact window; the postmortem closes the learning loop. Both are required for Sev1 / Sev2.

---

## 6. Blameless Postmortem Template

Every Sev1 (mandatory) and Sev2 (mandatory) postmortem uses this template. The template lives at this same path; teams copy it into a per-incident document at `company/project/<project>/incidents/<incident-id>-postmortem.md`.

```markdown
# Postmortem — <incident title>

| Field               | Value                                                        |
| ------------------- | ------------------------------------------------------------ |
| Incident ID         | INC-YYYY-MM-DD-NNN                                           |
| Severity            | Sev1 / Sev2                                                  |
| Detected            | YYYY-MM-DD HH:MM TZ                                          |
| Declared            | YYYY-MM-DD HH:MM TZ (severity at declaration; later changes) |
| Mitigated           | YYYY-MM-DD HH:MM TZ                                          |
| Resolved            | YYYY-MM-DD HH:MM TZ                                          |
| Incident Commander  | <name>                                                       |
| Authoring engineers | <names>                                                      |
| Customer impact     | <DAU affected> · <duration> · <surfaces>                     |
| Revenue impact      | <quantified or "none observed">                              |
| Regulatory exposure | <yes/no; if yes, disclosure status>                          |

## 1. Summary

Three to five sentences that a CEO can read in 60 seconds.

## 2. Timeline

Chronological table. One row per material event (alert, ack, hypothesis, action, observation).

## 3. Root cause

Technical root cause (the change in the system that broke). Distinct from "trigger" (the request or condition that exposed it).

## 4. Contributing factors

Process, tooling, monitoring, on-call structure, dependency, knowledge gap. List with no judgment of intent.

## 5. What went well

Detection time, comms, mitigation choice, escalation. Reinforce the things to keep.

## 6. What went poorly

Delay, missed signal, wrong action, comms gap. State without naming individuals; use roles.

## 7. Where we got lucky

The unintentional saves. These are the highest-priority follow-ups: luck doesn't recur.

## 8. Action items

| ID   | Item     | Owner | Severity (P0–P3) | Target close date | Status |
| :--- | :------- | :---- | :--------------- | :---------------- | :----- |
| AI-1 | <action> | <DRI> | P0 / P1 / ...    | YYYY-MM-DD        | Open   |

## 9. Independent Challenge requirement

If this postmortem lists ≥ 5 action items, an Independent Challenge round per `_base/independent-challenge-template.md` is mandatory before the postmortem is filed as closed.
```

**Blameless discipline.** Postmortems use roles, not names, in §§6–7. Individual coaching happens in 1:1s, never in postmortems. Any retaliation against an engineer for an honest postmortem disclosure is a CHRO-investigated misconduct event.

**Action item tracking.** Action items are tracked in the project dashboard (`company/project/_dashboard.md`) until closed. P0 / P1 action items must close within 30 days; P2 within 90 days; P3 are accepted as backlog.

---

## 7. Error Budget and QBR Cadence

Per-quarter, each surface declares an **error budget** — the total acceptable user-visible downtime expressed as a percentage of the SLO window. The product-specific delta defines the surface's specific SLO targets; the universal contract is:

| Quarterly artifact                | Owner             | Cadence              |
| :-------------------------------- | :---------------- | :------------------- |
| Error budget proposal             | VP Platform + CTO | Quarter -1           |
| Error budget approval             | CPO + CTO + CSO   | Quarter -1, week 12  |
| Burn-rate review                  | VP Platform       | Weekly               |
| QBR (Quarterly Business Review)   | All C-suite       | End of quarter       |
| Error-budget overspend escalation | VP Platform → CTO | Within 24h of breach |

**The discipline.** When the error budget is overspent, the surface freezes new feature work and reallocates engineering capacity to reliability work until the next quarter. This rule has no exceptions and the on-call DRI has the authority to declare the freeze.

---

## 8. Documentation Hooks

| Touch point                            | Where the link lives                                     |
| :------------------------------------- | :------------------------------------------------------- |
| Stage 11 universal frame               | `_base/pipeline.md` Stage 11                             |
| Stage 10 release checklist row 12      | `_base/pipeline.md` "Live Ops Readiness" sign-off        |
| Per-surface specialization             | `<product>/delta.md` Stage 11 section                    |
| Per-incident postmortem                | `company/project/<project>/incidents/<id>-postmortem.md` |
| Action item burn-down                  | `company/project/_dashboard.md` Action Items section     |
| ≥ 5 action items challenge requirement | `_base/independent-challenge-template.md`                |

---

## 9. Document Version History

| Version | Date           | Author            | Changes                                                                                                                                                                |
| :------ | :------------- | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | VP Platform + CSO | Initial publication. Sev1–Sev4 ladder, on-call rotation per surface, authority delegation table, lifecycle diagram, blameless postmortem template, error budget + QBR. |
