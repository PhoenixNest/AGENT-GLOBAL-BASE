# Exception Rules — Quarterly Configuration

> **Owner:** CHRO
> **Frequency:** Once per calendar quarter

---

## R0 Defects (Immediate Halt + Escalation)

| Trigger                                      | Escalation         | Response Time   |
| -------------------------------------------- | ------------------ | --------------- |
| Legal/compliance violation (FCRA, GDPR)      | CHRO + CSO + Legal | Immediate       |
| Discriminatory assessment (four-fifths rule) | CHRO + CIO         | Immediate       |
| Audit trail tampering (hash chain gap)       | CHRO + CIO + CSO   | Immediate       |
| Candidate PII data breach                    | CHRO + CIO + CSO   | Within 4 hours  |
| Assessment model bias detected               | CHRO + CIO         | Immediate       |
| Background Check Service compromise          | CHRO + CSO         | Within 4 hours  |
| GDPR erasure failure                         | CHRO + DPO         | Within 24 hours |

## R1 Defects (Halt + Remediation)

| Trigger                                         | Escalation                    | Response Time |
| ----------------------------------------------- | ----------------------------- | ------------- |
| Assessment scoring error                        | CHRO + CIO                    | 4 hours       |
| Candidate data corruption                       | CHRO + CIO                    | 4 hours       |
| Background check Major discrepancy (unresolved) | CHRO + CSO                    | 24 hours      |
| Sourcing channel compromised (> 50% fraudulent) | CHRO                          | 24 hours      |
| Data contract validation failure                | CHRO + CIO                    | 5 minutes     |
| Human review unavailable within SLA             | CHRO + relevant Chief Officer | 48 hours      |

## Edge Cases (Automated Handling)

| Edge Case                                    | System Action                                                    |
| -------------------------------------------- | ---------------------------------------------------------------- |
| Candidate requests accommodation             | Flag for CHRO review; assessment adapted                         |
| Non-traditional background                   | NLP weights adjusted to reduce pedigree bias                     |
| Two candidates tie within 1% Composite Score | Advance both; vetting gate breaks tie                            |
| Hiring manager disputes role specification   | Log dispute; PSD unchanged until next quarterly cycle            |
| Candidate withdraws mid-pipeline             | Log reason; advance next-ranked candidate                        |
| Competing offer detected                     | Auto-accelerate offer timeline; add signing bonus if within band |

---

**Configured By:** CHRO
**Quarter:** [Qn YYYY]
**Audit Hash:** [SHA-256]
