---
name: aws-monitoring
description: "Design and operate AWS security monitoring — CloudWatch, GuardDuty, Security Hub, VPC Flow Logs, and CloudTrail — to achieve MTTD below 5 minutes for critical threats and maintain continuous compliance posture across all accounts."
version: "1.0.0"
---

| Competency                     | Description                                                             | Quality Criteria                                                                                                                                          |
| ------------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CloudWatch Security Monitoring | Configuring CloudWatch for security event detection and alerting        | Creates custom metrics and alarms for security-relevant events; achieves MTTD <5 minutes for critical threats; integrates with SNS/PagerDuty for alerting |
| GuardDuty Management           | Configuring and tuning Amazon GuardDuty threat detection                | GuardDuty enabled across all accounts and regions; finding false positive rate <10%; automated response to critical findings via EventBridge              |
| Security Hub Orchestration     | Managing AWS Security Hub for centralized security posture management   | Security Hub enabled with all available standards (CIS, PCI DSS, AWS Foundational); findings aggregated and prioritized; compliance score ≥95%            |
| VPC Flow Log Analysis          | Configuring and analyzing VPC Flow Logs for network security monitoring | Flow logs enabled on all VPCs; analysis detects unauthorized network access, data exfiltration patterns, and lateral movement; retention ≥365 days        |
| CloudTrail & Audit Logging     | Ensuring comprehensive API audit logging                                | CloudTrail enabled in all regions with log file validation; management and data events logged; logs shipped to SIEM; integrity verified                   |
| Incident Response Integration  | Connecting monitoring alerts to incident response workflows             | Automated alerting with runbook attachment; mean time to respond (MTTR) <15 minutes for critical alerts; post-incident documentation                      |

## Trigger

GuardDuty finding with severity ≥ 7.0

## Initial Response (0-5 minutes)

1. [ ] Acknowledge PagerDuty alert
2. [ ] Open GuardDuty console → navigate to finding
3. [ ] Record finding ID, type, severity, and description
4. [ ] Post initial notification to #security-incidents Slack channel

## Triage (5-15 minutes)

5. [ ] Identify affected resource (EC2 instance, IAM user, etc.)
6. [ ] Check if resource is production or non-production
7. [ ] Review recent API activity for affected resource (CloudTrail)
8. [ ] Determine if finding is true positive or false positive

## Containment (15-30 minutes) — True Positive

9. [ ] **EC2 compromise**: Isolate instance (move to quarantine security group)
10. [ ] **IAM compromise**: Disable IAM user/role, rotate credentials
11. [ ] **S3 exposure**: Block public access, review bucket policy
12. [ ] Create EBS snapshot for forensics (if EC2)
13. [ ] Preserve CloudTrail logs for investigation

## Investigation (30 minutes - 2 hours)

14. [ ] Determine attack vector and timeline
15. [ ] Identify all affected resources
16. [ ] Check for lateral movement
17. [ ] Determine data exposure (if any)

## Eradication & Recovery (2-4 hours)

18. [ ] Remove attacker access (delete unauthorized resources, keys)
19. [ ] Patch vulnerability that enabled compromise
20. [ ] Restore affected services from clean state
21. [ ] Verify eradication (re-scan with GuardDuty)

## Post-Incident (24-48 hours)

22. [ ] Write incident report
23. [ ] Conduct blameless post-mortem
24. [ ] Update runbook with lessons learned
25. [ ] Implement preventive controls
26. [ ] Update risk register

```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3** (Architecture)           | Infrastructure monitoring architecture designed; CloudWatch, GuardDuty, Security Hub, and CloudTrail integration specified |
| **Stage 5** (Development)            | Monitoring infrastructure provisioned via Terraform; all logging and alerting configured and tested                        |
| **Stage 6** (Code Review)            | Monitoring configuration reviewed; alert thresholds validated; runbooks verified                                           |
| **Stage 8** (Integrity Verification) | Monitoring systems verified operational; test alerts confirm end-to-end alerting pipeline                                  |
| **Stage 10** (Release Readiness)     | Monitoring coverage confirmed for all production infrastructure; incident response runbooks validated                      |

## Quality Standards

| Metric                      | Standard                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------- |
| **GuardDuty Coverage**      | GuardDuty enabled in 100% of AWS accounts and regions; all datasources (S3, EKS, EBS) enabled      |
| **CloudTrail Coverage**     | Multi-region trail with management and data events; log file validation enabled; 365-day retention |
| **VPC Flow Logs**           | Flow logs enabled on 100% of VPCs; ALL traffic type; 365-day retention                             |
| **Security Hub Compliance** | Security Hub enabled with CIS, AWS FSBP, and PCI DSS standards; compliance score ≥95%              |
| **MTTD (Critical)**         | Mean time to detect critical threats <5 minutes                                                    |
| **MTTR (Critical)**         | Mean time to respond to critical alerts <15 minutes                                                |
| **Alert Accuracy**          | <10% false positive rate on security alerts                                                        |
| **Runbook Coverage**        | 100% of alert types have documented runbooks; runbooks tested quarterly                            |
| **S3 Access Logging**       | 100% of S3 buckets have access logging enabled; logs retained for 365 days                         |


---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
```
