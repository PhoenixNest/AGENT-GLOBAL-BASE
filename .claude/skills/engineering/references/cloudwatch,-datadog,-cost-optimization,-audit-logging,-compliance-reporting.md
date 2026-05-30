---
name: monitoring-audit
description: Audit the monitoring and alerting stack to ensure all production services have coverage for RED metrics (Rate, Errors, Duration), infrastructure health, and security events — producing a Monitoring Coverage Report for Stage 6 and Stage 8 reviews.
version: "1.0.0"
---

# Monitoring Audit

| Competency                | Description                                                       | Quality Criteria                                                                                                                |
| ------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| RED Metrics Audit         | Verify all services expose Request Rate, Error Rate, and Duration | Each service has CloudWatch/Datadog dashboards with all three RED metrics; alert thresholds defined for each                    |
| Infrastructure Coverage   | Verify all compute, database, and network resources are monitored | Zero unmonitored resources in production VPC; all ECS tasks, RDS instances, and ALBs have health alarms                         |
| Alert Quality Review      | Assess alert signal-to-noise ratio and action-ability             | Alerts without an associated runbook are flagged; alerts firing > 5 times/week without action are reviewed for threshold tuning |
| Security Event Monitoring | Verify CloudTrail, GuardDuty, and VPC Flow Logs are active        | CloudTrail enabled in all regions; GuardDuty findings routed to the security team; VPC Flow Logs retained ≥ 90 days             |

## Execution Guidance

### Monitoring Coverage Matrix

For each service in production, verify:

| Signal Type       | Tooling               | Alert Threshold Example                |
| ----------------- | --------------------- | -------------------------------------- |
| Request rate      | CloudWatch / Datadog  | Drop > 20% from baseline for 5 minutes |
| Error rate (5xx)  | ALB metrics           | > 1% over 2 minutes                    |
| P95 latency       | X-Ray / custom metric | > 2× SLO threshold for 5 minutes       |
| ECS task restarts | CloudWatch            | > 2 restarts in 10 minutes             |
| RDS CPU           | CloudWatch            | > 80% for 5 minutes                    |
| Disk space        | CloudWatch Agent      | > 85% utilized                         |

### Audit Output Format

The Monitoring Coverage Report must include:

1. **Coverage table:** Service → Signal → Covered (✅/❌) → Alert Name → Runbook Link
2. **Gap list:** All ❌ items with owner and remediation deadline
3. **Alert quality issues:** Over-firing or under-defined alerts
4. **Security event coverage:** CloudTrail/GuardDuty status per account/region
